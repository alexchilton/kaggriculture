"""Base vs the drain-ranked sell release, across a seed list, against the frozen pool.

This is the measurement the change has been waiting on. Everything measured so far was on the two
TAPE seeds, which is one shop draw each -- and `how_much_does_the_draw_move_us.py` put the draw at
$72,008 of spread, so a $2,511 result on one draw is inside the noise of the thing that was NOT
controlled.

The first attempt at this ran locally through `kagg.arena.evaluate` and died with
`BrokenProcessPool` -- ten workers, each holding a full env plus the bundled plan. Two things are
different here:

- **`--workers` defaults to 4, not 10.** The pool blew up on memory, not on logic.
- **Rows are written and flushed as each game finishes.** A run that only writes at the end loses
  everything when it is killed, which has already happened once on this box for 29,568 seasons.

`mirror` is deliberately NOT in the default opponent list. `_build` resolves MIRROR by rebuilding
the CANDIDATE, and the candidate here is a schedule agent rather than a heuristic parameter dict,
so a mirror row would silently measure something else. A mirror is 50% by construction anyway.

    python -u scripts/the_sell_change_across_seeds.py --range 700 712 \
        --out data/logs/sell_across_seeds.csv | tee data/logs/sell_across_seeds.log
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
DEFAULT_OPPONENTS = ("wheat_only", "strawberry", "cow_heavy", "carrot_hinge", "contrarian")


def _our_agent(module_name, seat):
    """The shipped agent, built exactly as `build_planner_submission` builds it."""
    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}
    return SA.make_agent(sched, seat, router=True)


TAPES = {"kawa": ("data/seed_scripts/kawa_2026-08-24/97466318.json", "カワシギ")}


def _play(job):
    """One seating of one seed against one opponent. Returns (ours, theirs)."""
    module_name, opponent, seed, swapped = job
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build

    seat = 1 if swapped else 0

    # **A tape opponent, not a heuristic.** The pool is nine variants of our own heuristic plus
    # `contrarian`; the field on the ladder submits fixed 720-turn scripts. A sell-side change is
    # judged by who is competing for the same book, and a scripted opponent sells on a schedule a
    # heuristic never reproduces. His actions are a fixed script, so they replay on any seed.
    if opponent.startswith("tape:"):
        path, who = TAPES[opponent.split(":", 1)[1]]
        rec = json.loads((REPO / path).read_text())
        steps = rec["steps"]
        names = (rec.get("info") or {}).get("TeamNames") or []
        his = names.index(who) if who in names else 0
        cfg = dict(rec.get("configuration") or {})
        cfg.pop("seed", None)

        env = make("kaggriculture", configuration=dict(cfg, seed=int(seed)), debug=False)
        env.reset(2)
        me = _our_agent(module_name, seat)
        for t in range(30 * TPD):
            o = env.state[seat].observation
            a = me(o, env.configuration)
            at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
            at = at if isinstance(at, dict) else {}
            n_us = len(o["farms"][seat].get("hands") or [])
            n_them = len(o["farms"][1 - seat].get("hands") or [])
            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n_them],
                     "market": at.get("market") or []}
            env.step([mine, yours] if seat == 0 else [yours, mine])
            if env.done:
                break
        farms = env.state[0].observation["farms"]
        return (float(farms[seat]["money"]), float(farms[1 - seat]["money"]))

    me = _our_agent(module_name, seat)
    them = _build(OPPONENTS[opponent], None)
    pair = (them, me) if swapped else (me, them)

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.run(list(pair))
    final = env.steps[-1]
    return (float(final[seat]["reward"]), float(final[1 - seat]["reward"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modules", default="sa_base,schedule_agent")
    ap.add_argument("--seeds", default=None, help="comma-separated seed list")
    ap.add_argument("--range", nargs=2, type=int, default=None, metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponents", default=",".join(DEFAULT_OPPONENTS))
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="data/logs/sell_across_seeds.csv")
    args = ap.parse_args()

    if args.seeds:
        seeds = [int(x) for x in args.seeds.split(",")]
    elif args.range:
        seeds = list(range(args.range[0], args.range[0] + args.range[1]))
    else:
        seeds = list(range(700, 712))
    modules = args.modules.split(",")
    opponents = args.opponents.split(",")

    jobs = [(m, opp, s, sw)
            for m in modules for opp in opponents for s in seeds for sw in (False, True)]
    print(f"{len(modules)} arms x {len(opponents)} opponents x {len(seeds)} seeds x 2 seatings "
          f"= {len(jobs)} games, {args.workers} workers")
    print(f"seeds {seeds}")
    print(f"rows -> {args.out}\n", flush=True)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("module,opponent,seed,swapped,ours,theirs,win\n")
    fh.flush()

    tally = collections.defaultdict(lambda: [0, 0, 0, 0.0])   # module -> [w, d, n, money]
    per_opp = collections.defaultdict(lambda: [0, 0, 0.0])    # (module, opp) -> [w, n, money]
    per_seed = collections.defaultdict(lambda: [0, 0, 0.0])   # (module, seed) -> [w, n, money]
    clock = time.perf_counter()
    done = 0

    def record(job, ours, theirs):
        m, opp, s, sw = job
        win = 1 if ours > theirs else 0
        fh.write(f"{m},{opp},{s},{int(sw)},{ours:.0f},{theirs:.0f},{win}\n")
        fh.flush()
        t = tally[m]
        t[0] += win
        t[1] += int(ours == theirs)
        t[2] += 1
        t[3] += ours
        for d, k in ((per_opp, (m, opp)), (per_seed, (m, s))):
            d[k][0] += win
            d[k][1] += 1
            d[k][2] += ours

    if args.workers > 1:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            for job, (ours, theirs) in zip(jobs, pool.map(_play, jobs)):
                record(job, ours, theirs)
                done += 1
                if done % 10 == 0:
                    print(f"  {done}/{len(jobs)}  {time.perf_counter() - clock:.0f}s", flush=True)
    else:
        for job in jobs:
            ours, theirs = _play(job)
            record(job, ours, theirs)
            done += 1
            print(f"  {done}/{len(jobs)} {job} ours {ours:,.0f} theirs {theirs:,.0f}", flush=True)

    fh.close()

    print(f"\n{'arm':<16}{'win':>8}{'draw':>8}{'games':>8}{'mean ours':>13}")
    for m in modules:
        w, d, n, money = tally[m]
        print(f"{m:<16}{w / max(1, n):>7.1%}{d / max(1, n):>8.1%}{n:>8}{money / max(1, n):>13,.0f}")

    print(f"\n{'opponent':<16}" + "".join(f"{m:>22}" for m in modules))
    for opp in opponents:
        cells = []
        for m in modules:
            w, n, money = per_opp[(m, opp)]
            cells.append(f"{w / max(1, n):>10.0%}{money / max(1, n):>12,.0f}")
        print(f"{opp:<16}" + "".join(cells))

    print(f"\n{'seed':<16}" + "".join(f"{m:>22}" for m in modules))
    for s in seeds:
        cells = []
        for m in modules:
            w, n, money = per_seed[(m, s)]
            cells.append(f"{w / max(1, n):>10.0%}{money / max(1, n):>12,.0f}")
        print(f"{str(s):<16}" + "".join(cells))

    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
