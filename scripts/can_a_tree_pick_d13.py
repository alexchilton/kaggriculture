"""Given the board at the end of d12, can a tree pick d13's planting?

Alex, 2026-08-21: "i want to know how well the decision tree can choose d13 based on the state of
d12 and what we know - and dont forget the animals and straw/melon are not interesing and probably
also forget the buy sell etc."

So the label is the PLANTING and nothing else, with the three things he has ruled out taken out:

  animals        already absent -- the label reads `plants`, never `places`
  melon/straw    ONE slot, chosen at d3 by `melon_branch` from the opponent's melon count.
                 MELON and STRAWBERRY collapse to BERRY.
  buys / sells   the h16 cadence handles them once the land is bought.

That leaves two candidate labels and they answer different questions:

  crop SET        WHICH crops.        A real decision.
  crop MULTISET   which and HOW MANY. The count is turn-bounded, not chosen -- measured over
                  2,982 mid-season day-rows, `corr(wheat, free_tiles_at_dawn) = 0.274` while his
                  day is 53.6% travel with zero idle turns on 43.4% of days.

Both are reported. If the SET is learnable and the MULTISET is not, that is the count being a
consequence rather than a choice, and the executor should be setting it.

**Split by GAME, and the baseline is the TRAIN majority scored on held-out games.** A row-level
split leaks the board across the fold; a test-majority baseline peeks.

    python -u scripts/can_a_tree_pick_d13.py --features data/day_rows_kawa.json \\
        --targets data/target_rows_kawa_norm_dedup.json --day 13
"""

import argparse
import collections
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from sklearn.tree import DecisionTreeClassifier, export_text     # noqa: E402

#: MELON and STRAWBERRY are the same slot. `melon_branch` picks between them at d3 from the
#: opponent's melon tile count, and `melon + strawberry == 31` in all 226 of his seasons.
BERRY = {"MELON": "BERRY", "STRAWBERRY": "BERRY"}


def labels(target, berry):
    p = [BERRY.get(c, c) if berry else c for c in (target.get("plants") or [])]
    return tuple(sorted(set(p))), tuple(sorted(p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--day", type=int, default=13)
    ap.add_argument("--days", nargs="*", type=int,
                    help="sweep several days and print one row each")
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--rules", action="store_true")
    #: **`my_seed_*` is a decision already made.** The tree found d13 from `my_seed_STRAWBERRY`
    #: alone at 98.4%, but that seed was BOUGHT on d12 -- so it reads a choice he has already paid
    #: for rather than predicting one. Dropping the seed features asks whether the BOARD carries the
    #: same information. If accuracy holds, the tree is doing real work; if it falls to the
    #: baseline, it was echoing the purchase.
    ap.add_argument("--no-seed-features", action="store_true")
    args = ap.parse_args()

    if args.days:
        return sweep(args)

    feat = json.loads(pathlib.Path(args.features).read_text())
    targ = json.loads(pathlib.Path(args.targets).read_text())
    lab = {(t["game"], t["seat"], t["day"]): t["target"] for t in targ}

    rows, seen = [], set()
    for f in feat:
        k = (f.get("game"), f.get("seat"), f.get("day"))
        if k not in lab or k in seen or f.get("day") != args.day:
            continue
        seen.add(k)
        rows.append({"seat": (f["game"], f["seat"]), "x": f["x"], "t": lab[k]})
    if not rows:
        raise SystemExit("no rows for day %d" % args.day)

    names = sorted({n for r in rows for n in r["x"]})
    if args.no_seed_features:
        names = [n for n in names if not n.startswith("my_seed_")]
        print("dropped %d my_seed_* features" % (64 - len(names)))
    seats = sorted({r["seat"] for r in rows})
    rng = np.random.RandomState(0)
    rng.shuffle(seats)
    cut = int(len(seats) * (1 - args.holdout))
    train, test = set(seats[:cut]), set(seats[cut:])
    print("day %d: %d seasons, %d features, %d held out\n"
          % (args.day, len(rows), len(names), len(test)))

    print("%-22s %8s %9s %8s %8s" % ("label", "classes", "baseline", "tree", "gain"))
    for berry in (False, True):
        for which, idx in (("crop SET", 0), ("crop MULTISET", 1)):
            y = {r["seat"]: labels(r["t"], berry)[idx] for r in rows}
            tr = [r for r in rows if r["seat"] in train]
            te = [r for r in rows if r["seat"] in test]
            Xtr = np.array([[float(r["x"].get(n, 0) or 0) for n in names] for r in tr])
            Xte = np.array([[float(r["x"].get(n, 0) or 0) for n in names] for r in te])
            ytr = [y[r["seat"]] for r in tr]
            yte = [y[r["seat"]] for r in te]

            modal = collections.Counter(ytr).most_common(1)[0][0]
            base = sum(1 for v in yte if v == modal) / len(yte)
            ids = {v: i for i, v in enumerate(sorted(set(ytr)))}
            clf = DecisionTreeClassifier(max_depth=args.depth, random_state=0) \
                .fit(Xtr, [ids[v] for v in ytr])
            acc = sum(1 for p, v in zip(clf.predict(Xte), (ids.get(v, -1) for v in yte))
                      if p == v) / len(yte)
            tag = "%s%s" % (which, "  (berry)" if berry else "")
            print("%-22s %8d %8.1f%% %7.1f%% %+7.1f"
                  % (tag, len(set(ytr)), 100 * base, 100 * acc, 100 * (acc - base)))
            if args.rules and berry and idx == 0:
                print(export_text(clf, feature_names=names, max_depth=3))

    print("\nbaseline = TRAIN majority class scored on held-out GAMES. The tree must beat it.")


def sweep(args):
    """One row per day: can the board at dawn pick that day's planting?

    The question this answers: the mid-season COUNT was measured as turn-bounded rather than chosen
    (`corr(wheat, free_tiles_at_dawn) = 0.274` pooled over d14-d27), yet a depth-3 tree read d13 and
    d14's multiset at 70-73% against a 25-31% baseline. Both cannot describe the whole middle. If
    the multiset gain decays across the sweep, the correlation was pooling days that behave
    differently; if it holds, the count is learnable and the planner should be told the number.
    """
    feat = json.loads(pathlib.Path(args.features).read_text())
    targ = json.loads(pathlib.Path(args.targets).read_text())
    lab = {(t["game"], t["seat"], t["day"]): t["target"] for t in targ}

    print("seed features dropped: %s   depth %d   holdout %.0f%%\n"
          % (args.no_seed_features, args.depth, 100 * args.holdout))
    print("%4s %7s | %8s %8s %8s %7s | %8s %8s %8s %7s"
          % ("day", "seasons", "sets", "base", "tree", "gain",
             "multi", "base", "tree", "gain"))
    for day in args.days:
        rows, seen = [], set()
        for f in feat:
            k = (f.get("game"), f.get("seat"), f.get("day"))
            if k not in lab or k in seen or f.get("day") != day:
                continue
            seen.add(k)
            rows.append({"seat": (f["game"], f["seat"]), "x": f["x"], "t": lab[k]})
        if len(rows) < 20:
            continue
        names = sorted({n for r in rows for n in r["x"]})
        if args.no_seed_features:
            names = [n for n in names if not n.startswith("my_seed_")]
        seats = sorted({r["seat"] for r in rows})
        rng = np.random.RandomState(0)
        rng.shuffle(seats)
        cut = int(len(seats) * (1 - args.holdout))
        train, test = set(seats[:cut]), set(seats[cut:])
        tr = [r for r in rows if r["seat"] in train]
        te = [r for r in rows if r["seat"] in test]
        Xtr = np.array([[float(r["x"].get(n, 0) or 0) for n in names] for r in tr])
        Xte = np.array([[float(r["x"].get(n, 0) or 0) for n in names] for r in te])

        line = "%4d %7d" % (day, len(rows))
        for idx in (0, 1):
            ytr = [labels(r["t"], True)[idx] for r in tr]
            yte = [labels(r["t"], True)[idx] for r in te]
            modal = collections.Counter(ytr).most_common(1)[0][0]
            base = sum(1 for v in yte if v == modal) / len(yte)
            ids = {v: i for i, v in enumerate(sorted(set(ytr)))}
            clf = DecisionTreeClassifier(max_depth=args.depth, random_state=0) \
                .fit(Xtr, [ids[v] for v in ytr])
            acc = sum(1 for p, v in zip(clf.predict(Xte), (ids.get(v, -1) for v in yte))
                      if p == v) / len(yte)
            line += " | %8d %7.1f%% %7.1f%% %+6.1f" % (len(ids), 100*base, 100*acc,
                                                       100*(acc-base))
        print(line)
    print("\nbaseline = TRAIN majority scored on held-out GAMES.")


if __name__ == "__main__":
    main()
