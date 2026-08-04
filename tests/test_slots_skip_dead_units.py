"""A slot must not be assigned a unit that cannot move.

Hands spawn on the four shed-access tiles in NWSE order and the cycle repeats every four, so units 3,
7, 11 ... all wake on `(5,5)` in SE. `(5,5)`'s only two neighbours are `(4,5)` in SW and `(5,4)` in NE,
and `ops.py:86` silently ignores a move onto LOCKED ground. So an SE-spawn unit cannot take a single
step until the farm owns SE -- which costs all three parcels, **$7,000** against a $3,000 opening bank.

The leader tape buys exactly two parcels (day 7 NE, day 10 SW) and never buys SE at all. Under that
plan, and under every plan our own search has ever found, units 3 and 7 are inert for the whole season.

Measured on one identical melon block, changing only the unit:

    unit 0  (4,4)  $15,575        unit 4  (4,4)  $15,365
    unit 1  (5,4)  $15,545        unit 5  (5,4)  $15,215
    unit 2  (4,5)  $15,515        unit 6  (4,5)  $14,975
    unit 3  (5,5)  $ 1,920        unit 7  (5,5)  $ 1,050

`decode()` mapped slot `k` to unit `k`, so an 8-slot genome spent two of its eight slots on units that
do nothing while still paying to hire them. The fix maps slots onto the units that can actually work:
`[0, 1, 2, 4, 5, 6, 8, 9]`.

The cost is hires, and it is small. Hands are dismissed and re-hired every dawn on a Fibonacci ladder
that resets daily, so reaching unit 9 instead of unit 7 is a few dollars a day against a recovered
unit worth roughly $15,000 a season.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

SE = (5, 5)


def test_the_premise_the_se_spawn_is_locked_without_every_parcel():
    """Guard the setup: if the board or land order changes, this suite must fail loudly."""
    assert R.shed_access_tiles()[3] == SE
    assert R.spawn_tile(3) == SE and R.spawn_tile(7) == SE
    assert R.land_purchases_for(SE) == 3
    assert sum(R.LAND_PRICES) == 7000 > C.OPENING_BANK


def test_working_units_never_include_an_se_spawn():
    """The vocabulary itself, so no caller has to remember the rule."""
    units = C.working_units(12)
    assert len(units) == 12
    assert len(set(units)) == 12, f"duplicate units would interleave two chains: {units}"
    for u in units:
        assert R.spawn_tile(u) != SE, f"unit {u} spawns on {SE} and cannot move"


def test_the_first_working_units_are_the_cheapest_ones():
    """Skipping must not reorder: unit 0 is free (the farmer) and low indices cost fewer hires."""
    assert C.working_units(8) == [0, 1, 2, 4, 5, 6, 8, 9]


@pytest.mark.parametrize("n_slots", [1, 4, 8, 12])
def test_a_genome_drives_only_working_units(n_slots):
    """The whole-genome form: no chain may be written onto a dead unit."""
    g = np.zeros((n_slots, len(C.GENES)), dtype=np.int64)
    for slot in range(n_slots):
        g[slot] = (C.KINDS.index("grow"), R.CROPS.index("MELON"), slot % len(C.BLOCKS),
                   C.START_DAY_CHOICES.index(2), C.LAND_DAY_CHOICES.index(0), 0, 0)
    script, _used, _skipped = C.decode(g.reshape(-1), n_slots)
    ops = np.asarray(script.unit_op)
    moves = {R.OP["NORTH"], R.OP["SOUTH"], R.OP["EAST"], R.OP["WEST"]}
    for u in range(ops.shape[1]):
        if R.spawn_tile(u) != SE:
            continue
        # A `ranch` on the SE *cell* is the one legitimate use of an SE unit: the pen stands on the
        # spawn tile itself, needs no movement, and the chain buys the parcel that unlocks it. What
        # must never happen is a unit being asked to *walk* from a tile it cannot leave.
        assert not (set(ops[:, u].tolist()) & moves), \
            f"unit {u} spawns on {SE}, cannot leave it, and was given movement ops"


def test_slot_three_is_worth_what_slot_two_is_worth():
    """The money form, and the point of the exercise.

    Before the fix slot 3 drove unit 3 and banked $1,920 against slot 2's $15,515 on an identical
    chain. Not exact afterwards -- a higher unit index hires more hands every dawn, which is real --
    but the same order of magnitude rather than an eighth.
    """
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    fields = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
              "buy_product", "buy_animal", "hire", "buy_land")
    block = [b for b in C.BLOCKS if C.land_cost(b[0]) == 0][0]

    def bank(slot):
        s = R.Script()
        R.grow(s, "MELON", list(block), plant_day=2, unit=C.working_units(8)[slot])
        a = s.arrays()
        state = J.reset_with_shops(1, seed=0)
        for t in range(s.T):
            acts = {f: jnp.asarray(np.stack([np.asarray(a[f][t]),
                                             np.zeros_like(np.asarray(a[f][t]))])[None])
                    for f in fields}
            state = J.step(state, J.Actions(**acts), weed_chance=0.0)
        return float(np.asarray(state.farm.money)[0, 0])

    two, three = bank(2), bank(3)
    assert three > two * 0.85, (
        f"slot 3 banks ${three:,.0f} against slot 2's ${two:,.0f}; it is still on a dead unit")
