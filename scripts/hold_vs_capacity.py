"""Does the hold time track the BOOK, and does he get goods in earlier?

Two questions in one pass, because they share the same arrival/departure bookkeeping:

  1. per product, median turns held  vs  that world's town capacity for it
     (capacity from `_town_consume`: shops every 4 steps, 2x for single-product shops; centre every
      24 steps, never FERTILIZER)
  2. when do the goods ARRIVE -- median arrival day per product, per seat

If holding tracks thinness, the rule is "a thin book cannot take a batch, so meter it; a deep book
can, so clear it on arrival". If arrivals are also earlier, he is selling into a book that has not
yet been filled by anyone -- the two compound.

    python -u scripts/hold_vs_capacity.py 107642213 107646523 107041112 107674019
"""
import collections, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def capacity(rep):
    cap = collections.Counter()
    for t, step in enumerate(rep.get("steps") or []):
        shops = (((step[0] or {}).get("observation") or {}).get("town") or {}).get("unlocked_shops") or []
        if t % 4 == 0:
            for name in shops:
                pr = K.SHOPS.get(name) or []
                m = 2 if len(pr) == 1 else 1
                for it in pr:
                    cap[it] += m
        if t % 24 == 0:
            for it in K.TOWN_CENTER_PRODUCTS:
                cap[it] += 1
    return cap


def main():
    pairs = []
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams, cap = rep["info"]["TeamNames"], capacity(rep)
        print(f"\n=== {ep} ===")
        print(f"{'team':18}{'product':11}{'capacity':>9}{'held turns':>12}{'arrives day':>13}"
              f"{'units in':>10}")
        for seat, team in enumerate(teams):
            levels = collections.defaultdict(list)
            for step in rep["steps"]:
                shed = (((step[seat] if seat < len(step) else None) or {})
                        .get("observation") or {}).get("private", {}).get("shed") or {}
                for p in PRODUCTS:
                    levels[p].append(int(shed.get(p, 0) or 0))
            for p in PRODUCTS:
                q, waits, arrivals, series = collections.deque(), [], [], levels[p]
                for t in range(1, len(series)):
                    d = series[t] - series[t - 1]
                    if d > 0:
                        q.extend([t] * d)
                        arrivals += [t] * d
                    elif d < 0:
                        for _ in range(-d):
                            if q:
                                waits.append(t - q.popleft())
                if not waits:
                    continue
                w = statistics.median(waits)
                day = statistics.median(arrivals) // 24
                print(f"{team[:18]:18}{p:11}{cap[p]:>9,}{w:>12.0f}{day:>13.0f}{len(arrivals):>10,}")
                pairs.append((cap[p], w, team))
    # does hold time fall as capacity rises?
    print("\nhold time by capacity band, all seats pooled:")
    bands = [(0, 0), (1, 50), (51, 200), (201, 400), (401, 10 ** 9)]
    for lo, hi in bands:
        v = [w for c, w, _t in pairs if lo <= c <= hi]
        if v:
            print(f"   capacity {lo:>4}-{hi if hi < 10**9 else 'inf':>5}: "
                  f"n={len(v):>3}  median hold {statistics.median(v):>5.1f} turns")


if __name__ == "__main__":
    main()
