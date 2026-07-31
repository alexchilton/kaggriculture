"""Batched farm bookkeeping: money, seeds, shed, units, land.

Everything a player owns that is not a tile. Same struct-of-arrays discipline as `TileState`:
fixed-width arrays with masked updates, so B games advance together.

The fiddly rules, all ported from `kaggriculture` and tested against it:

- **Hiring cost is Fibonacci and resets every morning.** `_fib(0)=1, _fib(1)=1, _fib(2)=2, ...`
  indexed by hires already made *today*. Paying it 30 times is what makes a big crew ruinous, and
  is why the economics doc's "labour is nearly free" claim had to be corrected.
- **Land unlocks in a fixed order** (NE, SW, SE) at 1000/2000/4000, and only in that order.
- **The shed caps total items, not items per product**, and end-of-day overflow is destroyed.
- **Carried inventory is uncapped during a day** but emptied into the shed each night.
"""

import numpy as np

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim.market import N_PRODUCTS, PRODUCT_INDEX
from kagg.sim.tiles import BOARD, CROPS, EMPTY, LOCKED, TILES

N_CROPS = len(CROPS)
MAX_UNITS = 24          # farmer plus up to 23 hands; the fee makes more than ~15 absurd
SHED_CAP = 100
LAND_PRICES = np.array(kg.LAND_PRICES, dtype=np.float64)
N_LAND = len(kg.LAND_PRICES)

SEED_COST = np.array([kg.CROPS[c]["seed"] for c in CROPS], dtype=np.float64)
CROP_TO_PRODUCT = np.array([PRODUCT_INDEX[c] for c in CROPS], dtype=np.int64)

# Fibonacci hire costs, precomputed. Index is hires already made today.
_FIB = [1, 1]
while len(_FIB) < MAX_UNITS + 2:
    _FIB.append(_FIB[-1] + _FIB[-2])
HIRE_COST = np.array(_FIB[:MAX_UNITS + 1], dtype=np.float64)


def shed_access_tiles(board=BOARD):
    """The four inner-corner tiles around the shed, in NWSE order."""
    half = board // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def default_spawn(board=BOARD):
    """First shed-access tile inside the always-unlocked NW quadrant."""
    half = board // 2
    return (half - 1, half - 1)


class FarmState:
    """Per-game farm bookkeeping for a batch of B games."""

    __slots__ = (
        "money", "seeds", "shed", "carried", "unit_pos", "n_units",
        "hires_today", "n_land",
    )

    def __init__(self, batch, starting_money=3000.0):
        self.money = np.full(batch, starting_money, dtype=np.float64)
        self.seeds = np.zeros((batch, N_CROPS), dtype=np.int64)
        self.shed = np.zeros((batch, N_PRODUCTS), dtype=np.int64)
        # Per-unit carried inventory. Uncapped during the day, emptied every night.
        self.carried = np.zeros((batch, MAX_UNITS, N_PRODUCTS), dtype=np.int64)
        self.unit_pos = np.zeros((batch, MAX_UNITS, 2), dtype=np.int64)
        self.unit_pos[:, :, 0] = default_spawn()[0]
        self.unit_pos[:, :, 1] = default_spawn()[1]
        self.n_units = np.ones(batch, dtype=np.int64)     # the farmer always exists
        self.hires_today = np.zeros(batch, dtype=np.int64)
        self.n_land = np.zeros(batch, dtype=np.int64)     # extra quadrants beyond NW

    @property
    def batch(self):
        return self.money.shape[0]

    def unit_mask(self):
        """[B, MAX_UNITS] bool: which unit slots are live this turn."""
        return np.arange(MAX_UNITS)[None, :] < self.n_units[:, None]


def hire(state, want):
    """Hire one hand where `want`, if affordable. Mirrors `_do_hire`.

    Cost is `HIRE_COST[hires_today]`, so it climbs steeply within a day and resets overnight.
    """
    cost = HIRE_COST[np.minimum(state.hires_today, MAX_UNITS)]
    doable = want & (state.money >= cost) & (state.n_units < MAX_UNITS)

    state.money = np.where(doable, state.money - cost, state.money)
    state.hires_today = np.where(doable, state.hires_today + 1, state.hires_today)

    # New hands spawn on a shed-access tile; the reference balances across the four, but a hand's
    # first action is almost always a move, so the NW tile is used for all of them here. This is
    # the one place the simulator is deliberately approximate -- see `docs/` and the parity notes.
    spawn = default_spawn()
    idx = np.minimum(state.n_units, MAX_UNITS - 1)
    games = np.arange(state.batch)
    state.unit_pos[games[doable], idx[doable], 0] = spawn[0]
    state.unit_pos[games[doable], idx[doable], 1] = spawn[1]
    state.carried[games[doable], idx[doable]] = 0
    state.n_units = np.where(doable, state.n_units + 1, state.n_units)
    return doable


def buy_land(state, tiles, want):
    """Unlock the next quadrant where `want`, if affordable. Mirrors `_do_buy_land`.

    Quadrants unlock in the fixed order NE, SW, SE, so which tiles become available is fully
    determined by how many have been bought already.
    """
    have = np.minimum(state.n_land, N_LAND - 1)
    cost = LAND_PRICES[have]
    doable = want & (state.n_land < N_LAND) & (state.money >= cost)
    if not doable.any():
        return doable

    state.money = np.where(doable, state.money - cost, state.money)

    for slot in range(N_LAND):
        buying = doable & (state.n_land == slot)
        if not buying.any():
            continue
        quadrant = kg.LAND_ORDER[slot]
        mask = _quadrant_mask(quadrant)
        newly = buying[:, None] & mask[None, :] & (tiles.kind == LOCKED)
        tiles.kind = np.where(newly, EMPTY, tiles.kind)

    state.n_land = np.where(doable, state.n_land + 1, state.n_land)
    return doable


def _quadrant_mask(name, board=BOARD):
    """[TILES] bool for one quadrant, using the reference's own naming."""
    half = board // 2
    mask = np.zeros(TILES, dtype=bool)
    for y in range(board):
        for x in range(board):
            q = ("N" if y < half else "S") + ("W" if x < half else "E")
            if q == name:
                mask[y * board + x] = True
    return mask


def buy_seeds(state, crop_id, counts):
    """Buy `counts` seeds of one crop where affordable, one unit at a time in effect.

    Seeds are a fixed price, so the whole order settles at once: buy as many as the bank allows.
    """
    cost = SEED_COST[crop_id]
    affordable = np.minimum(counts, np.floor_divide(state.money, cost).astype(np.int64))
    affordable = np.maximum(affordable, 0)

    state.money -= affordable * cost
    state.seeds[:, crop_id] += affordable
    return affordable


def drop_to_shed(state, unit_indices=None):
    """Move carried inventory into the shed, respecting the total cap. Mirrors `_drop_inventories_to_shed`.

    The reference walks units in order and items in insertion order, filling until the shed is
    full and **destroying** the remainder. Order matters when the cap binds, so this walks the
    same way rather than distributing proportionally.
    """
    games = np.arange(state.batch)
    for u in range(MAX_UNITS if unit_indices is None else len(unit_indices)):
        unit = u if unit_indices is None else unit_indices[u]
        for p in range(N_PRODUCTS):
            have = state.carried[games, unit, p]
            if not have.any():
                continue
            room = np.maximum(0, SHED_CAP - state.shed.sum(axis=1))
            take = np.minimum(have, room)
            state.shed[:, p] += take
            state.carried[games, unit, p] = 0     # overflow is destroyed, not kept
    return state


def end_of_day(state):
    """Reset the per-day counters. Units return to spawn and hands are dismissed."""
    drop_to_shed(state)
    spawn = default_spawn()
    state.unit_pos[:, :, 0] = spawn[0]
    state.unit_pos[:, :, 1] = spawn[1]
    state.n_units[:] = 1
    state.hires_today[:] = 0
    state.carried[:] = 0
    return state
