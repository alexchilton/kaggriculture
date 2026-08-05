"""Schedule a fixed mix of chains against the farm's cash flow.

`scripts/allocation_calculator.py` computes **what** to own in closed form -- drain divided by
yield-per-season, ranked by revenue per unit-day -- and lands on the leader's farm: 8 cows against his
8, 6 sheep against his 6, 48 strawberry tiles against his 41.
`scripts/build_calculated_genome.py` then wrote that exact mix into a genome and scored **$13,479**
against the beam's $72,543.

The mix was right and the farm still died, which localises the difficulty precisely: **cash is a flow,
not a stock.** The calculated plan ordered four cows and three sheep on day 5 -- $3,100 against a $3,000
bank -- and was broke before anything had sold. The beam, searching freely, put its pens on days 8 and 9
and banked five times as much with the same animals.

So the mix is arithmetic and the *schedule* is the problem. This module solves the schedule.

**Why greedy-by-payback is the right shape.** This is resource-constrained project scheduling: each
chain has an opening cost, a payback delay and a revenue stream, and one shared renewable budget. With a
single budget constraint and no precedence other than affordability, scheduling in order of payback time
and starting each chain the first day it clears is the classic near-optimal rule -- and it is what the
leader's timeline looks like from the outside:

    wheat and melon on day 0-2   (wheat is the only crop returning cash by day 3)
    NE parcel day 7, SW day 10   (out of that revenue, never the opening bank)
    strawberry days 7-14         (onto the ground as it arrives)

We derive that rather than copy it.

**What this does not do.** It does not choose the mix, it does not re-order the board, and it does not
model the opponent's draw on the shared market. It turns a mix into days.
"""

import numpy as np

from kagg.search import chains as C
from kagg.search import routines as R

# Opening cost of a chain, before any revenue. Seeds are per tile per cycle but the first cycle is what
# has to clear the bank; land is charged separately because it is a farm-level order.
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}

# --------------------------------------------------------------------------------------------------
# Market conditions: the drain is a randomised schedule, not a season constant
# --------------------------------------------------------------------------------------------------
# Eight shops open on days 3, 6, 9 ... 24, and **which shop lands on which day is drawn per game**
# (`jax_sim.random_unlock_days`; seed 0 gives [18,21,3,9,6,15,12,24], seed 1 [6,9,15,21,12,3,18,24]).
# A product has no shop demand at all until one of its shops opens, so "fill the drain" is an upper
# bound that assumes early unlocks.
#
# How many shops serve a product is therefore a risk measure, and it explains the leader's whole
# allocation -- market size TIMES robustness, not size alone:
#
#     WHEAT      5 shops  drain 662  $16,550  robust        -> he plants 40 tiles
#     STRAWBERRY 4 shops  drain 572  $68,640  robust        -> 41 tiles
#     MILK       3 shops  drain 500  $80,000  robust        -> 8 cows
#     TOMATO     2 shops  drain 374  $22,440  exposed       -> 0
#     EGG        2 shops  drain 338  $16,900  exposed       -> 0 geese
#     CARROT     2 shops  drain 338  $11,830  exposed       -> 0
#     WOOL       1 shop   drain 284  $56,800  a gamble      -> only 6 sheep
#     MELON      0 shops  drain 140  $35,000  base demand   -> 20 tiles, and it saturates
#
# Wool is a $56,800 market and he under-commits, because YARN_STORE can open on day 24. Melon has no
# shop at all: its 140 units are fixed base town demand that never grows, making it the least scalable
# product in the game -- and the one our own searches built a monoculture on.
#
# **An open-loop tape cannot react to the draw**, which is also why selling daily is the right cadence
# rather than a naive one: you cannot wait for a demand event you cannot observe, so you offer
# continuously and let `_process_market` fill what the shed and the shops allow.
SHOP_PRODUCTS = {
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "BAKERY": ("EGG", "WHEAT"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "YARN_STORE": ("WOOL",),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "PET_CAFE": ("CARROT",),
}
UNLOCK_DAYS = (3, 6, 9, 12, 15, 18, 21, 24)


def shops_serving(product):
    return sum(1 for prods in SHOP_PRODUCTS.values() if product in prods)


def expected_first_demand_day(product):
    """When shop demand for `product` can first be expected, over the unlock draw.

    The eight unlock days are a permutation across the eight shops, so a product served by `k` shops
    has its first demand at the minimum of `k` draws without replacement from `UNLOCK_DAYS`. Computed
    exactly rather than approximated -- it is eight values and a small combinatorial sum.

    Melon is served by no shop and sells against base town demand from day 0, so it returns 0.
    """
    import itertools

    k = shops_serving(product)
    if k == 0:
        return 0
    firsts = [min(c) for c in itertools.combinations(UNLOCK_DAYS, k)]
    return sum(firsts) / len(firsts)


# The opponent sells into the same town inventory, so a drain is shared. `data/logs/market_ceiling.log`
# records the whole-market $302,380 as "1.0x if split evenly between two players" -- and the leader's
# $139,121 is close to that half, i.e. he captures nearly his entire share. Halving here keeps the
# scheduling estimates from assuming an empty market.
OPPONENT_SHARE = 0.5


def payback_days(kind, what):
    """Days from starting a chain until it first puts money in the bank.

    The ranking key, and it is **the later of two things**: when the chain can physically produce, and
    when a shop exists to buy the product. Wheat produces at day 3 and is served by five shops so its
    demand arrives early too; wool produces at day 7 and waits a mean 13.5 days for its only shop, which
    is why an early sheep is money asleep.

    Ignoring the second term is what made the first version of this schedule wrong: it ranked purely on
    production and would happily open the season with sheep.
    """
    if kind == "ranch":
        a = R.ANIMALS[what]
        # First yield day, plus a day for the product to reach the shed and the market to resolve.
        ready = a["first_yield_day"] + 1
        product = a["product"]
    else:
        info = R.CROP_TABLE[what]
        ready = info["first"] + 1
        product = what
    return max(ready, expected_first_demand_day(product))


def opening_cost(kind, what, n_tiles):
    """Cash needed on the chain's first day, excluding land."""
    if kind == "ranch":
        return R.ANIMALS[what]["cost"] * n_tiles
    # Seeds for the first planting, plus a day of wheat if this is feeding anything (charged by the
    # ranch chains, not here).
    return SEED_COST[what] * n_tiles


def daily_burn(kind, what, n_tiles):
    """Recurring cost per day once running: feed for animals, nothing structural for crops."""
    if kind == "ranch":
        # Feeding every other day, which the two-strike escape rule permits.
        return R.ANIMALS[what]["cost"] * 0 + 25 * n_tiles / 2      # wheat at base $25
    return 0.0


def revenue_rate(kind, what, n_tiles):
    """Rough revenue per day once the chain is producing, from the measured season yields.

    Deliberately crude: this is a *scheduling* estimate used to decide affordability order, and the
    simulator is the judge of the result. A precise model here would be a second implementation of the
    game and would drift from it.
    """
    from kagg.economics import production as P

    if kind == "ranch":
        a = R.ANIMALS[what]
        events = max(1, (R.SEASON_DAYS - a["first_yield_day"]) // max(a["interval"], 1))
        units = events * a["max_held"] * n_tiles
        base = {"MILK": 160, "WOOL": 200, "EGG": 50}[a["product"]]
        # Capped by the shared drain, then discounted for the price curve: selling into a drain walks
        # the price down from base toward the floor, so realising base on every unit is not available.
        units = min(units, C.DRAIN_UNITS[a["product"]] * OPPONENT_SHARE)
        return units * base * 0.5 / max(R.SEASON_DAYS - a["first_yield_day"], 1)
    y = max(P.TILE_YIELD_FERTILIZED[what], P.TILE_YIELD_PER_SEASON[what])
    base = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250}[what]
    units = min(y * n_tiles, C.DRAIN_UNITS[what] * OPPONENT_SHARE)
    return units * base * 0.5 / R.SEASON_DAYS


def schedule(mix, bank=None, horizon=None, reserve=300.0):
    """Assign a `start_day` and `land_day` to every chain in `mix`, respecting cash.

    `mix` is a list of `(kind, what, tiles)` where `tiles` is the tuple of tiles the chain occupies.
    Returns `[(kind, what, tiles, start_day, land_day), ...]` in the order they should be started, plus
    the simulated bank curve for inspection.

    The rule: sort by payback, then walk the days forward maintaining a bank estimate, starting each
    chain the first day its opening cost clears with `reserve` left over. Land is bought the same way --
    one parcel at a time, the first day it clears -- because `_do_buy_land` unlocks in fixed order and
    silently no-ops when short, so ordering three parcels early buys two and reports three.
    """
    bank = C.OPENING_BANK if bank is None else bank
    horizon = R.SEASON_DAYS if horizon is None else horizon

    # Payback order, with a stable tiebreak so the schedule is reproducible.
    order = sorted(range(len(mix)),
                   key=lambda i: (payback_days(mix[i][0], mix[i][1]), i))

    # How many parcels the whole mix needs, and which chains are waiting on each.
    need = {i: R.land_purchases_for(mix[i][2][0]) for i in range(len(mix))}
    parcels_needed = max(need.values(), default=0)

    placed = {}                       # chain index -> start day
    parcel_day = {}                   # parcel index -> day bought
    parcels_bought = 0
    running = []                      # (index, kind, what, n_tiles)
    curve = []

    pending = list(order)
    for day in range(horizon):
        # Yesterday's production and today's costs.
        for i, kind, what, n in running:
            bank += revenue_rate(kind, what, n) - daily_burn(kind, what, n)
        bank = max(bank, 0.0)

        # Buy the next parcel as soon as it clears, if anything is waiting on it.
        if parcels_bought < parcels_needed:
            price = R.LAND_PRICES[parcels_bought]
            wanted_by = [i for i in pending if need[i] > parcels_bought]
            if wanted_by and bank >= price + reserve and day not in parcel_day.values():
                bank -= price
                parcel_day[parcels_bought] = day
                parcels_bought += 1

        # Start every chain that can now afford its opening cost and has its ground.
        for i in list(pending):
            kind, what, tiles = mix[i]
            if need[i] > parcels_bought:
                continue                       # ground not owned yet
            cost = opening_cost(kind, what, len(tiles))
            if bank < cost + reserve:
                continue
            bank -= cost
            placed[i] = day
            pending.remove(i)
            running.append((i, kind, what, len(tiles)))
        curve.append(bank)

    out = []
    for i in range(len(mix)):
        kind, what, tiles = mix[i]
        if i not in placed:
            continue                           # never affordable inside the season; drop it
        # The chain's `land_day` is when *its* parcel was bought, so `decode()`'s consolidated schedule
        # emits one order per parcel on the day this scheduler chose.
        ld = parcel_day.get(need[i] - 1, 0) if need[i] else 0
        out.append((kind, what, tiles, placed[i], ld))
    out.sort(key=lambda r: r[3])
    return out, curve, parcel_day


def to_genome(scheduled, n_slots):
    """Write a scheduled mix into a genome `decode()` can read."""
    g = np.zeros((n_slots, len(C.GENES)), dtype=np.int64)
    for slot, (kind, what, tiles, start, land_day) in enumerate(scheduled[:n_slots]):
        if kind == "ranch":
            block_i = next((i for i, gr in enumerate(C.RANCH_GROUPS) if gr == tuple(tiles)), None)
            what_i = R.ANIMAL_NAMES.index(what)
        else:
            block_i = next((i for i, b in enumerate(C.BLOCKS) if b == tuple(tiles)), None)
            what_i = R.CROPS.index(what)
        if block_i is None:
            continue                           # not in the vocabulary; leave the slot off
        row = [C.KINDS.index(kind), what_i, block_i,
               C.START_DAY_CHOICES.index(min(start, R.SEASON_DAYS - 2)),
               C.LAND_DAY_CHOICES.index(min(land_day, R.SEASON_DAYS - 1))]
        g[slot] = row + [0] * (len(C.GENES) - len(row))
    return g.reshape(-1)
