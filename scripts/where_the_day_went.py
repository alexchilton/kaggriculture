"""Per-day op counts for both seats of a downloaded replay.

Answers one question the season totals cannot: *when* does an op-count gap open.
"we water 209 more times than he does" is a season number, and a season number cannot tell a
uniform +7/day from a cliff at d20. The fix for those two is not the same fix.

Ops are counted from the ACTION stream, which is correct for unit ops (one action = one op
attempt) and wrong for market orders (the agent re-posts an order every turn -- see
`kagg/analysis/fills.py` and `feedback_offers_are_not_fills`). Market rows are therefore not
printed here.

    python -u scripts/where_the_day_went.py data/seed_scripts/ladder_2026-08-17/93839424.json
    python -u scripts/where_the_day_went.py <files...> --ops WATER,HARVEST,PLANT
"""

import argparse
import collections
import json
import pathlib
import sys

#: Tour shape, not work. Counted separately so a day that ran out of TURNS can be told from a day
#: that ran out of JOBS -- opposite diagnoses off the same missing op.
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}

DEFAULT_OPS = ("WATER", "HARVEST", "PLANT", "FEED", "CARE")


def seat_of_us(replay, me="alex chilton"):
    names = replay["info"]["TeamNames"]
    return names.index(me) if me in names else 0


def by_day(replay, seat):
    """`{day: Counter(op)}` plus `{day: bank}` at the day's last hour."""
    ops = collections.defaultdict(collections.Counter)
    bank = {}
    for step in replay["steps"]:
        obs = step[seat]["observation"] if seat < len(step) else None
        if obs is None:
            continue
        # `player` is only on the seat's own observation; day/hour are shared.
        day = obs.get("day")
        if day is None:
            continue
        act = step[seat].get("action") or {}
        units = [act.get("farmer") or []] + list(act.get("hands") or [])
        for u in units:
            if not u:
                ops[day]["IDLE"] += 1
                continue
            op = u[0]
            ops[day]["MOVE" if op in MOVES else op] += 1
        money = (obs.get("farms") or [{}])[0].get("money")
        if money is None:
            money = (obs.get("private") or {}).get("money")
        if money is not None:
            bank[day] = money
    return ops, bank


def report(path, ops_wanted, me="alex chilton"):
    replay = json.loads(pathlib.Path(path).read_text())
    us = seat_of_us(replay, me)
    them = 1 - us
    opp = replay["info"]["TeamNames"][them]
    rew = replay["rewards"]

    ours, our_bank = by_day(replay, us)
    theirs, their_bank = by_day(replay, them)

    print(f"\n=== {pathlib.Path(path).stem}  us ${rew[us]:,.0f}  vs  {opp} ${rew[them]:,.0f} "
          f" ({'WIN' if rew[us] > rew[them] else 'LOSS'} by ${abs(rew[us]-rew[them]):,.0f}) ===")
    head = "day " + " ".join(f"{o[:5]:>13}" for o in ops_wanted) + f"{'PASS':>13}"
    print(head)
    print("    " + " ".join(f"{'us/them':>13}" for _ in ops_wanted) + f"{'us/them':>13}")
    tot = collections.Counter()
    for day in sorted(set(ours) | set(theirs)):
        cells = []
        for o in ops_wanted:
            a, b = ours[day][o], theirs[day][o]
            tot[o] += a - b
            cells.append(f"{a:>6}/{b:<6}")
        a, b = ours[day]["PASS"], theirs[day]["PASS"]
        cells.append(f"{a:>6}/{b:<6}")
        print(f"{day:>3} " + " ".join(cells))
    print("tot " + " ".join(
        f"{sum(ours[d][o] for d in ours):>6}/{sum(theirs[d][o] for d in theirs):<6}"
        for o in ops_wanted))
    return {o: tot[o] for o in ops_wanted}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+")
    p.add_argument("--ops", default=",".join(DEFAULT_OPS))
    p.add_argument("--me", default="alex chilton")
    a = p.parse_args()
    ops = tuple(o.strip().upper() for o in a.ops.split(","))
    for f in a.files:
        report(f, ops, a.me)


if __name__ == "__main__":
    sys.exit(main())
