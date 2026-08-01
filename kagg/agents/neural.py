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


def make_agent(checkpoint=DEFAULT_CKPT, greedy=True):
    """Build a dict-observation agent from a saved checkpoint."""
    import jax
    import jax.numpy as jnp

    with Path(checkpoint).open("rb") as fh:
        params = pickle.load(fh)["params"]
    model = P.Policy()
    key = [jax.random.PRNGKey(0)]

    def agent(obs, config=None):
        me = obs["player"]
        privates = [obs["private"] if p == me else adapter.agent_private_stub() for p in range(2)]
        state = adapter.state_from_obs(obs, privates)
        tiles, units, glob = jax_obs.encode(state)
        heads, _value = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        masks = A.masks_for(state)

        if greedy:
            picked = {k: jnp.argmax(jnp.where(masks[k], v, -jnp.inf), axis=-1)
                      for k, v in heads.items()}
        else:
            key[0], sub = jax.random.split(key[0])
            picked, _lp, _e = A.sample(sub, heads, masks)

        # `_flat` folded [batch, seat] into one axis, so our seat is row `me`.
        n_units = 1 + len(obs["farms"][me].get("hands", []))
        return decode_action({k: np.asarray(v) for k, v in picked.items()}, n_units, seat=me)

    return agent


agent = None       # built lazily; a missing checkpoint should not break `import kagg.agents`
