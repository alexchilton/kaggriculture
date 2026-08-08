"""The day's bill prices the cheapest parcel, whichever one we are actually buying.

## The bug

`_days_bill` decides whether the day is short of cash, which is what arms `FUND_THE_DAY_WHEN_SHORT`
-- the rule that harvests the day's sellable produce first and delivers it on sight instead of
batching it to `DELIVER_MIN`. It prices land like this:

    bill += sum(R.LAND_PRICES[:int(row.get("land") or 0)])

`row["land"]` is how many parcels are bought THAT DAY, which is almost always 1. So the slice is
`LAND_PRICES[:1]`, which is `[1000]` -- the FIRST parcel -- on every land day of the season.
`LAND_PRICES` is `[1000, 2000, 4000]` and `_do_buy_land` unlocks `LAND_ORDER[n_already_bought]`,
so the price is fixed by how many we already own, not by how many we buy today.

On Seb's 1.32.6 schedule, land days [4, 6, 10]:

    d4    1st parcel, costs 1,000   billed 1,000    correct by coincidence
    d6    2nd parcel, costs 2,000   billed 1,000    under by 1,000
    d10   3rd parcel, costs 4,000   billed 1,000    under by 3,000

The error grows exactly as the parcels get expensive, so the funding rule is least reliable on the
days the farm is most stretched. Day 10 is the day we fail to buy the parcel at all and take it at
d11h00 instead -- our bank peaks at $1,871 against a $4,000 price while the bill claimed $1,000.

## What this test does NOT claim

It does not claim fixing the bill fixes day 10. `short_of_cash` also requires the sell row to still
owe something, and a correct bill only arms the rule -- it does not sell anything by itself. This
pins the arithmetic, which is wrong on its own terms and is cheap to state correctly.
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import routines as R
from kagg.search import schedule_agent as SA


def test_land_prices_are_the_ladder_this_test_assumes():
    """If the env's ladder changes, the numbers below are wrong and this should say so first."""
    assert R.LAND_PRICES == [1000, 2000, 4000], R.LAND_PRICES


@pytest.mark.parametrize("owned,expected", [(0, 1000), (1, 2000), (2, 4000)])
def test_one_parcel_is_billed_at_the_price_of_the_next_one(owned, expected):
    """Buying one parcel costs what the NEXT one costs, not what the first one costs."""
    got = SA._days_bill({"land": 1}, owned=owned)
    assert got == expected, (
        f"owning {owned} parcels and buying one more billed ${got:,.0f}, "
        f"but `_do_buy_land` will charge ${expected:,.0f}")


def test_two_parcels_in_one_day_bill_for_both():
    """The slice was right about one thing: a row asking for two must pay for two."""
    assert SA._days_bill({"land": 2}, owned=1) == 2000 + 4000


def test_a_day_with_no_land_is_unchanged():
    """The overwhelming majority of days. Nothing about them may move."""
    row = {"seeds": {"WHEAT": 4}, "hires": 3}
    assert SA._days_bill(row, owned=2) == SA._days_bill(row, owned=0)


def test_the_default_is_the_old_behaviour():
    """`owned` defaults to 0 so every existing caller keeps its exact meaning until it passes one."""
    assert SA._days_bill({"land": 1}) == SA._days_bill({"land": 1}, owned=0) == 1000
