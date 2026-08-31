"""Add the vocabulary size and feature widths to a checkpoint that was written without them.

    python -u scripts/stamp_checkpoint_provenance.py --ckpt <path> --vocab <path>

WHY THIS EXISTS
---------------
`dagger_tape.py:725` decides whether to keep or reset the bundle head with

    reset_bundle = ckpt.get("vocab_size") != vocab.size

and its own comment explains that a MISSING value counts as different on purpose: "An unrecorded
vocabulary cannot be shown to match, so it is reset." That is the right rule. But it means a
checkpoint written by a script that forgot the field loses its market head on the next `--init`,
with one line of warning in the middle of a startup banner.

That happened at 08:30:25 on 2026-08-31: the clone's bundle head, fitted to a geometric-mean 0.99516
on the teacher's own baskets, was reset to random initialisation.

The params are untouched here. Only the metadata that describes them is added, and only when it can
be verified: the vocabulary file is loaded and its size compared with the bundle head's actual
output width, so a wrong `--vocab` is refused rather than stamped on.
"""
import argparse
import pathlib
import pickle
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--vocab", required=True)
    args = ap.parse_args()

    from kagg.il import market_bundles as MB
    from kagg.rl import jax_obs

    ckpt_path = pathlib.Path(args.ckpt)
    ck = pickle.load(open(ckpt_path, "rb"))
    vocab = MB.load_vocab(args.vocab)

    print("ckpt   %s" % ckpt_path, flush=True)
    print("before vocab_size=%s tile=%s unit=%s glob=%s"
          % (ck.get("vocab_size"), ck.get("tile_features"), ck.get("unit_features"),
             ck.get("global_features")), flush=True)

    backup = ckpt_path.with_suffix(".pkl.bak")
    if not backup.exists():
        shutil.copy2(ckpt_path, backup)
        print("backup %s" % backup, flush=True)

    ck["vocab_size"] = vocab.size
    ck["vocab_path"] = str(args.vocab)
    ck["tile_features"] = jax_obs.TILE_FEATURES
    ck["unit_features"] = jax_obs.UNIT_FEATURES
    ck["global_features"] = jax_obs.GLOBAL_FEATURES

    tmp = ckpt_path.with_suffix(".pkl.tmp")
    with open(tmp, "wb") as f:
        pickle.dump(ck, f)
    tmp.replace(ckpt_path)

    print("after  vocab_size=%s tile=%s unit=%s glob=%s"
          % (ck["vocab_size"], ck["tile_features"], ck["unit_features"],
             ck["global_features"]), flush=True)
    print("params untouched", flush=True)


if __name__ == "__main__":
    main()
