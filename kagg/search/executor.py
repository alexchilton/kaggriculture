"""The plan interpreter: turns a :class:`~kagg.search.plan.Plan` into one turn's actions.

Deliberately mechanical. Everything here is *how to carry out* a plan, never *what plan to carry
out* -- no crop preferences, no sell cadence, no hiring curve, no priority between crops. Those all
live in the genes so that search owns them.

The only judgements baked in are ones that are forced by the rules rather than by taste:

- a unit works the **nearest** outstanding job inside its own block of tiles, because walking is
  the dominant cost and the alternative is to search over routes as well;
- within a tile, **DIG > HARVEST > WATER > PLANT**, because a weed blocks everything, an unharvested
  ongoing crop stops producing, and an unwatered plant dies after two days;
- a unit never requests a PLANT the farm has no seed for, because `interpreter` drops *every*
  PLANT for a crop when the requests exceed the seeds held.

Running the same code on both simulators
----------------------------------------

`decide` reads a :class:`View` -- a handful of arrays -- and writes a :class:`Decision`. Both the
batched simulator (`kagg.search.rollout`) and a live `kaggle_environments` observation
(`kagg.search.agent`) build the same View, so there is exactly one copy of the logic and no chance
of the searched behaviour and the submitted behaviour drifting apart.

Two divergences between the two simulators had to be designed around rather than discovered later:

**Market order slots.** The simulator settles every product's sell orders against both players
alternating unit by unit, then handles seeds, hiring and land. The reference instead pairs the
players' *i-th market order*. Those agree only if both players put the same product in the same
slot. So the emitted order list has a **fixed 8-slot layout** -- one slot per sellable crop, then
seed, hire, land -- with unwanted slots filled by ``["SELL", crop, 0]``, which `_parse_order`
rejects while the slot itself still lines up. That also keeps the list inside
`maxMarketOrdersPerTurn`, which the simulator does not model at all.

**Atomic PLANT.** The reference drops all PLANT requests for a crop when they exceed seeds held;
the simulator instead plants greedily unit by unit until the seeds run out. The parity gate never
caught this because its random scripts only ever move one unit. Not requesting more plants than
there are seeds makes the two agree, and `tests/test_search_executor.py` pins it.
"""

from dataclasses import dataclass

import numpy as np

from kagg.sim import ops as O
from kagg.search.plan import (
    BASE_PRICE,
    BLOCK_DAYS,
    BOARD,
    COOP,
    FERT_APPLY,
    FERT_SELL,
    FIRST_YIELD_DAY,
    HARVEST_DELTA,
    MAX_YIELD_DAY,
    N_BLOCKS,
    N_CROPS,
    N_ANIMALS,
    NO_STRUCTURE,
    ONGOING,
    ONGOING_THRESHOLD,
    PASTURE as PLAN_PASTURE,
    SEED_COST,
    TILES,
)

N_PRODUCTS = 9        # market.N_PRODUCTS; the sell/buy_product axis width

# `market.ANIMAL_COST`, inlined for the same reason the crop tables above are: this module is pure
# numpy and imported by the submission path, so it must not pull in jax.
ANIMAL_COST = np.array([300.0, 400.0, 500.0])

# Ceiling used only to size a wheat order against cash. Wheat's base price is $25 and it rises as the
# town runs dry, so budgeting at the top of the range under-orders rather than overdrawing.
WHEAT_PRICE_CAP = 60.0

# `plan.COOP`, renamed at the import site to avoid colliding with the tile-kind COOP below.
COOP_GENE_KIND = 1

# Tile kinds, matching `kagg.sim.tiles`.
EMPTY, LOCKED, WEED, PLANT, COOP, PASTURE = range(6)

MAX_EXEC_UNITS = 16      # the hire gene tops out at 14 hands plus the farmer
N_MARKET_SLOTS = 8


def _boustrophedon():
    """Tile visiting order: serpentine rows, so consecutive plan genes are spatial neighbours."""
    out = []
    for y in range(BOARD):
        xs = range(BOARD) if y % 2 == 0 else reversed(range(BOARD))
        for x in xs:
            out.append((x, y))
    return out


ORDER = _boustrophedon()
OX = np.array([p[0] for p in ORDER], dtype=np.int16)
OY = np.array([p[1] for p in ORDER], dtype=np.int16)
TILE_OF_ORD = (OY.astype(np.int64) * BOARD + OX.astype(np.int64))
ORD_OF_TILE = np.zeros(TILES, dtype=np.int16)
ORD_OF_TILE[TILE_OF_ORD] = np.arange(TILES, dtype=np.int16)
DIST = (np.abs(OX[:, None] - OX[None, :]) + np.abs(OY[:, None] - OY[None, :])).astype(np.int16)

# Neighbour order-position in each of the four move directions, -1 off the board.
_DIRS = [(0, -1), (0, 1), (1, 0), (-1, 0)]        # N, S, E, W -- matches ops.NORTH..WEST
NEIGH = np.full((TILES, 4), -1, dtype=np.int16)
for _i, (_x, _y) in enumerate(ORDER):
    for _d, (_dx, _dy) in enumerate(_DIRS):
        _nx, _ny = _x + _dx, _y + _dy
        if 0 <= _nx < BOARD and 0 <= _ny < BOARD:
            NEIGH[_i, _d] = ORD_OF_TILE[_ny * BOARD + _nx]
MOVE_OPS = np.array([O.NORTH, O.SOUTH, O.EAST, O.WEST], dtype=np.int64)

(JOB_NONE, JOB_DIG, JOB_HARVEST, JOB_WATER, JOB_PLANT,
 JOB_FEED, JOB_CARE, JOB_COLLECT, JOB_PLACE, JOB_BUILD) = range(10)
JOB_TO_OP = np.array([O.NOOP, O.DIG, O.HARVEST, O.WATER, O.PLANT_OP,
                      O.FEED, O.CARE, O.COLLECT_FERT, O.PLACE, O.BUILD_PASTURE], dtype=np.int64)

# **Jobs that only some units can serve**, because the rules gate them on what the unit is carrying:
# `jax_masks.py:96` needs `carrying_wheat` for FEED, and PLACE needs the animal in hand. `tile_jobs`
# is per-tile and cannot know, so `decide` masks these out for units that are not equipped.
CARRY_GATED = (JOB_FEED, JOB_PLACE)

# Item indices into the shed/carried axis, which is `PRODUCTS + ANIMALS` (`market.py:42`).
WHEAT_ITEM = 0
ANIMAL_ITEM_BASE = 9        # market.N_PRODUCTS; asserted in tests/test_executor_animals.py

# Where a night leaves every unit. `ops.SHED_TILES == [44, 45, 54, 55]`, and the simulator respawns
# the whole crew there at dawn -- so hour 0 is a **free** PICKUP window that needs no routing at all.
# Sending a unit to fetch wheat mid-day is what turned `jax_frontier` into a 70.5% PICKUP loop.
SHED_ORDS = ORD_OF_TILE[np.asarray(O.SHED_TILES)].astype(np.int64)

_BIG = np.int16(30000)


@dataclass
class View:
    """Everything the interpreter reads, batched over B games, in serpentine tile order."""

    day: int
    hour: int
    kind: np.ndarray            # [B, TILES] int
    crop: np.ndarray            # [B, TILES] int, -1 where no plant
    planted_day: np.ndarray     # [B, TILES] int
    watered: np.ndarray         # [B, TILES] bool
    yield_units: np.ndarray     # [B, TILES] int
    unit_ord: np.ndarray        # [B, MAX_EXEC_UNITS] int, serpentine position of each unit
    n_units: np.ndarray         # [B] int
    money: np.ndarray           # [B] float
    seeds: np.ndarray           # [B, N_CROPS] int
    shed: np.ndarray            # [B, N_CROPS] int
    prices: np.ndarray          # [B, N_CROPS] int
    n_land: np.ndarray          # [B] int

    # **Livestock, appended with defaults on 2026-08-04.** Defaults so `agent.py` -- which builds a
    # View by hand from a live observation dict -- keeps working unchanged and simply runs crop-only.
    # A required field here would break the submission path on import.
    animal: np.ndarray = None               # [B, TILES] int, -1 where none
    fed_today: np.ndarray = None            # [B, TILES] bool
    cared_today: np.ndarray = None          # [B, TILES] bool
    consecutive_unfed: np.ndarray = None    # [B, TILES] int
    fertilizer_available: np.ndarray = None  # [B, TILES] bool
    shed_animals: np.ndarray = None         # [B, N_ANIMALS] int
    shed_wheat: np.ndarray = None           # [B] int
    carried_wheat: np.ndarray = None        # [B, MAX_EXEC_UNITS] int
    carried_animal: np.ndarray = None       # [B, MAX_EXEC_UNITS] int, -1 where none

    def __post_init__(self):
        """Fill the livestock fields with 'no animals anywhere' when a caller omits them."""
        b, t = self.kind.shape
        u = self.unit_ord.shape[1]
        blanks = dict(
            animal=lambda: np.full((b, t), -1, dtype=np.int64),
            fed_today=lambda: np.zeros((b, t), dtype=bool),
            cared_today=lambda: np.zeros((b, t), dtype=bool),
            consecutive_unfed=lambda: np.zeros((b, t), dtype=np.int64),
            fertilizer_available=lambda: np.zeros((b, t), dtype=bool),
            shed_animals=lambda: np.zeros((b, N_ANIMALS), dtype=np.int64),
            shed_wheat=lambda: np.zeros(b, dtype=np.int64),
            carried_wheat=lambda: np.zeros((b, u), dtype=np.int64),
            carried_animal=lambda: np.full((b, u), -1, dtype=np.int64),
        )
        for name, make in blanks.items():
            if getattr(self, name) is None:
                object.__setattr__(self, name, make())


@dataclass
class Decision:
    """One turn of actions for B games, in the layout `kagg.sim.game.Actions` wants."""

    unit_op: np.ndarray         # [B, MAX_EXEC_UNITS]
    unit_crop: np.ndarray       # [B, MAX_EXEC_UNITS]
    sell: np.ndarray            # [B, N_CROPS]
    buy_seed: np.ndarray        # [B, N_CROPS]
    hire: np.ndarray            # [B] bool
    buy_land: np.ndarray        # [B] bool
    # Livestock. `game.Actions` has carried these slots all along; the executor never used them.
    unit_item: np.ndarray = None    # [B, MAX_EXEC_UNITS] item index for PICKUP / PLACE
    unit_qty: np.ndarray = None     # [B, MAX_EXEC_UNITS] quantity for PICKUP
    buy_animal: np.ndarray = None   # [B, N_ANIMALS] animals to order this turn
    buy_product: np.ndarray = None  # [B, N_PRODUCTS] products to buy -- wheat, as feed

    def __post_init__(self):
        b, u = self.unit_op.shape
        if self.unit_item is None:
            object.__setattr__(self, "unit_item", np.zeros((b, u), dtype=np.int64))
        if self.unit_qty is None:
            object.__setattr__(self, "unit_qty", np.zeros((b, u), dtype=np.int64))
        if self.buy_animal is None:
            object.__setattr__(self, "buy_animal", np.zeros((b, N_ANIMALS), dtype=np.int64))
        if self.buy_product is None:
            object.__setattr__(self, "buy_product", np.zeros((b, N_PRODUCTS), dtype=np.int64))


def tile_jobs(view, plan):
    """[B, TILES] job code per tile, and [B, TILES] bool for tiles this plan actually farms."""
    day = view.day
    crop_of = plan.crop_of.astype(np.int64)
    farmed = (crop_of >= 0) & (view.kind != LOCKED)

    want = np.maximum(crop_of, 0)
    growing = np.maximum(view.crop, 0)

    # PLANT: an empty farmed tile, on its phase day, inside the planting window, with a seed held.
    have_seed = np.take_along_axis(view.seeds, want, axis=1) > 0
    phase_ok = (day % 5) == plan.phase
    plant = (
        (view.kind == EMPTY)
        & phase_ok
        & (day <= plan.stop_plant[:, None])
        & have_seed
    )

    # HARVEST: the plan says how ripe to let each crop get. For a crop that clears the tile when
    # cut, that is an age relative to `max_yield_day`; for an ongoing crop it is a unit count.
    par = np.take_along_axis(plan.harvest_par.astype(np.int64), growing, axis=1)
    age = day - view.planted_day
    ongoing = ONGOING[growing]
    ripe_age = np.maximum(MAX_YIELD_DAY[growing] + HARVEST_DELTA[par], FIRST_YIELD_DAY[growing])
    ready = np.where(
        ongoing,
        (view.yield_units >= ONGOING_THRESHOLD[par]) & (age >= FIRST_YIELD_DAY[growing]),
        (view.yield_units > 0) & (age >= ripe_age),
    )
    is_plant = view.kind == PLANT
    harvest = is_plant & ready
    water = is_plant & ~view.watered

    # ---- livestock ----------------------------------------------------------------------------
    #
    # **Ordering is the whole risk here.** `jax_frontier` bought four animals, never once built a pen
    # (`max empty pens: 0` over 240 turns), and banked $380 with the livestock sitting in the shed as
    # dead capital. So: a structure gets built first, an animal is only ordered against a *standing
    # empty* pen (in `decide`), and FEED outranks everything optional because an animal unfed two
    # nights escapes with the whole purchase price (`jax_sim.py:1159`).
    wants_structure = plan.structure_of.astype(np.int64)
    build = (view.kind == EMPTY) & (wants_structure != NO_STRUCTURE) & (view.kind != LOCKED)
    is_structure = (view.kind == COOP) | (view.kind == PASTURE)
    has_animal = view.animal >= 0

    # An empty pen is where a carried animal goes.
    place = is_structure & ~has_animal
    # Hungry first, then the free upkeep. CARE and COLLECT_FERT cost nothing but the action.
    feed = has_animal & ~view.fed_today
    care = has_animal & ~view.cared_today
    collect = has_animal & view.fertilizer_available
    animal_harvest = has_animal & (view.yield_units > 0)

    # A structure tile is `FALLOW` in `crop_of` (`plan.decode`), so `farmed` excludes it -- livestock
    # jobs are therefore scored on their own mask rather than being multiplied away below.
    livestock = np.where(
        feed, JOB_FEED,
        np.where(animal_harvest, JOB_HARVEST,
                 np.where(care, JOB_CARE,
                          np.where(collect, JOB_COLLECT,
                                   np.where(place, JOB_PLACE,
                                            np.where(build, JOB_BUILD, JOB_NONE))))),
    )

    job = np.where(
        view.kind == WEED, JOB_DIG,
        np.where(harvest, JOB_HARVEST,
                 np.where(water, JOB_WATER,
                          np.where(plant, JOB_PLANT, JOB_NONE))),
    )
    job = job * farmed
    job = np.where(livestock != JOB_NONE, livestock, job)
    return job, farmed | (livestock != JOB_NONE)


def _owner(farmed, n_live):
    """Split the farmed tiles into one contiguous block per live unit.

    Contiguous in serpentine order, so a block is a compact strip of the farm and a unit is not
    asked to cross the board between jobs.
    """
    rank = np.cumsum(farmed, axis=1) - 1
    total = np.maximum(farmed.sum(axis=1), 1)
    owner = (rank * n_live[:, None]) // total[:, None]
    return np.minimum(owner, (n_live - 1)[:, None])


def _step_toward(pos, target, kind):
    """One legal move from `pos` toward `target`; the longer axis first, then the other.

    `pos` and `target` are ``[B, U]`` serpentine positions -- every unit in the batch is routed in
    one pass, because doing it per unit made the interpreter, not the simulator, the bottleneck.
    """
    dx = (OX[target].astype(np.int16) - OX[pos]).astype(np.int16)
    dy = (OY[target].astype(np.int16) - OY[pos]).astype(np.int16)

    horiz = np.where(dx > 0, 2, 3).astype(np.int8)       # E, W
    vert = np.where(dy > 0, 1, 0).astype(np.int8)        # S, N
    first = np.where(
        (np.abs(dx) >= np.abs(dy)) & (dx != 0), horiz, np.where(dy != 0, vert, horiz)
    )
    second = np.where(first == horiz, vert, horiz)
    first = np.where((dx == 0) & (dy == 0), -1, first)
    second = np.where((dx == 0) | (dy == 0), -1, second)

    def legal(direction):
        nb = NEIGH[pos, np.maximum(direction, 0)]
        blocked = np.take_along_axis(kind, nb.astype(np.int64), axis=1) == LOCKED
        return (direction >= 0) & (nb >= 0) & ~blocked

    direction = np.where(legal(first), first, np.where(legal(second), second, -1))
    return np.where(direction >= 0, MOVE_OPS[np.maximum(direction, 0)], O.NOOP)


def decide(view, plan):
    """Choose every unit's op and the turn's market orders for a whole batch."""
    batch = view.n_units.shape[0]
    games = np.arange(batch)
    day, hour = view.day, view.hour
    units = np.arange(MAX_EXEC_UNITS)

    job, farmed = tile_jobs(view, plan)
    n_live = np.clip(view.n_units, 1, MAX_EXEC_UNITS)
    owner = _owner(farmed, n_live)
    live = units[None, :] < view.n_units[:, None]                      # [B, U]

    # Nearest outstanding job inside each unit's own block, for every unit at once.
    pos = view.unit_ord
    mine = (owner[:, None, :] == units[None, :, None]) & (job > JOB_NONE)[:, None, :]
    mine &= live[:, :, None]
    # **Carry-gated jobs.** FEED needs the unit to hold wheat (`jax_masks.py:96`) and PLACE needs the
    # animal in hand, so a unit that is not equipped must not claim the job -- otherwise it walks
    # there, cannot act, and the tile stays unserved while the animal starves.
    can_feed = (view.carried_wheat > 0)[:, :, None]
    can_place = (view.carried_animal >= 0)[:, :, None]
    is_feed = (job == JOB_FEED)[:, None, :]
    is_place = (job == JOB_PLACE)[:, None, :]
    mine &= ~(is_feed & ~can_feed)
    mine &= ~(is_place & ~can_place)

    cost = np.where(mine, DIST[pos], _BIG)                             # [B, U, TILES]
    target = cost.argmin(axis=2)
    found = np.take_along_axis(cost, target[:, :, None], axis=2)[:, :, 0] < _BIG

    target_job = np.take_along_axis(job, target, axis=1)
    at_target = pos == target
    unit_op = np.where(at_target, JOB_TO_OP[target_job], _step_toward(pos, target, view.kind))
    unit_crop = np.maximum(np.take_along_axis(plan.crop_of.astype(np.int64), target, axis=1), 0)
    unit_op = np.where(found, unit_op, O.NOOP)

    # BUILD is two different ops depending on which structure the plan asked for, so it cannot be a
    # single entry in `JOB_TO_OP`.
    wants = np.take_along_axis(plan.structure_of.astype(np.int64), target, axis=1)
    building = found & at_target & (target_job == JOB_BUILD)
    unit_op = np.where(building & (wants == COOP_GENE_KIND), O.BUILD_COOP, unit_op)

    # PLACE carries the animal's item index; the reference reads which animal from the unit's hand.
    unit_item = np.zeros_like(unit_op)
    unit_qty = np.zeros_like(unit_op)
    placing = found & at_target & (target_job == JOB_PLACE)
    unit_item = np.where(placing, ANIMAL_ITEM_BASE + np.maximum(view.carried_animal, 0), unit_item)

    # ---- the dawn PICKUP window ----------------------------------------------------------------
    #
    # Every unit respawns on the shed at dawn (`ops.SHED_TILES`), so hour 0 is a free PICKUP with no
    # walking. Fetching feed mid-day is what turned `jax_frontier` into a 70.5% PICKUP loop, so it is
    # only ever done here. Units are claimed lowest-index first: animals to place, then feed wheat.
    at_shed = np.isin(pos, SHED_ORDS) & live
    has_animal_tiles = view.animal >= 0
    n_pens_free = (((view.kind == COOP) | (view.kind == PASTURE)).sum(axis=1)
                   - has_animal_tiles.sum(axis=1))
    shed_stock = view.shed_animals.sum(axis=1)
    want_collect = np.minimum(np.maximum(n_pens_free, 0), shed_stock)          # [B]
    herd_size = (view.animal >= 0).sum(axis=1)
    want_wheat = np.where(herd_size > 0, plan.feed_wheat * np.maximum(herd_size, 1), 0)

    rank = np.cumsum(at_shed, axis=1) - 1                                     # 0-based among at-shed
    # **NOT gated on being idle.** The first version required `~found`, so a unit only fetched feed if
    # it had no other job -- and at dawn every unit has watering or planting to do. Nobody ever picked
    # up wheat, `carrying_wheat` was never true, FEED could never be legal, and the herd starved: a
    # measured 14 pens built, 3 animals bought, **0 FEED**, $30 in the bank. Keeping an animal alive
    # outranks watering a plant, so the lowest-indexed units are claimed for it whatever else is going
    # on. `hungry` is what makes this bounded -- once the herd is fed the claim stops.
    hungry = (has_animal_tiles & ~view.fed_today).sum(axis=1)
    collect_animal = at_shed & (rank < want_collect[:, None]) & (view.carried_animal < 0)
    n_carriers = np.minimum(np.maximum(hungry, 0), 3)
    fetch_wheat = (at_shed & ~collect_animal
                   & (rank >= want_collect[:, None])
                   & (rank < (want_collect + n_carriers)[:, None])
                   & (view.shed_wheat[:, None] > 0) & (want_wheat[:, None] > 0)
                   & (view.carried_wheat <= 0))

    first_animal = np.argmax(view.shed_animals > 0, axis=1)
    unit_op = np.where(collect_animal, O.PICKUP, unit_op)
    unit_item = np.where(collect_animal, ANIMAL_ITEM_BASE + first_animal[:, None], unit_item)
    unit_qty = np.where(collect_animal, 1, unit_qty)

    unit_op = np.where(fetch_wheat, O.PICKUP, unit_op)
    unit_item = np.where(fetch_wheat, WHEAT_ITEM, unit_item)
    unit_qty = np.where(fetch_wheat, np.minimum(want_wheat, 10)[:, None], unit_qty)

    # Never ask to plant a crop the farm has no seed left for: the reference silently drops
    # *every* PLANT for that crop, which would waste the turn for several units at once. Units
    # claim seeds in index order, which is also the order the simulator spends them.
    seeds_left = view.seeds.copy()
    planting = found & at_target & (target_job == JOB_PLANT)
    for u in range(MAX_EXEC_UNITS):
        want = planting[:, u]
        if not want.any():
            continue
        crop = unit_crop[:, u]
        allowed = want & (seeds_left[games, crop] > 0)
        np.add.at(seeds_left, (games[allowed], crop[allowed]), -1)
        unit_op[:, u] = np.where(want & ~allowed, O.NOOP, unit_op[:, u])

    # ---- market -------------------------------------------------------------------------
    block = min(day // BLOCK_DAYS, N_BLOCKS - 1)
    dumping = day >= plan.dump_day
    tick = (hour % np.maximum(plan.sell_every, 1)) == 0

    price_ok = view.prices >= (plan.floor_frac * BASE_PRICE[None, :])
    qty = plan.sell_qty[:, block, :]
    qty = np.where(dumping[:, None], view.shed, np.where(price_ok, qty, 0))
    sell = np.where(tick[:, None], np.minimum(qty, view.shed), 0).astype(np.int64)

    # One crop's seeds per turn, rotating, so the fixed 8-slot order list always fits.
    buy_seed = np.zeros((batch, N_CROPS), dtype=np.int64)
    c = hour % N_CROPS
    upcoming = (
        (view.kind == EMPTY)
        & farmed
        & (plan.crop_of == c)
        & (day <= plan.stop_plant[:, None])
        & (((plan.phase - day) % 5) <= 1)      # due today or tomorrow
    )
    need = np.maximum(upcoming.sum(axis=1) - view.seeds[:, c], 0)
    budget = np.maximum(view.money - plan.seed_reserve, 0.0)
    buy_seed[:, c] = np.minimum(need, np.floor(budget / SEED_COST[c])).astype(np.int64)

    target_hands = plan.hires[games, min(day, plan.hires.shape[1] - 1)]
    hire = (view.n_units - 1) < target_hands

    slot = np.minimum(view.n_land, plan.land_day.shape[1] - 1)
    buy_land = (view.n_land < plan.land_day.shape[1]) & (day >= plan.land_day[games, slot])

    # ---- livestock orders ------------------------------------------------------------------------
    #
    # **An animal is only ordered against a standing empty pen.** This single condition is the fix for
    # `jax_frontier`, which bought its herd on day 0 against pens it never built and wrote off ~$1,400.
    # The shed count is subtracted too, or a slow placement queue would keep re-ordering.
    buy_animal = np.zeros((batch, N_ANIMALS), dtype=np.int64)
    housing = np.maximum(n_pens_free - shed_stock, 0)
    stocking = day >= plan.stock_day
    for a in range(N_ANIMALS):
        placed = (view.animal == a).sum(axis=1) + view.shed_animals[:, a]
        room = np.minimum(np.maximum(plan.herd[:, a] - placed, 0), housing)
        afford = np.floor(np.maximum(view.money, 0.0) / ANIMAL_COST[a]).astype(np.int64)
        take = np.where(stocking, np.minimum(room, afford), 0)
        buy_animal[:, a] = take
        housing = np.maximum(housing - take, 0)          # one pen per animal, first species first

    # Wheat is *bought*, not grown, when it is feed: the leaders buy 967 units a season for 14
    # animals. `feed_wheat` is units per animal, so the order tops the shed up to that.
    buy_product = np.zeros((batch, N_PRODUCTS), dtype=np.int64)
    short = np.maximum(want_wheat - view.shed_wheat, 0)
    wheat_budget = np.floor(np.maximum(view.money - plan.seed_reserve, 0.0) / WHEAT_PRICE_CAP)
    buy_product[:, WHEAT_ITEM] = np.minimum(short, wheat_budget.astype(np.int64))

    return Decision(
        unit_op=unit_op,
        unit_crop=unit_crop,
        sell=sell,
        buy_seed=buy_seed,
        hire=hire,
        buy_land=buy_land,
        unit_item=unit_item,
        unit_qty=unit_qty,
        buy_animal=buy_animal,
        buy_product=buy_product,
    )
