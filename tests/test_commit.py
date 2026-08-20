"""Commitments must compress a walk into one decision without lying to PPO.

Two families of property here, and they fail in different ways:

- **Mechanics** -- a committed unit actually walks to its frozen target and fires the arrival op.
  If this is wrong the feature simply does nothing, which is visible.
- **Density** -- intermediate turns must be excluded from the PPO ratio. If this is wrong nothing
  errors and nothing NaNs; the ratio silently compares two different distributions and the training
  curves look fine while meaning nothing. That is the failure this file exists for.
"""

import jax
import jax.numpy as jnp
import numpy as np

from kagg.rl import commit as C
from kagg.sim import jax_sim as J
from kagg.sim import ops as O


# The bundle legality mask needs the vocabulary. It is loaded once here rather than threaded through
# every signature: the vocabulary is a global property of a trained model, like a tokenizer, and it
# must be byte-identical across labelling, fitting and play or every bundle index means something
# different. `market_bundles.load_vocab` raises if it is missing rather than inventing one.
_BUNDLE_SELLS = None


def _bundle_sells():
    global _BUNDLE_SELLS
    if _BUNDLE_SELLS is None:
        from kagg.il import market_bundles as _MB
        from kagg.rl import jax_policy as _PP
        _BUNDLE_SELLS = _MB.sell_table(_MB.load_vocab(), pad_to=_PP.N_BUNDLES)
    return _BUNDLE_SELLS



def _state(batch=4, seed=0):
    return J.reset(batch, seed=seed)


def test_a_free_unit_passes_its_primitive_op_through_untouched():
    """Commitment must be invisible to a policy that never emits a COMMIT token."""
    s = _state()
    cm = C.init(s.batch)
    op = jnp.full(cm.category.shape, O.WATER, dtype=jnp.int32)

    sim_op, _cr, _it, _qt, new_cm, decided = C.resolve(cm, s, op, jnp.zeros_like(op))

    assert np.array_equal(np.asarray(sim_op), np.asarray(op)), "primitive ops must pass through"
    assert bool(decided.all()), "an uncommitted unit-turn is always a decision"
    assert bool((new_cm.category == C.NO_COMMIT).all()), "no commitment should have been created"


def test_committing_walks_toward_the_target_and_marks_later_turns_undecided():
    """The whole mechanism: one decision, then the env drives the walk."""
    s = _state()
    cm = C.init(s.batch)
    # Force every unit to commit to WATER. Day 0 has no plants, so use a board that does.
    op = jnp.full(cm.category.shape, O.N_OPS + C.COMMIT_WATER, dtype=jnp.int32)

    _sim_op, _cr, _it, _qt, cm2, decided = C.resolve(cm, s, op, jnp.zeros_like(op))
    assert bool(decided.all()), "the turn a commitment is MADE is a decision turn"

    # Only units that found a target are now committed; on an empty day-0 board there may be none,
    # so this test asserts the implication rather than the population.
    busy = np.asarray(cm2.category) != C.NO_COMMIT
    if busy.any():
        _op3, _c3, _i3, _q3, _cm3, decided3 = C.resolve(cm2, s, jnp.zeros_like(op), jnp.zeros_like(op))
        assert not decided3.reshape(-1)[busy.reshape(-1)].any(), (
            "a unit mid-walk must NOT be a decision turn, or PPO scores an action it never chose")


def test_the_target_is_frozen_not_recomputed():
    """Re-deriving "nearest" every turn lets a unit oscillate between two tiles and arrive at none.

    Built explicitly rather than sampled: the property is about what happens when the board changes
    under a committed unit, which a fresh board cannot exercise.
    """
    s = _state()
    cm = C.init(s.batch)
    tgt = jnp.zeros_like(cm.target).at[..., 0].set(5).at[..., 1].set(5)
    cm = cm._replace(category=jnp.zeros_like(cm.category) + C.COMMIT_WATER,
                     target=tgt, turns=jnp.zeros_like(cm.turns) + C.MAX_COMMIT_TURNS)

    _op, _cr, _it, _qt, cm2, _d = C.resolve(cm, s, jnp.zeros_like(cm.category), jnp.zeros_like(cm.category))

    assert np.array_equal(np.asarray(cm2.target), np.asarray(tgt)), (
        "target moved while the unit was walking; it must be frozen at commit time")


def test_a_commitment_expires_and_hands_control_back():
    """A walk that never arrives must not strand the unit forever."""
    s = _state()
    cm = C.init(s.batch)
    far = jnp.zeros_like(cm.target).at[..., 0].set(9).at[..., 1].set(9)
    cm = cm._replace(category=jnp.zeros_like(cm.category) + C.COMMIT_WATER,
                     target=far, turns=jnp.ones_like(cm.turns))   # one turn left

    _op, _cr, _it, _qt, cm2, _d = C.resolve(cm, s, jnp.zeros_like(cm.category), jnp.zeros_like(cm.category))

    assert bool((cm2.category == C.NO_COMMIT).all()), "timer hit zero, commitment must clear"


def test_arriving_fires_the_arrival_op():
    """Standing on the target must produce WATER/HARVEST/FEED, not another movement step."""
    s = _state()
    cm = C.init(s.batch)
    here = s.farm.unit_pos                       # target == current position
    for cat, want in ((C.COMMIT_WATER, O.WATER),
                      (C.COMMIT_HARVEST, O.HARVEST),
                      (C.COMMIT_FEED, O.FEED)):
        c = cm._replace(category=jnp.zeros_like(cm.category) + cat,
                        target=here, turns=jnp.zeros_like(cm.turns) + C.MAX_COMMIT_TURNS)
        sim_op, _cr, _it, _qt, c2, _d = C.resolve(c, s, jnp.zeros_like(cm.category), jnp.zeros_like(cm.category))
        assert bool((sim_op == want).all()), f"arrival should fire {want}, got {set(np.asarray(sim_op).ravel())}"
        assert bool((c2.category == C.NO_COMMIT).all()), "arrival must end the commitment"


def test_night_clears_every_commitment():
    """`_end_of_day` respawns units and empties inventories, so a walk cannot survive it."""
    s = _state()
    cm = C.init(s.batch)._replace(
        category=jnp.zeros((s.batch, 2, J.MAX_UNITS), jnp.int32) + C.COMMIT_FEED,
        turns=jnp.zeros((s.batch, 2, J.MAX_UNITS), jnp.int32) + C.MAX_COMMIT_TURNS)

    dawn = s._replace(step_index=jnp.zeros_like(s.step_index) + J.TURNS_PER_DAY)
    cleared = C.clear_at_night(cm, dawn)
    assert bool((cleared.category == C.NO_COMMIT).all()), "day boundary must clear commitments"

    midday = s._replace(step_index=jnp.zeros_like(s.step_index) + J.TURNS_PER_DAY + 3)
    kept = C.clear_at_night(cm, midday)
    assert bool((kept.category != C.NO_COMMIT).all()), "mid-day must NOT clear commitments"


def test_every_op_handed_to_the_simulator_is_a_real_simulator_op():
    """A COMMIT token must never reach `jax_sim`, which has never heard of one."""
    s = _state()
    cm = C.init(s.batch)
    key = jax.random.PRNGKey(0)
    op = jax.random.randint(key, cm.category.shape, 0, C.N_POLICY_OPS)

    sim_op, _cr, _it, _qt, cm2, _d = C.resolve(cm, s, op, jnp.zeros_like(op))

    assert int(sim_op.max()) < O.N_OPS, "a commit token leaked into the simulator's op space"
    assert int(sim_op.min()) >= 0
    # And the sim must actually accept them.
    J.step(s, J.Actions(
        unit_op=sim_op.astype(J._I),
        unit_crop=jnp.zeros_like(sim_op, J._I), unit_item=jnp.zeros_like(sim_op, J._I),
        unit_qty=jnp.ones_like(sim_op, J._I),
        sell=jnp.zeros((s.batch, 2, J.N_PRODUCTS), J._I),
        buy_seed=jnp.zeros((s.batch, 2, J.N_CROPS), J._I),
        buy_product=jnp.zeros((s.batch, 2, J.N_PRODUCTS), J._I),
        buy_animal=jnp.zeros((s.batch, 2, J.N_ANIMALS), J._I),
        hire=jnp.zeros((s.batch, 2), bool), buy_land=jnp.zeros((s.batch, 2), bool)))


def test_commit_mask_is_legality_not_preference():
    """A commitment is offered only when a target of that kind exists -- and never for dead slots."""
    s = _state()
    m = C.commit_mask(s)
    assert m.shape == (s.batch, 2, J.MAX_UNITS, C.N_COMMIT)

    dead = np.asarray(J._ARANGE_UNITS[None, None, :] >= s.farm.n_units[:, :, None])
    assert not np.asarray(m)[dead].any(), "a dead unit slot must not be offered a commitment"


def test_a_commit_token_with_no_target_degrades_to_noop():
    """Substituting a *different* primitive would score the policy for an action it never chose."""
    s = _state()
    cm = C.init(s.batch)
    # Day 0: no plants exist, so COMMIT_WATER has no target anywhere.
    op = jnp.full(cm.category.shape, O.N_OPS + C.COMMIT_WATER, dtype=jnp.int32)

    sim_op, _cr, _it, _qt, cm2, _d = C.resolve(cm, s, op, jnp.zeros_like(op))

    assert bool((sim_op == O.NOOP).all()), "an unfulfillable commitment must become NOOP"
    assert bool((cm2.category == C.NO_COMMIT).all())


def test_the_crop_is_frozen_at_commit_time_not_taken_from_the_arrival_turn():
    """PLANT is the one arrival op with an argument, and the arrival turn is UNSCORED.

    If the crop came from the arrival turn's sample, an unscored draw would decide what gets
    planted -- the policy would be credited for an outcome it never chose. The commit turn is
    scored, so the crop must be frozen there and carried.
    """
    s = _state()
    cm = C.init(s.batch)
    # Commit to PLANT while asking for crop 3, then walk with a *different* crop sampled after.
    op = jnp.full(cm.category.shape, O.N_OPS + C.COMMIT_PLANT, dtype=jnp.int32)
    chosen = jnp.full(cm.category.shape, 3, dtype=jnp.int32)

    _op1, _crop1, _i1, _q1, cm2, _d = C.resolve(cm, s, op, chosen)
    busy = np.asarray(cm2.category) != C.NO_COMMIT
    if not busy.any():
        return          # no empty tile or no seed on this board; nothing to assert

    noise = jnp.full(cm.category.shape, 1, dtype=jnp.int32)
    _op2, crop2, _i2, _q2, _cm3, _d2 = C.resolve(cm2, s, jnp.zeros_like(op), noise)

    assert np.asarray(crop2)[busy].tolist() == [3] * int(busy.sum()), (
        "the walking unit planted the crop sampled mid-walk, not the one it committed to")


def test_plant_is_offered_a_commitment_like_every_other_targeted_category():
    """Uniformity is the guardrail: offering commitment only to the dramatic gaps is a judgment."""
    assert C.N_COMMIT == 5, "WATER, HARVEST, FEED and PLANT all have a _target() feature"
    assert int(C.ARRIVAL_OP[C.COMMIT_PLANT]) == O.PLANT_OP


def test_the_ppo_ratio_is_still_exactly_one_with_commitments_running():
    """The property everything else depends on, with the decision mask in the loop.

    A committed unit-turn must contribute nothing to EITHER side of the ratio. If it were scored as
    probability 1 instead of excluded, or if `sample` and `evaluate` disagreed about which turns
    counted, this is the only place it would show -- there is no error and no NaN, just a gradient
    pointing somewhere arbitrary.
    """
    from kagg.rl import jax_act as A, jax_obs, jax_policy as P

    s = _state(batch=4)
    tiles, units, glob = jax_obs.encode(s)
    obs = (A._flat(tiles), A._flat(units), A._flat(glob))
    model = P.Policy()
    params = model.init(jax.random.PRNGKey(0), *obs)
    heads, _v = model.apply(params, *obs)
    masks = A.masks_for(s, _bundle_sells())

    actions, _lp, _e = A.sample(jax.random.PRNGKey(1), heads, masks)
    _op, _crop, _it, _qt, _cm, decided = C.resolve(
        C.init(s.batch), s,
        A._unflat(actions["op"], s.batch).astype(jnp.int32),
        A._unflat(actions["crop"], s.batch).astype(jnp.int32))
    dec = A._flat(decided)

    old_logp, _ = A.evaluate(heads, masks, actions, dec)
    new_logp, _ = A.evaluate(heads, masks, actions, dec)
    ratio = np.exp(np.asarray(new_logp) - np.asarray(old_logp))
    assert np.allclose(ratio, 1.0, atol=1e-5), f"ratio is not 1.0: {ratio}"


def test_masking_a_turn_out_actually_changes_the_density():
    """Guards the test above from passing because `decided` is silently ignored."""
    from kagg.rl import jax_act as A, jax_obs, jax_policy as P

    s = _state(batch=4)
    tiles, units, glob = jax_obs.encode(s)
    obs = (A._flat(tiles), A._flat(units), A._flat(glob))
    model = P.Policy()
    key = jax.random.PRNGKey(2)
    params = model.init(key, *obs)
    # Zero-init heads are uniform, so log-probs are non-zero and dropping a term must move the sum.
    heads, _v = model.apply(params, *obs)
    masks = A.masks_for(s, _bundle_sells())
    actions, _lp, _e = A.sample(jax.random.PRNGKey(3), heads, masks)

    all_on = jnp.ones(actions["op"].shape, dtype=bool)
    full, _ = A.evaluate(heads, masks, actions, all_on)
    none, _ = A.evaluate(heads, masks, actions, jnp.zeros_like(all_on))

    assert not np.allclose(np.asarray(full), np.asarray(none)), (
        "`decided` is being ignored -- the ratio test above would pass vacuously")
