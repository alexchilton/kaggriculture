"""When the teacher trades, does the net know which basket -- or does the decode throw it away?

    python -u scripts/is_the_market_head_empty_or_just_never_decoded.py \
        --ckpt data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl \
        --cache data/bc_rows_kawa_v2.npz

THE QUESTION
------------
The kawa clone scores `ACTED 0.727` and trades on 11-47 turns of 719, against the teacher's 51.0%.
Two explanations, and they lead opposite ways:

    the head is EMPTY        it never learned which basket to post. The kawa BC track is finished
                             and no decoder recovers anything.
    the DECODE discards it   the right basket is ranked high and `argmax` still picks EMPTY, because
                             "probably do nothing" beats 255 individually-unlikely baskets. Then the
                             information is already in the checkpoint and a threshold recovers it
                             with no retraining at all.

`CLAUDE.md` records this exact shape once already: greedy argmax over per-head marginals emitted
zero market orders while the marginals themselves discriminated 12:1. `neural._fire` was written for
that failure -- and it is applied to `sell` and `buy_product`, whose bucket 0 is "do nothing", while
`bundle` is decoded by a plain `argmax` whose index 0 is *also* "do nothing". Same failure, one head
still uncovered.

WHAT IS MEASURED
----------------
Only rows where the TEACHER TRADED (`y_bundle != 0`). On those:

    rank of the true bundle    0 means argmax already picks it. A low median with a low top-1 is
                               the decode verdict: the ordering is right, the winner is EMPTY.
    P(EMPTY) vs P(true)        how much probability mass the "do nothing" class is taking.
    recall @ k                 how often the truth is in the top k, which is what a threshold or a
                               sampled decode can reach.

And the counterfactual that matters: **top-1 among the NON-EMPTY classes.** If suppressing index 0
alone would have picked the right basket, the fix is one line in the decoder.
"""
import argparse
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

EMPTY_INDEX = 0            # index 0 is "place no orders" everywhere it is read


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--rows", type=int, default=20000, help="traded rows to score")
    ap.add_argument("--batch", type=int, default=256)
    args = ap.parse_args()

    import jax
    import jax.numpy as jnp

    from kagg.rl import jax_act as A, jax_policy as P

    ck = pickle.load(open(args.ckpt, "rb"))
    params = jax.tree_util.tree_map(jnp.asarray, ck["params"])
    widths = ck.get("widths")
    n_bundles = ck.get("vocab_size") or P.N_BUNDLES
    print(f"ckpt   {args.ckpt}")
    print(f"widths {widths}   vocabulary {n_bundles} bundles\n")

    d = np.load(args.cache)
    y = d["y_bundle"]
    traded = np.flatnonzero(y != EMPTY_INDEX)
    print(f"{len(y):,} rows, {len(traded):,} where the teacher traded "
          f"({len(traded) / len(y):.1%})")
    rng = np.random.default_rng(0)
    if len(traded) > args.rows:
        traded = rng.choice(traded, args.rows, replace=False)
        traded.sort()
    print(f"scoring {len(traded):,} of them\n", flush=True)

    model = P.Policy(d_model=ck["args"].get("d_model", 128) if isinstance(ck.get("args"), dict) else 128,
                     n_heads=ck["args"].get("heads", 4) if isinstance(ck.get("args"), dict) else 4,
                     n_layers=ck["args"].get("layers", 3) if isinstance(ck.get("args"), dict) else 3)

    @jax.jit
    def bundle_logits(t, u, g, m):
        heads, _v = model.apply(params, t, u, g)
        return P._masked_logits(heads["bundle"], m)

    ranks, p_empty, p_true, top1_nonempty = [], [], [], []
    for s in range(0, len(traded), args.batch):
        idx = traded[s:s + args.batch]
        t = jnp.asarray(d["tiles"][idx])[:, None]
        u = jnp.asarray(d["units"][idx])[:, None]
        g = jnp.asarray(d["glob"][idx])[:, None]
        # No player axis: `_flat` collapses it out of tiles/units/glob, so `heads["bundle"]` comes
        # back `[N, n_bundles]` and a `[N, 1, n_bundles]` mask cannot broadcast onto it.
        m = jnp.asarray(d["m_bundle"][idx])
        # Already `[N, n_bundles]` -- `_flat` collapsed the player axis, so there is no seat to pick.
        lg = np.asarray(bundle_logits(A._flat(t), A._flat(u), A._flat(g), m))
        pr = np.exp(lg - lg.max(-1, keepdims=True))
        pr /= pr.sum(-1, keepdims=True)
        truth = y[idx]
        # rank 0 == argmax already correct
        order = np.argsort(-lg, axis=-1)
        rank = np.argmax(order == truth[:, None], axis=-1)
        ranks.append(rank)
        p_empty.append(pr[:, EMPTY_INDEX])
        p_true.append(pr[np.arange(len(idx)), truth])
        blanked = lg.copy()
        blanked[:, EMPTY_INDEX] = -np.inf
        top1_nonempty.append(blanked.argmax(-1) == truth)
        if s % (args.batch * 20) == 0:
            print(f"  {s:,}/{len(traded):,}", flush=True)

    rank = np.concatenate(ranks)
    p_empty = np.concatenate(p_empty)
    p_true = np.concatenate(p_true)
    top1_ne = np.concatenate(top1_nonempty)

    print("\nOn turns where the teacher TRADED:")
    print(f"  top-1 (as decoded today)          {(rank == 0).mean():>7.1%}")
    print(f"  top-1 with EMPTY suppressed       {top1_ne.mean():>7.1%}   <- one line in the decoder")
    for k in (3, 5, 10, 25):
        print(f"  truth in top-{k:<3}                   {(rank < k).mean():>7.1%}")
    print(f"  median rank of the true bundle    {int(np.median(rank)):>7,} of {n_bundles}")
    print(f"  mean P(EMPTY)                     {p_empty.mean():>7.1%}")
    print(f"  mean P(true bundle)               {p_true.mean():>7.1%}")
    print(f"  argmax IS empty                   {(rank > 0).mean() * 0 + (p_empty > p_true).mean():>7.1%}"
          "   (P(EMPTY) beats P(true))")

    print("\nREAD IT LIKE THIS")
    print("  top-1 low, EMPTY-suppressed HIGH   the decode is the bug. No retraining needed --")
    print("                                     the clone's market head already knows the basket.")
    print("  both low, median rank high         the head never learned it. The kawa BC track is done.")


main()
