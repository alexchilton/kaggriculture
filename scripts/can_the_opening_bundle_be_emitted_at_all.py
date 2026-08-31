"""Turn 0's bundle is 0/16 in every round ever logged. Is it emittable, or is it forbidden?

    python -u scripts/can_the_opening_bundle_be_emitted_at_all.py --run data/dagger_tape/<run>

THE MEASUREMENT THIS ANSWERS
----------------------------
The 50-epoch offline fit reached unit-op agreement 0.662 and movement 0.320, then banked **$0 over
four seasons with `hands 0` on every day**. The teacher's opening is five HIREs plus the animals and
the seed, all in turn 0's single bundle. If that bundle never fires there is no crew, and no amount
of movement skill matters with one unit on the board.

`turn0 bundle 0/16` has been in every round line of every run. That is the number that was saying so.

**Three things can produce 0/16, and they need opposite fixes:**

    forbidden   the label's index is False in the bundle mask, so the masked argmax can never
                select it and `bc_dagger.loss_fn` zeroes the loss on it. Unlearnable by
                construction -- this project's recurring defect, and the reason `WEST` was pinned
                for ten rounds on a stranded hand.
    unsayable   `Vocabulary.index` returned 0 (EMPTY) for the teacher's opening, so the LABEL
                itself is "place no orders" and the student is scoring 0/16 against a target that
                is already wrong. This is the 2026-08-22 failure exactly.
    just hard   the label is present and legal, the student simply ranks another bundle above it.
                Then it is a training problem and more epochs / more day-0 weight is the answer.

WHAT IS PRINTED
---------------
For every turn-0 row in the stored aggregate: the teacher's bundle index, whether that index is
legal under the row's own mask, what the bundle decodes to, what the student picks instead, and
where the true label ranks in the student's ordering. A rank of 2 or 3 is "just hard"; a rank of
200 with the label masked out is not.

No environment and no rollout -- the aggregate rows already carry `masks` and `labels`.
"""
import argparse
import collections
import importlib.util
import pathlib
import pickle
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--ckpt", default=None, help="defaults to <run>/offline_50epochs.pkl if present")
    args = ap.parse_args()

    import jax.numpy as jnp

    from kagg.il import market_bundles as MB
    from kagg.rl import jax_policy as P

    DT = _load("dagger_tape", REPO / "scripts/dagger_tape.py")

    run = pathlib.Path(args.run)
    ckpt = pathlib.Path(args.ckpt) if args.ckpt else (run / "offline_50epochs.pkl")
    if not ckpt.exists():
        ckpt = run / "latest.pkl"
    ck = pickle.load(open(ckpt, "rb"))
    agg = pickle.load(open(run / "aggregate.pkl", "rb"))
    rows = list(agg.get("expert", [])) + list(agg.get("student", []))

    a = ck.get("args") or {}
    model = P.Policy(d_model=int(a.get("d_model", 128)), n_heads=int(a.get("heads", 4)),
                     n_layers=int(a.get("layers", 3)))
    params = ck["params"]
    vocab = MB.load_vocab(str(ck.get("vocab_path") or a.get("vocab")))
    class_w = DT.bundle_class_weights(rows, 1.0)

    turn0 = [r for r in rows if int(r.get("turn", 9999)) == 0]
    print("ckpt   %s" % ckpt, flush=True)
    print("vocab  %s  (%d entries)" % (ck.get("vocab_path") or a.get("vocab"), vocab.size), flush=True)
    print("turn-0 rows in the aggregate: %d\n" % len(turn0), flush=True)
    if not turn0:
        print("no turn-0 rows stored; nothing to check", flush=True)
        return

    empty_idx = vocab.index(MB.bundle_of([]))
    batch = DT.stack(turn0, class_w)
    heads, _v = model.apply(params, *batch["obs"])
    logits = np.asarray(heads["bundle"])
    mask = np.asarray(batch["masks"]["bundle"]).astype(bool)
    labels = np.asarray(batch["labels"]["bundle"]).reshape(len(turn0), -1)[:, 0]

    verdicts = collections.Counter()
    for i, r in enumerate(turn0):
        lab = int(labels[i])
        legal = bool(mask[i].reshape(-1)[lab])
        masked = np.where(mask[i].reshape(-1), logits[i].reshape(-1), -np.inf)
        pick = int(np.argmax(masked))
        # Rank of the true label among LEGAL classes, best first.
        order = np.argsort(-masked)
        rank = int(np.flatnonzero(order == lab)[0]) + 1 if legal else -1

        if lab == empty_idx:
            v = "LABEL IS EMPTY (unsayable)"
        elif not legal:
            v = "LABEL MASKED ILLEGAL (unlearnable)"
        elif rank <= 3:
            v = "legal, rank<=3 (just hard)"
        else:
            v = "legal, rank>3 (just hard, far)"
        verdicts[v] += 1

        if i < 6:
            print("  ep %-26s label %3d legal=%-5s rank %4s  picked %3d"
                  % (str(r.get("ep"))[:26], lab, legal, rank if rank > 0 else "-", pick), flush=True)
            print("      teacher bundle  %s" % (list(vocab.bundle(lab)) if lab < vocab.size else "?"),
                  flush=True)
            print("      student bundle  %s" % (list(vocab.bundle(pick)) if pick < vocab.size else "?"),
                  flush=True)

    print("\nVERDICT over %d turn-0 rows" % len(turn0), flush=True)
    for v, n in verdicts.most_common():
        print("  %-38s %d" % (v, n), flush=True)
    print("\n  EMPTY index in this vocabulary: %d" % empty_idx, flush=True)
    print("  labels seen: %s" % sorted(set(int(x) for x in labels)), flush=True)


if __name__ == "__main__":
    main()
