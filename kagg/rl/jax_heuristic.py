"""A competent farmer that runs inside the compiled rollout.

**Why this exists.** The RL opponent pool is frozen copies of a policy that has never farmed, plus
two scripted seats that bank $3,000 and $3,368. Nothing in it can punish a bad farm, so once the
policy clears the trader there is no opponent left with any play in it. `contrarian` and `converter`
bank $51k and could -- but they are Python agents over dict observations, and a Python agent cannot
run inside `jax.lax.scan`.

The options were: a `pure_callback` per turn (works, but serialises 256 games through Python every
step), or porting the logic to array operations. This is the port. It costs nothing at run time
because it is the same kind of code as `jax_masks.py`.

**Scope, stated honestly: this is the crop economy only.** Melon in, water it, harvest it, sell it.
That is the half that earns `contrarian`'s $51k, and it is deliberately not the animal economy --
which is the harder half, and the half `converter` gets wrong (562 PICKUP against 197 FEED, animals
accumulating unplaced in the shed). An opponent does not need to be our best agent. It needs to
beat a policy that does nothing, by enough that doing nothing stops being a draw.

**The one structural difference from the Python version.** `converter` allocates jobs with a
`claimed` set, walking units in order and letting each take the nearest unclaimed tile. That is
sequential state and does not vectorise. Here each unit takes the `i`-th nearest job instead, which
needs no shared state and gives the same non-overlapping allocation for the common case. It is a
worse allocation when the crew is larger than the job list; the cost is a unit walking further than
it had to, never two units fighting over one tile.
"""

import jax
import jax.numpy as jnp

from kagg.sim import jax_sim as J
from kagg.sim import ops as O
from kagg.sim.tiles import CROP_INDEX, EMPTY, FIRST_YIELD_DAY, MAX_YIELD_DAY, PLANT

MELON = CROP_INDEX["MELON"]
# Pinned as JAX arrays: these are indexed by `t.crop`, which is traced under jit, and a numpy array
# indexed by a tracer raises rather than lowering to a gather.
_FIRST_YIELD = jnp.asarray(FIRST_YIELD_DAY)
_MAX_YIELD_DAY = jnp.asarray(MAX_YIELD_DAY)
_XS = jnp.arange(J.BOARD * J.BOARD) % J.BOARD
_YS = jnp.arange(J.BOARD * J.BOARD) // J.BOARD
_BIG = jnp.int32(10_000)

# Defaults chosen to match what the island ES found for `converter`, which beat `contrarian` 87.5%
# head to head: melon is winner-take-all and worth committing to, and the crew is worth paying for
# once there is work.
MELON_TILES = 16
TARGET_HANDS = 10
CARRY_BEFORE_DROP = 6
SELL_MIN = 3
# Melon needs twelve days from planting to the end of its yield window, so seed bought later than
# this cannot mature before the season ends and is money set on fire.
LAST_PLANT_DAY = 16


def _step_toward(pos, target):
    """One legal step along the larger axis first, ties preferring horizontal.

    Mirrors `converter._step_toward` exactly so the two agents route the same way.
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
    """Flat index of the `rank`-th nearest true entry in `candidate`, or -1 if there are too few.

    `candidate` is [B, P, 100] bool; `pos` is [B, P, 2]; `rank` is a scalar. Distances to masked-out
    tiles are pushed past any real distance so they sort last, and the rank is then read straight
    out of the sort -- no loop, no shared state between units.
    """
    dist = jnp.abs(_XS[None, None, :] - pos[..., 0:1]) + jnp.abs(_YS[None, None, :] - pos[..., 1:2])
    dist = jnp.where(candidate, dist, _BIG)
    order = jnp.argsort(dist, axis=-1)
    idx = jnp.take_along_axis(order, jnp.full(pos.shape[:-1] + (1,), rank), axis=-1)[..., 0]
    ok = jnp.take_along_axis(dist, idx[..., None], axis=-1)[..., 0] < _BIG
    return jnp.where(ok, idx, -1)


def outstanding_jobs(state):
    """Tiles wanting work, per seat: `[B, P]`. Crop-agnostic, so it reads any policy's board.

    **This is a measurement, not a rule.** `actions` below sizes its own crew as
    `1 + jobs // 2` and that is fine -- it is a scripted agent and is allowed strategy. The learned
    policy is not given that relationship, because a prior asserting "hire in proportion to work"
    is a ratio read off what happens to work, the same species as "buy land on day 10", and it
    would cap the ceiling at whatever ratio was picked.

    What the trainer does with this is *log* it beside `crew`, which answers a question that was
    otherwise unanswerable: `hire` tripled to 0.331 the moment its prior target was removed, while
    every farming op collapsed and the bank fell to $527. If crew tracks this number, hiring is not
    the problem and the crew simply cannot convert work into money. If crew is flat while this
    swings, the policy cannot connect an eight-hires-a-day habit to a bad ending thirty days later
    through a critic at `ev_signal ~ 0.3` -- which is credit assignment, and pushing the prior
    harder would only have hidden it.

    Deliberately *not* the same expression `actions` uses: that one counts melon seed only, because
    it is a melon agent. This counts every crop's seed, because the policy plants whatever it likes
    and a melon-only count would read as "no work available" on a board full of carrots.
    """
    t, farm = state.tiles, state.farm
    day = (state.step_index // J.TURNS_PER_DAY)[:, None, None]
    is_plant = t.kind == PLANT
    ripe = is_plant & (day - t.planted_day >= _FIRST_YIELD[jnp.maximum(t.crop, 0)]) \
        & (t.yield_units > 0)
    dry = is_plant & ~t.watered_today
    free = t.kind == EMPTY
    return (dry.sum(axis=-1) + ripe.sum(axis=-1)
            + jnp.minimum(free.sum(axis=-1), farm.seeds.sum(axis=-1)))


def actions(state):
    """A `jax_sim.Actions` for both seats. Only seat selection decides who actually uses it."""
    t, farm = state.tiles, state.farm
    b = farm.money.shape[0]
    day = (state.step_index // J.TURNS_PER_DAY)[:, None]          # [B, 1]

    # ---- what is on the board ---------------------------------------------------------------
    is_plant = t.kind == PLANT
    age = day[..., None] - t.planted_day
    ripe = is_plant & (age >= _FIRST_YIELD[jnp.maximum(t.crop, 0)]) & (t.yield_units > 0)
    # A crop only accrues yield on a watered day inside its window, and two dry days kill it, so
    # "needs water" is both the urgent job and the productive one.
    dry = is_plant & ~t.watered_today
    free = t.kind == EMPTY

    # ---- units -------------------------------------------------------------------------------
    pos = farm.unit_pos                                            # [B, P, U, 2]
    live = jnp.arange(J.MAX_UNITS)[None, None, :] < farm.n_units[..., None]
    flat = pos[..., 1] * J.BOARD + pos[..., 0]                     # [B, P, U]
    on_shed = (flat[..., None] == J.SHED_TILES).any(axis=-1)
    carrying = farm.carried.sum(axis=-1)                           # [B, P, U]
    seeds_left = farm.seeds[..., MELON]                            # [B, P]

    def under(field):
        """The value of a board field on the tile each unit is standing on."""
        return jnp.take_along_axis(field[:, :, None, :].repeat(J.MAX_UNITS, axis=2),
                                   flat[..., None], axis=-1)[..., 0]

    here_ripe, here_dry, here_free = under(ripe), under(dry), under(free)

    # ---- the priority cascade ----------------------------------------------------------------
    # Ordered exactly as the Python agent orders it, and for the reasons recorded there: watering
    # outranks planting because a seed put in today dies overnight unless the same day waters it,
    # and harvesting outranks both because produce in the ground earns nothing.
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

    commit(here_ripe & (carrying < 12), O.HARVEST)
    commit(here_dry, O.WATER)
    commit(here_free & (seeds_left[..., None] > 0), O.PLANT_OP, MELON)
    commit(on_shed & (carrying >= CARRY_BEFORE_DROP), O.DROP)

    # Anything still undecided walks toward its own job. Each unit takes the rank-th nearest, so
    # two units never target the same tile without any shared `claimed` state.
    rank = jnp.arange(J.MAX_UNITS)

    def route(candidate):
        idx = jax.vmap(lambda r: _nth_nearest(pos[:, :, 0], candidate, r),
                       out_axes=-1)(rank)                          # [B, P, U]
        tgt = jnp.stack([idx % J.BOARD, idx // J.BOARD], axis=-1)
        return idx, _step_toward(pos, tgt)

    # Full hands go to the shed first; the nightly drop destroys anything over the 100-item cap.
    shed_xy = jnp.stack([J.SHED_TILES % J.BOARD, J.SHED_TILES // J.BOARD], axis=-1)
    d_shed = jnp.abs(shed_xy[None, None, None, :, 0] - pos[..., 0:1]) + \
        jnp.abs(shed_xy[None, None, None, :, 1] - pos[..., 1:2])
    nearest_shed = shed_xy[jnp.argmin(d_shed, axis=-1)]
    commit(carrying >= CARRY_BEFORE_DROP, _step_toward(pos, nearest_shed))

    for candidate in (ripe, dry):
        idx, step = route(candidate)
        commit(idx >= 0, step)

    idx, step = route(free)
    commit((idx >= 0) & (seeds_left[..., None] > 0), step)

    jobs = (dry.sum(axis=-1) + ripe.sum(axis=-1)
            + jnp.minimum(free.sum(axis=-1), farm.seeds[..., MELON]))

    # ---- market ------------------------------------------------------------------------------
    zeros_p = jnp.zeros((b, 2, J.N_PRODUCTS), dtype=J._I)
    sell = jnp.where(farm.shed[..., :J.N_PRODUCTS] >= SELL_MIN,
                     farm.shed[..., :J.N_PRODUCTS], 0).astype(J._I)
    # Wheat is an input, not a product: the town drains it all season and its price only rises.
    sell = sell.at[..., O.WHEAT_ITEM].set(0)

    # **Replant, and stop paying a crew with nothing to do.**
    #
    # Buying seed only on day 0 gave exactly one melon cycle: 19 tiles standing from day 2, harvested
    # on day 11 for a jump from $599 to $17,259, and then eighteen days of an empty farm bleeding
    # $176/day in wages down to $15,676. Melon takes twelve days from planting to its yield window
    # closing, so there is room for a second cycle if the seed goes in by about day 16.
    n_plants = is_plant.sum(axis=-1)                               # [B, P]
    short = jnp.maximum(0, MELON_TILES - farm.seeds[..., MELON] - n_plants)
    can_mature = day <= LAST_PLANT_DAY
    buy_seed = jnp.zeros((b, 2, J.N_CROPS), dtype=J._I)
    buy_seed = buy_seed.at[..., MELON].set(
        jnp.where(can_mature & (farm.money > 1500.0), short, 0).astype(J._I))

    return J.Actions(
        unit_op=jnp.where(live, op, O.NOOP).astype(J._I),
        unit_crop=crop.astype(J._I),
        unit_item=jnp.zeros_like(op, dtype=J._I),
        unit_qty=jnp.ones_like(op, dtype=J._I),
        sell=sell,
        buy_seed=buy_seed,
        buy_product=zeros_p,
        buy_animal=jnp.zeros((b, 2, J.N_ANIMALS), dtype=J._I),
        # Sized to outstanding work, not held flat. Hands are dismissed nightly and the Fibonacci
        # fee resets each morning, so crew size is a free daily choice -- and an idle hand is pure
        # cost. Measured: eighteen idle days cost more than a fifth of the season's earnings.
        hire=(farm.n_units < jnp.minimum(TARGET_HANDS, 1 + jobs // 2)) & (farm.money > 500.0),
        buy_land=jnp.zeros((b, 2), dtype=bool),
    )
