"""The property PPO's ratio depends on: `evaluate` must score what `sample` drew.

`ratio = exp(logp_new - logp_old)` is only a ratio of the *same* distribution if the update scores
the stored action under the same factorisation the behaviour policy sampled it from. Break that and
PPO silently optimises a comparison between two unrelated objects -- no error, no NaN, just a
gradient pointing somewhere arbitrary.

It became easy to break when the market heads stopped being independent. `sell` and `buy_product`
now carry a trade-mode axis and are read through `condition_on_trade`, so scoring them against a
marginal over modes -- or against the wrong mode -- would look completely normal and be wrong.
"""

import jax
import jax.numpy as jnp
import numpy as np

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J


def _setup(seed=0, batch=2):
    state = J.reset(batch, seed=seed)
    model = P.Policy()
    tiles, units, glob = jax_obs.encode(state)
    obs = (A._flat(tiles), A._flat(units), A._flat(glob))
    params = model.init(jax.random.PRNGKey(seed), *obs)
    heads, _value = model.apply(params, *obs)
    return heads, A.masks_for(state)


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


def test_every_head_the_simulator_reads_is_sampled():
    """`to_sim_actions` indexes every head, so a missing one is a KeyError at rollout time."""
    heads, masks = _setup()
    actions, _lp, _e = A.sample(jax.random.PRNGKey(4), heads, masks)

    sim = A.to_sim_actions(actions, batch=2)

    assert sim.unit_op.shape == (2, 2, J.MAX_UNITS)
    assert sim.sell.shape == (2, 2, J.N_PRODUCTS)
    assert "trade" in actions, "the conditioning variable must be stored, or evaluate cannot reuse it"
