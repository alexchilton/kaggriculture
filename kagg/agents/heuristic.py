"""Heuristic agent: many hands, wheat everywhere, sell continuously.

Deliberately self-contained -- no `kagg` imports -- so this same file can be loaded by the
arena, by `kaggle_environments`, or submitted as-is.

Strategy comes from the measured economics in `docs/economics_q5_findings.md`:

- **Wheat, not premium crops.** 28 units/tile/season against strawberry's 6, and wheat's market
  is nearly glut-proof (`above_func=log`): 2800 units still clears about $19/unit. Premium crops
  look better per unit and are far worse per tile.
- **Labour is cheap but NOT free, and the economics doc oversold it.** Hire cost is
  `fib(n)` for the n-th hire *and it resets every morning*, so you pay it 30 times. Eight hands
  is $54/day, about $1.6k a season. Fourteen hands is $986/day -- roughly $29.6k a season, which
  exceeds what the extra labour earns. Parameter search moved this from 17 hands down to 8 and
  gained 40%; "labour is nearly free" is only true up to about ten hands.
- **Melon alongside wheat.** Melon measured the best revenue per tile, but its market absorbs
  only ~113 units at half base against a season drain of 140, so only a dozen tiles of it.
- **Stagger the plantings.** The shed holds 100 items overnight and destroys the overflow, so a
  synchronised harvest across many tiles throws most of itself away. Each tile gets a phase and
  only plants on its phase day, which spreads the harvest evenly across the cycle.

Known gaps, all deliberate for a first version: no animals, no fertilizer, no premium crops, no
sell-timing (it sells continuously rather than deferring), and no market denial.
"""

TURNS_PER_DAY = 24
SHED_CAP = 100

# Copied rather than imported so this file stays submittable on its own.
# `ongoing` crops accumulate on the tile and survive harvest; the others clear the tile.
# Base market prices, for judging whether a current price is good or bad.
BASE_PRICE = {
    "WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
    "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100,
}

# Fertilizer doubles an ongoing crop's lifetime output, because the cap counts production
# *events* and a fertilized event grants 2 units instead of 1. Non-ongoing crops fill their
# watering window faster. Melon gains nothing -- its window already reaches max_yield unaided.
# Measured season yields, plain -> fertilized: wheat 28->42, strawberry 6->12, tomato 8->16.
FERTILIZER_HELPS = ("WHEAT", "CARROT", "STRAWBERRY", "TOMATO")

CROPS = {
    "WHEAT":      {"seed": 10, "first_yield": 2, "ripe_day": 4,  "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield": 2, "ripe_day": 3,  "ongoing": False},
    "MELON":      {"seed": 80, "first_yield": 10, "ripe_day": 12, "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield": 8, "ripe_day": 11, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield": 10, "ripe_day": 16, "ongoing": True},
}

# Everything worth tuning lives here so a search can optimise it without touching the policy.
# See `scripts/tune_heuristic.py`; the values below are the best found so far.
PARAMS = {
    "tiles_per_hand": 14,
    "max_hands": 14,
    "carry_before_drop": 25,
    "seed_buffer": 0,
    # Multiplier on the raw land prices ($1000/$2000/$4000) before we will expand.
    "land_slack": 3.0,
    # Fraction of owned tiles that must be planted before buying more land.
    "productive_gate": 0.8,
    # Stagger plantings across the cycle to spread the harvest. 1 disables staggering.
    "phase_mod": 5,
    # Tile budget per crop, in priority order; whatever is left goes to wheat.
    #
    # Strawberry is the premium position: a tile yields only 6 units a season, so supply
    # physically cannot reach the town's ~536-unit drain, and the price therefore stays far
    # above base -- observed at $310 against a $120 base in a real ranked match.
    # Melon is the opposite trap. It yields 12 units a tile but its glut curve is `sq`, the
    # harshest in the game, and its market absorbs only ~113 units at half base. Overcommitting
    # crashed it to $7 in that same match.
    # Set to 0 deliberately, against theory. Strawberry *should* be the premium position and a
    # real opponent beat us with it at $310/unit. But measured in mirror matches, every tile
    # given to strawberry made us worse ($31.6k at 0 tiles down to $18.4k at 25). The reason is
    # that this agent cannot exploit it: $100/tile of seed with no revenue for 16 days starves
    # the early game, and the agent sells everything the turn it is harvested, so it dumps
    # strawberry into an unaccumulated market instead of holding for the late scarcity premium.
    # Revisit once deferred selling and a wheat-funded capital ramp exist.
    # Cows: OFF, against the per-tile arithmetic, which said $725/tile and $2116 with CARE
    # versus wheat's $452. Measured against a fixed opponent pool they are net negative --
    # 70% win rate and $33.3k with none, 62% and $23.0k with ten -- and at 16 tiles the agent
    # collapses to $467, a capital death spiral: cows cost $400 each against a $3000 start.
    #
    # The gap between arithmetic and outcome is **routing**, the cost this project dropped as a
    # standalone question. A cow needs HARVEST, FEED, CARE and COLLECT_FERTILIZER each day, and
    # FEED draws from the unit's own inventory, so a keeper must walk to a shed tile, PICKUP
    # wheat, and walk back. That is 4-6 actions plus travel per cow per day against wheat's ~1.5
    # per tile. Per-tile revenue rankings that ignore action cost are not decision-ready.
    #
    # Two implementation bugs were found and fixed before accepting this: pastures were built
    # without checking a $400 cow was affordable (leaving tiles empty while the bank hit $76), and
    # collected fertilizer piled up unused because FERTILIZE always lost the priority contest.
    # Fixing both moved cows=8 from 23% to 37% win rate -- still far below 73% with none.
    #
    # Worth revisiting with animals placed *on* the shed-access tiles, which removes the feed walk
    # entirely, and with a wheat-funded ramp so cows are bought after cashflow exists rather than
    # out of starting capital. The machinery is all here and works; only the count is zero, and the
    # RL action space includes it so a policy can rediscover the tradeoff.
    "cow_tiles": 0,
    "strawberry_tiles": 0,
    # 25, and the route to that number is a lesson. Against `starter` 25 looked best; in mirror
    # matches 12 looked best; against a fixed pool judged on win rate 25 is best again (77% vs
    # 67%). Mirror optimises the symmetric case -- what is best if *both* play it -- which is not
    # what an Elo ladder rewards. A best response to a field is the thing to measure.
    "melon_tiles": 25,
    # Do not sell below this fraction of base price -- hold and let town drain lift it back.
    # A ranked replay showed the agent dumping melon at $7 against a $250 base.
    "sell_floor_frac": 0.55,
    # Do not spend seed on a crop whose price has collapsed; plant wheat instead. The same
    # replay showed $80 melon seeds being bought while melon sold for $25.
    "plant_floor_frac": 0.45,
    # From this day on, sell everything regardless of price -- unsold stock scores nothing.
    "endgame_day": 28,
    # Apply fertilizer only when it is free (collected from animals). Buying at $100 does not pay:
    # one application covers 3 days of one tile, worth about +$30 of wheat.
    "use_fertilizer": True,
    # Crop that fills every tile not claimed above. Wheat has the deepest market, but carrot
    # yields 29 units/tile/season against wheat's 28 at a $35 base against $25, and a real
    # opponent beat us using 16 carrot tiles and nothing else. Its season drain is 410, so
    # roughly 14 tiles saturates it -- past that the sqrt glut curve bites.
    "filler_crop": "WHEAT",
    # Cap on how many tiles we actually farm, regardless of how many are unlocked. A real opponent
    # beat us $24,984 to $18,997 using 25 tiles against our 50: spreading thin costs labour and
    # seed capital without adding output. 100 means no cap.
    "max_tiles": 100,
    # Deferred selling. Town drain runs all season whether or not we sell, so an untouched market
    # drifts into scarcity and price climbs well above base -- strawberry was observed at $310
    # against a $120 base. Selling early spends that premium; holding banks it.
    #
    # The catch, measured: there is no long-term storage. Overnight carry is 100 items and the
    # overflow is destroyed, and a ripe plant decays about a day after maturing. So the only
    # holdable quantity is roughly one shed. This window stops selling for the last few days
    # before the endgame dump, letting drain lift the price on what we are holding.
    "hold_days": 10,
}

LAND_PRICES = [1000, 2000, 4000]
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


def _quadrant_of(x, y, size):
    half = size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _shed_tiles(size):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _step_toward(pos, target):
    """One legal move that reduces Manhattan distance; longer axis first."""
    (x, y), (tx, ty) = pos, target
    dx, dy = tx - x, ty - y
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def _owned_tiles(farm, size):
    """Unlocked tiles, ordered so that consecutive indices are spatially close."""
    out = []
    for y in range(size):
        row = range(size) if y % 2 == 0 else reversed(range(size))
        for x in row:
            if farm["tiles"][y][x] != "LOCKED":
                out.append((x, y))
    return out


def _phase_ok(tile_index, day, p):
    """Whether this tile is allowed to be planted today, for harvest staggering."""
    mod = p["phase_mod"]
    return mod <= 1 or tile_index % mod == day % mod


def _is_animal_index(index, p):
    return index < p["cow_tiles"]


def _crop_for_index(index, p, prices=None):
    """Cows first, then strawberry, then melon, then wheat fills the remainder.

    A crop whose price has collapsed is replaced by wheat: paying $80 for melon seed while melon
    sells for $25 is how the first submitted agent bled money through the back half of the season.
    """
    cows = p["cow_tiles"]
    straw = p["strawberry_tiles"]
    intended = p["filler_crop"]
    if index < cows + straw and index >= cows:
        intended = "STRAWBERRY"
    elif index < cows + straw + p["melon_tiles"] and index >= cows + straw:
        intended = "MELON"
    if intended in ("MELON", "STRAWBERRY", "TOMATO") and prices:
        if prices.get(intended, 0) < p["plant_floor_frac"] * BASE_PRICE[intended]:
            return p["filler_crop"]
    return intended


COW_COST = 400


def _animal_job(tile, carried, shed, can_afford_cow=True):
    """What an animal tile needs. Returns (op, needs) where `needs` is an item to be carrying."""
    if tile is None:
        # Only claim the tile if a cow to put on it is actually affordable; an empty pasture is a
        # tile removed from production for nothing.
        return ("BUILD_PASTURE", None) if can_afford_cow else None
    if not isinstance(tile, dict):
        return None
    if tile.get("kind") == "WEED":
        return ("DIG", None)
    if "animal" not in tile:
        if tile.get("kind") != "PASTURE":
            return None
        if carried.get("COW", 0) >= 1:
            return ("PLACE", None)
        return ("PLACE", "COW") if shed.get("COW", 0) >= 1 else None

    # Order matters: harvest first so max_held never blocks production, then feed to keep the
    # animal alive, then CARE (which doubles the next yield), then take the free fertilizer.
    if tile.get("yield_units", 0) > 0:
        return ("HARVEST", None)
    if not tile.get("fed_today"):
        return ("FEED", None) if carried.get("WHEAT", 0) >= 1 else ("FEED", "WHEAT")
    if not tile.get("cared_today"):
        return ("CARE", None)
    if tile.get("fertilizer_available"):
        return ("COLLECT_FERTILIZER", None)
    return None


def _job_for_tile(tile, day, crop, has_seed, phase_ok, fertilizer_available=False):
    """What this tile needs, or None. Ordered by value: harvest, then water, then plant."""
    if tile is None:
        return "PLANT" if (has_seed and phase_ok) else None
    if not isinstance(tile, dict):
        return None
    kind = tile.get("kind")
    if kind == "WEED":
        return "DIG"
    if kind != "PLANT":
        return None

    spec = CROPS[tile["crop"]]
    age = day - tile["planted_day"]
    units = tile.get("yield_units", 0)
    # Ongoing crops are taken eagerly -- yield_units is a holding cap, so leaving units on the
    # tile forfeits the next production event. Others are held until the watering window closes,
    # because harvesting clears the tile and ends the cycle.
    ripe = age >= spec["first_yield"] if spec["ongoing"] else age >= spec["ripe_day"]
    if units > 0 and ripe:
        return "HARVEST"
    if not tile.get("watered_today"):
        return "WATER"
    # Fertilizer only pays on a watered day, so it comes after WATER, and only for crops that
    # actually respond. `fertilized_until_day` is inclusive of today.
    if fertilizer_available and tile["crop"] in FERTILIZER_HELPS:
        if tile.get("fertilized_until_day", -1) < day:
            return "FERTILIZE"
    return None


def _play(obs, p):
    size = len(obs["farms"][obs.get("player", 0)]["tiles"])
    me = obs.get("player", 0)
    farm = obs["farms"][me]
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    private = obs.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    seeds = private.get("seeds", {}) or {}
    inventories = private.get("inventories", [{}]) or [{}]
    money = farm["money"]

    tiles = _owned_tiles(farm, size)[: p["max_tiles"]]
    shed_tiles = _shed_tiles(size)
    unlocked = len(farm.get("unlocked_quadrants", ["NW"]))

    prices = (obs.get("market", {}) or {}).get("prices", {}) or {}

    # ---- market orders -------------------------------------------------------------------
    market = []

    # Hire at the start of the day; cost is fib(n) so a full crew is a rounding error.
    # Labour is nearly free: 14 hands cost about $1000 for the day and buy 336 actions, against
    # actions that move $20+ of wheat. The binding cost is routing, not the wage.
    if hour in (0, 1):
        target = min(p["max_hands"],
                     max(2, -(-len(tiles) // p["tiles_per_hand"])))
        already = len(farm.get("hands", []))
        for _ in range(max(0, min(5, target - already))):
            market.append(["HIRE"])

    # Price-aware selling. Holding is only free while the shed has room, so once it is nearly
    # full sell anyway -- losing goods to the nightly overflow is worse than a poor price.
    held = sum(shed.values())
    shed_pressed = held >= SHED_CAP * 0.8
    endgame = day >= p["endgame_day"]
    # Inside the hold window we sit on stock and let town drain lift the price, unless the shed is
    # nearly full -- losing goods to the nightly overflow is worse than a mediocre price.
    holding = (not endgame) and day >= p["endgame_day"] - p["hold_days"]
    for item, n in sorted(shed.items()):
        if n <= 0:
            continue
        if item == "FERTILIZER" and p["use_fertilizer"] and not endgame:
            continue  # worth more applied to wheat than sold
        # Hold back feed: an unfed cow escapes after two days and the pasture is wasted.
        sellable = n
        if item == "WHEAT" and not endgame and p["cow_tiles"]:
            sellable = max(0, n - 3 * p["cow_tiles"])
        if sellable <= 0:
            continue
        if holding and not shed_pressed:
            continue
        good_price = prices.get(item, 0) >= p["sell_floor_frac"] * BASE_PRICE.get(item, 0)
        if good_price or shed_pressed or endgame:
            market.append(["SELL", item, sellable])

    # Seeds for the plantings that are actually due, per crop, plus a buffer.
    due = {}
    for i, (x, y) in enumerate(tiles):
        if farm["tiles"][y][x] is None and _phase_ok(i, day, p):
            crop = _crop_for_index(i, p, prices)
            due[crop] = due.get(crop, 0) + 1
    for crop, n in sorted(due.items()):
        want = max(0, n + p["seed_buffer"] - seeds.get(crop, 0))
        if want and money > CROPS[crop]["seed"] * want * 2:
            market.append(["BUY_SEED", crop, want])

    # Cows, one at a time, only when a pasture is standing empty and there is real slack.
    empty_pastures = sum(
        1 for i, (x, y) in enumerate(tiles)
        if _is_animal_index(i, p)
        and isinstance(farm["tiles"][y][x], dict)
        and farm["tiles"][y][x].get("kind") == "PASTURE"
        and "animal" not in farm["tiles"][y][x]
    )
    if empty_pastures > shed.get("COW", 0) and money > 900:
        market.append(["BUY_ANIMAL", "COW", 1])

    # Only expand once the current land is genuinely productive. Buying early starves seed
    # and wage spending, which was measured leaving 18 tiles idle all season.
    planted = sum(
        1 for (x, y) in tiles
        if isinstance(farm["tiles"][y][x], dict) and farm["tiles"][y][x].get("kind") == "PLANT"
    )
    productive = planted / max(1, len(tiles))
    if (unlocked <= len(LAND_PRICES)
            and money >= LAND_PRICES[unlocked - 1] * p["land_slack"]
            and productive > p["productive_gate"]):
        market.append(["BUY_LAND"])

    # maxMarketOrdersPerTurn is 10 and extras are silently dropped, so sells come first.
    market = market[:10]

    # ---- unit assignment -----------------------------------------------------------------
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm.get("hands", [])]

    # Only ever spend fertilizer we were given for free by animals.
    fert_available = p["use_fertilizer"] and (
        shed.get("FERTILIZER", 0) > 0
        or any(inv.get("FERTILIZER", 0) > 0 for inv in inventories)
    )

    jobs = {}
    want_crop = {}
    needs_item = {}   # tile -> item the acting unit must be carrying
    for i, (x, y) in enumerate(tiles):
        tile = farm["tiles"][y][x]
        if _is_animal_index(i, p):
            # Any unit could be asked to fetch feed, so judge the job against an empty hand and
            # let the carrier check below decide who can actually do it.
            found = _animal_job(tile, {}, shed, can_afford_cow=money > COW_COST * 2)
            if found:
                jobs[(x, y)] = found[0]
                if found[1]:
                    needs_item[(x, y)] = found[1]
            continue
        crop = _crop_for_index(i, p, prices)
        job = _job_for_tile(
            tile, day, crop,
            has_seed=seeds.get(crop, 0) > 0,
            phase_ok=_phase_ok(i, day, p),
            fertilizer_available=fert_available,
        )
        if job:
            jobs[(x, y)] = job
            want_crop[(x, y)] = crop
            if job == "FERTILIZE":
                needs_item[(x, y)] = "FERTILIZER"

    actions = []
    claimed = set()
    planned = {}   # crop -> plants already requested this turn
    for unit_idx, pos in enumerate(positions):
        carried = inventories[unit_idx] if unit_idx < len(inventories) else {}
        carrying = sum(carried.values())

        # Full hands go to the shed, otherwise the nightly drop destroys the overflow.
        if carrying >= p["carry_before_drop"]:
            if pos in shed_tiles:
                actions.append(["DROP"])
                continue
            nearest = min(shed_tiles, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
            actions.append([_step_toward(pos, nearest)])
            continue

        candidates = [t for t in jobs if t not in claimed]
        if not candidates:
            actions.append(["DROP"] if carrying and pos in shed_tiles else ["PASS"])
            continue

        target = min(candidates, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
        op = jobs[target]

        # A unit already carrying fertilizer should spend it rather than walk past tiles that want
        # it: fertilizer left in the shed overnight is wasted capital, and it was measured piling
        # up to 7 units unused because FERTILIZE always lost the priority contest.
        if carried.get("FERTILIZER", 0) > 0:
            fert_targets = [t for t in candidates if jobs[t] == "FERTILIZE"]
            if fert_targets:
                target = min(fert_targets, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
                op = jobs[target]

        # FEED and PLACE draw from the unit's own inventory, not the shed, and that inventory is
        # emptied every night. So a unit assigned one of those must first collect the item from a
        # shed-access tile.
        required = needs_item.get(target)
        if required and carried.get(required, 0) < 1:
            if pos in shed_tiles:
                if shed.get(required, 0) >= 1:
                    claimed.add(target)
                    take = {"WHEAT": 6, "FERTILIZER": 4}.get(required, 1)
                    actions.append(["PICKUP", required, take])
                    continue
                actions.append(["PASS"])
                continue
            nearest = min(shed_tiles, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
            actions.append([_step_toward(pos, nearest)])
            continue

        # PLANT is atomically validated per crop: if requests exceed seeds held, ALL plant
        # requests for that crop are dropped. So never ask for more than we hold.
        crop = want_crop.get(target)
        if op == "PLANT" and planned.get(crop, 0) >= seeds.get(crop, 0):
            actions.append(["PASS"])
            continue

        claimed.add(target)
        if pos == target:
            if op == "PLANT":
                actions.append(["PLANT", crop])
                planned[crop] = planned.get(crop, 0) + 1
            elif op == "PLACE":
                actions.append(["PLACE", "COW"])
            else:
                actions.append([op])
        else:
            actions.append([_step_toward(pos, target)])

    return {"farmer": actions[0], "hands": actions[1:], "market": market}


def make_agent(overrides=None):
    """An agent closure bound to its own parameters.

    Lets several parameter sets play each other in one process, which is what an opponent pool
    and mirror-match tuning both need. `PARAMS` is captured by reference when no overrides are
    given, so the tuner can still mutate it in place.
    """
    params = PARAMS if not overrides else {**PARAMS, **overrides}

    def _agent(obs, config=None):
        return _play(obs, params)

    return _agent


def agent(obs, config=None):
    """Module-level entry point, as `kaggle_environments` and the Kaggle runtime expect."""
    return _play(obs, PARAMS)
