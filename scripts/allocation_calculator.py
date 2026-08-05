"""Compute the season's allocation in closed form, then check it against the leader's actual farm.

**The thesis being tested.** Once the game is properly defined this is a constrained optimisation, not
a search: the objective is nearly additive (chains interact only through the shared price curve, cash
timing, and tile/slot exclusivity), and the price curve is *concave* -- `price = base - amp *
shape(inventory - I0)` -- so marginal-value-per-resource ranking is near-optimal rather than a
heuristic. If that holds, the target mix can be **calculated** and the search only has to schedule it.

The falsifiable claim: this arithmetic should reproduce the new leader's measured allocation without
being told it. He plants **20 melon, 41 strawberry, 40 wheat tiles** and runs **14 pens** (8 cow,
6 sheep), banking $139,121 (`docs/new_leader_somewhere_after_2026-08-05.md`). If the numbers land near
that, the mix was never the hard part. If they do not, the gap names the constraint we have
mis-modelled, which is worth more than another search run.

Everything here is read from the measured tables rather than restated: `chains.DRAIN_UNITS` for the
town's whole-season appetite, `production.py` for per-tile yields, `market.BASE` for prices, and
`routines` for the day's turn budget. No fitted constants.
"""

import numpy as np

from kagg.economics import production as P
from kagg.search import chains as C
from kagg.search import routines as R
from kagg.sim import market as M

TURNS = R.TURNS_PER_DAY - 1          # turn 0 of each day is the market order
DAYS = R.SEASON_DAYS
BASE = {n: float(np.asarray(M.BASE)[i]) for i, n in enumerate(R.PRODUCTS)}

# What the leader actually did, for the comparison. Measured, not assumed.
LEADER = {"MELON": 20, "STRAWBERRY": 41, "WHEAT": 40, "pens": 14, "bank": 139_121}


def turns_per_tile(crop, water_every):
    """Turn cost of holding one tile for one day, amortised.

    A tile needs one WATER on the days it is visited, plus the walk between neighbours (~1 step in
    serpentine order), plus its share of PLANT and HARVEST across the season. Alternate-day visiting
    halves the water and walk, which is the whole reason a wide block fits.
    """
    info = R.CROP_TABLE[crop]
    cycles = 1 if info["ongoing"] else max(1, DAYS // max(info["max_day"], 1))
    per_visit = 1 + 1                       # WATER + one step of walk
    return per_visit / water_every + (2 * cycles) / DAYS


def crop_row(crop):
    """Marginal economics of one tile of `crop`, and how many tiles the town can absorb."""
    drain = C.DRAIN_UNITS[crop]
    base = BASE[crop]
    # Alternate-day watering only pays where the crop tolerates it: ongoing crops produce on a fixed
    # interval regardless of which days they are visited, one-shot crops have a harvest window that a
    # missed visit can forfeit. Measured: strawberry +52%, melon -28%.
    ongoing = R.CROP_TABLE[crop]["ongoing"]
    water_every = 2 if ongoing else 1
    yield_plain = P.TILE_YIELD_PER_SEASON[crop]
    yield_fert = P.TILE_YIELD_FERTILIZED[crop]
    # Fertilizer only if the herd supplies it: buying at ~$100 a unit lost money in every measurement.
    y = yield_fert if yield_fert > yield_plain else yield_plain
    tiles_to_fill = drain / max(y, 1e-9)
    tpt = turns_per_tile(crop, water_every)
    return dict(crop=crop, drain=drain, base=base, market=drain * base, yield_per_tile=y,
                water_every=water_every, tiles_to_fill=tiles_to_fill, turns_per_tile=tpt,
                tiles_per_unit=TURNS / tpt,
                # The ranking quantity: revenue per unit-day, i.e. per slot. This is what decides which
                # market to fill first when slots are the scarce resource.
                value_per_unit=drain * base / max(tiles_to_fill * tpt / TURNS, 1e-9))


def animal_row(name):
    """Marginal economics of one pen. Feed is a cost; fertilizer is a second revenue stream."""
    a = R.ANIMALS[name]
    product = a["product"]
    # Production events per season, capped by nothing (animals have no lifetime cap).
    events = max(0, (DAYS - a["first_yield_day"]) // max(a["interval"], 1))
    units = events * a["max_held"]
    revenue = units * BASE[product]
    # One fertilizer unit per animal per night, free to collect.
    fert_units = max(0, DAYS - a["first_yield_day"])
    fert_revenue = fert_units * BASE["FERTILIZER"]
    # Feed every other day, which the two-strike escape rule permits.
    feed_units = DAYS / 2
    feed_cost = feed_units * BASE["WHEAT"]
    # PICKUP+FEED on half the days, CARE/COLLECT/HARVEST daily, plus a step of walk.
    tpt = (2 / 2) + 3 + 1
    return dict(animal=name, cost=a["cost"], product=product, units=units, revenue=revenue,
                fert_units=fert_units, fert_revenue=fert_revenue, feed_cost=feed_cost,
                net=revenue + fert_revenue - feed_cost - a["cost"],
                turns_per_pen=tpt, pens_per_unit=TURNS / tpt)


print("=" * 100)
print("CROPS: what each market is worth, how many tiles fill it, how many tiles one unit can hold")
print("=" * 100)
rows = [crop_row(c) for c in R.CROPS]
print(f"{'crop':>11} {'drain':>6} {'base':>5} {'market $':>10} {'yield/tile':>11} "
      f"{'water':>6} {'tiles to fill':>14} {'tiles/unit':>11} {'slots to fill':>14}")
for r in sorted(rows, key=lambda r: -r["market"]):
    slots = r["tiles_to_fill"] / r["tiles_per_unit"]
    print(f"{r['crop']:>11} {r['drain']:>6} {r['base']:>5.0f} {r['market']:>10,.0f} "
          f"{r['yield_per_tile']:>11.0f} {'1/' + str(r['water_every']):>6} "
          f"{r['tiles_to_fill']:>14.1f} {r['tiles_per_unit']:>11.1f} {slots:>14.1f}")
total_market = sum(r["market"] for r in rows)
print(f"\ntotal crop market ${total_market:,.0f}")

print()
print("=" * 100)
print("ANIMALS: one pen over a season, feeding every other day and selling the fertilizer")
print("=" * 100)
arows = [animal_row(a) for a in R.ANIMAL_NAMES]
print(f"{'animal':>7} {'cost':>6} {'product':>9} {'units':>6} {'product $':>10} "
      f"{'fert $':>8} {'feed $':>8} {'NET $':>9} {'pens/unit':>10}")
for a in sorted(arows, key=lambda a: -a["net"]):
    print(f"{a['animal']:>7} {a['cost']:>6} {a['product']:>9} {a['units']:>6} {a['revenue']:>10,.0f} "
          f"{a['fert_revenue']:>8,.0f} {a['feed_cost']:>8,.0f} {a['net']:>9,.0f} "
          f"{a['pens_per_unit']:>10.1f}")

print()
print("=" * 100)
print("THE ALLOCATION: fill each market to its drain, best value per unit-day first")
print("=" * 100)
print("Constraints: 100 tiles (75 without buying SE, which the leader never buys), 4 shed cells,")
print(f"{TURNS} work turns per unit-day, and the opening bank of ${C.OPENING_BANK:,}.\n")

# Animal products have drains too, and the herd is limited by them as much as by turns.
best_animal = max(arows, key=lambda a: a["net"])
herd_by_drain = {}
for a in arows:
    d = C.DRAIN_UNITS.get(a["product"])
    if d:
        herd_by_drain[a["animal"]] = d / max(a["units"] / 1, 1e-9)

TILE_BUDGET = 75                     # NW + NE + SW: what the leader owns
plan, tiles_left = [], TILE_BUDGET
for r in sorted(rows, key=lambda r: -r["value_per_unit"]):
    take = min(r["tiles_to_fill"], tiles_left)
    if take < 1:
        continue
    plan.append((r["crop"], round(take), round(take / r["tiles_per_unit"], 1)))
    tiles_left -= take
print(f"{'crop':>11} {'tiles':>7} {'slots':>7}   (ranked by revenue per unit-day)")
for crop, t, s in plan:
    print(f"{crop:>11} {t:>7} {s:>7}")
print(f"{'unallocated':>11} {round(tiles_left):>7}")

print()
print("=" * 100)
print("AGAINST THE LEADER -- the falsifiable part")
print("=" * 100)
calc = {c: t for c, t, _ in plan}
print(f"{'crop':>11} {'calculated':>11} {'leader':>8} {'diff':>7}")
for crop in ("WHEAT", "STRAWBERRY", "MELON"):
    got, want = calc.get(crop, 0), LEADER[crop]
    print(f"{crop:>11} {got:>11} {want:>8} {got - want:>+7}")
print(f"\ncalculated herd cap by milk/wool drain: "
      f"{ {k: round(v, 1) for k, v in herd_by_drain.items()} }")
print(f"leader runs {LEADER['pens']} pens (8 cow, 6 sheep) and banks ${LEADER['bank']:,}")
print(f"\nsum of the markets we would fill: "
      f"${sum(C.DRAIN_UNITS[c] * BASE[c] for c in calc):,.0f} of ${total_market:,.0f} crop demand")
print("\nA close match means the mix was never the hard part and the search only has to schedule it.")
print("A miss names the constraint that is mis-modelled, which is worth more than another beam run.")
