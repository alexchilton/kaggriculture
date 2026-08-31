"""Held-out op accuracy for a replay clone, split into the WALK and the WORK.

    python -u scripts/split_the_clones_accuracy_by_op_class.py \
        --ckpt data/bc_runs/bcr_kawa-<stamp>/latest.pkl --rows data/bc_rows_kawa.npz

WHY THE SPLIT IS THE POINT
--------------------------
`bc_replay.py` prints one number, `ACTED`, over every op the teacher actually played. Movement is
in there, and movement is the hard part: measured 2026-08-28 on the same teachers with a hand-feature
model, excluding the walk took kawa from 78.7% to 97.4% and Crop Dusta from 65.7% to 93.0%
(`data/logs/bc_train_four_ways.log`). A single blended number cannot distinguish "cannot imitate
kawa's farming" from "cannot predict which way he walks", and only the first one would be fatal.

It matters because the shipped design already hands movement to the router
(`emit_dusta_bc_dataset.py`: *"a policy that emits movement can walk north when it should walk west,
and a wrong step puts the unit out of position for the whole routed day. Legality masking cannot
catch that because the wrong step is legal"*). So a clone that is strong on work ops and weak on the
walk is the USEFUL artifact, not a failed one.

**The holdout is the trailing block, and it is the poorest seats.** `bc_replay.py:158` takes
`idx_val = arange(n - n_val, n)` after `rank_seats` sorted richest-first, so validation is scored
against kawa's weakest games (~$51.7k end of a $51.7k-$161.9k range). This script scores the WHOLE
val block rather than `idx_val[:4096]`, which is what the trainer prints -- that slice is the first
4,096 rows of those seats, i.e. their opening turns only.
"""
import argparse
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

MOVE = ("NORTH", "SOUTH", "EAST", "WEST")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--rows", required=True)
    ap.add_argument("--holdout", type=float, default=0.05)
    ap.add_argument("--chunk", type=int, default=2048)
    args = ap.parse_args()

    import jax.numpy as jnp
    from kagg.il import replays as RP
    from kagg.rl import jax_act as A, jax_policy as P

    name_of = {code: nm for nm, code in RP.OP_CODE.items()}

    z = np.load(args.rows)
    n = len(z["y_op"])
    n_val = int(n * args.holdout)
    lo = n - n_val
    print(f"{args.rows}: {n:,} rows, scoring the whole {n_val:,}-row held-out block", flush=True)

    # **Read each array ONCE.** The cache is `np.savez_compressed`, so `z[k][idx]` decompresses the
    # WHOLE multi-GB array for every access -- eight chunks meant eight full decompressions and the
    # script sat there doing nothing visible. Slice to the held-out block on the single read.
    keep = {}
    for k in ("tiles", "units", "glob", "y_op", "live", "m_op"):
        keep[k] = np.asarray(z[k])[lo:]
        print(f"  loaded {k:<8}{str(keep[k].shape):>22}", flush=True)
    val = np.arange(n_val)

    with open(args.ckpt, "rb") as fh:
        ck = pickle.load(fh)
    params = ck["params"] if "params" in ck else ck
    ca = ck.get("args") or {}
    model = P.Policy(d_model=ca.get("d_model", 128), n_heads=ca.get("heads", 4),
                     n_layers=ca.get("layers", 3))

    hit = np.zeros(len(name_of) + 1, dtype=np.int64)
    tot = np.zeros(len(name_of) + 1, dtype=np.int64)
    # **What it plays INSTEAD, per teacher op.** An accuracy alone cannot separate three failures
    # that need three different fixes: predicting a MOVE means the walk is bleeding into the work
    # head, predicting a sibling work op means genuine confusion, and predicting the no-op means
    # class imbalance against a permissive mask. HARVEST is 48.3% while its mask
    # (`jax_masks.py:123`) already restricts it to ripe tiles, so the information is present and the
    # question is purely what wins instead.
    conf = np.zeros((len(name_of) + 1, len(name_of) + 1), dtype=np.int64)

    for s in range(0, len(val), args.chunk):
        sl = slice(s, s + args.chunk)
        heads, _v = model.apply(params, jnp.asarray(keep["tiles"][sl]),
                                jnp.asarray(keep["units"][sl]), jnp.asarray(keep["glob"][sl]))
        logits = P._masked_logits(heads["op"], jnp.asarray(keep["m_op"][sl]))
        pred = np.asarray(jnp.argmax(logits, axis=-1))
        y = keep["y_op"][sl]
        live = keep["live"][sl] > 0.5
        acted = live & (y != 0)                     # op 0 is the no-op; `bc_replay` scores the rest
        for c in np.unique(y[acted]):
            m = acted & (y == c)
            tot[c] += int(m.sum())
            hit[c] += int((pred[m] == c).sum())
            for p, k in zip(*np.unique(pred[m], return_counts=True)):
                conf[c, int(p)] += int(k)

    rows = [(name_of.get(int(c), str(c)), int(tot[c]), int(hit[c]))
            for c in range(len(tot)) if tot[c]]
    rows.sort(key=lambda r: -r[1])

    print(f"\n  {'op':<22}{'n':>10}{'acc':>8}")
    for nm, t, h in rows:
        print(f"  {nm:<22}{t:>10,}{h / t:>8.1%}")

    def agg(keep):
        t = sum(r[1] for r in rows if keep(r[0]))
        h = sum(r[2] for r in rows if keep(r[0]))
        return t, (h / t if t else 0.0)

    tm, am = agg(lambda nm: nm in MOVE)
    tw, aw = agg(lambda nm: nm not in MOVE)
    ta, aa = agg(lambda _nm: True)
    print(f"\n  {'class':<22}{'n':>10}{'acc':>8}")
    print(f"  {'MOVEMENT':<22}{tm:>10,}{am:>8.1%}")
    print(f"  {'WORK (router owns move)':<22}{tw:>10,}{aw:>8.1%}")
    print(f"  {'ALL ACTED':<22}{ta:>10,}{aa:>8.1%}")
    print(f"\n  movement is {tm / max(1, ta):.0%} of acted ops")
    print("  compare: hand-feature model on the same teacher, work-only, was 97.4%")

    print("\n  what it plays INSTEAD, for the ops that fail")
    for nm, t, h in rows:
        if t < 200 or h / t > 0.80:
            continue
        c = next(k for k, v in name_of.items() if v == nm)
        order = np.argsort(-conf[c])
        parts = []
        for p in order[:4]:
            if conf[c, p] == 0 or int(p) == c:
                continue
            parts.append(f"{name_of.get(int(p), int(p))} {conf[c, p] / t:.0%}")
        moves = sum(conf[c, k] for k, v in name_of.items() if v in MOVE)
        print(f"  {nm:<20} n={t:>7,}  correct {h / t:>5.0%}  "
              f"MOVES {moves / t:>4.0%}  |  {', '.join(parts)}")


main()
