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
# **The market is one categorical plus magnitudes.** `bundle` names WHICH orders go out together --
# including how many HIRE slots, which the sim has always read as a count and the old `Dense(2)`
# head could never express. The `qty_*` heads name HOW MANY, and are read only for the products the
# drawn bundle activates. See `kagg/il/market_bundles.py` for the measurement that sized this.
MARKET_HEADS = ("bundle", "qty_sell", "qty_buy_product", "qty_buy_seed")
ALL_HEADS = UNIT_HEADS + MARKET_HEADS

# Heads that carry a per-op axis and are read through `condition_on_op`: the arguments an op takes.
# A unit picks an op and *then* what to do it with, so `p(crop)` averaged over all 18 ops is not a
# distribution any unit acts from.
OP_CONDITIONED_HEADS = ("crop", "item", "qty")

# The conditioning variable, drawn before the heads that read it, and stored in `actions` because
# `evaluate` cannot reconstruct the slice the behaviour policy used without it.
#
# `trade` used to sit here too. It is gone: the bundle IS the coordinating decision now, and it
# coordinates exactly, not through a three-valued latent. The `qty_*` heads need no conditioning
# variable because the bundle already says which of their entries are read at all.
CONDITION_HEADS = ("op",)


def _flat(x):
    """[B, P, ...] -> [B*P, ...]; both seats run through the network as one batch."""
    return x.reshape(-1, *x.shape[2:])


def _unflat(x, b):
    return x.reshape(b, 2, *x.shape[1:])


def masks_for(state, bundle_sells):
    """Every head's legality mask, in network-flat layout.

    `bundle_sells` is `[N_BUNDLES, N_PRODUCTS]` bool -- does bundle `b` sell product `p` -- built
    once from the vocabulary by `market_bundles.sell_table`. It is a REQUIRED argument on purpose.
    A default of "everything is legal" is the failure mode this whole change exists to avoid: the
    policy emits orders that never fill, which looks identical from the outside to a decode that
    emits nothing, and the two have opposite fixes.

    **What this masks, and what it deliberately does not.** A bundle is illegal iff it sells a
    product the shed does not hold -- that is exact, cheap, and the one constraint the agent cannot
    discover by trying. Purchases and hires are NOT masked: their legality depends on price and on
    the Fibonacci hire ladder against a bank that the same turn's sells are still settling into
    (sells occupy earlier order slots), so a mask computed before the turn would be wrong in both
    directions. The simulator already rejects those cleanly, and `_do_hire` failing on a thin bank
    is a real decision the policy should learn to avoid, not one to hide from it.
    """
    b = state.farm.money.shape[0]
    op = jax_masks.unit_op_mask(state)
    crop = jax_masks.unit_crop_mask(state)
    item = jax_masks.unit_item_mask(state)
    qty = jnp.ones((b, 2, J.MAX_UNITS, len(P.UNIT_QTY_BUCKETS)), dtype=bool)

    # A bundle is legal unless it names a SELL for a product the shed is empty of.
    have = state.private.shed > 0                                    # [B, P, N_PRODUCTS]
    wants = jnp.asarray(bundle_sells, dtype=bool)                    # [N_BUNDLES, N_PRODUCTS]
    impossible = jnp.any(wants[None, None, :, :] & ~have[:, :, None, :], axis=-1)
    bundle = ~impossible                                             # [B, P, N_BUNDLES]

    # Quantity ladders are always drawable; the bundle decides which entries are ever read, and
    # bucket 0 is "do nothing", which is legal by construction.
    qty_sell = jnp.ones((b, 2, J.N_PRODUCTS, len(P.SELL_BUCKETS)), dtype=bool)
    qty_buy_product = jnp.ones((b, 2, J.N_PRODUCTS, len(P.BUY_BUCKETS)), dtype=bool)
    qty_buy_seed = jnp.ones((b, 2, J.N_CROPS, len(P.BUY_BUCKETS)), dtype=bool)

    out = {"op": op, "crop": crop, "item": item, "qty": qty, "bundle": bundle,
           "qty_sell": qty_sell, "qty_buy_product": qty_buy_product,
           "qty_buy_seed": qty_buy_seed}
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
    """Apply the conditioning step, on the variable the heads read.

    Kept as its own function even now that there is only one step: five call sites outside this
    module depend on it, including the KL prior and two offline decoders, and the market half used
    to have a step here too. A caller that conditions by hand is a caller that will forget.
    """
    return condition_on_op(heads, actions["op"])


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
    for k in ALL_HEADS:
        lp, ent = P.eval_head(conditioned[k], masks[k], actions[k])
        a = active.get(k)
        logps.append(_reduce(lp, a))
        entropies.append(_reduce(ent, a))
    return sum(logps), sum(entropies)


def sample(key, heads, masks):
    """Sample every head. Returns `(actions, log_prob, entropy)` with log_prob summed per seat.

    Every head is sampled, because the simulator reads a value from every slot. Only the heads the
    chosen op actually consults are *scored* -- see `active_unit_heads`.

    **`op` is drawn first and the argument heads are conditioned on it before they are sampled.**
    PICKUP and PLACE both read `item`/`qty` and their teacher distributions are nearly disjoint
    (total variation 0.900), so a single unconditioned head has to average them.

    **The market needs no such ordering any more.** `bundle` is drawn as one categorical, and the
    `qty_*` heads name magnitudes for entries the bundle has already selected -- so a quantity for a
    product the bundle never mentions is simply never read. Sampling products independently is what
    produced an agent that banked $1: calibrated marginals drawn separately give combinations the
    joint never contains. There are no independent product decisions left to get wrong.
    """
    keys = jax.random.split(key, len(ALL_HEADS) + 1)
    # `op` is ALL_HEADS[0], so it consumes keys[0] here and is skipped in the loop below: the key
    # assignment is unchanged from when it was drawn inline, and no key is used twice.
    actions = {"op": P.sample_head(keys[0], heads["op"], masks["op"])[0]}
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


def to_sim_actions(actions, batch, tables):
    """Assemble a `jax_sim.Actions` from sampled heads.

    `tables` is `market_bundles.tables(vocab)` wrapped in `jnp` arrays: the sampled bundle index
    selects a row, which says WHICH orders go out, and the `qty_*` heads supply HOW MANY for the
    entries that row selected. `Game._order_book` then compacts the result into the ten order slots
    in the canonical order agents write them, so the policy never learns slot ordering.

    **`hire` is a count, taken straight from the bundle row.** It used to be `u("hire").astype(bool)`
    against a simulator that documents the field as "COUNT of hands to hire this turn, not a flag"
    and warns at `jax_sim.py:315` that casting to bool "would collapse 'hire twice' to 'hire once'".
    That cast capped every learned policy at one hand per turn while the teacher's second most
    common market decision is ten hires in a single turn.

    **A selected product always moves at least one unit.** The bundle says "sell wheat" and the
    quantity head could still draw bucket 0, which means "do nothing" -- the two would contradict,
    and the bundle is the decision that carries the coordination. So a selected entry floors at 1,
    matching `market_bundles.to_sim_fields`, where a teacher naming no quantity means one unit.
    """
    u = lambda k: _unflat(actions[k], batch)   # noqa: E731
    idx = u("bundle")

    def gated(selected, buckets, head):
        want = selected[idx]                            # [B, P, K] counts from the bundle row
        drawn = buckets[u(head)].astype(J._I)           # [B, P, K] magnitudes from the qty head
        return jnp.where(want > 0, jnp.maximum(drawn, 1), 0).astype(J._I)

    return J.Actions(
        unit_op=u("op").astype(J._I),
        unit_crop=u("crop").astype(J._I),
        unit_item=u("item").astype(J._I),
        unit_qty=P.UNIT_QTY_BUCKETS[u("qty")].astype(J._I),
        sell=gated(tables["sell"], P.SELL_BUCKETS, "qty_sell"),
        buy_seed=gated(tables["buy_seed"], P.BUY_BUCKETS, "qty_buy_seed"),
        buy_product=gated(tables["buy_product"], P.BUY_BUCKETS, "qty_buy_product"),
        buy_animal=tables["buy_animal"][idx].astype(J._I),
        hire=tables["hire"][idx].astype(J._I),
        buy_land=tables["buy_land"][idx].astype(bool),
    )
