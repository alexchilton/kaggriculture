"""Parcels must be ordered a day apart, not three in the same three seconds.

`ranch()` and `grow()` both wrote their land orders as

    for k in range(land_purchases_for(tile)):
        script.buy_land[land_day * TURNS_PER_DAY + k] = 1

-- consecutive *turns* of one day. A chain wanting SE therefore asks for $1,000 + $2,000 + $4,000
inside three turns, against an opening bank of $3,000. `_do_buy_land` no-ops when money is short, so
the third order vanishes and the farm silently owns two quadrants while the chain believes it owns
three. That is the mechanism behind `test_locked_chain_relocates.py`: the pen then walks until a
LOCKED tile stops it and builds there.

Three turns is also the one spacing that can never work. Nothing is earned inside a single day worth
mentioning -- the market runs once per turn but crops are harvested daily -- so ordering on turns 0,
1 and 2 guarantees the farm is judged against the bank it woke up with. A day apart at least lets the
season pay for the next parcel, which is what the leader tape does: it buys on **day 7 and day 10**,
spaced, and never buys the third at all.

This does not claim a day is enough to afford it. It claims the schedule must be *expressible*, so
that when the search picks `land_day` it is choosing between plans that differ rather than between
plans that all collapse to "whatever $3,000 covers".
"""

import numpy as np

from kagg.search import routines as R

SE_TILE = (7, 8)          # needs all three parcels, in order NE -> SW -> SE
NE_TILE = (7, 1)          # needs one


def _order_turns(script):
    return np.flatnonzero(np.asarray(script.buy_land) > 0).tolist()


def _order_days(script):
    return sorted({t // R.TURNS_PER_DAY for t in _order_turns(script)})


def test_the_premise_the_far_corner_needs_three_parcels():
    assert R.land_purchases_for(SE_TILE) == 3
    assert R.land_purchases_for(NE_TILE) == 1
    assert R.LAND_PRICES == [1000, 2000, 4000]


def test_a_ranch_does_not_order_three_parcels_inside_one_day():
    s = R.ranch(R.Script(), "COW", SE_TILE, start_day=4, land_day=0)
    turns = _order_turns(s)
    assert len(turns) == 3, f"expected three orders, got {turns}"
    assert len(_order_days(s)) == 3, (
        f"all three parcels ordered on day(s) {_order_days(s)} at turns {turns}; "
        f"$7,000 cannot clear against a $3,000 bank inside one day")


def test_a_crop_chain_does_not_order_three_parcels_inside_one_day():
    """`grow()` has the identical loop, so it has the identical defect."""
    block = [(7, 8), (8, 8), (9, 8), (9, 9)]
    s = R.grow(R.Script(), "WHEAT", block, plant_day=6, land_day=0)
    assert len(_order_days(s)) == 3, (
        f"all three parcels ordered on day(s) {_order_days(s)} at turns {_order_turns(s)}")


def test_the_first_parcel_still_lands_on_the_requested_day():
    """Spacing must not silently delay the whole plan -- `land_day` still means what it says."""
    for land_day in (0, 3, 9):
        s = R.ranch(R.Script(), "COW", SE_TILE, start_day=land_day + 4, land_day=land_day)
        assert _order_days(s)[0] == land_day, (
            f"land_day={land_day} but the first order is on day {_order_days(s)[0]}")


def test_a_single_parcel_chain_is_unchanged():
    """One parcel has nothing to space, so this must be byte-identical to before."""
    s = R.ranch(R.Script(), "COW", NE_TILE, start_day=2, land_day=1)
    assert _order_turns(s) == [1 * R.TURNS_PER_DAY]


def test_orders_never_run_past_the_season():
    """`Script.op` drops out-of-range turns; the raw market arrays must honour the same contract."""
    s = R.ranch(R.Script(), "COW", SE_TILE, start_day=R.SEASON_DAYS - 1,
                land_day=R.SEASON_DAYS - 1)
    assert all(0 <= t < s.T for t in _order_turns(s))
