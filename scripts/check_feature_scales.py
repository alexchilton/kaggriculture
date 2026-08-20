"""Are the encoder's features on a scale a network can actually use?

Three specific ways this goes wrong, all silent:

  1. **A raw quantity next to a binary flag.** A bank of $121,180 in the same vector as a 0/1
     "is watered" flag means the first layer's gradient is dominated by one feature and the flag is
     numerically invisible. Nothing errors; the model just never learns the flag.
  2. **float16 overflow.** `build_bc_rows` stores features as float16 to fit 920,320 rows in RAM.
     float16's maximum is 65,504 -- a raw bank above that becomes `inf`, and `inf` through a
     LayerNorm produces `nan` for the WHOLE token, silently killing every feature beside it.
  3. **A dead feature.** A column that is constant across every row carries no information and may
     mean the encoder is not reading what it thinks it is. `verify_shard.py` checks carry
     specifically; this checks all of them.

This reads the real npz the fit will consume, so it measures what the network sees rather than what
the encoder intends.

    python -u scripts/check_feature_scales.py --rows /home/alex/rows_r0b
"""

import argparse
import glob
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

FLOAT16_MAX = 65504.0


def report(name, arr):
    """arr is [rows, tokens, features] or [rows, features]."""
    flat = arr.reshape(-1, arr.shape[-1]).astype(np.float32)
    print("\n%s  %s  dtype=%s" % (name, arr.shape, arr.dtype))

    n_inf = int(np.isinf(flat).sum())
    n_nan = int(np.isnan(flat).sum())
    if n_inf or n_nan:
        print("  *** %d inf and %d nan. float16 overflows above %.0f, and one inf through a "
              "LayerNorm makes the whole token nan. ***" % (n_inf, n_nan, FLOAT16_MAX))

    finite = np.where(np.isfinite(flat), flat, 0.0)
    lo, hi = finite.min(axis=0), finite.max(axis=0)
    mean, std = finite.mean(axis=0), finite.std(axis=0)

    big = np.where(np.abs(hi) > 10)[0]
    dead = np.where(std == 0)[0]
    near = np.where(np.abs(hi) > FLOAT16_MAX * 0.1)[0]

    print("  overall   min %+.3f  max %+.3f  mean %+.3f  std %.3f"
          % (finite.min(), finite.max(), finite.mean(), finite.std()))
    print("  features with |max| > 10 : %d of %d%s"
          % (len(big), flat.shape[1], ("  -> " + ", ".join(
              "f%d[%.0f]" % (i, hi[i]) for i in big[:10])) if len(big) else ""))
    print("  constant features        : %d of %d%s"
          % (len(dead), flat.shape[1], ("  -> " + ", ".join(
              "f%d=%.2f" % (i, mean[i]) for i in dead[:10])) if len(dead) else ""))
    if len(near):
        print("  *** within 10%% of the float16 ceiling: %s ***"
              % ", ".join("f%d[%.0f]" % (i, hi[i]) for i in near[:10]))

    # The per-feature table, because "overall std 1.2" can hide one feature at 40,000.
    print("  %-6s %10s %10s %10s %10s" % ("feat", "min", "max", "mean", "std"))
    order = np.argsort(-np.abs(hi))
    for i in order[:8]:
        print("  f%-5d %10.3f %10.3f %10.3f %10.3f" % (i, lo[i], hi[i], mean[i], std[i]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--n", type=int, default=4096)
    args = ap.parse_args()

    shards = sorted(glob.glob(args.rows.rstrip("/") + "/*.npz"))
    if not shards:
        raise SystemExit("no npz under %s" % args.rows)
    d = np.load(shards[0])
    n = min(args.n, len(d["y_bundle"]))
    print("reading %s rows of %s" % (format(n, ","), pathlib.Path(shards[0]).name))

    for key in ("tiles", "units", "glob"):
        report(key, d[key][:n])

    print("\n" + "-" * 74)
    print("What good looks like: |max| in single digits, std within about an order of")
    print("magnitude across features, no constant columns, nothing near 65,504.")
    print("A LayerNorm on the token AFTER the input projection fixes scale BETWEEN tokens;")
    print("it does not rescue a feature that overflowed to inf before it was ever stored.")


if __name__ == "__main__":
    main()
