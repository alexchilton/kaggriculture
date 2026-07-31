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
    FIRST_YIELD_DAY,
    HARVEST_DELTA,
    MAX_YIELD_DAY,
    N_BLOCKS,
    N_CROPS,
    ONGOING,
    ONGOING_THRESHOLD,
    SEED_COST,
    TILES,
)

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

JOB_NONE, JOB_DIG, JOB_HARVEST, JOB_WATER, JOB_PLANT = range(5)
JOB_TO_OP = np.array([O.NOOP, O.DIG, O.HARVEST, O.WATER, O.PLANT_OP], dtype=np.int64)

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


@dataclass
class Decision:
    """One turn of actions for B games, in the layout `kagg.sim.game.Actions` wants."""

    unit_op: np.ndarray         # [B, MAX_EXEC_UNITS]
    unit_crop: np.ndarray       # [B, MAX_EXEC_UNITS]
    sell: np.ndarray            # [B, N_CROPS]
    buy_seed: np.ndarray        # [B, N_CROPS]
    hire: np.ndarray            # [B] bool
    buy_land: np.ndarray        # [B] bool


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

    job = np.where(
        view.kind == WEED, JOB_DIG,
        np.where(harvest, JOB_HARVEST,
                 np.where(water, JOB_WATER,
                          np.where(plant, JOB_PLANT, JOB_NONE))),
    )
    return job * farmed, farmed


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
    cost = np.where(mine, DIST[pos], _BIG)                             # [B, U, TILES]
    target = cost.argmin(axis=2)
    found = np.take_along_axis(cost, target[:, :, None], axis=2)[:, :, 0] < _BIG

    target_job = np.take_along_axis(job, target, axis=1)
    at_target = pos == target
    unit_op = np.where(at_target, JOB_TO_OP[target_job], _step_toward(pos, target, view.kind))
    unit_crop = np.maximum(np.take_along_axis(plan.crop_of.astype(np.int64), target, axis=1), 0)
    unit_op = np.where(found, unit_op, O.NOOP)

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

    return Decision(
        unit_op=unit_op,
        unit_crop=unit_crop,
        sell=sell,
        buy_seed=buy_seed,
        hire=hire,
        buy_land=buy_land,
    )
