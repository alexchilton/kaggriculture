"""Does yesterday's ROW help predict today's? Measured teacher-forced AND rolled out.

Alex, 2026-08-21: "is there anyway of matching the nth day with the previous day as an included
factor to the tree because the day to play is highly dependent on the previous days board".

The board is already in the features -- they are read at hour 0 of day N, which is exactly what day
N-1 left behind. What is NOT there is the previous day's chosen TARGET ROW. Two boards can look
identical and carry different pending intent: seed bought yesterday for planting today, a pen built
but not yet stocked, a sale quota part-filled.

**The trap, and why this reports two numbers.** Training on Kawashigi's TRUE previous row and then
playing with OUR OWN predicted previous row is exposure bias, and it is the same failure that sank
the per-turn BC student earlier in this project -- 0.888 agreement on the teacher's own states,
0/0/4 and $438 on its own trajectory. So:

    TEACHER-FORCED   yesterday's row is the true one. Optimistic. Says whether the signal EXISTS.
    ROLLED OUT       yesterday's row is whatever the chain itself predicted, from d0 forward.
                     This is what play looks like, and the gap between them is the compounding.

A chain that is strong forced and weak rolled out has learned a mapping it cannot feed itself.

    python -u scripts/fit_chained_classifier.py --rows data/day_rows_kawa_target.json \\
        --targets data/target_rows_kawa.json --depth 4
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "MILK", "WOOL", "EGG",
            "FERTILIZER")
ANIMALS = ("GOOSE", "COW", "SHEEP")


def row_features(row, prefix="prev_"):
    """Summarise a target row as NUMBERS. The raw id would be a 150-level categorical."""
    if not row:
        return {}
    f = {prefix + k: float(row.get(k, 0) or 0)
         for k in ("hires", "land", "builds", "feeds", "cares", "harvests",
                   "fertilises", "clears")}
    plants = collections.Counter(row.get("plants") or [])
    f[prefix + "n_plants"] = float(sum(plants.values()))
    for c in CROPS:
        f[prefix + "plant_" + c] = float(plants.get(c, 0))
        f[prefix + "seed_" + c] = float((row.get("seeds") or {}).get(c, 0) or 0)
    for p in PRODUCTS:
        f[prefix + "sell_" + p] = float((row.get("sells") or {}).get(p, 0) or 0)
    for a in ANIMALS:
        f[prefix + "bought_" + a] = float((row.get("animals_bought") or {}).get(a, 0) or 0)
    f[prefix + "n_places"] = float(len(row.get("places") or []))
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--targets", required=True)
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--holdout", type=float, default=0.3)
    ap.add_argument("--max-day", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    import numpy as np
    from sklearn.tree import DecisionTreeClassifier

    rows = json.loads(pathlib.Path(args.rows).read_text())
    targets = json.loads(pathlib.Path(args.targets).read_text())

    by_key = {(t["game"], t["seat"], t["day"]): t for t in targets}
    row_of_id = {}
    for t in targets:
        row_of_id.setdefault(t["target_id"], t["target"])

    games = sorted({(r["game"], r["seat"]) for r in rows})
    rng = np.random.default_rng(args.seed)
    rng.shuffle(games)
    test_games = set(map(tuple, games[:max(1, int(len(games) * args.holdout))]))

    by_game = collections.defaultdict(dict)
    for r in rows:
        by_game[(r["game"], r["seat"])][r["day"]] = r

    def build(day, use_prev, prev_source):
        """prev_source: None = true previous row; dict = {game: predicted id} for rollout."""
        X, y, keys = [], [], []
        for g, days in by_game.items():
            r = days.get(day)
            if r is None:
                continue
            x = dict(r["x"])
            if use_prev and day > 0:
                if prev_source is None:
                    prev = by_key.get((g[0], g[1], day - 1))
                    x.update(row_features(prev["target"] if prev else None))
                else:
                    x.update(row_features(row_of_id.get(prev_source.get(g))))
            X.append(x)
            y.append(r["block"])
            keys.append(g)
        return X, y, keys

    names = sorted({k for r in rows for k in r["x"]}
                   | set(row_features(next(iter(row_of_id.values()))).keys()))
    index = {n: i for i, n in enumerate(names)}

    def mat(X):
        m = np.zeros((len(X), len(names)))
        for i, x in enumerate(X):
            for k, v in x.items():
                if k in index:
                    m[i, index[k]] = v
        return m

    print("%d features (%d base + previous-row summary)\n" % (len(names), len(rows[0]["x"])))
    print("%4s %8s %9s %10s %11s %10s"
          % ("day", "classes", "baseline", "no prev", "prev FORCED", "prev ROLLED"))

    rolled = {}          # game -> predicted target_id for the previous day
    models = {}
    for day in range(args.max_day + 1):
        Xb, y, keys = build(day, False, None)
        if not y:
            continue
        tr = [i for i, g in enumerate(keys) if g not in test_games]
        te = [i for i, g in enumerate(keys) if g in test_games]
        if len(tr) < 12 or not te:
            continue
        M = mat(Xb)
        ytr = [y[i] for i in tr]
        yte = np.array([y[i] for i in te])
        majority = collections.Counter(ytr).most_common(1)[0][0]
        base = float((yte == majority).mean())

        plain = DecisionTreeClassifier(max_depth=args.depth, random_state=args.seed)
        plain.fit(M[tr], ytr)
        acc_plain = float((plain.predict(M[te]) == yte).mean())

        Xf, _yf, _k = build(day, True, None)
        Mf = mat(Xf)
        forced = DecisionTreeClassifier(max_depth=args.depth, random_state=args.seed)
        forced.fit(Mf[tr], ytr)
        acc_forced = float((forced.predict(Mf[te]) == yte).mean())
        models[day] = forced

        if day == 0:
            acc_rolled = acc_forced
            for i, g in enumerate(keys):
                rolled[g] = y[i] if g not in test_games else forced.predict(Mf[[i]])[0]
        else:
            Xr, _yr, _kr = build(day, True, rolled)
            Mr = mat(Xr)
            pred_all = forced.predict(Mr)
            acc_rolled = float((pred_all[te] == yte).mean())
            for i, g in enumerate(keys):
                rolled[g] = y[i] if g not in test_games else pred_all[i]

        print("%4d %8d %8.1f%% %9.1f%% %10.1f%% %9.1f%%"
              % (day, len(set(y)), 100 * base, 100 * acc_plain,
                 100 * acc_forced, 100 * acc_rolled))

    print("\nFORCED uses Kawashigi's true previous row -- optimistic, says the signal exists.")
    print("ROLLED feeds the chain its OWN prediction from d0 forward -- this is what play does.")
    print("A large FORCED-minus-ROLLED gap is compounding, the failure that sank the BC student.")


if __name__ == "__main__":
    main()
