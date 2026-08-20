"""Label shards -> the arrays `kagg/il/bc.loss` consumes. One npz per input shard.

`bc.build_rows` reads Kaggle *replay files* through `kagg/il/replays.py`. Our teacher is the shipped
planner and its data comes from `label_games.py` as JSONL, so this is the equivalent path for that
format. Both end at the same arrays, and deliberately at the same encoder --
`adapter.state_from_obs` then `jax_obs.encode` -- because `adapter.py` warns at length that a second
encoder "is a thing that must agree forever and will not".

**Why per-shard npz rather than one file.** 920,320 rows x (100*27 + 13*28 + 60) floats is ~11.5 GB
at float32 against 13 GB of RAM on the box. Sixteen shards of ~57.5k rows each are ~720 MB, which
streams.

**The opponent's private state is stubbed, not stored.** A submission never sees it, so training on
the real thing would fit features that vanish at deployment. `adapter.agent_private_stub()` is what
play substitutes and it is what we train against.

    python -u scripts/build_bc_rows.py --shards /home/alex/labels_r0b \
        --vocab data/il/bundle_vocab.json --out /home/alex/rows_r0b
"""

import argparse
import glob
import json
import pathlib
import sys
import time

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.il import market_bundles as MB                      # noqa: E402
from kagg.il.replays import OP_CODE                           # noqa: E402
from kagg.rl import adapter, jax_obs, jax_policy as P         # noqa: E402
from kagg.sim import jax_sim as J                             # noqa: E402
from kagg.sim.market import ANIMALS, ITEM_INDEX, PRODUCTS     # noqa: E402
from kagg.sim.tiles import CROP_INDEX                         # noqa: E402

CROPS = [c for c, _ in sorted(CROP_INDEX.items(), key=lambda kv: kv[1])]
SELL_LADDER = np.asarray(P.SELL_BUCKETS)
BUY_LADDER = np.asarray(P.BUY_BUCKETS)
UNIT_LADDER = np.asarray(P.UNIT_QTY_BUCKETS)


def nearest(value, ladder):
    """Project a raw quantity onto the student's ladder.

    Nearest, not floor: with SELL_BUCKETS [0,1,3,10,30] a teacher selling 7 is much better described
    by 10 than by 3. Same rule as `bc_dagger._bucket_index`, which is the inverse of the decode.
    """
    return int(np.argmin(np.abs(ladder - value)))


def unit_labels(action_list, n_slots):
    """Kaggle unit actions -> (op, crop, item, qty) index arrays plus the live mask."""
    op = np.zeros(n_slots, dtype=np.int16)
    crop = np.zeros(n_slots, dtype=np.int16)
    item = np.zeros(n_slots, dtype=np.int16)
    qty = np.zeros(n_slots, dtype=np.int16)
    live = np.zeros(n_slots, dtype=bool)
    for u, a in enumerate(action_list[:n_slots]):
        if not a:
            continue
        live[u] = True
        name = str(a[0])
        op[u] = OP_CODE.get(name, OP_CODE.get("PASS", 0))
        if name == "PLANT" and len(a) > 1:
            crop[u] = CROP_INDEX.get(str(a[1]), 0)
        elif name in ("PICKUP", "DROP", "PLACE"):
            if len(a) > 1:
                item[u] = ITEM_INDEX.get(str(a[1]), 0)
            if len(a) > 2:
                qty[u] = nearest(float(a[2]), UNIT_LADDER)
    return op, crop, item, qty, live


def market_labels(orders, vocab):
    """Kaggle market list -> bundle index, per-product quantity buckets, and their weights.

    **The weights are the point.** `qty_sell` has one entry per product against a bundle naming one
    or two, and 78.9% of turns name nothing at all. Scoring every entry trains the rest toward
    bucket 0 on turns the teacher had no opinion about -- the padding mistake `bc.py` already warns
    about three times for the unit heads. A quantity is only a decision where the bundle asked for
    one.
    """
    bundle = MB.bundle_of(orders)
    idx = vocab.index(bundle)

    y_sell = np.zeros(len(PRODUCTS), dtype=np.int16)
    y_bp = np.zeros(len(PRODUCTS), dtype=np.int16)
    y_bs = np.zeros(len(CROPS), dtype=np.int16)
    w_sell = np.zeros(len(PRODUCTS), dtype=np.float32)
    w_bp = np.zeros(len(PRODUCTS), dtype=np.float32)
    w_bs = np.zeros(len(CROPS), dtype=np.float32)

    for o in (orders or ()):
        if not isinstance(o, (list, tuple)) or not o:
            continue
        op = str(o[0])
        name = str(o[1]) if len(o) > 1 else ""
        n = float(o[2]) if len(o) > 2 else 1.0
        if op == "SELL" and name in PRODUCTS:
            i = PRODUCTS.index(name)
            y_sell[i], w_sell[i] = nearest(n, SELL_LADDER), 1.0
        elif op == "BUY_PRODUCT" and name in PRODUCTS:
            i = PRODUCTS.index(name)
            y_bp[i], w_bp[i] = nearest(n, BUY_LADDER), 1.0
        elif op == "BUY_SEED" and name in CROPS:
            i = CROPS.index(name)
            y_bs[i], w_bs[i] = nearest(n, BUY_LADDER), 1.0
    return idx, y_sell, y_bp, y_bs, w_sell, w_bp, w_bs


def build(path, vocab, out_dir):
    rows = []
    with open(path) as fh:
        for line in fh:
            rows.append(json.loads(line))
    n = len(rows)
    if not n:
        return 0

    # `J.BOARD` is 10, so 100 tile tokens. Derived rather than written as a literal: the policy's
    # positional embedding is sized from the input, so a mismatch here would train against a board
    # shape the network never sees and fail only at load time.
    tiles = np.zeros((n, J.BOARD * J.BOARD, jax_obs.TILE_FEATURES), dtype=np.float16)
    units = np.zeros((n, J.MAX_UNITS, jax_obs.UNIT_FEATURES), dtype=np.float16)
    glob = np.zeros((n, jax_obs.GLOBAL_FEATURES), dtype=np.float16)

    y_op = np.zeros((n, J.MAX_UNITS), dtype=np.int16)
    y_crop = np.zeros((n, J.MAX_UNITS), dtype=np.int16)
    y_item = np.zeros((n, J.MAX_UNITS), dtype=np.int16)
    y_qty = np.zeros((n, J.MAX_UNITS), dtype=np.int16)
    live = np.zeros((n, J.MAX_UNITS), dtype=bool)

    y_bundle = np.zeros(n, dtype=np.int16)
    y_qs = np.zeros((n, len(PRODUCTS)), dtype=np.int16)
    y_qbp = np.zeros((n, len(PRODUCTS)), dtype=np.int16)
    y_qbs = np.zeros((n, len(CROPS)), dtype=np.int16)
    w_qs = np.zeros((n, len(PRODUCTS)), dtype=np.float32)
    w_qbp = np.zeros((n, len(PRODUCTS)), dtype=np.float32)
    w_qbs = np.zeros((n, len(CROPS)), dtype=np.float32)

    t0 = time.time()
    for r, row in enumerate(rows):
        ob, seat, act = row["obs"], int(row["seat"]), row["act"] or {}
        privates = [None, None]
        privates[seat] = ob.get("private")
        privates[1 - seat] = adapter.agent_private_stub()
        state = adapter.state_from_obs(ob, privates)
        t, u, g = jax_obs.encode(state)
        # `encode` returns [B, P, ...]; this row is that seat of a batch of one.
        tiles[r] = np.asarray(t)[0, seat]
        units[r] = np.asarray(u)[0, seat]
        glob[r] = np.asarray(g)[0, seat]

        acts = [act.get("farmer")] + list(act.get("hands") or [])
        (y_op[r], y_crop[r], y_item[r], y_qty[r], live[r]) = unit_labels(acts, J.MAX_UNITS)
        (y_bundle[r], y_qs[r], y_qbp[r], y_qbs[r],
         w_qs[r], w_qbp[r], w_qbs[r]) = market_labels(act.get("market") or [], vocab)

        if r and r % 20000 == 0:
            print("    %s %6d/%d  %.0f rows/s"
                  % (pathlib.Path(path).name, r, n, r / max(1e-6, time.time() - t0)), flush=True)

    out = pathlib.Path(out_dir) / (pathlib.Path(path).stem + ".npz")
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out, tiles=tiles, units=units, glob=glob,
        y_op=y_op, y_crop=y_crop, y_item=y_item, y_qty=y_qty, live=live,
        y_bundle=y_bundle, y_qty_sell=y_qs, y_qty_buy_product=y_qbp, y_qty_buy_seed=y_qbs,
        w_qty_sell=w_qs, w_qty_buy_product=w_qbp, w_qty_buy_seed=w_qbs)
    print("  wrote %s  rows=%d  in %.0fs" % (out, n, time.time() - t0), flush=True)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", required=True)
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", type=int, default=None, help="build a single shard index, for workers")
    args = ap.parse_args()

    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in b) for b in json.loads(pathlib.Path(args.vocab).read_text())],
        max_size=P.N_BUNDLES)
    print("vocabulary %d of %d slots" % (vocab.size, P.N_BUNDLES), flush=True)

    paths = sorted(glob.glob(args.shards.rstrip("/") + "/*.jsonl"))
    if args.only is not None:
        paths = [paths[args.only]]
    total = 0
    for p in paths:
        total += build(p, vocab, args.out)
    print("done: %s rows" % format(total, ","))


if __name__ == "__main__":
    main()
