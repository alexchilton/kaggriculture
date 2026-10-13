"""A mixed farm in one priority cascade: crops, herd, fertiliser and a liquidation glide.

> **BROKEN -- DO NOT USE AS AN OPPONENT YET. Banks $380 against `jax_heuristic`'s $30,292.**
> Traced, not guessed: it buys its 4 starter animals, they sit in the shed, and `max empty pens`
> over 240 turns is **0** -- it never successfully builds a pen. So `n_pen > 0` is never true, the
> animals can never be picked up or placed, and ~$1,400 of livestock is dead capital while the crop
> economy starves. `BUILD_PASTURE` is committed at 0.12% of actions and yields nothing, so either it
> is illegal from the state it is committed in or it has a cost that is not being checked. That is
> the next thing to fix. It is deliberately NOT registered as a role in `train_jax_rl.py`.
>
> Two bugs already found and fixed on the way, both worth keeping in mind for the next pass:
> a flat (unstaged) herd target made it spend the whole opening stake on livestock by day 3, and a
> unit that picked an animal up had no route to a pen, so PICKUP hit **70.5%** of all actions with
> 100% of them being `ANIMAL_ITEM[0]`.


**Why a single agent and not a composition.** `jax_homestead` split one crew between `jax_heuristic`
and `jax_rancher` and lost to the crop parent ($24,957 against $30,292, 0/48). Both parents allocate
jobs with `rank = arange(MAX_UNITS)`, assuming they own every hand, so any index split leaves the
nearest jobs of one arm unserved -- and the "fix" of rolling each arm's units to index 0 was worse
still ($16,422), because the crew is rebuilt from one hand every dawn and rolling unit 7 to index 0
made the crop arm plan for units that did not exist. One cascade over all units has no split to get
wrong.

**What it adds over both parents.**

- `COLLECT_FERT` is **free money nobody takes**: no action cost, every animal, every day, measured at
  about **$85** by `romanrozen/strong-statr-baseline-agent-lb-950`. `jax_heuristic` has no animals;
  `jax_rancher` has them and the trained policy runs `fert+` at 0.00%.
- A **liquidation glide path**. Unsold stock scores exactly zero at day 30. The public writeup's rule
  is `floor_q = ceil(have / max(1, days_left - 1))` once `days_left <= 12`, which drains inventory
  without dumping it into a price floor on the last day.
- **Crops and livestock on one board**, which is what the public meta actually runs (8 cows, 5 sheep,
  5 strawberry plots, 12 hands) and what no seat in our pool did.

**Constants are measured here, not imported from the meta.** `scripts/bench_jax_agents.py` shows two
of the three public numbers do *not* transfer to a two-player sandbox:

> **VOID -- the table below was measured with `weed_chance=0`.** That is `J.step`'s default, and with
> weeds off every game in a batch produces the *identical* final bank: 8 games, 8 identical values,
> unchanged across seeds. Each figure here is one deterministic board reported as a median over 48.
> With `--weeds 0.02` the same 8 games span $16,056 to $33,690, and `farm` beats `ranch` 76% rather
> than 100%. Re-measure before acting on any of it.

| | public meta | measured here |
|---|---|---|
| hands | 12 | no effect 8-14; `jax_heuristic` sizes its own crew from job count, so the cap never binds |
| melon tiles | 10 | **more is better** -- 20 tiles banked $40,308 against 16 tiles' $30,292 |
| herd | 15 | **transfers** -- 15 banked $28,543 against 11's $23,972 |

Melon inverts because the price crash the meta describes needs a crowded leaderboard all dumping on
day 10; with two farms the town drains faster than they can supply. That is a real difference between
our training sandbox and the ladder, and it is worth remembering before importing any other number.

**Not a submission.** `CLAUDE.md`: a heuristic is a teacher and a sparring partner, never the final
policy. This exists to be played against.
"""

import jax
import jax.numpy as jnp

from kagg.rl.jax_heuristic import _nth_nearest, _step_toward
from kagg.sim import jax_sim as J
from kagg.sim import ops as O
from kagg.sim.tiles import CROP_INDEX, EMPTY, FIRST_YIELD_DAY, PLANT

MELON = CROP_INDEX["MELON"]
_FIRST_YIELD = jnp.asarray(FIRST_YIELD_DAY)
COOP, PASTURE, NO_ANIMAL = J.COOP, J.PASTURE, J.NO_ANIMAL
SHEEP, COW = 2, 1

# Measured, not assumed -- see the table above.
MELON_TILES = 20

# **The herd is staged, and that is not decoration.** A flat target made this agent bank $395: with
# `room > 0` true from turn 0, it bought an animal every turn until its money hit the floor, spent
# the whole $3,000 stake on livestock in the first few turns, and then had nothing left for melon
# seed -- so the crop economy that earns $30k never started. `beicicc/c04` stages
# `CORE_HERD 4 -> MID_HERD 8 (day 7) -> TARGET_HERD 15 (day 11)` for exactly this reason, and pairs
# it with a cash reserve. Staging is what lets the two economies be funded in sequence rather than
# competing for the opening stake.
CORE_HERD, MID_HERD, TARGET_ANIMALS = 4, 8, 16
HERD_MID_DAY, HERD_FULL_DAY = 7, 11
# Never spend the last of the bank on an animal: seed, feed and hires all have to stay affordable.
CASH_RESERVE = 1_200.0
CARRY_BEFORE_DROP = 6
SELL_MIN = 3
LAST_PLANT_DAY = 16
LAST_ANIMAL_DAY = 11          # a herd bought later cannot reach its first yield in time
WHEAT_PER_ANIMAL = 4
CARRY_WHEAT = 2

# Unsold stock scores zero at day 30, so start draining inventory with twelve days left and spread it
# rather than dumping on the final day into a floored price.
LIQUIDATE_FROM_DAY = 18
SEASON_DAYS = 30


def actions(state):
    """A `jax_sim.Actions` for both seats; seat selection decides who uses it."""
    t, farm = state.tiles, state.farm
    b = farm.money.shape[0]
    day = (state.step_index // J.TURNS_PER_DAY)[:, None]                  # [B, 1]

    # ---- board ---------------------------------------------------------------------------------
    is_plant = t.kind == PLANT
    age = day[..., None] - t.planted_day
    ripe = is_plant & (age >= _FIRST_YIELD[jnp.maximum(t.crop, 0)]) & (t.yield_units > 0)
    dry = is_plant & ~t.watered_today
    free = t.kind == EMPTY

    has_animal = t.animal != NO_ANIMAL
    animal_ripe = has_animal & (t.yield_units > 0)
    needs_feed = has_animal & ~t.fed_today
    needs_care = has_animal & ~t.cared_today
    has_fert = has_animal & t.fertilizer_available
    empty_pen = ((t.kind == COOP) | (t.kind == PASTURE)) & ~has_animal

    n_animals = has_animal.sum(axis=-1)                                   # [B, P]
    n_pen = empty_pen.sum(axis=-1)
    n_melon = is_plant.sum(axis=-1)

    # ---- units ---------------------------------------------------------------------------------
    pos = farm.unit_pos
    live = jnp.arange(J.MAX_UNITS)[None, None, :] < farm.n_units[..., None]
    flat = pos[..., 1] * J.BOARD + pos[..., 0]
    on_shed = (flat[..., None] == J.SHED_TILES).any(axis=-1)
    carried = farm.carried
    carrying = carried.sum(axis=-1)
    held_wheat = carried[..., O.WHEAT_ITEM]
    held_animal = carried[..., J.ANIMAL_ITEM].sum(axis=-1)
    seeds_left = farm.seeds[..., MELON]
    shed_wheat = farm.shed[..., O.WHEAT_ITEM]
    shed_animal = farm.shed[..., J.ANIMAL_ITEM].sum(axis=-1)

    def under(field):
        return jnp.take_along_axis(field[:, :, None, :].repeat(J.MAX_UNITS, axis=2),
                                   flat[..., None], axis=-1)[..., 0]

    here_ripe, here_dry, here_free = under(ripe), under(dry), under(free)
    here_fert, here_feed, here_care = under(has_fert), under(needs_feed), under(needs_care)
    here_apick, here_pen = under(animal_ripe), under(empty_pen)

    op = jnp.full(flat.shape, O.NOOP, dtype=jnp.int32)
    crop = jnp.zeros_like(op)
    item = jnp.zeros_like(op)
    taken = jnp.zeros(flat.shape, dtype=bool)

    def commit(mask, new_op, new_crop=None, new_item=None):
        nonlocal op, crop, item, taken
        do = mask & ~taken & live
        op = jnp.where(do, new_op, op)
        if new_crop is not None:
            crop = jnp.where(do, new_crop, crop)
        if new_item is not None:
            item = jnp.where(do, new_item, item)
        taken = taken | do

    # ---- the cascade, ordered by what is lost if it is skipped ----------------------------------
    # FEED first because an animal unfed twice escapes with its whole $300-$500 purchase price, which
    # is a certain loss; a crop merely waits. COLLECT_FERT is next because it is free and daily.
    commit(here_feed & (held_wheat > 0), O.FEED)
    commit(here_fert, O.COLLECT_FERT)
    commit(here_care, O.CARE)
    commit(here_apick, O.HARVEST)
    commit(here_ripe & (carrying < 12), O.HARVEST)
    commit(here_dry, O.WATER)
    commit(here_pen & (held_animal > 0), O.PLACE)
    commit(here_free & (seeds_left[..., None] > 0) & (day[..., None] <= LAST_PLANT_DAY)
           & (n_melon[..., None] < MELON_TILES), O.PLANT_OP, MELON)
    # Build a pen when the herd has somewhere to go but nowhere to stand. Free, and one action.
    commit(here_free & ((n_animals + shed_animal)[..., None] > n_pen[..., None])
           & (n_pen[..., None] < TARGET_ANIMALS), O.BUILD_PASTURE)

    # ---- shed trips -----------------------------------------------------------------------------
    # `[B, P, U]`: `shed_wheat` and the feed count are per farm, `held_wheat` is per unit, so the
    # farm-level terms need the unit axis added before they meet it.
    want_wheat = ((shed_wheat > 0) & (needs_feed.sum(axis=-1) > 0))[..., None] & (held_wheat == 0)
    commit(on_shed & want_wheat, O.PICKUP, new_item=O.WHEAT_ITEM)
    # **`held_animal == 0` is load-bearing.** Without it a unit at the shed picks an animal up,
    # has nowhere to take it, and picks up again next turn: measured, PICKUP was **70.5%** of all
    # actions and 100% of them were `ANIMAL_ITEM[0]`, while the board never held a single animal.
    commit(on_shed & (shed_animal > 0)[..., None] & (n_pen > 0)[..., None] & (held_animal == 0),
           O.PICKUP, new_item=J.ANIMAL_ITEM[0])
    commit(on_shed & (carrying >= CARRY_BEFORE_DROP) & (held_animal == 0), O.DROP)

    # ---- routing: each unit walks to its rank-th nearest job -------------------------------------
    rank = jnp.arange(J.MAX_UNITS)

    def route(candidate):
        idx = jax.vmap(lambda r: _nth_nearest(pos[:, :, 0], candidate, r), out_axes=-1)(rank)
        tgt = jnp.stack([idx % J.BOARD, idx // J.BOARD], axis=-1)
        return idx, _step_toward(pos, tgt)

    shed_xy = jnp.stack([J.SHED_TILES % J.BOARD, J.SHED_TILES // J.BOARD], axis=-1)
    d_shed = jnp.abs(shed_xy[None, None, None, :, 0] - pos[..., 0:1]) + \
        jnp.abs(shed_xy[None, None, None, :, 1] - pos[..., 1:2])
    nearest_shed = shed_xy[jnp.argmin(d_shed, axis=-1)]
    commit(carrying >= CARRY_BEFORE_DROP, _step_toward(pos, nearest_shed))
    commit(want_wheat | ((shed_animal > 0) & (n_pen > 0))[..., None],
           _step_toward(pos, nearest_shed))

    # A unit holding an animal walks it to a pen before doing anything else -- the missing route
    # that caused the pickup loop. Placing frees the hand and starts the animal's yield clock.
    pen_idx, pen_step = route(empty_pen)
    commit((held_animal > 0) & (pen_idx >= 0), pen_step)

    for candidate in (needs_feed, has_fert, animal_ripe, ripe, dry, needs_care):
        idx, step = route(candidate)
        commit(idx >= 0, step)
    idx, step = route(free)
    commit((idx >= 0) & (seeds_left[..., None] > 0), step)

    jobs = (dry.sum(axis=-1) + ripe.sum(axis=-1) + needs_feed.sum(axis=-1)
            + has_fert.sum(axis=-1) + animal_ripe.sum(axis=-1))

    # ---- market ----------------------------------------------------------------------------------
    days_left = jnp.maximum(SEASON_DAYS - day, 1)
    have = farm.shed[..., :J.N_PRODUCTS]
    # Normal rule: sell anything above a small holdback. Glide: from LIQUIDATE_FROM_DAY, force out at
    # least an even share per remaining day so nothing is left scoring zero at the bell.
    floor_q = jnp.ceil(have / jnp.maximum(days_left - 1, 1)[..., None]).astype(J._I)
    liquidating = (day >= LIQUIDATE_FROM_DAY)[..., None]
    sell = jnp.where(liquidating, jnp.maximum(floor_q, jnp.where(have >= SELL_MIN, have, 0)),
                     jnp.where(have >= SELL_MIN, have, 0)).astype(J._I)

    seed_short = (n_melon + seeds_left) < MELON_TILES
    buy_seed = jnp.zeros((b, 2, J.N_CROPS), dtype=J._I)
    buy_seed = buy_seed.at[..., MELON].set(
        (seed_short & (day[:, 0:1] <= LAST_PLANT_DAY) & (farm.money > 400.0)).astype(J._I))

    wheat_want = WHEAT_PER_ANIMAL * n_animals
    buy_product = jnp.zeros((b, 2, J.N_PRODUCTS), dtype=J._I)
    buy_product = buy_product.at[..., O.WHEAT_ITEM].set(
        jnp.where((shed_wheat < wheat_want) & (farm.money > 300.0), CARRY_WHEAT, 0).astype(J._I))

    # Staged: a small starter herd, expanded only once the crop economy is paying for it.
    stage = jnp.where(day >= HERD_FULL_DAY, TARGET_ANIMALS,
                      jnp.where(day >= HERD_MID_DAY, MID_HERD, CORE_HERD))
    room = stage - (n_animals + shed_animal)
    can_buy = (day <= LAST_ANIMAL_DAY) & (room > 0) & (farm.money > CASH_RESERVE)
    buy_animal = jnp.zeros((b, 2, J.N_ANIMALS), dtype=J._I)
    take_sheep = can_buy & ((n_animals + shed_animal) % 2 == 0)
    buy_animal = buy_animal.at[..., SHEEP].set(take_sheep.astype(J._I))
    buy_animal = buy_animal.at[..., COW].set((can_buy & ~take_sheep).astype(J._I))

    return J.Actions(
        unit_op=jnp.where(live, op, O.NOOP).astype(J._I),
        unit_crop=crop.astype(J._I),
        unit_item=item.astype(J._I),
        unit_qty=jnp.where((op == O.PICKUP) & (item == O.WHEAT_ITEM), CARRY_WHEAT, 1).astype(J._I),
        sell=sell,
        buy_seed=buy_seed,
        buy_product=buy_product,
        buy_animal=buy_animal,
        # Crew scales with outstanding work, as `jax_heuristic` does -- a fixed target never binds
        # because the field generates the jobs that justify the hands.
        hire=(farm.n_units < jnp.minimum(J.MAX_UNITS, 1 + jobs // 2)) & (farm.money > 500.0),
        buy_land=(day >= 4) & (farm.money > 2500.0),
    )
