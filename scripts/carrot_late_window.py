#!/usr/bin/env python3
"""Put CARROT in the schedule's late plant window, and in the sells row so it can be sold.

`data/seed_scripts/victor/schedule.json` is NOT git-tracked, so every change to it has to be a
script or it is invisible and unrepeatable. Run with `--apply` to write, without to preview.

WHY the late window and not a swap
----------------------------------
Every earlier carrot arm (`docs/carrot_swap_2026-08-12.md`) substituted carrot for wheat mid-season
and correctly lost: at base prices wheat is $140/tile against carrot's $120. That is the wrong
question. Carrot's `max_yield_day` is 3 against wheat's 4, so `router.plant_prize` already ranks
them the other way once the season runs out of room:

    day            d20  d21  d22  d23  d24  d25  d26  d27  d28
    WHEAT           75   75   75   75   75   75   50   25    0
    CARROT          70   70   70   70   70   70   70   35    0

The crossover is d26. カワシギ (#1, 15-1 across 16 downloaded games) plants carrot -- and only
carrot -- from d21 to d26 in every one of them, buying the seed on d3/d6 and holding it for
eighteen days (`docs/kawashigi_one_board_2026-08-13.md`).

So this is additive, on ground that is being cleared anyway. `router._best_replant_crop` picks by
`plant_prize`, so offering both crops in the budget yields wheat through d25 and carrot from d26
without this script having to hard-code the changeover.

The second half matters as much as the first: **CARROT appears in no sells row in the shipped
schedule**, and that alone is what made the previous 384-game sweep meaningless -- carrot reached
the shed and never left it. The point is not that carrot outsells wheat. It is that by d28 we are
dumping 60 wheat and by d29 another 144 into a book we have already flattened, while carrot's book
has not been touched all season.
"""
import argparse
import collections
import json
import pathlib
import sys

PLAN = pathlib.Path("data/seed_scripts/victor/schedule.json")

#: The days whose plantings become carrot.
#:
#: **d26 alone was measured and produced ZERO carrot fills** -- the fourth invalid carrot arm in this
#: project, and for a new reason. A carrot sown on d26 reaches `max_day` 3 on d29, so `HARVEST` is
#: first offered on the last day of the season; it landed in the shed with no turn left to sell it
#: (`harvest d29 15->25`, `CARROT` absent from `fills.py` entirely, season -$1,401).
#:
#: `plant_prize` puts the wheat/carrot crossover at d26 and that is why d26 was tried first. The
#: prize function is right about revenue per tile at BASE price and blind to the thing that decides
#: it: by d28-d29 we dump 60 then 134 wheat into a book we have flattened to $42, while carrot's
#: book has not been touched all season. That is why the leader starts at d21 and not at the
#: crossover -- the late crop has to be harvestable AND sellable, and only the earlier window is
#: both.
CARROT_DAYS = (23, 24, 25, 26)

#: A carrot sown on day D is harvestable on D+3, so the earliest planting above lands in the shed on
#: d26. The sells row is a quota, not a promise, so this is sized at tiles times `max_yield` 4 and
#: spread over every day the crop can actually reach a book -- selling is the half that has failed
#: every previous time.
SELL_DAYS = (26, 27, 28, 29)


def rows_of(sched):
    return sched["days"] if isinstance(sched, dict) and "days" in sched else sched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=pathlib.Path, default=PLAN)
    ap.add_argument("--apply", action="store_true", help="write the file; otherwise preview only")
    args = ap.parse_args()

    sched = json.loads(args.plan.read_text())
    rows = rows_of(sched)

    moved = 0
    for day in CARROT_DAYS:
        row = rows.get(str(day))
        if not row:
            continue
        plants = row.get("plants") or []
        n = sum(1 for c in plants if c == "WHEAT")
        if not n:
            continue
        row["plants"] = ["CARROT" if c == "WHEAT" else c for c in plants]
        seeds = dict(row.get("seeds") or {})
        # The seed row must move with the plant row or the plant is held for a seed that never
        # arrives -- `HOLD_A_PLANT_STOP_UNTIL_ITS_SEED_ARRIVES`. This is the defect that made the
        # one earlier arm in the right window (`D=26`) read as seed-starved.
        if "WHEAT" in seeds:
            seeds["CARROT"] = seeds.pop("WHEAT")
        row["seeds"] = seeds
        moved += n
        print("  d%-3d %2d WHEAT -> CARROT   seeds now %s" % (day, n, seeds))

    if not moved:
        print("nothing to move; already applied?")
        return 1

    per_day = (moved * 4 + len(SELL_DAYS) - 1) // len(SELL_DAYS)
    for day in SELL_DAYS:
        row = rows.get(str(day))
        if row is None:
            continue
        sells = dict(row.get("sells") or {})
        sells["CARROT"] = sells.get("CARROT", 0) + per_day
        row["sells"] = sells
        print("  d%-3d sells CARROT %d" % (day, sells["CARROT"]))

    tot = collections.Counter()
    for r in rows.values():
        tot.update(r.get("plants") or [])
    print("\nseason plants now: %s" % dict(tot))

    if args.apply:
        args.plan.write_text(json.dumps(sched, indent=1))
        print("wrote %s" % args.plan)
    else:
        print("\n(preview only -- pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
