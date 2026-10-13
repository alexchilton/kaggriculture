"""The trained net as a shippable agent: numpy only, no jax, no flax.

    from kagg.agents import numpy_neural as NN
    agent = NN.make_agent("data/bc_runs/.../latest.pkl")
    action = agent(obs)

WHAT THIS IS
------------
`kagg/agents/neural.py` in the three numpy ports:

    neural.py                        numpy_neural.py
    adapter.state_from_obs           numpy_obs.state_from_obs
    jax_obs.encode                   numpy_obs.encode
    model.apply (flax)               numpy_policy.apply
    jax_act.masks_for / condition    numpy_act.masks_for / condition_all
    decode_action                    decode_action            (copied; it was already numpy)

Each port is pinned to its original by a test that runs both on a real board with the shipped agent
driving:

    tests/test_the_numpy_net_matches_the_flax_net.py
    tests/test_the_numpy_encoder_matches_the_jax_encoder.py
    tests/test_the_numpy_masks_match_the_jax_masks.py

and `tests/test_the_numpy_agent_plays_the_same_game.py` pins THIS file to `neural.py` at the level
that actually matters -- the emitted action dict, turn by turn. The three component tests can all
pass while the composition is wrong; this project has the receipt for that, 136 component parity
tests green while the simulator silently burned seeds.

WHY IT EXISTS AT ALL
--------------------
The competition runtime has never had jax or flax, so `neural.py` cannot be bundled. Without this
file the net can be trained and measured and never shipped, which is where it has sat.

WEIGHTS
-------
`EMBEDDED_WEIGHTS` is empty in the repo, where params are read from a checkpoint on disk. A
submission carries no `data/` tree, so `scripts/build_net_submission.py` fills it with the packed
arrays, base64 of zlib of a float32 npz -- 3.4 MB for the 958k-parameter net. Same construction as
`schedule_agent.EMBEDDED_OPENINGS`, and for the same reason: a bundle that reads from a path finds
nothing and fails silently, which is worse than failing loudly.
"""

import base64
import io
import pickle
import zlib
from pathlib import Path

import numpy as np

from kagg.il import market_bundles as MB
from kagg.rl import numpy_act as NA, numpy_obs as NO, numpy_policy as NP

#: Filled by the bundler; empty in the repo. See the module docstring.
EMBEDDED_WEIGHTS = ""

#: Product / crop / animal name lists in index order, for `market_bundles.orders_from_heads`.
#: Taken from the same tables the encoder uses, not written out, so a balance change cannot leave
#: this decoding one product into another's slot.
PRODUCTS = list(NO.PRODUCTS)
CROPS_ORDERED = [k for k, _ in sorted(NO.CROP_INDEX.items(), key=lambda kv: kv[1])]
ANIMALS_ORDERED = [k for k, _ in sorted(NO.ANIMAL_INDEX.items(), key=lambda kv: kv[1])]
ITEM_NAME = {v: k for k, v in NO.ITEM_INDEX.items()}
CROP_NAME = {v: k for k, v in NO.CROP_INDEX.items()}


def _op_names():
    """op code -> the environment's op name, from `replays.OP_CODE` inverted.

    Imported locally: `kagg.il.replays` imports `jax_policy` and `jax_sim` at module scope, so it
    cannot be on a submission's import path. The bundler inlines the resulting dict instead.
    """
    from kagg.il.replays import OP_CODE
    return {v: k for k, v in OP_CODE.items()}


#: Filled by the bundler when `replays` is unavailable; derived here otherwise.
CODE_OP = {}


def _code_op():
    global CODE_OP
    if not CODE_OP:
        CODE_OP = _op_names()
    return CODE_OP


def _uncap_sells(market, shed):
    """A SELL pinned at the top quantity class means "at least this much" -- read the real number.

    `MAX_QTY` is 64 and the head's class index IS the quantity, so 63 is the largest number it can
    name. Over カワシギ's four tapes, 2,576 market orders: the largest legitimate SELL is 41, there
    are ZERO orders between 42 and 69, and the only four above the cap are the same action, the
    day-29 wheat dump. So 63 is never a real label; it is saturation. Worth $1,930 on one tape.

    Only the top class is rewritten, and only when the barn holds more: asking for more than exists
    is a silent no-op, not a bigger sale.
    """
    if not shed:
        return market
    cap = NA.MAX_QTY - 1
    out = []
    for o in market:
        if o and len(o) > 2 and o[0] == "SELL" and int(o[2]) == cap:
            have = int(shed.get(o[1], 0) or 0)
            if have > cap:
                out.append([o[0], o[1], have])
                continue
        out.append(o)
    return out


def decode_action(heads, n_units, vocab, seat=0, shed=None):
    """Head indices -> the environment's action dict. Copied from `neural.decode_action`.

    Only the first `n_units` slots are emitted: the environment counts SUBMITTED actions in its
    atomic-PLANT rule, so a surplus action for a unit that does not exist can block a plant no real
    agent could block. That cost this project a day chasing a phantom simulator bug.
    """
    code_op = _code_op()
    op = np.asarray(heads["op"])[seat]
    crop = np.asarray(heads["crop"])[seat]
    item = np.asarray(heads["item"])[seat]
    qty = np.asarray(heads["qty"])[seat]

    units = []
    for i in range(n_units):
        name = code_op.get(int(op[i]), "PASS")
        if name == "PLANT":
            units.append(["PLANT", CROP_NAME.get(int(crop[i]), "MELON")])
        elif name in ("PICKUP", "DROP", "PLACE"):
            n = int(NA.UNIT_QTY_BUCKETS[int(qty[i])])
            units.append([name, ITEM_NAME.get(int(item[i]), "WHEAT"), n])
        else:
            units.append([name])

    # One bundle, not six marginals: the bundle names WHICH orders go out together, including how
    # many HIRE slots -- the teacher's second most common market decision is ten hires in one turn.
    market = MB.orders_from_heads(
        vocab, int(np.asarray(heads["bundle"])[seat]),
        np.asarray(heads["qty_sell"])[seat],
        np.asarray(heads["qty_buy_product"])[seat],
        np.asarray(heads["qty_buy_seed"])[seat],
        PRODUCTS, CROPS_ORDERED, ANIMALS_ORDERED)

    market = _uncap_sells(market, shed)
    # Ten orders a turn; the environment drops the rest silently, so cut here rather than by chance.
    return {"farmer": units[0], "hands": units[1:], "market": market[:10]}


# ---- weights -------------------------------------------------------------------------------------
def pack_weights(params):
    """A params pytree -> the base64 blob `EMBEDDED_WEIGHTS` holds.

    zlib of an uncompressed npz of float32 leaves, keyed by their '/'-joined tree path. float32 not
    float64: the net was trained in float32 and the extra eight bytes a leaf would double the
    artifact for no change in any argmax.
    """
    flat = {}

    def walk(node, prefix=""):
        if hasattr(node, "items"):
            for k, v in node.items():
                walk(v, prefix + k + "/")
        else:
            flat[prefix[:-1]] = np.asarray(node, dtype=np.float32)

    walk(params)
    buf = io.BytesIO()
    np.savez(buf, **flat)
    return base64.b64encode(zlib.compress(buf.getvalue(), 9)).decode("ascii")


def unpack_weights(blob):
    """The inverse of `pack_weights`, back to nested dicts of numpy arrays."""
    with np.load(io.BytesIO(zlib.decompress(base64.b64decode(blob)))) as z:
        flat = {k: np.asarray(z[k], dtype=np.float32) for k in z.files}
    out = {}
    for path, arr in flat.items():
        node = out
        parts = path.split("/")
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = arr
    return out


def _params_and_vocab(checkpoint=None):
    """`(packed_params, vocab, n_layers)` from the embedded blob, or from a checkpoint on disk.

    **The checkpoint's OWN vocabulary wins.** The vocabulary is a sorted list, so adding or removing
    one bundle shifts every index above it -- the agent would decode class 47 as a different order
    than it was trained to mean, emit it with the right shape, and be wrong all season with nothing
    to read anywhere. Measured on the kawa clone: index 1 was `SELL FERTILIZER` to the head and
    `HIRE x10` to the mask, and the agent fired 11 orders in 719 turns.
    """
    if EMBEDDED_WEIGHTS:
        raw = unpack_weights(EMBEDDED_WEIGHTS)
        return raw["params"] if "params" in raw else raw, _embedded_vocab(), EMBEDDED_LAYERS

    ck = pickle.load(open(Path(checkpoint), "rb"))
    stored = ck.get("vocab")
    if not stored:
        raise ValueError(
            "%s carries no embedded vocabulary. Playing it against whatever `bundle_vocab.json` "
            "holds today would silently re-index every market decision." % checkpoint)
    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in stored], max_size=NA.N_BUNDLES)
    n_layers = int((ck.get("args") or {}).get("layers", 3))
    return NP.pack(migrate_on_disk(ck, n_layers)), vocab, n_layers


def migrate_on_disk(ck, n_layers):
    """A checkpoint's params brought up to the CURRENT architecture, using jax's own migration.

    **There is deliberately no numpy re-implementation of `migrate_params`.** It has four branches
    -- input projections growing on the leading axis, the op head growing on the trailing one, the
    op-axis tiling, and exact matches -- and each is a place a second copy would silently disagree.
    Getting one wrong does not raise: it loads a checkpoint whose columns mean something else.

    This path exists only in the repo, where jax is present. A submission carries weights the
    bundler has ALREADY migrated, so `EMBEDDED_WEIGHTS` never comes through here and the shipped
    artifact contains no migration code at all.

    The trap this fixes was caught by `tests/test_the_numpy_agent_plays_the_same_game.py` on its
    first run: the checkpoint's `glob` projection is `[122, 128]` and the encoder now emits 183
    columns, so the matmul failed outright. It failing loudly is luck -- a checkpoint that had grown
    on a *trailing* axis instead would have loaded and played a different game.
    """
    import jax
    import jax.numpy as jnp

    from kagg.rl import jax_act as A, jax_obs, jax_policy as P
    from kagg.sim import jax_sim as _J

    model = P.Policy(d_model=int((ck.get("args") or {}).get("d_model", 128)),
                     n_heads=int((ck.get("args") or {}).get("heads", 4)),
                     n_layers=n_layers)
    _t, _u, _g = jax_obs.encode(_J.reset(1))
    template = model.init(jax.random.PRNGKey(0), A._flat(_t), A._flat(_u), A._flat(_g))
    del jnp
    return P.load_or_migrate(ck["params"], template)


#: Filled by the bundler alongside `EMBEDDED_WEIGHTS`.
EMBEDDED_VOCAB = []
EMBEDDED_LAYERS = 3


def _embedded_vocab():
    return MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in EMBEDDED_VOCAB], max_size=NA.N_BUNDLES)


# ---- the agent -----------------------------------------------------------------------------------
def make_agent(checkpoint=None):
    """The trained net as an agent callable, pure numpy.

    Mirrors `neural.make_agent` turn for turn. The `GameMemo` is held across the episode and reset
    when the step counter does not advance: the arena reuses one process across games, and a clock
    carried over dates this game's shops from the previous season -- which is exactly the feature
    the q4 latch reads.
    """
    params, vocab, n_layers = _params_and_vocab(checkpoint)
    bundle_ok = MB.valid_table(vocab, pad_to=NA.N_BUNDLES)
    memo = [NO.GameMemo(), -1]

    def agent(obs, config=None):
        me = obs["player"]
        step = int(obs.get("step", 0) or 0)
        if step <= memo[1]:
            memo[0] = NO.GameMemo()
        memo[1] = step
        memo[0].observe(obs, step)

        privates = [obs["private"] if p == me else NO.agent_private_stub() for p in range(2)]
        state = NO.state_from_obs(obs, privates, step=step, memo=memo[0])
        tiles, units, glob = NO.encode(state)
        heads, _value = NP.apply(params, NA._flat(tiles), NA._flat(units), NA._flat(glob),
                                 n_layers=n_layers)
        masks = NA.masks_for(state, bundle_ok)

        # **Conditioning first, or this cannot run at all.** `crop`/`item`/`qty` carry an op axis the
        # masks do not, so masking a raw head is a broadcast error -- [N, U, K] against [N, U, O, K].
        choice = {k: np.argmax(np.where(masks[k], heads[k], -np.inf), axis=-1)
                  for k in NA.CONDITION_HEADS}
        conditioned = NA.condition_all(heads, choice)

        picked = {}
        for k in NA.ALL_HEADS:
            picked[k] = np.argmax(np.where(masks[k], conditioned[k], -np.inf), axis=-1)

        # `_flat` folded [batch, seat] into one axis, so our seat is row `me`.
        n_units = 1 + len(obs["farms"][me].get("hands", []))
        return decode_action(picked, n_units, vocab, seat=me,
                             shed=(obs.get("private") or {}).get("shed"))

    return agent
