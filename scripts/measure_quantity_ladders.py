"""What quantities does the teacher actually trade, and what do our ladders cost us?

`SELL_BUCKETS = [0,1,3,10,30]` and `BUY_BUCKETS = [0,1,2,5]` were written down, not measured. The
student can only emit a ladder rung, so any teacher quantity off the ladder is an error the network
cannot drive to zero however long it trains -- and `BUY_SEED CARROT 8` projects onto 5, which is a
37% shortfall on every seed purchase of that size.

This prints the histogram and the projection error for the ladders as they stand, so a new ladder is
chosen from the distribution rather than from taste.

    python -u scripts/measure_quantity_ladders.py --shards /home/alex/labels_r0b --lines 200000
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.rl import jax_policy as P                           # noqa: E402

LADDERS = {
    "SELL": np.asarray(P.SELL_BUCKETS),
    "BUY_PRODUCT": np.asarray(P.BUY_BUCKETS),
    "BUY_SEED": np.asarray(P.BUY_BUCKETS),
    "BUY_ANIMAL": np.asarray(P.BUY_BUCKETS),
}


def projection_error(counts, ladder):
    """Mean |q - nearest(q)| / q over the observed quantities, weighted by how often each appears."""
    total = err = 0
    for q, n in counts.items():
        if q <= 0:
            continue
        near = int(ladder[int(np.argmin(np.abs(ladder - q)))])
        err += n * abs(q - near) / q
        total += n
    return (err / total) if total else 0.0


def best_ladder(counts, size, must_have_zero=True):
    """Greedy: repeatedly add the rung that removes the most weighted error. Not optimal, but it is
    read off the data, which is the whole point."""
    rungs = [0] if must_have_zero else []
    candidates = sorted(q for q in counts if q > 0)
    while len(rungs) < size and candidates:
        pick = min(candidates,
                   key=lambda c: projection_error(counts, np.asarray(sorted(rungs + [c]))))
        rungs = sorted(rungs + [pick])
        candidates = [c for c in candidates if c not in rungs]
    return rungs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", required=True)
    ap.add_argument("--lines", type=int, default=200000, help="lines to read per shard")
    args = ap.parse_args()

    counts = collections.defaultdict(collections.Counter)
    turns = 0
    for path in sorted(glob.glob(args.shards.rstrip("/") + "/*.jsonl")):
        with open(path) as fh:
            for i, line in enumerate(fh):
                if i >= args.lines:
                    break
                turns += 1
                for o in (json.loads(line).get("act") or {}).get("market") or ():
                    if isinstance(o, (list, tuple)) and o:
                        q = int(o[2]) if len(o) > 2 else 1
                        counts[str(o[0])][q] += 1

    print("turns read: %s\n" % format(turns, ","))
    for op in sorted(counts):
        c = counts[op]
        n = sum(c.values())
        print("%-12s  %s orders" % (op, format(n, ",")))
        for q, k in sorted(c.items())[:24]:
            print("    qty %-4d  %8s  %5.1f%%" % (q, format(k, ","), 100.0 * k / n))
        ladder = LADDERS.get(op)
        if ladder is not None:
            print("    current ladder %-18s  mean projection error %5.1f%%"
                  % (list(map(int, ladder)), 100 * projection_error(c, ladder)))
            fitted = best_ladder(c, len(ladder))
            print("    fitted  ladder %-18s  mean projection error %5.1f%%"
                  % (fitted, 100 * projection_error(c, np.asarray(fitted))))
        print()


if __name__ == "__main__":
    main()
