"""On an UNSOLVED day, how many jobs did the planner offer -- and how many did the router seat?

## Why this exists

`scripts/what_the_solved_day_drops.py` answers this for the precomputed days (d12+ on a
three-quadrant board). d6 is not one of them, so it runs the greedy, and the same question there
decides whether solving d6 could help at all:

    offered == seated       the router placed everything it was given. A better ROUTE cannot add a
                            water that was never a job. The defect is upstream, in the planner.
    offered  > seated       the router ran out of turns. An optimal tour has a real chance.

Measured against the d6 shortfall of `WATER 16/19` in both branch arms.

    python -u scripts/what_the_greedy_day_drops.py --arm melon --day 6
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.search import melon_branch as _MB          # noqa: E402

B3 = "data/seed_scripts/kawashigi/92466371.json"
A3 = "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"

CALLS = []          # (day, offered_ops, seated_ops, left_ops, tiles_left)


def ops_of(job):
    return tuple(o[0] for o in job.ops)


def instrument():
    """Patch BOTH planners.

    `cover.plan` picks its `assign` per day (`cover.py:1661`): `crew.cover` while
    `day < crew.ACTIVE_UNTIL_DAY` (8), `cover.cover` after. Patching only `cover.cover` measures
    nothing before d8 -- and reports one call in nine days, which is how this was caught.
    """
    from kagg.search import cover as C
    from kagg.search import crew as CREW

    CREW.cover = _make(CREW, CREW.cover, C)
    C.cover = _make(C, C.cover, C)


def _make(mod, real, C):
    def wrapped(units, jobs, budget, depots=C.SHED, carry=None, supply=None, deliver=True,
                wanted=None, day=None, rush=False, due=None):
        jobs = list(jobs)
        offered = collections.Counter(o for j in jobs for o in ops_of(j))
        out = real(units, jobs, budget, depots, carry, supply, deliver, wanted, day, rush, due)
        work, left = out
        seated = collections.Counter()
        for seq in work.values():
            for stop in seq:
                for o in ops_of(stop):
                    seated[o] += 1
        leftc = collections.Counter(o for j in left for o in ops_of(j))
        CALLS.append((day, offered, seated, leftc,
                      [tuple(j.tile) for j in left if "WATER" in ops_of(j)]))
        return out

    return wrapped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="melon")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--days", type=int, default=9)
    a = ap.parse_args()

    instrument()
    import breakdown as B
    import importlib
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (B3 if a.arm == "straw" else A3))
    opp = lambda: B.tape_policy(replay, TEAM, 1)                      # noqa: E731

    def ours():
        agent = SA.make_agent(sched, 0)
        return lambda o, t: agent(o)

    B.run(ours, opp, a.seed, a.weeds, stop_day=a.days,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))

    print(f"arm {a.arm!r}, seed {a.seed}, weeds {a.weeds}")
    print(f"cover.cover calls: {len(CALLS)}  by day: "
          f"{dict(collections.Counter(c[0] for c in CALLS))}\n")
    per_day = collections.defaultdict(lambda: [collections.Counter(), collections.Counter(),
                                               collections.Counter(), []])
    for day, off, seat, left, tiles in CALLS:
        if day is None:
            continue
        per_day[day][0].update(off)
        per_day[day][1].update(seat)
        per_day[day][2].update(left)
        per_day[day][3].extend(tiles)

    print(f"{'day':>4}{'WATER offered':>15}{'seated':>8}{'LEFT':>6}   unseated WATER tiles")
    for day in sorted(per_day):
        off, seat, left, tiles = per_day[day]
        print(f"{day:>4}{off['WATER']:>15}{seat['WATER']:>8}{left['WATER']:>6}   "
              + " ".join(str(t) for t in tiles[:10]))

    print("\nfull op table for the day of interest")
    for day in sorted(per_day):
        off, seat, left, _t = per_day[day]
        rows = sorted(set(off) | set(seat), key=lambda o: -off[o])
        print(f"\n  d{day}  " + "  ".join(f"{o} {off[o]}/{seat[o]}" for o in rows))


if __name__ == "__main__":
    main()
