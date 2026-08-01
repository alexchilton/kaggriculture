"""A mixed farm: wheat and cash crops alongside the herd, which is what the winners actually run.

**Why this exists when `shepherd` already plays the animal economy.** `shepherd` grows nothing. It
buys 100% of its feed and has no crop income at all. That was built on a measurement I got wrong: my
first pass over the replays required a crop argument on `PLANT`, found none because `PLANT` carries
no argument, and concluded the top seats never plant. They plant constantly.

Corrected, over the top 25 of 312 real leaderboard seats ($112k-$132k):

    seed UNITS bought, per seat        SELL units, share of all sales
      WHEAT       41   <-- largest      WHEAT       36.8%   <-- largest
      MELON       25                    FERTILIZER  23.1%
      CARROT      22                    MILK        19.7%
      STRAWBERRY  21                    WOOL        15.5%
      TOMATO       2                    MELON        2.2%
                                        CARROT       1.9%
    96 PLANT actions per seat           STRAWBERRY   0.8%
    first plant day 0, last day 26

So it is not a rancher and it is not a phase transition either -- they plant from day 0 to day 26
without stopping. **Wheat is simultaneously their biggest seed purchase and their biggest sale.**
They grow it, buy it as well (median 295 BUY_PRODUCT orders), feed the herd with it, and sell the
surplus. Melon, carrot and strawberry are real secondary lines, about 5% of sale volume together.

That is also the likeliest reason `converter` -- which farms melon -- held up better than `shepherd`
on fresh seeds despite banking less: it has an income line `shepherd` does not have at all.

**The tension this agent has to manage, and the reason the crew matters.** A crop dies after two
unwatered days and an animal escapes after two unfed nights, so both halves demand a visit *every
day*. One farmer has 24 actions. The winners run a crew of 12 against 11 animals plus crop tiles,
which is what makes both halves affordable at once -- the same argument `shepherd`'s docstring makes
about `rancher`, now applied to a second economy on top.

Plot layout: pasture takes the tiles nearest the shed, because feed is carried by hand and every step
is paid daily. Crops take the tiles after that -- water is not carried, so a longer walk costs a
step but never a wasted trip.
"""

BOARD = 10

ANIMALS = {
    "COW": {"cost": 400, "structure": "PASTURE", "product": "MILK", "interval": 2},
    "GOOSE": {"cost": 300, "structure": "COOP", "product": "EGG", "interval": 1},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "product": "WOOL", "interval": 3},
}
# Seed costs, from the environment: WHEAT is the cheapest thing on the board and the best seller.
SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
BASE_PRICE = {"MILK": 160, "EGG": 50, "WOOL": 200, "WHEAT": 25, "FERTILIZER": 100,
              "MELON": 90, "CARROT": 30, "STRAWBERRY": 60, "TOMATO": 45}
# Days from planting to the end of the yield window, so seed bought later is money burned.
CROP_SPAN = {"WHEAT": 8, "CARROT": 8, "MELON": 12, "STRAWBERRY": 14, "TOMATO": 14}

PARAMS = {
    # ---- herd, carried over from shepherd, whose animal half works ----
    "herd": 9,
    "sheep_share": 0.55,        # the ES's final best landed on the measured mix
    "hands_per_animal": 1.0,
    "max_hands": 12,
    "hire_reserve": 400.0,
    "feed_carry": 4,
    "wheat_per_animal": 2,      # bought feed, on top of what the farm grows
    # ---- crops, the half shepherd is missing ----
    # Wheat first because it is both the feed input and 36.8% of the winners' sales, then one cash
    # crop. Melon over strawberry: it is cheaper per seed and its span is short enough for two cycles.
    "wheat_tiles": 10,
    "cash_crop": "MELON",
    "cash_tiles": 8,
    "last_plant_day": 16,       # a 12-day melon span has to close before the season ends
    # ---- shared ----
    "sell_floor_frac": 0.65,
    "sell_batch": 3,
    "endgame_day": 27,
    # Pinned, not searched: measured median first land purchase is turn 242 = day 10, and
    # LAND_PRICES[0] + LAND_PRICES[1] is exactly the $3,000 opening bank.
    "land_day": 10,
    "land_reserve": 4000.0,
}


def _shed_tiles(size=BOARD):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _usable(size=BOARD, unlocked_quadrants=("NW",)):
    """Every unlocked tile, nearest the shed anchor first.

    Only one of the four shed-access inner corners starts usable -- the other three sit in NE, SW and
    SE, all locked. Returning all four is what once let an agent build a single pasture and idle.
    """
    half = size // 2

    def quadrant(x, y):
        return ("N" if y < half else "S") + ("W" if x < half else "E")

    anchor = (half - 1, half - 1)
    out = [(x, y) for y in range(size) for x in range(size)
           if quadrant(x, y) in unlocked_quadrants]
    out.sort(key=lambda t: (abs(t[0] - anchor[0]) + abs(t[1] - anchor[1]), t))
    return out


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
        seeds_held = farm.get("seeds", {}) or {}
        money = farm["money"]
        tiles = farm["tiles"]

        quads = tuple(farm.get("unlocked_quadrants", ["NW"]))
        usable = _usable(unlocked_quadrants=quads)
        # Pasture nearest the shed: feed is carried, so every step is paid every day. Crops after.
        pasture_plots = usable[: p["herd"]]
        crop_plots = usable[p["herd"]: p["herd"] + p["wheat_tiles"] + p["cash_tiles"]]
        wheat_plots = crop_plots[: p["wheat_tiles"]]
        cash_plots = crop_plots[p["wheat_tiles"]:]
        shed_tiles = _shed_tiles()
        endgame = day >= p["endgame_day"]
        cash = p["cash_crop"]

        positions = [tuple(farm["farmer"])] + [tuple(q) for q in farm.get("hands", [])]
        n_units = len(positions)

        def tile_at(xy):
            return tiles[xy[1]][xy[0]]

        # ---- board state ------------------------------------------------------------------
        placed, owned_kinds = [], {}
        for xy in pasture_plots:
            t = tile_at(xy)
            if isinstance(t, dict) and "animal" in t:
                placed.append(xy)
                owned_kinds[t["animal"]] = owned_kinds.get(t["animal"], 0) + 1
        n_placed = len(placed)

        held_animals = sum(inv.get(a, 0) for inv in inventories
                           for a in ("COW", "SHEEP", "GOOSE"))
        shed_animals = {a: shed.get(a, 0) for a in ("COW", "SHEEP", "GOOSE")}
        n_shed_animals = sum(shed_animals.values())

        def planted_count(plots, crop):
            n = 0
            for xy in plots:
                t = tile_at(xy)
                if isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == crop:
                    n += 1
            return n

        n_wheat = planted_count(wheat_plots, "WHEAT")
        n_cash = planted_count(cash_plots, cash)

        # ---- market -----------------------------------------------------------------------
        market = []

        # Feed first: two unfed nights costs the animal and its whole price.
        need_wheat = max(1, n_placed) * p["wheat_per_animal"] + n_units
        have_wheat = shed.get("WHEAT", 0) + sum(inv.get("WHEAT", 0) for inv in inventories)
        if have_wheat < need_wheat and money > 300:
            market.append(["BUY_PRODUCT", "WHEAT", min(need_wheat - have_wheat, 12)])

        # **Seed, which shepherd never buys.** Wheat is the cheapest seed on the board at $10 and the
        # winners' biggest sale line; the cash crop is the secondary income. Only while a planting
        # can still reach the end of its yield window.
        for crop, plots, standing in ((("WHEAT"), wheat_plots, n_wheat),
                                      (cash, cash_plots, n_cash)):
            if day + CROP_SPAN.get(crop, 12) > 29 or day > p["last_plant_day"]:
                continue
            short = len(plots) - standing - seeds_held.get(crop, 0)
            if short > 0 and money > SEED_COST.get(crop, 50) * short + 400:
                market.append(["BUY_SEED", crop, short])

        ready = sum(1 for xy in pasture_plots
                    if isinstance(tile_at(xy), dict)
                    and tile_at(xy).get("kind") == "PASTURE"
                    and "animal" not in tile_at(xy))
        if (n_placed + held_animals + n_shed_animals < p["herd"]
                and ready > held_animals + n_shed_animals and day <= 11):
            n_sheep = (owned_kinds.get("SHEEP", 0) + shed.get("SHEEP", 0)
                       + sum(inv.get("SHEEP", 0) for inv in inventories))
            n_cow = (owned_kinds.get("COW", 0) + shed.get("COW", 0)
                     + sum(inv.get("COW", 0) for inv in inventories))
            pick = "SHEEP" if n_sheep < p["sheep_share"] * (n_sheep + n_cow + 1) else "COW"
            if money > ANIMALS[pick]["cost"] + 500:
                market.append(["BUY_ANIMAL", pick, 1])

        n_extra = len(quads) - 1
        if n_extra < 2 and day >= p["land_day"] and money >= p["land_reserve"]:
            market.append(["BUY_LAND"])

        # Crew scaled to total daily work, not just the herd: a crop wants watering as surely as an
        # animal wants feeding, so both count.
        jobs = n_placed + n_wheat + n_cash
        want_hands = min(int(p["max_hands"]), int(round(jobs * p["hands_per_animal"] / 2)))
        if not endgame and n_units - 1 < want_hands and money > p["hire_reserve"] + 200:
            for _ in range(min(want_hands - (n_units - 1), 4)):
                market.append(["HIRE"])

        # Sell animal products and crops. Wheat is held back while the herd still needs feeding --
        # the winners sell it heavily, but they also grow far more of it than this does.
        sellable = ["WOOL", "MILK", "EGG", "FERTILIZER", cash]
        if endgame or have_wheat > need_wheat * 3:
            sellable.append("WHEAT")
        for product in sellable:
            have = shed.get(product, 0)
            if have <= 0:
                continue
            if product == "WHEAT" and not endgame:
                have = max(0, have - need_wheat)
            price = prices.get(product, BASE_PRICE.get(product, 0))
            if endgame or price >= BASE_PRICE.get(product, 0) * p["sell_floor_frac"]:
                qty = have if endgame else min(have, p["sell_batch"])
                if qty > 0:
                    market.append(["SELL", product, qty])

        # ---- units ------------------------------------------------------------------------
        claimed = set()
        acts = []
        for i, pos in enumerate(positions):
            inv = inventories[i] if i < len(inventories) else {}
            carried_total = sum(inv.values())
            on_shed = pos in shed_tiles
            here = tile_at(pos)
            act = None

            # Standing on a tile that wants something: do it, no walk, no collision.
            if here is None and (pos in pasture_plots):
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
            elif isinstance(here, dict) and here.get("kind") == "PLANT":
                # **Harvest before water, water before anything else.** Produce in the ground earns
                # nothing, and two dry days kill the plant outright.
                if here.get("yield_units", 0) > 0:
                    act = ["HARVEST"]
                elif not here.get("watered_today"):
                    act = ["WATER"]
            elif (isinstance(here, dict) and here.get("kind") == "PASTURE"
                  and "animal" not in here and pos in pasture_plots):
                for a in ("SHEEP", "COW"):
                    if inv.get(a, 0) >= 1:
                        act = ["PLACE", a]
                        break
            elif here is None and pos in crop_plots:
                crop = "WHEAT" if pos in wheat_plots else cash
                if seeds_held.get(crop, 0) >= 1:
                    act = ["PLANT"]

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

            # Otherwise walk to the nearest unclaimed job, animals first -- an unfed animal loses its
            # whole purchase price, a dry crop loses one tile's yield.
            if act is None:
                jobs_xy = []
                for xy in pasture_plots + crop_plots:
                    if xy in claimed or xy == pos:
                        continue
                    t = tile_at(xy)
                    if t is None:
                        if xy in pasture_plots or seeds_held.get(
                                "WHEAT" if xy in wheat_plots else cash, 0) >= 1:
                            jobs_xy.append(xy)
                    elif isinstance(t, dict) and "animal" in t:
                        if (t.get("yield_units", 0) > 0 or not t.get("fed_today")
                                or not t.get("cared_today") or t.get("fertilizer_available")):
                            jobs_xy.append(xy)
                    elif isinstance(t, dict) and t.get("kind") == "PLANT":
                        if t.get("yield_units", 0) > 0 or not t.get("watered_today"):
                            jobs_xy.append(xy)
                    elif isinstance(t, dict) and t.get("kind") in ("WEED", "PASTURE"):
                        jobs_xy.append(xy)
                if jobs_xy:
                    target = _nearest(pos, jobs_xy)
                    claimed.add(target)
                    act = [_step_toward(pos, target)]
                elif not on_shed:
                    act = [_step_toward(pos, _nearest(pos, shed_tiles))]
                else:
                    act = ["PASS"]

            acts.append(act)

        return {"farmer": acts[0], "hands": acts[1:], "market": market[:10]}

    return agent


agent = make_agent()
