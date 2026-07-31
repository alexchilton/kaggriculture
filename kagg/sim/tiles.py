"""Batched tile state: struct-of-arrays over [B, TILES], and the daily transitions.

Every tile in every game is a column in a handful of parallel integer arrays. No dicts, no
`None`, no per-tile Python objects -- those are what make the reference environment slow, and
they are also what makes it impossible to feed a GPU.

The two transitions here are the ones that run every night and decide what a farm is worth:

- `daily_refresh_plants` -- watering enforcement, ongoing-crop production, and the lifespan clock.
  This is where the rule that cost this project a day-one wrong turn lives: production stops once
  `production_count > max_yield`, so the cap counts **events**, not units per day.
- `decay_plants` -- what happens after a plant is finished, losing a unit every *other* step until
  the tile becomes a weed.

Both are ports of `kaggriculture` and are gated on `tests/test_sim_tiles.py`, which drives random
farm states through this and through the reference side by side.
"""

import numpy as np

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

BOARD = 10
TILES = BOARD * BOARD
TURNS_PER_DAY = 24

# Tile kinds. LOCKED and EMPTY are sentinels rather than absent values, so the arrays stay dense.
EMPTY, LOCKED, WEED, PLANT, COOP, PASTURE = range(6)

CROPS = list(kg.CROPS)
CROP_INDEX = {name: i for i, name in enumerate(CROPS)}
NO_CROP = -1

# Per-crop constants as arrays, indexed by crop id, so the transitions are branch-free.
FIRST_YIELD_DAY = np.array([kg.CROPS[c]["first_yield_day"] for c in CROPS], dtype=np.int64)
MAX_YIELD_DAY = np.array([kg.CROPS[c]["max_yield_day"] for c in CROPS], dtype=np.int64)
INTERVAL = np.array([kg.CROPS[c]["interval"] for c in CROPS], dtype=np.int64)
MAX_YIELD = np.array([kg.CROPS[c]["max_yield"] for c in CROPS], dtype=np.int64)
ONGOING = np.array([kg.CROPS[c]["ongoing"] for c in CROPS], dtype=bool)


class TileState:
    """Struct-of-arrays tile state for a batch of B games (one farm each).

    Field names deliberately mirror the reference environment's tile dict keys, so a reader can
    check a transition against `kaggriculture.py` without translating names.
    """

    __slots__ = (
        "kind", "crop", "planted_day", "watered_today", "consecutive_unwatered",
        "yield_units", "max_lifespan_step", "fertilized_until_day",
    )

    def __init__(self, batch):
        z = lambda dtype=np.int64: np.zeros((batch, TILES), dtype=dtype)  # noqa: E731
        self.kind = np.full((batch, TILES), EMPTY, dtype=np.int64)
        self.crop = np.full((batch, TILES), NO_CROP, dtype=np.int64)
        self.planted_day = z()
        self.watered_today = z(bool)
        self.consecutive_unwatered = z()
        self.yield_units = z()
        self.max_lifespan_step = np.full((batch, TILES), -1, dtype=np.int64)
        self.fertilized_until_day = np.full((batch, TILES), -1, dtype=np.int64)

    @property
    def batch(self):
        return self.kind.shape[0]

    def plant(self, mask, crop_id, day, turns_per_day=TURNS_PER_DAY):
        """Plant `crop_id` wherever `mask` is set. Mirrors `_new_plant`."""
        ongoing = ONGOING[crop_id]
        self.kind = np.where(mask, PLANT, self.kind)
        self.crop = np.where(mask, crop_id, self.crop)
        self.planted_day = np.where(mask, day, self.planted_day)
        self.watered_today = np.where(mask, False, self.watered_today)
        # Planting day counts as unwatered, exactly as the reference does.
        self.consecutive_unwatered = np.where(mask, 1, self.consecutive_unwatered)
        self.yield_units = np.where(mask, 0 if ongoing else 1, self.yield_units)
        lifespan = -1 if ongoing else (day + int(MAX_YIELD_DAY[crop_id]) + 1) * turns_per_day
        self.max_lifespan_step = np.where(mask, lifespan, self.max_lifespan_step)
        self.fertilized_until_day = np.where(mask, -1, self.fertilized_until_day)


def decay_plants(state, step):
    """Port of `_decay_plants`: a finished plant loses a unit every *other* step, then weeds.

    The parity trap is the parity check itself -- `(step - mls) % 2 != 0` means decay lands on
    alternate steps counted from the lifespan boundary, not on even steps.
    """
    mls = state.max_lifespan_step
    due = (state.kind == PLANT) & (mls >= 0) & (step >= mls) & (((step - mls) % 2) == 0)
    state.yield_units = np.where(due, state.yield_units - 1, state.yield_units)

    dead = due & (state.yield_units <= 0)
    state.kind = np.where(dead, WEED, state.kind)
    state.crop = np.where(dead, NO_CROP, state.crop)
    state.yield_units = np.where(dead, 0, state.yield_units)
    state.max_lifespan_step = np.where(dead, -1, state.max_lifespan_step)
    return state


def daily_refresh_plants(state, current_day, turns_per_day=TURNS_PER_DAY):
    """Port of `_daily_refresh_plants`, run at the end of each day.

    Order matters and follows the reference exactly: update the unwatered streak, kill anything
    unwatered twice running, then produce for ongoing crops only.
    """
    next_day = current_day + 1
    is_plant = state.kind == PLANT
    was_watered = state.watered_today & is_plant

    state.consecutive_unwatered = np.where(
        is_plant,
        np.where(was_watered, 0, state.consecutive_unwatered + 1),
        state.consecutive_unwatered,
    )
    state.watered_today = np.where(is_plant, False, state.watered_today)

    # Two consecutive unwatered days and the plant becomes a weed.
    died = is_plant & (state.consecutive_unwatered >= 2)
    state.kind = np.where(died, WEED, state.kind)
    state.crop = np.where(died, NO_CROP, state.crop)
    state.yield_units = np.where(died, 0, state.yield_units)
    state.max_lifespan_step = np.where(died, -1, state.max_lifespan_step)

    alive = (state.kind == PLANT) & ~died
    crop = np.where(alive, state.crop, 0)  # index safely; masked out below
    ongoing = ONGOING[crop] & alive
    if not ongoing.any():
        return state

    days_since = next_day - state.planted_day - FIRST_YIELD_DAY[crop]
    interval = np.maximum(INTERVAL[crop], 1)
    on_schedule = ongoing & (days_since >= 0) & ((days_since % interval) == 0)

    # The rule that matters: production stops once the *count of events* passes max_yield.
    production_count = np.where(on_schedule, days_since // interval + 1, 0)
    produces = on_schedule & (production_count <= MAX_YIELD[crop])

    # Fertilizer only pays on a day the tile was actually watered -- basic needs first.
    fertilized = produces & was_watered & (state.fertilized_until_day >= current_day)
    gain = np.where(fertilized, 2, 1)
    state.yield_units = np.where(
        produces, np.minimum(MAX_YIELD[crop], state.yield_units + gain), state.yield_units
    )

    # The final scheduled production starts the lifespan clock.
    final = produces & (production_count == MAX_YIELD[crop])
    state.max_lifespan_step = np.where(
        final, (next_day + 1) * turns_per_day, state.max_lifespan_step
    )
    return state
