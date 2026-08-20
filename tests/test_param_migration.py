"""Pre-op-axis checkpoints must load, and must mean the same thing after they load.

Giving `crop`/`item`/`qty` an op axis changes three kernels. Every BC checkpoint and -- more
importantly -- every `--kl-prior` anchor predates that change, so without a migration the one fix
that reversed this project's decline could not be loaded at all.

Shape compatibility is the easy half and the useless half. The property that matters is that tiling
the old kernel across the op axis reproduces the *old distribution* on every slice: if it does, the
migrated network is behaviourally identical to the checkpoint on day one and the op axis is a warm
start rather than a reset.
"""

import jax
import jax.numpy as jnp
import numpy as np
import pytest

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J


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



def _obs(seed=0, batch=2):
    state = J.reset(batch, seed=seed)
    tiles, units, glob = jax_obs.encode(state)
    return (A._flat(tiles), A._flat(units), A._flat(glob)), A.masks_for(state, _bundle_sells())


def _old_style_params(template, key):
    """`template` with the three argument heads collapsed back to their pre-op-axis widths.

    Built by shrinking the current tree rather than by pickling an old one, so the test does not
    depend on a binary artifact that will drift out of the repo.
    """
    from flax.traverse_util import flatten_dict, unflatten_dict

    flat = flatten_dict(template)
    out = {}
    for path, leaf in flat.items():
        key, sub = jax.random.split(key)
        leaf = jax.random.normal(sub, leaf.shape) * 0.1
        # The three expanded heads are exactly the leaves whose last axis is a multiple of N_OPS
        # *and* which the migration would expand; identify them the same way the migration does.
        if leaf.shape[-1] % P.N_OPS == 0 and path[-2].startswith("Dense") and any(
                leaf.shape[-1] == P.N_OPS * w
                for w in (J.N_CROPS, J.N_ITEMS, len(P.UNIT_QTY_BUCKETS))):
            leaf = leaf[..., : leaf.shape[-1] // P.N_OPS]
        out[path] = leaf
    return unflatten_dict(out)


def test_migration_expands_exactly_the_three_argument_heads():
    obs, _masks = _obs()
    model = P.Policy()
    template = model.init(jax.random.PRNGKey(0), *obs)
    old = _old_style_params(template, jax.random.PRNGKey(1))

    migrated = P.migrate_params(old, template)

    from flax.traverse_util import flatten_dict
    for path, leaf in flatten_dict(template).items():
        assert flatten_dict(migrated)[path].shape == leaf.shape, f"{path} has the wrong shape"


def test_migrated_params_give_the_same_distribution_on_every_op_slice():
    """The behavioural property: `p(arg | op)` is the old marginal `p(arg)`, for every op."""
    obs, _masks = _obs()
    model = P.Policy()
    template = model.init(jax.random.PRNGKey(0), *obs)
    old = _old_style_params(template, jax.random.PRNGKey(2))

    heads, _v = model.apply(P.migrate_params(old, template), *obs)

    for k, width in (("crop", J.N_CROPS), ("item", J.N_ITEMS),
                     ("qty", len(P.UNIT_QTY_BUCKETS))):
        h = np.asarray(heads[k])
        assert h.shape[-2:] == (P.N_OPS, width)
        first = h[..., 0, :]
        for op in range(1, P.N_OPS):
            assert np.allclose(h[..., op, :], first, atol=1e-5), (
                f"{k} slice {op} differs from slice 0, so the tiling is not op-major")


def test_a_migrated_checkpoint_still_satisfies_the_ppo_ratio_gate():
    """Migration must not break the property the whole update depends on."""
    obs, masks = _obs()
    model = P.Policy()
    template = model.init(jax.random.PRNGKey(0), *obs)
    heads, _v = model.apply(P.migrate_params(_old_style_params(template, jax.random.PRNGKey(3)),
                                             template), *obs)

    actions, old_logp, _e = A.sample(jax.random.PRNGKey(9), heads, masks)
    new_logp, _e2 = A.evaluate(heads, masks, actions)

    ratio = np.exp(np.asarray(new_logp) - np.asarray(old_logp))
    assert np.allclose(ratio, 1.0, atol=1e-5), f"ratio is not 1.0 after migration: {ratio}"


def test_current_params_pass_through_untouched():
    """`load_or_migrate` must be a no-op on an already-current checkpoint, not a re-tile."""
    obs, _masks = _obs()
    model = P.Policy()
    template = model.init(jax.random.PRNGKey(0), *obs)

    assert P.load_or_migrate(template, template) is template


def test_a_tree_that_is_neither_shape_is_rejected_loudly():
    """A genuinely incompatible checkpoint must raise, not be silently half-migrated."""
    obs, _masks = _obs()
    model = P.Policy()
    template = model.init(jax.random.PRNGKey(0), *obs)

    from flax.traverse_util import flatten_dict, unflatten_dict
    flat = flatten_dict(template)
    victim = next(p for p in flat if p[-1] == "kernel")
    flat[victim] = jnp.zeros((flat[victim].shape[0] + 3, flat[victim].shape[1]))

    with pytest.raises(ValueError, match="cannot migrate"):
        P.migrate_params(unflatten_dict(flat), template)
