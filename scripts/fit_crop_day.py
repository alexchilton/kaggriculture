"""Per day, can a tree pick the crop multiset from the dawn board -- held out by GAME?

Alex, 2026-08-21: "yeah try it on tets - i reckon it should work".

Class counts say what is POSSIBLE, not what is learnable. `scripts/class_counts_per_day.py` shows
tetsuya's mid-season sits at 10-21 classes with a 6-13 row library at 90% coverage, which is small
enough to select from. This is the test of whether anything actually selects it.

Two rules that decide whether the number means anything:

**Split by GAME, never by row.** Two days from the same season share a board, so a row-level split
leaks the answer across the fold. This has produced flattering numbers in this project before.

**The baseline is the TRAIN majority, evaluated on the held-out games.** Not the test majority --
that peeks. A day whose modal class covers 53% of seasons is not "learned" by a tree scoring 55%.

Because the mid-season label is 96-100% pure WHEAT for this player, the multiset is really an
integer. So the count is also reported as a regression: exact hit rate, within-one hit rate, and
mean absolute error. A tree that gets the count within one tile is useful; a classifier scoring 30%
on 17 unordered labels may be doing the same thing and reading as a failure.

    python -u scripts/fit_crop_day.py --features data/day_rows_tets.json \\
        --targets data/target_rows_tets.json
"""

import argparse
import collections
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text  # noqa: E402


def load(features, targets):
    feat = json.loads(pathlib.Path(features).read_text())
    targ = json.loads(pathlib.Path(targets).read_text())
    lab = {(t["game"], t["seat"], t["day"]):
           tuple(sorted(t["target"].get("plants") or [])) for t in targ}

    # **Deduplicate on (game, seat, day).** 167 episode ids sit in more than one directory under
    # `data/seed_scripts/`, so the extractors read the same replay several times and emit the same
    # day repeatedly. Kawashigi reported 228 rows a day from 213 game-seats, Ryo 145 from 109 --
    # a quarter of his rows were copies. The (game, seat) fold split keeps every copy in the same
    # fold, so this is not train/test leakage, but it silently reweights the duplicated seasons.
    rows, seen = [], set()
    for f in feat:
        k = (f.get("game"), f.get("seat"), f.get("day"))
        if k not in lab or k in seen:
            continue
        seen.add(k)
        rows.append({"game": f.get("game"), "seat": f.get("seat"), "day": f.get("day"),
                     "x": f["x"], "y": lab[k]})
    if rows and not rows[0]["x"]:
        raise SystemExit("features are empty -- build_day_rows writes them under 'x'")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--rules-for", nargs="*", type=int, default=[])
    args = ap.parse_args()

    rows = load(args.features, args.targets)
    if not rows:
        raise SystemExit("no (game, seat, day) key matched between the two files")
    names = sorted({k for r in rows for k in r["x"]})
    print("%d rows, %d features, %d game-seats\n"
          % (len(rows), len(names), len({(r["game"], r["seat"]) for r in rows})))

    seats = sorted({(r["game"], r["seat"]) for r in rows})
    rng = np.random.RandomState(0)
    rng.shuffle(seats)
    cut = int(len(seats) * (1 - args.holdout))
    train_seats, test_seats = set(seats[:cut]), set(seats[cut:])
    print("held out %d of %d game-seats\n" % (len(test_seats), len(seats)))

    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)

    print("%4s %6s %6s %8s %8s %8s   %8s %8s %7s"
          % ("day", "train", "test", "classes", "base", "tree", "n exact", "n +-1", "MAE"))
    for day in sorted(by_day):
        rs = by_day[day]
        tr = [r for r in rs if (r["game"], r["seat"]) in train_seats]
        te = [r for r in rs if (r["game"], r["seat"]) in test_seats]
        if len(tr) < 10 or len(te) < 5:
            continue

        Xtr = np.array([[float(r["x"].get(n, 0) or 0) for n in names] for r in tr])
        Xte = np.array([[float(r["x"].get(n, 0) or 0) for n in names] for r in te])
        ytr = [r["y"] for r in tr]
        yte = [r["y"] for r in te]

        # Baseline: the TRAIN majority class, scored on the held-out games.
        modal = collections.Counter(ytr).most_common(1)[0][0]
        base = sum(1 for y in yte if y == modal) / len(yte)

        # The label map comes from TRAIN only. A class that appears only in the held-out games maps
        # to -1, which the tree can never predict -- that is correct, not a bug: it is a class we
        # have never seen and would have to get wrong in play too.
        ids = {y: i for i, y in enumerate(sorted(set(ytr)))}
        clf = DecisionTreeClassifier(max_depth=args.depth, random_state=0) \
            .fit(Xtr, [ids[y] for y in ytr])
        acc = sum(1 for p, y in zip(clf.predict(Xte), (ids.get(y, -1) for y in yte))
                  if p == y) / len(yte)

        # The same day as a COUNT, because the multiset is 96-100% one crop for this player.
        ntr = np.array([len(y) for y in ytr], dtype=float)
        nte = np.array([len(y) for y in yte], dtype=float)
        reg = DecisionTreeRegressor(max_depth=args.depth, random_state=0).fit(Xtr, ntr)
        pred = np.round(reg.predict(Xte))
        exact = float((pred == nte).mean())
        near = float((np.abs(pred - nte) <= 1).mean())
        mae = float(np.abs(pred - nte).mean())

        print("%4d %6d %6d %8d %7.1f%% %7.1f%%   %7.1f%% %7.1f%% %7.2f"
              % (day, len(tr), len(te), len(set(ytr)), 100 * base, 100 * acc,
                 100 * exact, 100 * near, mae))

        if day in args.rules_for:
            print(export_text(reg, feature_names=names, max_depth=3))

    print("\nbase = TRAIN majority class scored on held-out games.  tree must BEAT it.")
    print("n exact / n +-1 / MAE are the same day predicted as a COUNT, not a class.")


if __name__ == "__main__":
    main()
