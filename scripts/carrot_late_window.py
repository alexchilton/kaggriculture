#!/usr/bin/env python3
"""Put CARROT in the schedule's late plant window at the scale the leader actually uses.

`data/seed_scripts/victor/schedule.json` is NOT git-tracked, so every change to it has to be a
script or it is invisible and unrepeatable. Run with `--apply` to write, without to preview.

WHAT THE 66 GAMES SAY, AND WHAT THIS SCRIPT USED TO GET WRONG
-------------------------------------------------------------
Earlier versions of this file swapped whole days of WHEAT for CARROT -- 55 tiles over d23-d26 --
on the theory that `plant_prize` crosses over at d26. Measured across all 66 downloaded games of
カワシギ (#1, 61-0-5), that is not what he does at all:

    day            d20   d21   d22   d23   d24   d25   d26   d27
    CARROT/game   0.02  1.29  1.15  0.30  1.03  1.00  0.76  0.00
    WHEAT /game   5.38  4.17  9.09  6.58  6.09  9.08  9.50  11.09

Carrot is a **side crop of 5-8 tiles for the whole season**, planted one or two a day BESIDE four to
eleven wheat on the same days. Never a replacement for wheat, never a whole day. Every game in the
sample plants some (1-8, median 6); no game plants more than 8.

The seed cadence is just as specific: he buys ~7.3 carrot seed on **d6** and holds it for fifteen
days, topping up ~1/day as he plants from d21. Buying at d6 and planting at d21 is not a rounding
error -- carrot seed is $20 and the d6 book is the cheapest it gets.

So `CARROT_PER_DAY` below is 1, not 14, and the wheat rows are left alone. The tiles come from the
same ground the day's own one-shot HARVESTs clear, which is what `router.REPLANT_A_CLEARED_TILE`
and `_best_replant_crop` already handle -- offering both crops in the budget yields wheat while
`plant_prize` prefers it and carrot once it does, with no hard-coded changeover.

WHY THIS COULD NOT BE MEASURED BEFORE
------------------------------------
`SELLABLE` in `schedule_agent_1455mh` listed six of the env's nine products and CARROT was not one
of them. It is the iteration domain of the only loop that emits a SELL, so a `sells` row naming
carrot was read by nothing. Traced on seed 11: 55 seeds bought, 38 planted, harvested on schedule,
**92 units standing in the shed on d29**, zero orders, $0 banked. Fixed, with
`tests/test_a_product_the_schedule_asks_to_sell_can_be_sold.py` pinning it.
"""
import argparse
import collections
import json
import pathlib
import sys

PLAN = pathlib.Path("data/seed_scripts/victor/schedule.json")

#: Days that take a carrot planting, and how many each. His mean is 1.29/1.15/0.30/1.03/1.00/0.76
#: over d21-d26 for a season total of 5-8; one a day over six days is the same shape at the same
#: scale, without pretending to a precision the spread does not support.
CARROT_DAYS = (21, 22, 23, 24, 25, 26)
CARROT_PER_DAY = 1

#: The day the seed is bought. His, and it is 15 days before the first planting.
SEED_DAY = 6

#: A carrot sown on day D reaches `first_yield_day` 2 on D+2 and `max_yield_day` 3 on D+3, and its
#: `max_lifespan_step` starts rotting it at D+4. So the d21 planting is sellable from d23 and the
#: d26 one from d28. The sells row is a quota, not a promise.
SELL_DAYS = (24, 25, 26, 27, 28, 29)


def rows_of(sched):
    return sched["days"] if isinstance(sched, dict) and "days" in sched else sched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", type=pathlib.Path, default=PLAN)
    ap.add_argument("--apply", action="store_true", help="write the file; otherwise preview only")
    ap.add_argument("--per-day", type=int, default=CARROT_PER_DAY,
                    help="carrot tiles per day in the window (his mean is ~1)")
    args = ap.parse_args()

    sched = json.loads(args.plan.read_text())
    rows = rows_of(sched)

    if any("CARROT" in (rows.get(str(d), {}).get("plants") or []) for d in CARROT_DAYS):
        print("carrot is already in the plants row; already applied?")
        return 1

    added = 0
    for day in CARROT_DAYS:
        row = rows.get(str(day))
        if row is None:
            continue
        # **Appended, not substituted.** He plants carrot BESIDE the day's wheat, and the four
        # earlier arms that swapped wheat out were measuring the missing wheat.
        row["plants"] = list(row.get("plants") or []) + ["CARROT"] * args.per_day
        added += args.per_day
        print("  d%-3d +%d CARROT (wheat row untouched: %d)" % (
            day, args.per_day,
            sum(1 for c in (row.get("plants") or []) if c == "WHEAT")))

    seed_row = rows.get(str(SEED_DAY))
    if seed_row is not None:
        seeds = dict(seed_row.get("seeds") or {})
        seeds["CARROT"] = seeds.get("CARROT", 0) + added
        seed_row["seeds"] = seeds
        print("  d%-3d seeds %s" % (SEED_DAY, seeds))

    # `max_yield` is 4 and a plain water adds one unit inside a two-day window, so a tile realistically
    # lands 2-3. Sized at 3 and spread, because an over-large quota is bounded by the shed anyway
    # while an under-sized one strands stock -- which is the failure this whole file exists to undo.
    per_day = max(1, (added * 3 + len(SELL_DAYS) - 1) // len(SELL_DAYS))
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
    print("his season carrot: 1-8, median 6")

    if args.apply:
        args.plan.write_text(json.dumps(sched, indent=1))
        print("wrote %s" % args.plan)
    else:
        print("\n(preview only -- pass --apply to write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
