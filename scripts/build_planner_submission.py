"""Bundle the covering planner into one self-contained `submission/main.py`.

`scripts/build_submission.py` copies a single dependency-free file verbatim, which is right for
`kagg/agents/contrarian.py` and useless here: the planner is four modules that import each other
plus a 64 KB schedule, and it is the agent that actually wins. Building the old way ships
contrarian and reports "submission verified" while none of the season's work is in the file --
which is exactly what happened on 2026-08-07, and is the `MEMORY.md` lesson about indirection
between the search space and the submission arriving in person.

## How it bundles

Each module's source is embedded **verbatim**, as an `r'''...'''` literal, and the round trip is
asserted before anything is written -- the builder parses its own output back and compares it to
the files on disk, byte for byte. A concatenated bundle was rejected: the four modules define
overlapping names (`ANIMALS`, `SHED`, `dist`) and flattening them would silently pick a winner.

At import the loader builds real module objects and installs them in `sys.modules` under their
real dotted names, in dependency order, so `from . import routines as R` resolves to the embedded
copy and never to anything on the Kaggle image. `kagg` and `kagg.search` are synthesised as
namespace packages with an empty `__path__`, so an accidental `import kagg.anything_else` fails
loudly instead of half-loading a repo that is not there.

None of the four modules touches the filesystem (no `__file__`, no `open`), which is what makes
this safe; the builder re-checks that rather than trusting this paragraph.

## The seat

`make_agent(schedule, me=...)` is bound to a seat, and a submission does not know its seat until
the first observation arrives. The entry point reads `obs["player"]` and builds lazily, one agent
per seat, and rebuilds at day 0 hour 0 so a second episode in the same process starts clean --
the agent carries a season of state (`pins`, `pen_for`, `planted`, `uncovered`) and reusing it
across games would be a slow, silent corruption rather than a crash.

Run: .venv/bin/python scripts/build_planner_submission.py
"""

import json
import pathlib
import sys

sys.path.insert(0, ".")

#: Dependency order, dotted name first. `schedule_agent` imports the three search modules; and
#: `routines` imports `kagg.economics.production` at module scope, inside `_crops_fertilizer_helps`,
#: to derive which crops fertilizer pays on. That import is the one that nearly shipped broken:
#: reaching it through the real `kagg/economics/__init__.py` pulls in `kagg.sim.town`, which reads
#: a JSON file off disk, and none of that exists on the Kaggle image. Bundling the leaf module and
#: stubbing the package it lives in keeps `routines.py` verbatim and never runs that `__init__`.
#: `production.py` itself imports only `typing` and the competition environment, which is by
#: definition present wherever this runs.
MODULES = (
    ("kagg.economics.production", "kagg/economics/production.py"),
    ("kagg.search.routines", "kagg/search/routines.py"),
    ("kagg.search.cover", "kagg/search/cover.py"),
    ("kagg.search.router", "kagg/search/router.py"),
    ("kagg.search.schedule_agent", "kagg/search/schedule_agent.py"),
)

#: Package stubs, created only where nothing real is already imported. Empty `__path__`, so an
#: import of anything NOT bundled fails loudly here instead of half-loading on the ladder.
PACKAGES = ("kagg", "kagg.economics", "kagg.search")

#: The schedule the planner runs. Thinned of the tape-only keys the agent never reads, so the
#: submission cannot accidentally depend on a replay it will not have.
#:
#: **2026-08-08: 90494364 -> 90976060. The shipped plan was calibrated for an economy that no longer
#: exists.** 90494364 was played on `townCenterSellInterval = 12`; the ladder runs 24 since the
#: 1.32.6 rebalance. Every `sells` row in it therefore assumes a town centre that drains the book
#: TWICE as fast as the real one, which is a mechanical explanation for the measurement in
#: `docs/the_shed_destroys_the_harvest_2026-08-08.md`: STRAWBERRY, MELON and WOOL driven to the $1
#: floor, wool below base on 558 of 719 turns, melon on 462. We were selling at a cadence the current
#: book cannot absorb.
#:
#: 90976060 is the same author on the CURRENT economy and is also his better game -- $128,518 against
#: 90494364's $110,820.
#:
#: **It also ends a measurement inconsistency worth naming.** Every fixture in the repo --
#: `scripts/handover.py`, `scripts/mirror`-style arms, `tests/test_the_shed_does_not_destroy_the_
#: harvest.py`, the reservation and price-aware measurements -- loads `TAPES["seb1326"]`, i.e.
#: 90976060, while this line shipped 90494364. So the local fixtures and the submission were
#: different agents, and their disagreement (mirror +2.9%, tape season -19%) was never about the sell
#: rule at all. One plan now, everywhere.
PLAN = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

TARGET = pathlib.Path("submission/main.py")

PREAMBLE = '''\
# Generated by scripts/build_planner_submission.py -- do not edit.
# Edit kagg/search/*.py and rebuild, so the submitted file cannot drift from the tested one.
"""Kaggriculture: a covering day planner running a fixed seasonal schedule.

Every module below is a verbatim copy of its file in the repository. The loader installs them
under their real dotted names before the entry point runs, so the code here behaves exactly as
it does in the repository and in the tests.
"""

import json
import sys
import types

_ORDER = {order!r}
_PACKAGES = {packages!r}
_SOURCES = {{}}
'''

EPILOGUE = '''

def _install():
    """Put the embedded modules into `sys.modules` under their real names, in dependency order.

    Package stubs are created only where nothing is already imported, so loading this file inside
    the repository does not blind the rest of the process to `kagg.agents` or `kagg.arena`. The
    leaf modules are always installed from the embedded copies -- byte-identical to the repo, so
    overwriting is a no-op there and is the whole point everywhere else.
    """
    for name in _PACKAGES:
        if name not in sys.modules:
            pkg = types.ModuleType(name)
            pkg.__path__ = []          # nowhere to search: an unbundled import fails loudly
            sys.modules[name] = pkg
        head, _, tail = name.rpartition(".")
        if head:
            setattr(sys.modules[head], tail, sys.modules[name])
    for name in _ORDER:
        parent_name, _, short = name.rpartition(".")
        mod = types.ModuleType(name)
        mod.__package__ = parent_name     # what makes `from . import routines` resolve
        sys.modules[name] = mod
        setattr(sys.modules[parent_name], short, mod)
        exec(compile(_SOURCES[name], "<" + name + ">", "exec"), mod.__dict__)
    return sys.modules["kagg.search.schedule_agent"]


_SCHEDULE = json.loads(_PLAN_JSON)
_SA = _install()
_AGENTS = {}


def agent(obs, config=None):
    """Module-level entry point.

    **This must be the LAST callable defined in this file.** `kaggle_environments` does not look
    for a function called `agent`; `get_last_callable` execs the module and takes
    `[v for v in namespace.values() if callable(v)][-1]`. A `make_agent` helper defined below
    this one was therefore picked as the entry point and invoked as `make_agent(observation,
    configuration)`, which died on `int('remainingOverageTime')` -- the observation being iterated
    as if it were the schedule. The builder now asserts this ordering.

    Built lazily because the seat is not known until an observation arrives, and rebuilt at the
    top of day 0 so a process that plays more than one episode does not carry a season of pins
    and pen reservations into the next one.
    """
    me = int(obs.get("player", 0) or 0)
    fresh = int(obs.get("day", 0) or 0) == 0 and int(obs.get("hour", 0) or 0) == 0
    if fresh or me not in _AGENTS:
        _AGENTS[me] = _SA.make_agent(_SCHEDULE, me, router=True)
    return _AGENTS[me](obs, config)
'''


def _check_imports(name, path, text):
    """Every `kagg` import in the module -- at any depth -- must land on something bundled.

    This is the check that was missing. A grep of the file's top-level imports said the planner
    needed nothing outside `kagg/search/`, and it was wrong: `routines._crops_fertilizer_helps`
    imports `kagg.economics.production` from inside a function body, and the bundle would have
    imported fine in the repo (where an editable install answers the import) and died on the
    ladder. AST, not grep, and function bodies included.
    """
    import ast

    bundled = {n for n, _ in MODULES} | set(PACKAGES)
    package = name.rpartition(".")[0]
    bad = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Import):
            wanted = [a.name for a in node.names if a.name.split(".")[0] == "kagg"]
        elif isinstance(node, ast.ImportFrom):
            root = package if node.level else (node.module or "")
            if node.level and node.module:
                root = f"{package}.{node.module}"
            if root.split(".")[0] != "kagg":
                continue
            # `from X import y` may name a module or an attribute; accept either reading.
            wanted = [f"{root}.{a.name}" if f"{root}.{a.name}" in bundled else root
                      for a in node.names]
        else:
            continue
        bad += [w for w in wanted if w not in bundled]
    if bad:
        raise SystemExit(
            f"{path}: imports {sorted(set(bad))}, which the bundle does not carry. "
            f"Add it to MODULES (and its package to PACKAGES) or the submission will die on Kaggle.")


def _literal(name, text):
    """Embed `text` verbatim as a raw triple-single-quoted literal, or refuse.

    Raw so no backslash in the source is reinterpreted, single-quoted because every docstring in
    these modules uses double quotes. Both assumptions are checked here rather than assumed: a
    quiet mangling would produce a file that imports and plays a subtly different game.
    """
    if "'''" in text:
        raise SystemExit(f"{name}: contains ''' and cannot be embedded raw")
    if text.rstrip("\n").endswith("\\"):
        raise SystemExit(f"{name}: ends in a backslash, which a raw literal cannot close")
    # No line continuation after the opening quotes: a raw literal keeps a trailing backslash
    # rather than swallowing the newline, which would prepend two stray characters to the module.
    return f"_SOURCES[{name!r}] = r'''{text}'''\n"


def build():
    sources = {}
    for name, path in MODULES:
        text = pathlib.Path(path).read_text()
        for forbidden in ("__file__", "open(", "read_text", "pathlib"):
            if forbidden in text:
                raise SystemExit(f"{path} touches the filesystem ({forbidden}); cannot bundle")
        _check_imports(name, path, text)
        sources[name] = text

    plan = json.loads(PLAN.read_text())
    thin = {d: {k: v for k, v in row.items() if k not in TAPE_ONLY} for d, row in plan.items()}

    out = [PREAMBLE.format(order=[n for n, _ in MODULES], packages=list(PACKAGES))]
    out += [_literal(name, sources[name]) for name, _ in MODULES]
    out.append(f"_PLAN_JSON = r'''{json.dumps(thin, indent=0)}'''\n")
    out.append(EPILOGUE)
    text = "".join(out)

    _assert_verbatim(text, sources, thin)
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_text(text)
    return TARGET


def _assert_verbatim(text, sources, thin):
    """Parse the generated file's own literals back and compare. Trust the round trip, not the code.

    This runs before the file is written, so a bundle that would have shipped a mangled module is
    never on disk to be submitted by mistake.
    """
    import ast

    tree = ast.parse(text)
    got = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
            continue
        target = node.targets[0]
        if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) \
                and target.value.id == "_SOURCES":
            got[ast.literal_eval(target.slice)] = node.value.value
        elif isinstance(target, ast.Name) and target.id == "_PLAN_JSON":
            got["__plan__"] = node.value.value

    for short, text_in in sources.items():
        if got.get(short) != text_in:
            raise SystemExit(f"{short}: embedded copy is not byte-identical to kagg/search/{short}.py")
    if json.loads(got.get("__plan__", "null")) != thin:
        raise SystemExit("the embedded schedule does not round-trip")


def standalone():
    """Import the built file from a directory with no repository in sight.

    This venv installs the repository as an EDITABLE package, which works through a `.pth` file
    that registers a finder on `sys.meta_path`. Neither `-I` nor emptying `sys.path` disables it,
    so the first version of this probe passed while quietly importing the real `kagg` -- a green
    check on exactly the thing it existed to rule out. The finder is removed by name before the
    bundle is loaded, which makes the process as blind to this repository as Kaggle is.
    """
    import subprocess
    import tempfile

    probe = (
        "import importlib.util, sys\n"
        # Strip the editable-install finder, then prove `kagg` is genuinely unreachable.
        "def _tag(f):\n"
        "    return (getattr(f, '__module__', '') + getattr(f, '__name__', '')\n"
        "            + type(f).__module__ + type(f).__name__).lower()\n"
        "sys.meta_path = [f for f in sys.meta_path if 'editable' not in _tag(f)]\n"
        # Drop only entries that actually contain a `kagg/` package. Matching the repo by NAME
        # also deleted this venv's site-packages, whose path contains "kaggriculture" too, and
        # took `kaggle_environments` down with it.
        "import os\n"
        "sys.path = [p for p in sys.path if not os.path.isdir(os.path.join(p or '.', 'kagg'))]\n"
        "try:\n"
        "    import kagg.arena\n"
        "    raise SystemExit('FAIL: the repository is still importable; probe proves nothing')\n"
        "except ImportError:\n"
        "    pass\n"
        f"spec = importlib.util.spec_from_file_location('sub', {str(TARGET.resolve())!r})\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        "installed = sorted(k for k in sys.modules if k == 'kagg' or k.startswith('kagg.'))\n"
        "for k in installed:\n"
        "    f = getattr(sys.modules[k], '__file__', None)\n"
        "    assert f is None, 'leaked a real file: ' + k + ' -> ' + str(f)\n"
        "assert callable(m.agent) and len(m._SCHEDULE) >= 29, len(m._SCHEDULE)\n"
        # Replicate `kaggle_environments.agent.get_last_callable` exactly: it execs the file and
        # takes the LAST callable in the namespace, not the one named `agent`. Getting this wrong
        # is silent -- the file imports, plays, and every game ends with a null reward.
        "ns = {}\n"
        f"exec(compile(open({str(TARGET.resolve())!r}).read(), 'sub', 'exec'), ns)\n"
        "last = [v for v in ns.values() if callable(v)][-1]\n"
        "assert last is ns['agent'], (\n"
        "    'the runtime would call ' + getattr(last, '__name__', repr(last))\n"
        "    + '(), not agent(): agent must be the LAST callable defined in the file')\n"
        "print('standalone import OK:', len(m._SCHEDULE), 'days;', ', '.join(installed))\n"
        "print('entry point OK: the last callable is agent()')\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = pathlib.Path(tmp) / "probe.py"
        path.write_text(probe)
        env = {"PATH": "/usr/bin:/bin", "HOME": str(pathlib.Path.home()), "PYTHONPATH": ""}
        r = subprocess.run([sys.executable, "-I", str(path)], cwd=tmp, env=env,
                           capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


#: Seed 11, weeds off, against Seb's replayed tape -- the season every number in `docs/` is
#: quoted on. `ours` is the gate; it must land to the dollar, because the environment is
#: deterministic given a seed and any drift at all means the bundle is not the measured code.
#:
#: The tape's own bank is recorded but NOT gated. It was $116,635 when the head-to-head was run
#: through `scripts/breakdown.py` and is $126,445 through this harness, on a season where our
#: side is bit-identical -- so the two harnesses differ in how they drive the REPLAY, not in how
#: they drive us. Gating on a number produced by a different harness would fail this build for a
#: property it is not testing. The bundle-versus-repo check below is the real equality test.
#: **Rebaselined 2026-08-08: 127,846 -> 71,894.** That figure was measured on env **1.32.2**, which
#: the ladder no longer runs. 1.32.6 halved the town centre's draw (`townCenterSellInterval` 12 -> 24)
#: and deleted the late-season demand ramp, so every bank in this project moved -- the same schedule
#: that banked $127,846 banks $63.5k on the new economy. Holding the old number gated every build
#: against an economy that does not exist.
#:
#: This is a tripwire, NOT the correctness check, and it is worth being explicit about that because
#: raising a reference to make a build pass is exactly how a regression gets shipped. The real test
#: is `ours == repo` on the line below: the bundle must reproduce the repo modules to the dollar.
#: That passed at $71,894 on both sides before this constant was touched, which is what makes the
#: rebaseline a record of a changed environment rather than a loosened gate.
#:
#: Also live in this build, and the reason the number is not simply "the old code on the new env":
#: `PRICE_AWARE_SELL_CAP = True` (see its docstring for the five-seed evidence).
#: **71,894 -> 58,104 on 2026-08-08** when `RESERVATION_SELL_CAP` was enabled. Recorded rather than
#: waved through: this fixture is DOWN 19% while the two that motivated the flag are up (mirror
#: 62,868 -> 64,667, handover +$2,822). Three fixtures, two up small, one down large -- the flag went
#: to the ladder on that mixed evidence deliberately, because the arena pool is saturated at 94.4%
#: and cannot discriminate a sell rule at all. If the ladder rating falls, this line is the first
#: thing to look at and the flag is the first thing to turn off.
#: **58,104 -> 57,595 on 2026-08-08** when the WHEAT feed reserve stopped counting `ripe_wheat`
#: (standing crop) as though it were feed. Flat on this fixture; the gain is elsewhere -- the herd now
#: matches the tape exactly (13 cows to 13, was 7), land parcel 3 moves d16 -> d12, and the mirror
#: goes 64,667 -> 69,228.
#: **57,595 -> 77,885 on 2026-08-08, +35%**, when `PLAN` moved off the 1.32.2-economy schedule
#: (90494364, `townCenterSellInterval = 12`) onto the same author's 1.32.6 game (90976060, interval
#: 24). The old plan's sell rows assumed a town centre draining the book twice as fast as the real
#: one; the new plan halves WOOL (230 -> 104) and cuts MELON (132 -> 96) -- the two steep `sq` price
#: curves we were driving to the $1 floor -- and puts the volume into MILK (179 -> 303), the one
#: product measured never to trade below base all season.
REFERENCE = {"seed": 11, "ours": 77885}

#: `actTimeout` is 1s per turn, but `remainingOverageTime` is a 60s bank for the whole episode and
#: disqualification happens only when the bank goes negative. So the constraint is total overage,
#: not the worst turn -- the day solve is always going to cost more than a second.
ACT_TIMEOUT, OVERAGE_BANK = 1.0, 60.0

#: **The local overage is not the number that matters, and reporting it alone shipped a
#: disqualification.** Submission 55352401 measured 2.8s of overage here and was charged 61.7s on
#: the ladder, which is not the ~2x a "slower worker" intuition suggests. The charge is
#: `max(0, t - 1)` per turn, so it is not linear in machine speed: a 3.8x slower box drags a whole
#: cohort of 0.3-0.9s turns across the one-second line AND charges for each of them. Same season,
#: same code, 22x the bill.
#:
#: 3.8x is measured, not assumed -- worst turn 7.39s on Kaggle against 1.96s here, on the same
#: agent. The gate charges at 6x so there is real headroom above the observed figure rather than a
#: margin chosen by feel, which is the mistake the first release made.
KAGGLE_SLOWDOWN = 6.0


def _season(policy, days=30, seed=None):
    """Play `policy` against Seb's tape and return (our bank, tape bank, per-turn seconds)."""
    import time

    from kaggle_environments import make

    from scripts.breakdown import TAPES, tape_policy

    replay, _schedule, team = TAPES["seb"]
    env = make("kaggriculture",
               configuration={"seed": seed or REFERENCE["seed"], "weedSpawnChance": 0.0})
    env.reset(2)
    opp = tape_policy(replay, team, 1)

    times = []
    for t in range(24 * days):
        if env.done:                      # the env closes the season itself; do not step past it
            break
        o0, o1 = env.state[0].observation, env.state[1].observation
        clock = time.perf_counter()
        a0 = policy(o0)
        times.append(time.perf_counter() - clock)
        a1 = opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    farms = env.state[0].observation["farms"]
    return round(float(farms[0]["money"])), round(float(farms[1]["money"])), times, team


def plays_a_real_game(seed=700):
    """Hand the FILE to `env.run`, the way the arena and Kaggle do, and require a real reward.

    Everything above drives `bundle.agent` directly, which is a different calling convention from
    the one the ladder uses: `env.run` picks the entry point itself, enforces `actTimeout`, and
    sets `reward = None` for an agent that errors, times out, or returns a malformed action. So a
    file can pass every check above and still score nothing -- which is exactly what happened, and
    `run_arena`'s own gate is what caught it. A null reward here is a build failure.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=True)
    env.run([str(TARGET), "starter"])
    final = env.steps[-1]
    reward, status = final[0]["reward"], final[0]["status"]
    ok = status == "DONE" and reward is not None and reward > 3000.0
    return ok, status, reward, final[1]["reward"]


def reproduce(days=30, verbose=True):
    """Play the BUILT FILE, and the repo modules, through one identical harness.

    The point is the word *built*. Every season number in `docs/` was produced by importing
    `kagg.search.schedule_agent` directly; none of them says anything about the artifact that
    gets uploaded. This plays the artifact, then plays the repo the same way, and requires the
    two to agree to the dollar -- which is a statement about the bundling, and is the only thing
    this script is in a position to prove.
    """
    import importlib.util
    import json as _json
    import pathlib as _pathlib

    spec = importlib.util.spec_from_file_location("_bundle", TARGET.resolve())
    bundle = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bundle)

    ours, tape, times, team = _season(bundle.agent, days=days)

    # The repo, driven the way every doc in this project drove it.
    from kagg.search import schedule_agent as SA

    # **`PLAN`, not a tape name.** This must be the SAME schedule the bundle embeds or the equality
    # check below compares two different agents and can never pass -- which is exactly what a
    # hard-coded `TAPES["seb"]` did the moment `PLAN` moved to 90976060.
    sched = {int(k): v for k, v in _json.loads(PLAN.read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    repo_agent = SA.make_agent(thin, 0, router=True)
    repo, repo_tape, _t, _team = _season(lambda o: repo_agent(o), days=days)

    overage = sum(max(0.0, s * KAGGLE_SLOWDOWN - ACT_TIMEOUT) for s in times)
    local = sum(max(0.0, s - ACT_TIMEOUT) for s in times)
    if verbose:
        print(f"tape season: bundle ${ours:,} vs {team} ${tape:,}  "
              f"(repo modules ${repo:,} vs ${repo_tape:,}; reference ${REFERENCE['ours']:,})")
        print(f"turn time over {len(times)} turns: worst {max(times) * 1000:.0f} ms, "
              f"mean {sum(times) / max(len(times), 1) * 1000:.0f} ms, "
              f"turns over {ACT_TIMEOUT:.0f}s: {sum(s > ACT_TIMEOUT for s in times)}")
        # Where the slow turns are matters more than how slow. The planner solves the whole day at
        # dawn and replays the committed tour for the other 23 hours, so cost concentrates on
        # hour 0 and grows with the crew and the tile count.
        slow = sorted(((s, i) for i, s in enumerate(times)), reverse=True)[:6]
        print("slowest turns: " + ", ".join(
            f"d{i // 24}h{i % 24} {s * 1000:.0f}ms" for s, i in slow))
        print(f"overage bank: {local:.1f}s here, {overage:.1f}s projected at {KAGGLE_SLOWDOWN:.0f}x "
              f"(measured ladder slowdown 3.8x), against a {OVERAGE_BANK:.0f}s bank")
        for f in (2, 3, 3.8, 5, 6, 8):
            o = sum(max(0.0, s * f - ACT_TIMEOUT) for s in times)
            print(f"    at {f:>3}x slower: worst {f * max(times):5.2f}s  "
                  f"turns over 1s {sum(s * f > ACT_TIMEOUT for s in times):3d}  "
                  f"overage {o:6.1f}s  {'ok' if o < OVERAGE_BANK else 'DISQUALIFIED'}")
    ok = (ours == repo) and (days < 30 or ours == REFERENCE["ours"])
    return ok, ours, tape, overage


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({len(path.read_text().splitlines())} lines, "
          f"{path.stat().st_size / 1024:.0f} KB)")
    ok, out = standalone()
    print(out)
    if not ok:
        print("BUILD FAILED: the bundle does not import on its own", file=sys.stderr)
        sys.exit(1)
    ok, status, reward, opp = plays_a_real_game()
    print(f"env.run vs starter: status {status}, reward "
          f"{'null' if reward is None else f'${reward:,.0f}'} vs "
          f"{'null' if opp is None else f'${opp:,.0f}'}")
    if not ok:
        print("BUILD FAILED: the runtime does not get a valid game out of this file",
              file=sys.stderr)
        sys.exit(1)

    days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    ok, ours, tape, overage = reproduce(days=days)
    if not ok:
        print("BUILD FAILED: the bundle does not reproduce the measured season", file=sys.stderr)
        sys.exit(1)
    if overage > OVERAGE_BANK:
        print(f"BUILD FAILED: {overage:.1f}s of projected overage at {KAGGLE_SLOWDOWN:.0f}x "
              f"against a {OVERAGE_BANK:.0f}s bank -- this is what a TIMEOUT looks like before "
              f"it happens", file=sys.stderr)
        sys.exit(1)
    print("submission verified")
