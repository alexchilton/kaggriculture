"""Turn sampled policy heads into a `jax_sim.Actions`, and score them for the PPO update.

Kept apart from the network so that "what the policy predicts" and "what the simulator is told"
have exactly one bridge between them. When those two drift apart the symptom is a policy that
trains happily and plays nothing like its rollouts, which is very hard to see from a loss curve.

Every head is **sampled** every turn, because the simulator reads a value from every slot. Only the
heads the chosen op actually consults are **scored** -- see `active_unit_heads`.

That distinction was originally the other way round here, on the argument that scoring every head
keeps the PPO ratio a ratio of the same distribution. The argument is technically sound and the
conclusion was still wrong: the unscored draws never touch the environment, so the effective policy
is the marginal over the fields that matter, and scoring the rest adds a zero-mean gradient over
roughly four times more parameters than the decision involved. Removing it dropped measured entropy
from ~100 nats to ~15, which is the size of the noise that was being carried.
"""

import jax
import jax.numpy as jnp

from kagg.rl import jax_masks, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

UNIT_HEADS = ("op", "crop", "item", "qty")
MARKET_HEADS = ("sell", "buy_product", "buy_seed", "buy_animal", "hire", "buy_land")
ALL_HEADS = UNIT_HEADS + MARKET_HEADS

# Heads that carry a per-trade-mode axis and are read through `condition_on_trade`. Only the
# per-product quantity heads: those are the ones a teacher decides *together*, and the ones where
# treating nine marginals as a joint produced an agent that emitted no orders at all under argmax
# and spent its bank on noise under independent sampling.
CONDITIONED_HEADS = ("sell", "buy_product")


def _flat(x):
    """[B, P, ...] -> [B*P, ...]; both seats run through the network as one batch."""
    return x.reshape(-1, *x.shape[2:])


def _unflat(x, b):
    return x.reshape(b, 2, *x.shape[1:])


def masks_for(state):
    """Every head's legality mask, in network-flat layout."""
    b = state.farm.money.shape[0]
    op = jax_masks.unit_op_mask(state)
    crop = jax_masks.unit_crop_mask(state)
    item = jax_masks.unit_item_mask(state)
    qty = jnp.ones((b, 2, J.MAX_UNITS, len(P.UNIT_QTY_BUCKETS)), dtype=bool)
    market = jax_masks.market_masks(state, P.SELL_BUCKETS, P.BUY_BUCKETS)
    # Every trade mode is always legal: it is a coordinating latent, not a claim about the board,
    # and the per-product masks still enforce what the shed and the bank can actually support.
    trade = jnp.ones((b, 2, P.N_TRADE_MODES), dtype=bool)
    out = {"op": op, "crop": crop, "item": item, "qty": qty, "trade": trade, **market}
    return {k: _flat(v) for k, v in out.items()}


def forward(params, model, state):
    """Run the network on a sim state. Returns `(heads, value, masks)`, all network-flat."""
    tiles, units, glob = jax_obs.encode(state)
    heads, value = model.apply(params, _flat(tiles), _flat(units), _flat(glob))
    return heads, value, masks_for(state)


def active_unit_heads(op):
    """[B, U] bool per conditional head: does the chosen op actually read this field?

    **Heads the op ignores must not contribute to the density or the entropy.** They are still
    sampled -- the simulator wants a value in every slot -- but scoring them is pure variance: the
    gradient `advantage * grad log pi(sampled)` lands on a head whose sampled value had no causal
    effect on the outcome. It is zero-mean, so unbiased, but it dilutes a fixed advantage budget
    across roughly four times more parameters than the decision needed, and in a finite batch it
    can push irrelevant heads toward confident nonsense purely from sampling noise -- which then
    shows up as "entropy fell" and reads as learning.

    Masking them out is the standard hierarchical-policy treatment (AlphaStar does exactly this)
    and loses nothing: the effective policy is the marginal over the fields that matter, and the
    ignored draws are auxiliary randomness that never touches the environment.
    """
    is_plant = op == O.PLANT_OP
    takes_item = (op == O.PICKUP) | (op == O.PLACE)
    return {
        "op": jnp.ones_like(is_plant),      # the op head always decides something
        "crop": is_plant,                   # only PLANT reads a crop
        "item": takes_item,                 # only PICKUP and PLACE read an item
        "qty": takes_item,                  # ...and a quantity
    }


def _reduce(x, active=None):
    """Sum a head's per-element contribution to one scalar per seat, zeroing inactive elements."""
    if active is not None:
        x = jnp.where(active, x, 0.0)
    return x.reshape(x.shape[0], -1).sum(axis=-1)


def condition_on_trade(heads, trade):
    """Select each product head's slice for the sampled trade mode.

    `sell` and `buy_product` carry a `[.., N_PRODUCTS, N_TRADE_MODES, K]` axis; once the mode is
    drawn, the conditional distribution over products is the corresponding slice. This is what makes
    the factorisation `p(trade) * prod_i p(product_i | trade)` exact rather than mean-field -- the
    per-product decisions share one coordinating variable, which is how a teacher actually trades.
    """
    idx = trade[..., None, None, None]                    # [.., 1, 1, 1]
    out = dict(heads)
    for k in CONDITIONED_HEADS:
        out[k] = jnp.take_along_axis(heads[k], jnp.broadcast_to(
            idx, heads[k].shape[:-2] + (1, heads[k].shape[-1])), axis=-2)[..., 0, :]
    return out


def sample(key, heads, masks):
    """Sample every head. Returns `(actions, log_prob, entropy)` with log_prob summed per seat.

    Every head is sampled, because the simulator reads a value from every slot. Only the heads the
    chosen op actually consults are *scored* -- see `active_unit_heads`.

    **`trade` is drawn first and the product heads are conditioned on it.** Sampling them
    independently is what produced an agent that banked $1: nine calibrated marginals drawn
    separately give combinations the joint never contains.
    """
    keys = jax.random.split(key, len(ALL_HEADS) + 1)
    actions = {"trade": P.sample_head(keys[-1], heads["trade"], masks["trade"])[0]}
    conditioned = condition_on_trade(heads, actions["trade"])

    for k, sub in zip(ALL_HEADS, keys):
        actions[k] = P.sample_head(sub, conditioned[k], masks[k])[0]

    active = active_unit_heads(actions["op"])
    logps, entropies = [], []
    for k in ALL_HEADS + ("trade",):
        src = conditioned[k] if k in CONDITIONED_HEADS else heads[k]
        lp, ent = P.eval_head(src, masks[k], actions[k])
        a = active.get(k)
        logps.append(_reduce(lp, a))
        entropies.append(_reduce(ent, a))
    return actions, sum(logps), sum(entropies)


def evaluate(heads, masks, actions):
    """Score stored actions under current params, for the ratio in the PPO objective.

    The active set is derived from the *stored* op, so behaviour and update agree on exactly which
    heads were part of the decision. Deriving it from anything else would make the ratio a ratio of
    two different distributions.

    **The trade mode is conditioned on for the same reason and it is not optional.** The behaviour
    policy drew its products from the slice its sampled mode selected, so scoring them under a
    different slice -- or under a marginal over modes -- would put a different distribution in the
    numerator of the PPO ratio than the one that generated the data. `p(trade)` is scored too, so
    the density is the full `p(trade) * prod_i p(product_i | trade)` and the ratio stays a ratio of
    the same object.
    """
    active = active_unit_heads(actions["op"])
    conditioned = condition_on_trade(heads, actions["trade"])
    logps, entropies = [], []
    for k in ALL_HEADS + ("trade",):
        src = conditioned[k] if k in CONDITIONED_HEADS else heads[k]
        lp, ent = P.eval_head(src, masks[k], actions[k])
        a = active.get(k)
        logps.append(_reduce(lp, a))
        entropies.append(_reduce(ent, a))
    return sum(logps), sum(entropies)


def to_sim_actions(actions, batch):
    """Assemble a `jax_sim.Actions` from sampled heads.

    The market heads emit *quantities per product*; `Game._order_book` compacts them into the ten
    order slots in the canonical order agents write them, so the policy never learns slot ordering.
    """
    u = lambda k: _unflat(actions[k], batch)   # noqa: E731

    return J.Actions(
        unit_op=u("op").astype(J._I),
        unit_crop=u("crop").astype(J._I),
        unit_item=u("item").astype(J._I),
        unit_qty=P.UNIT_QTY_BUCKETS[u("qty")].astype(J._I),
        sell=P.SELL_BUCKETS[u("sell")].astype(J._I),
        buy_seed=P.BUY_BUCKETS[u("buy_seed")].astype(J._I),
        buy_product=P.BUY_BUCKETS[u("buy_product")].astype(J._I),
        buy_animal=u("buy_animal").astype(J._I),
        hire=u("hire").astype(bool),
        buy_land=u("buy_land").astype(bool),
    )
