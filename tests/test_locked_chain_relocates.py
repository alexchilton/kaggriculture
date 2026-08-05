"""A chain aimed at ground the farm never unlocks must not quietly build somewhere else.

This is the same silent-no-op family as `test_unit_spawn_routing.py`, one level up. `ops.py:86`
ignores a move onto a LOCKED tile, so a unit walking to a quadrant it does not own simply stops at
the border -- and then BUILD_PASTURE and PLACE fire wherever it happens to be standing. Nothing
raises, the animal is real, and the money is real. Only the *plan* is fiction.

Measured on the beam genome that scored 16/16 and $64,146:

    genome says pens at   (1, 1)  (7, 8)  (2, 8)  (6, 9)
    animals actually at   (1, 1)  (2, 4)  (6, 4)  (7, 4)

It ordered all three parcels on turn 0 -- $1,000 + $2,000 + $4,000 against a $3,000 opening bank --
so NE and SW cleared, SE never did, and three of the four chains relocated to the last row they could
reach. Fifty tiles were still LOCKED at the bell.

Why this matters beyond the wrong label: the action space is **degenerate**. Every SE ranch tile
behind the same border collapses onto the same real farm, so the beam spends evaluations
distinguishing genomes that are identical in effect, and a genuinely better configuration is hidden
behind a wall of duplicates.

These tests state the contract. They are expected to be RED until #26 is fixed; the fix has a real
design choice behind it (skip the chain in `decode()` so it shows up in `skipped`, versus validate
after decoding and reject the genome), which is why the contract is written down before either.
"""

import numpy as np
import pytest

from kagg.search import chains as C
from kagg.search import routines as R

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")

# SE, and unaffordable on day 0: reaching it costs all three parcels in sequence, $7,000 against a
# $3,000 bank. `_do_buy_land` no-ops when money is short rather than refusing the plan.
SE_TILE = (7, 8)
SE_LAND_COST = 7000


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


def _animal_tiles(state):
    from kagg.sim import jax_sim as J
    animals = np.asarray(state.tiles.animal)[0, 0]
    return {(int(i) % R.BOARD_SIZE, int(i) // R.BOARD_SIZE)
            for i in np.flatnonzero(animals != J.NO_ANIMAL)}


def test_the_premise_the_far_corner_costs_more_than_the_opening_bank():
    """Guard the setup itself, so this suite fails loudly if land prices or the stake ever move."""
    assert C.land_cost(SE_TILE) == SE_LAND_COST
    assert SE_LAND_COST > C.OPENING_BANK
    assert R.quadrant_of(*SE_TILE) == "SE"


def _genome(tile, land_day=0, start_day=0, n_slots=8):
    g = np.zeros((n_slots, len(C.GENES)), dtype=np.int64)
    # The block gene selects a pen *group* now, so pick the single-pen group on this tile.
    group_i = next(i for i, g in enumerate(C.RANCH_GROUPS) if g == (tile,))
    row = [C.KINDS.index("ranch"), R.ANIMAL_NAMES.index("COW"), group_i,
           C.START_DAY_CHOICES.index(start_day), C.LAND_DAY_CHOICES.index(land_day)]
    g[0] = row + [0] * (len(C.GENES) - len(row))
    return g.reshape(-1)


def test_a_pen_on_unaffordable_ground_does_not_appear_somewhere_else():
    """The core claim: whatever pens exist stand on the tiles that were asked for.

    Deliberately at the `decode()` layer rather than `ranch()`. A routine is handed one tile and one
    day and cannot know what the farm can afford -- that depends on every *other* chain's land orders
    and on whether anything has been earned yet. Affordability is a whole-genome property, so
    `decode()` is where it is decided and where this has to be tested.
    """
    script, _used, _skipped = C.decode(_genome(SE_TILE), 8)
    tiles = _animal_tiles(_run(script))
    assert tiles <= {SE_TILE}, (
        f"asked for a pen on {SE_TILE}, which the farm never unlocks, and got animals on "
        f"{sorted(tiles)} instead -- the walk stopped at the border and built there")


def test_ground_bought_out_of_revenue_is_still_allowed():
    """The other side of the rule, and the one that matters more.

    Waiting is worth real money and the leader buys on days 7 and 10, so a late parcel must NOT be
    refused just because the opening bank could not have covered it on day 0.

    Uses a **one-parcel** tile deliberately. `SE_TILE` needs all three parcels -- $7,000 -- and since
    2026-08-05 the gate weighs the amount as well as the day, so $7,000 on day 10 is correctly refused
    against an estimated $3,000 bank. That refusal is the point of the gate, not a regression: what has
    to keep working is the cheap parcel the leader actually buys.
    """
    ne = next(t for t in C.RANCH_TILES if R.land_purchases_for(t) == 1)
    _script, used, skipped = C.decode(_genome(ne, land_day=7, start_day=11), 8)
    assert skipped == 0, "a $1,000 parcel funded by a week of revenue was refused as unaffordable"
    assert any(u[0] == "ranch" and ne in u[2] for u in used)


def test_the_border_tile_is_where_it_actually_lands():
    """Pins the mechanism, not just the symptom, so a future fix cannot pass by accident.

    Walking `(4,4)` -> `(7,8)` is EAST x3 then SOUTH x4. The eastward legs cross NE, which is bought.
    Every southward leg enters SE, which is not, so all four are ignored and the unit is left on
    `(7,4)` -- exactly where the $64,146 genome put one of its cows.
    """
    s = R.ranch(R.Script(), "COW", SE_TILE, start_day=0, land_day=0, unit=1)
    tiles = _animal_tiles(_run(s))
    if tiles == {SE_TILE} or not tiles:
        pytest.skip("relocation no longer happens; this mechanism test has served its purpose")
    assert tiles == {(7, 4)}, f"expected the border tile (7, 4), got {sorted(tiles)}"


def test_decode_does_not_report_a_chain_it_could_not_place():
    """`decode()` returns `used` and `skipped` so an unusable genome reads as unusable rather than as
    a weak strategy. A chain that relocates is unusable and is currently counted as used."""
    g = np.zeros((8, len(C.GENES)), dtype=np.int64)
    group_i = next(i for i, g in enumerate(C.RANCH_GROUPS) if g == (SE_TILE,))
    row = [C.KINDS.index("ranch"), R.ANIMAL_NAMES.index("COW"), group_i,
           C.START_DAY_CHOICES.index(0), C.LAND_DAY_CHOICES.index(0)]
    g[0] = row + [0] * (len(C.GENES) - len(row))
    script, used, skipped = C.decode(g.reshape(-1), 8)
    placed = _animal_tiles(_run(script))
    claimed = {t for u in used if u[0] == "ranch" for t in u[2]}
    assert claimed <= placed, (
        f"decode reports pens at {sorted(claimed)} with {skipped} skipped, but the season ends with "
        f"animals at {sorted(placed)}")


def test_two_different_far_tiles_are_not_the_same_farm():
    """The degeneracy, stated directly: distinct genomes must not collapse to identical action tapes.

    If they do, the beam is paying to evaluate duplicates and cannot see past them.
    """
    far = [t for t in C.RANCH_TILES if R.quadrant_of(*t) == "SE"]
    if len(far) < 2:
        pytest.skip("needs at least two SE ranch tiles to compare")
    a = R.ranch(R.Script(), "COW", far[0], start_day=0, land_day=0, unit=1)
    b = R.ranch(R.Script(), "COW", far[1], start_day=0, land_day=0, unit=1)
    assert _animal_tiles(_run(a)) != _animal_tiles(_run(b)), (
        f"pens ordered on {far[0]} and {far[1]} produce the same farm; the search cannot tell these "
        f"two genomes apart")
