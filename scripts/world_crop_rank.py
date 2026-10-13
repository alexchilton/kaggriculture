"""Crop value PER WORLD: the same tile is worth 3x more in one town than another.

Two facts already measured, combined:

  book capacity   `_town_consume` -- each unlocked shop takes 1 of each product it carries every 4
                  steps (2 if the shop carries only ONE product), and the centre takes 1 of
                  everything except FERTILIZER every 24. So capacity is a pure function of the shop
                  DRAW, which is the world. STRAWBERRY: 174 units in a town with no FARMERS_MARKET,
                  642 in one with it.
  tile yield      `max_yield` is a count of production EVENTS (reference/kaggriculture.py:795), so a
                  tile is worth `units x price(book) - seed` over its life.

Price is taken at the book level a full field of that crop would drive it to, not at base -- selling
past capacity is what collapses a price, and that is a per-world quantity.

    python -u scripts/world_crop_rank.py                # the nine gate worlds
    python -u scripts/world_crop_rank.py BAKERY PIZZA_SHOP
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

TURNS = 720


def capacity(shops):
    """Units of each product this town removes over a 30-day season."""
    cap = collections.Counter()
    for t in range(TURNS):
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


def tile(c, fert=False):
    d = K.CROPS[c]
    if d["ongoing"]:
        units = d["max_yield"]
        life = d["first_yield_day"] + d["interval"] * (d["max_yield"] - 1)
    else:
        window = d["max_yield_day"] - (d["max_yield_day"] + 1) // 2 + 1
        units = min(d["max_yield"], window * (2 if fert else 1))
        life = d["max_yield_day"] + 1
    return units, life


def price_at(prod, sold, cap):
    """Mean price for `sold` units into a book the town drains `cap` of over the season."""
    glut = max(0, sold - cap)
    inv = K.MARKET_I0 + glut
    return (K.market_price(prod, K.MARKET_I0) + K.market_price(prod, inv)) / 2


def main():
    worlds = {}
    if len(sys.argv) > 1:
        worlds["ARGV"] = sys.argv[1:]
    else:
        import scripts.breakdown as B
        for tape in sorted(k for k in B.TAPES if k.startswith("spa")):
            rep = json.loads((ROOT / B.TAPES[tape][0]).read_text())
            seen = []
            for step in rep["steps"]:
                for s in (((step[0] or {}).get("observation") or {}).get("town") or {}).get(
                        "unlocked_shops") or []:
                    if s not in seen:
                        seen.append(s)
            worlds[tape] = seen
    crops = list(K.CROPS)
    print(f"{'world':14}{'shops':44}" + "".join(f"{c[:6]:>8}" for c in crops))
    print(f"{'':14}{'':44}" + "".join(f"{'$/t/day':>8}" for _ in crops))
    for name, shops in worlds.items():
        cap = capacity(shops)
        row = f"{name:14}{','.join(s[:6] for s in shops)[:43]:44}"
        best, bestc = -1, ""
        for c in crops:
            units, life = tile(c)
            # a 20-tile block of this crop is what a real field commits
            sold = units * 20
            px = price_at(c, sold, cap[c])
            net = units * px - K.CROPS[c]["seed"]
            rate = net / life
            row += f"{rate:>8.0f}"
            if rate > best:
                best, bestc = rate, c
        print(row + f"   best: {bestc}")


if __name__ == "__main__":
    main()
