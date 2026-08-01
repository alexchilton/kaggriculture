"""A livestock-and-wheat agent that runs inside the compiled rollout.

**Why this exists.** `jax_heuristic` is the crop economy only, by explicit design, and it banks
$23,783. It was the RL pool's only opponent with any play in it, so the policy has never once been
punished for ignoring the animal economy -- and the animal economy is the game.

Measured, over 312 real leaderboard seats spanning $3.5k to $132k. Spearman correlation of each op's
share of a seat's actions with the money it banked:

    FEED   +0.452     PICKUP        +0.381     PLANT  -0.358
    CARE   +0.441     BUILD_PASTURE +0.376     WATER  -0.276
    harv/plant +0.439 DROP          +0.371     MOVE   -0.098
                      COLLECT_FERT  +0.340

Six of the top seven are the wheat -> animal -> product pipeline, and the two crop ops are
*negatively* correlated: the top decile plants 1.27% of its actions against the bottom quartile's
3.77%, and waters 7.6% against 17.7%. Heavy farming is the signature of a player who caps out low.

The top 25 seats' playbook, measured the same way:

    animals      median 11 -- SHEEP 55%, COW 43%, GOOSE 1.8%   (pastures, not coops)
    first animal turn 1 (day 0);  last day 11
    wheat        BOUGHT, median 295 orders, first at turn 2 -- not grown
    crew         median 12, peak 13 (re-hired nightly, 281 orders)
    land         2 quadrants, first at median turn 242 = day 10
    feed:care    1.01 -- fed and cared in equal measure
    sells        WHEAT 47.5%, FERTILIZER 23.1%, WOOL 12.0%, MILK 9.1%

So: buy livestock immediately, buy wheat to feed it, harvest wool and milk, collect the fertiliser
the animals produce, sell all four, and buy land only once there is income to justify it. Planting is
a rounding error -- the top seats plant about eighty times in a season.

**Two rules this had to respect.** An animal escapes after two unfed nights (`jax_sim` `unfed >= 2`)
and every first-yield day is later -- GOOSE 4, COW 8, SHEEP 6 -- so an animal that is not fed every
single day is a guaranteed total loss of its $300-$500. Feeding is therefore not an optimisation, it
is the whole position. And `FEED` consumes one carried WHEAT per animal per day, so a unit must be
holding wheat when it arrives: the shed round trip is part of the loop, not an overhead on it.
"""

import jax
import jax.numpy as jnp

from kagg.sim import jax_sim as J
from kagg.sim import ops as O
from kagg.sim.tiles import ANIMAL_STRUCTURE, EMPTY, NO_ANIMAL, PASTURE

_XS = jnp.arange(J.BOARD * J.BOARD) % J.BOARD
_YS = jnp.arange(J.BOARD * J.BOARD) // J.BOARD
_BIG = jnp.int32(10_000)

COW = 1
SHEEP = 2
COW_ITEM = int(J.N_PRODUCTS) + COW
SHEEP_ITEM = int(J.N_PRODUCTS) + SHEEP
FERT_ITEM = 8
_ANIMAL_STRUCTURE = jnp.asarray(ANIMAL_STRUCTURE)

# Sized from the measured playbook above, not tuned. These are the dials an ES pass would move.
TARGET_ANIMALS = 11
TARGET_HANDS = 12
# **The shed holds 100 items and the nightly dump discards the overflow**, so wheat sitting in it is
# not a buffer, it is a claim on the only storage the produce has. First version bought to
# 3 x herd and accumulated 67 wheat by day 29; 5,408 harvested products arrived over the season and
# the shed ended with five, the rest destroyed on the nightly dump. Buy one day of feed, no more.
# **But the shed must still hold enough for the whole crew in one morning.** PICKUP takes
# `min(want_qty, in_shed)` against a shed shared by every unit, so a crew of fifteen each asking for
# six against a shed of twelve leaves most of them empty-handed -- and an empty-handed unit retries
# next turn, which is what drove PICKUP to 38-52% of all actions. Feed is one wheat per animal per
# day, so hold a couple of days of it and have each unit carry a small share.
WHEAT_PER_ANIMAL = 4
CARRY_WHEAT = 2               # wheat a unit takes from the shed before setting out, in one action
CARRY_BEFORE_DROP = 6
# Sell on sight. Produce waiting for a batch of three is produce risking the cap, and the glut curves
# punish dumping far less than the dump destroys.
SELL_MIN = 1
SHED_SOFT_CAP = 60            # stop buying wheat above this, to leave room for produce
LAND_DAY = 10                 # median first land purchase across 312 real seats
LAND_MIN_MONEY = 6000.0
LAST_ANIMAL_DAY = 11          # measured last animal purchase; later cannot reach first yield


def _step_toward(pos, target):
    """One legal step along the larger axis first, ties preferring horizontal.

    Identical to `jax_heuristic._step_toward` so both agents route the same way and a difference
    between them is never a routing artifact.
    """
    dx = target[..., 0] - pos[..., 0]
    dy = target[..., 1] - pos[..., 1]
    horiz = (dx != 0) & ((jnp.abs(dx) >= jnp.abs(dy)) | (dy == 0))
    return jnp.where(
        horiz,
        jnp.where(dx > 0, O.EAST, O.WEST),
        jnp.where(dy != 0, jnp.where(dy > 0, O.SOUTH, O.NORTH), O.NOOP),
    ).astype(jnp.int32)


def _nth_nearest(pos, candidate, rank):
    """Flat index of the `rank`-th nearest true entry, or -1 if there are too few.

    The rank is what stops two units walking to the same animal without any shared claim state --
    the same device `jax_heuristic` uses, and the thing the RL policy's own observation still lacks.
    """
    dist = jnp.abs(_XS[None, None, :] - pos[..., 0:1]) + jnp.abs(_YS[None, None, :] - pos[..., 1:2])
    dist = jnp.where(candidate, dist, _BIG)
    order = jnp.argsort(dist, axis=-1)
    idx = jnp.take_along_axis(order, jnp.full(pos.shape[:-1] + (1,), rank), axis=-1)[..., 0]
    ok = jnp.take_along_axis(dist, idx[..., None], axis=-1)[..., 0] < _BIG
    return jnp.where(ok, idx, -1)


def actions(state):
    """A `jax_sim.Actions` for both seats; seat selection decides who uses it."""
    t, farm = state.tiles, state.farm
    b = farm.money.shape[0]
    day = (state.step_index // J.TURNS_PER_DAY)[:, None]              # [B, 1]

    # ---- board ------------------------------------------------------------------------------
    has_animal = t.animal != NO_ANIMAL
    # Product waiting on an animal. Ripeness for animals is just "units held", with no lifetime cap.
    animal_ripe = has_animal & (t.yield_units > 0)
    needs_feed = has_animal & ~t.fed_today
    needs_care = has_animal & ~t.cared_today
    has_fert = has_animal & t.fertilizer_available
    empty_pasture = (t.kind == PASTURE) & ~has_animal
    buildable = t.kind == EMPTY

    n_animals = has_animal.sum(axis=-1)                               # [B, P]
    n_pasture = ((t.kind == PASTURE) & ~has_animal).sum(axis=-1)

    # ---- units ------------------------------------------------------------------------------
    pos = farm.unit_pos                                               # [B, P, U, 2]
    live = jnp.arange(J.MAX_UNITS)[None, None, :] < farm.n_units[..., None]
    flat = pos[..., 1] * J.BOARD + pos[..., 0]
    on_shed = (flat[..., None] == J.SHED_TILES).any(axis=-1)
    carried = farm.carried                                            # [B, P, U, N_ITEMS]
    carrying = carried.sum(axis=-1)
    held_wheat = carried[..., O.WHEAT_ITEM]
    held_cow = carried[..., COW_ITEM]
    held_sheep = carried[..., SHEEP_ITEM]
    held_animal = held_cow + held_sheep
    shed_wheat = farm.shed[..., O.WHEAT_ITEM]                         # [B, P]
    shed_cow = farm.shed[..., COW_ITEM]
    shed_sheep = farm.shed[..., SHEEP_ITEM]
    shed_animal = shed_cow + shed_sheep

    def under(field):
        return jnp.take_along_axis(field[:, :, None, :].repeat(J.MAX_UNITS, axis=2),
                                   flat[..., None], axis=-1)[..., 0]

    here_ripe = under(animal_ripe)
    here_feed = under(needs_feed)
    here_care = under(needs_care)
    here_fert = under(has_fert)
    here_pasture = under(empty_pasture)
    here_build = under(buildable)

    # ---- the priority cascade ---------------------------------------------------------------
    # **Feeding outranks everything that is not already free.** Two unfed nights and the animal is
    # gone with its whole purchase price, while a harvest merely waits. `CARE` is next because the
    # measured feed:care ratio is 1.01 -- the top agents treat them as one visit, and the care bonus
    # is only realised on a day that both fed and produced.
    op = jnp.full(flat.shape, O.NOOP, dtype=jnp.int32)
    item = jnp.zeros_like(op)
    taken = jnp.zeros(flat.shape, dtype=bool)

    def commit(mask, new_op, new_item=None):
        nonlocal op, item, taken
        do = mask & ~taken & live
        op = jnp.where(do, new_op, op)
        if new_item is not None:
            item = jnp.where(do, new_item, item)
        taken = taken | do

    commit(here_feed & (held_wheat > 0), O.FEED)
    commit(here_ripe & (carrying < 12), O.HARVEST)
    commit(here_care, O.CARE)
    commit(here_fert & (carrying < 12), O.COLLECT_FERT)
    # Placing a carried animal on an empty pasture. `PLACE` reads `unit_item`, and the structure has
    # to match: cow and sheep are both PASTURE animals, which is why geese are not bought at all.
    commit(here_pasture & (held_cow > 0), O.PLACE, COW_ITEM)
    commit(here_pasture & (held_sheep > 0), O.PLACE, SHEEP_ITEM)
    # Pastures are free and instant, so build them wherever a unit happens to stand while there are
    # animals still to house.
    want_pasture = (n_pasture + n_animals) < TARGET_ANIMALS
    commit(here_build & want_pasture[..., None], O.BUILD_PASTURE)

    # At the shed: drop produce, then take an animal to house, then top up wheat.
    commit(on_shed & (carrying - held_wheat >= CARRY_BEFORE_DROP), O.DROP)
    commit(on_shed & (shed_cow[..., None] > 0) & (held_animal == 0), O.PICKUP, COW_ITEM)
    commit(on_shed & (shed_sheep[..., None] > 0) & (held_animal == 0), O.PICKUP, SHEEP_ITEM)
    # **One pickup, not one per unit of wheat.** `unit_qty` is per action, so taking a day's feed in
    # a single PICKUP is what stops units standing on the shed re-picking every turn -- the first
    # version emitted PICKUP on 52% of all unit actions against a measured winner target of 2.3%.
    commit(on_shed & (shed_wheat[..., None] > 0) & (held_wheat == 0), O.PICKUP, O.WHEAT_ITEM)

    # ---- routing ----------------------------------------------------------------------------
    rank = jnp.arange(J.MAX_UNITS)

    def route(candidate):
        idx = jax.vmap(lambda r: _nth_nearest(pos[:, :, 0], candidate, r), out_axes=-1)(rank)
        tgt = jnp.stack([idx % J.BOARD, idx // J.BOARD], axis=-1)
        return idx, _step_toward(pos, tgt)

    shed_xy = jnp.stack([J.SHED_TILES % J.BOARD, J.SHED_TILES // J.BOARD], axis=-1)
    d_shed = jnp.abs(shed_xy[None, None, None, :, 0] - pos[..., 0:1]) + \
        jnp.abs(shed_xy[None, None, None, :, 1] - pos[..., 1:2])
    to_shed = _step_toward(pos, shed_xy[jnp.argmin(d_shed, axis=-1)])

    # A unit carrying an animal is holding $300-$500 of idle capital; house it before anything else.
    idx, step = route(empty_pasture)
    commit((held_animal > 0) & (idx >= 0), step)

    # Out of wheat with animals to feed, or produce to bank: go to the shed.
    commit((held_wheat == 0) & (shed_wheat[..., None] > 0)
           & (needs_feed.sum(axis=-1)[..., None] > 0), to_shed)
    commit(carrying - held_wheat >= CARRY_BEFORE_DROP, to_shed)
    commit((held_animal == 0) & (shed_animal[..., None] > 0), to_shed)

    # Then the jobs, hungriest first.
    for candidate in (needs_feed, animal_ripe, needs_care, has_fert):
        idx, step = route(candidate)
        commit(idx >= 0, step)

    # Nothing to do near an animal: build out the pasture capacity.
    idx, step = route(buildable)
    commit((idx >= 0) & want_pasture[..., None], step)

    # ---- market -----------------------------------------------------------------------------
    zeros_p = jnp.zeros((b, 2, J.N_PRODUCTS), dtype=J._I)

    # Sell every product the shed holds, except wheat, which is feedstock. The measured playbook
    # sells wheat heavily, but it is buying and reselling on price swings -- a timing strategy this
    # agent deliberately does not attempt, because holding feed is worth more than the spread.
    sell = jnp.where(farm.shed[..., :J.N_PRODUCTS] >= SELL_MIN,
                     farm.shed[..., :J.N_PRODUCTS], 0).astype(J._I)
    sell = sell.at[..., O.WHEAT_ITEM].set(0)

    # Buy wheat to a buffer sized by the herd. Running dry costs animals, so this is the one order
    # that must never be skipped.
    shed_total = farm.shed.sum(axis=-1)
    want_wheat = jnp.maximum(
        0, WHEAT_PER_ANIMAL * jnp.maximum(n_animals, 1) + farm.n_units - shed_wheat)
    buy_product = zeros_p.at[..., O.WHEAT_ITEM].set(
        jnp.where((farm.money > 200.0) & (shed_total < SHED_SOFT_CAP),
                  jnp.minimum(want_wheat, 20), 0).astype(J._I))

    # Buy livestock immediately and stop at the measured last useful day: an animal bought after
    # day 11 cannot reach its first yield before the season ends.
    room = TARGET_ANIMALS - (n_animals + shed_animal)
    can_buy = (day <= LAST_ANIMAL_DAY) & (room > 0) & (farm.money > 900.0)
    buy_animal = jnp.zeros((b, 2, J.N_ANIMALS), dtype=J._I)
    # Sheep 55% / cow 43% in the measured mix; alternate so both are represented without a RNG.
    take_sheep = can_buy & ((n_animals + shed_animal) % 2 == 0)
    take_cow = can_buy & ~take_sheep
    buy_animal = buy_animal.at[..., SHEEP].set(take_sheep.astype(J._I))
    buy_animal = buy_animal.at[..., COW].set(take_cow.astype(J._I))

    return J.Actions(
        unit_op=jnp.where(live, op, O.NOOP).astype(J._I),
        unit_crop=jnp.zeros_like(op, dtype=J._I),
        unit_item=item.astype(J._I),
        # `unit_qty` is read per action. A wheat pickup takes a day's feed in one go; every other
        # op wants one.
        unit_qty=jnp.where((op == O.PICKUP) & (item == O.WHEAT_ITEM),
                           CARRY_WHEAT, 1).astype(J._I),
        sell=sell,
        buy_seed=jnp.zeros((b, 2, J.N_CROPS), dtype=J._I),
        buy_product=buy_product,
        buy_animal=buy_animal,
        # Every animal is a daily feed-plus-care visit, so the crew scales with the herd rather than
        # with a fixed target. Hands are dismissed nightly and the Fibonacci fee resets each morning.
        hire=(farm.n_units < jnp.minimum(TARGET_HANDS, 2 + n_animals))
             & (farm.money > 500.0),
        # Land only once there is income to justify it: the median winning seat buys its first
        # quadrant on day 10, and the seat that bought three from turn 1 banked $9,443.
        buy_land=(day >= LAND_DAY) & (farm.money > LAND_MIN_MONEY),
    )
