"""The shed is reachable from a LOCKED shed-access tile. PICKUP, DROP and PLACE must be legal there.

**Same defect as `test_a_hand_can_walk_off_the_tile_it_spawned_on.py`, one line further down.**
`jax_masks.unit_op_mask` built its shed predicate as:

    on_shed = (idx[..., None] == J.SHED_TILES).any(axis=-1) & (kind != J.LOCKED)

The reference does not have that second term, and says so in a comment written for this exact case
(`reference/kaggriculture.py:337-340`):

    # Shed operations resolve before the LOCKED guard. They use the tile only as
    # a standing position -- the shed itself is always owned -- and three of the
    # four shed-access tiles start LOCKED, so guarding them first would make the
    # shed unreachable from those tiles.

`_apply_unit_action` handles DROP, PICKUP and PLACE *above* `if tile == "LOCKED": return`, and each
one tests `_is_shed_adjacent((fx, fy), board_size)` and nothing else about the tile.

Our own fast simulator already agrees with the reference -- `jax_sim.py:683` is `on_shed = (idx ==
SHED_TILES).any(-1)` with no lock term, which is why 300/300 episodes of parity pass. Only the RL
mask disagreed, and the mask is compared to nothing by that gate.

**Cost.** Two independent locks, exactly as before: `greedy_action` argmaxes over `_masked_logits`
so the op is unemittable, and `bc_dagger.py:226` zeroes the loss on labels the mask calls illegal so
it never reaches the gradient. Three of the four shed-access tiles are LOCKED on day 0 -- (5,4),
(4,5) and (5,5) -- and hands spawn on all of them.

PLACE has two branches and only the shed one changes. Placing an animal still requires a matching
empty structure, which a LOCKED tile can never be.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import jax_masks
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

SHED_ACCESS = [(4, 4), (5, 4), (4, 5), (5, 5)]


def state_at(x, y, carried=None, shed=None):
    """Day-0 state with unit 0 of seat 0 at `(x, y)`, holding `carried`, shed holding `shed`."""
    st = J.reset(1)
    pos = np.asarray(st.farm.unit_pos).copy()
    pos[0, 0, 0] = (x, y)
    car = np.asarray(st.farm.carried).copy()
    car[0, 0, 0, :] = 0
    if carried is not None:
        car[0, 0, 0, carried] = 1
    sh = np.asarray(st.farm.shed).copy()
    sh[0, 0, :] = 0
    if shed is not None:
        sh[0, 0, shed] = 1
    farm = st.farm._replace(
        unit_pos=jnp.asarray(pos, dtype=J._I),
        carried=jnp.asarray(car, dtype=J._I),
        shed=jnp.asarray(sh, dtype=J._I),
    )
    return st._replace(farm=farm)


def mask_at(x, y, carried=None, shed=None):
    st = state_at(x, y, carried, shed)
    return np.asarray(jax_masks.unit_op_mask(st))[0, 0, 0], st


def locked_access_tiles():
    kind = np.asarray(J.reset(1).tiles.kind)[0, 0]
    return [(x, y) for x, y in SHED_ACCESS if kind[y * J.BOARD + x] == J.LOCKED]


def test_the_fixture_has_locked_shed_tiles_to_test():
    """If this fails every assertion below is vacuous -- there would be nothing locked to stand on."""
    locked = locked_access_tiles()
    assert len(locked) == 3, "expected three LOCKED shed-access tiles on day 0, got %r" % locked


def test_pickup_is_legal_from_a_locked_shed_tile():
    for x, y in locked_access_tiles():
        mask, _ = mask_at(x, y, shed=J.WHEAT_ITEM)
        assert mask[O.PICKUP], (
            "PICKUP masked out at (%d,%d) with wheat in the shed. The reference resolves PICKUP "
            "before the LOCKED guard (kaggriculture.py:358-370) and would have executed it." % (x, y))


def test_drop_is_legal_from_a_locked_shed_tile():
    for x, y in locked_access_tiles():
        mask, _ = mask_at(x, y, carried=J.WHEAT_ITEM)
        assert mask[O.DROP], (
            "DROP masked out at (%d,%d) while carrying wheat; the reference executes it "
            "(kaggriculture.py:342-356)." % (x, y))


def test_place_is_legal_from_a_locked_shed_tile():
    for x, y in locked_access_tiles():
        mask, _ = mask_at(x, y, carried=J.WHEAT_ITEM)
        assert mask[O.PLACE], (
            "PLACE masked out at (%d,%d) while carrying wheat; the reference takes the shed-drop "
            "branch there (kaggriculture.py:391-411)." % (x, y))


def test_the_unlocked_shed_tile_was_never_affected():
    """(4,4) is inside NW and always worked. It must keep working."""
    mask, _ = mask_at(4, 4, carried=J.WHEAT_ITEM, shed=J.WHEAT_ITEM)
    assert mask[O.PICKUP] and mask[O.DROP] and mask[O.PLACE]


def test_shed_ops_are_still_refused_away_from_the_shed():
    """The half of the rule that stays: position still decides, on a locked tile or an open one."""
    for x, y in [(0, 0), (2, 2), (7, 7)]:
        assert (x, y) not in SHED_ACCESS
        mask, _ = mask_at(x, y, carried=J.WHEAT_ITEM, shed=J.WHEAT_ITEM)
        assert not mask[O.PICKUP], "PICKUP legal at (%d,%d), which is not shed-adjacent" % (x, y)
        assert not mask[O.DROP], "DROP legal at (%d,%d), which is not shed-adjacent" % (x, y)


def test_pickup_still_needs_something_in_the_shed():
    """Emptiness is a real no-op in the reference and must stay masked."""
    for x, y in locked_access_tiles():
        mask, _ = mask_at(x, y, shed=None)
        assert not mask[O.PICKUP], "PICKUP legal at (%d,%d) with an empty shed" % (x, y)


def test_drop_still_needs_something_carried():
    for x, y in locked_access_tiles():
        mask, _ = mask_at(x, y, carried=None)
        assert not mask[O.DROP], "DROP legal at (%d,%d) carrying nothing" % (x, y)


def test_tile_ops_are_still_refused_on_the_locked_shed_tile():
    """Only the shed ops move. PLANT/WATER/BUILD stay refused, as the reference refuses them."""
    for x, y in locked_access_tiles():
        mask, _ = mask_at(x, y, carried=J.FERT_ITEM, shed=J.WHEAT_ITEM)
        for op in (O.PLANT_OP, O.WATER, O.HARVEST, O.BUILD_COOP, O.BUILD_PASTURE, O.FERTILIZE):
            assert not mask[op], (
                "op %d became legal on LOCKED (%d,%d); only the shed ops were supposed to change"
                % (op, x, y))


def test_commit_pickup_will_walk_to_a_locked_shed_tile():
    """`commit._candidates` carried the same term, and its own docstring says it must not.

    It claims to "mirror `jax_masks.unit_op_mask` exactly" -- and it did, faithfully, including the
    bug. A COMMIT_PICKUP that refuses three of the four shed tiles sends every unit to (4,4).
    """
    from kagg.rl import commit

    st = state_at(0, 0, shed=J.WHEAT_ITEM)
    cand = np.asarray(commit._candidates(st))[commit.COMMIT_PICKUP][0, 0]
    for x, y in locked_access_tiles():
        assert cand[y * J.BOARD + x], (
            "COMMIT_PICKUP will not target the LOCKED shed tile (%d,%d), so no unit can ever be "
            "sent there -- but PICKUP is legal there and the simulator executes it" % (x, y))


def test_commit_pickup_still_needs_stock_and_a_shed_tile():
    """The rest of that predicate must not have moved."""
    from kagg.rl import commit

    empty = np.asarray(commit._candidates(state_at(0, 0, shed=None)))[commit.COMMIT_PICKUP][0, 0]
    assert not empty.any(), "COMMIT_PICKUP has a target with an empty shed"

    stocked = np.asarray(
        commit._candidates(state_at(0, 0, shed=J.WHEAT_ITEM)))[commit.COMMIT_PICKUP][0, 0]
    hits = {(int(i) % J.BOARD, int(i) // J.BOARD) for i in np.flatnonzero(stocked)}
    assert hits == set(SHED_ACCESS), (
        "COMMIT_PICKUP targets %r; it must be exactly the four shed-access tiles" % sorted(hits))


def test_the_mask_agrees_with_the_simulator_that_executes_it():
    """The two must not disagree: `jax_sim` has no lock term on `on_shed`, so neither may the mask.

    Driven through the real simulator rather than by reading it: PICKUP from a LOCKED shed tile has
    to actually move a unit of wheat out of the shed.
    """
    x, y = 5, 5
    assert (x, y) in locked_access_tiles()
    st = state_at(x, y, shed=J.WHEAT_ITEM)
    before = int(np.asarray(st.farm.shed)[0, 0, J.WHEAT_ITEM])
    assert before == 1

    n_units = np.asarray(st.farm.n_units).copy()
    n_units[0, 0] = max(1, int(n_units[0, 0]))
    st = st._replace(farm=st.farm._replace(n_units=jnp.asarray(n_units, dtype=J._I)))

    acts = J.zero_actions(1)
    op = np.asarray(acts.unit_op).copy()
    op[:] = O.NOOP
    op[0, 0, 0] = O.PICKUP
    item = np.asarray(acts.unit_item).copy()
    item[0, 0, 0] = J.WHEAT_ITEM
    qty = np.asarray(acts.unit_qty).copy()
    qty[0, 0, 0] = 1
    acts = acts._replace(
        unit_op=jnp.asarray(op, dtype=J._I),
        unit_item=jnp.asarray(item, dtype=J._I),
        unit_qty=jnp.asarray(qty, dtype=J._I),
    )

    out = J.step(st, acts)
    after = int(np.asarray(out.farm.shed)[0, 0, J.WHEAT_ITEM])
    carried = int(np.asarray(out.farm.carried)[0, 0, 0, J.WHEAT_ITEM])
    assert after == 0 and carried == 1, (
        "the simulator refused a PICKUP from a LOCKED shed tile (shed %d->%d, carried %d). If this "
        "fails the simulator has the bug too and the parity gate is wrong, not just the mask."
        % (before, after, carried))

    mask = np.asarray(jax_masks.unit_op_mask(st))[0, 0, 0]
    assert mask[O.PICKUP], (
        "the simulator executed the PICKUP and the mask calls it illegal -- the mask's contract is "
        "'would the reference silently no-op this?' and the answer here is no")
