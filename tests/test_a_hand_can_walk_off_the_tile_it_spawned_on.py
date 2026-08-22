"""A hand spawns on a LOCKED shed-access tile. It must be allowed to walk off it.

**The defect.** `jax_masks.can_move` required the destination tile to be unlocked:

    unlocked = ... t.kind[target] != J.LOCKED
    return inside & unlocked

The reference has no such rule, and says why in a comment written for this exact case
(`reference/kaggriculture.py:327-329`):

    # Movement onto LOCKED tiles is allowed: a hand can spawn on a locked
    # shed-access tile, and blocking movement would strand it there forever.
    # Tile operations (PLANT, WATER, etc.) still no-op on LOCKED tiles.

`jax_masks`' own contract is "would the reference silently no-op this?" -- and for movement the
answer is no, it executes it.

**What it cost.** Measured 2026-08-22 on tape `92498144`, turn 1, day 0, only NW unlocked. The crew
stands at `farmer (4,4)` and hands `(5,4) (4,5) (5,5) (4,4) (5,4)` -- the four shed-access tiles,
three of which are LOCKED because the NW quadrant is `x < 5, y < 5`. For the hand at `(5,5)` every
one of the four neighbours is LOCKED, so under the old mask it could not move at all, ever.

The teacher's label for that hand on that turn is `WEST`. So:

  - `greedy_action` argmaxes over `_masked_logits`, so WEST carried -1e9 and was unemittable at any
    parameter setting;
  - `bc_dagger.py:226` zeroes the loss on labels the mask calls illegal, so it never reached the
    gradient either.

Two independent locks. The checkpoint sat at `WEST 24/25 = 0.960` for ten rounds in a four-game run
and sixteen in a single-game run, while every other op read 1.000 -- 162 of 163 exact, one action
permanently wrong. Driving alone that one stranded hand dragged whole-season op agreement to ~0.78,
and every hypothesis raised to explain that number -- aliasing, opponent conditioning, capacity, the
beta anneal -- was explaining a masking bug.

Tile ops are NOT changed: the reference does still no-op PLANT/WATER/HARVEST on a LOCKED tile, and
`unit_op_mask` must keep refusing them.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import jax_masks
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

#: The four shed-access tiles on a 10x10 board. Three are outside the NW quadrant (`x < 5, y < 5`)
#: and therefore LOCKED on day 0, which is what makes this reachable at all.
SHED_ACCESS = [(4, 4), (5, 4), (4, 5), (5, 5)]
MOVES = {O.NORTH: (0, -1), O.SOUTH: (0, 1), O.EAST: (1, 0), O.WEST: (-1, 0)}


def state_with_unit_at(x, y):
    """A fresh day-0 state with unit 0 of seat 0 standing at `(x, y)`."""
    st = J.reset(1)
    pos = np.asarray(st.farm.unit_pos).copy()
    pos[0, 0, 0] = (x, y)
    farm = st.farm._replace(unit_pos=jnp.asarray(pos, dtype=J._I))
    return st._replace(farm=farm)


def op_mask_at(x, y):
    st = state_with_unit_at(x, y)
    return np.asarray(jax_masks.unit_op_mask(st))[0, 0, 0], st


def test_the_spawn_tiles_really_are_locked_on_day_zero():
    """If this fails the fixture has drifted and every assertion below is vacuous."""
    st = J.reset(1)
    kind = np.asarray(st.tiles.kind)[0, 0]
    locked = [(x, y) for x, y in SHED_ACCESS if kind[y * J.BOARD + x] == J.LOCKED]
    assert (5, 5) in locked, (
        "the hand's spawn tile is not LOCKED on day 0, so the stranding case this test pins "
        "cannot occur -- the board or the quadrant rule changed")
    assert len(locked) == 3, "expected three of the four shed-access tiles locked, got %r" % locked


def test_a_hand_on_a_locked_tile_can_still_walk():
    """The bug, at the exact state that produced it: (5,5) on day 0, every neighbour LOCKED."""
    mask, _st = op_mask_at(5, 5)
    legal = [op for op in MOVES if mask[op]]
    assert legal, (
        "the hand at (5,5) has NO legal move. It spawned on a locked shed-access tile and the mask "
        "has stranded it for the whole season -- exactly what reference/kaggriculture.py:327-329 "
        "says must not happen")
    assert mask[O.WEST], "WEST is the teacher's own label for this hand on turn 1"


def test_every_in_bounds_move_is_legal_regardless_of_lock():
    """Movement legality is bounds ONLY, matching the reference."""
    for x, y in SHED_ACCESS + [(0, 0), (9, 9), (5, 4), (4, 5)]:
        mask, _st = op_mask_at(x, y)
        for op, (dx, dy) in MOVES.items():
            nx, ny = x + dx, y + dy
            inside = 0 <= nx < J.BOARD and 0 <= ny < J.BOARD
            assert bool(mask[op]) == inside, (
                "at (%d,%d) op %d: mask says %s, in-bounds is %s -- movement must depend on the "
                "board edge and nothing else" % (x, y, op, bool(mask[op]), inside))


def test_the_board_edge_still_blocks():
    """The half of the rule that stays. A corner unit cannot walk off the board."""
    mask, _st = op_mask_at(0, 0)
    assert not mask[O.WEST] and not mask[O.NORTH]
    assert mask[O.EAST] and mask[O.SOUTH]


def test_tile_ops_are_still_refused_on_a_locked_tile():
    """The reference DOES no-op PLANT/WATER/HARVEST on LOCKED. Only movement changed."""
    mask, st = op_mask_at(5, 5)
    kind = np.asarray(st.tiles.kind)[0, 0]
    assert kind[5 * J.BOARD + 5] == J.LOCKED
    for op in (O.PLANT_OP, O.WATER, O.HARVEST, O.BUILD_COOP, O.BUILD_PASTURE):
        assert not mask[op], (
            "op %d became legal on a LOCKED tile; only movement was supposed to change" % op)
