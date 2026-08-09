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


#: Units of rival supply arriving in the same book, per unit we sell.
#:
#: This is the old `OPPONENT_SHARE` reinterpreted. It used to be half of a *cap*; here it is the
#: rate at which someone else fills the book alongside us, which is what actually sets the price we
#: realise. Measured on the ladder: milk realises $205/unit in our wins and $73 in our losses on
#: identical board state, so the opponent's supply is worth more than any board decision in the
#: estimate. 1.0 means "they sell as much as we do", which is what a mirror-ish field does.
CONTEST = 1.0

#: Resolution of the sell-volume search in `best_revenue`, in units. Absolute, never relative.
_VOLUME_STEP = 4

_REVENUE_CACHE = {}


def sale_revenue(prod, units, contest=CONTEST):
    """Total dollars for selling `units` of `prod` across a season, on the environment's own curve.

    The book is not a bucket with a lid on it. It starts 10,000 deep and `market_price` is a smooth
    decreasing function of `inventory - I0`, so the drain is not a ceiling: selling past it lowers
    the price and does not stop the sale. Pricing every unit at `base * 0.5` and clipping the count
    at `DRAIN_UNITS * 0.5` gets both halves wrong at once, and the clip is the worse of the two --
    melon yields 12 units a tile against a clip of 15, so two melon tiles and sixteen scored
    identically and the planner stopped buying melon ground.

    The model here is deliberately three lines. As the season runs, the book carries our sales plus
    the rival's, less what the town has drained away, so by the time we have sold our `k`-th unit
    the level above `I0` is about

        net(k) = k * (1 + contest - drain / units)

    -- our `k`, their `contest * k`, minus the `drain * k / units` the town has taken by that point
    in the season. Price that with `market_price` and sum. When production is small enough that the
    drain outruns supply the term goes negative, `net` clamps at zero and every unit fetches base
    price, which is the correct answer for wheat and the reason wheat needs no correction.

    Sampled at 24 points rather than summed unit by unit: this is a scheduling estimate inside a
    beam search, the simulator is the judge of the result, and a precise model here would be a
    second implementation of the game that then drifts from the first.
    """
    units = int(max(0, units))
    if units <= 0:
        return 0.0
    key = (prod, units, round(contest, 3))
    hit = _REVENUE_CACHE.get(key)
    if hit is not None:
        return hit
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg

    i0 = kg.MARKET_PARAMS[prod]["I0"]
    # `.get(prod, 0)` and not `[prod]`: FERTILIZER has no entry, and that is not an oversight in the
    # table -- no shop carries it and `_town_center_sell` skips it explicitly, so its drain really is
    # zero. Nothing ever leaves that book but our own sales, which makes it the steepest product in
    # the game to oversupply and the only one where holding stock can never pay off.
    slope = 1.0 + contest - C.DRAIN_UNITS.get(prod, 0) / float(units)
    # Exact below 512 units, sampled above it. A resolution that VARIES with `units` makes the
    # result non-monotone in `units` -- measured: 24 melon tiles scored below 16, and 8 cows below
    # 4, purely from the grid moving. That is indistinguishable from a real economic optimum and
    # would have been read as one.
    n = units if units <= 512 else 512
    total = 0.0
    for j in range(n):
        k = units * (j + 0.5) / n
        total += kg.market_price(prod, int(round(i0 + max(0.0, slope * k))))
    val = total / n * units
    _REVENUE_CACHE[key] = val
    return val


def best_revenue(prod, produced, contest=CONTEST):
    """What `produced` units are worth, given we may decline to sell the ones that pay nothing.

    `sale_revenue` is not monotone: past some volume each extra unit earns less than it costs the
    units behind it, and total revenue falls. That is a real property of the market and not a
    modelling artifact -- it is the same fact `HOLD_A_FLOORED_BOOK` acts on in the shipped agent,
    where a unit sold into a floored book earns $1 and costs ~$150 on everything sold after it.

    But it must not make *ground* look worthless. Owning a tile never obliges us to dump its output,
    so the value of production is the best we could do with it, which is monotone non-decreasing in
    `produced` and concave. Concavity is the property the planner actually needs: without it the
    estimate is linear and the search hands the whole farm to whichever product has the highest base
    price, because nothing tells it the book fills up.
    """
    produced = int(max(0, produced))
    if produced <= 0:
        return 0.0
    # The candidate volumes must form a grid that GROWS with `produced` -- a fixed absolute step, so
    # the set searched at 200 units contains the set searched at 100. A step of `produced // 24`
    # does not, and the maximum over a shifting grid is not monotone.
    # Stop at the FIRST local peak, never the global one. Once `market_price` bottoms out at
    # `PRICE_FLOOR` the revenue of `q` units is `q * $1` and rises without limit, so a global search
    # always returns "dump 3,000 units at $5" -- which is not a strategy, it is the estimate leaving
    # the region it models. That branch is what made geese look unbounded on 2026-08-09, and it is
    # the same mistake `HOLD_A_FLOORED_BOOK` exists to stop the shipped agent making for real.
    best = 0.0
    for q in range(_VOLUME_STEP, produced + 1, _VOLUME_STEP):
        v = sale_revenue(prod, q, contest)
        if v > best:
            best = v
        elif v < best * 0.98:
            return best
    return max(best, sale_revenue(prod, produced, contest))


def revenue_rate(kind, what, n_tiles):
    """Rough revenue per day once the chain is producing, from the measured season yields.

    Deliberately crude: this is a *scheduling* estimate used to decide affordability order, and the
    simulator is the judge of the result. A precise model here would be a second implementation of the
    game and would drift from it.
    """
    from kagg.economics import production as P

    # **WARNING, measured 2026-08-09: the `min(..., DRAIN_UNITS * OPPONENT_SHARE)` below is wrong,
    # and it got worse when `DRAIN_UNITS` was corrected to 1.32.6.** Do not wire this planner into a
    # submission until it is replaced.
    #
    # The drain is not a ceiling. Each book starts 10,000 deep and `market_price` only falls as
    # `inventory - I0` grows, so selling past the drain lowers the price without stopping the sale.
    # Revenue-maximising volume against the cap this function applies:
    #
    #     product   drain  cap now  opt vol   $ at opt   $ at cap   forgone
    #     MELON        30       15      180     31,509      3,750     27,759
    #     MILK        322      161      320     51,200     25,760     25,440
    #     WOOL        204      102      225     42,947     20,400     22,547
    #     STRAW       452      226      400     48,000     27,120     20,880
    #
    # So the cap forgoes ~$96k of revenue across four products, and correcting `DRAIN_UNITS`
    # multiplied the melon error by 4.67x rather than removing it. `scripts/measure_true_drain.py`
    # reached the same conclusion from a tape and it was not acted on.
    #
    # The binding constraint is not the drain, it is **contest**. Both sides selling the same volume:
    #
    #     product   each sells   $/u solo   $/u contested
    #     MELON            110        229             139
    #     MILK             200        160              32
    #     WOOL             200        200              40
    #     STRAW            260        120              15
    #
    # which is what the ladder shows: milk realises $205/unit in our wins and $73 in our losses, on
    # identical board state. The replacement is a marginal-revenue curve carrying a *measured* rival
    # supply term, not a share dial -- see `docs/the_planner_prices_the_wrong_market_2026-08-08.md`.
    if kind == "ranch":
        a = R.ANIMALS[what]
        # `ANIMAL_YIELD_PER_SEASON`, not `events * max_held`. `max_held` caps the *unharvested*
        # buffer -- `kaggriculture.py:813` is `yield_units = min(max_held, yield_units + 1 + bonus)`
        # -- so an animal makes one unit per event and the old formula overstated every herd by
        # 4-6x. Corrected, milk's 160-unit peak is ~14 cows rather than 2.4, which finally brackets
        # the 9 cows and 11 sheep the rank-1 ladder agent actually runs.
        units = P.ANIMAL_YIELD_PER_SEASON[a["product"]] * n_tiles
        days = max(R.SEASON_DAYS - a["first_yield_day"], 1)
        return best_revenue(a["product"], units) / days
    y = max(P.TILE_YIELD_FERTILIZED[what], P.TILE_YIELD_PER_SEASON[what])
    return best_revenue(what, y * n_tiles) / R.SEASON_DAYS


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
    running = []                      # (index, kind, what, n_tiles, earns_from)
    curve = []

    pending = list(order)
    for day in range(horizon):
        # Yesterday's production and today's costs.
        #
        # **Revenue starts at `earns_from`, not at the start day**, and getting that wrong is what put
        # our land purchase on day 3 instead of the leader's day 7. A cow produces nothing until
        # `first_yield_day = 8`, but this credited $720/day from the moment the chain started -- so with
        # two cow chains, two wheat and a melon it believed it had earned $5,340 by day 3 when the real
        # bank was about $1,800, and cheerfully bought a parcel it could not fund a crop on.
        #
        # Costs, by contrast, start immediately. Feed is due from the day the animal is placed.
        for i, kind, what, n, earns_from in running:
            if day >= earns_from:
                bank += revenue_rate(kind, what, n)
            bank -= daily_burn(kind, what, n)
        bank = max(bank, 0.0)

        # **Chains before land, and land only out of revenue.** Buying a parcel the first day it
        # "clears" is greedy-by-affordability, not greedy-by-value, and it is the exact mistake the
        # beam's old `LAND_DAY_CHOICES.index(0)` hardcode made. Traced on the first run of this
        # scheduler: day 0 spent $1,000 of a $3,000 bank on the NE parcel, which left $1,920 and blocked
        # a $1,200 cow herd by $80 -- the largest market in the game, lost to an $80 shortfall.
        #
        # So: fund every chain that can start on ground already owned, then consider land, and never
        # before `EARLIEST_REVENUE_DAY` since until then the opening bank is the whole of the money.
        for i in list(pending):
            kind, what, tiles = mix[i]
            if need[i] > parcels_bought:
                continue
            cost = opening_cost(kind, what, len(tiles))
            if bank < cost + reserve:
                continue
            bank -= cost
            placed[i] = day
            pending.remove(i)
            running.append((i, kind, what, len(tiles), day + payback_days(kind, what)))

        # Now land, out of what is left -- and **only when the chain that wants it can also be paid
        # for.** Buying the parcel alone was the defect: the schedule spent $1,000 on day 3 and then had
        # nothing left for the 24 tiles of strawberry seed the parcel was bought for, so `decode()`
        # refused the chain and the ground sat idle. Ground with no crop on it is worse than no ground.
        #
        # This is what makes the rule reproduce the leader instead of merely resembling him. He buys on
        # **days 7 and 10**, not day 3, because that is when a parcel *and* the chain behind it both
        # clear. Requiring the pair moves our purchase from day 3 to the same window, from the same
        # greedy rule -- the timing is derived, not copied.
        if parcels_bought < parcels_needed and day >= C.EARLIEST_REVENUE_DAY:
            price = R.LAND_PRICES[parcels_bought]
            wanted_by = [i for i in pending if need[i] > parcels_bought]
            if wanted_by:
                # The cheapest chain waiting on this parcel: if even that cannot follow, waiting is
                # strictly better than owning idle ground.
                follow_on = min(opening_cost(mix[i][0], mix[i][1], len(mix[i][2]))
                                for i in wanted_by)
                if bank >= price + follow_on + reserve and day not in parcel_day.values():
                    bank -= price
                    parcel_day[parcels_bought] = day
                    parcels_bought += 1

        # And anything the new ground just unblocked.
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
            running.append((i, kind, what, len(tiles), day + payback_days(kind, what)))
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
