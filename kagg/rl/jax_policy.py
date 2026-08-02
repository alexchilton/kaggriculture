"""The per-turn policy: an entity transformer over tiles, units and one global token.

## Why this shape

`docs/lessons_carried_over.md` records the entity transformer as the one architectural win that
transferred cleanly from Orbit Wars, and every top finisher in that competition whose write-up we
have used one. The farm is a set of 100 tiles and up to 24 units, not an image: a unit cares about
the tile it stands on and about which other tiles still need work, and attention expresses that
directly while a convolution has to rediscover it.

## Why the action space is factored, not joint

A unit picks an op (18), and PLANT/PICKUP/PLACE need a crop (5), an item (12) and a quantity (4).
Jointly that is over 4000 outcomes per unit and 24 units per turn. Factoring the heads turns it
into a few hundred logits, which is the difference between a tractable policy and the action space
blow-up that `docs/rl_postmortem_and_fix_plan.md` blames for the last collapse.

**The factorisation is autoregressive, not independent, and that distinction was load-bearing.**
This file used to claim the heads were "conditionally independent given the state, so the joint
log-prob is the sum -- exact, not an approximation". That is true for *scoring* a log-prob and
false for *producing* an action, and `CLAUDE.md` records the cost: argmax over independent
marginals emits zero market orders, because nine separate "probably not" decisions compose into
"never", while independent sampling from those same marginals fires combinations the joint never
contains. The marginals were never the problem -- they discriminate 12:1 -- the decode was.

So the conditioning variables are drawn first and the dependent heads read the slice they select:
`trade` before the per-product quantities, and `op` before the `crop` / `item` / `qty` arguments
that op takes. `p(op) * p(crop|op)` is an exact factorisation of a joint containing the dominant
correlation, and it still costs one forward pass, because each conditioning variable has few enough
values to emit every slice at once. See `jax_act.condition_on_op` and `condition_on_trade`.

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
            # **The unit argument heads are conditioned on the op, not independent of it.**
            #
            # This is the same correction as the market heads below, applied to the other half of
            # the action space, and it is the second half of Ender's solution -- whose first half,
            # KL-to-prior, is what reversed this project's decline. A unit picks an op and then the
            # argument that op takes; `p(crop)` marginalised over all 18 ops is not a distribution
            # any unit ever acts from. PLANT wants a crop the shed has seed for, PICKUP wants an
            # item that is on the ground, PLACE wants one that is in hand -- and a single marginal
            # has to average those into something that suits none of them.
            #
            # The failure it produces is quieter than the market one, because `active_unit_heads`
            # already zeroes these heads for ops that ignore them. So the damage is confined to the
            # PLANT / PICKUP / PLACE slots: exactly the productive ops, and exactly the ones a
            # replay shows the policy failing to use.
            #
            # Cost is one slice per op on three small heads -- about 46k parameters, and no extra
            # forward pass, because the conditioning variable is drawn from a head this same pass
            # already produced.
            "crop": nn.Dense(N_OPS * J.N_CROPS, **D)(utok)
                      .reshape(-1, n_units, N_OPS, J.N_CROPS),
            "item": nn.Dense(N_OPS * J.N_ITEMS, **D)(utok)
                      .reshape(-1, n_units, N_OPS, J.N_ITEMS),
            "qty": nn.Dense(N_OPS * len(UNIT_QTY_BUCKETS), **D)(utok)
                      .reshape(-1, n_units, N_OPS, len(UNIT_QTY_BUCKETS)),
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


# ---- checkpoint migration ----------------------------------------------------------------------

# Kernel and bias for each of `crop`, `item`, `qty` -- the only leaves the op axis can touch.
N_OP_EXPANDED_LEAVES = 2 * len(("crop", "item", "qty"))


def migrate_params(old, template):
    """Load pre-op-axis params into the current architecture, tiling the argument heads.

    **Why this exists rather than "retrain from scratch".** Giving `crop`/`item`/`qty` an op axis
    changes three kernels, and nothing else: the trunk, `op`, the value head and every market head
    keep their shapes. A straight `pickle.load` still fails, which would strand every BC checkpoint
    -- and, more seriously, `--kl-prior`, which loads a *second* network of the same architecture.
    The KL-to-prior anchor is the change that reversed this project's decline; losing it to a decode
    fix would be a bad trade.

    **Tiling is exact, not an approximation.** The new head reads slice `op` of a flat
    `[N_OPS * K]` output, so writing the old `[K]` kernel into every slice initialises
    `p(arg | op)` to the old marginal `p(arg)` for every op -- which *is* the mean-field policy the
    checkpoint was trained as. Day-one behaviour is therefore identical, and the op axis starts
    learning the deviation from a warm point rather than from zero.

    The migration is shape-driven rather than keyed on Flax's `Dense_7`-style autonames, because
    those renumber silently if a head is ever added above them. It asserts that exactly
    `N_OP_EXPANDED_LEAVES` leaves were expanded, so a partial migration cannot pass quietly.
    """
    from flax.traverse_util import flatten_dict, unflatten_dict

    flat_old, flat_new = flatten_dict(old), flatten_dict(template)
    if set(flat_old) != set(flat_new):
        missing = sorted("/".join(p) for p in set(flat_new) - set(flat_old))
        extra = sorted("/".join(p) for p in set(flat_old) - set(flat_new))
        raise ValueError(
            f"checkpoint does not match this architecture; missing {missing}, unexpected {extra}")

    out, expanded = {}, []
    for path, new_leaf in flat_new.items():
        o = jnp.asarray(flat_old[path])
        if o.shape == new_leaf.shape:
            out[path] = o
        elif (o.ndim == new_leaf.ndim and o.shape[:-1] == new_leaf.shape[:-1]
                and new_leaf.shape[-1] == o.shape[-1] * N_OPS):
            # `[.., K] -> [.., N_OPS * K]`, laid out as op-major so that flat index `op * K + k`
            # is slice `op`'s entry `k`. `tile` repeats the whole K-block, which is exactly that.
            out[path] = jnp.tile(o, (1,) * (o.ndim - 1) + (N_OPS,))
            expanded.append("/".join(path))
        else:
            raise ValueError(
                f"cannot migrate {'/'.join(path)}: {o.shape} -> {new_leaf.shape}")

    if len(expanded) != N_OP_EXPANDED_LEAVES:
        raise ValueError(
            f"expected to expand {N_OP_EXPANDED_LEAVES} leaves onto the op axis, expanded "
            f"{len(expanded)}: {sorted(expanded)}. The checkpoint is not a pre-op-axis one.")
    return unflatten_dict(out)


def load_or_migrate(raw, template):
    """`raw` params as-is when they already fit, migrated when they are pre-op-axis."""
    from flax.traverse_util import flatten_dict

    flat_raw, flat_new = flatten_dict(raw), flatten_dict(template)
    if set(flat_raw) == set(flat_new) and all(
            jnp.shape(flat_raw[p]) == jnp.shape(v) for p, v in flat_new.items()):
        return raw
    return migrate_params(raw, template)


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
