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

# Heads that carry a per-op axis and are read through `condition_on_op`: the arguments an op takes.
# A unit picks an op and *then* what to do it with, so `p(crop)` averaged over all 18 ops is not a
# distribution any unit acts from.
OP_CONDITIONED_HEADS = ("crop", "item", "qty")

# The conditioning variables themselves, drawn before the heads that read them. `op` is per unit
# and `trade` is per seat, but they play the same role and are stored in `actions` for exactly the
# same reason: `evaluate` cannot reconstruct the slice the behaviour policy used without them.
CONDITION_HEADS = ("trade", "op")


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


def _select_slice(heads, keys, index):
    """Gather each named head's slice at `index` along its second-to-last axis.

    Shared by both conditioning steps because they are the same operation: a head shaped
    `[.., C, K]` carries one length-`K` distribution per value of a conditioning variable, and once
    that variable is drawn the conditional distribution is the corresponding slice. `index` must
    broadcast against `heads[k].shape[:-2]`.
    """
    out = dict(heads)
    for k in keys:
        idx = jnp.broadcast_to(index, heads[k].shape[:-2])[..., None, None]
        idx = jnp.broadcast_to(idx, heads[k].shape[:-2] + (1, heads[k].shape[-1]))
        out[k] = jnp.take_along_axis(heads[k], idx, axis=-2)[..., 0, :]
    return out


def condition_on_trade(heads, trade):
    """Select each product head's slice for the sampled trade mode.

    `sell` and `buy_product` carry a `[.., N_PRODUCTS, N_TRADE_MODES, K]` axis; once the mode is
    drawn, the conditional distribution over products is the corresponding slice. This is what makes
    the factorisation `p(trade) * prod_i p(product_i | trade)` exact rather than mean-field -- the
    per-product decisions share one coordinating variable, which is how a teacher actually trades.
    """
    # `trade` is one value per seat, `[N]`, against heads whose leading axes are `[N, N_PRODUCTS]`:
    # every product in a seat reads the same mode, which is the entire point of a coordinating
    # latent, so it broadcasts across the product axis.
    return _select_slice(heads, CONDITIONED_HEADS, trade[..., None])


def condition_on_op(heads, op):
    """Select each argument head's slice for the sampled op, per unit.

    `crop`, `item` and `qty` carry a `[.., MAX_UNITS, N_OPS, K]` axis. Unlike `trade` the
    conditioning variable is **per unit**, not per seat -- each unit picks its own op and reads its
    own argument distribution -- so `op` is `[N, MAX_UNITS]` and indexes elementwise rather than
    broadcasting.

    **Why this is not redundant with `active_unit_heads`, and how much it actually buys.** That
    function decides *whether* a head counts; this one decides *which distribution* it is. But it
    only buys something where **two or more ops read the same head**, and that is worth stating
    precisely, because the first version of this docstring got it wrong:

    - `crop` is read by PLANT alone. `active_unit_heads` already confined it to PLANT slots, so
      the old single head was *already* `p(crop | PLANT)` and the op axis adds nothing but
      untrained slices. Measured after a BC retrain: the PLANT slice moves, every other slice sits
      at exactly uniform. This head is along for the ride.
    - `item` and `qty` are read by **both** PICKUP and PLACE, and those two teacher distributions
      are nearly disjoint (total variation 0.900 -- you pick up what is on the ground and place
      what is in hand). A single head has to average them. That averaging is the real thing this
      function removes.

    So the claim to make for the unit heads is narrow: it is a fix for `item`/`qty`, not for
    `crop`. The broader argument for autoregressive decode still rests on the market heads, where
    nine products share one head and the decode was measurably destroying the joint.
    """
    return _select_slice(heads, OP_CONDITIONED_HEADS, op)


def condition_all(heads, actions):
    """Apply both conditioning steps, in the order the variables are drawn.

    One function so that no caller can remember one step and forget the other -- and there are now
    five call sites outside this module, including the KL prior and two offline decoders.
    """
    return condition_on_op(condition_on_trade(heads, actions["trade"]), actions["op"])


def _score(conditioned, masks, actions, decided=None):
    """Log-prob and entropy of `actions` under already-conditioned heads, summed per seat.

    **`sample` and `evaluate` both come through here, and that is deliberate.** The PPO ratio is
    only a ratio of one distribution if the update scores the stored action under the same
    factorisation the behaviour policy sampled from. Two copies of this loop is how that drifts:
    the divergence produces no error and no NaN, just a gradient pointing somewhere arbitrary and a
    training curve that looks healthy. `tests/test_jax_act.py` pins `ratio == 1.0` at init, but a
    single code path is the reason it stays true rather than the reason we would find out.
    """
    active = active_unit_heads(actions["op"])
    # **A unit walking out a commitment contributes nothing to the density.**
    #
    # Not scored as probability 1 -- excluded. Both `logp` and the entropy for that unit-turn drop
    # out of the sum, so the term is identical under old and new parameters and `exp(0 - 0) = 1`
    # for that slot by construction. That is the same trick `active` already plays for heads an op
    # does not read, and it is why a multi-turn commitment cannot corrupt the PPO ratio: there is
    # no second code path to drift, only a wider mask on the one that already exists.
    if decided is not None:
        active = {k: v & decided for k, v in active.items()}
    logps, entropies = [], []
    for k in ALL_HEADS + ("trade",):
        lp, ent = P.eval_head(conditioned[k], masks[k], actions[k])
        a = active.get(k)
        logps.append(_reduce(lp, a))
        entropies.append(_reduce(ent, a))
    return sum(logps), sum(entropies)


def sample(key, heads, masks):
    """Sample every head. Returns `(actions, log_prob, entropy)` with log_prob summed per seat.

    Every head is sampled, because the simulator reads a value from every slot. Only the heads the
    chosen op actually consults are *scored* -- see `active_unit_heads`.

    **The two conditioning variables are drawn first, and the heads that read them are conditioned
    before they are sampled.** `trade` before the per-product quantities, `op` before the `crop` /
    `item` / `qty` arguments. Sampling the products independently is what produced an agent that
    banked $1 -- nine calibrated marginals drawn separately give combinations the joint never
    contains -- and the same argument applies to `item`/`qty`, which PICKUP and PLACE both read and
    which a single head therefore has to average across two nearly disjoint distributions.
    """
    keys = jax.random.split(key, len(ALL_HEADS) + 1)
    # `op` is ALL_HEADS[0], so it consumes keys[0] here and is skipped in the loop below: the key
    # assignment is unchanged from when it was drawn inline, and no key is used twice.
    actions = {
        "trade": P.sample_head(keys[-1], heads["trade"], masks["trade"])[0],
        "op": P.sample_head(keys[0], heads["op"], masks["op"])[0],
    }
    conditioned = condition_all(heads, actions)

    for k, sub in zip(ALL_HEADS, keys):
        if k in CONDITION_HEADS:
            continue
        actions[k] = P.sample_head(sub, conditioned[k], masks[k])[0]

    return actions, *_score(conditioned, masks, actions)


def evaluate(heads, masks, actions, decided=None):
    """Score stored actions under current params, for the ratio in the PPO objective.

    The active set is derived from the *stored* op, so behaviour and update agree on exactly which
    heads were part of the decision. Deriving it from anything else would make the ratio a ratio of
    two different distributions.

    **Both conditioning variables are read from storage for the same reason, and neither is
    optional.** The behaviour policy drew its products from the slice its sampled trade mode
    selected and its crop from the slice its sampled op selected. Scoring either under a different
    slice -- or under a marginal over the conditioning variable -- would put a different
    distribution in the numerator of the PPO ratio than the one that generated the data. `p(trade)`
    and `p(op)` are scored too, so the density is the full
    `p(trade) * p(op) * prod p(product|trade) * prod p(arg|op)` and the ratio stays a ratio of the
    same object.

    `decided` is the stored per-unit "this turn was a decision" mask from the rollout. Passing the
    stored one rather than recomputing it is the same discipline as deriving the active set from the
    stored op: recomputing would let the update disagree with behaviour about which turns counted.
    """
    return _score(condition_all(heads, actions), masks, actions, decided)


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
