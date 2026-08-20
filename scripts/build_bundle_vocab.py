"""Write the market bundle vocabulary from label shards, and report what it would truncate.

The vocabulary is an ARTIFACT, not a constant. The same file has to be used to build the labels, to
fit, and to play -- if it differs anywhere, every bundle index means something else in the loss than
at play time, and nothing offline shows it because every index is still a valid index. So this
writes it once, to a path everything downstream is pointed at.

    python -u scripts/build_bundle_vocab.py --shards /home/alex/labels_r0 \
        --out data/il/bundle_vocab.json

Prints coverage before writing. **Read it.** A bundle outside the vocabulary is one the policy can
never emit, and 128 slots looked sufficient on a four-game pilot (117 bundles) against 197 on the
full 640-game set.
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.il import market_bundles as MB          # noqa: E402
from kagg.rl import jax_policy as P               # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", required=True, help="directory of *.jsonl label shards")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-size", type=int, default=None,
                    help="defaults to jax_policy.N_BUNDLES -- the head cannot express more")
    args = ap.parse_args()

    max_size = args.max_size or P.N_BUNDLES
    paths = sorted(glob.glob(args.shards.rstrip("/") + "/*.jsonl"))
    if not paths:
        raise SystemExit("no shards under %s" % args.shards)

    counts = collections.Counter()
    turns = 0
    for p in paths:
        with open(p) as fh:
            for line in fh:
                row = json.loads(line)
                counts[MB.bundle_of((row.get("act") or {}).get("market") or [])] += 1
                turns += 1
    print("shards %d   player-turns %s   distinct bundles %s"
          % (len(paths), format(turns, ","), format(len(counts), ",")), flush=True)

    every = list(counts.elements())
    vocab = MB.Vocabulary.from_bundles(every, max_size=max_size)
    cov = vocab.coverage(every)
    print("vocabulary %d of %d head slots   coverage %.4f%%" % (vocab.size, max_size, 100.0 * cov))

    if vocab.size >= max_size and len(counts) > max_size:
        lost = len(counts) - max_size
        print("  TRUNCATED: %d bundles do not fit and can NEVER be emitted by the policy." % lost)
        print("  Raise jax_policy.N_BUNDLES above %d, or accept the %.4f%% of turns lost."
              % (len(counts), 100.0 * (1.0 - cov)))

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([[list(pair) for pair in vocab.bundle(i)]
                               for i in range(vocab.size)]))
    print("wrote %s" % out)

    print("\n  rank   count    cum%   bundle")
    tot, cum = sum(counts.values()), 0
    for i, (b, n) in enumerate(counts.most_common(12), 1):
        cum += n
        label = ", ".join("%s %s" % (a, c) if c else a for a, c in b) or "(empty)"
        print("  %4d  %7d  %6.2f   %s" % (i, n, 100.0 * cum / tot, label[:84]))


if __name__ == "__main__":
    main()
