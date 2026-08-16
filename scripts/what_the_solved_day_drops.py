"""On a SOLVED day, which jobs does the precomputed route fail to seat -- and are they waterings?

## Why this exists

`cover.cover` returns EARLY on any day in `PRECOMPUTED_ROUTES`:

    pre = _apply_precomputed(day, units, jobs, ...)
    if pre is not None:
        return pre

So on those days none of the greedy machinery runs. Not the `at_risk` pass order, not `REPAIR`,
not `COMPACT`. A job the solved route has no stop for goes to `_insert_leftovers`, which does a
cheapest FEASIBLE insertion into tours that are already built, and returns whatever would not fit.

The solved days start at **d12** on a three-quadrant board and **d9** on a four-quadrant one.
The strawberry deaths in live ladder games start at d12-d14. That is the coincidence this script
tests, and the mechanism it suspects is specific: the days were solved for a board carrying 34
strawberry tiles, and the melon fork puts 42 on it. Eight tiles with no solved stop, eight tiles
dying on d14.

## What it prints

Per day, from the first solved day on:

    jobs        how many jobs the planner offered
    seated      how many the precomputed route placed
    inserted    how many leftovers `_insert_leftovers` found room for
    DROPPED     how many it could not place -- these are simply not done that day
    of which    the dropped jobs that are a WATER, and the crop on the tile

A dropped WATER is a tile that goes a night unwatered. Two of those in a row is a weed
(`_daily_refresh_plants`), so a tile appearing here on consecutive days is a tile we are killing.

    python -u scripts/what_the_solved_day_drops.py --seed 11 --fork
"""
import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import melon_branch as _MB

DROPS = []          # (day, jobs, seated, inserted, dropped, [(tile, ops, crop), ...])


def instrument():
    """Wrap `cover.cover` so every call records what the precomputed path could not place."""
    from kagg.search import cover as C

    real = C.cover

    # `cover.plan` calls this POSITIONALLY through its `assign` alias, so the signature has to be
    # the real one rather than `**kw`.
    def wrapped(units, jobs, budget, depots=C.SHED, carry=None, supply=None, deliver=True,
                wanted=None, day=None, rush=False, due=None):
        jobs = list(jobs)
        pre = None
        if day in C.PRECOMPUTED_ROUTES:
            # Count seats WITHOUT the leftover pass, so seated and inserted separate cleanly.
            plan = C.PRECOMPUTED_ROUTES.get(day) or {}
            pool = {}
            for j in jobs:
                pool.setdefault((tuple(j.tile), tuple(o[0] for o in j.ops)), []).append(j)
            seated = 0
            for u_str, work in plan.items():
                if int(u_str) >= len(units):
                    continue
                for tile, ops in work:
                    key = (tuple(tile), tuple(ops))
                    if pool.get(key):
                        pool[key].pop()
                        seated += 1
            pre = seated
        out = real(units, jobs, budget, depots, carry, supply, deliver, wanted, day, rush, due)
        if pre is not None:
            work, left = out
            placed = sum(len(v) for v in work.values())
            DROPS.append((day, len(jobs), pre, placed - pre, list(left)))
        return out

    C.cover = wrapped


def crop_of(job):
    return getattr(job, "crop", None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005, help="the LADDER value")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--fork", action="store_true",
                    help="force the melon->strawberry fork open by dropping the opponent-melon "
                         "threshold to 0. This is the board the solved days were NOT solved for.")
    a = ap.parse_args()

    instrument()
    import json

    from scripts import breakdown as B

    # Built exactly as `breakdown.main` builds it -- same tape schedule, same economy, same shop
    # draw -- so the day this reports is the day the grid reports.
    replay, schedule, team = B.TAPES[B.DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    mod = B.load_agent_module(a.module)
    if a.fork:
        # The gate asks about the OPPONENT's melon; 0 makes every opponent qualify. Nothing else
        # changes, so the only difference downstream is our own crop mix.
        _MB.OPPONENT_MELON = 0

    def mine():
        agent = mod.make_agent(thin, 0, router=True)
        return lambda o, t: agent(o)

    opp = lambda: B.tape_policy(replay, team, 1)          # noqa: E731
    B.run(mine, opp, a.seed, a.weeds, stop_day=a.days,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))

    print(f"seed {a.seed}, weedSpawnChance {a.weeds}, module {a.module}\n")
    print(f"{'day':>4}{'jobs':>7}{'seated':>8}{'inserted':>10}{'DROPPED':>9}   dropped WATER tiles")
    for day, n, seated, inserted, left in DROPS:
        waters = [j for j in left if any(o[0] == "WATER" for o in j.ops)]
        tiles = " ".join(str(tuple(j.tile)) for j in waters[:8])
        print(f"{day:>4}{n:>7}{seated:>8}{inserted:>10}{len(left):>9}   "
              f"{len(waters)} water: {tiles}")

    dry = collections.Counter()
    for day, _n, _s, _i, left in DROPS:
        for j in left:
            if any(o[0] == "WATER" for o in j.ops):
                dry[tuple(j.tile)] += 1
    repeat = {t: c for t, c in dry.items() if c >= 2}
    print(f"\ntiles whose WATER was dropped on 2+ solved days: {len(repeat)}")
    for t, c in sorted(repeat.items(), key=lambda kv: -kv[1])[:20]:
        print(f"   {t}  dropped on {c} days")


if __name__ == "__main__":
    main()
