"""Batched unit operations: what a farmer or hand does on the tile it stands on.

Every game in the batch applies the *same-indexed* unit's action simultaneously, with each game
free to choose a different op. So the op dispatch becomes one masked update per op rather than a
branch per unit -- nine cheap vector writes instead of B*U Python branches.

Ports of `_apply_unit_action`. The rules that are easy to get wrong, and are therefore tested:

- **Movement is blocked by the board edge and by LOCKED tiles**, and silently does nothing
  otherwise. A no-op move still burns the unit's action for the turn.
- **WATER carries the yield bonus for non-ongoing crops**, but only inside the window
  `(max_yield_day + 1) // 2 <= age <= max_yield_day`, and only once per day.
- **Fertilizer doubles that bonus**, but only on a day the tile is watered -- basic needs first.
- **HARVEST clears the tile for non-ongoing crops** and leaves ongoing ones standing.
"""

import numpy as np

from kagg.sim.tiles import (
    BOARD,
    EMPTY,
    LOCKED,
    MAX_YIELD,
    MAX_YIELD_DAY,
    NO_CROP,
    ONGOING,
    PLANT,
    WEED,
)

# Op codes. NOOP covers both PASS and any action that turns out to be illegal.
NOOP, NORTH, SOUTH, EAST, WEST, WATER, HARVEST, PLANT_OP, DIG = range(9)

# (dx, dy) per op, indexed by op code; y grows downward, matching FARMER_MOVES.
_DX = np.zeros(9, dtype=np.int64)
_DY = np.zeros(9, dtype=np.int64)
_DX[EAST], _DX[WEST] = 1, -1
_DY[SOUTH], _DY[NORTH] = 1, -1


def move(state, pos, ops):
    """Apply movement ops. `pos` is [B, 2] as (x, y); returns the new positions.

    A move off the board or onto a LOCKED tile is silently ignored, exactly as the reference does,
    so the unit stays put and loses the turn.
    """
    pos = np.array(pos, dtype=np.int64, copy=True)
    ops = np.asarray(ops)

    nx = pos[:, 0] + _DX[ops]
    ny = pos[:, 1] + _DY[ops]
    in_bounds = (nx >= 0) & (nx < BOARD) & (ny >= 0) & (ny < BOARD)

    # Clip only for the lookup; out-of-bounds games are masked out immediately after.
    target = np.clip(ny, 0, BOARD - 1) * BOARD + np.clip(nx, 0, BOARD - 1)
    unlocked = state.kind[np.arange(state.batch), target] != LOCKED

    is_move = (ops >= NORTH) & (ops <= WEST)
    legal = is_move & in_bounds & unlocked
    pos[:, 0] = np.where(legal, nx, pos[:, 0])
    pos[:, 1] = np.where(legal, ny, pos[:, 1])
    return pos


def _tile_index(pos):
    return pos[:, 1] * BOARD + pos[:, 0]


def water(state, pos, active, day):
    """Apply WATER where `active`. Returns nothing; mutates `state`.

    The non-ongoing yield bonus is the subtle part: it lands only inside the watering window and
    only once per day, and fertilizer doubles it.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)

    kind = state.kind[games, idx]
    already = state.watered_today[games, idx]
    doable = active & (kind == PLANT) & ~already
    if not doable.any():
        return

    state.watered_today[games, idx] = np.where(doable, True, state.watered_today[games, idx])

    crop = np.where(doable, state.crop[games, idx], 0)
    age = day - state.planted_day[games, idx]
    window_start = (MAX_YIELD_DAY[crop] + 1) // 2
    in_window = (age >= window_start) & (age <= MAX_YIELD_DAY[crop])
    gains = doable & ~ONGOING[crop] & in_window

    fertilized = state.fertilized_until_day[games, idx] >= day
    bonus = np.where(fertilized, 2, 1)
    updated = np.minimum(MAX_YIELD[crop], state.yield_units[games, idx] + bonus)
    state.yield_units[games, idx] = np.where(gains, updated, state.yield_units[games, idx])


def harvest(state, pos, active, day, carried):
    """Apply HARVEST where `active`, adding units to `carried` [B, N_CROPS].

    Non-ongoing crops clear the tile; ongoing crops stay and keep producing. Nothing is harvested
    before `first_yield_day`, which is what stops an immature ongoing crop being stripped.
    """
    from kagg.sim.tiles import FIRST_YIELD_DAY

    games = np.arange(state.batch)
    idx = _tile_index(pos)

    kind = state.kind[games, idx]
    units = state.yield_units[games, idx]
    crop = np.where(kind == PLANT, state.crop[games, idx], 0)
    age = day - state.planted_day[games, idx]

    doable = active & (kind == PLANT) & (units > 0) & (age >= FIRST_YIELD_DAY[crop])
    if not doable.any():
        return carried

    np.add.at(carried, (games[doable], crop[doable]), units[doable])
    state.yield_units[games, idx] = np.where(doable, 0, state.yield_units[games, idx])

    # Harvesting a non-ongoing crop takes the plant with it.
    cleared = doable & ~ONGOING[crop]
    state.kind[games, idx] = np.where(cleared, EMPTY, state.kind[games, idx])
    state.crop[games, idx] = np.where(cleared, NO_CROP, state.crop[games, idx])
    state.max_lifespan_step[games, idx] = np.where(cleared, -1, state.max_lifespan_step[games, idx])
    return carried


def dig(state, pos, active):
    """Apply DIG where `active`: clears weeds and plants, leaving an empty tile."""
    games = np.arange(state.batch)
    idx = _tile_index(pos)

    kind = state.kind[games, idx]
    doable = active & ((kind == WEED) | (kind == PLANT))

    state.kind[games, idx] = np.where(doable, EMPTY, state.kind[games, idx])
    state.crop[games, idx] = np.where(doable, NO_CROP, state.crop[games, idx])
    state.yield_units[games, idx] = np.where(doable, 0, state.yield_units[games, idx])
    state.max_lifespan_step[games, idx] = np.where(doable, -1, state.max_lifespan_step[games, idx])


def plant(state, pos, active, crop_id, day, turns_per_day=24):
    """Apply PLANT where `active`, on empty tiles only.

    Seed availability is the caller's responsibility: the reference validates PLANT atomically per
    crop across all of a player's units, dropping every request for a crop when they exceed the
    seeds held, and that check needs the whole turn's actions at once.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)

    doable = active & (state.kind[games, idx] == EMPTY)
    if not doable.any():
        return

    mask = np.zeros_like(state.kind, dtype=bool)
    mask[games[doable], idx[doable]] = True
    state.plant(mask, crop_id, day, turns_per_day)
