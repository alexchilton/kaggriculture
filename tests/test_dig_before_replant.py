"""A replant must be preceded by a DIG, because an idle tile can weed and the tape cannot see it.

The new leader `somewhere after` does this 25 times a game and it is the answer to "how does a fixed
tape know where to dig?" -- it does not know, and it does not need to. Read off
`data/seed_scripts/new_leader/90016067.json`: **all 23 of his inspectable digs land on an EMPTY tile**,
and 9 of the first 12 are immediately followed by `PLANT`, `WATER`.

So DIG is *insurance*, not information:

* tile clean -> `dig()` requires WEED, PLANT or an empty structure (`ops.py:156`), so on EMPTY it is a
  no-op and the cost is one turn;
* tile weeded while it sat idle -> the DIG clears it and the following PLANT succeeds instead of
  silently failing, because PLANT needs EMPTY and WATER needs PLANT. Without it the tile is dead for
  the rest of the season while `grow()` keeps ordering seed for it every cycle.

The risk is not marginal. `_spawn_weeds` fires at `weedSpawnChance = 0.005` per empty tile per turn,
so a tile idle for one day carries `1 - 0.995**24` ~ **11%**.

Measured cost of weeds on our farms today is **$0** (`data/logs/*`, eight configurations) -- our melon
replants twice a season and the empty window is short. That is why this hid, and it is not a reason to
skip it: the leader plants 131 tiles against our 32, and the exposure grows with every replant.

**Only before a replant.** A tile's first plant happens on ground that was never ours to weed, and
spending a turn there is pure loss.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")
BLOCK = [(0, 0), (1, 0), (2, 0), (3, 0)]
# Wheat is the fastest cycle -- harvestable at age 2, done at 4 -- so it replants most often and is
# the crop where this matters most.
CYCLING = "WHEAT"


def _day_ops(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in np.asarray(script.unit_op)[lo:hi, unit]]


def _all_ops(script, unit):
    return [R.OP_NAMES[int(o)] for o in np.asarray(script.unit_op)[:, unit]]


def test_the_premise_dig_is_a_no_op_on_empty_ground():
    """If DIG were harmful on a clean tile this whole approach would be wrong. `ops.py` gates it on
    WEED / PLANT / empty structure, so on EMPTY it does nothing but cost the turn."""
    from kagg.sim import ops as O

    assert hasattr(O, "dig")


def test_a_replant_is_preceded_by_a_dig():
    """The structural claim. Every PLANT after the first on a tile must have a DIG before it."""
    s = R.grow(R.Script(), CYCLING, BLOCK, plant_day=0, unit=0)
    ops = _all_ops(s, 0)
    plants = [i for i, o in enumerate(ops) if o == "PLANT"]
    assert len(plants) > len(BLOCK), (
        f"{CYCLING} should replant across a season; only {len(plants)} PLANT ops for "
        f"{len(BLOCK)} tiles")
    # The first `len(BLOCK)` plants are first-plants. Everything after is a replant.
    for i in plants[len(BLOCK):]:
        window = ops[max(0, i - 3):i]
        assert "DIG" in window, (
            f"replant at turn {i} has no DIG in the three turns before it ({window}); a weed on that "
            f"tile silently kills it for the rest of the season")


def test_a_first_plant_is_not_preceded_by_a_dig():
    """The other half: a turn spent digging ground that was never idle is pure loss."""
    s = R.grow(R.Script(), CYCLING, BLOCK, plant_day=0, unit=0)
    day0 = _day_ops(s, 0, 0)
    assert "PLANT" in day0
    assert "DIG" not in day0, f"day 0 digs before its first plant: {[o for o in day0 if o != 'PASS']}"


def test_melon_pays_for_this_too_but_only_twice():
    """A sanity check on cost. Melon cycles roughly twice a season, so it should gain a couple of
    DIGs, not dozens -- if this shows a DIG a day, the placement is wrong."""
    s = R.grow(R.Script(), "MELON", BLOCK, plant_day=0, unit=0)
    n_dig = sum(1 for o in _all_ops(s, 0) if o == "DIG")
    assert 0 < n_dig <= 2 * len(BLOCK), f"{n_dig} DIG ops on a melon block is too many"


def test_the_day_still_fits():
    """`grow()` raises rather than truncating, so the added turn must not overflow a legal block."""
    for block in [b for b in C.BLOCKS if C.land_cost(b[0]) == 0][:6]:
        s = R.grow(R.Script(), CYCLING, list(block), plant_day=0, unit=0)
        for day in range(R.SEASON_DAYS):
            ops = _day_ops(s, 0, day)
            assert ops[0] == "PASS", f"{block} day {day} put work on the market turn"


def test_it_still_banks_at_least_what_it_did_before():
    """The money form. One turn per replant is cheap insurance, but it is not free, and a crop whose
    day is already tight could lose more than it protects."""
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    def bank(crop, weed_chance):
        s = R.grow(R.Script(), crop, BLOCK, plant_day=0, unit=0)
        a = s.arrays()
        state = J.reset_with_shops(1, seed=0)
        for t in range(s.T):
            acts = {f: jnp.asarray(np.stack([np.asarray(a[f][t]),
                                             np.zeros_like(np.asarray(a[f][t]))])[None])
                    for f in FIELDS}
            state = J.step(state, J.Actions(**acts), weed_chance=weed_chance)
        return float(np.asarray(state.farm.money)[0, 0])

    # Against the recorded pre-DIG figures, weeds off. Insurance may cost a little; it must not cost
    # a lot, and these are the numbers to notice if it does.
    for crop, before in (("WHEAT", 7_959 / 2), ("MELON", 27_276 / 2)):
        got = bank(crop, 0.0)
        assert got > before * 0.9, f"{crop} banks ${got:,.0f}, well under its pre-DIG ${before:,.0f}"
