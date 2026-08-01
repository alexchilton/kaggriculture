"""Converter: buy wheat, feed it to livestock, sell milk and wool.

Reverse-engineered from episode 89197802, where the top two agents banked $106k and $113k while our
best agent (`contrarian`) banks about $38k. Both winners ran the same engine, and neither one is
mainly a farmer:

- **83% of the winner's revenue was milk and wool.** The runner-up made 81% by *trading* wheat.
  Crops were a sideline for both.
- **Wheat is an input, not a product.** The town drains it every turn of the season, so its price
  rises monotonically -- measured $25 to $56 across one game -- and it is the only good with a
  guaranteed upward curve. Both winners *bought* it rather than growing it, then converted it into
  $160 milk and $200 wool.
- **Animals were bought on turn 1** and the herd was expanded in a single burst once land allowed:
  yjhv built two pastures on day 0, then ten on day 10 and eight on day 11, going from 2 animals to
  20 in two days. There was no gradual ramp.
- **The herd sits on top of the shed.** Twenty animals inside x 2-7, y 1-7, wrapped around the four
  shed-access tiles. Feeding is the busiest recurring job on the farm -- one wheat per animal per
  day -- so every step of walking is paid twenty times a day for twenty days.
- **52-58% of unit actions were PASS in the first eight days.** They hire early and let hands idle,
  paying the Fibonacci fee to have labour standing by *before* the animals need it. Our heuristic
  hires to fill available work, which is the wrong way round.

Why this is worth building rather than tuning `rancher`: `rancher` keeps six animals and no hired
hands, and merely ties `heuristic`. The gap here is structural -- the feed loop, the wheat purchase
and the shed-adjacent layout -- not a parameter.

The one thing deliberately not copied is the runner-up's wheat arbitrage (buy at $37, sell at $44).
It works, but it is a bet on the town's drain schedule rather than on production, and it competes
for the same bank the herd needs.
"""

import numpy as np

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

BOARD = 10
SHED_ACCESS = [(4, 4), (5, 4), (4, 5), (5, 5)]

PARAMS = {
    "target_herd": 20,          # yjhv held 20; smlcr 12. The larger herd won.
    "cows_per_sheep": 1.4,      # cow: 6 milk/season at $160; sheep: slower but $200
    "expand_day": 8,            # the burst, timed to when melon revenue lands
    "max_hands": 14,            # both winners held 12; feeding 20 animals needs ~160 of 288 actions
    "min_hands": 2,
    "work_per_hand": 2.0,       # jobs a hand clears per day, used to size the crew
    "wheat_buffer": 40,         # shed wheat to keep ahead of the feed loop
    "wheat_per_turn": 2,
    "wheat_cheap": 32,          # below this, stockpile: the price only ever rises
    "wheat_stock_qty": 6,
    "shed_sell_at": 55,         # sell down before the 100-item cap destroys the overflow
    "melon_tiles": 14,          # melon is winner-take-all, and it funds the herd
    "sell_every": 3,
    "min_sell_qty": 2,
    "land_days": (2, 8),        # NE then SW; neither winner ever bought SE
    "reserve": 250.0,           # never spend the last of the bank on wheat
}


def _quadrant(x, y):
    return ("N" if y < 5 else "S") + ("W" if x < 5 else "E")


def _shed_ring():
    """Tiles ordered by walking distance from the shed -- where the herd goes.

    Feeding costs one trip per animal per day for twenty days, so this ordering is most of the
    agent's efficiency. Both winners' herds are exactly this shape.
    """
    tiles = []
    for y in range(BOARD):
        for x in range(BOARD):
            if (x, y) in SHED_ACCESS:
                continue        # keep the access tiles clear for pickup and drop
            d = min(abs(x - ax) + abs(y - ay) for ax, ay in SHED_ACCESS)
            tiles.append((d, x, y))
    tiles.sort()
    return [(x, y) for _d, x, y in tiles]


RING = _shed_ring()


def _step_toward(pos, target):
    """One legal step along the larger axis first; ties prefer horizontal."""
    (x, y), (tx, ty) = pos, target
    if x != tx and (abs(tx - x) >= abs(ty - y) or y == ty):
        return "EAST" if tx > x else "WEST"
    if y != ty:
        return "SOUTH" if ty > y else "NORTH"
    return None


def make_agent(overrides=None):
    p = dict(PARAMS)
    p.update(overrides or {})

    def agent(obs, config=None):
        me = obs["player"]
        farm = obs["farms"][me]
        private = obs["private"]
        tiles = farm["tiles"]
        money = farm["money"]
        day = obs.get("day", 0)
        hour = obs.get("hour", 0)
        shed = private.get("shed", {})
        seeds = private.get("seeds", {})
        inventories = private.get("inventories", [{}])
        unlocked = farm.get("unlocked_quadrants", ["NW"])
        prices = obs["market"]["prices"]

        def tile(x, y):
            return tiles[y][x]

        def usable(x, y):
            return _quadrant(x, y) in unlocked

        # ---- census -------------------------------------------------------------------------
        animals, empty_structs, plants, free = [], [], [], []
        for y in range(BOARD):
            for x in range(BOARD):
                if not usable(x, y):
                    continue
                c = tile(x, y)
                if c is None:
                    free.append((x, y))
                elif isinstance(c, dict):
                    if "animal" in c:
                        animals.append((x, y, c))
                    elif c.get("kind") in ("PASTURE", "COOP"):
                        empty_structs.append((x, y))
                    elif c.get("kind") == "PLANT":
                        plants.append((x, y, c))

        herd = len(animals)
        n_melon = sum(1 for _x, _y, c in plants if c.get("crop") == "MELON")
        positions = [tuple(farm["farmer"])] + [tuple(h) for h in farm.get("hands", [])]

        # The day's outstanding jobs, computed before the market block because crew size depends
        # on them. Feeding is the recurring one that pays; the rest are opportunistic.
        hungry = [(x, y) for x, y, c in animals if not c.get("fed_today")]
        uncared = [(x, y) for x, y, c in animals if c.get("cared_today") is False]
        fertile = [(x, y) for x, y, c in animals if c.get("fertilizer_available")]
        ripe = [(x, y) for x, y, c in animals if c.get("yield_units", 0) > 0]
        # **Pens are built just before the animals arrive, not on turn 1.**
        #
        # Sized naively this is 20 - 2 - 0 = 18 build jobs on the opening turn, which is more work
        # than the whole crew can do and it sits above planting in the priority order. The agent
        # then spends its first days building pasture for livestock it cannot afford until day 8,
        # while $1,120 of melon seed sits unplanted in the store -- and melon is the thing that pays
        # for the livestock. Measured, that ordering swung the final bank between $291 and $8,382
        # on neighbouring seeds depending on how it happened to fall out.
        building_season = day >= p["expand_day"] - 2
        build_spots = ([t for t in RING if t in free][: max(0, p["target_herd"] - herd
                                                            - len(empty_structs))]
                       if building_season else [])

        # ---- market -------------------------------------------------------------------------
        market = []

        # Sell the products, not the inputs. Wheat is feed and is never sold.
        #
        # Selling is also throttled to ten market orders a turn, and the shed holds 100 items
        # *total* across every product with the overflow destroyed each night. A herd of twenty
        # produces milk, wool, eggs and fertilizer daily on top of any crop, so waiting until the
        # shed is nearly full risks a multi-turn liquidation lag and destroyed stock. Sell on a
        # cadence, and sell everything the moment the shed gets close to the cap.
        shed_total = sum(v for k, v in shed.items() if k not in ("COW", "SHEEP", "GOOSE"))
        urgent = shed_total >= p["shed_sell_at"]
        if hour % p["sell_every"] == 0 or urgent:
            for item in ("MILK", "WOOL", "EGG", "FERTILIZER", "MELON", "STRAWBERRY", "CARROT"):
                have = shed.get(item, 0)
                if have >= (1 if urgent else p["min_sell_qty"]):
                    market.append(["SELL", item, have])

        # Wheat, continuously and in small lots, exactly as both winners bought it. One per animal
        # per day is the burn rate, so the buffer has to lead the herd rather than follow it.
        # **The season is phased, and the phases do not overlap.**
        #
        # A single priority list cannot express this: during the opening the wheat-and-feed loop
        # consumed the whole crew -- 517 PICKUPs against 128 FEEDs -- while three melon plants of a
        # planned fourteen sat unwatered and died by day 6, and the bank drained to $25 buying feed
        # for animals that did not exist. The replay is explicit about the order: melon goes in on
        # turn 1, the herd arrives on days 10-11, and the melon revenue is what pays for it.
        #
        # So before `expand_day` this is a melon farm and buys nothing else. After it, the herd is
        # the priority and crops are maintenance.
        livestock_phase = day >= p["expand_day"]

        # Wheat only ever gets more expensive: both players' feed demand drains the town's stock
        # all season and the price rose $25 -> $56 monotonically in the replay. So buy it cheap and
        # early rather than at a steady trickle -- the top two both bought at a constant rate and
        # one of them paid a median $58 for the privilege. Stock is worth holding here in a way it
        # is for no other good.
        wheat_price = prices.get("WHEAT", 30)
        need_wheat = (max(0, p["wheat_buffer"] + herd * 2 - shed.get("WHEAT", 0))
                      if livestock_phase or herd else 0)
        qty = p["wheat_stock_qty"] if wheat_price <= p["wheat_cheap"] else p["wheat_per_turn"]
        if need_wheat > 0 and money > p["reserve"] + wheat_price * qty:
            market.append(["BUY_PRODUCT", "WHEAT", min(qty, need_wheat)])

        # Land: NE then SW, on schedule. Neither winner bought SE.
        n_extra = len(unlocked) - 1
        if n_extra < 2 and day >= p["land_days"][min(n_extra, 1)]:
            cost = kg.LAND_PRICES[n_extra] if n_extra < len(kg.LAND_PRICES) else 1e9
            if money >= cost + p["reserve"]:
                market.append(["BUY_LAND"])

        # Herd: two on turn 1, then the whole rest in one burst once land is in.
        #
        # **Never buy an animal there is nowhere to put.** The first version bought one per turn
        # regardless, and ended a season with 37 sheep in the shed -- about $20,000 of livestock in
        # storage producing nothing, which is the whole reason the bank never rose above $500. An
        # animal only earns once it is standing on a pasture, so purchases are capped by the pens
        # that are actually free right now, minus whatever is already waiting to be carried out.
        waiting = sum(shed.get(a, 0) for a in ("COW", "SHEEP", "GOOSE"))
        room = len(empty_structs) - waiting
        want_now = 2 if day < p["expand_day"] else p["target_herd"]
        if herd < want_now and room > 0:
            n_cows = sum(1 for _x, _y, c in animals if c["animal"] == "COW")
            n_sheep = herd - n_cows
            pick = "COW" if n_cows <= n_sheep * p["cows_per_sheep"] else "SHEEP"
            if money >= kg.ANIMALS[pick]["cost"] + p["reserve"]:
                market.append(["BUY_ANIMAL", pick, 1])

        # **Melon first, and it pays for everything else.**
        #
        # Melon's glut curve is `sq`, so only ~158 units fit above I0 before the price floors: it is
        # winner-take-all between the two players, and whoever commits first takes the pot. Measured
        # directly -- `contrarian` banks $51k in this matchup almost entirely from melon, 225 units
        # off 24 tiles. An earlier version of this agent skipped melon to protect its opening bank,
        # handed that whole market over uncontested, and then could never afford livestock either.
        # Fourteen seeds cost $1,120 of a $3,000 start and return tens of thousands.
        #
        # It also fixes the ordering: melon revenue lands around day 8, which is exactly when the
        # herd wants expanding. Crops fund animals -- animals were never meant to come out of the
        # starting bank.
        if day == 0 and seeds.get("MELON", 0) + n_melon < p["melon_tiles"]:
            market.append(
                ["BUY_SEED", "MELON", p["melon_tiles"] - seeds.get("MELON", 0) - n_melon])

        # **Crew sized to the day's actual work, not held flat.**
        #
        # Both winners held twelve hands from day 0 and spent 52-58% of unit-actions on PASS in the
        # first eight days. That is not a ramp-up strategy, it is waste: hands are dismissed every
        # night and the Fibonacci fee resets each morning, so crew size is a free, memoryless choice
        # with no path dependency at all. Twelve hands cost $376/day against $12 for five, and the
        # twelfth hire alone costs $144. Carrying a full crew through the empty early days burns
        # roughly $2,900 -- close to the entire starting bank -- to watch them stand still.
        #
        # So count the jobs and buy the labour they need. This is the one place we should beat the
        # replay rather than copy it.
        jobs = (len(hungry) + len(ripe) + len(fertile) + len(uncared)
                + len(build_spots) + sum(1 for _x, _y, c in plants if not c.get("watered_today")))
        target_hands = int(min(p["max_hands"], max(p["min_hands"], jobs / p["work_per_hand"])))
        if len(farm.get("hands", [])) < target_hands:
            market.append(["HIRE"])

        # ---- units --------------------------------------------------------------------------
        actions, claimed = [], set()

        # **Each unit owns a fixed slice of the herd, for the whole game.**
        #
        # The first version picked the nearest outstanding job for each unit, recomputed every turn.
        # Units then oscillated: as another unit moved or an animal got fed, the "nearest" job
        # changed underneath them and they turned around. Measured over one season it spent 4,351
        # actions moving against 263 feeding, harvested 72 times where a 15-animal herd over twenty
        # days needs about 180, and lost four animals to starvation -- two missed feeds and an
        # animal escapes. Stable ownership costs a little walking distance and buys a
        # feed-harvest-sell loop that actually completes.
        n_units = max(1, len(positions))
        for idx, pos in enumerate(positions):
            inv = inventories[idx] if idx < len(inventories) else {}
            carrying = sum(inv.values())
            wheat_held = inv.get("WHEAT", 0)
            on_shed = pos in SHED_ACCESS
            mine = animals[idx::n_units]          # the same animals every turn
            act = None

            def go(target):
                d = _step_toward(pos, target)
                return [d] if d else None

            def nearest_shed():
                return min(SHED_ACCESS, key=lambda s: abs(s[0] - pos[0]) + abs(s[1] - pos[1]))

            # 1. Harvest anything ready -- **animals and crops both**.
            #
            # Rewriting this loop for stable per-unit animal ownership quietly dropped crop
            # harvesting altogether. The agent then planted melon, watered it faithfully for twelve
            # days, never picked it, and watched it expire: zero HARVEST actions and zero SELL
            # orders across an entire season. Every other symptom followed from that one omission --
            # nothing harvested means nothing in the shed, nothing sold, no money, and so no
            # animals either, because a $400 cow is unaffordable on a bank that never grew.
            for ax, ay, c in mine:
                if c.get("yield_units", 0) > 0 and carrying < 12:
                    act = ["HARVEST"] if pos == (ax, ay) else go((ax, ay))
                    break
            if act is None and carrying < 12:
                for tx, ty, c in plants:
                    if (tx, ty) in claimed or c.get("yield_units", 0) <= 0:
                        continue
                    claimed.add((tx, ty))
                    act = ["HARVEST"] if pos == (tx, ty) else go((tx, ty))
                    break

            # 2. Bank the haul: the nightly drop destroys anything past the 100-item shed cap, and
            #    produce in a hand cannot be sold.
            if act is None and carrying - wheat_held >= 6:
                act = ["DROP"] if on_shed else go(nearest_shed())

            # 2b. **Opening phase: this is a melon farm.** Planting and watering outrank
            #     everything, because seed in the store earns nothing and two dry days kill a $250
            #     plant. Ordering these below the feed loop is what let fourteen seeds become three
            #     plants and then none.
            if act is None and not livestock_phase:
                if seeds.get("MELON", 0) > 0:
                    far = [t for t in reversed(RING) if t in free and t not in claimed]
                    if far:
                        tx, ty = far[0]
                        claimed.add((tx, ty))
                        act = ["PLANT", "MELON"] if pos == (tx, ty) else go((tx, ty))
                if act is None:
                    for tx, ty, c in plants:
                        if (tx, ty) in claimed or c.get("watered_today"):
                            continue
                        claimed.add((tx, ty))
                        act = ["WATER"] if pos == (tx, ty) else go((tx, ty))
                        break

            # 3. Place first, feed second. Placing was below feeding, and feeding always has work
            #    -- an animal needs it daily -- so units never reached the placement step and bought
            #    livestock simply accumulated in the shed.
            if act is None and empty_structs:
                held = next((a for a in ("COW", "SHEEP", "GOOSE") if inv.get(a, 0) > 0), None)
                if held:
                    ax, ay = empty_structs[0]
                    act = ["PLACE", held] if pos == (ax, ay) else go((ax, ay))
                elif any(shed.get(a, 0) > 0 for a in ("COW", "SHEEP", "GOOSE")):
                    a = next(a for a in ("COW", "SHEEP", "GOOSE") if shed.get(a, 0) > 0)
                    act = ["PICKUP", a, 1] if on_shed else go(nearest_shed())

            # 4. Feed. Two missed days and the animal escapes.
            if act is None:
                unfed = [(ax, ay) for ax, ay, c in mine if not c.get("fed_today")]
                if unfed:
                    if wheat_held > 0:
                        ax, ay = unfed[0]
                        act = ["FEED"] if pos == (ax, ay) else go((ax, ay))
                    elif shed.get("WHEAT", 0) > 0:
                        act = (["PICKUP", "WHEAT", min(6, len(unfed))] if on_shed
                               else go(nearest_shed()))

            # 5. **Water before any of the optional animal jobs.**
            #
            # Watering is time-critical in exactly the way feeding is: two dry days and the plant
            # dies, taking its $250 with it, and melon only accrues yield on days it is watered
            # inside its window. Below fertilizer and care it never happened at all -- those always
            # have work once a herd exists -- so the agent bought melon seed, planted it, and then
            # let it die while tending cows. Crops fund the herd; they cannot be the leftover.
            if act is None:
                for tx, ty, c in plants:
                    if (tx, ty) in claimed or c.get("watered_today"):
                        continue
                    claimed.add((tx, ty))
                    act = ["WATER"] if pos == (tx, ty) else go((tx, ty))
                    break

            # 6. Build the pens the herd will need, nearest the shed first.
            if act is None and idx < len(build_spots):
                bx, by = build_spots[idx]
                act = ["BUILD_PASTURE"] if pos == (bx, by) else go((bx, by))

            # 6. Free money: one action per animal per day, and fertilizer sells for ~$100.
            if act is None:
                for ax, ay, c in mine:
                    if c.get("fertilizer_available"):
                        act = ["COLLECT_FERTILIZER"] if pos == (ax, ay) else go((ax, ay))
                        break

            # 7. CARE banks +1 on the next fed production. With this much idle capacity it is
            #    nearly free, so every animal gets it every cycle.
            if act is None:
                for ax, ay, c in mine:
                    if not c.get("cared_today") and c.get("fed_today"):
                        act = ["CARE"] if pos == (ax, ay) else go((ax, ay))
                        break

            # 8. Plant the melon we bought seed for, on tiles *away* from the shed so the herd keeps
            #    the short-walk ring it needs for feeding. This sits above watering because seed in
            #    the store earns nothing and the yield window starts from the day it goes in.
            if act is None and seeds.get("MELON", 0) > 0:
                far = [t for t in reversed(RING) if t in free and t not in claimed]
                if far:
                    tx, ty = far[0]
                    claimed.add((tx, ty))
                    act = ["PLANT", "MELON"] if pos == (tx, ty) else go((tx, ty))

            # 9. Watering. An unwatered plant dies after two dry days and takes its $250 with it,
            #    so melon is watered like the economy it is.
            if act is None:
                for tx, ty, c in plants:
                    if (tx, ty) in claimed or c.get("watered_today"):
                        continue
                    claimed.add((tx, ty))
                    act = ["WATER"] if pos == (tx, ty) else go((tx, ty))
                    break

            if act is None and carrying > 0:
                act = ["DROP"] if on_shed else go(nearest_shed())

            actions.append(act or ["PASS"])

        return {"farmer": actions[0], "hands": actions[1:], "market": market[:10]}

    return agent


agent = make_agent()
