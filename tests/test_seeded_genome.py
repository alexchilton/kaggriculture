"""`chains.seeded_genome` is meant to be CEM's starting point. It was worse than random noise.

Measured before the fix: 0 of 16 wins and $0 banked, while a uniformly random population reached
$51,535 in 22 generations and ignored the seed entirely. Two stacked defects, both invisible from the
genome alone:

- It set `land_day=8` for every slot while buying animals from day 0, so three of the four ranch cells
  sat on land the farm did not own yet. `_do_place` fails on a LOCKED tile, the animal is never
  placed, and `FEED` then has nothing to feed -- silently, because a failed op is a no-op.
- It asked for all four ranch cells, and reaching `(5,5)` costs all three land parcels in sequence:
  $1,000 + $2,000 + $4,000 = $7,000 against a $2,058 opening bank. `_do_buy_land` no-ops when money
  is short and the routine writes the order on exactly one turn, so a purchase missed once is missed
  for the whole season.

The second is the more general trap and is why the first test here is about affordability rather than
about ordering: a chain whose land never unlocks costs feed and crew every day and returns nothing.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.search import chains as C
from kagg.search import routines as R
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

OPENING_BANK = 3000          # `kaggriculture.py:237` startingMoney
FIRST_PARCEL = R.LAND_PRICES[0]


def _slots(genome, n_slots):
    return np.asarray(genome, dtype=np.int64).reshape(n_slots, len(C.GENES))


def _land_cost(n_parcels):
    return sum(R.LAND_PRICES[:n_parcels])


@pytest.mark.parametrize("n_slots", [4, 8, 12])
def test_the_seed_buys_at_most_one_parcel_before_it_has_earned_anything(n_slots):
    """Land is bought out of working capital, and working capital is what binds.

    The second parcel costs $2,000 of a $3,000 opening bank, and `sell_timing_sweep.log` measured that
    delaying sells by two days costs 62% of the season -- the winner's own bank drops to **$4 on day 1**
    and stays under $2,000 until day 8. Committing $3,000 to land before a single harvest is not
    "affordable", it is bankruptcy with a receipt. One parcel is the most a starting point may assume.
    """
    g = _slots(C.seeded_genome(n_slots), n_slots)
    needed = 0
    for slot in range(n_slots):
        kind = C.KINDS[int(g[slot, 0]) % len(C.KINDS)]
        if kind == "off":
            continue
        tile = (C.RANCH_CELLS[int(g[slot, 2]) % len(C.RANCH_CELLS)] if kind == "ranch"
                else C.BLOCKS[int(g[slot, 2]) % len(C.BLOCKS)][0])
        land_day = C.LAND_DAY_CHOICES[int(g[slot, 4]) % len(C.LAND_DAY_CHOICES)]
        if land_day == 0:
            needed = max(needed, R.land_purchases_for(tile))
    assert _land_cost(needed) <= FIRST_PARCEL, (
        f"the seed commits {needed} parcels (${_land_cost(needed):,}) on day 0 out of "
        f"${OPENING_BANK:,}, leaving ${OPENING_BANK - _land_cost(needed):,} of working capital")


@pytest.mark.parametrize("n_slots", [4, 8, 12])
def test_land_is_bought_no_later_than_the_chain_that_stands_on_it_starts(n_slots):
    """Buying the animal before its pen's quadrant is unlocked wastes the animal and the feed."""
    g = _slots(C.seeded_genome(n_slots), n_slots)
    for slot in range(n_slots):
        kind = C.KINDS[int(g[slot, 0]) % len(C.KINDS)]
        if kind == "off":
            continue
        start_day = C.START_DAY_CHOICES[int(g[slot, 3]) % len(C.START_DAY_CHOICES)]
        land_day = C.LAND_DAY_CHOICES[int(g[slot, 4]) % len(C.LAND_DAY_CHOICES)]
        tile = (C.RANCH_CELLS[int(g[slot, 2]) % len(C.RANCH_CELLS)] if kind == "ranch"
                else C.BLOCKS[int(g[slot, 2]) % len(C.BLOCKS)][0])
        if R.land_purchases_for(tile) == 0:
            continue                       # NW is owned at spawn; land_day is irrelevant there
        assert land_day <= start_day, (
            f"slot {slot} ({kind} on {tile}) starts day {start_day} but buys land day {land_day}")


def _bank(script, seed=0):
    """Final bank for `script` in seat 0 against a passing opponent, weeds off."""
    state = J.reset_with_shops(1, seed=seed)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {}
        for f in FIELDS:
            mine = np.asarray(arrs[f][t])
            acts[f] = jnp.asarray(np.stack([mine, np.zeros_like(mine)])[None])
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    return float(np.asarray(state.farm.money)[0, 0])


def test_the_seed_banks_more_than_doing_nothing():
    """The bar a starting point has to clear. It was banking $0 -- worse than an empty tape."""
    idle = _bank(R.Script())
    script, used, skipped = C.decode(C.seeded_genome(8), 8)
    assert skipped == 0, f"{skipped} of 8 seeded chains were illegal"
    seeded = _bank(script)
    assert seeded > idle, f"seeded genome banked ${seeded:,.0f} against ${idle:,.0f} for an idle farm"


def test_the_seed_never_runs_its_bank_to_zero():
    """The failure mode itself, pinned directly rather than through the final bank.

    At $0 every subsequent order silently no-ops: no feed, so the animals starve; no seeds, so the
    atomic PLANT rule drops the whole crop. The season is over on the day the bank empties, and the
    final number does not say which day that was. This does.
    """
    script, _used, _skipped = C.decode(C.seeded_genome(8), 8)
    state = J.reset_with_shops(1, seed=0)
    arrs = script.arrays()
    curve = []
    for day in range(R.SEASON_DAYS):
        for t in range(day * R.TURNS_PER_DAY, min((day + 1) * R.TURNS_PER_DAY, script.T)):
            acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                             np.zeros_like(np.asarray(arrs[f][t]))])[None])
                    for f in FIELDS}
            state = J.step(state, J.Actions(**acts), weed_chance=0.0)
        curve.append(float(np.asarray(state.farm.money)[0, 0]))
    broke = [d for d, m in enumerate(curve) if m <= 0]
    assert not broke, (f"bank hits zero on day(s) {broke[:5]}; curve "
                       f"{[f'{m:,.0f}' for m in curve[:12]]}")


def test_the_seed_places_every_animal_it_buys():
    """The mechanism, isolated: animals bought must end the season alive in a pen.

    `buy_animal` moves money and `PLACE` moves the animal onto the tile. A locked tile fails the
    second silently, so counting purchases against livestock is the direct test of the defect.
    """
    script, used, _ = C.decode(C.seeded_genome(8), 8)
    bought = int(script.buy_animal.sum())
    if bought == 0:
        pytest.skip("this seed keeps no animals")
    state = J.reset_with_shops(1, seed=0)
    arrs = script.arrays()
    for t in range(script.T):
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)
    alive = int((np.asarray(state.tiles.animal)[0, 0] != J.NO_ANIMAL).sum())
    assert alive > 0, f"bought {bought} animals across the season and none is in a pen at the end"
