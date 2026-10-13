"""targets(day, shops_open) -> the amounts SpaTaro would have on the board that day.

The planner does not need his actions. It needs a per-day TARGET STATE to steer toward, because
his flows are undeliverable from our bank -- he over-requests `BUY_LAND` in 162 of 179 seasons and
funds exactly two parcels in all 179, and his `hires` rows are sized against his money, not ours.
A state target survives arriving late: a flow row saying "buy 2 cows on d6" is simply lost if we
were broke, while "have 8 cows by d9" buys three on d7 and still lands.

Two backends behind one call, chosen by measurement, not by taste:

    matrix   per-(cluster, day, quantity) quartiles. Exact, interpretable, and it is the thing
             that generates the p25/p50/p75 tolerance band -- inside the band, do nothing.
    ridge    a linear model per (day, quantity) over the eight shop-open indicators. Sees the FULL
             shop set rather than the first shop alone, so it can answer for shop combinations the
             179 seasons never showed. Ridge and not a tree or a net because 179 seasons against
             nine features is a linear problem; anything with more capacity fits the sample.

`baseline` is the third arm and the one that decides whether any of this is real: the global median
per (day, quantity), with NO world input at all. A backend that cannot beat it is saying the world
does not determine the amounts.

Fitted on 179 seasons of submission 56114097 only.
"""
import argparse, json, statistics
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SEASON = 30

#: The eight shops, in a fixed order so a feature vector means the same thing every time.
SHOPS = ("BAKERY", "BRUNCH_SPOT", "FARMERS_MARKET", "ICE_CREAM_SHOP",
         "PET_CAFE", "PIZZA_SHOP", "SMOOTHIE_SHOP", "YARN_STORE")

#: Demand clusters, measured on the d9 board over the 179 (`docs/the_plan_2026-09-11.md`).
#: Shops in a cluster put the same animals and crops on the board; the cluster, not the shop name,
#: is what the amounts depend on.
CLUSTERS = {
    "milk_berry": ("SMOOTHIE_SHOP", "ICE_CREAM_SHOP"),
    "wheat":      ("PIZZA_SHOP", "BAKERY"),
    "berry":      ("BRUNCH_SPOT", "FARMERS_MARKET"),
    "wool":       ("YARN_STORE",),
    "carrot":     ("PET_CAFE",),
}
SHOP_CLUSTER = {s: c for c, ss in CLUSTERS.items() for s in ss}

#: What the planner steers. Animals and crops are counts ON the board; `planted` and `owned` are
#: tile counts; `money` is the bank at dawn.
QUANTITIES = ("COW", "SHEEP", "GOOSE", "WHEAT", "STRAWBERRY", "CARROT", "MELON", "TOMATO",
              "planted", "owned", "money")
ANIMAL_Q = ("COW", "SHEEP", "GOOSE")
CROP_Q = ("WHEAT", "STRAWBERRY", "CARROT", "MELON", "TOMATO")


def quantity(state_row, q):
    if q in ANIMAL_Q:
        return state_row["animals"].get(q, 0)
    if q in CROP_Q:
        return state_row["crops"].get(q, 0)
    return state_row.get(q, 0)


def features(shops_open):
    """[1, is_open(BAKERY), ..., is_open(YARN_STORE)] -- the world, as the planner can see it."""
    s = set(shops_open or ())
    return np.array([1.0] + [1.0 if x in s else 0.0 for x in SHOPS])


def first_cluster(unlocks, day):
    """The cluster of the FIRST shop open by `day`, or None before any shop opens."""
    for d, shop in sorted(unlocks):
        if d <= day:
            return SHOP_CLUSTER.get(shop)
    return None


def load(landed="data/spataro_landed_rows.json", state="data/spataro_state.json",
         flows="data/spataro_plan_rows.json"):
    """[(unlocks, {day: {q: value}})] -- one entry per season."""
    unlocks = {p["ep"]: p["unlocks"] for p in json.loads((ROOT / flows).read_text())}
    out = []
    for s in json.loads((ROOT / state).read_text()):
        u = unlocks.get(s["ep"])
        if not u:
            continue
        days = {int(d): {q: quantity(r, q) for q in QUANTITIES} for d, r in s["state"].items()}
        out.append({"ep": s["ep"], "bank": s["bank"], "unlocks": u, "days": days})
    return out


def shops_by_day(unlocks, day):
    return tuple(shop for d, shop in sorted(unlocks) if d <= day)


class Baseline:
    """The global median per (day, quantity). No world input. The arm the others must beat."""

    name = "baseline"

    def fit(self, seasons):
        self.table = {}
        for day in range(SEASON):
            for q in QUANTITIES:
                vals = [s["days"][day][q] for s in seasons if day in s["days"]]
                if vals:
                    self.table[(day, q)] = statistics.median(vals)
        return self

    def predict(self, day, shops_open):
        return {q: self.table.get((day, q), 0.0) for q in QUANTITIES}


class Matrix:
    """Per-(cluster, day, quantity) quartiles, keyed on the first shop's demand cluster."""

    name = "matrix"

    def fit(self, seasons):
        self.table, self.fallback = {}, Baseline().fit(seasons)
        buckets = defaultdict(list)
        for s in seasons:
            for day in s["days"]:
                c = first_cluster(s["unlocks"], day)
                if c:
                    buckets[(c, day)].append(s["days"][day])
        for (c, day), rows in buckets.items():
            for q in QUANTITIES:
                v = sorted(r[q] for r in rows)
                self.table[(c, day, q)] = (v[len(v) // 4], statistics.median(v),
                                           v[(3 * len(v)) // 4], len(v))
        return self

    def cluster_of(self, shops_open):
        for shop in (shops_open or ()):
            c = SHOP_CLUSTER.get(shop)
            if c:
                return c
        return None

    def predict(self, day, shops_open):
        c = self.cluster_of(shops_open)
        out = {}
        for q in QUANTITIES:
            cell = self.table.get((c, day, q)) if c else None
            out[q] = cell[1] if cell else self.fallback.predict(day, shops_open)[q]
        return out

    def band(self, day, shops_open, q):
        """(p25, p50, p75, n) -- the tolerance band. Inside it, the planner does nothing."""
        c = self.cluster_of(shops_open)
        return self.table.get((c, day, q)) if c else None


class Ridge:
    """One linear model per (day, quantity) over the eight shop-open indicators."""

    name = "ridge"

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, seasons):
        self.w, self.fallback = {}, Baseline().fit(seasons)
        for day in range(SEASON):
            rows = [s for s in seasons if day in s["days"]]
            if len(rows) < 12:
                continue
            X = np.stack([features(shops_by_day(s["unlocks"], day)) for s in rows])
            # The intercept is NOT penalised -- penalising it would shrink every prediction toward
            # zero on a quantity like `money`, which is thousands of dollars and would swamp the fit.
            pen = self.alpha * np.eye(X.shape[1])
            pen[0, 0] = 0.0
            A = X.T @ X + pen
            for q in QUANTITIES:
                y = np.array([s["days"][day][q] for s in rows], dtype=float)
                try:
                    self.w[(day, q)] = np.linalg.solve(A, X.T @ y)
                except np.linalg.LinAlgError:
                    pass
        return self

    def predict(self, day, shops_open):
        x = features(shops_open)
        out = {}
        for q in QUANTITIES:
            w = self.w.get((day, q))
            out[q] = float(x @ w) if w is not None else self.fallback.predict(day, shops_open)[q]
        return out


def evaluate(seasons, backends, folds=5, days=range(3, SEASON), seed=0):
    """Mean absolute error per quantity, on seasons the backend never saw."""
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(seasons))
    err = {b.name: defaultdict(list) for b in backends}
    for k in range(folds):
        test_idx = set(order[k::folds].tolist())
        train = [s for i, s in enumerate(seasons) if i not in test_idx]
        test = [s for i, s in enumerate(seasons) if i in test_idx]
        for b in backends:
            b.fit(train)
            for s in test:
                for day in days:
                    if day not in s["days"]:
                        continue
                    pred = b.predict(day, shops_by_day(s["unlocks"], day))
                    for q in QUANTITIES:
                        err[b.name][q].append(abs(pred[q] - s["days"][day][q]))
    return {n: {q: float(np.mean(v)) for q, v in d.items() if v} for n, d in err.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--alpha", type=float, default=1.0)
    ap.add_argument("--out", default="data/spataro_target_matrix.json")
    args = ap.parse_args()

    seasons = load()
    print(f"{len(seasons)} seasons of submission 56114097\n")

    backends = [Baseline(), Matrix(), Ridge(args.alpha)]
    res = evaluate(seasons, backends, folds=args.folds)
    base = res["baseline"]
    print(f"held-out mean absolute error, {args.folds}-fold over seasons, days 3..29")
    print(f"{'quantity':12} {'baseline':>10} {'matrix':>10} {'vs base':>9} "
          f"{'ridge':>10} {'vs base':>9}")
    for q in QUANTITIES:
        if q not in base:
            continue
        m, r = res["matrix"].get(q), res["ridge"].get(q)
        f = lambda v: f"{100 * (v - base[q]) / base[q]:>+8.1f}%" if base[q] else "       -"
        print(f"{q:12} {base[q]:>10,.1f} {m:>10,.1f} {f(m):>9} {r:>10,.1f} {f(r):>9}")

    # Refit on everything and write the matrix the planner will read.
    mat = Matrix().fit(seasons)
    table = defaultdict(lambda: defaultdict(dict))
    for (c, day, q), (p25, p50, p75, n) in mat.table.items():
        table[c][str(day)][q] = [p25, p50, p75, n]
    out = ROOT / args.out
    out.write_text(json.dumps(
        {"submission": 56114097, "seasons": len(seasons), "clusters": CLUSTERS,
         "quantities": list(QUANTITIES), "shops": list(SHOPS),
         "source": "scripts/spa_targets.py from data/spataro_state.json",
         "table": {c: dict(d) for c, d in table.items()}}, indent=1))
    print(f"\nwrote {out} ({out.stat().st_size:,} B)")

    print("\nthe matrix the planner reads, p50 by cluster:")
    print(f"{'cluster':12} {'day':>4} " + " ".join(f"{q[:5]:>6}" for q in
          ("COW", "SHEEP", "WHEAT", "STRAWBERRY", "CARROT", "MELON", "planted", "money")))
    for c in CLUSTERS:
        for day in (6, 9, 12, 20, 26):
            cells = [mat.table.get((c, day, q)) for q in
                     ("COW", "SHEEP", "WHEAT", "STRAWBERRY", "CARROT", "MELON", "planted", "money")]
            if not any(cells):
                continue
            print(f"{c:12} {day:>4} " + " ".join(
                f"{(x[1] if x else 0):>6,.0f}" for x in cells))


if __name__ == "__main__":
    main()
