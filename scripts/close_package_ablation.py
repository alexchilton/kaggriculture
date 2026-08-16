"""Add the close-package deltas back ONE AT A TIME, and score each on win rate.

## Why

`fe7aad6` scored **1947.9** on the ladder. The next release added six behaviour changes aimed at
d29, shipped as one block, and scored **1384.8**. Today's two submissions still carry that block and
sit at 1406 and 1361. Routes are unchanged between the two builds, so the ~550 points are the block.

The block measured `+$2,246` on the season and `stranded 62 -> 16 units` -- on ONE seed, against the
tape, with no pool run and no win rate. That is selection on money, on a single sample, with eight
deltas at once: three rules this project already had, all broken in one release. This script is the
bisection that should have come first.

## Arms

`base` turns all six off, which is `fe7aad6`'s behaviour. Each `+NAME` arm turns exactly one back on.
`current` turns all six on and must reproduce today's build.

    NO_UPKEEP_ON_THE_LAST_DAY            router     no FEED/CARE on d29, executor and plan
    LAST_DAY_DEADLINE_WALK               agent      the closing walk is planned, not left to slack
    MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE  cover      a d29 stop keeps its seat when its ops shrink
    TRIM_A_TAIL_THAT_CANNOT_COME_HOME    cover      a tour gives up work it cannot deliver
    WALK_THE_LOAD_HOME_DAYS              agent      (10,) -> (10, 29)
    TRIM_HOME_DAYS                       cover      frozenset() -> {29}

`+melon_d3` is separate: it is not part of the block. It moves the melon->strawberry fork from
`d5 >= 7` to `d3 >= 9`, which is the rule that separates カワシギ's own 51 games perfectly (his
melon-heavy games top out at 8 opponent melon on d3; his strawberry-heavy ones start at 9, and the
classes MERGE by d5). Measured on the five losses it fires identically to the old rule, so expect a
null here -- it is included to confirm that rather than assume it.

## Method

**Each arm plays a FROZEN BUNDLE opponent, never another arm.** Three of the six flags live in
`cover` and `router`, which the private-module trick still shares, so two arms in one process would
overwrite each other's dials and both seats would play the second one loaded. A built submission
carries its own copies of every module, so it is immune. Verified directly on 2026-08-15:
`WHEAT->MELON 16` moved our board 12 -> 28 melon while the opponent's stayed byte-identical.

Both seats are played, because they are different boards and identical policies do not draw.

One OS process per game: the first run in a process differs from later ones.

Win rate is the score. The ladder is Elo -- a $43k win and a $4k win are worth the same.

    python -u scripts/close_package_ablation.py --seeds 24 --workers 8
"""
import argparse
import collections
import importlib
import importlib.util
import json
import pathlib
import statistics
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent

#: `flag -> (module, value when the delta is ON, value when OFF)`.
DELTAS = {
    "NO_UPKEEP_ON_THE_LAST_DAY":           ("kagg.search.router", True, False),
    "LAST_DAY_DEADLINE_WALK":              ("kagg.search.schedule_agent", True, False),
    "MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE": ("kagg.search.cover", True, False),
    "TRIM_A_TAIL_THAT_CANNOT_COME_HOME":   ("kagg.search.cover", True, False),
    "WALK_THE_LOAD_HOME_DAYS":             ("kagg.search.schedule_agent", (10, 29), (10,)),
    "TRIM_HOME_DAYS":                      ("kagg.search.cover", frozenset({29}), frozenset()),
}

#: Not part of the block. The fork rule read off カワシギ's 51 games.
MELON_D3 = {"MELON_YIELD_FROM_DAY": ("kagg.search.schedule_agent", 3, 5),
            "OPPONENT_MELON": ("kagg.search.schedule_agent", 9, 7)}

ARMS = ["base", "current"] + [f"+{k}" for k in DELTAS] + ["+melon_d3"]


def apply_arm(arm):
    """Set every dial for one arm. `base` is `fe7aad6`: all six deltas off."""
    mods = {name: importlib.import_module(name)
            for name in {m for m, _, _ in list(DELTAS.values()) + list(MELON_D3.values())}}
    # the fork rule stays at the SHIPPED setting unless this arm is testing it
    for flag, (mod, on, off) in MELON_D3.items():
        setattr(mods[mod], flag, on if arm == "+melon_d3" else off)
    for flag, (mod, on, off) in DELTAS.items():
        want = on if (arm == "current" or arm == f"+{flag}") else off
        setattr(mods[mod], flag, want)
    return mods


def one(seed, arm, seat, opponent):
    from kaggle_environments import make

    apply_arm(arm)
    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")

    sp = importlib.util.spec_from_file_location("opp", opponent)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json")), me=seat)
    for t in range(719):
        acts = [None, None]
        acts[seat] = me(env.state[seat].observation, t)
        acts[1 - seat] = mod.agent(env.state[1 - seat].observation, t)
        env.step(acts)
        if env.done:
            break
    fin = env.steps[-1]
    return dict(seed=seed, arm=arm, seat=seat,
                mine=fin[seat]["reward"], theirs=fin[1 - seat]["reward"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--arms", nargs="+", default=ARMS)
    ap.add_argument("--child", nargs=3, default=None)
    a = ap.parse_args()

    if a.child:
        print(json.dumps(one(int(a.child[0]), a.child[1], int(a.child[2]), a.opponent)))
        return

    seeds = list(range(1, a.seeds + 1))
    jobs = [(s, arm, seat) for arm in a.arms for s in seeds for seat in (0, 1)]
    print(f"{len(jobs)} games = {len(a.arms)} arms x {len(seeds)} seeds x 2 seats, "
          f"opponent {a.opponent}")
    print("base = fe7aad6 (all six close deltas OFF). Each +NAME turns exactly one back on.\n",
          flush=True)

    def child(job):
        s, arm, seat = job
        p = subprocess.run([sys.executable, "-u", __file__, "--child", str(s), arm, str(seat),
                            "--opponent", a.opponent],
                           capture_output=True, text=True, cwd=REPO,
                           env={**__import__("os").environ, "PYTHONPATH": "."})
        try:
            return json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            return dict(seed=s, arm=arm, seat=seat, failed=(p.stderr or p.stdout)[-160:])

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        rows = list(ex.map(child, jobs))

    by = collections.defaultdict(list)
    for r in rows:
        if r.get("failed"):
            print(f"  {r['arm']} seed {r['seed']} seat {r['seat']} FAILED {r['failed'][:120]}")
            continue
        by[r["arm"]].append(r)

    print(f"{'arm':<38}{'games':>7}{'WIN':>8}{'draw':>7}{'mean $':>11}{'vs base':>10}")
    base = by.get("base") or []
    base_win = sum(1 for r in base if r["mine"] > r["theirs"]) / max(1, len(base))
    out = []
    for arm in a.arms:
        rs = by.get(arm) or []
        if not rs:
            continue
        w = sum(1 for r in rs if r["mine"] > r["theirs"]) / len(rs)
        d = sum(1 for r in rs if r["mine"] == r["theirs"]) / len(rs)
        m = statistics.mean(r["mine"] for r in rs)
        print(f"{arm:<38}{len(rs):>7}{w:>8.1%}{d:>7.1%}{m:>11,.0f}{w - base_win:>+10.1%}")
        out.append((arm, w, m, len(rs)))
    json.dump([dict(arm=x[0], win=x[1], money=x[2], n=x[3]) for x in out],
              open(REPO / "data/logs/close_ablation.json", "w"), indent=1)

    if base:
        n = len(base)
        se = (0.25 / n) ** 0.5
        print(f"\nbaseline {base_win:.1%} on {n} games; 1 sd of a coin-flip duel is {se:.1%}, "
              f"so treat anything under {2*se:.1%} as noise.")
    print("Win rate is the score. The block measured +$2,246 of season money and lost ~550 rating "
          "points, which is what selecting on money does.")


if __name__ == "__main__":
    main()
