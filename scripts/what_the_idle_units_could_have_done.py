"""When a unit PASSes in the solver zone, was there work it could have reached?

The op histogram for d12-d29 (`data/logs/op_histogram.log`) says we PASS **482.5** unit-turns per
seat against カワシギ's **200.9**, and that he spends 480 MORE turns walking than we do. The gap is
entirely d12-d23 -- it stops at d24 where the live planner takes over from the solver -- and it is
worst on the days the crew is 13.

That reframes the standing-crop gap. It is not that the day is full and the far tiles cannot be
reached; it is that a third of the crew is standing still while crop sits ripe.

**But a PASS is not automatically waste.** A unit may be parked because everything ripe is already
claimed by another unit, or because the only remaining work is further away than the turns left in
the day. So this counts, for every PASS turn:

    reachable_ripe   tiles carrying `yield_units > 0` whose Chebyshev distance from the idle unit is
                     small enough that the unit could walk there, HARVEST, and still walk to a shed
                     access tile before the day ends. That is `2*d_tile + d_home + 1 <= turns_left`,
                     using the tile as the pivot rather than the unit's start, so it is an upper
                     bound on what one unit could do alone.
    claimed          how many of those tiles ANOTHER unit of ours harvests later the same day. A
                     tile someone else collects is not lost work, so it is reported separately and
                     must not be counted as an opportunity.
    thirsty          tiles with a crop that is not watered today -- the other thing an idle unit
                     could always be doing, and the input to the weed rule.

A PASS with zero unclaimed reachable ripe tiles and zero thirsty tiles is a correct PASS. Anything
else is the solver declining work it had the turns for.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
US = "alex chilton"
KAWA = "カワシギ"
SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]
DAYS = range(12, 24)


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def home(t):
    return min(cheb(t, s) for s in SHED)


def units(obs, seat):
    farms = (obs or {}).get("farms") or []
    if seat >= len(farms):
        return []
    f = farms[seat]
    out = [tuple(f["farmer"]) if f.get("farmer") else None]
    for h in (f.get("hands") or []):
        out.append(tuple(h) if h else None)
    return out


def board(obs, seat):
    """`([(y,x,units)], [(y,x)])` -- ripe crop tiles, and crop tiles not watered today."""
    farms = (obs or {}).get("farms") or []
    if seat >= len(farms):
        return [], []
    ripe, thirsty = [], []
    for y, row in enumerate(farms[seat].get("tiles") or []):
        for x, t in enumerate(row):
            if not isinstance(t, dict) or not t.get("crop"):
                continue
            u = int(t.get("yield_units", 0) or 0)
            if u > 0:
                ripe.append((y, x, u))
            if not t.get("watered_today", t.get("watered", False)):
                thirsty.append((y, x))
    return ripe, thirsty


def main(paths):
    tot = collections.Counter()
    per_day = collections.defaultdict(collections.Counter)
    seats = 0
    for p in paths:
        f = pathlib.Path(p)
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else (names.index(KAWA) if KAWA in names else 0)
        steps = r.get("steps") or []
        seats += 1

        # tiles OUR units harvest, per day, so a claimed tile is not called an opportunity
        harvested = collections.defaultdict(set)
        for t, step in enumerate(steps):
            if seat >= len(step):
                continue
            act = (step[seat] or {}).get("action") or {}
            pos = units((step[0] or {}).get("observation") or {}, seat)
            ops = [act.get("farmer")] + list(act.get("hands") or [])
            for i, op in enumerate(ops):
                if op and op[0] == "HARVEST" and i < len(pos) and pos[i]:
                    harvested[t // TPD].add(pos[i])

        for t, step in enumerate(steps):
            day, hour = t // TPD, t % TPD
            if day not in DAYS or seat >= len(step):
                continue
            act = (step[seat] or {}).get("action") or {}
            ops = [act.get("farmer")] + list(act.get("hands") or [])
            if not any(op and op[0] == "PASS" for op in ops):
                continue
            obs = (step[0] or {}).get("observation") or {}
            pos = units(obs, seat)
            ripe, thirsty = board(obs, seat)
            left = TPD - hour
            for i, op in enumerate(ops):
                if not (op and op[0] == "PASS") or i >= len(pos) or not pos[i]:
                    continue
                u = pos[i]
                tot["pass"] += 1
                per_day[day]["pass"] += 1
                reach = [(y, x, n) for y, x, n in ripe
                         if cheb(u, (y, x)) + home((y, x)) + 1 <= left]
                unclaimed = [c for c in reach if (c[0], c[1]) not in harvested[day]]
                th = [c for c in thirsty if cheb(u, c) + home(c) + 1 <= left]
                if reach:
                    tot["pass_with_reachable_ripe"] += 1
                    per_day[day]["pass_with_reachable_ripe"] += 1
                if unclaimed:
                    tot["pass_with_UNCLAIMED_ripe"] += 1
                    per_day[day]["pass_with_UNCLAIMED_ripe"] += 1
                    tot["units_on_the_table"] += sum(c[2] for c in unclaimed)
                if th:
                    tot["pass_with_reachable_thirsty"] += 1
                    per_day[day]["pass_with_reachable_thirsty"] += 1
                if not unclaimed and not th:
                    tot["pass_CORRECT"] += 1
                    per_day[day]["pass_CORRECT"] += 1

    n = max(1, seats)
    print(f"{seats} seats, days {DAYS.start}-{DAYS.stop-1}\n")
    print(f"{'day':>5}{'PASS':>9}{'reach ripe':>12}{'UNCLAIMED':>11}{'thirsty':>9}{'correct':>9}")
    for day in sorted(per_day):
        d = per_day[day]
        print(f"{day:>5}{d['pass']/n:>9.1f}{d['pass_with_reachable_ripe']/n:>12.1f}"
              f"{d['pass_with_UNCLAIMED_ripe']/n:>11.1f}"
              f"{d['pass_with_reachable_thirsty']/n:>9.1f}{d['pass_CORRECT']/n:>9.1f}")
    print()
    print(f"   PASS turns per seat                       {tot['pass']/n:>8.1f}")
    print(f"   ... with a reachable ripe tile            {tot['pass_with_reachable_ripe']/n:>8.1f}")
    print(f"   ... with an UNCLAIMED reachable ripe tile {tot['pass_with_UNCLAIMED_ripe']/n:>8.1f}")
    print(f"   ... with a reachable thirsty tile         "
          f"{tot['pass_with_reachable_thirsty']/n:>8.1f}")
    print(f"   ... nothing reachable: a CORRECT pass     {tot['pass_CORRECT']/n:>8.1f}")


if __name__ == "__main__":
    main(sys.argv[1:])
