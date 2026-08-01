"""The per-turn policy: an entity transformer over tiles, units and one global token.

## Why this shape

`docs/lessons_carried_over.md` records the entity transformer as the one architectural win that
transferred cleanly from Orbit Wars, and every top finisher in that competition whose write-up we
have used one. The farm is a set of 100 tiles and up to 24 units, not an image: a unit cares about
the tile it stands on and about which other tiles still need work, and attention expresses that
directly while a convolution has to rediscover it.

## Why the action space is factored, not joint

A unit picks an op (18), and PLANT/PICKUP/PLACE need a crop (5), an item (12) and a quantity (4).
Jointly that is over 4000 outcomes per unit and 24 units per turn. Factoring into independent heads
turns it into 18+5+12+4 logits, which is the difference between a tractable policy and the action
space blow-up that `docs/rl_postmortem_and_fix_plan.md` blames for the last collapse. The heads are
conditionally independent given the state, so the joint log-prob is the sum -- exact, not an
approximation, because we sample every head every turn.

## Why the market head does not learn slot ordering

`Game._order_book` compacts the convenience arrays into ten slots in the canonical order agents
write them. So the policy emits *quantities per product* and never has to discover that its sells
should precede its buys. That removes a whole permutation problem from the learning task and loses
nothing an agent could express.

## The no-op question

`unit_op_mask` never masks NOOP. A policy that must act every turn learns to thrash, and the
post-mortem is explicit that masking the no-op to force action is a quality judgment, not a
legality one. Standing still is a legitimate move here -- 32% of the winning agent's unit-actions
in episode 89197802 were PASS.
"""

import flax.linen as nn
import jax
import jax.numpy as jnp

from kagg.rl import jax_obs
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

N_OPS = O.N_OPS

# **The policy computes in float32, deliberately and explicitly.**
#
# `jax_sim` turns on `jax_enable_x64` globally, because the reference environment keeps money as a
# Python float and parity has to be exact. With x64 on, anything that does not *state* its dtype
# defaults to float64 -- including `self.param(...)` -- and one float64 positional embedding is
# enough to promote the entire forward pass. This card runs float64 at **1/32** the float32 rate,
# so the symptom is not a wrong answer, it is a policy that trains ~30x too slowly while looking
# perfectly healthy. Measured here: 24 turns/s before, on a simulator that alone does 44,700/s.
#
# So every module and every parameter below pins its dtype. Do not remove these: the default is
# wrong in this project specifically, and the failure is silent.
DTYPE = jnp.float32

# Quantity ladders. Coarse on purpose: the difference between selling 30 and 31 is noise, and every
# extra bucket is another logit to learn. Bucket 0 is always "do nothing", and always legal.
# How many coarse "what kind of market turn is this" modes the per-product heads condition on.
# Three is the smallest number that can express the distinction the data actually shows -- no
# trading, ordinary trading, and liquidating the shed before the 100-item cap destroys the overflow.
N_TRADE_MODES = 3

SELL_BUCKETS = jnp.asarray([0, 1, 3, 10, 30], dtype=jnp.int32)
BUY_BUCKETS = jnp.asarray([0, 1, 2, 5], dtype=jnp.int32)
UNIT_QTY_BUCKETS = jnp.asarray([1, 2, 5, 10], dtype=jnp.int32)


class Block(nn.Module):
    """Pre-LN transformer block. Pre-LN because post-LN needs a warmup to stay stable."""

    d_model: int
    n_heads: int

    @nn.compact
    def __call__(self, x):
        h = nn.LayerNorm(dtype=DTYPE, param_dtype=DTYPE)(x)
        x = x + nn.MultiHeadDotProductAttention(
            num_heads=self.n_heads, qkv_features=self.d_model,
            dtype=DTYPE, param_dtype=DTYPE)(h, h)
        h = nn.LayerNorm(dtype=DTYPE, param_dtype=DTYPE)(x)
        x = x + nn.Sequential([
            nn.Dense(self.d_model * 4, dtype=DTYPE, param_dtype=DTYPE), nn.gelu,
            nn.Dense(self.d_model, dtype=DTYPE, param_dtype=DTYPE),
        ])(h)
        return x


class Policy(nn.Module):
    """Shared trunk, per-unit action heads, market heads and a value head."""

    d_model: int = 128
    n_heads: int = 4
    n_layers: int = 3

    @nn.compact
    def __call__(self, tiles, units, glob):
        """`tiles [N, 100, F]`, `units [N, 24, F]`, `glob [N, F]`, where N = batch * seats."""
        n_tiles = tiles.shape[1]
        n_units = units.shape[1]

        # Separate embeddings per entity type: a tile feature vector and a unit feature vector
        # share no columns, so one projection would have to waste capacity keeping them apart.
        tiles, units, glob = (x.astype(DTYPE) for x in (tiles, units, glob))
        t = nn.Dense(self.d_model, dtype=DTYPE, param_dtype=DTYPE)(tiles)
        u = nn.Dense(self.d_model, dtype=DTYPE, param_dtype=DTYPE)(units)
        g = nn.Dense(self.d_model, dtype=DTYPE, param_dtype=DTYPE)(glob)[:, None, :]

        # Learned positional embedding for tiles only. Units are genuinely permutation-equivalent
        # given their coordinates are already features, but a tile's identity *is* its position.
        # The explicit dtype is load-bearing -- see the DTYPE note at the top of this file.
        t = t + self.param("tile_pos", nn.initializers.normal(0.02),
                           (1, n_tiles, self.d_model), DTYPE)
        u = u + self.param("unit_pos", nn.initializers.normal(0.02),
                           (1, n_units, self.d_model), DTYPE)

        x = jnp.concatenate([g, t, u], axis=1)
        for _ in range(self.n_layers):
            x = Block(self.d_model, self.n_heads)(x)
        x = nn.LayerNorm(dtype=DTYPE, param_dtype=DTYPE)(x)

        gtok = x[:, 0]
        utok = x[:, 1 + n_tiles:]

        # Heads are zero-initialised so the policy starts uniform over legal actions. A policy that
        # starts with strong arbitrary preferences spends its first million steps unlearning them.
        zero = nn.initializers.zeros
        D = dict(kernel_init=zero, dtype=DTYPE, param_dtype=DTYPE)
        heads = {
            "op": nn.Dense(N_OPS, **D)(utok),
            "crop": nn.Dense(J.N_CROPS, **D)(utok),
            "item": nn.Dense(J.N_ITEMS, **D)(utok),
            "qty": nn.Dense(len(UNIT_QTY_BUCKETS), **D)(utok),
            # **The market heads are conditioned on a coarse `trade` decision, not independent.**
            #
            # Emitting nine per-product distributions and reading them as a joint is a mean-field
            # approximation, and it fails in both directions when decoded. Argmax over the
            # marginals emits *zero* orders -- nine separate "probably not sell" decisions compose
            # into "never sell" -- and the agent banks exactly its starting money. Independent
            # sampling from the same marginals banks $1, firing combinations the true joint never
            # produces. The marginals themselves are fine: 12:1 discrimination on `buy_product`
            # between turns the teacher traded and turns it did not. It is the factorisation that
            # loses the information, because a teacher liquidating the shed makes one coordinated
            # decision across products rather than nine coin flips.
            #
            # So each product head emits one slice per trade mode and the mode is sampled first:
            # `p(trade) * prod_i p(product_i | trade)` is an exact factorisation of a joint with
            # the dominant correlation in it, and it still costs a single forward pass because the
            # conditioning variable has only `N_TRADE_MODES` values.
            "trade": nn.Dense(N_TRADE_MODES, **D)(gtok),
            "sell": nn.Dense(J.N_PRODUCTS * N_TRADE_MODES * len(SELL_BUCKETS), **D)(gtok)
                      .reshape(-1, J.N_PRODUCTS, N_TRADE_MODES, len(SELL_BUCKETS)),
            "buy_product": nn.Dense(J.N_PRODUCTS * N_TRADE_MODES * len(BUY_BUCKETS), **D)(gtok)
                      .reshape(-1, J.N_PRODUCTS, N_TRADE_MODES, len(BUY_BUCKETS)),
            "buy_seed": nn.Dense(J.N_CROPS * len(BUY_BUCKETS), **D)(gtok)
                      .reshape(-1, J.N_CROPS, len(BUY_BUCKETS)),
            "buy_animal": nn.Dense(J.N_ANIMALS * 2, **D)(gtok)
                      .reshape(-1, J.N_ANIMALS, 2),
            "hire": nn.Dense(2, **D)(gtok),
            "buy_land": nn.Dense(2, **D)(gtok),
        }
        # **The value head is bounded to [0, 1], and that bound is a fact, not a heuristic.**
        # The reward is 1 for a win and 0 for a loss, paid once, and gamma <= 1 -- so no state can
        # be worth more than 1 or less than 0. Left unbounded it drifts straight past that: with a
        # 64-turn horizon against 719-turn episodes, only about one update in eleven contains a
        # terminal reward, and the other ten train the critic purely on its own predictions. That
        # bootstrap has no unique fixed point at gamma ~ 1, and it was measured climbing to 1.315 --
        # an impossible value -- while `explained_variance` still read +0.98, because a critic that
        # is self-consistently wrong explains its own targets perfectly.
        #
        # A sigmoid makes the impossible unreachable, and costs nothing when the estimate is honest.
        value = nn.sigmoid(nn.Dense(1, dtype=DTYPE, param_dtype=DTYPE)(gtok)[..., 0])
        return heads, value


# ---- distribution helpers ----------------------------------------------------------------------

NEG_INF = jnp.asarray(-1e9, dtype=DTYPE)


def _masked_logits(logits, mask):
    """Illegal options are pushed to -inf, with a fallback so no row is entirely masked."""
    mask = jnp.broadcast_to(mask, logits.shape)
    safe = jnp.where(mask.any(axis=-1, keepdims=True), mask, jnp.ones_like(mask))
    return jnp.where(safe, logits, NEG_INF)


def sample_head(key, logits, mask):
    """Sample one categorical head, returning `(action, log_prob, entropy)`."""
    logits = _masked_logits(logits, mask)
    logp = jax.nn.log_softmax(logits, axis=-1)
    action = jax.random.categorical(key, logits, axis=-1)
    chosen = jnp.take_along_axis(logp, action[..., None], axis=-1)[..., 0]
    p = jnp.exp(logp)
    entropy = -jnp.sum(jnp.where(p > 0, p * logp, 0.0), axis=-1)
    return action, chosen, entropy


def eval_head(logits, mask, action):
    """Log-prob and entropy of an already-chosen action, for the PPO update."""
    logits = _masked_logits(logits, mask)
    logp = jax.nn.log_softmax(logits, axis=-1)
    chosen = jnp.take_along_axis(logp, action[..., None], axis=-1)[..., 0]
    p = jnp.exp(logp)
    entropy = -jnp.sum(jnp.where(p > 0, p * logp, 0.0), axis=-1)
    return chosen, entropy
