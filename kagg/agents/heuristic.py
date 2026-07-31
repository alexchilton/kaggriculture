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
- **Stagger the plantings.** The shed holds 100 items overnight and destroys the overflow, so a
  synchronised harvest across many tiles throws most of itself away. Each tile gets a phase and
  only plants on its phase day, which spreads the harvest evenly across the cycle.

Known gaps, all deliberate for a first version: no animals, no fertilizer, no premium crops, no
sell-timing (it sells continuously rather than deferring), and no market denial.
"""

CROP = "WHEAT"
CYCLE_DAYS = 4          # wheat: plant, water through the window, harvest on day 4
MAX_YIELD_DAY = 4
FIRST_YIELD_DAY = 2
SEED_COST = 10
TURNS_PER_DAY = 24
SHED_CAP = 100

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


def _phase_ok(tile_index, day):
    """Whether this tile is allowed to be planted today, for harvest staggering."""
    mod = PARAMS["phase_mod"]
    return mod <= 1 or tile_index % mod == day % mod


def _job_for_tile(tile, day, has_seed, phase_ok):
    """What this tile needs, or None. Ordered by value: harvest, then water, then plant."""
    if tile is None:
        return ("PLANT", None) if (has_seed and phase_ok) else None
    if not isinstance(tile, dict):
        return None
    kind = tile.get("kind")
    if kind == "WEED":
        return ("DIG", None)
    if kind != "PLANT":
        return None

    age = day - tile["planted_day"]
    units = tile.get("yield_units", 0)
    if units > 0 and age >= MAX_YIELD_DAY:
        return ("HARVEST", None)
    if not tile.get("watered_today"):
        return ("WATER", None)
    return None


def agent(obs, config=None):
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

    tiles = _owned_tiles(farm, size)
    shed_tiles = _shed_tiles(size)
    unlocked = len(farm.get("unlocked_quadrants", ["NW"]))

    # ---- market orders -------------------------------------------------------------------
    market = []

    # Hire at the start of the day; cost is fib(n) so a full crew is a rounding error.
    # Labour is nearly free: 14 hands cost about $1000 for the day and buy 336 actions, against
    # actions that move $20+ of wheat. The binding cost is routing, not the wage.
    if hour in (0, 1):
        target = min(PARAMS["max_hands"],
                     max(2, -(-len(tiles) // PARAMS["tiles_per_hand"])))
        already = len(farm.get("hands", []))
        for _ in range(max(0, min(5, target - already))):
            market.append(["HIRE"])

    # Sell everything sellable. Wheat's curve is shallow enough that holding is not worth the
    # shed pressure, and selling keeps room for the next drop.
    for item, n in sorted(shed.items()):
        if n > 0 and item != "FERTILIZER":
            market.append(["SELL", item, n])

    # Seeds for the plantings that are actually due, plus a small buffer.
    due = sum(
        1 for i, (x, y) in enumerate(tiles)
        if farm["tiles"][y][x] is None and _phase_ok(i, day)
    )
    want_seed = max(0, due + PARAMS["seed_buffer"] - seeds.get(CROP, 0))
    if want_seed and money > SEED_COST * want_seed:
        market.append(["BUY_SEED", CROP, want_seed])

    # Only expand once the current land is genuinely productive. Buying early starves seed
    # and wage spending, which was measured leaving 18 tiles idle all season.
    planted = sum(
        1 for (x, y) in tiles
        if isinstance(farm["tiles"][y][x], dict) and farm["tiles"][y][x].get("kind") == "PLANT"
    )
    productive = planted / max(1, len(tiles))
    if (unlocked <= len(LAND_PRICES)
            and money >= LAND_PRICES[unlocked - 1] * PARAMS["land_slack"]
            and productive > PARAMS["productive_gate"]):
        market.append(["BUY_LAND"])

    # maxMarketOrdersPerTurn is 10 and extras are silently dropped, so sells come first.
    market = market[:10]

    # ---- unit assignment -----------------------------------------------------------------
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm.get("hands", [])]
    seed_budget = seeds.get(CROP, 0)

    jobs = {}
    for i, (x, y) in enumerate(tiles):
        job = _job_for_tile(
            farm["tiles"][y][x], day,
            has_seed=seed_budget > 0,
            phase_ok=_phase_ok(i, day),
        )
        if job:
            jobs[(x, y)] = job[0]

    actions = []
    claimed = set()
    planned_plants = 0
    for unit_idx, pos in enumerate(positions):
        carried = inventories[unit_idx] if unit_idx < len(inventories) else {}
        carrying = sum(carried.values())

        # Full hands go to the shed, otherwise the nightly drop destroys the overflow.
        if carrying >= PARAMS["carry_before_drop"]:
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

        # PLANT is atomically validated: if requests exceed seeds, ALL plant requests for the
        # crop are dropped. So never ask for more than we hold.
        if op == "PLANT" and planned_plants >= seed_budget:
            actions.append(["PASS"])
            continue

        claimed.add(target)
        if pos == target:
            actions.append(["PLANT", CROP] if op == "PLANT" else [op])
            if op == "PLANT":
                planned_plants += 1
        else:
            actions.append([_step_toward(pos, target)])

    return {"farmer": actions[0], "hands": actions[1:], "market": market}
