"""Which block does this player play today? A decision tree per day, and it PRINTS ITS RULES.

Alex, 2026-08-20: "what is the classification criteria that returns us a days of tape", and then
"ah ok a decision tree sounds good".

**A tree rather than a net, deliberately.** The artifact Alex asked for has to be editable -- "i do
want to then be able to go in and later change the day parts individually". A tree answers the
question in the form of the answer: readable rules over named features. A net would reach similar
accuracy and tell us nothing about the criteria, which was the actual question. If the tree
plateaus well below what the data allows, that is the moment to reach for something bigger.

**One tree per day.** Block ids are day-local -- block `a1b2c3d4e5` on d5 has no meaning on d6 --
so a single model with `day` as a feature would be predicting across incomparable label sets.

**Split by GAME, never by row.** A game contributes ~30 rows that share a seed, an opponent and a
board lineage. Splitting rows at random puts d7 of a game in train and d8 of the SAME game in test,
and the score then measures memorising a game rather than generalising to a new one. This is the
same failure `fit_bc.py` had when its instrument probed the shard it had just trained on.

**Read accuracy against the MAJORITY BASELINE, not against zero.** A day whose top block covers 80%
of games is 80% predictable by a constant. Only the gap over that baseline is information -- the
same trap as the 0.788 empty-bundle rate in the BC work, which was an untrained network's score.

    python -u scripts/fit_day_classifier.py --rows data/day_rows_kawa.json --depth 4
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def vectorise(rows):
    names = sorted({k for r in rows for k in r["x"]})
    index = {n: i for i, n in enumerate(names)}
    return names, index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--min-games", type=int, default=12)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--show-rules-for", type=int, nargs="*", default=[8, 12, 16])
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import numpy as np
    from sklearn.tree import DecisionTreeClassifier, export_text

    rows = json.loads(pathlib.Path(args.rows).read_text())
    names, index = vectorise(rows)
    print("%d rows, %d features" % (len(rows), len(names)))

    games = sorted({(r["game"], r["seat"]) for r in rows})
    rng = np.random.default_rng(args.seed)
    rng.shuffle(games)
    n_test = max(1, int(len(games) * args.holdout))
    test_games = set(map(tuple, games[:n_test]))
    print("game-seats: %d train, %d held out\n" % (len(games) - n_test, n_test))

    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)

    print("%4s %7s %7s %8s %9s %9s %8s"
          % ("day", "train", "test", "classes", "baseline", "tree", "gain"))
    gains = []
    kept_rules = {}
    for day in sorted(by_day):
        day_rows = by_day[day]
        tr = [r for r in day_rows if (r["game"], r["seat"]) not in test_games]
        te = [r for r in day_rows if (r["game"], r["seat"]) in test_games]
        if len(tr) < args.min_games or not te:
            continue

        def mat(rs):
            x = np.zeros((len(rs), len(names)), dtype=np.float64)
            for i, r in enumerate(rs):
                for k, v in r["x"].items():
                    x[i, index[k]] = v
            return x, [r["block"] for r in rs]

        xtr, ytr = mat(tr)
        xte, yte = mat(te)

        # The baseline is the TRAIN majority applied to test -- what a constant would score.
        majority = collections.Counter(ytr).most_common(1)[0][0]
        base = sum(1 for y in yte if y == majority) / len(yte)

        clf = DecisionTreeClassifier(max_depth=args.depth, random_state=args.seed)
        clf.fit(xtr, ytr)
        acc = float((clf.predict(xte) == np.array(yte)).mean())
        gains.append(acc - base)
        print("%4d %7d %7d %8d %8.1f%% %8.1f%% %+7.1f%%"
              % (day, len(tr), len(te), len(set(ytr)), 100 * base, 100 * acc,
                 100 * (acc - base)))
        if day in args.show_rules_for:
            kept_rules[day] = export_text(clf, feature_names=names, max_depth=args.depth)

    if gains:
        print("\nmean gain over the majority baseline: %+.1f%% across %d days"
              % (100 * sum(gains) / len(gains), len(gains)))

    for day, text in sorted(kept_rules.items()):
        print("\n=== THE CRITERIA THE TREE FOUND, day %d ===" % day)
        print(text[:2600])


if __name__ == "__main__":
    main()
