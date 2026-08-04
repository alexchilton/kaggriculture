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
from kagg.sim.game import (  # noqa: E402
    LAST_STEP,
    MAX_ORDERS,
    N_PLAYERS,
    ORDER_BUY_ANIMAL,
    ORDER_BUY_LAND,
    ORDER_BUY_PRODUCT,
    ORDER_BUY_SEED,
    ORDER_HIRE,
    ORDER_NONE,
    ORDER_SELL,
)

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

SHED_ACCESS = jnp.asarray(F.shed_access_tiles(), dtype=_I)      # [4, 2], NWSE order
# The same four tiles as flat indices, for the shed-adjacency test that gates DROP/PICKUP/PLACE.
SHED_TILES = jnp.asarray(O.SHED_TILES, dtype=_I)

# ---- the animal economy ------------------------------------------------------------------------
COOP, PASTURE = T.COOP, T.PASTURE
NO_ANIMAL = T.NO_ANIMAL
N_ITEMS = M.N_ITEMS
N_ANIMALS = M.N_ANIMALS
WHEAT_ITEM = O.WHEAT_ITEM
FERT_ITEM = O.FERT_ITEM

ANIMAL_STRUCTURE = jnp.asarray(T.ANIMAL_STRUCTURE, dtype=_I)
ANIMAL_FIRST_YIELD_DAY = jnp.asarray(T.ANIMAL_FIRST_YIELD_DAY, dtype=_I)
ANIMAL_INTERVAL = jnp.asarray(T.ANIMAL_INTERVAL, dtype=_I)
ANIMAL_MAX_HELD = jnp.asarray(T.ANIMAL_MAX_HELD, dtype=_I)
ANIMAL_TO_PRODUCT = jnp.asarray(T.ANIMAL_TO_PRODUCT, dtype=_I)
ANIMAL_COST = jnp.asarray(M.ANIMAL_COST, dtype=_F)
ANIMAL_ITEM = jnp.asarray(M.ANIMAL_ITEM, dtype=_I)
BUYABLE = jnp.asarray(M.BUYABLE, dtype=bool)

_ARANGE_UNITS = jnp.arange(MAX_UNITS, dtype=_I)
_ARANGE_CROPS = jnp.arange(N_CROPS, dtype=_I)
_ARANGE_PRODUCTS = jnp.arange(N_PRODUCTS, dtype=_I)
_ARANGE_ITEMS = jnp.arange(N_ITEMS, dtype=_I)


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
    # Animal occupancy of a COOP/PASTURE tile; NO_ANIMAL means the structure stands empty.
    animal: jnp.ndarray
    placed_day: jnp.ndarray
    consecutive_unfed: jnp.ndarray
    fed_today: jnp.ndarray
    cared_today: jnp.ndarray
    fertilizer_available: jnp.ndarray
    pending_care_bonus: jnp.ndarray


class Farm(NamedTuple):
    """Everything a player owns that is not a tile. Leading axes are `[B, N_PLAYERS, ...]`."""

    money: jnp.ndarray            # [B, P]                    float64
    seeds: jnp.ndarray            # [B, P, N_CROPS]
    shed: jnp.ndarray             # [B, P, N_ITEMS]  -- products *and* animals
    carried: jnp.ndarray          # [B, P, MAX_UNITS, N_ITEMS]
    unit_pos: jnp.ndarray         # [B, P, MAX_UNITS, 2]      as (x, y)
    n_units: jnp.ndarray          # [B, P]
    hires_today: jnp.ndarray      # [B, P]
    n_land: jnp.ndarray           # [B, P]


class State(NamedTuple):
    """A batch of B two-player games. A pytree, so it passes straight through `jit` and `scan`."""

    step_index: jnp.ndarray       # [B] int32 -- per game, so episodes can be out of phase
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
        return self.step_index // TURNS_PER_DAY          # [B]


class Actions(NamedTuple):
    """One turn's actions for every game and both players. Mirrors `kagg.sim.game.Actions`.

    - `unit_op`   [B, P, MAX_UNITS]   op code per unit, from `kagg.sim.ops`
    - `unit_crop` [B, P, MAX_UNITS]   crop id for PLANT ops, ignored otherwise
    - `sell`      [B, P, N_PRODUCTS]  units offered for sale
    - `buy_seed`  [B, P, N_CROPS]     seeds to buy
    - `hire`      [B, P]              COUNT of hands to hire this turn, not a flag
    - `buy_land`  [B, P]              COUNT of quadrants to unlock this turn, not a flag
    """

    unit_op: jnp.ndarray
    unit_crop: jnp.ndarray
    unit_item: jnp.ndarray
    unit_qty: jnp.ndarray
    sell: jnp.ndarray
    buy_seed: jnp.ndarray
    buy_product: jnp.ndarray
    buy_animal: jnp.ndarray
    hire: jnp.ndarray
    buy_land: jnp.ndarray


def zero_actions(batch, players=N_PLAYERS):
    """An all-NOOP action set, the JAX counterpart of constructing `game.Actions`."""
    return Actions(
        unit_op=jnp.zeros((batch, players, MAX_UNITS), dtype=_I),
        unit_crop=jnp.zeros((batch, players, MAX_UNITS), dtype=_I),
        unit_item=jnp.zeros((batch, players, MAX_UNITS), dtype=_I),
        unit_qty=jnp.zeros((batch, players, MAX_UNITS), dtype=_I),
        sell=jnp.zeros((batch, players, N_PRODUCTS), dtype=_I),
        buy_seed=jnp.zeros((batch, players, N_CROPS), dtype=_I),
        buy_product=jnp.zeros((batch, players, N_PRODUCTS), dtype=_I),
        buy_animal=jnp.zeros((batch, players, N_ANIMALS), dtype=_I),
        hire=jnp.zeros((batch, players), dtype=_I),
        buy_land=jnp.zeros((batch, players), dtype=_I),
    )


def from_numpy_actions(actions, players=N_PLAYERS):
    """Convert a `kagg.sim.game.Actions` into this module's pytree, for lockstep testing."""
    return Actions(
        unit_op=jnp.asarray(actions.unit_op, dtype=_I),
        unit_crop=jnp.asarray(actions.unit_crop, dtype=_I),
        unit_item=jnp.asarray(actions.unit_item, dtype=_I),
        unit_qty=jnp.asarray(actions.unit_qty, dtype=_I),
        sell=jnp.asarray(actions.sell, dtype=_I),
        buy_seed=jnp.asarray(actions.buy_seed, dtype=_I),
        buy_product=jnp.asarray(actions.buy_product, dtype=_I),
        buy_animal=jnp.asarray(actions.buy_animal, dtype=_I),
        # Integer counts, not flags: casting to bool here would collapse "hire twice" to "hire once".
        hire=jnp.asarray(actions.hire, dtype=_I),
        buy_land=jnp.asarray(actions.buy_land, dtype=_I),
    )


def _canonical(actions):
    """Force the action dtypes the step function scatters into. A no-op when they already match."""
    return Actions(
        unit_op=actions.unit_op.astype(_I),
        unit_crop=actions.unit_crop.astype(_I),
        unit_item=actions.unit_item.astype(_I),
        unit_qty=actions.unit_qty.astype(_I),
        sell=actions.sell.astype(_I),
        buy_seed=actions.buy_seed.astype(_I),
        buy_product=actions.buy_product.astype(_I),
        buy_animal=actions.buy_animal.astype(_I),
        hire=actions.hire.astype(_I),
        buy_land=actions.buy_land.astype(_I),
    )


def stack_actions(frames):
    """Stack per-step `Actions` (numpy or JAX) into one time-major pytree for `rollout`."""
    frames = [a if isinstance(a, Actions) else from_numpy_actions(a) for a in frames]
    return Actions(*[jnp.stack([getattr(a, f) for a in frames]) for f in Actions._fields])


SHOP_UNLOCK_INTERVAL = 3   # reference `townShopUnlockInterval` (`kaggriculture.py:836`)


def random_unlock_days(batch, seed=0):
    """A `[B, N_SHOPS]` unlock-day array: one random shop every `SHOP_UNLOCK_INTERVAL` days, per game.

    **This is the reachable configuration, and `NEVER` everywhere is not.** The reference opens one
    shop every three days in *every* episode (`kaggriculture.py:855`), so all eight are trading by
    day 24. A frozen town is not a hard setting of the real game; it is a game that does not exist.

    Only the *order* is random, which is deliberate: it is the simulator's one real seed-to-seed
    variation, and it is what decides which product's price runs first. The total drain is therefore
    identical across games while the path to it is not -- so a batch cannot learn one market's
    timing and call it the market. `search/rollout.sample_unlock_schedule` already made exactly this
    choice for the CEM search; this is the batched form of it.

    Kept separate from `unlock_array` rather than folded into it as a `None` default, because
    `unlock_array(None)` is what `reset` hands the numpy `Game` in lockstep parity tests -- and a
    default that sampled would make the two simulators disagree at the top of every one of them.
    """
    rng = np.random.default_rng(seed)
    out = np.full((batch, N_SHOPS), NEVER, dtype=np.int32)
    days = SHOP_UNLOCK_INTERVAL * (1 + np.arange(N_SHOPS, dtype=np.int32))
    for b in range(batch):
        out[b, rng.permutation(N_SHOPS)] = days
    return jnp.asarray(out)


def unlock_array(schedule, batch):
    """Build the `[B, N_SHOPS]` unlock-day array from a `{day: shop_index}` dict.

    Same input the numpy `Game` takes. A shop absent from the schedule never opens.

    Also accepts an already-built `[B, N_SHOPS]` array, which is how a *per-game* schedule is
    expressed -- a dict cannot say "a different order in each game", and that is the shape the
    reference actually produces. `None` and `{}` both still mean a frozen town, unchanged, because
    the lockstep parity harness passes `None` to both simulators and must keep getting the same
    thing from each.
    """
    if schedule is not None and not isinstance(schedule, dict):
        out = np.asarray(schedule, dtype=np.int32)
        if out.shape == (N_SHOPS,):
            out = np.broadcast_to(out, (batch, N_SHOPS))
        if out.shape != (batch, N_SHOPS):
            raise ValueError(f"unlock array has shape {out.shape}, expected ({batch}, {N_SHOPS})")
        return jnp.asarray(out)

    out = np.full((batch, N_SHOPS), NEVER, dtype=np.int32)
    for day, shop in (schedule or {}).items():
        out[:, int(shop)] = min(int(out[0, int(shop)]), int(day))
    return jnp.asarray(out)


def reset_with_shops(batch, seed=0, **kw):
    """`reset` with a real per-game shop schedule. **Use this for anything that trains or measures.**

    Plain `reset` defaults to a frozen town, and every RL and evaluation entry point took that
    default: measured, the town then bought **140** wheat over a season against the reference's
    **698**, holding end-of-season wheat at $37 instead of $51 and milk at $263 instead of $340.
    The whole pipeline was learning and being scored in a market that discounted its own output by
    27-38% at the tail.

    The default is left alone rather than fixed in place because `_run_lockstep` passes
    `unlock_schedule=None` to *both* simulators, so a sampling default would desynchronise the
    parity gate at construction. The gate stays byte-identical; the callers move.
    """
    return reset(batch, unlock_schedule=random_unlock_days(batch, seed=seed), seed=seed, **kw)


def reset(batch, starting_money=3000.0, unlock_schedule=None, seed=0, players=N_PLAYERS,
          phase=None):
    """Initial state, identical to a freshly constructed `kagg.sim.game.Game`.

    `phase` is an optional `[batch]` array of starting turn indices. **`step_index` is per game**,
    not one scalar for the batch, so episodes can be out of phase with each other -- which is the
    whole point. With a shared counter every game terminates on the same turn, so a terminal reward
    arrives in one burst every ~11 updates and the critic spends the other ten regressing onto its
    own predictions. Batch size cannot fix that: it makes the burst bigger, not more frequent.

    Leaving `phase` as None starts every game at turn 0, which is the old behaviour exactly and is
    what the parity harness relies on.
    """
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
        animal=jnp.full(shape, NO_ANIMAL, dtype=_I),
        placed_day=jnp.zeros(shape, dtype=_I),
        consecutive_unfed=jnp.zeros(shape, dtype=_I),
        fed_today=jnp.zeros(shape, dtype=bool),
        cared_today=jnp.zeros(shape, dtype=bool),
        fertilizer_available=jnp.zeros(shape, dtype=bool),
        pending_care_bonus=jnp.zeros(shape, dtype=_I),
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
        shed=jnp.zeros((batch, players, N_ITEMS), dtype=_I),
        carried=jnp.zeros((batch, players, MAX_UNITS, N_ITEMS), dtype=_I),
        unit_pos=pos,
        n_units=jnp.ones((batch, players), dtype=_I),
        hires_today=jnp.zeros((batch, players), dtype=_I),
        n_land=jnp.zeros((batch, players), dtype=_I),
    )
    return State(
        step_index=(jnp.zeros((batch,), dtype=_I) if phase is None
                    else jnp.asarray(phase, dtype=_I)),
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
    # `day` arrives as `[B]` (per game) and everything gathered below is `[B, P]`, so give it the
    # seat axis once here rather than at each of the dozen comparisons that follow.
    day = day[:, None]
    """Every unit acts, one slot at a time, both players and the whole batch at once.

    The slot loop stays sequential because two of a player's units may stand on the same tile in
    the same turn, and the reference resolves that in unit order -- the first waters, the second
    finds the tile already watered. Vectorizing it away would silently double those effects.

    The loop runs to `max(n_units)` rather than to `MAX_UNITS`, which is the JAX equivalent of the
    numpy sim's `if not active.any(): continue`. For most of a day only the farmer exists, so this
    is the difference between one iteration and twenty-four.
    """
    live = _ARANGE_UNITS[None, None, :] < farm.n_units[:, :, None]

    # PLANT is validated atomically per crop across all of a player's units: if the turn's requests
    # for a crop exceed the seeds held, `interpreter` drops **every** one of them rather than the
    # excess. Spending greedily unit by unit -- which is what this port did, and what the numpy sim
    # did until it was caught -- plants some where the reference plants none. Computed once for the
    # turn, before any seed is spent, because the reference tests the requests against the seeds
    # held at the *start* of the turn.
    asking = live & (actions.unit_op == O.PLANT_OP)                          # [B, P, U]
    demand = jnp.sum(
        jnp.where(
            asking[..., None],
            jnp.clip(actions.unit_crop, 0, N_CROPS - 1)[..., None] == _ARANGE_CROPS,
            False,
        ),
        axis=2,
    ).astype(_I)                                                             # [B, P, N_CROPS]
    blocked = demand > farm.seeds                                            # [B, P, N_CROPS]

    def body(u, carry):
        tl, seeds, unit_pos, carried, shed = carry
        active = lax.dynamic_index_in_dim(live, u, axis=2, keepdims=False)
        op = lax.dynamic_index_in_dim(actions.unit_op, u, axis=2, keepdims=False)
        want_crop = lax.dynamic_index_in_dim(actions.unit_crop, u, axis=2, keepdims=False)
        want_item = lax.dynamic_index_in_dim(actions.unit_item, u, axis=2, keepdims=False)
        want_qty = lax.dynamic_index_in_dim(actions.unit_qty, u, axis=2, keepdims=False)
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
        animal = _gather(tl.animal, idx)
        placed = _gather(tl.placed_day, idx)
        unfed = _gather(tl.consecutive_unfed, idx)
        fed = _gather(tl.fed_today, idx)
        cared = _gather(tl.cared_today, idx)
        fert_avail = _gather(tl.fertilizer_available, idx)
        care_bonus = _gather(tl.pending_care_bonus, idx)
        has_animal = animal != NO_ANIMAL
        # Shed access is gated on an *unlocked* access tile: three of the four sit in quadrants
        # that stay locked until bought, and hands spawn on exactly those.
        on_shed = (idx[..., None] == SHED_TILES).any(axis=-1) & (kind != LOCKED)

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

        carried_u = lax.dynamic_index_in_dim(carried, u, axis=2, keepdims=False)

        # --- HARVEST: non-ongoing crops come up with the harvest, ongoing ones stay --------
        c = jnp.where(kind == PLANT, jnp.clip(crop, 0, N_CROPS - 1), 0)
        age = day - planted_day
        doable = (
            active & (op == O.HARVEST) & (kind == PLANT) & (units > 0)
            & (age >= FIRST_YIELD_DAY[c])
        )
        got = jnp.where(doable, units, 0)
        prod = CROP_TO_PRODUCT[c]
        carried_u = carried_u + (_ARANGE_ITEMS == prod[..., None]).astype(_I) * got[..., None]
        units = jnp.where(doable, 0, units)
        cleared = doable & ~ONGOING[c]
        kind = jnp.where(cleared, EMPTY, kind)
        crop = jnp.where(cleared, NO_CROP, crop)
        lifespan = jnp.where(cleared, -1, lifespan)

        # --- HARVEST on an animal: the reference branches on the tile, not on the op --------
        a_safe = jnp.where(has_animal, jnp.clip(animal, 0, len(ANIMAL_STRUCTURE) - 1), 0)
        doable = active & (op == O.HARVEST) & has_animal & (units > 0)
        got = jnp.where(doable, units, 0)
        a_prod = ANIMAL_TO_PRODUCT[a_safe]
        carried_u = carried_u + (_ARANGE_ITEMS == a_prod[..., None]).astype(_I) * got[..., None]
        units = jnp.where(doable, 0, units)

        # --- DIG: weeds, plants, and *empty* structures. A placed animal is untouchable -----
        empty_structure = ((kind == COOP) | (kind == PASTURE)) & ~has_animal
        doable = active & (op == O.DIG) & ((kind == WEED) | (kind == PLANT) | empty_structure)
        kind = jnp.where(doable, EMPTY, kind)
        crop = jnp.where(doable, NO_CROP, crop)
        units = jnp.where(doable, 0, units)
        lifespan = jnp.where(doable, -1, lifespan)

        # --- BUILD_COOP / BUILD_PASTURE: free, instant, empty tiles only --------------------
        for op_code, structure in ((O.BUILD_COOP, COOP), (O.BUILD_PASTURE, PASTURE)):
            doable = active & (op == op_code) & (kind == EMPTY)
            kind = jnp.where(doable, structure, kind)
            animal = jnp.where(doable, NO_ANIMAL, animal)
            units = jnp.where(doable, 0, units)
            has_animal = animal != NO_ANIMAL

        # --- FEED: one carried WHEAT, once per animal per day -------------------------------
        held_wheat = carried_u[..., WHEAT_ITEM]
        doable = active & (op == O.FEED) & has_animal & ~fed & (held_wheat > 0)
        carried_u = carried_u - (_ARANGE_ITEMS == WHEAT_ITEM).astype(_I) * doable[..., None]
        fed = fed | doable

        # --- CARE: banks a bonus that only pays out on a fed production day -----------------
        doable = active & (op == O.CARE) & has_animal & ~cared
        cared = cared | doable

        # --- COLLECT_FERTILIZER: one per animal per day, refreshed nightly ------------------
        doable = active & (op == O.COLLECT_FERT) & has_animal & fert_avail
        carried_u = carried_u + (_ARANGE_ITEMS == FERT_ITEM).astype(_I) * doable[..., None]
        fert_avail = fert_avail & ~doable

        # --- FERTILIZE: spend a carried FERTILIZER, active for day..day+2 -------------------
        held_fert = carried_u[..., FERT_ITEM]
        doable = active & (op == O.FERTILIZE) & (kind == PLANT) & (held_fert > 0)
        carried_u = carried_u - (_ARANGE_ITEMS == FERT_ITEM).astype(_I) * doable[..., None]
        fert = jnp.where(doable, jnp.maximum(fert, day + 2), fert)

        # --- PLANT: only on an empty tile, and only if a seed is actually in store ----------
        # A PLANT onto an occupied tile is a free no-op in the reference. Charging a seed for it
        # anyway is the bug that failed the numpy gate 40/40 while every unit test passed, so the
        # seed is spent from `doable` (the plant landed) and never from `planting` (it was tried).
        c = jnp.clip(want_crop, 0, N_CROPS - 1)
        held = jnp.take_along_axis(seeds, c[..., None], axis=-1)[..., 0]
        barred = jnp.take_along_axis(blocked, c[..., None], axis=-1)[..., 0]
        planting = (
            active & (op == O.PLANT_OP) & (want_crop >= 0) & (want_crop < N_CROPS)
            & (held > 0) & ~barred
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

        # --- PLACE: an animal into a matching empty structure, else a partial shed drop -----
        # The reference returns from the animal branch whenever the unit stands on a matching
        # empty structure, even when the placement fails for want of the animal in hand, so the
        # fall-through is gated on the structure and not on the placement succeeding.
        animal_id = want_item - N_PRODUCTS
        is_animal = active & (animal_id >= 0) & (animal_id < len(ANIMAL_STRUCTURE))
        safe_animal = jnp.where(is_animal, jnp.clip(animal_id, 0, len(ANIMAL_STRUCTURE) - 1), 0)
        structure_match = (
            (op == O.PLACE) & is_animal & (kind == ANIMAL_STRUCTURE[safe_animal]) & ~has_animal
        )
        held_item = jnp.take_along_axis(
            carried_u, jnp.clip(want_item, 0, N_ITEMS - 1)[..., None], axis=-1)[..., 0]
        placing = structure_match & (held_item > 0)
        carried_u = carried_u - (
            (_ARANGE_ITEMS == jnp.clip(want_item, 0, N_ITEMS - 1)[..., None])
            & placing[..., None]
        ).astype(_I)
        animal = jnp.where(placing, safe_animal, animal)
        placed = jnp.where(placing, day, placed)
        units = jnp.where(placing, 0, units)
        unfed = jnp.where(placing, 0, unfed)
        fed = fed & ~placing
        cared = cared & ~placing
        fert_avail = fert_avail & ~placing
        care_bonus = jnp.where(placing, 0, care_bonus)
        has_animal = animal != NO_ANIMAL

        # --- PICKUP / DROP / PLACE-to-shed: everything that moves goods to or from the shed --
        room = jnp.maximum(0, SHED_CAP - shed.sum(axis=-1, dtype=_I))
        item_hot = (_ARANGE_ITEMS == jnp.clip(want_item, 0, N_ITEMS - 1)[..., None])

        taking = active & (op == O.PICKUP) & on_shed & (want_qty > 0)
        in_shed = jnp.take_along_axis(
            shed, jnp.clip(want_item, 0, N_ITEMS - 1)[..., None], axis=-1)[..., 0]
        take = jnp.where(taking, jnp.minimum(want_qty, in_shed), 0)
        shed = shed - item_hot.astype(_I) * take[..., None]
        carried_u = carried_u + item_hot.astype(_I) * take[..., None]

        dropping = active & (op == O.PLACE) & ~structure_match & on_shed & (want_qty > 0)
        held_item = jnp.take_along_axis(
            carried_u, jnp.clip(want_item, 0, N_ITEMS - 1)[..., None], axis=-1)[..., 0]
        give = jnp.where(dropping, jnp.minimum(jnp.minimum(want_qty, held_item), room), 0)
        shed = shed + item_hot.astype(_I) * give[..., None]
        carried_u = carried_u - item_hot.astype(_I) * give[..., None]

        # DROP empties the whole load, item by item, and destroys whatever will not fit.
        emptying = active & (op == O.DROP) & on_shed
        for it in range(N_ITEMS):
            have = jnp.where(emptying, carried_u[..., it], 0)
            room = jnp.maximum(0, SHED_CAP - shed.sum(axis=-1, dtype=_I))
            hot = (_ARANGE_ITEMS == it).astype(_I)
            shed = shed + hot * jnp.minimum(have, room)[..., None]
            carried_u = carried_u - hot * have[..., None]

        carried = lax.dynamic_update_slice_in_dim(carried, carried_u[:, :, None, :], u, axis=2)

        tl = Tiles(
            kind=_scatter(tl.kind, idx, kind),
            crop=_scatter(tl.crop, idx, crop),
            planted_day=_scatter(tl.planted_day, idx, planted_day),
            watered_today=_scatter(tl.watered_today, idx, watered),
            consecutive_unwatered=_scatter(tl.consecutive_unwatered, idx, unwatered),
            yield_units=_scatter(tl.yield_units, idx, units),
            max_lifespan_step=_scatter(tl.max_lifespan_step, idx, lifespan),
            fertilized_until_day=_scatter(tl.fertilized_until_day, idx, fert),
            animal=_scatter(tl.animal, idx, animal),
            placed_day=_scatter(tl.placed_day, idx, placed),
            consecutive_unfed=_scatter(tl.consecutive_unfed, idx, unfed),
            fed_today=_scatter(tl.fed_today, idx, fed),
            cared_today=_scatter(tl.cared_today, idx, cared),
            fertilizer_available=_scatter(tl.fertilizer_available, idx, fert_avail),
            pending_care_bonus=_scatter(tl.pending_care_bonus, idx, care_bonus),
        )
        return tl, seeds, unit_pos, carried, shed

    n_slots = jnp.max(farm.n_units)
    tl, seeds, unit_pos, carried, shed = lax.fori_loop(
        0, n_slots, body, (tiles, farm.seeds, farm.unit_pos, farm.carried, farm.shed)
    )
    return tl, farm._replace(seeds=seeds, unit_pos=unit_pos, carried=carried, shed=shed)


# ---- market ---------------------------------------------------------------------------------


def _order_book(actions):
    """Compact the turn's orders into `[B, P, MAX_ORDERS]` op/item/qty. Mirrors `Game._order_book`.

    The reference pairs the two players' i-th *orders*, so the simulator needs the same notion of
    a slot. Candidates are laid out in the order agents write them -- sells, seeds, products,
    animals, HIRE, BUY_LAND -- and a running count gives each present order its slot. Orders past
    the tenth are dropped, as `maxMarketOrdersPerTurn` does.
    """
    b, p = actions.hire.shape
    ops, items, qtys = [], [], []

    def add(kind, item_ids, qty):
        ops.append(jnp.full(qty.shape, kind, dtype=_I))
        items.append(jnp.broadcast_to(jnp.asarray(item_ids, dtype=_I), qty.shape))
        qtys.append(qty.astype(_I))

    for i in range(N_PRODUCTS):
        add(ORDER_SELL, i, actions.sell[:, :, i])
    for c in range(N_CROPS):
        add(ORDER_BUY_SEED, c, actions.buy_seed[:, :, c])
    for i in range(N_PRODUCTS):
        add(ORDER_BUY_PRODUCT, i, actions.buy_product[:, :, i])
    for a in range(N_ANIMALS):
        add(ORDER_BUY_ANIMAL, a, actions.buy_animal[:, :, a])
    # One slot per hire -- see the note in `kagg/sim/game.py::_order_book`. HIRE and BUY_LAND are
    # atomic per *slot*, not per turn, so a count of `n` emits `n` unit candidates and the existing
    # `slot < MAX_ORDERS` clamp enforces `maxMarketOrdersPerTurn`.
    n_hire = actions.hire.astype(_I)
    n_land = actions.buy_land.astype(_I)
    for k in range(MAX_ORDERS):
        add(ORDER_HIRE, 0, (n_hire > k).astype(_I))
    for k in range(MAX_ORDERS):
        add(ORDER_BUY_LAND, 0, (n_land > k).astype(_I))

    c_op = jnp.stack(ops, axis=2)
    c_item = jnp.stack(items, axis=2)
    c_qty = jnp.stack(qtys, axis=2)

    present = c_qty > 0
    slot = jnp.cumsum(present, axis=2) - 1
    # Everything that does not earn a slot is scattered into a scratch column and dropped.
    target = jnp.where(present & (slot < MAX_ORDERS), slot, MAX_ORDERS)
    bi = jnp.arange(b)[:, None, None]
    pi = jnp.arange(p)[None, :, None]

    zeros = jnp.zeros((b, p, MAX_ORDERS + 1), dtype=_I)
    op = zeros.at[bi, pi, target].set(c_op)[:, :, :MAX_ORDERS]
    item = zeros.at[bi, pi, target].set(c_item)[:, :, :MAX_ORDERS]
    qty = zeros.at[bi, pi, target].set(c_qty)[:, :, :MAX_ORDERS]
    return op, item, qty


def _process_market(farm, tiles, inventory, actions):
    """Settle the turn's orders slot by slot, both players in lockstep.

    A port of `_process_market`'s shape, not just its arithmetic: the reference walks the players'
    order lists **by slot**, so the two players' i-th orders trade against each other and against
    the same inventory. Settling all sells and then all buys prices a same-slot buy against a book
    the sells have already lifted, which `BUY_PRODUCT` makes visible on ordinary turns.

    The unit loop is a `while`, not a bounded `for`: it terminates on "nobody committed", which is
    exactly the reference's `if not committed_any: break` and cannot be made to spin.

    **Returns an accounting alongside the state**, `(farm, tiles, inventory, acct)`, where `acct`
    names every dollar this function moved: `hire` and `land` as positive costs, `trade` as the
    signed net of sells against seed / product / animal buys.

    This is instrumentation, not simulation. `step` discards it and XLA eliminates the dead
    subtractions, so the training hot path is unchanged; `step_accounted` is the entry point that
    keeps it. It is threaded out of here rather than reconstructed from state deltas outside
    because it cannot be reconstructed: `_end_of_day` zeroes `hires_today` on the last turn of
    every day, so on exactly the turns where a crew is most expensive there is no observable
    counter left to difference. `n_units` resets nightly for the same reason.
    """
    op_all, item_all, qty_all = _order_book(actions)
    # Positive numbers are money leaving the farm. `money_in` is the mark against which the net
    # trade is recovered at the end, so no sell has to be counted twice.
    money_in = farm.money
    hire_spend = jnp.zeros_like(farm.money)
    land_spend = jnp.zeros_like(farm.money)
    # Gross, not net. `trade` alone cannot answer "does the chain ever terminate in money" -- a
    # season that sells nothing and a season that sells $600 and spends $1,200 both read -$648.
    sell_income = jnp.zeros_like(farm.money)
    buy_spend = jnp.zeros_like(farm.money)

    for slot in range(MAX_ORDERS):
        sop = op_all[:, :, slot]
        sitem = item_all[:, :, slot]
        srem = qty_all[:, :, slot]

        # Atomic orders resolve once, in seat order, and then the slot is spent.
        before_hire = farm.money
        farm = _hire(farm, sop == ORDER_HIRE)
        hire_spend = hire_spend + (before_hire - farm.money)
        before_land = farm.money
        farm, tiles = _buy_land(farm, tiles, sop == ORDER_BUY_LAND)
        land_spend = land_spend + (before_land - farm.money)
        atomic = (sop == ORDER_HIRE) | (sop == ORDER_BUY_LAND)
        # A malformed sub-op is dropped rather than retried: only two products are buyable.
        bad = (sop == ORDER_BUY_PRODUCT) & ~BUYABLE[jnp.clip(sitem, 0, N_PRODUCTS - 1)]
        srem = jnp.where(atomic | bad, 0, srem)

        prod_idx = jnp.clip(sitem, 0, N_PRODUCTS - 1)

        def cond(carry):
            rem, _m, _s, _sd, _inv, _in, _out, progress = carry
            return progress & jnp.any(rem > 0)

        def body(carry):
            rem, money, shed, seeds, inv, income, outgo, _p = carry
            live = (rem > 0) & (sop != ORDER_NONE)

            # Both seats quoted from the same pre-commit inventory, before either commits.
            sell_q = jnp.take_along_axis(price(inv), prod_idx, axis=1).astype(_F)
            buy_q = jnp.take_along_axis(price(inv - 1), prod_idx, axis=1).astype(_F)
            quote = jnp.where(
                sop == ORDER_SELL, sell_q,
                jnp.where(
                    sop == ORDER_BUY_PRODUCT, buy_q,
                    jnp.where(
                        sop == ORDER_BUY_SEED, SEED_COST[jnp.clip(sitem, 0, N_CROPS - 1)],
                        jnp.where(
                            sop == ORDER_BUY_ANIMAL,
                            ANIMAL_COST[jnp.clip(sitem, 0, N_ANIMALS - 1)], 0.0))))

            committed = jnp.zeros(rem.shape[0], dtype=bool)
            for seat in range(N_PLAYERS):
                op_s, item_s = sop[:, seat], sitem[:, seat]
                live_s, q_s = live[:, seat], quote[:, seat]
                prod_hot = (_ARANGE_PRODUCTS == prod_idx[:, seat][:, None])
                item_hot = (_ARANGE_ITEMS == prod_idx[:, seat][:, None])
                crop_hot = (_ARANGE_CROPS == jnp.clip(item_s, 0, N_CROPS - 1)[:, None])
                animal_hot = (
                    _ARANGE_ITEMS == ANIMAL_ITEM[jnp.clip(item_s, 0, N_ANIMALS - 1)][:, None])

                have = jnp.sum(jnp.where(item_hot, shed[:, seat, :], 0), axis=-1)
                afford = money[:, seat] >= q_s
                selling = live_s & (op_s == ORDER_SELL) & (have > 0)
                buying = live_s & (op_s == ORDER_BUY_PRODUCT) & afford
                seeding = live_s & (op_s == ORDER_BUY_SEED) & afford
                animaling = live_s & (op_s == ORDER_BUY_ANIMAL) & afford

                spend = (buying | seeding | animaling).astype(_F) * q_s
                earned = selling.astype(_F) * q_s
                money = money.at[:, seat].add(earned - spend)
                income = income.at[:, seat].add(earned)
                outgo = outgo.at[:, seat].add(spend)
                shed = shed.at[:, seat].add(
                    item_hot.astype(_I) * (buying.astype(_I) - selling.astype(_I))[:, None]
                    + animal_hot.astype(_I) * animaling.astype(_I)[:, None])
                seeds = seeds.at[:, seat].add(crop_hot.astype(_I) * seeding.astype(_I)[:, None])
                # A unit clearing at the floor pays out but does not deepen the glut.
                inv = inv + prod_hot.astype(_I) * (
                    (selling & (q_s > PRICE_FLOOR)).astype(_I) - buying.astype(_I))[:, None]

                ok = selling | buying | seeding | animaling
                committed = committed | ok
                # A failed commit abandons the rest of that order, as the reference does.
                rem = rem.at[:, seat].set(
                    jnp.where(live_s & ~ok, 0, rem[:, seat] - ok.astype(_I)))
            return rem, money, shed, seeds, inv, income, outgo, jnp.any(committed)

        _rem, money, shed, seeds, inventory, sell_income, buy_spend, _prog = lax.while_loop(
            cond, body,
            (srem, farm.money, farm.shed, farm.seeds, inventory,
             sell_income, buy_spend, jnp.asarray(True)),
        )
        farm = farm._replace(money=money, shed=shed, seeds=seeds)

    # Net trade is recovered rather than accumulated: everything this function moved is either a
    # hire, a land purchase, or a trade, so the residual IS the trade. That makes the invariant
    # `trade - hire - land == money_end - money_start` true by construction rather than by
    # agreement between two separately-maintained counters, which is the failure species
    # `CLAUDE.md` records for the per-opponent win rate.
    acct = {
        "hire": hire_spend,
        "land": land_spend,
        "trade": (farm.money - money_in) + hire_spend + land_spend,
        # Gross halves of `trade`, accumulated rather than recovered. They are kept as a *separate*
        # pair of counters precisely so that `sell == trade + buy` is an independent check rather
        # than an identity -- if the two ever disagree, one of them is wrong, and a decomposition
        # that cannot be caught being wrong is not worth having.
        "sell": sell_income,
        "buy": buy_spend,
    }
    return farm, tiles, inventory, acct


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

    # A new hand takes the least-occupied shed-access tile, ties broken in NWSE order -- a port of
    # `_spawn_hand`, matching `farm.hire`. Spawning every hand on NW instead is not a harmless
    # approximation: a hand standing elsewhere works different tiles, so the banks part company
    # within a few hundred steps of the first hire.
    live = _ARANGE_UNITS[None, None, :] < farm.n_units[:, :, None]          # [B, P, U]
    on_tile = (
        (farm.unit_pos[:, :, :, None, 0] == SHED_ACCESS[None, None, None, :, 0])
        & (farm.unit_pos[:, :, :, None, 1] == SHED_ACCESS[None, None, None, :, 1])
        & live[..., None]
    )                                                                       # [B, P, U, 4]
    occupancy = on_tile.sum(axis=2)                                         # [B, P, 4]
    choice = jnp.argmin(occupancy, axis=-1)                                 # first min, so NWSE
    spawn = SHED_ACCESS[choice]                                             # [B, P, 2]

    return farm._replace(
        money=jnp.where(doable, farm.money - cost, farm.money),
        hires_today=farm.hires_today + doable.astype(_I),
        n_units=farm.n_units + doable.astype(_I),
        unit_pos=jnp.where(sel[..., None], spawn[:, :, None, :], farm.unit_pos),
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
    """Units the town removes this step. Shops tick every 4 steps, the centre every 12.

    `step` and `day` are `[B]` now, so every comparison against them needs a trailing axis to line
    up with the `[B, N_PRODUCTS]` result.
    """
    unlocked = (unlock_day <= day[:, None]).astype(_I)
    shops = jnp.where((step % W.SHOP_INTERVAL == 0)[:, None], unlocked @ SHOP_PULL, 0)
    centre = jnp.where(
        (step % W.CENTER_INTERVAL == 0)[:, None],
        _center_multiplier(day)[:, None] * CENTER_PULL[None, :], 0
    )
    return shops + centre


def _decay_plants(tiles, step):
    """A finished plant loses a unit every *other* step counted from the lifespan boundary.

    `step` is `[B]`; tile fields are `[B, P, TILES]`, so it needs two trailing axes.
    """
    mls = tiles.max_lifespan_step
    step = step[:, None, None]
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
    """The nightly transition: watering enforcement, then ongoing production, in that order.

    `current_day` is `[B]`; every tile field is `[B, P, TILES]`, so it needs two trailing axes.
    """
    current_day = current_day[:, None, None]
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
    flat = farm.carried.reshape(b, p, MAX_UNITS * N_ITEMS)
    start = jnp.sum(farm.shed, axis=-1, dtype=_I)[..., None]
    inclusive = jnp.cumsum(flat, axis=-1, dtype=_I)
    exclusive = inclusive - flat
    take = jnp.minimum(SHED_CAP, start + inclusive) - jnp.minimum(SHED_CAP, start + exclusive)
    shed = farm.shed + take.reshape(b, p, MAX_UNITS, N_ITEMS).sum(axis=2, dtype=_I)
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


def _daily_refresh_animals(tiles, current_day):
    """Port of `_daily_refresh_animals`. Order is load-bearing; see the numpy twin in `ops.py`.

    Unfed twice and the animal escapes, leaving the bare structure. Production lands on the
    interval from `first_yield_day`, capped at `max_held`. The care bonus is consumed only on a day
    that both fed and produced, and a fresh one is banked only when the animal was cared for *and*
    fed.
    """
    current_day = current_day[:, None, None]
    next_day = current_day + 1
    has_animal = tiles.animal != NO_ANIMAL
    fed = tiles.fed_today & has_animal

    unfed = jnp.where(has_animal, jnp.where(fed, 0, tiles.consecutive_unfed + 1),
                      tiles.consecutive_unfed)
    escaped = has_animal & (unfed >= 2)

    animal = jnp.where(escaped, NO_ANIMAL, tiles.animal)
    units = jnp.where(escaped, 0, tiles.yield_units)
    bonus_held = jnp.where(escaped, 0, tiles.pending_care_bonus)
    unfed = jnp.where(escaped, 0, unfed)

    live = has_animal & ~escaped
    a = jnp.where(live, jnp.clip(animal, 0, len(ANIMAL_STRUCTURE) - 1), 0)

    days_since = next_day - tiles.placed_day - ANIMAL_FIRST_YIELD_DAY[a]
    interval = jnp.maximum(ANIMAL_INTERVAL[a], 1)
    produces = live & (days_since >= 0) & ((days_since % interval) == 0)

    bonus = jnp.where(produces & fed, bonus_held, 0)
    units = jnp.where(produces, jnp.minimum(ANIMAL_MAX_HELD[a], units + 1 + bonus), units)
    bonus_held = jnp.where(produces, 0, bonus_held)

    banked = live & tiles.cared_today & fed
    bonus_held = jnp.where(banked, bonus_held + 1, bonus_held)

    return tiles._replace(
        animal=animal,
        yield_units=units,
        consecutive_unfed=unfed,
        pending_care_bonus=bonus_held,
        fertilizer_available=jnp.where(live, True, tiles.fertilizer_available),
        fed_today=jnp.where(live, False, tiles.fed_today),
        cared_today=jnp.where(live, False, tiles.cared_today),
    )


def _night(tiles, farm, key, day, weed_chance):
    tiles = _daily_refresh_plants(tiles, day)
    # `_end_of_day` refreshes plants and then animals, in that order, per farm.
    tiles = _daily_refresh_animals(tiles, day)
    if weed_chance:
        key, sub = jax.random.split(key)
        roll = jax.random.uniform(sub, tiles.kind.shape)
        tiles = tiles._replace(
            kind=jnp.where((tiles.kind == EMPTY) & (roll < weed_chance), WEED, tiles.kind)
        )
    return tiles, _end_of_day(farm), key


# ---- the loop --------------------------------------------------------------------------------


def _select_per_game(mask, a, b):
    """Pick `a` where `mask[g]`, else `b`, for pytrees whose arrays lead with the game axis."""
    return jax.tree_util.tree_map(
        lambda x, y: jnp.where(mask.reshape((-1,) + (1,) * (x.ndim - 1)), x, y), a, b)


@functools.partial(jax.jit, static_argnames=("weed_chance",))
def step(state, actions, weed_chance=0.0):
    """Advance every game by one turn. The whole turn is one traced graph.

    Phase order follows the reference exactly and is not cosmetic: selling happens *before* the
    town drains, so the price a player receives is set by the pre-drain inventory. Swapping the
    two shifts every sale price in the game.
    """
    return step_accounted(state, actions, weed_chance)[0]


def step_accounted(state, actions, weed_chance=0.0):
    """`step`, plus a decomposition of every dollar the turn moved.

    Returns `(state, acct)` where `acct` maps `"hire"` / `"land"` / `"trade"` to `[B, P]` arrays.
    `hire` and `land` are positive costs; `trade` is the signed net of sells against buys. The
    invariant, pinned by `tests/test_money_accounting.py`, is exact:

        money_after - money_before == trade - hire - land

    with no tolerance, because money is float64 under the x64 flag and every mutation is an add of
    a quoted price. A residual would mean the decomposition describes something other than what
    happened.

    **There is no upkeep line, and that is a fact about the game rather than an omission here.**
    `_end_of_day` and `_night` move no money at all. What looks like upkeep is `hire`: the crew is
    reset to a single unit every night, so holding a crew of N costs `sum(HIRE_COST[:N])` *every
    day*, and `HIRE_COST` is Fibonacci -- $54/day for eight units, $376/day for twelve, $986/day
    for fourteen. A policy that re-hires each morning is paying a large recurring bill that is
    booked as a one-off purchase, which is exactly the kind of thing a per-game-day bank curve
    hides.
    """
    actions = _canonical(actions)
    day = state.step_index // TURNS_PER_DAY                # [B]

    tiles, farm = _apply_unit_actions(state.tiles, state.farm, actions, day)

    # One slot-paired pass now covers sells, seeds, products, animals, hiring and land, because
    # the reference settles them together and their order relative to one another is observable.
    farm, tiles, inventory, acct = _process_market(farm, tiles, state.inventory, actions)

    inventory = inventory - _drain(state.step_index, day, state.unlock_day)
    tiles = _decay_plants(tiles, state.step_index)

    # Night is now per game, so it cannot be a `lax.cond` on a scalar: different games cross the
    # day boundary on different turns. The nightly transition is computed for every game and
    # selected where it applies. That costs the night path on every step rather than one turn in
    # 24 -- the price of letting episodes run out of phase, and cheaper than the alternative of
    # vmapping several whole simulator states, which multiplies the compiled graph instead.
    is_night = (((state.step_index + 1) % TURNS_PER_DAY) == 0)          # [B]
    n_tiles, n_farm, n_key = _night(tiles, farm, state.key, day, weed_chance)
    tiles = _select_per_game(is_night, n_tiles, tiles)
    farm = _select_per_game(is_night, n_farm, farm)
    key = n_key

    return state._replace(
        step_index=state.step_index + 1,
        tiles=tiles,
        farm=farm,
        inventory=inventory,
        key=key,
    ), acct


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
        return self.step_index // TURNS_PER_DAY          # [B]

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
