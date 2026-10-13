"""How much of each product the TOWN can absorb in a season, against what each agent actually sold.

`_town_consume` (reference/kaggriculture.py:728) is the only thing that removes stock from the book:

    every `townShopSellInterval` (4) steps   each unlocked shop instance takes 1 of each product it
                                             carries -- 2 if that shop carries only ONE product
    every `townCenterSellInterval` (24) steps  the centre takes 1 of every product EXCEPT FERTILIZER

So a product's seasonal capacity is fixed by the shop DRAW, which is the world. Sell inside it and
the price recovers between sales; sell past it and the book fills permanently and the price
collapses -- which is the same thing whatever hour it happens at.

FERTILIZER is in no shop and is excluded from the centre: its book never drains at all.

    python -u scripts/book_capacity.py 107642213 107646523 107399673
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def capacity(rep):
    """Units of each product the town removes over the recorded season, read off the real draw."""
    cap = collections.Counter()
    steps = rep.get("steps") or []
    for t, step in enumerate(steps):
        obs = ((step[0] or {}).get("observation") or {})
        shops = (obs.get("town") or {}).get("unlocked_shops") or []
        if t % 4 == 0:
            for name in shops:
                prods = K.SHOPS.get(name) or []
                mult = 2 if len(prods) == 1 else 1
                for item in prods:
                    cap[item] += mult
        if t % 24 == 0:
            for item in K.TOWN_CENTER_PRODUCTS:
                cap[item] += 1
    return cap


def main():
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        cap = capacity(rep)
        shops = collections.Counter()
        for step in rep["steps"]:
            for s in ((step[0] or {}).get("observation") or {}).get("town", {}).get("unlocked_shops") or []:
                shops[s] = 1
        # units OFFERED are not fills; use the shed-settling sells as a ceiling on what they pushed
        sold = [collections.Counter() for _ in teams]
        for step in rep["steps"][1:]:
            for seat in range(len(teams)):
                for o in ((step[seat] or {}).get("action") or {}).get("market") or []:
                    if o and o[0] == "SELL":
                        sold[seat][o[1]] += 1        # count TURNS, not units offered
        print(f"\n=== {ep}  shops: {sorted(shops)} ===")
        print(f"{'product':12}{'town takes':>11}{'per day':>9}   "
              + "".join(f"{t[:16]:>18}" for t in teams))
        print(f"{'':12}{'':11}{'':9}   " + "".join(f"{'sell-turns':>18}" for _ in teams))
        for p in sorted(set(cap) | {q for s in sold for q in s}):
            row = f"{p:12}{cap[p]:>11,}{cap[p]/30:>9.1f}   "
            for s in sold:
                row += f"{s[p]:>18,}"
            print(row)


if __name__ == "__main__":
    main()
