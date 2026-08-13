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
4. **Where did the money go?** Per-day bank delta in the closing week, against what actually
   changed hands. Buying an input to make an output worth less is the fastest way to end poor.
5. **Weeds**, split by origin -- a tile that went CROP -> WEED is a missed watering, EMPTY -> WEED is
   a spawn. They are different problems and only one of them is bad luck.

## Every column here is a FILL, a board COUNT, or is labelled `offered`

This file is the reason `kagg/analysis/replay_fills.py` exists. It used to print a column headed
`crops planted (offers)` -- two contradictory claims in one label -- whose values were BUY_SEED
order quantities summed over turns. The agent re-posts a standing order on every turn until it
fills, so against the tiles that actually changed on the same four recordings:

    92564858   real WHEAT 138 STRAWBERRY 34 MELON 18   printed MELON 251, WHEAT 148, STRAW 92
    92566708   real WHEAT 139 STRAWBERRY 36 MELON 19   printed STRAW 460, MELON 386, WHEAT 378

Those numbers were quoted into an analysis before anyone noticed. Nothing printed here may be an
order count unless its heading says `offered`, and an `offered` figure never sits in the same column
as a fill.

    python -u scripts/why_we_lost.py ~/Downloads/91779414.json
    python -u scripts/why_we_lost.py data/seed_scripts/ours_weeds/*.json --me "alex chilton"
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from reference.kaggriculture import MARKET_PARAMS, PRICE_FLOOR, market_price

from kagg.analysis.replay_fills import (animals_alive, offered, real_plants,
                                        season_drain, seat_of, shop_instances,
                                        trade_fills, weeds_by_origin)

CROPS = ("WHEAT", "STRAWBERRY", "MELON", "CARROT", "TOMATO")
PRODUCTS = ("MILK", "WOOL", "EGG", "STRAWBERRY", "MELON", "WHEAT", "CARROT", "TOMATO",
            "FERTILIZER")


def analyse(path, me="alex chilton"):
    replay = json.loads(pathlib.Path(path).read_text())
    cfg = replay.get("configuration") or {}
    names = replay["info"]["TeamNames"]
    rewards = replay.get("rewards") or [0, 0]
    steps = replay["steps"]
    us = seat_of(replay, me)
    them = 1 - us
    won = rewards[us] > rewards[them]

    print("=" * 96)
    print(f"{pathlib.Path(path).name}   {'WIN' if won else 'LOSS'}   "
          f"us ${rewards[us]:,.0f}  vs  {names[them]} ${rewards[them]:,.0f}")
    print(f"  weedSpawnChance={cfg.get('weedSpawnChance')}  "
          f"townCenterSellInterval={cfg.get('townCenterSellInterval')}  seat {us}")

    # 1. what the town wanted
    dem = season_drain(replay)
    print(f"\n  SHOPS  {sorted(shop_instances(replay).items())}")
    print("  demand DRAINED over the season, units (exact -- `_town_consume` is arithmetic):")
    for product, units in dem.most_common():
        print(f"     {product:<11} {units:>6,}")

    # 2. what we made -- board counts, never orders
    fills = trade_fills(replay)
    print("\n  PLANTED, tiles that BECAME a crop (a COUNT of the board, not an order):")
    print(f"  {'':<6}" + "".join(f"{c.lower()[:10]:>12}" for c in CROPS))
    plants = {}
    for seat, lab in ((us, "US"), (them, "THEM")):
        plants[seat] = real_plants(replay, seat)
        print(f"  {lab:<6}" + "".join(f"{plants[seat][c]:>12,}" for c in CROPS))
    print("  BUY_SEED units OFFERED (what was asked for, re-posted every turn until it filled --")
    print("  NOT a plant count; on these games it runs up to 20x the tiles that changed):")
    for seat, lab in ((us, "US"), (them, "THEM")):
        asked = offered(replay, seat).get("BUY_SEED") or collections.Counter()
        print(f"  {lab:<6}" + "".join(f"{asked[c]:>12,}" for c in CROPS))

    print("\n  HERD standing at the close, head (a COUNT of the board):")
    for seat, lab in ((us, "US"), (them, "THEM")):
        print(f"  {lab:<6} {dict(animals_alive(replay, seat))}")

    # 3. what changed hands, and what it fetched
    print("\n  UNITS THAT CHANGED HANDS -- fills recovered from the shed and the market ledger.")
    print("  `shared` moved for certain but both sides traded it that turn; `unres` was hidden by")
    print("  the $1 floor, where a sale does not add to supply. Neither is folded into a seat.")
    print(f"  shed readable on {fills.coverage(us):.0%} of our turns, "
          f"{fills.coverage(them):.0%} of theirs")
    print(f"\n  {'product':<12}{'our sold':>10}{'our bought':>12} | {'their sold':>11}"
          f"{'their bought':>14} | {'shared':>8}{'unres':>7}{'drained':>9}")
    for product in PRODUCTS:
        row = (fills.sold[us][product], fills.bought[us][product],
               fills.sold[them][product], fills.bought[them][product],
               fills.shared_sold[product], fills.unresolved_sold[product])
        if not any(row) and not dem.get(product):
            continue
        print(f"  {product:<12}{row[0]:>10,}{row[1]:>12,} | {row[2]:>11,}{row[3]:>14,} | "
              f"{row[4]:>8,}{row[5]:>7,}{dem.get(product, 0):>9,}")

    market = (steps[-1][0] or {}).get("observation", {}).get("market") or {}
    inventory = market.get("inventory") or {}
    print("\n  CLOSING PRICES (a product at the floor is one we flooded):")
    for product in PRODUCTS:
        if product not in inventory:
            continue
        price = market_price(product, inventory[product], market.get("params"))
        base = MARKET_PARAMS[product]["base"]
        note = "  <-- FLOOR" if price <= PRICE_FLOOR + 1e-6 else (
            "  <-- above base" if price > base else "")
        print(f"     {product:<11} ${price:>7.2f}  of base ${base:<5} "
              f"drained {dem.get(product, 0):>5,}{note}")

    # 4. where the money went -- fills per day, not orders per day
    turns_per_day = int(cfg.get("turnsPerDay") or 24)
    last_day = (len(steps) - 1) // turns_per_day
    print(f"\n  CLOSING WEEK -- units that FILLED that day, not orders emitted\n")
    print(f"  {'':<6}{'our $':>10}{'delta':>9}{'sold u':>8}{'bought u':>10} | "
          f"{'their $':>10}{'delta':>9}{'sold u':>8}{'bought u':>10}")
    previous = [None, None]
    for day in range(max(0, last_day - 6), last_day + 1):
        t = min(day * turns_per_day + turns_per_day - 1, len(steps) - 1)
        farms = (steps[t][0] or {}).get("observation", {}).get("farms") or []
        if len(farms) < 2:
            break
        cells = []
        for seat in (us, them):
            money = farms[seat]["money"]
            delta = money - previous[seat] if previous[seat] is not None else 0
            previous[seat] = money
            cells.append((money, delta,
                          sum(fills.sold_by_day[seat][day].values()),
                          sum(fills.bought_by_day[seat][day].values())))
        print(f"  d{day:<5}{cells[0][0]:>10,.0f}{cells[0][1]:>+9,.0f}{cells[0][2]:>8,}"
              f"{cells[0][3]:>10,} | {cells[1][0]:>10,.0f}{cells[1][1]:>+9,.0f}"
              f"{cells[1][2]:>8,}{cells[1][3]:>10,}")

    # 5. weeds by origin
    print("\n  WEEDS by origin (CROP = a missed watering, EMPTY = a spawn) -- board transitions:")
    for seat, lab in ((us, "US"), (them, "THEM")):
        from_crop, from_empty, cleared = weeds_by_origin(replay, seat)
        final = sum(1 for row in (steps[-1][0]["observation"]["farms"][seat]["tiles"])
                    for tile in row if isinstance(tile, dict) and tile.get("kind") == "WEED")
        digs = sum(1 for t in range(len(steps))
                   for unit in ([((steps[t][seat] or {}).get("action") or {}).get("farmer")]
                                + list(((steps[t][seat] or {}).get("action") or {})
                                       .get("hands") or []))
                   if unit and unit[0] == "DIG")
        print(f"     {lab:<5} from CROP {from_crop:>3}  from EMPTY {from_empty:>3}  "
              f"cleared {cleared:>3}  DIG ops offered {digs:>3}  standing at close {final:>3}")


def summarise(path, me="alex chilton"):
    """One row per game. Built for a folder of ladder pulls, where the pattern is the point and the
    per-game detail is noise -- `analyse()` is still there for the one that looks odd.

    Every `_us` / `_them` figure is a FILL, not an order. The previous version summed SELL order
    quantities off the action stream, so a re-posted quota was counted once per turn it stood.
    """
    replay = json.loads(pathlib.Path(path).read_text())
    names = replay["info"]["TeamNames"]
    rewards = replay.get("rewards") or [0, 0]
    us = seat_of(replay, me)
    them = 1 - us
    dem = season_drain(replay)
    fills = trade_fills(replay)
    herd = animals_alive(replay, us)
    plants = real_plants(replay, us)
    return dict(
        game=pathlib.Path(path).stem, won=rewards[us] > rewards[them],
        ours=rewards[us], theirs=rewards[them], opp=names[them][:16],
        cow=herd.get("COW", 0), sheep=herd.get("SHEEP", 0), goose=herd.get("GOOSE", 0),
        wheat_planted=plants.get("WHEAT", 0),
        wheat_drain=dem.get("WHEAT", 0),
        wheat_sold_us=fills.sold[us].get("WHEAT", 0),
        wheat_sold_them=fills.sold[them].get("WHEAT", 0),
        wheat_shared=fills.shared_sold.get("WHEAT", 0),
        milk_drain=dem.get("MILK", 0), milk_sold_us=fills.sold[us].get("MILK", 0),
        fert_sold_us=fills.sold[us].get("FERTILIZER", 0),
        fert_sold_them=fills.sold[them].get("FERTILIZER", 0),
        carrot_drain=dem.get("CARROT", 0), tomato_drain=dem.get("TOMATO", 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("replays", nargs="+")
    ap.add_argument("--me", default="alex chilton")
    ap.add_argument("--summary", action="store_true", help="one row per game")
    args = ap.parse_args()
    if args.summary:
        rows = []
        for replay in args.replays:
            try:
                rows.append(summarise(replay, args.me))
            except Exception as exc:                                    # noqa: BLE001
                print(f"{replay}: FAILED {type(exc).__name__}: {exc}")
        if not rows:
            return
        rows.sort(key=lambda r: r["ours"] - r["theirs"])
        print("  every unit column below is a FILL (units that changed hands) or a board COUNT.")
        print("  `shared` is volume both sides traded on the same turn, left unattributed.\n")
        print(f"{'game':>9} {'res':>4} {'ours':>9} {'theirs':>9} {'opponent':<16} "
              f"{'cow':>4}{'shp':>4}{'gse':>4}{'wheatPlanted':>13} | {'WHEATdrain':>10} "
              f"{'soldUs':>7} {'soldThem':>9} {'shared':>7} | {'MILKdrain':>9} {'soldUs':>7} | "
              f"{'FERTsoldUs':>11} {'them':>5} | {'CARdrain':>8} {'TOMdrain':>8}")
        for r in rows:
            print(f"{r['game']:>9} {'WIN' if r['won'] else 'LOSS':>4} {r['ours']:>9,.0f} "
                  f"{r['theirs']:>9,.0f} {r['opp']:<16} {r['cow']:>4}{r['sheep']:>4}"
                  f"{r['goose']:>4}{r['wheat_planted']:>13,} | "
                  f"{r['wheat_drain']:>10,} {r['wheat_sold_us']:>7,} {r['wheat_sold_them']:>9,} "
                  f"{r['wheat_shared']:>7,} | {r['milk_drain']:>9,} {r['milk_sold_us']:>7,} | "
                  f"{r['fert_sold_us']:>11,} {r['fert_sold_them']:>5,} | "
                  f"{r['carrot_drain']:>8,} {r['tomato_drain']:>8,}")
        wins = sum(1 for r in rows if r["won"])
        print(f"\n  {wins}W {len(rows)-wins}L of {len(rows)}   "
              f"median ours ${sorted(r['ours'] for r in rows)[len(rows)//2]:,.0f}  "
              f"theirs ${sorted(r['theirs'] for r in rows)[len(rows)//2]:,.0f}")
        return
    for replay in args.replays:
        try:
            analyse(replay, args.me)
        except Exception as exc:                                        # noqa: BLE001
            print(f"{replay}: FAILED {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
