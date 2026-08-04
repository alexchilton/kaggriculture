"""Driving a searched plan inside the real `kaggle_environments` environment.

The point of this module is that it contains **no** decision logic. It converts one observation
dict into the same :class:`~kagg.search.executor.View` the batched simulator produces, calls the
same `decide`, and converts the result back into the action dict the environment wants. If the
searched behaviour and the played behaviour ever disagree, it is a bug here or a genuine
simulator divergence -- never a second copy of the strategy that drifted.

The emitted market order list is **compacted, in `game._order_book`'s canonical order, and capped at
``MAX_ORDERS``**. It was a fixed 8-slot layout padded with ``["SELL", crop, 0]`` until 2026-08-04, on
the reasoning that `_parse_order` rejects a zero quantity while the slot still lines up. The rejection
is real; the conclusion was not. `reference/kaggriculture.py:534` truncates with
``queues.append(q[:max_orders])`` **before** parsing, so a padding entry costs a slot exactly as a
real order does -- and the padding was harmless only because nothing had ever exceeded ten. See
`to_action` for the measurement that exposed it.
"""

import json
import os
from pathlib import Path

import numpy as np

from kagg.search import executor as X
from kagg.search.plan import (
    ANIMAL_NAMES,
    ANIMAL_PRODUCT_NAMES,
    CROP_NAMES,
    N_ANIMALS,
    N_CROPS,
    N_PRODUCTS,
    decode,
    pad_genome,
)

# `reference/kaggriculture.py:526`, `maxMarketOrdersPerTurn`. Truncation is positional and applied
# before `_parse_order`, so this is a hard budget on the emitted list length.
MAX_ORDERS = 10

# `market.PRODUCTS` order, rebuilt here so the submission path stays free of the sim package.
PRODUCT_NAMES = CROP_NAMES + ANIMAL_PRODUCT_NAMES

DEFAULT_PLAN = Path(__file__).with_name("best_plan.json")


def plan_path():
    """Which plan file `agent` plays.

    Overridable by ``KAGG_SEARCH_PLAN`` so that a plan can be measured in the arena without
    overwriting the saved one. The environment variable is read per call rather than cached
    because the arena runs matches in freshly spawned worker processes.
    """
    return Path(os.environ.get("KAGG_SEARCH_PLAN", DEFAULT_PLAN))

# `kagg/sim/ops.py:43-44`, in order. **All eighteen**, because the eight livestock ops were absent
# and `_unit_action` fell through to `OP_NAMES.get(op, "PASS")` -- so FEED, CARE, PICKUP, PLACE, DROP,
# FERTILIZE, COLLECT_FERTILIZER and BUILD_* rendered as `["PASS"]` rather than failing loudly. A
# census of the $147,178 seat's tape (`data/logs/tape_diff_merged.log`) found our agent emitting none
# of those eight in 720 turns while the winner spent 44% of its unit-ops on real work against our 22%.
OP_NAMES = {
    0: "PASS", 1: "NORTH", 2: "SOUTH", 3: "EAST", 4: "WEST",
    5: "WATER", 6: "HARVEST", 7: "PLANT", 8: "DIG",
    9: "PICKUP", 10: "DROP", 11: "PLACE", 12: "FEED", 13: "CARE",
    14: "COLLECT_FERTILIZER", 15: "FERTILIZE", 16: "BUILD_COOP", 17: "BUILD_PASTURE",
}
PLANT_OP = 7
PICKUP_OP = 9
PLACE_OP = 11

# `market.ITEMS` = products then animals, rebuilt here so the submission path stays free of the sim
# package. The ordering is asserted against `kagg.sim.market` in
# `tests/test_observation_view_sees_livestock.py`, since `unit_item` is an index into it.
ITEM_NAMES = PRODUCT_NAMES + ANIMAL_NAMES

_KIND = {"WEED": X.WEED, "PLANT": X.PLANT, "COOP": X.COOP, "PASTURE": X.PASTURE}


def observation_view(obs):
    """Build a batch-of-one View from a live observation."""
    me = obs.get("player", 0)
    farm = obs["farms"][me]
    private = obs.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    seeds = private.get("seeds", {}) or {}
    prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
    board = farm["tiles"]

    kind = np.zeros((1, X.TILES), dtype=np.int64)
    crop = np.full((1, X.TILES), -1, dtype=np.int64)
    planted = np.zeros((1, X.TILES), dtype=np.int64)
    watered = np.zeros((1, X.TILES), dtype=bool)
    units = np.zeros((1, X.TILES), dtype=np.int64)
    # Livestock, per tile. Omitting these is what made the submission blind to its own herd: the
    # `View` defaults fill them with "no animals anywhere", and every livestock mask in `executor.py`
    # is gated on `has_animal`, `fertilizer_available` or a unit's carried wheat -- so FEED, CARE,
    # PICKUP and PLACE could never fire. Measured on episode 89873723 seat 0: 14 animals on the board
    # and 0 seen. `rollout.build_view` has always passed these; the two builders simply disagreed.
    animal = np.full((1, X.TILES), -1, dtype=np.int64)
    fed = np.zeros((1, X.TILES), dtype=bool)
    cared = np.zeros((1, X.TILES), dtype=bool)
    unfed = np.zeros((1, X.TILES), dtype=np.int64)
    fert_ready = np.zeros((1, X.TILES), dtype=bool)

    for i, (x, y) in enumerate(X.ORDER):
        cell = board[y][x]
        if cell == "LOCKED":
            kind[0, i] = X.LOCKED
            continue
        if cell is None:
            kind[0, i] = X.EMPTY
            continue
        kind[0, i] = _KIND.get(cell.get("kind"), X.EMPTY)
        if cell.get("kind") == "PLANT":
            crop[0, i] = CROP_NAMES.index(cell["crop"])
            planted[0, i] = cell.get("planted_day", 0)
            watered[0, i] = bool(cell.get("watered_today"))
        # An occupied pen carries the animal on the same dict as the structure, so this is not an
        # `elif` on kind -- a PASTURE tile is both the pen and the cow.
        name = cell.get("animal")
        if name:
            animal[0, i] = ANIMAL_NAMES.index(name)
            fed[0, i] = bool(cell.get("fed_today"))
            cared[0, i] = bool(cell.get("cared_today"))
            unfed[0, i] = int(cell.get("consecutive_unfed", 0))
            fert_ready[0, i] = bool(cell.get("fertilizer_available"))
        units[0, i] = cell.get("yield_units", 0)

    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm.get("hands", [])]
    unit_ord = np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64)
    for u, (x, y) in enumerate(positions[: X.MAX_EXEC_UNITS]):
        unit_ord[0, u] = X.ORD_OF_TILE[y * X.BOARD + x]

    # `private["inventories"]` is one item->qty dict per unit, farmer first, in the same order as
    # `farmer` + `hands`. FEED spends wheat from the unit's *own* inventory, so a parser that reports
    # zero carried wheat makes the PICKUP -> FEED loop -- the busiest thing a large herd does --
    # unreachable no matter what the plan asks for.
    inventories = private.get("inventories") or []
    carried_wheat = np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64)
    carried_animal = np.full((1, X.MAX_EXEC_UNITS), -1, dtype=np.int64)
    for u, inv in enumerate(inventories[: X.MAX_EXEC_UNITS]):
        inv = inv or {}
        carried_wheat[0, u] = int(inv.get("WHEAT", 0))
        for a, animal_name in enumerate(ANIMAL_NAMES):
            if int(inv.get(animal_name, 0)) > 0:
                # First match wins, mirroring `rollout._carried_animal`'s argmax. A unit holding two
                # species at once is possible but never useful -- PLACE consumes one.
                carried_animal[0, u] = a
                break

    return X.View(
        day=int(obs.get("day", 0)),
        hour=int(obs.get("hour", 0)),
        kind=kind,
        crop=crop,
        planted_day=planted,
        watered=watered,
        yield_units=units,
        unit_ord=unit_ord,
        n_units=np.array([min(len(positions), X.MAX_EXEC_UNITS)]),
        money=np.array([float(farm["money"])]),
        seeds=np.array([[int(seeds.get(c, 0)) for c in CROP_NAMES]]),
        # `PRODUCT_NAMES`, not `CROP_NAMES`: the four animal products are ~83% of the leaders'
        # revenue, and reading only the crops here is what made the submission path blind to them.
        shed=np.array([[int(shed.get(c, 0)) for c in PRODUCT_NAMES]]),
        prices=np.array([[int(prices.get(c, 0)) for c in PRODUCT_NAMES]]),
        n_land=np.array([len(farm.get("unlocked_quadrants", ["NW"])) - 1]),
        # Livestock, in the same order `rollout.build_view` passes it. `BUY_ANIMAL` deposits into the
        # shed, so `shed_animals` is what `PICKUP` then `PLACE` draws on to fill a pen.
        animal=animal,
        fed_today=fed,
        cared_today=cared,
        consecutive_unfed=unfed,
        fertilizer_available=fert_ready,
        shed_animals=np.array([[int(shed.get(a, 0)) for a in ANIMAL_NAMES]]),
        shed_wheat=np.array([int(shed.get("WHEAT", 0))]),
        carried_wheat=carried_wheat,
        carried_animal=carried_animal,
    )


def _unit_action(op, crop, item=0, qty=0):
    """Render one unit's op in the environment's wire format.

    Arities are read off the winner's own tape rather than inferred: every op is `["OP"]` except
    `PLANT` (`["PLANT", crop]`), `PICKUP` (`["PICKUP", item, qty]`) and `PLACE`, which is
    `["PLACE", animal]` for an animal but `["PLACE", item, qty]` when dropping a product.

    An unknown op raises instead of silently becoming `PASS`. The old `.get(op, "PASS")` default is
    what let eight missing entries in `OP_NAMES` degrade into no-ops with nothing in the logs.
    """
    op = int(op)
    if op == PLANT_OP:
        return ["PLANT", CROP_NAMES[int(crop)]]
    if op == PICKUP_OP:
        return ["PICKUP", ITEM_NAMES[int(item)], max(int(qty), 1)]
    if op == PLACE_OP:
        i = int(item)
        # Animals sit above the products in `ITEMS` and take no quantity; products do.
        return ["PLACE", ITEM_NAMES[i]] if i >= N_PRODUCTS else \
               ["PLACE", ITEM_NAMES[i], max(int(qty), 1)]
    if op not in OP_NAMES:
        raise KeyError(f"unit op {op} has no wire name; `kagg/sim/ops.py` defines 0..17")
    return [OP_NAMES[op]]


def to_action(obs, decision, n_units):
    """Turn one game's Decision into the environment's action dict."""
    hour = int(obs.get("hour", 0))
    units = [_unit_action(decision.unit_op[0, u], decision.unit_crop[0, u],
                          decision.unit_item[0, u], decision.unit_qty[0, u])
             for u in range(n_units)]

    # **Compacted, in `game._order_book`'s canonical order, and never longer than MAX_ORDERS.**
    #
    # This was a fixed 8-slot layout padded with `["SELL", crop, 0]`, on the stated reasoning that
    # `_parse_order` rejects a zero quantity while the slot still lines up. The rejection is real but
    # the conclusion was wrong: `reference/kaggriculture.py:534` does `queues.append(q[:max_orders])`
    # **before** any parsing, so truncation is positional and a padding entry consumes a slot exactly
    # as a real order does. Widening sells from 5 to 9 pushed the list to 12 and silently dropped the
    # last two -- HIRE and BUY_LAND -- for 55% money drift against the real environment.
    #
    # The simulator was already right: `_order_book` keeps only positive quantities and clamps to ten.
    # Mirroring that here makes the two agree by construction rather than by staying under the cap.
    # BUY_ANIMAL and BUY_PRODUCT are emitted for the first time; without them the submission could not
    # buy an animal or a unit of feed whatever the plan said.
    market = []

    def order(entry, qty):
        if int(qty) > 0:
            market.append(entry + [int(qty)])

    for i in range(N_PRODUCTS):
        order(["SELL", PRODUCT_NAMES[i]], decision.sell[0, i])
    buying = hour % N_CROPS
    order(["BUY_SEED", CROP_NAMES[buying]], decision.buy_seed[0, buying])
    for i in range(N_PRODUCTS):
        order(["BUY_PRODUCT", PRODUCT_NAMES[i]], decision.buy_product[0, i])
    for a in range(N_ANIMALS):
        order(["BUY_ANIMAL", ANIMAL_NAMES[a]], decision.buy_animal[0, a])

    # Atomic orders last in the canonical order, but they must never be the ones truncated: both
    # resolve ahead of the per-unit lockstep at their slot, so they get first claim on that turn's
    # cash. Reserve room for them by trimming sells rather than letting the tail fall off.
    # **One HIRE order per hand.** `_process_market` resolves one atomic order per slot, so N hands is
    # N orders -- `decision.hire` is a count (`executor.py`), matching `game.py:277`'s `(n_hire > k)`
    # expansion. It was `if bool(...)` here, which flattened a six-hand opening to one hand and made
    # the leaders' two-HIRE first turn unreachable from the submission.
    #
    # BUY_LAND keeps the last slot: `LAND_PRICES[0]` is $1,000 against a hire ladder starting at $1, and
    # the land unlock gates the melon and strawberry tiles whose first yield lands on day 10.
    # Hiring takes only the slots the market is not using, with a floor of one so a busy turn still
    # ramps the crew. Letting it take the whole budget is a measured failure, not a hypothetical: a
    # fourteen-hand request filled all ten slots, `market[: MAX_ORDERS - 10]` truncated every sell and
    # buy to nothing, and the season ended on $98 against a $3,000 stake. Selling is the revenue; hands
    # only multiply what a farm can already afford to do.
    n_hire = int(decision.hire[0])
    land = [["BUY_LAND"]] if bool(decision.buy_land[0]) else []
    hire_slots = max(1, MAX_ORDERS - len(land) - len(market))
    hires = [["HIRE"]] * min(n_hire, hire_slots)
    atomic = hires + land
    if len(market) + len(atomic) > MAX_ORDERS:
        market = market[: MAX_ORDERS - len(atomic)]
    market.extend(atomic)

    return {"farmer": units[0], "hands": units[1:], "market": market}


def make_agent(genome):
    """An agent closure bound to one genome."""
    plan = decode(np.asarray(genome)[None, :])

    def _agent(obs, config=None):
        view = observation_view(obs)
        decision = X.decide(view, plan)
        return to_action(obs, decision, int(view.n_units[0]))

    return _agent


def load_best(path=None):
    """Load a saved genome, migrating it if it predates a later gene block.

    `pad_genome` is applied *here*, at the one boundary where a genome enters the process from disk,
    rather than inside `decode` -- so a length mismatch anywhere else is still a loud error. The file
    on disk holds 277 genes from before the livestock blocks were appended on 2026-08-04; without this
    the shipped default plan raises on load and the submission agent does not start.
    """
    with open(path or plan_path()) as handle:
        return pad_genome(np.array(json.load(handle)["genome"], dtype=np.int64))


def save_best(genome, meta=None, path=None):
    payload = {"genome": [int(v) for v in genome]}
    payload.update(meta or {})
    with open(path or plan_path(), "w") as handle:
        json.dump(payload, handle, indent=1)


_AGENT = None
_AGENT_PATH = None


def agent(obs, config=None):
    """Module entry point, so the searched plan can be used as a pool spec or submitted."""
    global _AGENT, _AGENT_PATH
    path = plan_path()
    if _AGENT is None or _AGENT_PATH != path:
        _AGENT, _AGENT_PATH = make_agent(load_best(path)), path
    return _AGENT(obs, config)
