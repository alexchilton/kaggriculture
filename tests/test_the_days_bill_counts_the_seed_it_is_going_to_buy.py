"""`_days_bill` counts the seed the row buys, so a day that cannot afford it knows it is short.

`short_of_cash` (`schedule_agent.py:1695`) is the single signal that tells the planner a day
must get its produce to the shed while the market is open rather than batching it to dusk. It is
`_days_bill_now(row) > money`, and `_days_bill` prices seed with

    R.CROP_TABLE.get(crop, {}).get("seed", 0)

`R` is `kagg.search.routines` and `R.CROP_TABLE["MELON"]` is
`{'first': 10, 'max_day': 12, 'max_yield': 6, 'ongoing': False, 'interval': 0}` -- there is no
`seed` key on it, so the default fires for every crop and **seed contributes exactly $0 to the
bill**. The price lives on `RT.SEED_COST` (`{'MELON': 80, 'STRAWBERRY': 100, 'WHEAT': 10}`), which is
what the seed-ordering sort already reads.

Measured on Victor's d10, seed 11 -- the first day the grid diverges after nine matching days:

    row seeds        MELON 14, STRAWBERRY 16, WHEAT 1   = $2,730
    _days_bill                                            $2,286   <- less than the seed alone
    _days_bill_now   (bill minus the $1,000 parcel)       $1,286
    dawn bank                                             $2,125

So d10 reads as comfortably funded, `short_of_cash` is False, and every delivery rule that keys off
it is switched off on the one day that needs it. The day then runs on $16 from h3 to h20 while thirty
melon ride around in hands, and four strawberry stops are walked past with no seed.

This is a pricing bug, not a policy question. `_days_bill`'s own docstring says it is "deliberately
coarse" and that "animals and land dominate it by an order of magnitude over seeds and hires" -- on
d10 the seed is larger than the parcel, so that reasoning does not hold and never did.

Two assertions:

  1. **The premise.** `CROP_TABLE` really has no `seed` key, so this is the mechanism and not a
     coincidence of one row's arithmetic.
  2. The bill for a row covers the seed that row buys.
"""
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import kagg.search.schedule_agent as SA  # noqa: E402

SCHEDULE = REPO / "data/seed_scripts/victor/schedule.json"
SCHED = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
#: The day the grid first diverges, and the day whose seed is larger than its parcel.
FOCUS_DAY = 10


def _seed_cost(row):
    return sum(SA.RT.SEED_COST.get(c, 0) * int(q) for c, q in (row.get("seeds") or {}).items())


def test_the_premise_crop_table_carries_no_seed_price():
    """If `CROP_TABLE` grows a `seed` key this file is testing nothing; fail loudly instead."""
    melon = SA.R.CROP_TABLE.get("MELON") or {}
    assert "seed" not in melon, (
        f"CROP_TABLE['MELON'] now has a seed price ({melon}); the lookup in `_days_bill` may be "
        f"correct after all and this test's premise is stale")


@pytest.mark.parametrize("day", sorted(d for d in SCHED if (SCHED[d].get("seeds") or {})))
def test_the_bill_covers_the_rows_seed(day):
    row = SCHED[day]
    bill = SA._days_bill(row)
    seed = _seed_cost(row)
    assert bill >= seed, (
        f"d{day} row buys {dict(row.get('seeds') or {})} costing ${seed:,.0f} and its whole bill "
        f"prices at ${bill:,.0f}. `_days_bill` looks the seed price up on `R.CROP_TABLE`, which "
        f"carries no `seed` key, so every seed costs $0. `short_of_cash` is "
        f"`_days_bill_now(row) > money`, so the day cannot know it is short and every delivery rule "
        f"keyed off it stays switched off.")


def test_the_focus_day_is_short_at_dawn():
    """d10's dawn bank is $2,125 (measured, seed 11). Priced correctly the row does not fit."""
    row = SCHED[FOCUS_DAY]
    assert SA._days_bill_now(row) > 2125, (
        f"d{FOCUS_DAY} prices at ${SA._days_bill_now(row):,.0f} against a $2,125 dawn bank, so it "
        f"reads as funded. Its seed alone is ${_seed_cost(row):,.0f}.")
