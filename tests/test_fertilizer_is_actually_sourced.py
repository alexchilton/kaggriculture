"""A chain that intends to fertilize must order the fertilizer, exactly as it orders its seeds.

`grow(fertilize=True)` emits a PICKUP of FERTILIZER at spawn and then one FERTILIZE per tile. Both
ops are real and both are counted -- a 4-tile wheat block emits 24 FERTILIZE ops across a season. All
of them do nothing, because `ops.py:378` requires `carried[FERTILIZER] > 0` and the PICKUP draws from
a shed that no order ever stocks.

Measured on the $64,146 beam genome, substituting each slot in turn:

    grow WHEAT  f    16/16   $54,316
    grow WHEAT       16/16   $54,316      identical, to the dollar, in all eight slots

So the `fertilize` gene added in #23 is reachable, is exercised by the catalog, and is worth exactly
zero -- which is indistinguishable from "fertilizer does not help" unless you look at the ops.

`grow()` already models this correctly for seeds: `script.buy_seed[d, c_idx] += n_plant` on the same
day the planting happens. Fertilizer needs the same treatment. An animal chain is *not* a sufficient
source: `ranch()` sells its collected fertilizer every day, so a farm with cows still has an empty
shed by the time the crop unit reaches for it.

Whether buying it at roughly $100 a unit pays is a question for the search, not for this routine.
The point here is that the option must be real before it can be priced.
"""

import numpy as np
import pytest

from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")
FERT = R.PRODUCTS.index("FERTILIZER")
BLOCK = [(0, 0), (1, 0), (2, 0), (3, 0)]
HELPED = sorted(R.FERTILIZER_HELPS)


def _count(script, unit, op_name):
    return sum(1 for o in np.asarray(script.unit_op)[:, unit] if R.OP_NAMES[int(o)] == op_name)


def _run(script, seed=0):
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return state


@pytest.mark.parametrize("crop", HELPED)
def test_a_fertilizing_chain_orders_the_fertilizer_it_picks_up(crop):
    """The structural claim, independent of price."""
    s = R.grow(R.Script(), crop, BLOCK, plant_day=0, unit=0, fertilize=True)
    picked = _count(s, 0, "PICKUP")
    ordered = int(np.asarray(s.buy_product)[:, FERT].sum())
    assert picked > 0, f"{crop} was asked to fertilize and never reaches for any fertilizer"
    assert ordered >= picked, (
        f"{crop} picks fertilizer up {picked} times but orders {ordered} units; the shed is empty "
        f"and every FERTILIZE after it is a no-op")


def test_an_unfertilized_chain_orders_none():
    """The option must stay opt-in -- a plain chain must not start buying fertilizer."""
    s = R.grow(R.Script(), "WHEAT", BLOCK, plant_day=0, unit=0, fertilize=False)
    assert int(np.asarray(s.buy_product)[:, FERT].sum()) == 0


def test_melon_orders_none_even_when_asked():
    """Melon yields 12 per tile fertilized or not, so `FERTILIZER_HELPS` excludes it. Buying for it
    would be pure loss, and this is the one crop the beam actually favours."""
    assert "MELON" not in R.FERTILIZER_HELPS
    s = R.grow(R.Script(), "MELON", BLOCK, plant_day=0, unit=0, fertilize=True)
    assert int(np.asarray(s.buy_product)[:, FERT].sum()) == 0
    assert _count(s, 0, "FERTILIZE") == 0


@pytest.mark.parametrize("crop", HELPED)
def test_fertilizing_actually_changes_the_season(crop):
    """The money form. Not that it *wins* -- that it is not identical, which is what it is today."""
    plain = R.grow(R.Script(), crop, BLOCK, plant_day=0, unit=0, fertilize=False)
    fert = R.grow(R.Script(), crop, BLOCK, plant_day=0, unit=0, fertilize=True)
    m_plain = float(np.asarray(_run(plain).farm.money)[0, 0])
    m_fert = float(np.asarray(_run(fert).farm.money)[0, 0])
    assert m_plain != m_fert, (
        f"{crop} banks ${m_plain:,.0f} with and without fertilizer; the FERTILIZE ops are no-ops")
