"""Read a downloaded ladder replay and say, in numbers, why the game went the way it did.

Built after four separate losses were diagnosed by hand and the same five questions were asked each
time. Answers them off the recording alone -- no simulation, no re-play, so nothing here can be an
artifact of our own harness.

The five:

1. **What did the town want?** The seed varies exactly one thing (`weedSpawnChance` aside): which
   shops unlock and when (`kaggriculture.py:878`). A shop is a DRAIN -- every `townShopSellInterval`
   steps each instance removes `1` unit of each of its products, or `2` if it sells only one
   (`_town_consume`). That drain is what holds a price up, so demand is measured in units-per-season
   absorbed, not in shop names.
2. **What did we make?** Herd by species and crop plantings, against what the town was draining.
3. **What did it fetch?** `market_price` at the close, against base. A product at `PRICE_FLOOR` is
   one we flooded.
4. **Where did the money go?** Per-day bank delta in the closing week, against buys still being
   offered. Buying an input to make an output worth less is the fastest way to end poor.
5. **Weeds**, split by origin -- a tile that went CROP -> WEED is a missed watering, EMPTY -> WEED is
   a spawn. They are different problems and only one of them is bad luck.

    python -u scripts/why_we_lost.py ~/Downloads/91779414.json
    python -u scripts/why_we_lost.py data/seed_scripts/ours_weeds/*.json --me "alex chilton"
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from reference.kaggriculture import (ANIMALS, MARKET_PARAMS, PRICE_FLOOR, SHOPS,
                                     market_price)

#: `_town_consume`: every `townShopSellInterval` steps, each shop instance removes one unit of each
#: product it sells -- doubled when it sells only one. Defaults from the env spec.
SHOP_SELL_INTERVAL = 4
CENTER_INTERVAL = 24


def shop_demand(unlocked, steps):
    """Units per product the shops drain over `steps` turns. The real measure of demand."""
    ticks = steps // SHOP_SELL_INTERVAL
    out = collections.Counter()
    for name in unlocked:
        products = SHOPS.get(name, [])
        mult = 2 if len(products) == 1 else 1
        for p in products:
            out[p] += mult * ticks
    return out


def analyse(path, me="alex chilton"):
    d = json.loads(pathlib.Path(path).read_text())
    cfg = d.get("configuration") or {}
    names = d["info"]["TeamNames"]
    rewards = d.get("rewards") or [0, 0]
    steps = d["steps"][1:]
    us = names.index(me) if me in names else 0
    them = 1 - us
    won = rewards[us] > rewards[them]

    print("=" * 78)
    print(f"{pathlib.Path(path).name}   {'WIN' if won else 'LOSS'}   "
          f"us ${rewards[us]:,.0f}  vs  {names[them]} ${rewards[them]:,.0f}")
    print(f"  weedSpawnChance={cfg.get('weedSpawnChance')}  "
          f"townCenterSellInterval={cfg.get('townCenterSellInterval')}  seat {us}")

    last = len(steps) - 1
    obs = (steps[last][0] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    town = obs.get("town") or {}
    unlocked = town.get("unlocked_shops") or []

    # 1. what the town wanted
    dem = shop_demand(unlocked, len(steps))
    print(f"\n  SHOPS  {sorted(collections.Counter(unlocked).items())}")
    print("  demand drained over the season, units:")
    for p, q in dem.most_common():
        print(f"     {p:<11} {q:>6,}")

    # 2. what we made
    print(f"\n  {'':<6} {'herd':<28} {'crops planted (offers)':<34}")
    for seat, label in ((us, "US"), (them, "THEM")):
        herd = collections.Counter()
        for r in farms[seat]["tiles"]:
            for c in r:
                if isinstance(c, dict) and c.get("animal"):
                    herd[c["animal"]] += 1
        seeds = collections.Counter()
        sold = collections.Counter()
        for t in range(len(steps)):
            a = ((steps[t][seat] or {}).get("action") or {})
            for m in (a.get("market") or []):
                if not m or len(m) < 3:
                    continue
                if m[0] == "BUY_SEED":
                    seeds[m[1]] += int(m[2])
                elif m[0] == "SELL":
                    sold[m[1]] += int(m[2])
        print(f"  {label:<6} {str(dict(herd)):<28} {str(dict(seeds.most_common(4))):<34}")
        print(f"  {'':<6} sells offered: {sold.most_common(6)}")

    # 3. what it fetched
    mk = obs.get("market") or {}
    inv = mk.get("inventory") or {}
    print("\n  CLOSING PRICES (a product at the floor is one we flooded):")
    for p in ("MILK", "WOOL", "EGG", "STRAWBERRY", "MELON", "WHEAT", "CARROT",
              "TOMATO", "FERTILIZER"):
        if p not in inv:
            continue
        price = market_price(p, inv[p], mk.get("params"))
        base = MARKET_PARAMS[p]["base"]
        note = "  <-- FLOOR" if price <= PRICE_FLOOR + 1e-6 else (
            "  <-- above base" if price > base else "")
        print(f"     {p:<11} ${price:>7.2f}  of base ${base:<5} "
              f"drained {dem.get(p, 0):>5,}{note}")

    # 4. where the money went
    print(f"\n  CLOSING WEEK  {'our$':>10} {'delta':>9} {'ourBuys':>8} | "
          f"{'their$':>10} {'delta':>9} {'theirBuys':>10}")
    prev = [None, None]
    for day in range(max(0, len(steps) // 24 - 6), len(steps) // 24):
        t = min(day * 24 + 23, last)
        f = ((steps[t][0] or {}).get("observation") or {}).get("farms") or []
        if len(f) < 2:
            break
        row = []
        for seat in (us, them):
            buys = 0
            for h in range(24):
                tt = day * 24 + h
                if tt > last:
                    break
                for m in (((steps[tt][seat] or {}).get("action") or {}).get("market") or []):
                    if m and m[0] in ("BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL") and len(m) > 2:
                        buys += int(m[2])
            money = f[seat]["money"]
            delta = money - prev[seat] if prev[seat] is not None else 0
            prev[seat] = money
            row.append((money, delta, buys))
        print(f"  d{day:<11} {row[0][0]:>10,.0f} {row[0][1]:>+9,.0f} {row[0][2]:>8} | "
              f"{row[1][0]:>10,.0f} {row[1][1]:>+9,.0f} {row[1][2]:>10}")

    # 5. weeds by origin
    print("\n  WEEDS by origin (CROP = a missed watering, EMPTY = a spawn):")
    for seat, label in ((us, "US"), (them, "THEM")):
        prevmap = None
        origin = collections.Counter()
        cleared = 0
        for t in range(len(steps)):
            f = ((steps[t][0] or {}).get("observation") or {}).get("farms") or []
            if len(f) <= seat:
                continue
            cur = {}
            for y, row in enumerate(f[seat]["tiles"]):
                for x, c in enumerate(row):
                    cur[(x, y)] = ("WEED" if isinstance(c, dict) and c.get("kind") == "WEED"
                                   else ("CROP" if isinstance(c, dict) and c.get("crop")
                                         else ("OTHER" if isinstance(c, dict) else "EMPTY")))
            if prevmap:
                for k, v in cur.items():
                    if v == "WEED" and prevmap.get(k) != "WEED":
                        origin[prevmap.get(k)] += 1
                    elif prevmap.get(k) == "WEED" and v != "WEED":
                        cleared += 1
            prevmap = cur
        final = sum(1 for r in farms[seat]["tiles"] for c in r
                    if isinstance(c, dict) and c.get("kind") == "WEED")
        digs = sum(1 for t in range(len(steps))
                   for x in ([((steps[t][seat] or {}).get("action") or {}).get("farmer")]
                             + list(((steps[t][seat] or {}).get("action") or {}).get("hands") or []))
                   if x and x[0] == "DIG")
        print(f"     {label:<5} from CROP {origin.get('CROP', 0):>3}  from EMPTY "
              f"{origin.get('EMPTY', 0):>3}  cleared {cleared:>3}  DIGs {digs:>3}  final {final:>3}")


def summarise(path, me="alex chilton"):
    """One row per game. Built for a folder of ladder pulls, where the pattern is the point and the
    per-game detail is noise -- `analyse()` is still there for the one that looks odd."""
    d = json.loads(pathlib.Path(path).read_text())
    names = d["info"]["TeamNames"]
    rewards = d.get("rewards") or [0, 0]
    steps = d["steps"][1:]
    us = names.index(me) if me in names else 0
    them = 1 - us
    obs = (steps[-1][0] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    dem = shop_demand((obs.get("town") or {}).get("unlocked_shops") or [], len(steps))
    sold = {}
    for seat in (us, them):
        c = collections.Counter()
        for t in range(len(steps)):
            for m in (((steps[t][seat] or {}).get("action") or {}).get("market") or []):
                if m and m[0] == "SELL" and len(m) > 2:
                    c[m[1]] += int(m[2])
        sold[seat] = c
    herd = collections.Counter()
    for r in farms[us]["tiles"]:
        for c in r:
            if isinstance(c, dict) and c.get("animal"):
                herd[c["animal"]] += 1
    return dict(
        game=pathlib.Path(path).stem, won=rewards[us] > rewards[them],
        ours=rewards[us], theirs=rewards[them], opp=names[them][:16],
        cow=herd.get("COW", 0), sheep=herd.get("SHEEP", 0), goose=herd.get("GOOSE", 0),
        wheat_drain=dem.get("WHEAT", 0), wheat_us=sold[us].get("WHEAT", 0),
        wheat_them=sold[them].get("WHEAT", 0),
        milk_drain=dem.get("MILK", 0), milk_us=sold[us].get("MILK", 0),
        fert_us=sold[us].get("FERTILIZER", 0), fert_them=sold[them].get("FERTILIZER", 0),
        carrot_drain=dem.get("CARROT", 0), tomato_drain=dem.get("TOMATO", 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("replays", nargs="+")
    ap.add_argument("--me", default="alex chilton")
    ap.add_argument("--summary", action="store_true", help="one row per game")
    args = ap.parse_args()
    if args.summary:
        rows = []
        for r in args.replays:
            try:
                rows.append(summarise(r, args.me))
            except Exception as exc:                                    # noqa: BLE001
                print(f"{r}: FAILED {type(exc).__name__}: {exc}")
        rows.sort(key=lambda r: r["ours"] - r["theirs"])
        print(f"{'game':>9} {'res':>4} {'ours':>9} {'theirs':>9} {'opponent':<16} "
              f"{'cow':>4}{'shp':>4}{'gse':>4} | {'WHEATdrain':>10} {'us':>5} {'them':>5} | "
              f"{'MILKdrain':>9} {'us':>5} | {'FERTus':>7} {'them':>5} | {'CARdrain':>8} {'TOMdrain':>8}")
        for r in rows:
            print(f"{r['game']:>9} {'WIN' if r['won'] else 'LOSS':>4} {r['ours']:>9,.0f} "
                  f"{r['theirs']:>9,.0f} {r['opp']:<16} {r['cow']:>4}{r['sheep']:>4}{r['goose']:>4} | "
                  f"{r['wheat_drain']:>10,} {r['wheat_us']:>5,} {r['wheat_them']:>5,} | "
                  f"{r['milk_drain']:>9,} {r['milk_us']:>5,} | {r['fert_us']:>7,} {r['fert_them']:>5,} | "
                  f"{r['carrot_drain']:>8,} {r['tomato_drain']:>8,}")
        w = sum(1 for r in rows if r["won"])
        print(f"\n  {w}W {len(rows)-w}L of {len(rows)}   "
              f"median ours ${sorted(r['ours'] for r in rows)[len(rows)//2]:,.0f}  "
              f"theirs ${sorted(r['theirs'] for r in rows)[len(rows)//2]:,.0f}")
        return
    for r in args.replays:
        try:
            analyse(r, args.me)
        except Exception as exc:                                        # noqa: BLE001
            print(f"{r}: FAILED {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
