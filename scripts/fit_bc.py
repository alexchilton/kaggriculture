"""Round 0 of the imitation chain: fit the policy to the teacher's own states. This IS the BC stage.

`bc_dagger.py` frames the whole chain with one knob -- "beta is the probability that a turn is
actually executed by the teacher rather than the student. beta=1 is plain behaviour cloning on
teacher states." This script is that beta=1 round, run offline because our teacher is the shipped
Python planner and cannot live inside a `jax.scan` the way `jax_rancher` does.

**No offline number here is evidence that it works.** Two have already lied in this project: 86.2%
per-decision accuracy on teacher states scored 79.3% error on its own trajectory, and six
well-fitted market marginals composed into an agent that never traded and banked exactly its $3,000
start. So this prints the ARGMAX MIX every epoch, against the teacher's measured distribution, and
that is the number to read -- a falling loss with a degenerate argmax is the failure mode, not a
contradiction of it.

Reference numbers from 920,320 teacher turns:

    empty market bundle    78.9% of turns
    non-empty market       21.1%

If the student's argmax is ~100% empty, the head has collapsed to the majority class and no amount
of further training fixes it. That is the same disease as `P(move) = 6e-5` in the parked BC track.

    python -u scripts/fit_bc.py --rows /home/alex/rows_r0b --vocab data/il/bundle_vocab.json \
        --out data/bc/bc_bundle.pkl --epochs 3
"""

import argparse
import collections
import glob
import json
import pathlib
import pickle
import sys
import time

import jax
import jax.numpy as jnp
import numpy as np
import optax

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.il import bc, market_bundles as MB                  # noqa: E402
from kagg.rl import jax_act as A, jax_obs, jax_policy as P    # noqa: E402
from kagg.sim import jax_sim as J                             # noqa: E402

# What the teacher does, measured on 920,320 player-turns of ead81e2 self-play. The argmax mix is
# read against these, not against a previous epoch.
TEACHER_EMPTY_RATE = 0.789


def load_shard(path):
    d = np.load(path)
    return {k: d[k] for k in d.files}


def batches(shard, size, rng):
    n = len(shard["y_bundle"])
    order = rng.permutation(n)
    for i in range(0, n - size + 1, size):
        sl = order[i:i + size]
        yield {k: v[sl] for k, v in shard.items()}


def to_loss_batch(b):
    """npz arrays -> the dict `bc.loss_terms` reads, with masks all-legal.

    Masks are permissive here on purpose and it is worth saying why, because a permissive mask is
    normally the bug: the TEACHER's action is legal by construction -- it played it -- so masking
    the label out of its own support could only ever remove signal. The legality mask that matters
    is at PLAY time, in `jax_act.masks_for`, where it stops the student choosing something the shed
    cannot back.
    """
    out = {
        "live": b["live"],
        "y_op": b["y_op"].astype(np.int32),
        "y_crop": b["y_crop"].astype(np.int32),
        "y_item": b["y_item"].astype(np.int32),
        "y_qty": b["y_qty"].astype(np.int32),
        "y_bundle": b["y_bundle"].astype(np.int32),
        "y_qty_sell": b["y_qty_sell"].astype(np.int32),
        "y_qty_buy_product": b["y_qty_buy_product"].astype(np.int32),
        "y_qty_buy_seed": b["y_qty_buy_seed"].astype(np.int32),
        "w_qty_sell": b["w_qty_sell"],
        "w_qty_buy_product": b["w_qty_buy_product"],
        "w_qty_buy_seed": b["w_qty_buy_seed"],
    }
    n, u = len(b["y_bundle"]), b["y_op"].shape[1]
    out["m_op"] = np.ones((n, u, P.N_OPS), bool)
    out["m_crop"] = np.ones((n, u, J.N_CROPS), bool)
    out["m_item"] = np.ones((n, u, J.N_ITEMS), bool)
    out["m_qty"] = np.ones((n, u, len(P.UNIT_QTY_BUCKETS)), bool)
    out["m_bundle"] = np.ones((n, P.N_BUNDLES), bool)
    out["m_qty_sell"] = np.ones((n, J.N_PRODUCTS, len(P.SELL_BUCKETS)), bool)
    out["m_qty_buy_product"] = np.ones((n, J.N_PRODUCTS, len(P.BUY_BUCKETS)), bool)
    out["m_qty_buy_seed"] = np.ones((n, J.N_CROPS, len(P.BUY_BUCKETS)), bool)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, help="directory of npz shards from build_bc_rows.py")
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--smooth", type=float, default=0.02)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    vocab = MB.Vocabulary.from_bundles(
        [tuple(tuple(p) for p in x) for x in json.loads(pathlib.Path(args.vocab).read_text())],
        max_size=P.N_BUNDLES)
    print("vocabulary %d of %d slots" % (vocab.size, P.N_BUNDLES), flush=True)

    shards = sorted(glob.glob(args.rows.rstrip("/") + "/*.npz"))
    if not shards:
        raise SystemExit("no npz under %s" % args.rows)
    print("shards: %d" % len(shards), flush=True)

    probe = load_shard(shards[0])
    n_tiles = probe["tiles"].shape[1]
    model = P.Policy()
    key = jax.random.PRNGKey(args.seed)
    params = model.init(key,
                        jnp.zeros((1, n_tiles, jax_obs.TILE_FEATURES)),
                        jnp.zeros((1, probe["units"].shape[1], jax_obs.UNIT_FEATURES)),
                        jnp.zeros((1, jax_obs.GLOBAL_FEATURES)))
    n_params = sum(int(x.size) for x in jax.tree_util.tree_leaves(params))
    print("params: %s   tile/unit/glob %d/%d/%d"
          % (format(n_params, ","), jax_obs.TILE_FEATURES, jax_obs.UNIT_FEATURES,
             jax_obs.GLOBAL_FEATURES), flush=True)

    optimiser = optax.chain(optax.clip_by_global_norm(0.5), optax.adam(args.lr))
    opt_state = optimiser.init(params)

    @jax.jit
    def step(params, opt_state, tiles, units, gfeat, batch):
        def loss_fn(p):
            heads, _v = model.apply(p, tiles, units, gfeat)
            # `bc.loss` returns (total, per_head). The per-head dict is what tells us WHICH head is
            # not learning -- a falling total with a flat bundle term is the failure this whole
            # pipeline exists to catch -- so it is carried through as aux rather than discarded.
            return bc.loss(heads, batch, smooth=args.smooth)
        (loss, per_head), grads = jax.value_and_grad(loss_fn, has_aux=True)(params)
        updates, opt_state = optimiser.update(grads, opt_state, params)
        return optax.apply_updates(params, updates), opt_state, loss, per_head

    @jax.jit
    def argmax_mix(params, tiles, units, gfeat):
        heads, _v = model.apply(params, tiles, units, gfeat)
        return jnp.argmax(heads["bundle"], axis=-1), jnp.argmax(heads["op"], axis=-1)

    rng = np.random.default_rng(args.seed)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(args.epochs):
        t0, seen, tot = time.time(), 0, 0.0
        head_tot = collections.defaultdict(float)
        for sp in shards:
            shard = load_shard(sp)
            for b in batches(shard, args.batch, rng):
                tiles = jnp.asarray(b["tiles"], dtype=jnp.float32)
                units = jnp.asarray(b["units"], dtype=jnp.float32)
                gfeat = jnp.asarray(b["glob"], dtype=jnp.float32)
                lb = {k: jnp.asarray(v) for k, v in to_loss_batch(b).items()}
                params, opt_state, loss, per_head = step(
                    params, opt_state, tiles, units, gfeat, lb)
                tot += float(loss)
                for h, v in per_head.items():
                    head_tot[h] += float(v)
                seen += 1
            del shard

        # ---- THE INSTRUMENT. Read this, not the loss. ----
        probe_shard = load_shard(shards[0])
        sl = slice(0, min(4096, len(probe_shard["y_bundle"])))
        bmax, omax = argmax_mix(
            params,
            jnp.asarray(probe_shard["tiles"][sl], dtype=jnp.float32),
            jnp.asarray(probe_shard["units"][sl], dtype=jnp.float32),
            jnp.asarray(probe_shard["glob"][sl], dtype=jnp.float32))
        bmax = np.asarray(bmax)
        empty_rate = float((bmax == 0).mean())
        teacher_empty = float((probe_shard["y_bundle"][sl] == 0).mean())
        top = collections.Counter(bmax.tolist()).most_common(5)

        print("\nepoch %d  loss %.4f  %d batches  %.0fs"
              % (epoch, tot / max(1, seen), seen, time.time() - t0))
        print("  per head                 : %s"
              % "  ".join("%s %.4f" % (h, head_tot[h] / max(1, seen))
                          for h in sorted(head_tot)))
        print("  bundle argmax empty rate : %.3f   teacher %.3f   (reference %.3f)"
              % (empty_rate, teacher_empty, TEACHER_EMPTY_RATE))
        print("  bundle argmax top 5      : %s"
              % ", ".join("idx %d x%d" % (i, n) for i, n in top))
        if empty_rate > 0.98:
            print("  *** COLLAPSED to the majority class. A falling loss does not contradict this;")
            print("      it is the six-marginals failure in a new form. Stop and diagnose. ***")
        del probe_shard

        with out.open("wb") as fh:
            pickle.dump({"params": params, "vocab_size": vocab.size,
                         "tile_features": jax_obs.TILE_FEATURES,
                         "unit_features": jax_obs.UNIT_FEATURES,
                         "global_features": jax_obs.GLOBAL_FEATURES,
                         "n_bundles": P.N_BUNDLES}, fh)
        print("  checkpoint -> %s" % out, flush=True)


if __name__ == "__main__":
    main()
