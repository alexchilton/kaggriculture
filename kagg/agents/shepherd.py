"""A livestock agent with a crew: `rancher`'s economy, scaled by the thing `rancher` refuses.

**Why this exists, and what it changes.** `rancher` banks $45.7k on six cows with **zero hired
hands**, and its own comment records why it stops there:

    "herd": 6,   # measured optimum: 4 -> $31.6k, 6 -> $45.7k, 10 -> $15.9k.
                 # Action budget, not money.

That is correct and it is the ceiling. One farmer has 24 actions a day; every animal needs a feed, a
care and a harvest, plus the walk between them, so a herd of ten starves and drops to $15.9k. The
conclusion drawn was "animals do not scale". The actual conclusion is "animals do not scale on one
pair of hands".

Measured across 312 real leaderboard seats ($3.5k-$132k), the top 25 run **11 animals AND a crew of
12**, re-hired every morning. They are not choosing between the herd and the wages; the wages are
what make the herd work. The correlations say the same thing -- FEED +0.452 and CARE +0.441 are the
two strongest predictors of money in the game, ahead of everything else, while PLANT is -0.358 and
WATER -0.276.

The rest of the measured playbook, applied here directly:

    animals   median 11 -- SHEEP 55%, COW 43%, GOOSE 1.8%    (pastures, not coops)
              first purchase day 0, last day 11
    wheat     BOUGHT, median 295 orders, from day 0 -- not grown
    crew      median 12, peak 13
    land      2 quadrants, first at median turn 242 = **day 10**
    feed:care 1.01 -- one visit, both ops
    sells     WHEAT 47.5%, FERTILIZER 23.1%, WOOL 12.0%, MILK 9.1%

`FERTILIZER` at 23% of the winners' sales is the line most easily missed: an animal produces it for
free, every day, and `rancher` already collects it. With eleven animals instead of six it is a
quarter of the income.

**Two rules the game enforces that shape everything above.** An animal escapes after two unfed
nights, and first yield is day 4 for a goose, 6 for a sheep, 8 for a cow -- so an unfed animal is a
guaranteed total loss of its $300-$500, never a slow one. And `FEED` consumes one carried WHEAT per
animal per day, so a unit has to be holding wheat when it arrives: the shed trip is inside the loop.

**Land at day 10, not day 2.** `LAND_PRICES` is (1000, 2000, 4000) and the first two sum to exactly
the $3,000 opening bank, so buying early is affordable and ruinous -- the replay seat that bought
three quadrants from turn 1 banked $9,443 against the leaders' $130k. `converter` ships
`land_days=(2, 8)`; the measured median is day 10, once there is income to pay for it.
"""

BOARD = 10

ANIMALS = {
    "COW": {"cost": 400, "structure": "PASTURE", "product": "MILK", "interval": 2},
    "GOOSE": {"cost": 300, "structure": "COOP", "product": "EGG", "interval": 1},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "product": "WOOL", "interval": 3},
}
BASE_PRICE = {"MILK": 160, "EGG": 50, "WOOL": 200, "WHEAT": 25, "FERTILIZER": 100}

PARAMS = {
    # Sheep and cow only: both are PASTURE animals, and BUILD_PASTURE correlates with money at
    # +0.376 against BUILD_COOP's +0.022. Geese are 1.8% of the winners' purchases.
    "herd": 11,
    "sheep_share": 0.55,        # measured 55/43 sheep/cow among the top 25
    # The crew is the whole point. Scaled to the herd rather than fixed, because an idle hand is
    # pure cost and hands are dismissed nightly, so the size is a free choice every morning.
    "hands_per_animal": 1.0,
    "max_hands": 12,
    "hire_reserve": 400.0,      # never hire down to nothing; feed comes first
    "sell_floor_frac": 0.70,
    "sell_batch": 3,
    "endgame_day": 27,
    "feed_carry": 4,
    "wheat_per_animal": 3,
    # **Pinned, and deliberately excluded from the ES search.** Measured median first land purchase
    # across 312 real leaderboard seats is turn 242 = day 10. `LAND_PRICES[0] + LAND_PRICES[1]` is
    # exactly the $3,000 opening bank, so anything earlier is affordable and ruinous -- the seat that
    # bought three quadrants from turn 1 banked $9,443 against the leaders' $130k. A fact this well
    # measured is a constant, not a dial: see the note in `scripts/tune_shepherd.py`.
    "land_day": 10,
    "land_reserve": 4000.0,
}


def _shed_tiles(size=BOARD):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _plots(size=BOARD, unlocked_quadrants=("NW",)):
    """Herd tiles, nearest the shed first, restricted to unlocked quadrants.

    Only one of the four shed-access tiles starts usable -- the other three inner corners sit in NE,
    SW and SE, all locked. Handing back all four is what once let the farmer build a single pasture
    and idle twenty turns a day, per `rancher`.
    """
    half = size // 2

    def quadrant(x, y):
        return ("N" if y < half else "S") + ("W" if x < half else "E")

    anchor = (half - 1, half - 1)
    usable = [(x, y) for y in range(size) for x in range(size)
              if quadrant(x, y) in unlocked_quadrants]
    usable.sort(key=lambda t: (abs(t[0] - anchor[0]) + abs(t[1] - anchor[1]), t))
    return usable


def _step_toward(pos, target):
    (x, y), (tx, ty) = pos, target
    dx, dy = tx - x, ty - y
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def _nearest(pos, targets):
    return min(targets, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))


def make_agent(overrides=None):
    p = dict(PARAMS)
    if overrides:
        p.update(overrides)

    def agent(obs, config=None):
        me = obs.get("player", 0)
        farm = obs["farms"][me]
        day = obs.get("day", 0)
        private = obs.get("private", {}) or {}
        shed = private.get("shed", {}) or {}
        inventories = private.get("inventories") or [{}]
        prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
        money = farm["money"]
        tiles = farm["tiles"]

        quads = tuple(farm.get("unlocked_quadrants", ["NW"]))
        plots = _plots(unlocked_quadrants=quads)[: p["herd"]]
        shed_tiles = _shed_tiles()
        endgame = day >= p["endgame_day"]

        positions = [tuple(farm["farmer"])] + [tuple(q) for q in farm.get("hands", [])]
        n_units = len(positions)

        def tile_at(xy):
            return tiles[xy[1]][xy[0]]

        # ---- what the herd needs right now --------------------------------------------------
        placed, owned_kinds = [], {}
        for xy in plots:
            t = tile_at(xy)
            if isinstance(t, dict) and "animal" in t:
                placed.append(xy)
                owned_kinds[t["animal"]] = owned_kinds.get(t["animal"], 0) + 1
        n_placed = len(placed)

        held_animals = sum(
            inv.get(a, 0) for inv in inventories for a in ("COW", "SHEEP", "GOOSE"))
        shed_animals = {a: shed.get(a, 0) for a in ("COW", "SHEEP", "GOOSE")}
        n_shed_animals = sum(shed_animals.values())

        # ---- market -------------------------------------------------------------------------
        market = []

        # **Feed first, always.** Two unfed nights and an animal leaves with its whole price. The
        # buffer scales with the herd because every animal eats one wheat a day.
        need_wheat = max(1, n_placed) * p["wheat_per_animal"] + n_units
        have_wheat = shed.get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in inventories)
        if have_wheat < need_wheat and money > 300:
            market.append(["BUY_PRODUCT", "WHEAT", min(need_wheat - have_wheat, 20)])

        # Livestock, up to the herd target, only into pasture that exists or is about to. Buying an
        # animal with nowhere to put it leaves it in the shed, unfed, and it is money burned.
        ready = sum(1 for xy in plots
                    if isinstance(tile_at(xy), dict)
                    and tile_at(xy).get("kind") == "PASTURE"
                    and "animal" not in tile_at(xy))
        want_more = n_placed + held_animals + n_shed_animals < p["herd"]
        if want_more and ready > held_animals + n_shed_animals and day <= 11:
            # Alternate to land near the measured 55/43 split without needing an RNG.
            n_sheep = owned_kinds.get("SHEEP", 0)
            n_cow = owned_kinds.get("COW", 0)
            pick = "SHEEP" if n_sheep <= n_cow * (p["sheep_share"] / (1 - p["sheep_share"])) \
                else "COW"
            if money > ANIMALS[pick]["cost"] + 500:
                market.append(["BUY_ANIMAL", pick, 1])

        # **Land at day 10, not day 2.** See the module docstring: the first two quadrants cost
        # exactly the opening bank, so early is affordable and ruinous.
        n_extra = len(quads) - 1
        if n_extra < 2 and day >= p["land_day"] and money >= p["land_reserve"]:
            market.append(["BUY_LAND"])

        # **The crew, which is what `rancher` will not pay for.** Hands are dismissed nightly and the
        # Fibonacci fee resets each morning, so this is a fresh decision every day and an idle hand
        # is a wasted one. Sized to the herd: eleven animals is eleven feed-and-care visits.
        want_hands = min(int(p["max_hands"]), int(round(n_placed * p["hands_per_animal"])))
        if (not endgame and n_units - 1 < want_hands
                and money > p["hire_reserve"] + 200):
            for _ in range(min(want_hands - (n_units - 1), 4)):
                market.append(["HIRE"])

        # Sell everything the animals make. Fertiliser is 23% of the winners' income and costs
        # nothing to produce. Wheat is feed and is never sold.
        for product in ("WOOL", "MILK", "EGG", "FERTILIZER"):
            have = shed.get(product, 0)
            if have <= 0:
                continue
            price = prices.get(product, BASE_PRICE.get(product, 0))
            floor = BASE_PRICE.get(product, 0) * p["sell_floor_frac"]
            if endgame or price >= floor:
                qty = have if endgame else min(have, p["sell_batch"])
                if qty > 0:
                    market.append(["SELL", product, qty])

        # ---- units --------------------------------------------------------------------------
        # One pass per unit, with a `claimed` set so two units never walk to the same tile. That is
        # the multi-unit problem `rancher` never had to solve and the reason its herd could not grow.
        claimed = set()
        acts = []
        for i, pos in enumerate(positions):
            inv = inventories[i] if i < len(inventories) else {}
            carried_total = sum(inv.get(k, 0) for k in inv)
            on_shed = pos in shed_tiles
            here = tile_at(pos)
            act = None

            # On a tile that wants something, do it -- no walk, no collision.
            if pos in plots:
                if here is None:
                    act = ["BUILD_PASTURE"]
                elif isinstance(here, dict) and here.get("kind") == "WEED":
                    act = ["DIG"]
                elif isinstance(here, dict) and "animal" in here:
                    if here.get("yield_units", 0) > 0:
                        act = ["HARVEST"]
                    elif not here.get("fed_today") and inv.get("WHEAT", 0) >= 1:
                        act = ["FEED"]
                    elif not here.get("cared_today"):
                        act = ["CARE"]
                    elif here.get("fertilizer_available"):
                        act = ["COLLECT_FERTILIZER"]
                elif (isinstance(here, dict) and here.get("kind") == "PASTURE"
                      and "animal" not in here):
                    for a in ("SHEEP", "COW"):
                        if inv.get(a, 0) >= 1:
                            act = ["PLACE", a]
                            break

            # At the shed: bank produce, take an animal that needs housing, top up feed.
            if act is None and on_shed:
                if carried_total - inv.get("WHEAT", 0) >= p["sell_batch"]:
                    act = ["DROP"]
                elif n_shed_animals and not any(inv.get(a, 0) for a in ("SHEEP", "COW")):
                    for a in ("SHEEP", "COW"):
                        if shed_animals.get(a, 0) >= 1:
                            act = ["PICKUP", a, 1]
                            shed_animals[a] -= 1
                            break
                elif inv.get("WHEAT", 0) < 1 and shed.get("WHEAT", 0) >= 1:
                    act = ["PICKUP", "WHEAT", p["feed_carry"]]

            # Otherwise walk to the nearest unclaimed job.
            if act is None:
                jobs = []
                for xy in plots:
                    if xy in claimed or xy == pos:
                        continue
                    t = tile_at(xy)
                    if t is None:
                        jobs.append(xy)
                    elif isinstance(t, dict) and "animal" in t:
                        if (t.get("yield_units", 0) > 0 or not t.get("fed_today")
                                or not t.get("cared_today")
                                or t.get("fertilizer_available")):
                            jobs.append(xy)
                    elif isinstance(t, dict) and t.get("kind") in ("WEED", "PASTURE"):
                        jobs.append(xy)
                if jobs:
                    target = _nearest(pos, jobs)
                    claimed.add(target)
                    act = [_step_toward(pos, target)]
                elif carried_total and not on_shed:
                    act = [_step_toward(pos, _nearest(pos, shed_tiles))]
                elif not on_shed:
                    act = [_step_toward(pos, _nearest(pos, shed_tiles))]
                else:
                    act = ["PASS"]

            acts.append(act)

        return {"farmer": acts[0], "hands": acts[1:], "market": market[:10]}

    return agent


agent = make_agent()
