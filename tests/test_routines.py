"""The chain is the unit of search, and a chain is bound to a square.

These tests exist because a sub-action search provably cannot find the animal economy. FEED is
illegal until an animal is on the board unfed with a unit carrying wheat (`jax_masks.py:93`), and
buying the animal first is a *deterministic* loss -- `consecutive_unfed >= 2` escapes it
(`kaggriculture.py:786`) against $300-$500 and a first yield 4-8 days out. So every partial prefix
of the chain is money-negative, and neither a hill-climber selecting on money nor a policy sampling
from a distribution where FEED has zero mass can assemble it.

The fix is a representation in which a partial chain **cannot be expressed**. What the search then
owns is which routine, on which square, from which day -- strategy -- while correctness lives in the
decoder.

**The square is not decoration.** It fixes three things at once, all of them consequences of the
dawn reset (`kaggriculture.py:847-851`, which dismisses every hand and teleports the farmer to
`(4,4)`): which unit can run the routine at all, whether a land parcel must be bought first, and how
far somebody has to walk there *every day* rather than once.
"""

import numpy as np
import pytest

from kagg.search import routines as R
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")


def run(script, seed=0):
    """Final money for seat 0 running `script`, seat 1 passing. Weeds off, so this is exact."""
    import jax.numpy as jnp

    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {}
        for f in FIELDS:
            mine = np.asarray(arrs[f][t])
            acts[f] = jnp.asarray(np.stack([mine, np.zeros_like(mine)])[None])   # [1, 2, ...]
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return float(np.asarray(state.farm.money)[0, 0])


# ---------------------------------------------------------------------------
# Geometry: what binds a chain to a square
# ---------------------------------------------------------------------------

def test_a_shed_access_cell_is_the_only_unlocked_one():
    """Three of the four cells start LOCKED, so `buy_land` gates the ranch."""
    tiles = R.shed_access_tiles()
    assert tiles == [(4, 4), (5, 4), (4, 5), (5, 5)]
    assert [t for t in tiles if R.quadrant_of(*t) == "NW"] == [(4, 4)]


def test_the_square_determines_the_unit():
    """`_spawn_hand` is deterministic, so each ranch cell has exactly one unit that starts on it.

    This is what removes movement from the routine entirely, and it is the fix for a first version
    that walked to the cell once on the start day and then starved every animal outside `(4,4)`
    because the farmer respawns at `(4,4)` each dawn.
    """
    assert R.SPAWN == (4, 4)
    assert R.unit_for_cell((4, 4)) == 0        # the farmer
    assert R.unit_for_cell((5, 4)) == 1        # first hand
    assert R.unit_for_cell((4, 5)) == 2
    assert R.unit_for_cell((5, 5)) == 3


@pytest.mark.parametrize("tile,n_land", [((4, 4), 0), ((5, 4), 1), ((4, 5), 2), ((5, 5), 3)])
def test_the_square_determines_the_land_bill(tile, n_land):
    """`LAND_ORDER` is bought strictly in sequence, so SE costs all three parcels."""
    assert R.land_purchases_for(tile) == n_land


# ---------------------------------------------------------------------------
# The chain is whole or absent
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tile", [(4, 4), (5, 4), (4, 5), (5, 5)])
def test_a_ranch_feeds_its_animal_every_remaining_day(tile):
    """Two consecutive unfed days kills it, so a missing day is not a rounding error."""
    s = R.Script()
    R.ranch(s, animal="COW", tile=tile, start_day=1)
    u = R.unit_for_cell(tile)
    fed = R.feed_days(s, unit=u)
    for d in range(R.place_day(s, unit=u), R.SEASON_DAYS):
        assert d in fed, f"day {d} has no FEED on {tile}; the animal escapes after two"


def test_a_partial_chain_cannot_be_expressed():
    """No API buys an animal without committing the feed loop that keeps it alive."""
    assert not hasattr(R, "buy_animal"), "no raw buy-animal primitive may be exposed"
    s = R.Script()
    R.ranch(s, animal="COW", tile=(4, 4), start_day=1)
    bought = int(np.asarray(s.buy_animal).sum())
    assert bought == 1
    assert len(R.feed_days(s, unit=0)) >= R.SEASON_DAYS - 2


@pytest.mark.parametrize("tile", [(4, 4), (5, 4), (4, 5), (5, 5)])
def test_a_ranch_never_emits_a_movement_op(tile):
    """Every cell is somebody's spawn, so no routine ever needs to walk.

    Movement is what couples an open-loop script to its own history: a unit's tile is the cumulative
    sum of its movement ops. The dawn reset bounds that coupling to a single day, and a zero-movement
    routine removes it outright.
    """
    s = R.Script()
    R.ranch(s, animal="COW", tile=tile, start_day=1)
    ops = np.asarray(s.unit_op)
    moves = np.isin(ops, [R.OP["NORTH"], R.OP["SOUTH"], R.OP["EAST"], R.OP["WEST"]]).sum()
    assert moves == 0, f"{moves} movement ops emitted for {tile}, which is a spawn tile"


@pytest.mark.parametrize("tile", [(5, 4), (4, 5), (5, 5)])
def test_a_far_cell_rehires_its_hand_every_single_day(tile):
    """Hands are dismissed at every dawn, so one hire on day 0 buys one day of work."""
    s = R.Script()
    R.ranch(s, animal="COW", tile=tile, start_day=1)
    u = R.unit_for_cell(tile)
    for day in range(1, R.SEASON_DAYS):
        t = day * R.TURNS_PER_DAY
        assert int(s.hire[t]) >= u, f"day {day} hires {int(s.hire[t])}, needs {u} for unit {u}"


# ---------------------------------------------------------------------------
# The claims that matter, measured in the simulator rather than argued
# ---------------------------------------------------------------------------

def test_a_ranch_routine_pays_for_itself():
    empty = R.Script()
    baseline = run(empty)
    ranched = R.Script()
    R.ranch(ranched, animal="COW", tile=(4, 4), start_day=1)
    got = run(ranched)
    assert got > baseline, f"ranch lost money: ${got:,.0f} vs baseline ${baseline:,.0f}"


def test_a_second_cell_adds_money_on_top_of_the_first():
    """The regression that exposed the dawn reset: two cows once scored *worse* than one.

    `(5,4)` costs $1,000 of land and a $1/day hand on top of the animal, so it has to earn more than
    that -- which it cannot do at all if the hand is not re-hired daily.
    """
    one = R.Script()
    R.ranch(one, animal="COW", tile=(4, 4), start_day=1)
    single = run(one)

    two = R.Script()
    R.ranch(two, animal="COW", tile=(4, 4), start_day=1)
    R.ranch(two, animal="COW", tile=(5, 4), start_day=1, land_day=0)
    double = run(two)

    assert double > single, (
        f"adding the (5,4) cell lost money: ${double:,.0f} vs ${single:,.0f} for one cell")
