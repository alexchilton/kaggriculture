"""Answer economics question 5: does town drain exceed player supply for premium goods?

The question decides whether the strategy is "wheat volume" or "premium timing".

Three things are measured here, all against the parity-tested market model in
`kagg.economics.market`:

1. Season town drain per product, which is the demand side and is fixed.
2. What a realistic tile commitment can actually supply, using measured per-tile yields.
3. What that supply fetches under a sale policy that respects the 100-item shed cap.

Run: python scripts/answer_q5.py
"""

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.economics.market import (
    BASE,
    DAYS,
    I0,
    PRODUCTS,
    absorption,
    drain_per_day,
    inventory_path,
    observe_unlocks,
    price,
)
from kagg.economics.production import (
    ANIMAL_YIELD_PER_SEASON,
    TILE_YIELD_PER_SEASON,
    first_harvest_day,
    probe_crop,
    seed_cost_per_tile_season,
)

TURNS_PER_DAY = 24
LAST_STEP = 718  # the final step the interpreter processes (episodeSteps - 2)
SHED_CAP = 100
SEEDS = [11, 23, 42]
QUADRANT = 25


def shop_count(item):
    return sum(1 for products in kg.SHOPS.values() if item in products)


def drain_rate_schedule(item, unlocks, start_day):
    """Sell at exactly the town drain rate, which holds price near base.

    Quantity is whatever the drain absorbs, so this is the *sustainable ceiling* rather
    than a policy for a fixed harvest.
    """
    per_day = drain_per_day(unlocks)[item]
    # The clamp matters: day 29's slot is step 719, which `inventory_path` never reaches, so
    # without it the final day's sale is silently dropped from the ceiling.
    return {
        min(day * TURNS_PER_DAY + TURNS_PER_DAY - 1, LAST_STEP): per_day[day]
        for day in range(start_day, DAYS)
        if per_day[day]
    }


def drip_schedule(qty, start_day, last_day=29):
    """Spread `qty` evenly over the selling window, one instalment per day.

    Used to compare timing at *equal quantity* against :func:`late_schedule`; comparing a
    drip that moves the whole season's drain against a dump of one quadrant's harvest
    measures quantity, not timing.
    """
    days = list(range(start_day, last_day + 1))
    if not days:
        return {}
    per, extra = divmod(qty, len(days))
    sales = {}
    for i, day in enumerate(days):
        take = per + (1 if i >= len(days) - extra else 0)
        if take:
            step = min(day * TURNS_PER_DAY + TURNS_PER_DAY - 1, LAST_STEP)
            sales[step] = sales.get(step, 0) + take
    return sales


_PRODUCTION_CACHE = {}


def production_schedule(crop, tiles):
    """When a `tiles`-tile block of `crop` actually delivers, as {day: units}.

    Taken from the live-env probe rather than assumed, because arrival timing is what makes a
    hold-and-sell-late plan legal or illegal.
    """
    if crop not in _PRODUCTION_CACHE:
        _PRODUCTION_CACHE[crop] = probe_crop(crop).harvests
    return {day: units * tiles for day, units in _PRODUCTION_CACHE[crop]}


def max_deferred_schedule(production, shed_cap=SHED_CAP, last_day=29):
    """Sell as late as physically possible, given harvest arrival and overnight storage.

    Only `shed_cap` items survive the night (`_drop_inventories_to_shed` destroys the rest),
    so on any day where stock would exceed the cap the excess **must** be sold that day.
    Everything still held on `last_day` is sold then.

    This replaces an earlier "hold it all, dump at the end" schedule that quietly assumed
    unlimited storage and so overstated the gain from selling late.
    """
    sales = {}
    stock = 0
    forced_total = 0
    for day in range(last_day + 1):
        stock += production.get(day, 0)
        forced = stock if day == last_day else max(0, stock - shed_cap)
        if forced:
            step = min(day * TURNS_PER_DAY + TURNS_PER_DAY - 1, LAST_STEP)
            sales[step] = sales.get(step, 0) + forced
            stock -= forced
            if day < last_day:
                forced_total += forced
    return sales, forced_total


def revenue(item, unlocks, sales):
    _, rev = inventory_path(item, unlocks, sales=sales)
    return rev


def main():
    unlocks = observe_unlocks(SEEDS[0])
    print(f"Unlock schedule (seed {SEEDS[0]}, pass vs pass): {unlocks}\n")

    print("=" * 100)
    print("A. DEMAND SIDE -- town drain per season (fixed; no player can change it)")
    print("=" * 100)
    print(f"{'product':12s} {'shops':>5s} {'drain':>7s} {'price@0 sales':>14s} {'base':>6s} "
          f"{'x base':>7s} {'absorb@base':>12s} {'absorb@50%base':>15s}")
    drains = {}
    for item in PRODUCTS:
        path, _ = inventory_path(item, unlocks)
        drain = I0[item] - path[-1]
        drains[item] = drain
        end = price(item, path[-1])
        print(f"{item:12s} {shop_count(item):5d} {drain:7d} {end:14d} {BASE[item]:6d} "
              f"{end / BASE[item]:6.2f}x {absorption(item, I0[item], 1.0):12d} "
              f"{absorption(item, I0[item], 0.5):15d}")

    print()
    print("=" * 100)
    print("B. SUPPLY SIDE -- what one quadrant (25 tiles) can produce, vs the drain")
    print("=" * 100)
    print(f"{'crop':12s} {'units/tile':>11s} {'25 tiles':>9s} {'drain':>7s} "
          f"{'supply/drain':>13s} {'tiles to saturate':>18s} {'seed $ to saturate':>19s}")
    for item, per_tile in TILE_YIELD_PER_SEASON.items():
        supply = per_tile * QUADRANT
        drain = drains[item]
        tiles_needed = drain / per_tile
        seed = tiles_needed * seed_cost_per_tile_season(item)
        print(f"{item:12s} {per_tile:11d} {supply:9d} {drain:7d} {supply / drain:12.2f}x "
              f"{tiles_needed:18.1f} {seed:19.0f}")
    for item, per_tile in ANIMAL_YIELD_PER_SEASON.items():
        product = next(a["product"] for a in kg.ANIMALS.values() if a["product"] == item)
        supply = per_tile * QUADRANT
        drain = drains[product]
        print(f"{item:12s} {per_tile:11d} {supply:9d} {drain:7d} {supply / drain:12.2f}x "
              f"{drain / per_tile:18.1f} {'(animal cost)':>19s}")

    print()
    print("=" * 100)
    print("C. THE DECISION -- one quadrant, same quantity, drip vs deferred-as-far-as-storage-allows")
    print("=" * 100)
    print(f"{'crop':12s} {'qty':>6s} {'drip rev':>10s} {'$/unit':>8s} | "
          f"{'deferred':>10s} {'$/unit':>8s} {'gain':>7s} | {'forced early':>13s} {'held to end':>12s}")
    for item, per_tile in TILE_YIELD_PER_SEASON.items():
        qty = per_tile * QUADRANT
        start = first_harvest_day(item)
        production = production_schedule(item, QUADRANT)
        drip = revenue(item, unlocks, drip_schedule(qty, start))
        deferred_sales, forced = max_deferred_schedule(production)
        deferred = revenue(item, unlocks, deferred_sales)
        held = sum(deferred_sales.values()) - forced
        print(f"{item:12s} {qty:6d} {drip:10.0f} {drip / max(qty, 1):8.1f} | "
              f"{deferred:10.0f} {deferred / max(qty, 1):8.1f} {deferred / max(drip, 1):6.2f}x | "
              f"{forced:13d} {held:12d}")
    print()
    print("'forced early' is product that had to be sold before the end because it would not")
    print("survive the night. Storage is 100 items, so most of a season cannot be held back.")

    print()
    print("=" * 100)
    print("D. CAPITAL / TIMING REALITY CHECK")
    print("=" * 100)
    for item in TILE_YIELD_PER_SEASON:
        seed = kg.CROPS[item]["seed"]
        print(f"{item:12s} seed ${seed:3d}/tile/cycle  first harvest day "
              f"{first_harvest_day(item):2d}  25 tiles first cycle = ${seed * QUADRANT:5d} "
              f"({'AFFORDABLE' if seed * QUADRANT <= 3000 else 'EXCEEDS $3000 START'})")

    print()
    print("Drain stability across seeds (unlock order differs, totals barely do):")
    for seed in SEEDS:
        u = observe_unlocks(seed)
        row = {i: I0[i] - inventory_path(i, u)[0][-1]
               for i in ("WHEAT", "TOMATO", "STRAWBERRY", "MELON", "MILK")}
        print(f"  seed {seed}: {row}")


if __name__ == "__main__":
    main()
