"""The composition test. A real state, the real mask, a real sample, stepped by the real simulator.

**Why this exists.** `tests/test_the_bundle_head_reaches_the_simulator.py` hand-builds action dicts
and asserts on their contents. It passed 18 green while `jax_act.masks_for` crashed on EVERY call,
because no test ever called it: it reads `state.private.shed` and `jax_sim.State` has no `private`
field. That is CLAUDE.md's "a gate only tests what it exercises", for the fourth recorded time in
this project -- single-unit scripts, then a JAX suite with no atomic-PLANT rule, then 300 episodes
that never contested the market, now this.

So this test asserts almost nothing about values. It asserts the pipeline RUNS, end to end, on the
objects the trainer and the agent actually pass around:

    J.reset -> model.apply -> masks_for -> sample -> to_sim_actions -> J.step

If any link is broken -- a wrong attribute, a shape that cannot broadcast, a head the network does
not emit -- this fails. That is the whole job.
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg.il import market_bundles as MB
from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J


@pytest.fixture(scope="module")
def world():
    """A real batch-of-two sim state, a real initialised policy, and a real bundle vocabulary."""
    batch = 2
    state = J.reset(batch)
    model = P.Policy()
    tiles, units, glob = jax_obs.encode(state)
    params = model.init(jax.random.PRNGKey(0), A._flat(tiles), A._flat(units), A._flat(glob))

    vocab = MB.Vocabulary.from_bundles([
        MB.bundle_of([]),
        MB.bundle_of([["HIRE"]] * 10),
        MB.bundle_of([["SELL", "WHEAT", 4]]),
        MB.bundle_of([["BUY_SEED", "WHEAT", 2]]),
    ])
    return batch, state, model, params, vocab


def test_masks_for_runs_on_a_real_state(world):
    """The bug that 18 green tests missed: `masks_for` never executed once."""
    batch, state, model, params, vocab = world
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    assert set(masks) >= set(A.ALL_HEADS), "every head the sampler reads needs a mask"


def test_the_bundle_mask_matches_the_head_width(world):
    """`valid_table` returns `vocab.size` entries; the head is `N_BUNDLES` wide. They must meet."""
    batch, state, model, params, vocab = world
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    assert masks["bundle"].shape[-1] == P.N_BUNDLES, (
        "bundle mask is %d wide against a %d-wide head -- these cannot broadcast, and a gather on "
        "an unmasked dead index clamps silently under jit rather than raising"
        % (masks["bundle"].shape[-1], P.N_BUNDLES))


def test_a_bundle_outside_the_vocabulary_is_masked_illegal(world):
    """Padding rows must be ILLEGAL, not merely absent.

    JAX clamps out-of-range gather indices under jit, so an unmasked padding index would silently
    decode as the highest-numbered real bundle -- a wrong order, emitted confidently, with nothing
    raised anywhere.
    """
    batch, state, model, params, vocab = world
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    pad = np.asarray(masks["bundle"])[:, vocab.size:]
    assert pad.size > 0, "vocabulary already fills the head; widen the test vocabulary"
    assert not pad.any(), "padding bundles are selectable"


def test_a_sell_is_LEGAL_even_when_the_shed_is_empty(world):
    """The mask deliberately does NOT consult the shed. This asserts the reversal, with its reason.

    It used to refuse any bundle selling a product the shed lacked. Three measurements removed that:

      - the reference simply declines an unbacked sell, `_commit_unit` at
        `reference/kaggriculture.py:653` returning False -- no penalty, no error;
      - 48.75% of the TEACHER's own SELL orders have a pre-turn shed of zero for that product, and
        none of them coincide with a same-turn DROP: they are the hourly re-offer;
      - the BC loss is permissive, so a strict play mask vetoed bundles the student was trained to
        emit, on 52% of sell-turns, and handed their probability to a different trade.

    A student that cannot emit what its teacher emitted cannot imitate it.
    """
    batch, state, model, params, vocab = world
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    sell_wheat = vocab.index(MB.bundle_of([["SELL", "WHEAT", 4]]))
    assert np.asarray(masks["bundle"])[:, sell_wheat].all(), (
        "selling wheat on an empty shed is masked out; the environment refuses it harmlessly and "
        "the teacher does it constantly")
    # ...and the empty bundle is always available, or the policy has no legal move at all.
    assert np.asarray(masks["bundle"])[:, 0].all()


def test_sample_then_step_completes_a_turn(world):
    """End to end. This is the test whose absence let a dead branch look healthy."""
    batch, state, model, params, vocab = world
    tables = {k: jnp.asarray(v) for k, v in MB.tables(vocab, pad_to=P.N_BUNDLES).items()}
    tiles, units, glob = jax_obs.encode(state)
    heads, _value = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))

    actions, log_prob, entropy = A.sample(jax.random.PRNGKey(1), heads, masks)
    assert np.all(np.isfinite(np.asarray(log_prob))), "log_prob must be finite for the PPO ratio"

    sim_actions = A.to_sim_actions(actions, batch, tables)
    nxt = J.step(state, sim_actions)
    assert int(np.asarray(nxt.step_index)[0]) == int(np.asarray(state.step_index)[0]) + 1


def test_the_sampled_bundle_is_always_a_legal_one(world):
    """A sampler that can draw a masked-out class makes the legality mask decorative."""
    batch, state, model, params, vocab = world
    tiles, units, glob = jax_obs.encode(state)
    heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    for seed in range(8):
        actions, _lp, _e = A.sample(jax.random.PRNGKey(seed), heads, masks)
        drawn = np.asarray(actions["bundle"])
        legal = np.asarray(masks["bundle"])
        assert legal[np.arange(len(drawn)), drawn].all(), "sampled an illegal bundle"


def test_evaluate_agrees_with_sample(world):
    """`evaluate` scores stored actions under current params -- it is the PPO ratio's numerator.

    If it disagrees with `sample` about shapes or conditioning, the ratio is between two different
    distributions and every policy gradient is wrong in a way no loss curve reveals.
    """
    batch, state, model, params, vocab = world
    tiles, units, glob = jax_obs.encode(state)
    heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
    masks = A.masks_for(state, MB.valid_table(vocab, pad_to=P.N_BUNDLES))
    actions, log_prob, _e = A.sample(jax.random.PRNGKey(3), heads, masks)
    again, _ent = A.evaluate(heads, masks, actions)
    assert np.allclose(np.asarray(log_prob), np.asarray(again), atol=1e-4)
