"""JAX port of the numpy-batched simulator: the whole turn as one jitted kernel.

Why this exists
---------------
The numpy sim is parity-exact against the reference environment (60/60 full-length episodes) but
its throughput *peaks around B=512-1024 and then falls*. A simulator that gets slower as the batch
grows is not bound by arithmetic; it is bound by roughly fifty small numpy calls per step plus the
Python loops over the 24 unit slots and over market settlement. `jax.jit` is the direct answer to
that shape of problem: one traced graph, no per-op dispatch, and throughput that rises with B
instead of falling.

The second thing the numpy profile hides is that its speed is a function of how little is
happening. It is built out of `if not x.any(): continue` short-circuits, so an empty board with
all-NOOP actions is its best case and is roughly **20x faster than a turn where a full crew of 24
is working** -- which is what a competent policy's turns look like. The JAX sim is far flatter
across that range. `scripts/bench_jax_sim.py` measures all three profiles rather than quoting the
flattering one; read it before citing any number from either simulator.

Correctness contract
--------------------
This module reproduces `kagg.sim.game.Game` **exactly**, field for field, not merely closely. The
numpy sim is the reference here; because it is itself gated against `reference/kaggriculture.py`,
matching it transitively inherits that guarantee. `tests/test_jax_sim.py` drives both
implementations in lockstep for full 719-step episodes and compares every array after every step.
That length is not decorative -- the numpy sim passed a 200-step check and then failed the
719-step gate 40/40 on a seed-accounting bug that took hundreds of steps to become visible.

Deliberate divergences, carried over unchanged from the numpy sim
-----------------------------------------------------------------
- **Weed spawning is statistically faithful, not sequence-identical.** The reference draws from a
  per-day Python `random.Random` shared by both farms, one draw per empty tile. Porting that
  draw-for-draw costs millions of scalar RNG calls per batch and would destroy the speedup the
  simulator exists for. Here it is a single vectorized `jax.random.uniform` over `[B, P, TILES]`,
  which is a *third* RNG stream (reference, numpy sim, JAX sim all differ). Parity is therefore
  established with `weed_chance=0`, exactly as the numpy gate does.
- **Shop unlock order is supplied by the caller.** Which shop unlocks on a given day depends on
  both players' board occupancy, because `_spawn_weeds` consumes the shared RNG stream before
  `rng.choice` picks the shop. It is passed in as `unlock_day` rather than derived.
- **Hands all spawn on the NW shed-access tile.** The reference balances new hands across the four
  inner corners; the numpy sim does not, and neither does this.

One further, JAX-only reordering, which is *not* a divergence
-------------------------------------------------------------
The numpy sim runs player 0's whole unit phase and then player 1's. Here both players advance
together on a `[B, P, ...]` player axis. That is sound because the unit phase touches only the
acting player's own tiles and farm -- there is no shared state until market settlement, and market
settlement keeps its strict seat alternation. The same argument licenses settling all nine
products concurrently: each product has its own inventory, shed column and order book, and the
only shared quantity is money, which accumulates by addition.

Numerics
--------
`jax_enable_x64` is switched on at import. Money is `float64` in the numpy sim and the bank is the
environment's reward, so silently demoting it to `float32` would be exactly the kind of quiet
divergence this project has already been bitten by once. Everything else is `int32`, which is what
a GPU wants. The price curve is evaluated analytically rather than from a lookup table;
`test_jax_sim.py` asserts it is bit-identical to `kagg.sim.market.price` across a 150,000-wide
inventory range, which is far outside anything an episode can reach.
"""

import functools
from typing import NamedTuple

import jax
import numpy as np

jax.config.update("jax_enable_x64", True)

import jax.numpy as jnp  # noqa: E402
from jax import lax  # noqa: E402

from kaggle_environments.envs.kaggriculture import kaggriculture as kg  # noqa: E402

from kagg.sim import farm as F  # noqa: E402
from kagg.sim import market as M  # noqa: E402
from kagg.sim import ops as O  # noqa: E402
from kagg.sim import tiles as T  # noqa: E402
from kagg.sim import town as W  # noqa: E402
from kagg.sim.game import LAST_STEP, N_PLAYERS  # noqa: E402

# ---- shapes and constants, all lifted straight from the numpy sim -------------------------------

BOARD = T.BOARD
TILES = T.TILES
TURNS_PER_DAY = T.TURNS_PER_DAY
MAX_UNITS = F.MAX_UNITS
N_CROPS = F.N_CROPS
N_PRODUCTS = M.N_PRODUCTS
N_SHOPS = W.N_SHOPS
N_LAND = F.N_LAND
SHED_CAP = F.SHED_CAP
PRICE_FLOOR = M.PRICE_FLOOR

EMPTY, LOCKED, WEED, PLANT = T.EMPTY, T.LOCKED, T.WEED, T.PLANT
NO_CROP = T.NO_CROP

NEVER = np.int32(1 << 24)   # unlock day for a shop that never opens

_I = jnp.int32
_F = jnp.float64

FIRST_YIELD_DAY = jnp.asarray(T.FIRST_YIELD_DAY, dtype=_I)
MAX_YIELD_DAY = jnp.asarray(T.MAX_YIELD_DAY, dtype=_I)
INTERVAL = jnp.asarray(T.INTERVAL, dtype=_I)
MAX_YIELD = jnp.asarray(T.MAX_YIELD, dtype=_I)
ONGOING = jnp.asarray(T.ONGOING, dtype=bool)

CROP_TO_PRODUCT = jnp.asarray(F.CROP_TO_PRODUCT, dtype=_I)
SEED_COST = jnp.asarray(F.SEED_COST, dtype=_F)
HIRE_COST = jnp.asarray(F.HIRE_COST, dtype=_F)
LAND_PRICES = jnp.asarray(F.LAND_PRICES, dtype=_F)

SHOP_PULL = jnp.asarray(W.SHOP_PULL, dtype=_I)
CENTER_PULL = jnp.asarray(W.CENTER_PULL, dtype=_I)
_CENTER_SCHEDULE = tuple(sorted(kg.TOWN_CENTER_DEMAND_SCHEDULE))

BASE = jnp.asarray(M.BASE, dtype=_F)
INV0 = jnp.asarray(M.I0, dtype=_F)
BELOW_FUNC = jnp.asarray(M.BELOW_FUNC, dtype=_I)
ABOVE_FUNC = jnp.asarray(M.ABOVE_FUNC, dtype=_I)
BELOW_AMP = jnp.asarray(M._BELOW_AMP, dtype=_F)
ABOVE_AMP = jnp.asarray(M._ABOVE_AMP, dtype=_F)

SPAWN_X, SPAWN_Y = F.default_spawn()

_DX = jnp.asarray(O._DX, dtype=_I)
_DY = jnp.asarray(O._DY, dtype=_I)

# [N_LAND, TILES] -- which tiles each purchasable quadrant covers, in LAND_ORDER.
QUAD_MASKS = jnp.asarray(
    np.stack([F._quadrant_mask(q) for q in kg.LAND_ORDER]), dtype=bool
)

# [TILES] -- everything outside the NW quadrant starts locked.
_locked0 = np.zeros(TILES, dtype=bool)
for _y in range(BOARD):
    for _x in range(BOARD):
        if not (_x < BOARD // 2 and _y < BOARD // 2):
            _locked0[_y * BOARD + _x] = True
INITIAL_LOCKED = jnp.asarray(_locked0, dtype=bool)

_ARANGE_UNITS = jnp.arange(MAX_UNITS, dtype=_I)
_ARANGE_CROPS = jnp.arange(N_CROPS, dtype=_I)
_ARANGE_PRODUCTS = jnp.arange(N_PRODUCTS, dtype=_I)


# ---- state ---------------------------------------------------------------------------------


class Tiles(NamedTuple):
    """Tile state for both farms: every field is `[B, N_PLAYERS, TILES]`.

    Names mirror `kagg.sim.tiles.TileState`, which in turn mirrors the reference's tile dict keys,
    so a transition can be checked against `kaggriculture.py` without translating anything.
    `watered_today` is `int32` 0/1 rather than bool purely so the whole struct shares a dtype.
    """

    kind: jnp.ndarray
    crop: jnp.ndarray
    planted_day: jnp.ndarray
    watered_today: jnp.ndarray
    consecutive_unwatered: jnp.ndarray
    yield_units: jnp.ndarray
    max_lifespan_step: jnp.ndarray
    fertilized_until_day: jnp.ndarray


class Farm(NamedTuple):
    """Everything a player owns that is not a tile. Leading axes are `[B, N_PLAYERS, ...]`."""

    money: jnp.ndarray            # [B, P]                    float64
    seeds: jnp.ndarray            # [B, P, N_CROPS]
    shed: jnp.ndarray             # [B, P, N_PRODUCTS]
    carried: jnp.ndarray          # [B, P, MAX_UNITS, N_PRODUCTS]
    unit_pos: jnp.ndarray         # [B, P, MAX_UNITS, 2]      as (x, y)
    n_units: jnp.ndarray          # [B, P]
    hires_today: jnp.ndarray      # [B, P]
    n_land: jnp.ndarray           # [B, P]


class State(NamedTuple):
    """A batch of B two-player games. A pytree, so it passes straight through `jit` and `scan`."""

    step_index: jnp.ndarray       # scalar int32
    tiles: Tiles
    farm: Farm
    inventory: jnp.ndarray        # [B, N_PRODUCTS]
    unlock_day: jnp.ndarray       # [B, N_SHOPS] -- day each shop opens, NEVER if it never does
    key: jnp.ndarray              # PRNG key, only consumed when weeds are enabled

    @property
    def batch(self):
        return self.inventory.shape[0]

    @property
    def day(self):
        return self.step_index // TURNS_PER_DAY


class Actions(NamedTuple):
    """One turn's actions for every game and both players. Mirrors `kagg.sim.game.Actions`.

    - `unit_op`   [B, P, MAX_UNITS]   op code per unit, from `kagg.sim.ops`
    - `unit_crop` [B, P, MAX_UNITS]   crop id for PLANT ops, ignored otherwise
    - `sell`      [B, P, N_PRODUCTS]  units offered for sale
    - `buy_seed`  [B, P, N_CROPS]     seeds to buy
    - `hire`      [B, P]              hire one hand this turn
    - `buy_land`  [B, P]              unlock the next quadrant
    """

    unit_op: jnp.ndarray
    unit_crop: jnp.ndarray
    sell: jnp.ndarray
    buy_seed: jnp.ndarray
    hire: jnp.ndarray
    buy_land: jnp.ndarray


def zero_actions(batch, players=N_PLAYERS):
    """An all-NOOP action set, the JAX counterpart of constructing `game.Actions`."""
    return Actions(
        unit_op=jnp.zeros((batch, players, MAX_UNITS), dtype=_I),
        unit_crop=jnp.zeros((batch, players, MAX_UNITS), dtype=_I),
        sell=jnp.zeros((batch, players, N_PRODUCTS), dtype=_I),
        buy_seed=jnp.zeros((batch, players, N_CROPS), dtype=_I),
        hire=jnp.zeros((batch, players), dtype=bool),
        buy_land=jnp.zeros((batch, players), dtype=bool),
    )


def from_numpy_actions(actions, players=N_PLAYERS):
    """Convert a `kagg.sim.game.Actions` into this module's pytree, for lockstep testing."""
    return Actions(
        unit_op=jnp.asarray(actions.unit_op, dtype=_I),
        unit_crop=jnp.asarray(actions.unit_crop, dtype=_I),
        sell=jnp.asarray(actions.sell, dtype=_I),
        buy_seed=jnp.asarray(actions.buy_seed, dtype=_I),
        hire=jnp.asarray(actions.hire, dtype=bool),
        buy_land=jnp.asarray(actions.buy_land, dtype=bool),
    )


def _canonical(actions):
    """Force the action dtypes the step function scatters into. A no-op when they already match."""
    return Actions(
        unit_op=actions.unit_op.astype(_I),
        unit_crop=actions.unit_crop.astype(_I),
        sell=actions.sell.astype(_I),
        buy_seed=actions.buy_seed.astype(_I),
        hire=actions.hire.astype(bool),
        buy_land=actions.buy_land.astype(bool),
    )


def stack_actions(frames):
    """Stack per-step `Actions` (numpy or JAX) into one time-major pytree for `rollout`."""
    frames = [a if isinstance(a, Actions) else from_numpy_actions(a) for a in frames]
    return Actions(*[jnp.stack([getattr(a, f) for a in frames]) for f in Actions._fields])


def unlock_array(schedule, batch):
    """Build the `[B, N_SHOPS]` unlock-day array from a `{day: shop_index}` dict.

    Same input the numpy `Game` takes. A shop absent from the schedule never opens.
    """
    out = np.full((batch, N_SHOPS), NEVER, dtype=np.int32)
    for day, shop in (schedule or {}).items():
        out[:, int(shop)] = min(int(out[0, int(shop)]), int(day))
    return jnp.asarray(out)


def reset(batch, starting_money=3000.0, unlock_schedule=None, seed=0, players=N_PLAYERS):
    """Initial state, identical to a freshly constructed `kagg.sim.game.Game`."""
    shape = (batch, players, TILES)
    tiles = Tiles(
        kind=jnp.broadcast_to(jnp.where(INITIAL_LOCKED, LOCKED, EMPTY).astype(_I), shape),
        crop=jnp.full(shape, NO_CROP, dtype=_I),
        planted_day=jnp.zeros(shape, dtype=_I),
        watered_today=jnp.zeros(shape, dtype=_I),
        consecutive_unwatered=jnp.zeros(shape, dtype=_I),
        yield_units=jnp.zeros(shape, dtype=_I),
        max_lifespan_step=jnp.full(shape, -1, dtype=_I),
        fertilized_until_day=jnp.full(shape, -1, dtype=_I),
    )
    pos = jnp.stack(
        [
            jnp.full((batch, players, MAX_UNITS), SPAWN_X, dtype=_I),
            jnp.full((batch, players, MAX_UNITS), SPAWN_Y, dtype=_I),
        ],
        axis=-1,
    )
    farm = Farm(
        money=jnp.full((batch, players), starting_money, dtype=_F),
        seeds=jnp.zeros((batch, players, N_CROPS), dtype=_I),
        shed=jnp.zeros((batch, players, N_PRODUCTS), dtype=_I),
        carried=jnp.zeros((batch, players, MAX_UNITS, N_PRODUCTS), dtype=_I),
        unit_pos=pos,
        n_units=jnp.ones((batch, players), dtype=_I),
        hires_today=jnp.zeros((batch, players), dtype=_I),
        n_land=jnp.zeros((batch, players), dtype=_I),
    )
    return State(
        step_index=jnp.asarray(0, dtype=_I),
        tiles=tiles,
        farm=farm,
        inventory=jnp.broadcast_to(jnp.asarray(M.I0, dtype=_I), (batch, N_PRODUCTS)),
        unlock_day=unlock_array(unlock_schedule, batch),
        key=jax.random.PRNGKey(seed),
    )


# ---- market pricing -------------------------------------------------------------------------


def _shape_fn(func_id, x):
    """Vectorized `kaggriculture._shape`, selecting per element by function id.

    The five branches are all evaluated and then selected. That is wasteful on paper and free in
    practice: `func_id` is a compile-time constant array, so XLA constant-folds the selection.
    """
    x = jnp.maximum(x, 0.0)
    branches = (x, x * x, jnp.sqrt(x), jnp.log1p(x), jnp.log10(1.0 + x))
    out = jnp.zeros_like(x)
    for fid, values in enumerate(branches):
        out = jnp.where(func_id == fid, values, out)
    return out


def price(inventory):
    """Price of every product. `inventory` is `[..., N_PRODUCTS]`; returns int32.

    Bit-identical to `kagg.sim.market.price` -- asserted over a 150,000-wide inventory range in
    `tests/test_jax_sim.py` rather than assumed, because a single off-by-one here would shift
    every sale in the game and would look exactly like a strategy difference.
    """
    inv = inventory.astype(_F)
    scarce = BASE + BELOW_AMP * _shape_fn(BELOW_FUNC, INV0 - inv)
    glut = BASE - ABOVE_AMP * _shape_fn(ABOVE_FUNC, inv - INV0)
    raw = jnp.where(inv < INV0, scarce, glut)
    return jnp.maximum(PRICE_FLOOR, jnp.rint(raw)).astype(_I)


# ---- unit actions ---------------------------------------------------------------------------


def _gather(arr, idx):
    """`arr[b, p, idx[b, p]]` for `arr` of shape [B, P, TILES]."""
    return jnp.take_along_axis(arr, idx[..., None], axis=-1)[..., 0]


def _scatter(arr, idx, value):
    """`arr[b, p, idx[b, p]] = value[b, p]`, returning the updated array."""
    b = jnp.arange(arr.shape[0])[:, None]
    p = jnp.arange(arr.shape[1])[None, :]
    return arr.at[b, p, idx].set(value)


def _apply_unit_actions(tiles, farm, actions, day):
    """Every unit acts, one slot at a time, both players and the whole batch at once.

    The slot loop stays sequential because two of a player's units may stand on the same tile in
    the same turn, and the reference resolves that in unit order -- the first waters, the second
    finds the tile already watered. Vectorizing it away would silently double those effects.

    The loop runs to `max(n_units)` rather than to `MAX_UNITS`, which is the JAX equivalent of the
    numpy sim's `if not active.any(): continue`. For most of a day only the farmer exists, so this
    is the difference between one iteration and twenty-four.
    """
    live = _ARANGE_UNITS[None, None, :] < farm.n_units[:, :, None]

    def body(u, carry):
        tl, seeds, unit_pos, carried = carry
        active = lax.dynamic_index_in_dim(live, u, axis=2, keepdims=False)
        op = lax.dynamic_index_in_dim(actions.unit_op, u, axis=2, keepdims=False)
        want_crop = lax.dynamic_index_in_dim(actions.unit_crop, u, axis=2, keepdims=False)
        pos = lax.dynamic_index_in_dim(unit_pos, u, axis=2, keepdims=False)   # [B, P, 2]

        # --- movement: blocked by the board edge and by LOCKED tiles, otherwise silent -----
        moving = active & (op >= O.NORTH) & (op <= O.WEST)
        nx = pos[..., 0] + _DX[op]
        ny = pos[..., 1] + _DY[op]
        in_bounds = (nx >= 0) & (nx < BOARD) & (ny >= 0) & (ny < BOARD)
        target = jnp.clip(ny, 0, BOARD - 1) * BOARD + jnp.clip(nx, 0, BOARD - 1)
        unlocked = _gather(tl.kind, target) != LOCKED
        legal = moving & in_bounds & unlocked
        pos = jnp.stack(
            [jnp.where(legal, nx, pos[..., 0]), jnp.where(legal, ny, pos[..., 1])], axis=-1
        )
        unit_pos = lax.dynamic_update_slice_in_dim(unit_pos, pos[:, :, None, :], u, axis=2)

        idx = pos[..., 1] * BOARD + pos[..., 0]
        kind = _gather(tl.kind, idx)
        crop = _gather(tl.crop, idx)
        planted_day = _gather(tl.planted_day, idx)
        watered = _gather(tl.watered_today, idx)
        unwatered = _gather(tl.consecutive_unwatered, idx)
        units = _gather(tl.yield_units, idx)
        lifespan = _gather(tl.max_lifespan_step, idx)
        fert = _gather(tl.fertilized_until_day, idx)

        # --- WATER: the non-ongoing yield bonus lands only inside the window, once a day ----
        doable = active & (op == O.WATER) & (kind == PLANT) & (watered == 0)
        watered = jnp.where(doable, 1, watered)
        c = jnp.where(doable, jnp.clip(crop, 0, N_CROPS - 1), 0)
        age = day - planted_day
        window_start = (MAX_YIELD_DAY[c] + 1) // 2
        in_window = (age >= window_start) & (age <= MAX_YIELD_DAY[c])
        gains = doable & ~ONGOING[c] & in_window
        bonus = jnp.where(fert >= day, 2, 1)
        units = jnp.where(gains, jnp.minimum(MAX_YIELD[c], units + bonus), units)

        # --- HARVEST: non-ongoing crops come up with the harvest, ongoing ones stay --------
        c = jnp.where(kind == PLANT, jnp.clip(crop, 0, N_CROPS - 1), 0)
        age = day - planted_day
        doable = (
            active & (op == O.HARVEST) & (kind == PLANT) & (units > 0)
            & (age >= FIRST_YIELD_DAY[c])
        )
        got = jnp.where(doable, units, 0)
        prod = CROP_TO_PRODUCT[c]
        carried_u = lax.dynamic_index_in_dim(carried, u, axis=2, keepdims=False)
        carried_u = carried_u + (_ARANGE_PRODUCTS == prod[..., None]).astype(_I) * got[..., None]
        carried = lax.dynamic_update_slice_in_dim(carried, carried_u[:, :, None, :], u, axis=2)
        units = jnp.where(doable, 0, units)
        cleared = doable & ~ONGOING[c]
        kind = jnp.where(cleared, EMPTY, kind)
        crop = jnp.where(cleared, NO_CROP, crop)
        lifespan = jnp.where(cleared, -1, lifespan)

        # --- DIG: clears weeds and plants alike ---------------------------------------------
        doable = active & (op == O.DIG) & ((kind == WEED) | (kind == PLANT))
        kind = jnp.where(doable, EMPTY, kind)
        crop = jnp.where(doable, NO_CROP, crop)
        units = jnp.where(doable, 0, units)
        lifespan = jnp.where(doable, -1, lifespan)

        # --- PLANT: only on an empty tile, and only if a seed is actually in store ----------
        # A PLANT onto an occupied tile is a free no-op in the reference. Charging a seed for it
        # anyway is the bug that failed the numpy gate 40/40 while every unit test passed, so the
        # seed is spent from `doable` (the plant landed) and never from `planting` (it was tried).
        c = jnp.clip(want_crop, 0, N_CROPS - 1)
        held = jnp.take_along_axis(seeds, c[..., None], axis=-1)[..., 0]
        planting = (
            active & (op == O.PLANT_OP) & (want_crop >= 0) & (want_crop < N_CROPS) & (held > 0)
        )
        doable = planting & (kind == EMPTY)
        ongoing = ONGOING[c]
        kind = jnp.where(doable, PLANT, kind)
        crop = jnp.where(doable, c, crop)
        planted_day = jnp.where(doable, day, planted_day)
        watered = jnp.where(doable, 0, watered)
        unwatered = jnp.where(doable, 1, unwatered)         # planting day counts as unwatered
        units = jnp.where(doable, jnp.where(ongoing, 0, 1), units)
        new_life = jnp.where(ongoing, -1, (day + MAX_YIELD_DAY[c] + 1) * TURNS_PER_DAY)
        lifespan = jnp.where(doable, new_life, lifespan)
        fert = jnp.where(doable, -1, fert)
        spent = ((_ARANGE_CROPS == c[..., None]) & doable[..., None]).astype(_I)
        seeds = seeds - spent

        tl = Tiles(
            kind=_scatter(tl.kind, idx, kind),
            crop=_scatter(tl.crop, idx, crop),
            planted_day=_scatter(tl.planted_day, idx, planted_day),
            watered_today=_scatter(tl.watered_today, idx, watered),
            consecutive_unwatered=_scatter(tl.consecutive_unwatered, idx, unwatered),
            yield_units=_scatter(tl.yield_units, idx, units),
            max_lifespan_step=_scatter(tl.max_lifespan_step, idx, lifespan),
            fertilized_until_day=_scatter(tl.fertilized_until_day, idx, fert),
        )
        return tl, seeds, unit_pos, carried

    n_slots = jnp.max(farm.n_units)
    tl, seeds, unit_pos, carried = lax.fori_loop(
        0, n_slots, body, (tiles, farm.seeds, farm.unit_pos, farm.carried)
    )
    return tl, farm._replace(seeds=seeds, unit_pos=unit_pos, carried=carried)


# ---- market ---------------------------------------------------------------------------------


def _settle_sales(farm, inventory, sell):
    """Settle sells one unit at a time, both players alternating, re-quoting after every unit.

    Both seats are quoted against the same pre-commit inventory and commit in seat order, so seat
    0 takes the better price on each contested unit -- that asymmetry is in the reference and is
    load-bearing, so the seat loop is unrolled rather than vectorized.

    All nine products settle concurrently, which the numpy sim cannot do because it iterates
    products in Python. They are independent: each has its own inventory column, shed column and
    order book, and the only shared quantity is money, which only ever accumulates by addition.

    The loop is a `while`, not a bounded `for`. The numpy sim runs `max(remaining)` iterations and
    breaks early; a game that orders more than it holds simply spins. Terminating on
    "nobody can still trade" reaches the identical fixed point and cannot be made to spin.
    """
    remaining = jnp.maximum(sell, 0)

    def cond(carry):
        rem, shed, _money, _inv = carry
        return jnp.any((rem > 0) & (shed > 0))

    def body(carry):
        rem, shed, money, inv = carry
        for seat in range(rem.shape[1]):
            doing = (rem[:, seat] > 0) & (shed[:, seat] > 0)     # [B, N_PRODUCTS]
            unit_price = price(inv)
            gain = jnp.sum(jnp.where(doing, unit_price, 0), axis=-1).astype(_F)
            money = money.at[:, seat].add(gain)
            shed = shed.at[:, seat].add(-doing.astype(_I))
            rem = rem.at[:, seat].add(-doing.astype(_I))
            # A unit clearing at the floor pays out but does not deepen the glut.
            inv = inv + (doing & (unit_price > PRICE_FLOOR)).astype(_I)
        return rem, shed, money, inv

    _rem, shed, money, inventory = lax.while_loop(
        cond, body, (remaining, farm.shed, farm.money, inventory)
    )
    return farm._replace(shed=shed, money=money), inventory


def _buy_seeds(farm, buy_seed):
    """Buy seeds, crop by crop in index order.

    The crop loop stays sequential because each purchase draws on the same bank: buying wheat
    first can be what makes melon unaffordable. Players are independent and go together.
    """
    money, seeds = farm.money, farm.seeds
    for c in range(N_CROPS):
        want = buy_seed[:, :, c]
        cost = SEED_COST[c]
        affordable = jnp.minimum(want, jnp.floor_divide(money, cost).astype(_I))
        affordable = jnp.maximum(affordable, 0)
        money = money - affordable.astype(_F) * cost
        seeds = seeds.at[:, :, c].add(affordable)
    return farm._replace(money=money, seeds=seeds)


def _hire(farm, want):
    """Hire one hand where affordable. Cost is Fibonacci in hires already made *today*.

    Skipped wholesale when nobody in the batch is hiring, which is the JAX equivalent of the numpy
    sim's `if actions.hire[:, p].any()`. Worth a branch: the carried-inventory reset rewrites a
    `[B, P, MAX_UNITS, N_PRODUCTS]` array, the largest single buffer in the step.
    """
    return lax.cond(jnp.any(want), _hire_impl, lambda f, w: f, farm, want)


def _hire_impl(farm, want):
    cost = HIRE_COST[jnp.minimum(farm.hires_today, MAX_UNITS)]
    doable = want & (farm.money >= cost) & (farm.n_units < MAX_UNITS)

    slot = jnp.minimum(farm.n_units, MAX_UNITS - 1)
    sel = (_ARANGE_UNITS == slot[..., None]) & doable[..., None]    # [B, P, MAX_UNITS]
    spawn = jnp.asarray([SPAWN_X, SPAWN_Y], dtype=_I)
    return farm._replace(
        money=jnp.where(doable, farm.money - cost, farm.money),
        hires_today=farm.hires_today + doable.astype(_I),
        n_units=farm.n_units + doable.astype(_I),
        unit_pos=jnp.where(sel[..., None], spawn, farm.unit_pos),
        carried=jnp.where(sel[..., None], 0, farm.carried),
    )


def _buy_land(farm, tiles, want):
    """Unlock the next quadrant. The order NE, SW, SE is fixed, so `n_land` selects the mask.

    Land is bought at most three times in an episode, so the whole phase sits behind a branch --
    otherwise every one of 719 turns pays for a `[B, P, TILES]` quadrant gather and rewrite.
    """
    return lax.cond(
        jnp.any(want), _buy_land_impl, lambda f, t, w: (f, t), farm, tiles, want
    )


def _buy_land_impl(farm, tiles, want):
    have = jnp.minimum(farm.n_land, N_LAND - 1)
    cost = LAND_PRICES[have]
    doable = want & (farm.n_land < N_LAND) & (farm.money >= cost)

    newly = doable[..., None] & QUAD_MASKS[have] & (tiles.kind == LOCKED)
    tiles = tiles._replace(kind=jnp.where(newly, EMPTY, tiles.kind))
    farm = farm._replace(
        money=jnp.where(doable, farm.money - cost, farm.money),
        n_land=farm.n_land + doable.astype(_I),
    )
    return farm, tiles


# ---- town, decay, night ----------------------------------------------------------------------


def _center_multiplier(day):
    out = jnp.ones_like(day)
    for threshold, mult in _CENTER_SCHEDULE:
        out = jnp.where(day >= threshold, mult, out)
    return out


def _drain(step, day, unlock_day):
    """Units the town removes this step. Shops tick every 4 steps, the centre every 12."""
    unlocked = (unlock_day <= day).astype(_I)
    shops = jnp.where(step % W.SHOP_INTERVAL == 0, unlocked @ SHOP_PULL, 0)
    centre = jnp.where(
        step % W.CENTER_INTERVAL == 0, _center_multiplier(day) * CENTER_PULL, 0
    )
    return shops + centre


def _decay_plants(tiles, step):
    """A finished plant loses a unit every *other* step counted from the lifespan boundary."""
    mls = tiles.max_lifespan_step
    due = (tiles.kind == PLANT) & (mls >= 0) & (step >= mls) & (((step - mls) % 2) == 0)
    units = jnp.where(due, tiles.yield_units - 1, tiles.yield_units)

    dead = due & (units <= 0)
    return tiles._replace(
        kind=jnp.where(dead, WEED, tiles.kind),
        crop=jnp.where(dead, NO_CROP, tiles.crop),
        yield_units=jnp.where(dead, 0, units),
        max_lifespan_step=jnp.where(dead, -1, mls),
    )


def _daily_refresh_plants(tiles, current_day):
    """The nightly transition: watering enforcement, then ongoing production, in that order."""
    next_day = current_day + 1
    is_plant = tiles.kind == PLANT
    was_watered = (tiles.watered_today != 0) & is_plant

    unwatered = jnp.where(
        is_plant,
        jnp.where(was_watered, 0, tiles.consecutive_unwatered + 1),
        tiles.consecutive_unwatered,
    )
    watered_today = jnp.where(is_plant, 0, tiles.watered_today)

    died = is_plant & (unwatered >= 2)
    kind = jnp.where(died, WEED, tiles.kind)
    crop = jnp.where(died, NO_CROP, tiles.crop)
    units = jnp.where(died, 0, tiles.yield_units)
    lifespan = jnp.where(died, -1, tiles.max_lifespan_step)

    alive = (kind == PLANT) & ~died
    c = jnp.where(alive, jnp.clip(crop, 0, N_CROPS - 1), 0)
    ongoing = ONGOING[c] & alive

    days_since = next_day - tiles.planted_day - FIRST_YIELD_DAY[c]
    interval = jnp.maximum(INTERVAL[c], 1)
    on_schedule = ongoing & (days_since >= 0) & ((days_since % interval) == 0)

    # The rule that cost this project a day-one wrong turn: production stops once the count of
    # *events* passes max_yield, not once the daily units do.
    production_count = jnp.where(on_schedule, days_since // interval + 1, 0)
    produces = on_schedule & (production_count <= MAX_YIELD[c])

    # Fertilizer only pays on a day the tile was actually watered -- basic needs first.
    fertilized = produces & was_watered & (tiles.fertilized_until_day >= current_day)
    gain = jnp.where(fertilized, 2, 1)
    units = jnp.where(produces, jnp.minimum(MAX_YIELD[c], units + gain), units)

    final = produces & (production_count == MAX_YIELD[c])
    lifespan = jnp.where(final, (next_day + 1) * TURNS_PER_DAY, lifespan)

    return tiles._replace(
        kind=kind,
        crop=crop,
        watered_today=watered_today,
        consecutive_unwatered=unwatered,
        yield_units=units,
        max_lifespan_step=lifespan,
    )


def _drop_to_shed(farm):
    """Empty every unit's carried inventory into the shed, respecting the total cap.

    The reference walks units in order and products in insertion order, filling until the shed is
    full and **destroying** the remainder, so the order decides who loses their haul. That is a
    prefix-sum, not a loop: after walking the first `i` items the shed total is
    `min(SHED_CAP, start + cumsum_i)`, so each item's intake is the difference between consecutive
    clamped prefixes. 288 sequential Python steps collapse to one `cumsum`.
    """
    b, p = farm.money.shape
    flat = farm.carried.reshape(b, p, MAX_UNITS * N_PRODUCTS)
    start = jnp.sum(farm.shed, axis=-1, dtype=_I)[..., None]
    inclusive = jnp.cumsum(flat, axis=-1, dtype=_I)
    exclusive = inclusive - flat
    take = jnp.minimum(SHED_CAP, start + inclusive) - jnp.minimum(SHED_CAP, start + exclusive)
    shed = farm.shed + take.reshape(b, p, MAX_UNITS, N_PRODUCTS).sum(axis=2, dtype=_I)
    return farm._replace(shed=shed)


def _end_of_day(farm):
    """Night: haul to the shed, units back to spawn, hands dismissed, day counters reset."""
    farm = _drop_to_shed(farm)
    spawn = jnp.asarray([SPAWN_X, SPAWN_Y], dtype=_I)
    return farm._replace(
        unit_pos=jnp.broadcast_to(spawn, farm.unit_pos.shape).astype(_I),
        n_units=jnp.ones_like(farm.n_units),
        hires_today=jnp.zeros_like(farm.hires_today),
        carried=jnp.zeros_like(farm.carried),
    )


def _night(tiles, farm, key, day, weed_chance):
    tiles = _daily_refresh_plants(tiles, day)
    if weed_chance:
        key, sub = jax.random.split(key)
        roll = jax.random.uniform(sub, tiles.kind.shape)
        tiles = tiles._replace(
            kind=jnp.where((tiles.kind == EMPTY) & (roll < weed_chance), WEED, tiles.kind)
        )
    return tiles, _end_of_day(farm), key


# ---- the loop --------------------------------------------------------------------------------


@functools.partial(jax.jit, static_argnames=("weed_chance",))
def step(state, actions, weed_chance=0.0):
    """Advance every game by one turn. The whole turn is one traced graph.

    Phase order follows the reference exactly and is not cosmetic: selling happens *before* the
    town drains, so the price a player receives is set by the pre-drain inventory. Swapping the
    two shifts every sale price in the game.
    """
    actions = _canonical(actions)
    day = state.step_index // TURNS_PER_DAY

    tiles, farm = _apply_unit_actions(state.tiles, state.farm, actions, day)

    farm, inventory = _settle_sales(farm, state.inventory, actions.sell)
    farm = _buy_seeds(farm, actions.buy_seed)
    farm = _hire(farm, actions.hire)
    farm, tiles = _buy_land(farm, tiles, actions.buy_land)

    inventory = inventory - _drain(state.step_index, day, state.unlock_day)
    tiles = _decay_plants(tiles, state.step_index)

    is_night = ((state.step_index + 1) % TURNS_PER_DAY) == 0
    tiles, farm, key = lax.cond(
        is_night,
        lambda t, f, k: _night(t, f, k, day, weed_chance),
        lambda t, f, k: (t, f, k),
        tiles, farm, state.key,
    )

    return state._replace(
        step_index=state.step_index + 1,
        tiles=tiles,
        farm=farm,
        inventory=inventory,
        key=key,
    )


def done(state):
    """True once the episode is over, matching the numpy sim's `step()` return value."""
    return state.step_index > LAST_STEP


def money(state):
    """[B, P] current bank for each player -- the environment's reward."""
    return state.farm.money


def prices(state):
    return price(state.inventory)


@functools.partial(jax.jit, static_argnames=("weed_chance",))
def rollout(state, actions_seq, weed_chance=0.0):
    """Run a whole scripted episode inside one XLA call.

    `actions_seq` is an `Actions` pytree whose leaves carry a leading time axis. Scanning the step
    function removes one Python round-trip per turn, which is the remaining per-step overhead once
    the step itself is jitted -- worth about 45% on this machine. Returns the final state and the
    per-step `[T, B, P]` bank.

    The outer `jit` is not optional. A bare `lax.scan` outside `jit` recompiles on every call, and
    for a 60-step scan that costs 0.8s against 0.06s of actual work -- a 13x slowdown that looks
    exactly like "JAX is slow" if you do not check.
    """
    def body(s, a):
        s = step(s, a, weed_chance=weed_chance)
        return s, s.farm.money

    return lax.scan(body, state, actions_seq)


class JaxGame:
    """Thin stateful wrapper matching `kagg.sim.game.Game`'s surface, for tests and benchmarks.

    Real training should drive `step`/`rollout` functionally; this exists so the two simulators
    can be compared line for line without a translation layer in the test.
    """

    def __init__(self, batch, starting_money=3000.0, weed_chance=0.0, seed=0,
                 unlock_schedule=None):
        self.weed_chance = weed_chance
        self.state = reset(
            batch, starting_money=starting_money, unlock_schedule=unlock_schedule, seed=seed
        )

    @property
    def batch(self):
        return self.state.batch

    @property
    def step_index(self):
        return int(self.state.step_index)

    @property
    def day(self):
        return self.step_index // TURNS_PER_DAY

    @property
    def inventory(self):
        return self.state.inventory

    def money(self):
        return self.state.farm.money

    def prices(self):
        return prices(self.state)

    def step(self, actions):
        if not isinstance(actions, Actions):
            actions = from_numpy_actions(actions)
        self.state = step(self.state, actions, weed_chance=self.weed_chance)
        return bool(done(self.state))
