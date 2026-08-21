"""Predict the CONTENTS of a day's target row, not its identity. And use several previous days.

Alex, 2026-08-21: "i cant believe that the ones past d12 are not completely dependent on the
previous few days...".

He is right, and the earlier test could not have found it. `fit_day_classifier` predicts the row ID
as one of N classes, and at d17 there are 149 distinct ids across 161 training games -- nearly every
row occurs ONCE. A class seen once is unpredictable by construction, whatever the dependence. So
"0.0% at d18" measured the granularity of the label, not the structure of the game.

This asks the question that can actually be answered: how many wheat does he plant today, how much
does he sell, does he buy land. Those repeat constantly even when the whole row never does.

Reported per field, per day, as R^2 on HELD-OUT GAMES against predicting the training mean. R^2 <= 0
means the feature set says nothing; 1.0 is exact. A field can be perfectly predictable while the row
it belongs to is unique.

**History depth is a parameter, because "the previous few days" is the hypothesis under test.**
`--history 3` adds the summaries of d-1, d-2 and d-3.

**Deeper trees than the classifier used.** Adding 32 history features to a depth-4 tree can only
dilute it -- there are more useful splits than depth allows, so the extra columns crowd out the
board. That confound is removed here by fitting a small forest with real depth.

    python -u scripts/fit_row_fields.py --rows data/day_rows_kawa_target.json \\
        --targets data/target_rows_kawa.json --history 3
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.fit_chained_classifier import row_features                # noqa: E402

CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
#: The fields worth predicting: what the day DOES. Chosen before looking at any result.
FIELDS = (["hires", "land", "builds", "feeds", "cares", "harvests", "n_plants"]
          + ["plant_" + c for c in CROPS]
          + ["seed_" + c for c in CROPS]
          + ["sell_WHEAT", "sell_MELON", "sell_STRAWBERRY", "sell_MILK", "sell_WOOL",
             "sell_FERTILIZER"])


def field_value(row, field):
    if row is None:
        return 0.0
    if field == "n_plants":
        return float(len(row.get("plants") or []))
    if field.startswith("plant_"):
        return float(collections.Counter(row.get("plants") or []).get(field[6:], 0))
    if field.startswith("seed_"):
        return float((row.get("seeds") or {}).get(field[5:], 0) or 0)
    if field.startswith("sell_"):
        return float((row.get("sells") or {}).get(field[5:], 0) or 0)
    return float(row.get(field, 0) or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--history", type=int, default=3)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--days", nargs="*", type=int,
                    default=[8, 12, 14, 16, 18, 20, 22, 25])
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import numpy as np
    from sklearn.ensemble import RandomForestRegressor

    rows = json.loads(pathlib.Path(args.rows).read_text())
    targets = json.loads(pathlib.Path(args.targets).read_text())
    by_key = {(t["game"], t["seat"], t["day"]): t["target"] for t in targets}

    by_game = collections.defaultdict(dict)
    for r in rows:
        by_game[(r["game"], r["seat"])][r["day"]] = r

    games = sorted(by_game)
    rng = np.random.default_rng(args.seed)
    rng.shuffle(games)
    test = set(map(tuple, games[:max(1, int(len(games) * args.holdout))]))

    def sample(day):
        X, Y, keys = [], [], []
        for g, days in by_game.items():
            r = days.get(day)
            if r is None:
                continue
            x = dict(r["x"])
            for back in range(1, args.history + 1):
                prev = by_key.get((g[0], g[1], day - back)) if day - back >= 0 else None
                x.update(row_features(prev, prefix="d%d_" % back))
            today = by_key.get((g[0], g[1], day))
            if today is None:
                continue
            X.append(x)
            Y.append([field_value(today, f) for f in FIELDS])
            keys.append(g)
        return X, np.array(Y, dtype=float), keys

    print("history = %d previous day(s); R^2 on held-out games, vs predicting the train mean")
    print("negative R^2 means the features are worse than a constant\n")
    header = "%4s" % "day"
    for f in ("n_plants", "plant_WHEAT", "plant_MELON", "seed_WHEAT",
              "sell_WHEAT", "sell_MILK", "hires", "land"):
        header += " %11s" % f[:11]
    print(header)

    want = [FIELDS.index(f) for f in ("n_plants", "plant_WHEAT", "plant_MELON", "seed_WHEAT",
                                      "sell_WHEAT", "sell_MILK", "hires", "land")]

    for day in args.days:
        X, Y, keys = sample(day)
        if len(X) < 30:
            continue
        names = sorted({k for x in X for k in x})
        idx = {n: i for i, n in enumerate(names)}
        M = np.zeros((len(X), len(names)))
        for i, x in enumerate(X):
            for k, v in x.items():
                M[i, idx[k]] = v
        tr = [i for i, g in enumerate(keys) if g not in test]
        te = [i for i, g in enumerate(keys) if g in test]
        if len(tr) < 20 or len(te) < 5:
            continue

        line = "%4d" % day
        for j in want:
            ytr, yte = Y[tr, j], Y[te, j]
            if float(np.std(yte)) < 1e-9:
                line += " %11s" % "const"
                continue
            model = RandomForestRegressor(n_estimators=120, max_depth=8,
                                          random_state=args.seed, n_jobs=-1)
            model.fit(M[tr], ytr)
            pred = model.predict(M[te])
            ss_res = float(((yte - pred) ** 2).sum())
            ss_tot = float(((yte - ytr.mean()) ** 2).sum())
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
            line += " %11.2f" % r2
        print(line)

    print("\nA field can be highly predictable while the ROW it belongs to is unique --")
    print("which is why exact row-id accuracy went to zero after d17 and this need not.")


if __name__ == "__main__":
    main()
