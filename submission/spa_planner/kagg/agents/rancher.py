"""Rancher: a tiny, wage-free animal farm. A structurally different agent, not a retuned heuristic.

Built because the ladder replays said so. Across 17 recorded losses, the three largest --
$104k, $93k and $84k -- were all **small 8-15 tile farms built almost entirely on pasture
animals, two of them with zero hired hands**. Our own measurements had concluded animals were net
negative, but that was measured against a pool of our own agent with our own routing, so it was
plausibly an artifact rather than a fact about animals.

The design inverts every choice `heuristic.py` makes:

- **No hired hands at all.** Wages are the hidden tax: the cost is Fibonacci and resets every
  morning, so eight hands is about $1.6k a season and fourteen is nearly $30k. A farm small enough
  for one farmer pays none of it.
- **Everything on the shed-access tiles.** `FEED` and `PLACE` draw from the unit's *carried*
  inventory, not the shed, so a distant animal costs a walk to fetch wheat every single day.
  Standing on a shed tile makes PICKUP, FEED, CARE, HARVEST, DROP and SELL all zero-movement. That
  removes the routing cost which is what actually made animals lose in our earlier test.
- **Animals, not crops.** `_daily_refresh_animals` has no lifetime production cap, unlike plants:
  a cow yields all season. Milk's base is $160 against a season town drain of 446 units, far more
  than one farm can supply.
- **Sell into the drain, never in bulk.** Milk's glut curve is linear with amplitude ~$2.10/unit,
  so 200 units dumped at once floors the price. A trickle matched to demand holds it near base.

Self-contained -- no `kagg` imports -- so the arena, `kaggle_environments` and Kaggle can all load
this file directly.
"""

BOARD = 10
TURNS_PER_DAY = 24

ANIMALS = {
    "COW":   {"cost": 400, "structure": "PASTURE", "product": "MILK",  "interval": 2},
    "GOOSE": {"cost": 300, "structure": "COOP",    "product": "EGG",   "interval": 1},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "product": "WOOL",  "interval": 3},
}
BASE_PRICE = {"MILK": 160, "EGG": 50, "WOOL": 200, "WHEAT": 25, "FERTILIZER": 100}

PARAMS = {
    "animal": "COW",
    # How many animals to run. Kept small on purpose: one farmer has 24 actions a day and each
    # animal needs feed, care and a harvest, so the crew size is bounded by the action budget,
    # not by money.
    "herd": 6,   # measured optimum: 4 -> $31.6k, 6 -> $45.7k, 10 -> $15.9k. Action budget, not money.
    # Sell only when the price is at least this fraction of base, so a trickle meets the town
    # drain instead of flooding a shallow market.
    "sell_floor_frac": 0.75,
    # Sell at most this many units per turn, for the same reason.
    "sell_batch": 2,
    # From this day, liquidate regardless of price -- unsold stock scores nothing.
    "endgame_day": 28,
    # Feed buffer to carry, so a missed pickup never starves an animal (two unfed days and it
    # escapes, wasting both the animal and the structure).
    "feed_carry": 8,
}


def _shed_tiles(size=BOARD):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _plots(size=BOARD, unlocked_quadrants=("NW",)):
    """Tiles for the herd, nearest the shed first, restricted to unlocked quadrants.

    The subtlety that cost a rebuild: **only one of the four shed-access tiles starts usable.**
    The access tiles are the inner corners (4,4), (5,4), (4,5), (5,5), and three of those sit in
    NE, SW and SE -- all locked at the start. An earlier version handed back all four, so the
    farmer could only ever build one pasture and idled for twenty turns a day.
    """
    half = size // 2

    def quadrant(x, y):
        return ("N" if y < half else "S") + ("W" if x < half else "E")

    anchor = (half - 1, half - 1)
    usable = [
        (x, y)
        for y in range(size)
        for x in range(size)
        if quadrant(x, y) in unlocked_quadrants
    ]
    # Nearest the shed anchor first: every step away is an action spent walking, every day.
    usable.sort(key=lambda t: (abs(t[0] - anchor[0]) + abs(t[1] - anchor[1]), t))
    return usable


def _step_toward(pos, target):
    (x, y), (tx, ty) = pos, target
    dx, dy = tx - x, ty - y
    if abs(dx) >= abs(dy):
        return "EAST" if dx > 0 else "WEST"
    return "SOUTH" if dy > 0 else "NORTH"


def agent(obs, config=None):
    me = obs.get("player", 0)
    farm = obs["farms"][me]
    day = obs.get("day", 0)
    private = obs.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    carried = (private.get("inventories") or [{}])[0]
    prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
    money = farm["money"]
    tiles = farm["tiles"]

    spec = ANIMALS[PARAMS["animal"]]
    animal, structure, product = PARAMS["animal"], spec["structure"], spec["product"]
    quads = tuple(farm.get("unlocked_quadrants", ["NW"]))
    plots = _plots(unlocked_quadrants=quads)[: PARAMS["herd"]]
    shed_tiles = _shed_tiles()
    pos = tuple(farm["farmer"])
    endgame = day >= PARAMS["endgame_day"]

    # ---- market ---------------------------------------------------------------------------
    market = []

    # Wheat is feed, and it is the only product buyable back from the market. Keep a buffer.
    need_feed = PARAMS["herd"] * 2
    if shed.get("WHEAT", 0) + carried.get("WHEAT", 0) < need_feed and money > 400:
        market.append(["BUY_PRODUCT", "WHEAT", need_feed])

    placed = sum(
        1 for (x, y) in plots
        if isinstance(tiles[y][x], dict) and "animal" in tiles[y][x]
    )
    ready = sum(
        1 for (x, y) in plots
        if isinstance(tiles[y][x], dict) and tiles[y][x].get("kind") == structure
        and "animal" not in tiles[y][x]
    )
    owned = shed.get(animal, 0) + carried.get(animal, 0)
    if placed + owned < PARAMS["herd"] and ready > owned and money > spec["cost"] + 600:
        market.append(["BUY_ANIMAL", animal, 1])

    # More land, once the herd has filled what we own and the money is comfortable. Each quadrant
    # is 25 more tiles, but only a few near the shed are reachable within one farmer's action
    # budget, so this is about unlocking the *other three shed-access tiles*, not about acreage.
    land_cost = [1000, 2000, 4000]
    n_extra = len(quads) - 1
    if (n_extra < len(land_cost) and placed >= len(plots)
            and money > land_cost[n_extra] + spec["cost"] * 2):
        market.append(["BUY_LAND"])

    # Trickle sales: the market is shallow, so meet the drain rather than flood it.
    held = shed.get(product, 0)
    if held > 0:
        good = prices.get(product, 0) >= PARAMS["sell_floor_frac"] * BASE_PRICE[product]
        if endgame:
            market.append(["SELL", product, held])
        elif good:
            market.append(["SELL", product, min(held, PARAMS["sell_batch"])])
    for extra in ("FERTILIZER",):
        if shed.get(extra, 0) > 4:
            market.append(["SELL", extra, shed[extra]])

    # ---- the single farmer ------------------------------------------------------------------
    act = ["PASS"]
    x, y = pos
    tile = tiles[y][x]
    on_shed = pos in shed_tiles

    # Anything carried is dropped before the night destroys the overflow.
    if on_shed and sum(carried.values()) >= 20:
        return {"farmer": ["DROP"], "hands": [], "market": market[:10]}

    # Collect a bought animal while standing on the shed. PLACE draws from *carried* inventory,
    # and an empty structure is rarely a shed tile, so without this the animal sits in the shed
    # forever: the farmer walks to the empty pasture, finds it has nothing to place, and walks
    # back. Measured as a herd stuck at one for an entire season.
    empty_structures = [
        (px, py) for (px, py) in plots
        if isinstance(tiles[py][px], dict)
        and tiles[py][px].get("kind") == structure
        and "animal" not in tiles[py][px]
    ]
    if on_shed and empty_structures and carried.get(animal, 0) < 1 and shed.get(animal, 0) >= 1:
        return {"farmer": ["PICKUP", animal, 1], "hands": [], "market": market[:10]}
    if carried.get(animal, 0) >= 1 and empty_structures and pos not in empty_structures:
        target = min(empty_structures, key=lambda t: abs(t[0] - pos[0]) + abs(t[1] - pos[1]))
        return {"farmer": [_step_toward(pos, target)], "hands": [], "market": market[:10]}

    if pos in plots:
        if tile is None:
            act = ["BUILD_PASTURE"] if structure == "PASTURE" else ["BUILD_COOP"]
        elif isinstance(tile, dict) and tile.get("kind") == "WEED":
            act = ["DIG"]
        elif isinstance(tile, dict) and tile.get("kind") == structure and "animal" not in tile:
            if carried.get(animal, 0) >= 1:
                act = ["PLACE", animal]
            elif on_shed and shed.get(animal, 0) >= 1:
                act = ["PICKUP", animal, 1]
            elif shed.get(animal, 0) >= 1:
                act = [_step_toward(pos, min(shed_tiles, key=lambda t: abs(t[0] - x) + abs(t[1] - y)))]
        elif isinstance(tile, dict) and "animal" in tile:
            # Harvest first so max_held never blocks the next production, then feed to keep it
            # alive, then CARE, which doubles the following yield.
            if tile.get("yield_units", 0) > 0:
                act = ["HARVEST"]
            elif not tile.get("fed_today"):
                if carried.get("WHEAT", 0) >= 1:
                    act = ["FEED"]
                elif on_shed and shed.get("WHEAT", 0) >= 1:
                    act = ["PICKUP", "WHEAT", PARAMS["feed_carry"]]
                else:
                    act = [_step_toward(pos, min(shed_tiles, key=lambda t: abs(t[0] - x) + abs(t[1] - y)))]
            elif not tile.get("cared_today"):
                act = ["CARE"]
            elif tile.get("fertilizer_available"):
                act = ["COLLECT_FERTILIZER"]
            else:
                act = ["PASS"]

    if act == ["PASS"]:
        # Go to whichever plot still needs something; otherwise sit on the shed and bank produce.
        pending = []
        for (px, py) in plots:
            t = tiles[py][px]
            if t is None:
                pending.append((px, py))                      # bare tile: build here
            elif isinstance(t, dict) and "animal" in t:
                # An occupied structure keeps `kind == structure`, so it must be matched on the
                # animal first. Checking `kind` alone made the farmer's own tile always "pending"
                # at distance zero, so it selected itself every turn and never left -- one cow,
                # twenty idle turns a day, for the whole season.
                if (t.get("yield_units", 0) > 0 or not t.get("fed_today")
                        or not t.get("cared_today")):
                    pending.append((px, py))
            elif isinstance(t, dict) and t.get("kind") in ("WEED", structure):
                pending.append((px, py))                      # weed to clear, or empty structure
        if pending:
            target = min(pending, key=lambda t: abs(t[0] - x) + abs(t[1] - y))
            act = [_step_toward(pos, target)] if target != pos else ["PASS"]
        elif sum(carried.values()) and not on_shed:
            act = [_step_toward(pos, min(shed_tiles, key=lambda t: abs(t[0] - x) + abs(t[1] - y)))]
        elif on_shed and sum(carried.values()):
            act = ["DROP"]

    return {"farmer": act, "hands": [], "market": market[:10]}
