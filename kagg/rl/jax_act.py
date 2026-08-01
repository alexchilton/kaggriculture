"""Turn sampled policy heads into a `jax_sim.Actions`, and score them for the PPO update.

Kept apart from the network so that "what the policy predicts" and "what the simulator is told"
have exactly one bridge between them. When those two drift apart the symptom is a policy that
trains happily and plays nothing like its rollouts, which is very hard to see from a loss curve.

The joint log-prob is the sum over heads, and the sum runs over **every head, every turn**, even
heads the chosen op ignores -- a crop head is sampled whether or not the op is PLANT. That is not
waste, it is what keeps the density correct: the behaviour policy sampled those heads, so the
update has to score them. Dropping the unused ones would make the ratio in the PPO objective the
ratio of two different distributions.
"""

import jax
import jax.numpy as jnp

from kagg.rl import jax_masks, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

UNIT_HEADS = ("op", "crop", "item", "qty")
MARKET_HEADS = ("sell", "buy_product", "buy_seed", "buy_animal", "hire", "buy_land")
ALL_HEADS = UNIT_HEADS + MARKET_HEADS


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
    out = {"op": op, "crop": crop, "item": item, "qty": qty, **market}
    return {k: _flat(v) for k, v in out.items()}


def forward(params, model, state):
    """Run the network on a sim state. Returns `(heads, value, masks)`, all network-flat."""
    tiles, units, glob = jax_obs.encode(state)
    heads, value = model.apply(params, _flat(tiles), _flat(units), _flat(glob))
    return heads, value, masks_for(state)


def sample(key, heads, masks):
    """Sample every head. Returns `(actions, log_prob, entropy)` with log_prob summed per seat."""
    keys = jax.random.split(key, len(ALL_HEADS))
    actions, logps, entropies = {}, [], []
    for k, sub in zip(ALL_HEADS, keys):
        a, lp, ent = P.sample_head(sub, heads[k], masks[k])
        actions[k] = a
        # Per-unit and per-product heads carry an extra axis; sum it so every head contributes one
        # scalar per seat, and the joint density is the sum over all of them.
        logps.append(lp.reshape(lp.shape[0], -1).sum(axis=-1))
        entropies.append(ent.reshape(ent.shape[0], -1).sum(axis=-1))
    return actions, sum(logps), sum(entropies)


def evaluate(heads, masks, actions):
    """Score stored actions under current params, for the ratio in the PPO objective."""
    logps, entropies = [], []
    for k in ALL_HEADS:
        lp, ent = P.eval_head(heads[k], masks[k], actions[k])
        logps.append(lp.reshape(lp.shape[0], -1).sum(axis=-1))
        entropies.append(ent.reshape(ent.shape[0], -1).sum(axis=-1))
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
