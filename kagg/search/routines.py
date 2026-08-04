"""Macro-routines: the chain is the unit of search, not the sub-action.

**Why this module exists.** A sub-action search cannot find the animal economy, and that is a
structural fact rather than a tuning problem. Two mechanics close the door:

- `consecutive_unfed >= 2` escapes the animal (`kaggriculture.py:786`), so buying one you will not
  feed every day is a *deterministic* loss of $300-$500, not a bad expectation.
- FEED is illegal until an animal is on the board, unfed, with a unit standing on it carrying wheat
  (`jax_masks.py:93`), so a policy samples FEED from a distribution where it has zero mass.

Every prefix of the chain is therefore money-negative and every complete chain needs ~15 coordinated
edits at specific tiles on specific days. A hill-climber selecting on money rejects step one forever;
PPO learns to stop buying animals, which re-masks FEED and closes the loop. Both failures are the
same wall.

The fix is not a better optimiser. It is a representation in which a partial chain **cannot be
expressed**. A routine emits the whole chain or nothing, so the valley is not crossed -- it is not in
the space. What the search then owns is *which* routine, *where*, *when* and *how many*, which is
strategy, while correctness lives in the decoder.

**The ranch cell.** The four shed-access tiles are `(4,4) (5,4) (4,5) (5,5)` -- the inner corners
around the shed. PICKUP, DROP and shed-PLACE test only shed-adjacency, and FEED/CARE/HARVEST test
only that the unit stands on the animal's tile. Put the pen *on* a shed-access tile and one unit can
run the entire loop -- draw feed, feed, care, harvest, deposit -- **without ever moving**, in 5 of
the day's 24 turns. That matters beyond convenience: a unit's tile is the cumulative sum of its
movement ops, so in an open-loop script one edited step silently invalidates every later op. A
zero-movement routine has no such coupling, which is what makes it a safe unit of search.

**Land is the gate.** Only `(4,4)` is in NW, the sole quadrant unlocked at the start; the other three
cells begin LOCKED. `LAND_ORDER` is `['NE','SW','SE']` at `[1000, 2000, 4000]`, bought in sequence,
so cell `(5,5)` costs $7,000 of land to reach. This is also why an agent that never buys land plays
the whole season on 25 tiles of 100.
"""

import numpy as np

# ---------------------------------------------------------------------------
# The reference's own tables, mirrored. Kept as literals rather than imported so this module has no
# dependency on `reference/`, and pinned by `tests/test_routines.py` against the geometry helpers.
# ---------------------------------------------------------------------------

OP_NAMES = [
    "PASS", "NORTH", "SOUTH", "EAST", "WEST",
    "WATER", "HARVEST", "PLANT", "DIG",
    "PICKUP", "DROP", "PLACE", "FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE",
    "BUILD_COOP", "BUILD_PASTURE",
]
OP = {n: i for i, n in enumerate(OP_NAMES)}

PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
CROPS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]
ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]
ITEMS = PRODUCTS + ANIMAL_NAMES          # the `unit_item` domain, 12 wide

ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
STRUCTURE_OP = {"COOP": OP["BUILD_COOP"], "PASTURE": OP["BUILD_PASTURE"]}

LAND_ORDER = ["NE", "SW", "SE"]
LAND_PRICES = [1000, 2000, 4000]

BOARD_SIZE = 10
TURNS_PER_DAY = 24
SEASON_DAYS = 30
T_DEFAULT = 719          # the recorder's length: 30 days of 24 turns, minus the unplayed last turn
U_DEFAULT = 24


def quadrant_of(x, y, board_size=BOARD_SIZE):
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def shed_access_tiles(board_size=BOARD_SIZE):
    """The four inner-corner tiles around the shed, in the reference's NWSE order."""
    half = board_size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


SPAWN = (4, 4)          # `_default_spawn`: the only shed-access tile inside the starting quadrant


def spawn_order(board_size=BOARD_SIZE, n=8):
    """Unit index -> the tile that unit spawns on at dawn.

    Mirrors `_spawn_hand`: minimum occupancy over the shed-access tiles, ties broken by NWSE index.
    The farmer occupies `(4,4)` first, so hands land on `(5,4)`, `(4,5)`, `(5,5)` in that order --
    **exactly one per ranch cell, with no movement required by any of them.**

    Note it does *not* filter for unlocked quadrants, so a hand really does spawn on a LOCKED tile.
    It can still PICKUP and DROP there (those test only shed-adjacency) but cannot BUILD, because a
    LOCKED tile is the string `"LOCKED"` rather than `None`.
    """
    tiles = shed_access_tiles(board_size)
    occ = {t: 0 for t in tiles}
    occ[tuple(SPAWN)] += 1
    order = [tuple(SPAWN)]
    for _ in range(n):
        best = min(occ.items(), key=lambda kv: (kv[1], tiles.index(kv[0])))[0]
        order.append(best)
        occ[best] += 1
    return order


def unit_for_cell(tile, board_size=BOARD_SIZE):
    """The lowest unit index that spawns on `tile`.

    Also the number of hands that must be hired that day to bring it into existence, since hands are
    dismissed every dawn (`kaggriculture.py:849`) and unit `k` is the `k`-th hand.
    """
    for i, t in enumerate(spawn_order(board_size)):
        if t == tuple(tile):
            return i
    raise ValueError(f"{tile} is not a spawn tile")


def land_purchases_for(tile, board_size=BOARD_SIZE):
    """How many sequential BUY_LAND orders are needed before `tile` is unlocked.

    `_do_buy_land` ignores its caller's wishes and unlocks `LAND_ORDER[n_already_bought]`, so
    reaching SE costs all three purchases whether or not NE and SW are wanted.
    """
    q = quadrant_of(*tile, board_size=board_size)
    if q == "NW":
        return 0
    return LAND_ORDER.index(q) + 1


class Script:
    """A mutable action tape: `[T, U]` unit ops plus the per-turn market vector.

    Deliberately plain arrays rather than a builder DSL. The optimiser mutates *plans*, expands them
    through the routines below into one of these, and hands the arrays straight to the simulator --
    the same arrays `scripts/build_script_submission.py` already turns into a verified submission.
    """

    def __init__(self, T=T_DEFAULT, U=U_DEFAULT):
        self.T, self.U = T, U
        self.unit_op = np.zeros((T, U), np.int64)      # 0 == PASS
        self.unit_crop = np.zeros((T, U), np.int64)
        self.unit_item = np.zeros((T, U), np.int64)
        self.unit_qty = np.zeros((T, U), np.int64)
        self.sell = np.zeros((T, len(PRODUCTS)), np.int64)
        self.buy_seed = np.zeros((T, len(CROPS)), np.int64)
        self.buy_product = np.zeros((T, len(PRODUCTS)), np.int64)
        self.buy_animal = np.zeros((T, len(ANIMAL_NAMES)), np.int64)
        self.hire = np.zeros(T, np.int64)
        self.buy_land = np.zeros(T, np.int64)

    def arrays(self):
        return {f: getattr(self, f) for f in
                ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
                 "buy_product", "buy_animal", "hire", "buy_land")}

    def op(self, t, u, name, item=None, qty=0, crop=None):
        """Write one unit op. Out-of-range turns are dropped so a routine may run past the season."""
        if not (0 <= t < self.T):
            return
        self.unit_op[t, u] = OP[name]
        if item is not None:
            self.unit_item[t, u] = ITEMS.index(item)
            self.unit_qty[t, u] = qty
        if crop is not None:
            self.unit_crop[t, u] = CROPS.index(crop)


# ---------------------------------------------------------------------------
# Routines
# ---------------------------------------------------------------------------

def ranch(script, animal, tile, start_day, land_day=0, sell=True, unit=None):
    """Build a pen on `tile`, stock it, and feed it every remaining day of the season.

    Emits the complete chain and nothing partial. There is deliberately no primitive that buys an
    animal without also committing the feed loop that keeps it alive -- that combination is the
    $300-$500 deterministic loss the search must never be able to propose.

    **Everything here is a consequence of the dawn reset** (`kaggriculture.py:847-851`), which
    dismisses every hand, teleports the farmer back to `(4,4)` and resets the hire ladder:

    - The cell determines the unit. `_spawn_hand` is deterministic, so hand `k` lands on the `k`-th
      shed-access tile; running cell `(5,5)` means being unit 3 and hiring three hands. No routine
      ever emits a movement op, which is why the first version -- which walked once, on the start day
      -- silently starved every animal outside `(4,4)`.
    - Those hires repeat **every day**. The Fibonacci ladder resets daily, so three hands cost
      $1+$1+$2 = $4/day, about $120 across a season.
    - Carried inventory is auto-deposited at dusk, so the daily DROP is only needed to get product
      into the shed in time for that day's sell order.

    `land_day` is separate from `start_day` because `_do_buy_land` silently no-ops when money is
    short and the parcels cost $1,000/$2,000/$4,000 in sequence. Funding SE means earning first, so
    when to buy land is a plan parameter, never a default.
    """
    if tuple(tile) not in shed_access_tiles():
        raise ValueError(f"{tile} is not a shed-access tile; the loop would need movement")
    if animal not in ANIMALS:
        raise ValueError(f"unknown animal {animal}")

    info = ANIMALS[animal]
    a_idx = ANIMAL_NAMES.index(animal)
    wheat = PRODUCTS.index("WHEAT")
    prod_idx = PRODUCTS.index(info["product"])
    u = unit_for_cell(tile) if unit is None else unit

    # --- land: every parcel up to and including this cell's quadrant ------
    for k in range(land_purchases_for(tile)):
        t = land_day * TURNS_PER_DAY + k
        if 0 <= t < script.T:
            script.buy_land[t] = 1

    # --- the crew this cell needs, re-hired every dawn --------------------
    # `maximum`, not `+=`: a cell needing 3 hands already provides units 1 and 2 for the nearer
    # cells, so co-located routines must not each add their own.
    for day in range(start_day, SEASON_DAYS):
        t = day * TURNS_PER_DAY
        if u > 0 and t < script.T:
            script.hire[t] = max(int(script.hire[t]), u)

    def day_loop(day, setup):
        """One day on the cell. `setup` prepends build/stock/place before the feed cycle."""
        d = day * TURNS_PER_DAY
        # Order feed a turn ahead of drawing it, so the market has resolved either way.
        script.buy_product[d, wheat] += 1
        t = d + 1
        if setup:
            script.buy_animal[d, a_idx] += 1
            script.op(t, u, "BUILD_PASTURE" if info["structure"] == "PASTURE" else "BUILD_COOP")
            script.op(t + 1, u, "PICKUP", item=animal, qty=1)
            script.op(t + 2, u, "PLACE", item=animal, qty=1)
            t += 3
        script.op(t, u, "PICKUP", item="WHEAT", qty=1)
        script.op(t + 1, u, "FEED")
        # CARE grants +1 yield on the next fed production day, and `pending_care_bonus` accumulates
        # while it waits, capped at `max_held`. One turn a day for roughly double output; it is why
        # CARE correlates +0.441 with money across 312 real leaderboard seats.
        script.op(t + 2, u, "CARE")
        script.op(t + 3, u, "HARVEST")
        script.op(t + 4, u, "DROP")
        if sell:
            # Over-requesting is safe: `_process_market` stops when the shed runs dry. Selling daily
            # is the naive cadence -- it walks our own price down the glut curve -- and the timing is
            # a plan parameter the search should own rather than something fixed here.
            script.sell[t + 5, prod_idx] += info["max_held"]

    day_loop(start_day, setup=True)
    for day in range(start_day + 1, SEASON_DAYS):
        day_loop(day, setup=False)
    return script


CROP_TABLE = {
    # `first`/`max_day` are ages in days since planting; `ongoing` crops are never cleared by a
    # harvest and accrue to a lifetime cap instead. Mirrored from `kagg.sim.tiles`, pinned by tests.
    "WHEAT":      {"first": 2,  "max_day": 4,  "max_yield": 6, "ongoing": False},
    "CARROT":     {"first": 2,  "max_day": 3,  "max_yield": 4, "ongoing": False},
    "TOMATO":     {"first": 8,  "max_day": 8,  "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"first": 10, "max_day": 10, "max_yield": 4, "ongoing": True},
    "MELON":      {"first": 10, "max_day": 12, "max_yield": 6, "ongoing": False},
}

# `_DX`/`_DY` in `kagg.sim.ops`: NORTH is dy=-1, SOUTH dy=+1, EAST dx=+1, WEST dx=-1. So north is
# *smaller* y, which agrees with `quadrant_of` calling y < half "N". Getting this backwards would
# send every path the wrong way and is silent, because a blocked move is a no-op rather than an error.
def _path_ops(src, dst):
    """Movement ops walking `src` -> `dst`. X first, then Y; any order works inside one quadrant."""
    ops = []
    dx = dst[0] - src[0]
    dy = dst[1] - src[1]
    ops += ["EAST"] * dx if dx > 0 else ["WEST"] * (-dx)
    ops += ["SOUTH"] * dy if dy > 0 else ["NORTH"] * (-dy)
    return ops


def serpentine(tiles):
    """Order `tiles` so consecutive entries are adjacent where possible: rows, alternating direction.

    A boustrophedon keeps the walk between tiles at one step instead of jumping back to the row start,
    which matters because the turn budget is the binding constraint on how many tiles one unit can work.
    """
    rows = {}
    for x, y in tiles:
        rows.setdefault(y, []).append((x, y))
    out = []
    for i, y in enumerate(sorted(rows)):
        row = sorted(rows[y], key=lambda t: t[0], reverse=bool(i % 2))
        out += row
    return out


def grow(script, crop_name, tiles, plant_day, harvest_age=None, land_day=0, sell=True, unit=0):
    """Plant, water and harvest a block of tiles, re-walking from spawn every day.

    The crop analogue of `ranch()`, and structurally harder for one reason: `ranch()` is safe because
    it binds to a shed-access tile and therefore **never emits a movement op**, so an edit cannot
    invalidate later positions. There are only four such tiles and animals want them, so a crop block
    lives on the other ~96 and this routine has to route. Everything below follows from that.

    - **The walk repeats every day.** `_end_of_day` teleports every unit back to spawn at dawn
      (`jax_sim.py:1228-1236`), so a routine that walks to the block once and then emits WATER for the
      rest of the season waters the *spawn tile*. This is the same defect `ranch()` records fixing.
    - **Water every day, both crop types.** `_daily_refresh_plants` kills any PLANT tile at
      `consecutive_unwatered >= 2` regardless of `ONGOING`. The yield *bonus* only lands for
      non-ongoing crops inside `[(max_day+1)//2, max_day]` (`jax_sim.py:632-636`), which tempts a
      reader into skipping water for tomato and strawberry -- that kills them.
    - **One-shot crops cycle, ongoing crops do not.** HARVEST sets a non-ongoing tile back to EMPTY
      (`jax_sim.py:651`), so wheat can be replanted the next day and run several cycles a season.
      An ongoing tile survives its harvest and keeps producing to a lifetime cap.
    - **Ongoing crops are harvested every eligible day, deliberately.** Once `production_count` hits
      `MAX_YIELD` the tile's `max_lifespan_step` is set and `_decay_plants` eats a unit every other
      step, so accumulated yield rots. HARVEST is a silent no-op when nothing is ready
      (`doable` requires `units > 0`), so harvesting daily costs one turn and makes decay unreachable
      rather than merely unlikely.
    - **Seeds are ordered at dawn and planted later the same day.** The atomic PLANT rule
      (`jax_sim.py:565-582`) tests a turn's requests against seeds held at the *start* of that turn and
      drops **every** request for a crop when demand exceeds supply, not just the excess. Ordering on
      turn `d` and planting from `d+1` means the seeds have settled. `+=` is correct here, unlike the
      `maximum` used for hires: two blocks of the same crop on one day need the sum of their seeds,
      whereas they *share* the hands they hire.
    - **No DROP, and therefore the sell waits for the next dawn.** `_end_of_day` calls `_drop_to_shed`
      unconditionally (`jax_sim.py:1230`), so a harvest reaches the shed at dusk without a walk back.
      But it is in `carried` until then, so a SELL on the harvest day itself quotes against a shed that
      does not hold the crop. `ranch()` gets away with a same-day sell only because it stands on a shed
      tile and emits DROP first; out in a field, DROP cannot reach the shed. Measured: selling same-day
      banked **zero revenue on every crop**, losing exactly the seed cost
      (`tests/test_crop_routine.py::test_a_crop_routine_pays_for_itself`).

    Raises rather than truncates when a day's work will not fit in 24 turns -- a silently overflowing
    day would spill ops into the next dawn, where the unit has been teleported away.
    """
    if crop_name not in CROP_TABLE:
        raise ValueError(f"unknown crop {crop_name}")
    tiles = [tuple(t) for t in tiles]
    if not tiles:
        raise ValueError("grow() needs at least one tile")
    quads = {quadrant_of(*t) for t in tiles}
    if len(quads) > 1:
        raise ValueError(f"block spans quadrants {sorted(quads)}; v1 routes inside one quadrant only")

    info = CROP_TABLE[crop_name]
    c_idx = CROPS.index(crop_name)
    prod_idx = PRODUCTS.index(crop_name)
    ordered = serpentine(tiles)
    # Default to the top of the bonus-water window: the most yield from one planting. A caller wanting
    # more cycles of a fast crop passes a smaller age explicitly -- that trade is a plan parameter.
    age_to_harvest = info["max_day"] if harvest_age is None else harvest_age
    if age_to_harvest < info["first"]:
        raise ValueError(f"{crop_name} cannot be harvested before age {info['first']}")

    for k in range(land_purchases_for(ordered[0])):
        t = land_day * TURNS_PER_DAY + k
        if 0 <= t < script.T:
            script.buy_land[t] = 1

    # `maximum`, not `+=`: co-located routines share the crew, exactly as in `ranch()`.
    for day in range(plant_day, SEASON_DAYS):
        t = day * TURNS_PER_DAY
        if unit > 0 and t < script.T:
            script.hire[t] = max(int(script.hire[t]), unit)

    # Per-tile planting day, so one-shot crops can start a fresh cycle after each harvest.
    planted = {t: None for t in ordered}

    for day in range(plant_day, SEASON_DAYS):
        d = day * TURNS_PER_DAY
        # `Script.op` drops out-of-range turns so a routine may run past the season; the market arrays
        # are raw indexing and must honour the same contract explicitly.
        if d >= script.T:
            break
        jobs = {}
        for tile in ordered:
            p = planted[tile]
            if p is None:
                # **WATER on the planting day, not from the next one.** A seedling is already at
                # `consecutive_unwatered = 1`, so skipping today's water lets dusk take it to 2 and
                # `_daily_refresh_plants` turns it into a WEED on its first night -- after which WATER
                # (needs `kind == PLANT`) and PLANT (needs `EMPTY`) both silently no-op forever while
                # the routine keeps buying seeds. Traced in `data/logs/crop_trace.log`.
                jobs[tile] = ["PLANT", "WATER"]
            else:
                age = day - p
                if info["ongoing"]:
                    jobs[tile] = ["WATER"] + (["HARVEST"] if age >= info["first"] else [])
                elif age >= age_to_harvest:
                    # Water first: it still lands inside the bonus window on the harvest day itself.
                    jobs[tile] = ["WATER", "HARVEST"]
                else:
                    jobs[tile] = ["WATER"]

        n_plant = sum(1 for v in jobs.values() if "PLANT" in v)
        if n_plant:
            script.buy_seed[d, c_idx] += n_plant

        t = d + 1                      # turn 0 of the day is the market order; work starts at +1
        pos = tuple(SPAWN)
        for tile in ordered:
            for op_name in _path_ops(pos, tile):
                script.op(t, unit, op_name)
                t += 1
            pos = tile
            for op_name in jobs[tile]:
                script.op(t, unit, op_name, crop=crop_name if op_name == "PLANT" else None)
                t += 1
        if t > d + TURNS_PER_DAY:
            raise ValueError(
                f"day {day} needs {t - d} turns for {len(ordered)} tiles but a day is "
                f"{TURNS_PER_DAY}; use a smaller or closer block")

        if sell and any("HARVEST" in v for v in jobs.values()):
            # **Next dawn, not this evening.** The harvest is in `carried` until `_drop_to_shed` runs at
            # dusk, so a sell on this day finds an empty shed. Over-requesting is safe --
            # `_process_market` stops when the shed runs dry -- and the cadence itself is a plan
            # parameter, not a fact about the crop.
            n_harvested = sum(1 for v in jobs.values() if "HARVEST" in v)
            t_sell = (day + 1) * TURNS_PER_DAY
            if t_sell < script.T:
                script.sell[t_sell, prod_idx] += info["max_yield"] * n_harvested

        for tile in ordered:
            if "PLANT" in jobs[tile]:
                planted[tile] = day
            elif "HARVEST" in jobs[tile] and not info["ongoing"]:
                planted[tile] = None       # cleared to EMPTY, so it replants next day

    return script


# ---------------------------------------------------------------------------
# Inspection helpers, used by the tests to check the tape rather than trust it
# ---------------------------------------------------------------------------

def _turns_with(script, unit, op_name):
    return np.flatnonzero(np.asarray(script.unit_op)[:, unit] == OP[op_name])


def feed_days(script, unit):
    return {int(t) // TURNS_PER_DAY for t in _turns_with(script, unit, "FEED")}


def place_day(script, unit):
    ts = _turns_with(script, unit, "PLACE")
    return int(ts[0]) // TURNS_PER_DAY if len(ts) else None


def build_turn(script, unit):
    ops = np.asarray(script.unit_op)[:, unit]
    ts = np.flatnonzero((ops == OP["BUILD_PASTURE"]) | (ops == OP["BUILD_COOP"]))
    return int(ts[0]) if len(ts) else None
