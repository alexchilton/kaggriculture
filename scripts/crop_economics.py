"""What is a tile worth, given what the town wants? Pure arithmetic, no game.

Answers the question the ladder losses keep posing: we plant WHEAT, STRAWBERRY and MELON on every
seed, and the seed decides what the town will actually eat. This ranks every crop and every animal
by what it earns, for a given shop draw, so the planting mix can follow the draw instead of a tape.

## The model, and why each piece is what it is

**Demand is an appetite, not a price.** `_town_consume` removes units from the market every
`townShopSellInterval` (4) steps: one per product per shop instance, doubled when the shop sells only
one thing. The town centre removes one of every product except FERTILIZER every
`townCenterSellInterval` (24). Over 719 turns that is 179 shop ticks and 29 centre ticks. Selling
into an appetite keeps the price up; selling past it is what floors a book.

**Price is the reference's own curve.** `market_price(product, inventory)` is imported, not
reimplemented. Stock rises by one per unit sold and falls by the town's eating, so the price of the
Nth unit sold is `market_price(p, I0 + sold_so_far - eaten_so_far)`. Revenue is the sum over units,
which is why a product is worth less per unit the more of it you make.

**Yields are measured, not derived.** `kagg.economics.production` probed them against the real env:
a WHEAT tile gives 28 a season (42 fertilized), CARROT 29, MELON 12, TOMATO 8, STRAWBERRY 6. Do not
re-derive these from `max_yield` in the rules table -- that table is per production EVENT and reading
it as a season total is a documented day-one mistake.

**Costs.** Seed is `PLANTINGS_PER_SEASON x CROPS[crop]["seed"]` -- the number of times a tile is
re-sown in a season, also measured. An animal costs its purchase price plus one wheat a day for the
rest of the season, charged at the wheat price the town's own appetite implies.

## What it deliberately does not model

Turns, walking, watering, the opponent, and the fact that both farms sell into the same book. So
these are ceilings per tile, not predictions of a season. They are meant for ranking -- "given this
draw, is a carrot tile worth more than a melon tile" -- which is the decision the schedule currently
makes blind.

    python -u scripts/crop_economics.py                      # the draws from our ladder losses
    python -u scripts/crop_economics.py --shops PIZZA_SHOP,PIZZA_SHOP,BAKERY
    python -u scripts/crop_economics.py --random 200         # what holds across draws
"""

import argparse
import collections
import json
import pathlib
import random
import sys

sys.path.insert(0, ".")

from kagg.economics.production import (ANIMAL_YIELD_PER_SEASON, PLANTINGS_PER_SEASON,
                                       TILE_YIELD_FERTILIZED, TILE_YIELD_PER_SEASON)
from reference.kaggriculture import (ANIMALS, CROPS, MARKET_I0, SHOPS, TOWN_CENTER_PRODUCTS,
                                     market_price)

STEPS = 719
SHOP_TICKS = STEPS // 4
CENTER_TICKS = STEPS // 24
SEASON_DAYS = 30


def appetite(shops):
    """Units of each product the town eats over a season, for this shop draw."""
    out = collections.Counter()
    for name in shops:
        products = SHOPS.get(name, [])
        mult = 2 if len(products) == 1 else 1
        for p in products:
            out[p] += mult * SHOP_TICKS
    for p in TOWN_CENTER_PRODUCTS:
        out[p] += CENTER_TICKS
    return out


def revenue(product, units, eaten, share=1.0):
    """What `units` of `product` fetch when the town will eat `eaten` of them over the season.

    Both are spread evenly across the season, so the stock the Nth unit meets is
    `I0 + N*share - eaten*(N/units)`. `share` is how much of the book is ours: at 1.0 we are the only
    seller, which flatters us -- the opponent sells into the same book.
    """
    if units <= 0:
        return 0.0
    total = 0.0
    for n in range(units):
        eaten_by_now = eaten * (n / units)
        total += market_price(product, MARKET_I0 + n * share - eaten_by_now)
    return total


def rank(shops, fertilized=False, share=1.0):
    app = appetite(shops)
    wheat_price = revenue("WHEAT", 1, app.get("WHEAT", 0)) or 25.0
    rows = []
    yields = TILE_YIELD_FERTILIZED if fertilized else TILE_YIELD_PER_SEASON
    for crop, units in yields.items():
        seed = PLANTINGS_PER_SEASON[crop] * CROPS[crop]["seed"]
        gross = revenue(crop, units, app.get(crop, 0), share)
        rows.append(("tile", crop, units, app.get(crop, 0), gross, seed, gross - seed))
    for animal, spec in ANIMALS.items():
        p = spec["product"]
        units = ANIMAL_YIELD_PER_SEASON[p]
        feed = SEASON_DAYS * wheat_price
        gross = revenue(p, units, app.get(p, 0), share)
        rows.append(("pen", animal, units, app.get(p, 0), gross, spec["cost"] + feed,
                     gross - spec["cost"] - feed))
    rows.sort(key=lambda r: -r[6])
    return rows, app, wheat_price


def show(title, shops, fertilized=False, share=1.0):
    rows, app, wheat_price = rank(shops, fertilized, share)
    print(f"\n=== {title} ===")
    print(f"  shops {sorted(collections.Counter(shops).items())}")
    print(f"  wheat costs ${wheat_price:.0f} to buy at this appetite"
          f"{'   [fertilized yields]' if fertilized else ''}")
    print(f"  {'':<5} {'what':<11} {'units/season':>12} {'town eats':>10} {'gross':>9} "
          f"{'cost':>8} {'NET each':>9}")
    for kind, what, units, eats, gross, cost, net in rows:
        print(f"  {kind:<5} {what:<11} {units:>12} {eats:>10,} {gross:>9,.0f} "
              f"{cost:>8,.0f} {net:>9,.0f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shops", help="comma-separated shop names")
    ap.add_argument("--random", type=int, default=0, help="average over N random 8-shop draws")
    ap.add_argument("--fertilized", action="store_true")
    ap.add_argument("--share", type=float, default=1.0,
                    help="fraction of the book that is ours; 0.5 = an equal opponent")
    args = ap.parse_args()

    if args.shops:
        show("given", [s.strip() for s in args.shops.split(",")], args.fertilized, args.share)
        return

    if args.random:
        names = sorted(SHOPS)
        tally = collections.defaultdict(list)
        rng = random.Random(0)
        for _ in range(args.random):
            draw = [rng.choice(names) for _ in range(8)]
            rows, _app, _w = rank(draw, args.fertilized, args.share)
            for i, (_k, what, *_r, net) in enumerate(rows):
                tally[what].append((i, net))
        print(f"\n=== {args.random} random draws, "
              f"{'fertilized' if args.fertilized else 'unfertilized'}, share {args.share} ===")
        print(f"  {'what':<11} {'mean NET':>10} {'best rank':>10} {'worst':>7} {'times #1':>9}")
        for what, vals in sorted(tally.items(), key=lambda kv: -sum(v[1] for v in kv[1])/len(kv[1])):
            ranks = [v[0] for v in vals]
            nets = [v[1] for v in vals]
            print(f"  {what:<11} {sum(nets)/len(nets):>10,.0f} {min(ranks):>10} "
                  f"{max(ranks):>7} {ranks.count(0):>9}")
        return

    # Default: the draws from the ladder games we actually lost.
    folder = pathlib.Path("data/seed_scripts/ladder")
    seen = set()
    for p in sorted(folder.glob("*.json"))[:4]:
        d = json.loads(p.read_text())
        steps = d["steps"][1:]
        shops = tuple(((steps[-1][0] or {}).get("observation") or {}).get("town", {})
                      .get("unlocked_shops") or [])
        if not shops or shops in seen:
            continue
        seen.add(shops)
        show(p.stem, list(shops), args.fertilized, args.share)


if __name__ == "__main__":
    main()
