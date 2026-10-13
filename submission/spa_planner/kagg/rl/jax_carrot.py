"""A carrot fleet that runs inside the compiled rollout.

A port of the public Kaggle baseline `makimakiai/kaggriculture-carrot-fleet-simple-python-baseline`
to array operations, for the same reason `jax_heuristic` exists: a Python agent over dict
observations cannot run inside `jax.lax.scan`, and a `pure_callback` per turn would serialise 256
games through Python every step.

**Why this one, of the public notebooks.** It is 205 lines against `jax_heuristic`'s 198, so it is
the only published agent in the same size class as an existing port -- the herd-focused ones are
1,700+. It is also *different in kind* from what the pool already contains: `jax_heuristic` commits
to melon on 16 tiles, this one carpets every unlocked tile with carrot and harvests on a three-day
cycle. Opponent diversity in this project has repeatedly turned out to be diversity of crop dial
rather than of play style, and `CLAUDE.md` names that as a trap; a short cycle against a long one is
a real difference in tempo, not a different dial setting.

**Credit.** The strategy, the constants and the priority ordering are the notebook author's. What is
here is the translation to a batched jit-safe form.

**Two deviations from the original, both forced by the interface rather than chosen.**

- *Job allocation.* The Python walks units in order and lets each claim the nearest unclaimed job
  from a shared `free_tasks` set. That is sequential state and does not vectorise. As in
  `jax_heuristic`, each unit takes the `i`-th nearest job instead: no shared state, same
  non-overlapping allocation in the common case, and when the crew outnumbers the jobs the cost is
  a unit walking further than it needed to -- never two units fighting over one tile.
- *Hiring cadence.* The original emits `TARGET_HANDS - len(hands)` HIRE orders in a single turn at
  `hour == 0`.

  **This docstring previously claimed that was inexpressible, and that was wrong.** It read the
  reference's "Atomic orders (HIRE, BUY_LAND): handle once, in player order" as one hire per turn.
  That comment sits inside `for i in range(max_len)` over the *order slots*
  (`reference/kaggriculture.py:538`); "atomic" means the slot resolves once and is then spent so the
  per-unit SELL/BUY lockstep skips it. Each slot holding a HIRE fires its own hire, so up to
  `maxMarketOrdersPerTurn` (10) hires per turn are legal -- and `senkin13` opens with two, banking
  $145,034 (`docs/the_winners_are_open_loop_2026-08-04.md`).

  `Actions.hire` is an integer count as of 2026-08-04, so the original cadence *is* now expressible.
  This port still hires on any turn while below target, which reaches the same crew; emitting the
  full shortfall at `hour == 0` would now be the faithful version. Pinned by
  `tests/test_multiple_hires_per_turn.py`.
"""

import jax
import jax.numpy as jnp

from kagg.sim import jax_sim as J
from kagg.sim import ops as O
from kagg.sim.tiles import CROP_INDEX, EMPTY, PLANT, WEED

CARROT = CROP_INDEX["CARROT"]

# The author's constants, kept at their published values.
#
# `HARVEST_AGE = 3` is the notebook's `MAX_YIELD_DAY`, and it coincides exactly with the
# simulator's `MAX_YIELD_DAY[CARROT] = 3` -- so this harvests at the *end* of the yield window,
# which is what "harvests at full yield" in the notebook's docstring means. Carrot's
# `FIRST_YIELD_DAY` is 2, so waiting the extra day is a deliberate choice to take the whole crop
# rather than an off-by-one.
HARVEST_AGE = 3
LAST_PLANT_DAY = 26
TARGET_HANDS = 6
SEED_COST = 20
# The author's cash buffer: seed is bought out of `money - 100`, so the farm never spends itself to
# exactly zero and keeps enough to hire the next morning.
CASH_BUFFER = 100.0

_XS = jnp.arange(J.BOARD * J.BOARD) % J.BOARD
_YS = jnp.arange(J.BOARD * J.BOARD) // J.BOARD
_BIG = jnp.int32(10_000)


def _step_toward(pos, target):
    """One legal step along the larger axis first, ties preferring horizontal.

    The original routes with a BFS that respects LOCKED tiles. A BFS per unit per turn does not
    vectorise, and `jax_heuristic` already established the greedy step as the routing this project
    uses -- so the two scripted opponents route the same way and a difference between them is a
    difference of strategy rather than of pathfinder.
    """
    dx = target[..., 0] - pos[..., 0]
    dy = target[..., 1] - pos[..., 1]
    horiz = (dx != 0) & ((jnp.abs(dx) >= jnp.abs(dy)) | (dy == 0))
    op = jnp.where(
        horiz,
        jnp.where(dx > 0, O.EAST, O.WEST),
        jnp.where(dy != 0, jnp.where(dy > 0, O.SOUTH, O.NORTH), O.NOOP),
    )
    return op.astype(jnp.int32)


def _nth_nearest(pos, candidate, rank):
    """Flat index of the `rank`-th nearest true entry in `candidate`, or -1 if there are too few."""
    dist = jnp.abs(_XS[None, None, :] - pos[..., 0:1]) + jnp.abs(_YS[None, None, :] - pos[..., 1:2])
    dist = jnp.where(candidate, dist, _BIG)
    order = jnp.argsort(dist, axis=-1)
    idx = jnp.take_along_axis(order, jnp.full(pos.shape[:-1] + (1,), rank), axis=-1)[..., 0]
    ok = jnp.take_along_axis(dist, idx[..., None], axis=-1)[..., 0] < _BIG
    return jnp.where(ok, idx, -1)


def actions(state):
    """A `jax_sim.Actions` for both seats. Only seat selection decides who actually uses it."""
    t, farm = state.tiles, state.farm
    b = farm.money.shape[0]
    day = (state.step_index // J.TURNS_PER_DAY)[:, None]            # [B, 1]

    # ---- the board, as the author's `_jobs` reads it -----------------------------------------
    is_carrot = (t.kind == PLANT) & (t.crop == CARROT)
    age = day[..., None] - t.planted_day
    ripe = is_carrot & (age >= HARVEST_AGE) & (t.yield_units > 0)
    # `watered_today` is int 0/1 rather than bool so the Tiles struct shares one dtype.
    dry = is_carrot & (t.watered_today == 0) & ~ripe
    # The author splits watering into two priorities: a plant that missed yesterday is as urgent as
    # a weed, because two dry days kill it outright.
    urgent_dry = dry & (t.consecutive_unwatered > 0)
    weed = t.kind == WEED
    free = t.kind == EMPTY

    # ---- units --------------------------------------------------------------------------------
    pos = farm.unit_pos                                             # [B, P, U, 2]
    live = jnp.arange(J.MAX_UNITS)[None, None, :] < farm.n_units[..., None]
    flat = pos[..., 1] * J.BOARD + pos[..., 0]                      # [B, P, U]
    seeds_left = farm.seeds[..., CARROT]                            # [B, P]
    # `day` is [B, 1] and `seeds_left[..., None]` is [B, P, 1], so `day` must gain the unit axis
    # explicitly. Left implicit this broadcasts *by coincidence* whenever `batch == players == 2`
    # and raises for every other batch size -- and a two-game test is exactly the case that cannot
    # see it. Same shape as the parity harness's `n_units = 1`.
    can_plant = (day[..., None] <= LAST_PLANT_DAY) & (seeds_left[..., None] > 0)

    def under(field):
        """The value of a board field on the tile each unit is standing on."""
        return jnp.take_along_axis(field[:, :, None, :].repeat(J.MAX_UNITS, axis=2),
                                   flat[..., None], axis=-1)[..., 0]

    here_weed, here_urgent, here_ripe = under(weed), under(urgent_dry), under(ripe)
    here_dry, here_free = under(dry), under(free)

    op = jnp.full(flat.shape, O.NOOP, dtype=jnp.int32)
    crop = jnp.zeros_like(op)
    taken = jnp.zeros(flat.shape, dtype=bool)

    def commit(mask, new_op, new_crop=None):
        nonlocal op, crop, taken
        do = mask & ~taken & live
        op = jnp.where(do, new_op, op)
        if new_crop is not None:
            crop = jnp.where(do, new_crop, crop)
        taken = taken | do

    # ---- the author's priority order, applied on the tile the unit already stands on ----------
    # (0) weeds and plants that missed a watering, (1) harvest, (2) ordinary watering, (3) plant.
    # Weeds outrank harvest because a weed spreads; a missed watering outranks it because the plant
    # dies tonight either way.
    commit(here_weed, O.DIG)
    commit(here_urgent, O.WATER)
    commit(here_ripe, O.HARVEST)
    commit(here_dry, O.WATER)
    commit(here_free & can_plant, O.PLANT_OP, CARROT)

    # ---- anything undecided walks toward its own job, in the same priority order ---------------
    rank = jnp.arange(J.MAX_UNITS)

    def route(candidate):
        idx = jax.vmap(lambda r: _nth_nearest(pos[:, :, 0], candidate, r), out_axes=-1)(rank)
        tgt = jnp.stack([idx % J.BOARD, idx // J.BOARD], axis=-1)
        return idx, _step_toward(pos, tgt)

    for candidate in (weed | urgent_dry, ripe, dry):
        idx, step = route(candidate)
        commit(idx >= 0, step)

    idx, step = route(free)
    commit((idx >= 0) & can_plant, step)

    # ---- market -------------------------------------------------------------------------------
    # **Sell every carrot that reaches the shed**, with no minimum. The author's whole thesis is
    # turnover on a three-day cycle, so holding stock to clear a threshold would be a different
    # agent -- `jax_heuristic`'s `SELL_MIN` is deliberately not copied.
    sell = jnp.zeros((b, 2, J.N_PRODUCTS), dtype=J._I)
    sell = sell.at[..., CARROT].set(farm.shed[..., CARROT].astype(J._I))

    # Buy enough seed to fill the empty tiles, out of `money - 100`, while there is still time for
    # a crop to mature.
    empty_tiles = free.sum(axis=-1)                                 # [B, P]
    wanted = jnp.maximum(0, empty_tiles - seeds_left)
    affordable = jnp.maximum(0.0, farm.money - CASH_BUFFER) // SEED_COST
    qty = jnp.minimum(wanted, affordable.astype(wanted.dtype))
    buy_seed = jnp.zeros((b, 2, J.N_CROPS), dtype=J._I)
    buy_seed = buy_seed.at[..., CARROT].set(
        jnp.where(day <= LAST_PLANT_DAY, qty, 0).astype(J._I))

    return J.Actions(
        unit_op=jnp.where(live, op, O.NOOP).astype(J._I),
        unit_crop=crop.astype(J._I),
        unit_item=jnp.zeros_like(op, dtype=J._I),
        unit_qty=jnp.ones_like(op, dtype=J._I),
        sell=sell,
        buy_seed=buy_seed,
        buy_product=jnp.zeros((b, 2, J.N_PRODUCTS), dtype=J._I),
        buy_animal=jnp.zeros((b, 2, J.N_ANIMALS), dtype=J._I),
        # See the module docstring: one hire per turn is the interface limit, so this hires on any
        # turn while short rather than emitting the whole shortfall at `hour == 0`.
        hire=farm.n_units < TARGET_HANDS,
        buy_land=jnp.zeros((b, 2), dtype=bool),
    )
