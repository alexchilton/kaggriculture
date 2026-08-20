"""Re-solve every precomputed day against the plan we actually ship, in day order.

`kagg/search/solved_days.py` was solved on seed 11 against the **victor** tape, whose schedule the
agent played at the time. The agent has shipped Kawashigi's plan since 2026-08-13 and the routes were
never regenerated. Measured 2026-08-15, `--tape kawashigi --days 30`:

    precomputed ON (shipped)   d29 $139,025      work 2979  move 3036  idle 987
    PRECOMPUTED_ROUTES = {}    d29 $118,660      work 2895  move 3150  idle 957

So the stale routes are still worth **+$20,365** -- and `cover.PRECOMPUTED_MISSES` says only a
quarter of them are even being seated:

    day    stops in plan   skipped   SEATED   % used
     12               50        37       13      26%
     16               64        46       18      28%
     18               69        54       15      22%
     23               74        65        9      12%
     24               58        45       13      22%
     25               59        41       18      31%
     26               60        39       21      35%
     27               61        44       17      28%
     28               51        41       10      20%
     29               25        16        9      36%
    tot              571       428      143      25%

**Why a route solved for another player's plan works at all**, since that is the obvious objection:
the BOARD is identical in every game. `_initial_tile(x, y, board_size)` returns
`None if quadrant == "NW" else "LOCKED"` -- a pure function of coordinates -- and the only two
`random.Random` calls in `reference/kaggriculture.py` drive the weed spawn and the shop draw. So
geometry, distances and the shed position are shared; what a different plan changes is the JOB POOL
(which quadrants are bought and when, what is planted where, where pens sit, how big the crew is).
`_apply_precomputed` keeps partial matches, so we get the surviving quarter in a genuinely optimal
order and the greedy for the rest.

**Day order is not a convenience, it is a correctness requirement.** Each solved day changes the
next day's board, so a fixture dumped for d16 while d12 still runs the greedy describes a board the
shipped agent will never see. This script therefore installs each solved route into
`solved_days.py` before dumping the next day's fixture, which is what the old hand-run procedure
described in that file's docstring and never automated.

    python -u scripts/resolve_days.py --seconds 300
    python -u scripts/resolve_days.py --days 12,16 --seconds 60      # a quick smoke run

The file is rewritten in place. `git diff kagg/search/solved_days.py` is the review, and
`scripts/breakdown.py --tape kawashigi --days 30` is the judgement.
"""
import argparse
import datetime
import json
import pathlib
import pprint
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TARGET = REPO / "kagg" / "search" / "solved_days.py"
FIXTURES = REPO / "tests" / "fixtures"
#: **Every precomputed day, not a subset.** This was `(12, 16, 18, 23, 24, 25, 26, 27, 28, 29)` --
#: the ten days that existed when the script was written -- and `solved_days.py` has held all
#: eighteen of d12-d29 since 2026-08-15. `_write_solved` starts from `_load_solved()`, so the days
#: left out are preserved rather than deleted; they are simply never re-solved, and a day solved
#: against an older planner is exactly the stale artifact this script exists to remove. A run that
#: silently skips eight of eighteen days reads as a full regeneration and is not one.
DEFAULT_DAYS = tuple(range(12, 30))


def _run(cmd, log):
    """Run a step, streaming to the log AND to stdout, and fail loudly."""
    print(f"\n$ {' '.join(str(c) for c in cmd)}", flush=True)
    log.write(f"\n$ {' '.join(str(c) for c in cmd)}\n")
    log.flush()
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    log.write(out)
    log.flush()
    print(out, flush=True)
    if p.returncode != 0:
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(str(c) for c in cmd)}")
    return out


def _load_solved():
    """Read SOLVED_DAYS out of the module without importing `cover` and its whole graph."""
    ns = {}
    exec(compile(TARGET.read_text(), str(TARGET), "exec"), ns)      # noqa: S102 -- our own file
    return ns["SOLVED_DAYS"]


def _write_solved(solved, note):
    body = ["\n"]
    body.append("SOLVED_DAYS = {\n")
    for d in sorted(solved):
        body.append(f"    {d}: {{\n")
        for u in sorted(solved[d]):
            seq = solved[d][u]
            body.append(f"        {u}: {pprint.pformat(seq, width=10_000, compact=True)},\n")
        body.append("    },\n")
    body.append("}\n")
    TARGET.write_text(note + "".join(body))
    print(f"  wrote {TARGET.relative_to(REPO)} -- days {sorted(solved)}", flush=True)


HEADER = '''"""Days solved offline, as visit orders. Generated -- do not hand-edit.

Each day is `{{unit_index: [[tile, [op, ...]], ...]}}`, the exact assignment and order
`scripts/solve_day.py` found against `cover.py`'s own cost model. `cover._apply_precomputed`
seats them; a stop whose job today's board does not have is skipped and the rest still apply.

**Solved against the plan in `kagg/plan.py`, seed 11, tape kawashigi.** The board has no random
terrain -- `_initial_tile` is a pure function of coordinates and the env's only RNG drives the weed
spawn and the shop draw -- so geometry is identical in every game and these carry across seeds.
They do NOT carry across PLANS: the previous generation was solved against the victor tape and by
2026-08-15 only 143 of its 571 stops still matched a job our board had, the rest being silently
skipped. That stale quarter was still worth +$20,365 against no precomputation at all, which is the
measure of how much the geometry alone is worth and why regenerating was worth doing.

Regenerated {when} by `scripts/resolve_days.py`, IN DAY ORDER: each solved day changes the next
day's board, so every fixture is dumped with all earlier routes already installed. Re-run that
script rather than editing this file or dumping a fixture by hand.
"""
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", default=",".join(str(d) for d in DEFAULT_DAYS),
                    help="comma-separated, solved in the order given")
    ap.add_argument("--tape", default="kawashigi")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--seconds", type=float, default=300.0, help="solver budget PER DAY")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--log", default="data/logs/resolve_days.log")
    args = ap.parse_args()

    days = [int(d) for d in args.days.split(",") if d.strip()]
    logpath = REPO / args.log
    logpath.parent.mkdir(parents=True, exist_ok=True)

    solved = _load_solved()
    note = HEADER.format(when=datetime.date.today().isoformat())

    with logpath.open("w") as log:
        print(f"re-solving {days} against tape {args.tape}, seed {args.seed}, "
              f"{args.seconds}s each\nlog: {logpath}", flush=True)
        log.write(f"resolve_days {days} tape={args.tape} seed={args.seed} "
                  f"seconds={args.seconds}\n")
        for day in days:
            fixture = FIXTURES / f"day_{day}_{args.tape}.json"
            route = REPO / "data" / "logs" / f"route_d{day}_{args.tape}.json"
            route.parent.mkdir(parents=True, exist_ok=True)

            print(f"\n{'=' * 70}\n=== day {day}\n{'=' * 70}", flush=True)
            # 1. Dump the fixture the SHIPPED planner sees today, with every earlier day installed.
            _run([sys.executable, "-u", "scripts/dump_day_jobs.py", "--day", str(day),
                  "--tape", args.tape, "--seed", str(args.seed), "--module", args.module,
                  "--out", str(fixture.relative_to(REPO))], log)
            # 2. Solve it.
            _run([sys.executable, "-u", "scripts/solve_day.py", str(fixture.relative_to(REPO)),
                  "--seconds", str(args.seconds), "--dump-route", str(route.relative_to(REPO))],
                 log)
            # 3. Install it, so the NEXT dump sees the board this route produces.
            got = json.loads(route.read_text())
            solved[day] = {int(u): [(tuple(s["tile"]), tuple(o[0] for o in s["ops"]))
                                    for s in seq]
                           for u, seq in got.items()}
            _write_solved(solved, note)

    print(f"\ndone. review with:  git diff --stat {TARGET.relative_to(REPO)}")
    print(f"judge with:  PYTHONPATH=. python -u scripts/breakdown.py "
          f"--tape {args.tape} --module {args.module} --days 30")


if __name__ == "__main__":
    main()
