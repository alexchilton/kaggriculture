"""The chain routines must not throw away the fertilizer economy.

`jax_sim` models fertilizer fully -- `COLLECT_FERTILIZER` at `jax_sim.py:690`, `FERTILIZE` at `:697`,
and the payoff at `:1192-1193` where a fertilized watered tile gains 2 yield units instead of 1. The
*routines* used none of it: `ranch()` emitted BUILD/PICKUP/PLACE/FEED/CARE/HARVEST/DROP and `grow()`
emitted PLANT/WATER/HARVEST/SELL, so every animal in every chain search produced its fertilizer onto
the tile and left it there to expire.

That is not a missing nicety. Three measured facts say it is the main reason to own an animal at all:

* `kagg/search/plan.py:145` -- the leaders ran 318 collects, 107 fertilises, and sold 406 units for
  **~$21,900**. The best whole farm this project has searched banks $50,916.
* `kagg/agents/shepherd.py:28` -- across winner replays FERTILIZER is **23.1% of sales**, against
  MILK at 9.1%. It is the second-biggest revenue line after wheat.
* `kagg/economics/production.py:53-55` -- "the wheat -> animal -> fertilizer -> premium-crop loop
  ... is the main structural reason to keep animals."

The consequence is that every animal verdict this project has produced was measured on a milk-only
cow. `data/logs/animal_diagnostic.log` concluded "animals cost more than the crop they displace" from
a best-case substitution of -$503 -- a number taken with two of the animal's three income paths
absent from the tape. The search never rejected animals; it was never shown one.

**Melon is the exception and it is enforced here rather than left to a caller.**
`production.py:42` measured melon gaining exactly nothing from fertilizer -- 12 units either way,
because its watering window already fills `max_yield` unfertilized -- while tomato and strawberry
*double*. A fertilize op on a melon tile is a wasted turn out of a 24-turn day, so `grow()` must
refuse it even when asked.
"""

import numpy as np
import pytest

from kagg.economics import production as P
from kagg.search import routines as R

FERT = R.PRODUCTS.index("FERTILIZER")
COW_CELL = (4, 4)          # the one shed-access tile owned at spawn

# Crops whose measured season yield actually rises with fertilizer. Melon is deliberately absent.
GAINS = tuple(c for c in R.CROPS
              if P.TILE_YIELD_FERTILIZED[c] > P.TILE_YIELD_PER_SEASON[c])


def _ops_on_day(script, unit, day):
    lo, hi = day * R.TURNS_PER_DAY, (day + 1) * R.TURNS_PER_DAY
    return [R.OP_NAMES[int(o)] for o in script.unit_op[lo:hi, unit]]


def _run(script, seed=0):
    """Final money for seat 0, seat 1 passing. Weeds off, so the number is exact."""
    import jax.numpy as jnp
    from kagg.sim import jax_sim as J

    fields = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
              "buy_product", "buy_animal", "hire", "buy_land")
    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in fields}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return float(np.asarray(state.farm.money)[0, 0])


# ---------------------------------------------------------------------------
# ranch(): the animal's fertilizer must be picked up and sold
# ---------------------------------------------------------------------------

def test_the_melon_exclusion_is_read_from_measurement_not_hardcoded():
    """Guards the guard. If someone edits the yield tables, `GAINS` must follow them."""
    assert "MELON" not in GAINS, "production.py measured melon gaining nothing from fertilizer"
    assert set(GAINS) == {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY"}, GAINS


def test_ranch_collects_the_fertilizer_its_animal_produces():
    """One per animal per day, refreshed nightly, at **no action cost** (`plan.py:144`).

    A day the chain does not collect is a unit of free product left on the tile to expire.
    """
    s = R.ranch(R.Script(), "COW", COW_CELL, start_day=0)
    u = R.unit_for_cell(COW_CELL)
    days = [d for d in range(1, R.SEASON_DAYS)
            if "COLLECT_FERTILIZER" in _ops_on_day(s, u, d)]
    missing = [d for d in range(1, R.SEASON_DAYS) if d not in days]
    assert not missing, (
        f"no COLLECT_FERTILIZER on day(s) {missing[:8]} of {R.SEASON_DAYS}; "
        f"each is one free unit abandoned on the tile")


def test_ranch_sells_the_fertilizer_it_collects():
    """Collecting without a sell path is what `rollout.py:52` records having shipped once already:
    "WOOL and FERTILIZER were never sold: `decide` could not observe that it held them."
    """
    s = R.ranch(R.Script(), "COW", COW_CELL, start_day=0)
    assert int(np.asarray(s.sell)[:, FERT].sum()) > 0, \
        "fertilizer is collected but never offered to the market"


def test_a_ranch_can_be_told_not_to_collect():
    """The knob has to exist in both positions, or the A/B below cannot be measured."""
    s = R.ranch(R.Script(), "COW", COW_CELL, start_day=0, collect_fertilizer=False)
    u = R.unit_for_cell(COW_CELL)
    ops = [op for d in range(R.SEASON_DAYS) for op in _ops_on_day(s, u, d)]
    assert "COLLECT_FERTILIZER" not in ops
    assert int(np.asarray(s.sell)[:, FERT].sum()) == 0


def test_a_cow_banks_more_once_its_fertilizer_is_collected():
    """The headline. `animal_diagnostic.log` priced a cow at -$503 against a melon block with this
    revenue absent; the leaders drew ~$21,900 from it.
    """
    without = _run(R.ranch(R.Script(), "COW", COW_CELL, start_day=0, collect_fertilizer=False))
    with_fert = _run(R.ranch(R.Script(), "COW", COW_CELL, start_day=0, collect_fertilizer=True))
    assert with_fert > without, (
        f"collecting fertilizer earned nothing: ${with_fert:,.0f} vs ${without:,.0f}")


# ---------------------------------------------------------------------------
# grow(): fertilize what gains, never melon
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("crop_name", GAINS)
def test_grow_fertilizes_a_crop_that_gains_from_it(crop_name):
    tiles = [(3, 3)]
    s = R.grow(R.Script(), crop_name, tiles, plant_day=0, fertilize=True)
    ops = [op for d in range(R.SEASON_DAYS) for op in _ops_on_day(s, 0, d)]
    assert "FERTILIZE" in ops, f"{crop_name} gains " \
        f"{P.TILE_YIELD_FERTILIZED[crop_name] - P.TILE_YIELD_PER_SEASON[crop_name]} units/season " \
        f"from fertilizer and the chain never applies it"


def test_grow_never_fertilizes_melon_even_when_asked():
    """`production.py:42`: melon's watering window already fills `max_yield`, so a FERTILIZE on a
    melon tile buys nothing and costs a turn out of 24. Refusing it is the routine's job, not the
    caller's -- the beam builds melon farms and would otherwise pay the turn for nothing.
    """
    s = R.grow(R.Script(), "MELON", [(3, 3)], plant_day=0, fertilize=True)
    ops = [op for d in range(R.SEASON_DAYS) for op in _ops_on_day(s, 0, d)]
    assert "FERTILIZE" not in ops, "melon gains 0 units from fertilizer; the turn is wasted"
    assert "PICKUP" not in ops, "and no fertilizer should be fetched for it either"


def test_grow_does_not_fertilize_unless_asked():
    """Opt-in, so every measurement taken before this change stays reproducible."""
    s = R.grow(R.Script(), "STRAWBERRY", [(3, 3)], plant_day=0)
    ops = [op for d in range(R.SEASON_DAYS) for op in _ops_on_day(s, 0, d)]
    assert "FERTILIZE" not in ops


@pytest.mark.parametrize("n_tiles", [1, 2, 4])
def test_fertilizing_never_overflows_the_day(n_tiles):
    """`grow()` raises rather than truncating an over-budget day, because a spilled op lands after
    the dawn teleport. Adding fertilizer ops must not turn a legal block illegal -- the routine has
    to drop the fertilizing instead, or the search silently loses those blocks as 'skipped'.
    """
    tiles = [(x, 3) for x in range(n_tiles)]
    s = R.grow(R.Script(), "STRAWBERRY", tiles, plant_day=0, fertilize=True)
    for day in range(R.SEASON_DAYS):
        ops = _ops_on_day(s, 0, day)
        assert len(ops) <= R.TURNS_PER_DAY
        # turn 0 of each day is reserved for the market order
        assert ops[0] == "PASS", f"day {day} put work on the market turn"
