"""Play a trained checkpoint in the real environment, as an ordinary dict-observation agent.

This is the piece that turns "the loss went down" into a number that means something. Offline
accuracy measures *imitation*: a model can reproduce 77% of a teacher's actions and still play
badly, because the 23% it misses may be exactly the decisions that mattered -- buying the seed,
selling before the shed overflows. Only a game says which.

Three steps, and the middle one is deliberately not new code:

1. `adapter.state_from_obs` rebuilds a `jax_sim.State` from the dict observation;
2. the *same* `jax_obs.encode` the policy trained on turns that into features;
3. `decode_action` turns the sampled heads back into the `{"farmer", "hands", "market"}` dict the
   environment expects -- the inverse of `kagg.il.replays.encode_action`.

**The opponent's private state is not visible here**, and must not be visible in training either:
the environment gives an agent `agent_private_stub()` for the other seat, so a policy trained on the
full pair would be reading information it will not have at play time. `replays.iter_turns` hides it
for the same reason.
"""

import pickle
from pathlib import Path

import numpy as np

from kagg.il.replays import ANIMAL_INDEX, OP_CODE, PRODUCTS
from kagg.rl import adapter, jax_act as A, jax_obs, jax_policy as P
from kagg.sim.tiles import CROP_INDEX

CODE_OP = {v: k for k, v in OP_CODE.items()}
CROP_NAME = {v: k for k, v in CROP_INDEX.items()}
ITEM_NAME = {}
ANIMAL_NAME = {v: k for k, v in ANIMAL_INDEX.items()}

DEFAULT_CKPT = Path("data/bc/bc.pkl")


def _item_names():
    from kagg.sim.market import ITEM_INDEX
    return {v: k for k, v in ITEM_INDEX.items()}


ITEM_NAME = _item_names()


def _fire(probs, threshold):
    """Which slots act, and with which non-zero bucket.

    **Neither argmax nor sampling works on these heads, and the reason is measured.** Bucket 0 is
    "do nothing", and a teacher acts on only 4.7% of (turn, product) cells for `sell` and 3.6% for
    `buy_product`. The model learns that dependence well -- mean P(act) is 0.183 against 0.051 for
    `sell`, and 0.367 against 0.031 for `buy_product`, a 12:1 discrimination -- but it is
    *under-confident*, and P(act) rarely clears a half.

    So `argmax` picks bucket 0 on every product on every turn and the agent banks exactly its
    $3,000 start, while independent sampling fires thousands of low-probability false positives
    across nine products and 720 turns and ends on $1. Both discard a signal the network has.

    A threshold keeps it: act where the model is confident, and take its preferred quantity there.
    """
    p_act = 1.0 - probs[..., 0]
    bucket = probs[..., 1:].argmax(axis=-1) + 1
    return np.where(p_act > threshold, bucket, 0)


def decode_action(heads, n_units, seat=0):
    """Sampled head indices -> the environment's action dict.

    Only the first `n_units` slots are emitted: the environment counts *submitted* actions in its
    atomic-PLANT rule, so a surplus action for a unit that does not exist can block a plant that no
    real agent could block. That cost this project a day of chasing a phantom simulator bug.
    """
    op = np.asarray(heads["op"])[seat]
    crop = np.asarray(heads["crop"])[seat]
    item = np.asarray(heads["item"])[seat]
    qty = np.asarray(heads["qty"])[seat]

    units = []
    for i in range(n_units):
        name = CODE_OP.get(int(op[i]), "PASS")
        if name == "PLANT":
            units.append(["PLANT", CROP_NAME.get(int(crop[i]), "MELON")])
        elif name in ("PICKUP", "DROP", "PLACE"):
            n = int(np.asarray(P.UNIT_QTY_BUCKETS)[int(qty[i])])
            units.append([name, ITEM_NAME.get(int(item[i]), "WHEAT"), n])
        else:
            units.append([name])

    market = []
    sell = np.asarray(heads["sell"])[seat]
    buy_p = np.asarray(heads["buy_product"])[seat]
    buy_s = np.asarray(heads["buy_seed"])[seat]
    buy_a = np.asarray(heads["buy_animal"])[seat]

    for p, name in enumerate(PRODUCTS):
        n = int(np.asarray(P.SELL_BUCKETS)[int(sell[p])])
        if n:
            market.append(["SELL", name, n])
    for p, name in enumerate(PRODUCTS):
        n = int(np.asarray(P.BUY_BUCKETS)[int(buy_p[p])])
        if n:
            market.append(["BUY_PRODUCT", name, n])
    for c, name in CROP_NAME.items():
        n = int(np.asarray(P.BUY_BUCKETS)[int(buy_s[c])])
        if n:
            market.append(["BUY_SEED", name, n])
    for a, name in ANIMAL_NAME.items():
        if int(buy_a[a]):
            market.append(["BUY_ANIMAL", name, 1])
    if int(np.asarray(heads["hire"])[seat]):
        market.append(["HIRE"])
    if int(np.asarray(heads["buy_land"])[seat]):
        market.append(["BUY_LAND"])

    # The environment accepts ten orders a turn and silently drops the rest, so the cut is made
    # here rather than left to chance about which ones survive.
    return {"farmer": units[0], "hands": units[1:], "market": market[:10]}


# Every head whose class 0 means "do nothing". `hire` and `buy_land` are binary and belong here for
# exactly the same reason as the quantity heads: hiring happens on 7.4% of turns, so the mode is
# "do not hire" on essentially every turn and argmax would build a farm with no crew.
MARKET_HEADS = ("sell", "buy_product", "buy_seed", "buy_animal", "hire", "buy_land")


def calibrate(params, model, shard=None, sample=4096):
    """Per-head firing thresholds, set so the agent acts as often as the teacher did.

    **One global threshold cannot work, because the heads are on entirely different scales.** The
    teacher acts on 4.7% of `sell` cells and 1.2% of `buy_seed` cells, and the model's confidence
    tracks that: P(act) reaches 0.95 for `sell` and never exceeds 0.27 for `buy_seed`, typically
    sitting at 0.046. A threshold that lets `sell` through silences `buy_seed` completely, which is
    fatal -- no seed means no crop, no harvest, no revenue, and a bank that ends exactly where it
    started.

    So each head gets the quantile of its own predicted-probability distribution that reproduces the
    teacher's observed rate. It is calibration against the training data, not a tuned dial.
    """
    import glob

    import jax

    shards = sorted(glob.glob("data/il/shard_*.npz"))
    if not shards:
        return {}
    z = np.load(shard or shards[-1])
    t, u, g = z["tiles"][-sample:], z["units"][-sample:], z["glob"][-sample:]
    heads, _ = model.apply(params, np.asarray(t, np.float32), np.asarray(u, np.float32),
                           np.asarray(g, np.float32))

    out = {}
    for k in MARKET_HEADS:
        y = np.asarray(z[f"y_{k}"][-sample:])
        rate = float((y > 0).mean())
        p_act = 1.0 - np.asarray(jax.nn.softmax(heads[k], axis=-1))[..., 0]
        # The threshold that fires on exactly the teacher's share of cells.
        out[k] = float(np.quantile(p_act, 1.0 - rate)) if 0.0 < rate < 1.0 else 1.1
    return out


def make_agent(checkpoint=DEFAULT_CKPT, threshold=None):
    """Build a dict-observation agent from a saved checkpoint.

    Unit ops are decoded greedily: their classes are genuinely mutually exclusive -- a unit does
    exactly one thing -- and the mode is the right answer there. The market heads are decoded by
    `_fire`, because bucket 0 is "do nothing" against a heavily imbalanced base rate and the mode
    is *always* "do nothing" even when the model is confident it should act. See `_fire`.
    """
    import jax
    import jax.numpy as jnp

    with Path(checkpoint).open("rb") as fh:
        raw = pickle.load(fh)["params"]
    model = P.Policy()
    # Pre-op-axis checkpoints are tiled onto the current argument heads. See
    # `jax_policy.migrate_params` -- the tiling is behaviour-preserving, so this does not change
    # what an older submission checkpoint plays.
    from kagg.sim import jax_sim as _J
    _t, _u, _g = jax_obs.encode(_J.reset(1))
    params = P.load_or_migrate(raw, model.init(
        jax.random.PRNGKey(0), A._flat(_t), A._flat(_u), A._flat(_g)))
    thresholds = calibrate(params, model)
    if threshold is not None:
        thresholds = {k: threshold for k in MARKET_HEADS}

    def agent(obs, config=None):
        me = obs["player"]
        privates = [obs["private"] if p == me else adapter.agent_private_stub() for p in range(2)]
        state = adapter.state_from_obs(obs, privates)
        tiles, units, glob = jax_obs.encode(state)
        heads, _value = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(state)

        # **Conditioning comes first, and without it this function cannot run at all.**
        #
        # `sell`/`buy_product` carry a trade-mode axis and `crop`/`item`/`qty` an op axis that the
        # masks do not, so `jnp.where(masks[k], heads[k], -inf)` on a raw head is a broadcast error
        # -- `[N, 9, K]` against `[N, 9, 3, K]`. This loop used to iterate `heads.items()` and had
        # been broken since the trade axis landed; it is the same bug still open in
        # `eval_policy.py:41`.
        #
        # The conditioning variables are decoded greedily. That is the right call for `op`, whose
        # classes are genuinely exclusive, and it is the standing compromise for `trade`, which the
        # per-product `_fire` thresholds then work within.
        choice = {k: jnp.argmax(jnp.where(masks[k], heads[k], -jnp.inf), axis=-1)
                  for k in A.CONDITION_HEADS}
        conditioned = A.condition_all(heads, choice)

        picked = {}
        for k in A.ALL_HEADS:
            logits = jnp.where(masks[k], conditioned[k], -jnp.inf)
            if k in MARKET_HEADS:
                picked[k] = _fire(np.asarray(jax.nn.softmax(logits, axis=-1)),
                                  thresholds.get(k, 0.5))
            else:
                picked[k] = np.asarray(jnp.argmax(logits, axis=-1))

        # `_flat` folded [batch, seat] into one axis, so our seat is row `me`.
        n_units = 1 + len(obs["farms"][me].get("hands", []))
        return decode_action(picked, n_units, seat=me)

    return agent


agent = None       # built lazily; a missing checkpoint should not break `import kagg.agents`
