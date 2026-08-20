"""When the tree picks the WRONG block, how wrong is it? Exact match is a harsh metric.

Alex, 2026-08-20: "if we can match the kawa it puts us pretty damm high".

`fit_day_classifier.py` reports EXACT block agreement -- 83.6% at d6, 58.2% at d12 on held-out
games. That undersells it, because two blocks can differ only in which thirsty tile gets watered
first. Measured on the same player: movement is 44-62% of what separates two of his days, WATER is
61-100% of the field-work differences, and the router re-derives both from the live board at each
stop (`_live_ops`). A wrong pick that differs only there costs nothing to execute.

So this asks a better question: **when the tree is wrong, is the block it chose a near neighbour of
the right one, or an unrelated day?**

The comparison that makes the answer meaningful is against a RANDOM pick from the same day's
library. If wrong picks are as far from the truth as a random block, the tree's confidence is
worthless off-target. If they are much closer, exact-match accuracy is a floor and the effective
accuracy is far higher.

**This measures op agreement, not money.** A replay-based score -- run both blocks against the same
board in the fast sim and compare harvested/sold/banked -- would be the real answer, and the sim is
parity-exact at 300/300 full-length episodes so it is available. This is the cheap version, and it
is honest about being a proxy: two sequences can be op-identical and bank differently if timing
shifts a sale across a price move.

    python -u scripts/wrong_pick_cost.py --rows data/day_rows_kawa.json --depth 4
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.what_differs_between_blocks import diff, TURNS_PER_DAY      # noqa: E402


def distance(a, b):
    """Differing unit-slots between two whole days, split into cheap and expensive."""
    tally = collections.Counter()
    diff({h: a[h] for h in range(TURNS_PER_DAY)},
         {h: b[h] for h in range(TURNS_PER_DAY)}, tally)
    cheap = expensive = 0
    for k, v in tally.items():
        if k.startswith("_") or k == "market orders differ":
            continue
        # Movement and watering are re-derived by the router from the live board, so a block that
        # disagrees only there is executed correctly anyway. Everything else is a real difference.
        if "movement" in k or "idle" in k:
            cheap += v
        else:
            expensive += v
    return cheap, expensive, tally["market orders differ"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--min-games", type=int, default=12)
    ap.add_argument("--max-day", type=int, default=16)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import numpy as np
    from sklearn.tree import DecisionTreeClassifier

    rows = json.loads(pathlib.Path(args.rows).read_text())
    blocks_path = pathlib.Path(args.rows).with_name(
        pathlib.Path(args.rows).stem + ".blocks.json")
    blocks = json.loads(blocks_path.read_text())

    names = sorted({k for r in rows for k in r["x"]})
    index = {n: i for i, n in enumerate(names)}

    games = sorted({(r["game"], r["seat"]) for r in rows})
    rng = np.random.default_rng(args.seed)
    rng.shuffle(games)
    n_test = max(1, int(len(games) * args.holdout))
    test_games = set(map(tuple, games[:n_test]))

    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)

    print("%d rows, %d features, %d test game-seats\n" % (len(rows), len(names), n_test))
    print("%4s %7s %8s %11s %11s %11s"
          % ("day", "exact", "wrong n", "wrong: real", "random: real", "wrong/random"))

    for day in sorted(by_day):
        if day > args.max_day:
            break
        day_rows = by_day[day]
        tr = [r for r in day_rows if (r["game"], r["seat"]) not in test_games]
        te = [r for r in day_rows if (r["game"], r["seat"]) in test_games]
        if len(tr) < args.min_games or not te:
            continue
        lib = blocks.get(str(day), {})

        def mat(rs):
            x = np.zeros((len(rs), len(names)))
            for i, r in enumerate(rs):
                for k, v in r["x"].items():
                    x[i, index[k]] = v
            return x

        clf = DecisionTreeClassifier(max_depth=args.depth, random_state=args.seed)
        clf.fit(mat(tr), [r["block"] for r in tr])
        pred = clf.predict(mat(te))

        exact = 0
        wrong_real, wrong_n = [], 0
        rand_real = []
        known = [b for b in lib if len(lib[b]) == TURNS_PER_DAY]
        for r, p in zip(te, pred):
            truth = r["block"]
            if p == truth:
                exact += 1
                continue
            if p not in lib or truth not in lib:
                continue
            if len(lib[p]) != TURNS_PER_DAY or len(lib[truth]) != TURNS_PER_DAY:
                continue
            wrong_n += 1
            _c, e, _m = distance(lib[p], lib[truth])
            wrong_real.append(e)
            # Baseline: a block drawn at random from the same day's library.
            other = known[int(rng.integers(len(known)))]
            if other != truth and len(lib[other]) == TURNS_PER_DAY:
                _c2, e2, _m2 = distance(lib[other], lib[truth])
                rand_real.append(e2)

        if not wrong_real or not rand_real:
            print("%4d %6.1f%% %8d      -           -           -" %
                  (day, 100.0 * exact / len(te), wrong_n))
            continue
        w = sum(wrong_real) / len(wrong_real)
        rd = sum(rand_real) / len(rand_real)
        print("%4d %6.1f%% %8d %11.1f %11.1f %11s"
              % (day, 100.0 * exact / len(te), wrong_n, w, rd,
                 "%.2f" % (w / rd) if rd else "-"))

    print("\n'real' counts differing unit-slots EXCLUDING movement and idle, which the router")
    print("re-derives from the live board. wrong/random well below 1.00 means the tree's mistakes")
    print("are near neighbours, and exact-match accuracy is a floor rather than the true rate.")


if __name__ == "__main__":
    main()
