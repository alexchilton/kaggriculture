"""The crop still standing at the bell -- when was it planted, and how far out is it?

Alex, 2026-08-25: *"considering we know pretty much that at the end we cant get everything in --
probably because too far away -- should we be planting those in the first place a long way away
after day 24 or so?"*

$2,748 a season is standing unharvested at the bell (`what_we_grow_and_never_collect.py`). A PLANT
costs a seed and a turn, both paid up front, so a planting that cannot be collected is pure loss and
-- unlike the dawn drop -- it is decidable BEFORE the cost is incurred, from two things the agent
already knows: the day, and the distance from the tile to where the crew starts.

This prints, for every tile carrying yield at the end:

    planted_day        how late it went in
    distance           Chebyshev from `_default_spawn`, which is where every hand starts each day
                       (`reference/kaggriculture.py` `_end_of_day` resets `farm["farmer"]` to it)
    ripe_day           planted_day + CROPS[crop]["first_yield_day"]

against the same figures for tiles that WERE harvested. If the standing ones are late and far while
the collected ones are early or near, a cutoff of the form "no PLANT past day D beyond distance R"
is well founded and its parameters are readable straight off the table.

If they overlap, the loss is not about distance and a cutoff would refuse plantings that do pay.

    python -u scripts/should_we_plant_that_far_that_late.py --range 700 6
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _play(job):
    seed, opponent, module_name = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)

    board = len(env.state[0].observation["farms"][0]["tiles"])
    spawn = KG._default_spawn(board)
    # Every tile ever planted, and the last time we saw yield on it.
    ever = {}
    for t in range(30 * TPD):
        o0 = env.state[0].observation
        for y, row in enumerate(o0["farms"][0].get("tiles") or []):
            for x, cell in enumerate(row):
                if isinstance(cell, dict) and cell.get("kind") == "PLANT":
                    ever[(y, x)] = (cell.get("crop"), int(cell.get("planted_day", 0) or 0))
        a0 = me(o0, env.configuration)
        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": a0["market"]},
                  them(env.state[1].observation, env.configuration)])
        if env.done:
            break

    obs = env.state[0].observation
    standing, collected = [], []
    for y, row in enumerate(obs["farms"][0].get("tiles") or []):
        for x, cell in enumerate(row):
            if not isinstance(cell, dict) or cell.get("kind") != "PLANT":
                continue
            crop = cell.get("crop")
            spec = KG.CROPS.get(crop)
            if not spec:
                continue
            pd = int(cell.get("planted_day", 0) or 0)
            dist = max(abs(y - spawn[0]), abs(x - spawn[1]))
            left = int(spec.get("max_yield", 0)) - int(cell.get("yield_units", 0) or 0)
            ripe = pd + int(spec.get("first_yield_day", 0))
            row_ = (crop, pd, dist, ripe, left)
            (standing if left > 0 else collected).append(row_)
    return standing, collected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()

    seeds = list(range(a.range[0], a.range[0] + a.range[1]))
    jobs = [(s, a.opponent, a.module) for s in seeds]
    print(f"{len(jobs)} seasons vs {a.opponent}\n", flush=True)

    S, C = [], []
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for (seed, _o, _m), (st, co) in zip(jobs, pool.map(_play, jobs)):
            S += st
            C += co
            print(f"  seed {seed:<5} standing {len(st):>4} tiles   collected {len(co):>4}",
                  flush=True)

    def summarise(rows, label):
        if not rows:
            print(f"{label:<12} none")
            return
        n = len(rows)
        print(f"{label:<12}{n:>7}"
              f"{sum(r[1] for r in rows) / n:>16.1f}"
              f"{sum(r[2] for r in rows) / n:>12.1f}"
              f"{sum(r[3] for r in rows) / n:>12.1f}"
              f"{sum(r[4] for r in rows) / n:>12.1f}")

    print(f"\n{'group':<12}{'tiles':>7}{'mean planted_day':>16}{'mean dist':>12}"
          f"{'mean ripe':>12}{'units left':>12}")
    summarise(S, "STANDING")
    summarise(C, "collected")

    print(f"\nstanding tiles by planted_day x distance (the cutoff, if there is one)\n")
    grid = collections.Counter()
    for crop, pd, dist, ripe, left in S:
        grid[(pd, dist)] += 1
    days = sorted({k[0] for k in grid})
    dists = sorted({k[1] for k in grid})
    print(f"{'day':<6}" + "".join(f"{'d' + str(d):>6}" for d in dists))
    for pd in days:
        print(f"{pd:<6}" + "".join(f"{grid.get((pd, d), 0):>6}" for d in dists))

    late_far = sum(1 for c, pd, di, r, l in S if pd >= 24)
    print(f"\nstanding tiles planted on day 24 or later: {late_far} of {len(S)}")
    print("A cutoff is only justified if the STANDING rows are both later AND further than the")
    print("collected ones. If they overlap, refusing them would refuse plantings that do pay.")


if __name__ == "__main__":
    main()
