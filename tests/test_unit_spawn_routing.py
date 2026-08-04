"""A routine must walk from the tile its own unit spawns on, not from `SPAWN`.

`spawn_order()` mirrors `_spawn_hand`: the farmer takes `(4,4)` and hands fill the shed-access tiles
in NWSE order, cycling every four units.

    unit  0    1      2      3      4    5      6      7
    tile (4,4) (5,4) (4,5)  (5,5)  (4,4) (5,4) (4,5)  (5,5)

`grow()` computed its path with `pos = tuple(SPAWN)` for **every** unit, so a unit that does not
spawn on `(4,4)` executes a correct-length walk from the wrong origin and arrives displaced by the
difference. Nothing raises: a blocked move is a no-op and WATER/PLANT/HARVEST on the wrong tile
silently do nothing, so the chain looks healthy and simply earns less.

Measured on one MELON block `[(0,0),(1,0),(2,0),(3,0)]`, identical in every respect but the unit:

    unit 0  $15,575     spawns (4,4), correct
    unit 1  $15,545     lands on (1,0) -- still inside this block, so it survives by luck
    unit 2  $ 5,402     lands on (0,1) -- one row outside the block
    unit 3  $ 1,920     lands on (1,1) -- outside the block

A genome with 8 slots drives units 0-7, so half of them were working tiles they did not own. The
`unit 1` row is the reason this hid for so long: the damage depends on the block's geometry, and the
cheapest blocks to test are the ones where the offset happens to stay inside the block.
"""

import numpy as np
import pytest

from kagg.search import routines as R

BLOCK = [(0, 0), (1, 0), (2, 0), (3, 0)]
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


def _ops_on_day(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in script.unit_op[lo:hi, unit]]


def _tiles_worked(script, unit, day):
    """Replay from the unit's REAL spawn tile and report where each work op actually lands."""
    pos = list(R.spawn_order(n=8)[unit])
    worked = []
    for name in _ops_on_day(script, unit, day):
        if name in MOVES:
            dx, dy = MOVES[name]
            pos = [pos[0] + dx, pos[1] + dy]
        elif name in ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE"):
            worked.append(tuple(pos))
    return worked


@pytest.mark.parametrize("unit", [0, 1, 2, 3, 4, 5, 6, 7])
def test_a_crop_chain_works_the_tiles_it_was_given(unit):
    """The structural statement, independent of prices and of which block is used."""
    s = R.grow(R.Script(), "MELON", BLOCK, plant_day=0, unit=unit)
    worked = _tiles_worked(s, unit, 3)
    stray = sorted({t for t in worked if t not in set(BLOCK)})
    assert not stray, (
        f"unit {unit} spawns on {R.spawn_order(n=8)[unit]} and works {stray}, "
        f"which is outside its block {BLOCK}")


@pytest.mark.parametrize("unit", [1, 2, 5, 6])
def test_a_unit_that_can_reach_nw_earns_what_unit_zero_earns(unit):
    """The money form, for the units the routing can actually help.

    Units 3 and 7 spawn on `(5,5)` in SE, whose only two neighbours `(4,5)` SW and `(5,4)` NE are
    both LOCKED on day 0. They cannot move at all until a parcel is bought, and no routing fixes
    that -- see `test_the_se_corner_unit_is_trapped_until_land_is_bought`. Units 1, 2, 5 and 6 each
    have an unlocked step to `(4,4)`, so they must match unit 0.

    Before the fix: unit 2 $5,402 and unit 6 $4,862 against unit 0's $15,575, because the X-first
    walk pushed WEST into locked SW and lost four turns a day. After: $15,515 and $14,975.
    """
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    fields = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
              "buy_product", "buy_animal", "hire", "buy_land")

    def run(script):
        state = J.reset_with_shops(1, seed=0)
        a = script.arrays()
        for t in range(script.T):
            acts = {f: jnp.asarray(np.stack([np.asarray(a[f][t]),
                                             np.zeros_like(np.asarray(a[f][t]))])[None])
                    for f in fields}
            state = J.step(state, J.Actions(**acts), weed_chance=0.0)
        return float(np.asarray(state.farm.money)[0, 0])

    s0 = R.Script(); R.grow(s0, "MELON", BLOCK, plant_day=0, unit=0)
    su = R.Script(); R.grow(su, "MELON", BLOCK, plant_day=0, unit=unit)
    base, got = run(s0), run(su)
    # Not exact: a higher unit index hires more hands every dawn, which is a real cost.
    assert got > base * 0.85, (
        f"unit {unit} banked ${got:,.0f} against unit 0's ${base:,.0f} on an identical chain")


def test_the_se_corner_unit_is_trapped_until_land_is_bought():
    """Not a bug to fix -- a fact the search must be allowed to see.

    `(5,5)` is SE. Its neighbours are `(4,5)` SW and `(5,4)` NE, and `ops.py:86` silently ignores a
    move onto a LOCKED tile. So units 3 and 7 cannot leave their spawn on day 0 no matter how the
    path is routed, and a chain assigned to them does almost nothing until a parcel is bought.
    Slot 3 of an 8-slot genome is therefore worth far less than slot 2, which the search should be
    pricing rather than us pretending otherwise.
    """
    tiles = R.shed_access_tiles()
    se = tiles[3]
    assert se == (5, 5)
    assert R.spawn_tile(3) == se and R.spawn_tile(7) == se
    neighbours = [(se[0] - 1, se[1]), (se[0], se[1] - 1)]
    assert all(R.land_purchases_for(n) > 0 for n in neighbours), \
        "both neighbours of the SE spawn must start locked, or this trap does not exist"


def test_the_spawn_table_is_what_the_routines_assume():
    """Pins the assumption itself, so a change in `_spawn_hand` breaks here rather than silently."""
    assert R.spawn_order(n=8)[:5] == [(4, 4), (5, 4), (4, 5), (5, 5), (4, 4)]
