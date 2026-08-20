"""The property PPO's ratio depends on: `evaluate` must score what `sample` drew.

`ratio = exp(logp_new - logp_old)` is only a ratio of the *same* distribution if the update scores
the stored action under the same factorisation the behaviour policy sampled it from. Break that and
PPO silently optimises a comparison between two unrelated objects -- no error, no NaN, just a
gradient pointing somewhere arbitrary.

It became easy to break when the market heads stopped being independent. `sell` and `buy_product`
now carry a trade-mode axis and are read through `condition_on_trade`, so scoring them against a
marginal over modes -- or against the wrong mode -- would look completely normal and be wrong.

`crop`, `item` and `qty` now carry an op axis and are read through `condition_on_op` for exactly
the same reason. The op case is the more dangerous of the two, because `active_unit_heads` already
zeroes those heads for ops that ignore them -- so a conditioning bug hides on every slot except the
PLANT / PICKUP / PLACE ones, which is a minority of them, and shows up as a ratio that is *almost*
one.
"""

import jax
import jax.numpy as jnp
import numpy as np

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
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



def _setup(seed=0, batch=2):
    state = J.reset(batch, seed=seed)
    model = P.Policy()
    tiles, units, glob = jax_obs.encode(state)
    obs = (A._flat(tiles), A._flat(units), A._flat(glob))
    params = model.init(jax.random.PRNGKey(seed), *obs)
    heads, _value = model.apply(params, *obs)
    return heads, A.masks_for(state, _bundle_sells())


def test_evaluate_reproduces_the_log_prob_sample_returned():
    """The whole correctness property, in one assertion."""
    heads, masks = _setup()
    actions, logp_sampled, _ent = A.sample(jax.random.PRNGKey(1), heads, masks)
    logp_scored, _ent2 = A.evaluate(heads, masks, actions)

    assert np.allclose(np.asarray(logp_sampled), np.asarray(logp_scored), atol=1e-5), (
        f"sample and evaluate disagree: {np.asarray(logp_sampled)} vs {np.asarray(logp_scored)}")


def test_the_product_heads_really_are_conditioned_on_the_trade_mode():
    """If the mode did not select a slice, this would pass for the wrong reason.

    Scoring the same actions under a *different* trade mode must give a different log-prob --
    otherwise `condition_on_trade` is a no-op and the factorisation is still mean-field.
    """
    heads, masks = _setup()
    # Make the slices genuinely differ; a zero-initialised head is identical across modes, so the
    # test would pass trivially on an untrained network.
    key = jax.random.PRNGKey(2)
    heads = dict(heads)
    for k in A.CONDITIONED_HEADS:
        key, sub = jax.random.split(key)
        heads[k] = jax.random.normal(sub, heads[k].shape)

    actions, _lp, _e = A.sample(jax.random.PRNGKey(3), heads, masks)
    as_drawn, _ = A.evaluate(heads, masks, actions)

    other = dict(actions)
    other["trade"] = (actions["trade"] + 1) % P.N_TRADE_MODES
    as_other, _ = A.evaluate(heads, masks, other)

    assert not np.allclose(np.asarray(as_drawn), np.asarray(as_other), atol=1e-4), (
        "changing the trade mode did not change the score, so the product heads are not "
        "conditioned on it")


def test_the_unit_heads_carry_an_op_axis():
    """The shape is the change; if this is wrong nothing below means anything."""
    heads, _masks = _setup()
    assert heads["crop"].shape[-2:] == (P.N_OPS, J.N_CROPS)
    assert heads["item"].shape[-2:] == (P.N_OPS, J.N_ITEMS)
    assert heads["qty"].shape[-2:] == (P.N_OPS, len(P.UNIT_QTY_BUCKETS))


def test_condition_on_op_selects_a_different_slice_per_op():
    """Isolated: no active-set masking, no op log-prob, just the gather."""
    heads, _masks = _setup()
    key = jax.random.PRNGKey(5)
    heads = dict(heads)
    for k in A.OP_CONDITIONED_HEADS:
        key, sub = jax.random.split(key)
        heads[k] = jax.random.normal(sub, heads[k].shape)

    op = jnp.zeros(heads["op"].shape[:-1], dtype=jnp.int32)
    a = A.condition_on_op(heads, op + O.PLANT_OP)
    b = A.condition_on_op(heads, op + O.PICKUP)

    for k in A.OP_CONDITIONED_HEADS:
        assert a[k].shape == heads[k].shape[:-2] + (heads[k].shape[-1],), (
            f"{k} must lose the op axis once conditioned")
        assert not np.allclose(np.asarray(a[k]), np.asarray(b[k])), (
            f"{k} is identical under two different ops, so condition_on_op is a no-op")


def test_scoring_under_the_wrong_op_slice_changes_the_answer():
    """The conditioning is isolated here, and it has to be, or the test proves nothing.

    Changing the op inside `actions` would move three things at once: which slice is selected, the
    op head's own log-prob, and -- via `active_unit_heads` -- which heads are counted at all. It
    would also push most slots to the `-1e9` illegal floor, where both sides saturate and compare
    equal for entirely the wrong reason.

    So `actions` is held fixed and only the heads handed to `_score` are re-conditioned. The active
    set, the chosen indices and the op log-prob are then identical by construction, and the *only*
    thing that can move the total is which argument slice `crop`/`item`/`qty` were read from.
    """
    heads, masks = _setup()
    key = jax.random.PRNGKey(6)
    heads = dict(heads)
    for k in A.OP_CONDITIONED_HEADS:
        key, sub = jax.random.split(key)
        heads[k] = jax.random.normal(sub, heads[k].shape)

    actions, _lp, _e = A.sample(jax.random.PRNGKey(7), heads, masks)

    # PLANT is illegal for every unit at reset -- nobody holds seed -- so a sampled op set contains
    # no slot that reads an argument head, and the comparison below would be vacuous. The op is
    # therefore assigned rather than drawn, and `masks["op"]` is relaxed so the assignment does not
    # push every slot to the illegal floor where both sides saturate equal. Op *legality* is not
    # what is under test here; `tests/test_jax_masks.py` owns that.
    masks = {**masks, "op": jnp.ones_like(masks["op"])}
    actions = {**actions, "op": jnp.full_like(actions["op"], O.PLANT_OP)}
    assert bool(A.active_unit_heads(actions["op"])["crop"].all()), "every slot should read a crop"

    as_drawn, _ = A._score(A.condition_all(heads, actions), masks, actions)

    wrong = {**actions, "op": jnp.full_like(actions["op"], O.PICKUP)}
    as_wrong, _ = A._score(A.condition_all(heads, wrong), masks, actions)

    assert not np.allclose(np.asarray(as_drawn), np.asarray(as_wrong), atol=1e-4), (
        "conditioning on a different op gave the same score, so the argument heads are not "
        "conditioned on the op at all")


def test_the_ppo_ratio_is_exactly_one_before_the_params_move():
    """The gate the spec named. `exp(new - old)` must be 1 when nothing has changed.

    This is the failure mode that produces training curves which look fine and lie: if `sample` and
    `evaluate` disagree about the factorisation, PPO's ratio compares two different distributions
    and every downstream number is meaningless. It costs one forward pass to check.
    """
    heads, masks = _setup()
    actions, old_logp, _e = A.sample(jax.random.PRNGKey(8), heads, masks)
    new_logp, _e2 = A.evaluate(heads, masks, actions)

    ratio = np.exp(np.asarray(new_logp) - np.asarray(old_logp))
    assert np.allclose(ratio, 1.0, atol=1e-5), f"PPO ratio is not 1.0 at init: {ratio}"


def test_every_head_the_simulator_reads_is_sampled():
    """`to_sim_actions` indexes every head, so a missing one is a KeyError at rollout time."""
    heads, masks = _setup()
    actions, _lp, _e = A.sample(jax.random.PRNGKey(4), heads, masks)

    sim = A.to_sim_actions(actions, batch=2)

    assert sim.unit_op.shape == (2, 2, J.MAX_UNITS)
    assert sim.sell.shape == (2, 2, J.N_PRODUCTS)
    assert "trade" in actions, "the conditioning variable must be stored, or evaluate cannot reuse it"
