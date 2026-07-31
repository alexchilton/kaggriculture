"""Contrarian: a compact, opponent-reading, late-selling farm.

Deliberately self-contained -- no `kagg` imports -- so this file can be loaded by the arena
from a path, by `kaggle_environments`, or submitted as-is.

**Why this agent exists.** `kagg/arena/pool.py` claims eight competing strategies, but every
member is `heuristic.make_agent()` with different dials: same tile ordering, same hiring curve,
same job priorities, same sell cadence. The pool therefore tests robustness to *crop mix* and
nothing else, while `docs/experiment_log.md` section 7 records that the opponents which actually
beat us on the ladder differed in **how** they played. This agent shares no code and no decision
rule with the heuristic. Four things about it are structurally different, and each is taken from a
measurement already in this repo:

1. **It reads the opponent's board.** `docs/competition_brief.md` records that both farms are
   fully visible -- tiles, crop, `planted_day` -- and only sheds are private. Nothing in the pool
   uses that. Melon is winner-take-all: `MARKET_PARAMS["MELON"]` has `above_func="sq"` with
   `above_target=3.60` and `T=300`, so amp is 0.01 and the price hits the floor about 158 units
   above `I0`. Selling 100 melon from `I0` earns ~$21.7k; selling the *next* 100 earns ~$4.8k.
   So committing tiles to melon against a melon opponent is the worst move on the board and
   committing against a melon-free opponent is the best. That is a branch no fixed dial can
   express, and `experiment_log.md` section 5 records `melon_heavy` as the one matchup the
   heuristic never solved (30% win rate). This agent takes melon only when the opponent has left
   it alone, and otherwise takes strawberry -- which `docs/economics_q5_findings.md` measures as
   needing **89 tiles to saturate town demand**, i.e. physically uncontestable, and which a real
   ladder opponent beat us with at $310/unit.

2. **It farms a compact disc around the shed and buys land for access, not for area.**
   `competition_brief.md` calls routing "a first-class cost"; `economics_q5_findings.md` closes
   by naming routing the highest-value unknown; and CLAUDE.md records that cows lost despite
   winning on per-tile revenue *because* of routing. Tiles are taken in order of Manhattan
   distance to the nearest shed-access tile and capped, so buying a quadrant mostly buys a second
   shed-access tile and shorter walks rather than more land. The cited replay where an opponent
   won $24,984 to $18,997 on 25 tiles against our 50 is the same lesson from the other side.

3. **It waters before it harvests on the last day of the window.** `_apply_unit_action`'s WATER
   branch grants yield only while `window_start <= age <= max_yield_day`, and HARVEST on a
   non-ongoing crop clears the tile. Harvesting first on day `max_yield_day` therefore throws away
   that day's unit. The heuristic checks HARVEST before WATER. Wheat's measured 28 units/season is
   3.5 per planting against a reachable 4.

4. **It holds per product against a price floor, not on a global calendar.** The heuristic's
   `hold_days` stops *all* selling for a fixed window. Here wheat -- deep market, `above_func=log`,
   still $18 at 2800 units glutted -- is sold continuously for cashflow, while the premium crop is
   held until town drain has lifted its price past a floor taken from the "price at zero player
   sales" column of `economics_q5_findings.md`. The floor drips the stock out instead of dumping
   it, which also keeps the 100-item shed from destroying incoming wheat overnight.

**Deliberate omissions.** No animals (measured net negative in `experiment_log.md` section 5, and
the routing fix they need is a different agent again), no fertilizer, no carrot.
"""

TURNS_PER_DAY = 24
SHED_CAP = 100

# Copied from `reference/kaggriculture.py` rather than imported, so this file stays submittable.
BASE_PRICE = {
    "WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120, "MELON": 250,
    "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100,
}

CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2,  "max_yield_day": 4,  "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield_day": 2,  "max_yield_day": 3,  "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield_day": 8,  "max_yield_day": 8,  "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "ongoing": True},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "ongoing": False},
}

LAND_PRICES = [1000, 2000, 4000]
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
MARKET_I0 = 10000

PARAMS = {
    # Farm only the tiles closest to the shed. 30 against the board's 100 is the "concentrated
    # farm" position: a ladder opponent beat us $24,984 to $18,997 on 25 tiles against our 50.
    "max_tiles": 30,
    # Hands are cheap up to about eight -- fib(0..7) sums to $54/day, ~$1.6k a season -- and a
    # compact farm needs fewer of them because each unit walks less per job.
    "max_hands": 8,
    "tiles_per_hand": 4,
    # Drop often: SELL draws from the shed, not from a unit's hands, so cargo held in hand is
    # cargo that cannot be sold. Trips are short on a compact farm.
    "carry_before_drop": 10,
    # Wheat's cycle is exactly `max_yield_day` = 4 days, so a mod-4 phase makes every tile
    # replant on the same day it is harvested and spreads the harvest evenly across the cycle.
    "phase_mod": 4,
    "filler_crop": "WHEAT",
    # Tiles committed to the premium crop, once chosen. Melon is capped near the 11.7 tiles that
    # `economics_q5_findings.md` measures as saturating its 140-unit season drain; strawberry is
    # not capped by saturation (89 tiles to saturate) but by seed capital and shed room.
    "premium_tiles": {"MELON": 12, "STRAWBERRY": 18},
    # Melon is judged contested if any of these fire. Market inventory is used as well as the
    # opponent's tiles because inventory is a durable record that somebody has already sold, and
    # it survives the opponent's tile being cleared by the harvest.
    "melon_opp_tiles": 5,
    "melon_glut_units": 30,
    # Never spend the last of the bank on premium seed; a strawberry tile pays nothing for ten
    # days and the heuristic's own docstring blames exactly this for its strawberry failure.
    "premium_reserve": 1200,
    "premium_seed_batch": 4,
    # Hold the premium crop until town drain has lifted its price this far. Reference points are
    # the measured price at zero player sales in `economics_q5_findings.md`: strawberry $314,
    # melon $293, tomato $109. These floors sit below those, so they are reached partway through
    # the season and the stock drips out instead of arriving all at once.
    "premium_floor": {"STRAWBERRY": 220, "MELON": 275, "TOMATO": 95, "CARROT": 30},
    # Wheat funds the ramp, so it is sold whenever the price is not actively bad.
    "staple_floor_frac": 0.8,
    # Shed is 100 items and the overflow is destroyed at DROP and again overnight. Past these
    # fractions the floors are ignored, because a bad price beats a destroyed crop.
    "shed_pressure": 0.70,
    "shed_panic": 0.88,
    # Front-running. If the opponent is about to bring this many units of something we hold to
    # market within `front_run_lead` days, sell now: price is a ladder over cumulative inventory
    # and the first seller takes the top of it.
    "front_run_units": 18,
    "front_run_lead": 2,
    "land_slack": 2.5,
    "productive_gate": 0.7,
    "endgame_day": 27,
    # Planting late in the day risks the tile: `_new_plant` sets `consecutive_unwatered` to 1, so
    # a tile planted and not watered the same day is a weed by morning.
    "plant_cutoff_hour": 20,
}


def _shed_tiles(size):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _step_toward(pos, target):
    (x, y), (tx, ty) = pos, target
    dx, dy = tx - x, ty - y
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def _shed_distance(pos, shed):
    return min(abs(pos[0] - t[0]) + abs(pos[1] - t[1]) for t in shed)


def _farm_tiles(farm, size, max_tiles):
    """Unlocked tiles, nearest the shed first.

    This is the routing decision. The heuristic scans rows and takes a prefix, which spreads its
    farm across the whole quadrant; taking the nearest tiles instead means every cargo trip is
    short, and it means buying a quadrant is mostly buying a second shed-access tile.
    """
    shed = _shed_tiles(size)
    out = []
    for y in range(size):
        for x in range(size):
            if farm["tiles"][y][x] != "LOCKED":
                out.append((_shed_distance((x, y), shed), y, x))
    out.sort()
    return [(x, y) for _, y, x in out[:max_tiles]]


def _opponent_crops(opp):
    """Tiles the opponent currently has planted, per crop, and units ripening soon.

    Only the board is readable -- their shed is private -- so this counts standing production,
    which is what will hit the market next.
    """
    counts = {}
    if not opp:
        return counts
    for row in opp["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = tile.get("crop")
                counts[crop] = counts.get(crop, 0) + 1
    return counts


def _opponent_incoming(opp, day, lead):
    """Units of each product the opponent can bring to market within `lead` days."""
    incoming = {}
    if not opp:
        return incoming
    for row in opp["tiles"]:
        for tile in row:
            if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
                continue
            crop = tile.get("crop")
            spec = CROPS.get(crop)
            if not spec:
                continue
            age = day - tile.get("planted_day", day)
            if spec["ongoing"]:
                units = tile.get("yield_units", 0) if age + lead >= spec["first_yield_day"] else 0
            else:
                units = 6 if age + lead >= spec["max_yield_day"] else 0
            if units:
                incoming[crop] = incoming.get(crop, 0) + units
    return incoming


def _premium_crop(opp_counts, market_inventory, p):
    """Melon while the opponent leaves it alone, strawberry once they do not.

    Melon's glut curve is `sq`, the harshest in the game: about 158 units above `I0` and the price
    is on the floor. Two committed players cannot both be paid for it, so this is a genuine
    either/or rather than a weighting.
    """
    melon_inv = market_inventory.get("MELON", MARKET_I0)
    contested = (
        opp_counts.get("MELON", 0) >= p["melon_opp_tiles"]
        or melon_inv >= MARKET_I0 + p["melon_glut_units"]
    )
    return "STRAWBERRY" if contested else "MELON"


def _crop_plan(tiles, premium, p):
    """Index -> crop. Premium takes the tiles furthest from the shed.

    Wheat is the crop with cargo: it is harvested every four days and every harvest is a walk to
    the shed. Strawberry is watered daily and harvested twice in its life. So the crop that walks
    gets the short walk.
    """
    n = len(tiles)
    n_premium = min(p["premium_tiles"].get(premium, 0), max(0, n - 6))
    first_premium = n - n_premium
    return [p["filler_crop"] if i < first_premium else premium for i in range(n)]


def _tile_job(tile, day, crop, has_seed, phase_ok, can_plant):
    """What this tile needs, or None.

    WATER outranks HARVEST inside the watering window, which is the reverse of the heuristic and
    is worth a unit per cycle: `_apply_unit_action` grants the watering bonus while
    `window_start <= age <= max_yield_day`, and HARVEST on a non-ongoing crop clears the tile.
    """
    if tile is None:
        return "PLANT" if (has_seed and phase_ok and can_plant) else None
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
    watered = tile.get("watered_today")

    if spec["ongoing"]:
        if units > 0 and age >= spec["first_yield_day"]:
            return "HARVEST"
        return None if watered else "WATER"

    if not watered and age <= spec["max_yield_day"]:
        return "WATER"
    if units > 0 and age >= spec["max_yield_day"]:
        return "HARVEST"
    return None if watered else "WATER"


def _sell_orders(shed, prices, opp_incoming, day, p):
    """Per-product hold, not a global calendar."""
    held = sum(shed.values())
    pressed = held >= SHED_CAP * p["shed_pressure"]
    panic = held >= SHED_CAP * p["shed_panic"]
    endgame = day >= p["endgame_day"]

    orders = []
    for item, n in sorted(shed.items(), key=lambda kv: (-kv[1], kv[0])):
        if n <= 0 or item not in BASE_PRICE:
            continue
        price = prices.get(item, 0)
        if endgame or panic:
            orders.append(["SELL", item, n])
            continue
        floor = p["premium_floor"].get(item)
        if floor is None:
            if price >= p["staple_floor_frac"] * BASE_PRICE[item] or pressed:
                orders.append(["SELL", item, n])
            continue
        # Front-run: the opponent is about to glut this good, and the price ladder pays whoever
        # sells into the shallow end of it first.
        crowded = opp_incoming.get(item, 0) >= p["front_run_units"]
        if price >= floor or crowded or pressed:
            orders.append(["SELL", item, n])
    return orders


def _play(obs, p):
    farms = obs.get("farms") or []
    me = obs.get("player", 0)
    if not farms or me >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}

    farm = farms[me]
    size = len(farm["tiles"])
    opp = farms[1 - me] if len(farms) > 1 else None
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    private = obs.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    seeds = private.get("seeds", {}) or {}
    inventories = private.get("inventories", [{}]) or [{}]
    money = farm["money"]
    market = obs.get("market", {}) or {}
    prices = market.get("prices", {}) or {}
    inventory = market.get("inventory", {}) or {}

    tiles = _farm_tiles(farm, size, p["max_tiles"])
    shed_tiles = _shed_tiles(size)
    unlocked = len(farm.get("unlocked_quadrants", ["NW"]))

    premium = _premium_crop(_opponent_crops(opp), inventory, p)
    plan = _crop_plan(tiles, premium, p)
    incoming = _opponent_incoming(opp, day, p["front_run_lead"])

    # ---- market orders -------------------------------------------------------------------
    orders = []

    # Hands are cleared every night, so the crew is rebuilt each morning. Sized to the work on a
    # compact farm rather than to the board: ~30 tiles is ~60 jobs a day against 24 actions per
    # unit, so six or seven units is enough and fib() keeps that under $30/day.
    if hour == 0:
        target = min(p["max_hands"], max(3, -(-len(tiles) // p["tiles_per_hand"])))
        for _ in range(max(0, target - len(farm.get("hands", [])))):
            orders.append(["HIRE"])

    orders.extend(_sell_orders(shed, prices, incoming, day, p))

    can_plant = hour <= p["plant_cutoff_hour"]
    due = {}
    if can_plant:
        for i, (x, y) in enumerate(tiles):
            if farm["tiles"][y][x] is None and (i % p["phase_mod"] == day % p["phase_mod"]):
                due[plan[i]] = due.get(plan[i], 0) + 1
    for crop, want_n in sorted(due.items()):
        want = max(0, want_n - seeds.get(crop, 0))
        if not want:
            continue
        cost = CROPS[crop]["seed"]
        if crop == p["filler_crop"]:
            if money > cost * want * 2:
                orders.append(["BUY_SEED", crop, want])
        else:
            want = min(want, p["premium_seed_batch"])
            if money - cost * want >= p["premium_reserve"]:
                orders.append(["BUY_SEED", crop, want])

    planted = sum(
        1 for (x, y) in tiles
        if isinstance(farm["tiles"][y][x], dict) and farm["tiles"][y][x].get("kind") == "PLANT"
    )
    if (unlocked <= len(LAND_PRICES)
            and money >= LAND_PRICES[unlocked - 1] * p["land_slack"]
            and planted / max(1, len(tiles)) > p["productive_gate"]):
        orders.append(["BUY_LAND"])

    orders = orders[:10]

    # ---- unit assignment -----------------------------------------------------------------
    positions = [tuple(farm["farmer"])] + [tuple(h) for h in farm.get("hands", [])]

    jobs = {}
    want_crop = {}
    for i, (x, y) in enumerate(tiles):
        crop = plan[i]
        job = _tile_job(
            farm["tiles"][y][x], day, crop,
            has_seed=seeds.get(crop, 0) > 0,
            phase_ok=(i % p["phase_mod"] == day % p["phase_mod"]),
            can_plant=can_plant,
        )
        if job:
            jobs[(x, y)] = job
            want_crop[(x, y)] = crop

    actions = []
    claimed = set()
    planned = {}
    for unit_idx, pos in enumerate(positions):
        carried = inventories[unit_idx] if unit_idx < len(inventories) else {}
        carrying = sum(carried.values())

        if carrying >= p["carry_before_drop"]:
            if pos in shed_tiles:
                actions.append(["DROP"])
            else:
                nearest = min(shed_tiles, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
                actions.append([_step_toward(pos, nearest)])
            continue

        candidates = [t for t in jobs if t not in claimed]
        if not candidates:
            actions.append(["DROP"] if carrying and pos in shed_tiles else ["PASS"])
            continue

        target = min(candidates, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
        op = jobs[target]

        # PLANT is validated atomically per crop: if requests exceed seeds held, every PLANT for
        # that crop is dropped. So never ask for more than we hold.
        crop = want_crop.get(target)
        if op == "PLANT" and planned.get(crop, 0) >= seeds.get(crop, 0):
            actions.append(["DROP"] if carrying and pos in shed_tiles else ["PASS"])
            continue

        claimed.add(target)
        if pos == target:
            if op == "PLANT":
                actions.append(["PLANT", crop])
                planned[crop] = planned.get(crop, 0) + 1
            else:
                actions.append([op])
        else:
            actions.append([_step_toward(pos, target)])

    return {"farmer": actions[0], "hands": actions[1:], "market": orders}


def make_agent(overrides=None):
    """An agent closure bound to its own parameters, so variants can play each other."""
    params = PARAMS if not overrides else {**PARAMS, **overrides}

    def _agent(obs, config=None):
        return _play(obs, params)

    return _agent


def agent(obs, config=None):
    """Module-level entry point, as `kaggle_environments` and the Kaggle runtime expect."""
    return _play(obs, PARAMS)
