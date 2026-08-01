"""Observations for the per-turn policy: `jax_sim.State` -> per-seat entity tokens.

The policy sees the board as **entities, not a picture**: 100 tile tokens, 24 unit tokens and one
global token, all encoded per seat so self-play can drive both sides from one set of parameters.
That shape is deliberate -- it is what worked for every top finisher whose write-up we have, and
`docs/lessons_carried_over.md` records the entity transformer as the transferable win from Orbit
Wars.

Three encoding decisions worth stating, because each one is a choice and not an accident:

- **The opponent's board is a summary, not 100 more tokens.** `contrarian`'s entire edge is reading
  what the opponent grows and switching off a contested crop, so the information has to be present;
  but which *tile* they used never mattered, only the mix. Fourteen aggregate numbers on the global
  token buy that at a fraction of the attention cost of doubling the sequence.
- **Everything is scaled to roughly unit range**, because the raw quantities span money in the tens
  of thousands and a boolean. Divisors are fixed constants rather than running statistics: a
  normaliser that drifts during self-play makes an old checkpoint silently incomparable.
- **Nothing here is a quality judgment.** These are facts about the state. Anything resembling
  "this tile is a good idea" belongs in the policy, not the features -- hand-built priors in the
  observation are how a heuristic's ceiling gets baked in where nobody can see it.
"""

import jax.numpy as jnp

from kagg.sim import jax_sim as J

N_KINDS = 6           # EMPTY, LOCKED, WEED, PLANT, COOP, PASTURE
_XS = jnp.arange(J.BOARD * J.BOARD) % J.BOARD
_YS = jnp.arange(J.BOARD * J.BOARD) // J.BOARD
N_CROPS = J.N_CROPS
N_ANIMAL_KINDS = len(J.ANIMAL_STRUCTURE)

TILE_FEATURES = N_KINDS + N_CROPS + N_ANIMAL_KINDS + 11      # 25
UNIT_FEATURES = 4 + J.N_ITEMS                                # 16
GLOBAL_FEATURES = 3 + 2 + J.N_PRODUCTS * 2 + N_CROPS + J.N_ITEMS + 3 + 14   # 57

# Fixed scales. Chosen from measured ranges, and frozen so checkpoints stay comparable.
MONEY_SCALE = 50_000.0
PRICE_SCALE = 250.0
INVENTORY_SCALE = 500.0


def _one_hot(x, n):
    return (x[..., None] == jnp.arange(n)).astype(jnp.float32)


def encode(state):
    """Return `(tiles, units, glob)` for both seats.

    Shapes are `[B, P, TILES, TILE_FEATURES]`, `[B, P, MAX_UNITS, UNIT_FEATURES]` and
    `[B, P, GLOBAL_FEATURES]`. Seat `p` sees its own farm in full and the other seat in aggregate.
    """
    t, farm = state.tiles, state.farm
    # `[B]`, not a scalar: `jax_sim` keeps `step_index` per game so episodes can run out of phase.
    day = (state.step_index // J.TURNS_PER_DAY).astype(jnp.float32)        # [B]
    hour = (state.step_index % J.TURNS_PER_DAY).astype(jnp.float32)        # [B]
    day_t = day[:, None, None]                                             # against [B, P, TILES]
    day_g = day[:, None]                                                   # against [B, P]

    # ---- tiles ---------------------------------------------------------------------------------
    is_plant = t.kind == J.PLANT
    has_animal = t.animal != J.NO_ANIMAL
    tiles = jnp.concatenate(
        [
            _one_hot(t.kind, N_KINDS),
            _one_hot(jnp.where(is_plant, t.crop, -1), N_CROPS),
            _one_hot(jnp.where(has_animal, t.animal, -1), N_ANIMAL_KINDS),
            (t.yield_units / 8.0).astype(jnp.float32)[..., None],
            t.watered_today.astype(jnp.float32)[..., None],
            (t.consecutive_unwatered / 2.0).astype(jnp.float32)[..., None],
            # Age drives every yield rule, so give it directly rather than making the net subtract.
            jnp.where(is_plant, (day_t - t.planted_day) / 30.0, 0.0)
            .astype(jnp.float32)[..., None],
            (t.fertilized_until_day >= day_t).astype(jnp.float32)[..., None],
            t.fed_today.astype(jnp.float32)[..., None],
            t.cared_today.astype(jnp.float32)[..., None],
            t.fertilizer_available.astype(jnp.float32)[..., None],
            (t.pending_care_bonus / 4.0).astype(jnp.float32)[..., None],
            (t.consecutive_unfed / 2.0).astype(jnp.float32)[..., None],
            # An animal two days unfed escapes tonight; that cliff is worth its own feature.
            (has_animal & (t.consecutive_unfed >= 1)).astype(jnp.float32)[..., None],
        ],
        axis=-1,
    )

    # ---- units ---------------------------------------------------------------------------------
    live = J._ARANGE_UNITS[None, None, :] < farm.n_units[:, :, None]
    pos = farm.unit_pos
    flat = pos[..., 1] * J.BOARD + pos[..., 0]
    on_shed = (flat[..., None] == J.SHED_TILES).any(axis=-1)

    # **Where the nearest job is, given rather than derived.**
    #
    # This file already takes that position elsewhere -- "Age drives every yield rule, so give it
    # directly rather than making the net subtract" -- and it is the move Ender's whole
    # target-selection pipeline is built on: precompute the intercept geometry and hand it to the
    # policy rather than making a transformer learn orbital mechanics from raw positions through
    # reward alone. Ours is the trivial version of the same problem, Manhattan distance on a static
    # 10x10 grid.
    #
    # Measured motivation: over 412,992 owned-unit actions the policy placed 4,591 animals and fed
    # 12, and planted 13,439 crops and harvested 98. Setup actions -- one-shot, on the tile the unit
    # already occupies -- are common; maintenance actions, which require *returning to the same tile
    # on a later day*, are three orders of magnitude rarer. Every unit is reset to spawn each night,
    # so every return is a fresh multi-step walk whose payoff arrives days later, and the chance of
    # sampling one correctly decays exponentially with its length. With 98 successes in 413k actions
    # there is essentially no completed trajectory for the critic to learn from.
    #
    # This is a fact, not a quality judgment: it says where the nearest dry plant is, not that
    # watering is what the unit ought to do. `CLAUDE.md` draws the line at masking to *force* an
    # action, which this does not do -- a unit is free to ignore it, as it is free to ignore `age`.
    def _target(candidate):
        """Signed direction and distance to the nearest tile satisfying `candidate`. [B, P, U, 3]"""
        dx = _XS[None, None, None, :] - pos[..., 0:1]
        dy = _YS[None, None, None, :] - pos[..., 1:2]
        dist = jnp.abs(dx) + jnp.abs(dy)
        masked = jnp.where(candidate[:, :, None, :], dist, 999)
        nearest = jnp.argmin(masked, axis=-1)[..., None]
        found = jnp.take_along_axis(masked, nearest, axis=-1) < 999
        take = lambda a: jnp.take_along_axis(a, nearest, axis=-1)   # noqa: E731
        return jnp.concatenate([
            jnp.where(found, take(dx) / (J.BOARD - 1.0), 0.0),
            jnp.where(found, take(dy) / (J.BOARD - 1.0), 0.0),
            # Distance is inverted so "nothing to do" and "very far" are both near zero, and a job
            # underfoot is 1. A raw distance would make the absent case indistinguishable from a
            # nearby one only by the sign of a separate flag.
            jnp.where(found, 1.0 / (1.0 + take(masked).astype(jnp.float32)), 0.0),
        ], axis=-1).astype(jnp.float32)

    is_plant_t = t.kind == J.PLANT
    needs_water = is_plant_t & ~t.watered_today
    has_animal_t = t.animal != J.NO_ANIMAL

    # **Mirror `jax_masks.HARVEST` exactly, or this points units at jobs they cannot do and hides
    # jobs they can.** The mask is `ripe_plant | (has_animal & units_held > 0)`, and this target
    # was only the crop half of it -- so a unit got a directional pull toward a ripe melon and
    # none at all toward a goose with eggs waiting. FEED has never once fired in 90 updates and
    # animal-product harvest sits with it; giving the crop economy geometry the animal economy
    # does not have would keep it that way by construction.
    #
    # The crop half also dropped the mask's `FIRST_YIELD_DAY` condition, which made it *broader*
    # than legality: it pointed at seedlings carrying yield they are not yet old enough to take.
    # A target that says "go here" for an illegal op is worse than no target -- it spends the walk
    # and then masks the payoff.
    crop_safe_t = jnp.clip(t.crop, 0, N_CROPS - 1)
    ripe_crop = (is_plant_t & (t.yield_units > 0)
                 & ((day_t - t.planted_day) >= J.FIRST_YIELD_DAY[crop_safe_t]))
    is_ripe = ripe_crop | (has_animal_t & (t.yield_units > 0))
    needs_feed = has_animal_t & ~t.fed_today

    units = jnp.concatenate(
        [
            live.astype(jnp.float32)[..., None],
            (pos[..., 0] / (J.BOARD - 1.0)).astype(jnp.float32)[..., None],
            (pos[..., 1] / (J.BOARD - 1.0)).astype(jnp.float32)[..., None],
            on_shed.astype(jnp.float32)[..., None],
            jnp.minimum(farm.carried / 10.0, 3.0).astype(jnp.float32),
            _target(needs_water),
            _target(is_ripe),
            _target(needs_feed),
            _target(t.kind == J.EMPTY),
        ],
        axis=-1,
    )

    # ---- opponent summary ----------------------------------------------------------------------
    # Seat 0's opponent is seat 1 and vice versa, so a reversal along the player axis gives each
    # seat the other's aggregate without materialising two separate encodings.
    kind_counts = jnp.stack(
        [(t.kind == k).sum(axis=-1) for k in range(N_KINDS)], axis=-1) / 100.0
    crop_counts = jnp.stack(
        [((t.kind == J.PLANT) & (t.crop == c)).sum(axis=-1) for c in range(N_CROPS)],
        axis=-1) / 100.0
    animal_counts = jnp.stack(
        [(t.animal == a).sum(axis=-1) for a in range(N_ANIMAL_KINDS)], axis=-1) / 20.0
    board_summary = jnp.concatenate(
        [kind_counts, crop_counts, animal_counts], axis=-1).astype(jnp.float32)
    opponent = board_summary[:, ::-1]
    opp_money = farm.money[:, ::-1]

    # ---- global --------------------------------------------------------------------------------
    prices = (J.price(state.inventory) / PRICE_SCALE).astype(jnp.float32)
    inventory = ((state.inventory - J.INV0) / INVENTORY_SCALE).astype(jnp.float32)
    b = farm.money.shape[0]

    # **What the next purchase costs, as a share of everything the farm has.**
    #
    # `money`, `n_land` and `hires_today` are all present, but no price is. The policy therefore has
    # to learn the lookups `n_land -> {1000, 2000, 4000}` and `hires_today -> mult * fib(n)` through
    # reward alone, and the reward is terminal -- 700 turns after the purchase.
    #
    # Measured motivation: `LAND_PRICES[0] + LAND_PRICES[1]` is exactly $3,000, the opening bank, and
    # both purchases are affordability-legal. A policy that buys two quadrants on day 0 is broke for
    # the remaining twenty-five days, which is precisely what the update-250 replay does -- $3,000 to
    # $0 by day 5, then nothing. Across 312 real seats the median first land purchase is turn 242
    # (day 10) and the top decile buys 1.59 quadrants; the seat that bought three from turn 1 banked
    # $9,443 against the leaders' $130k. So the quadrant is not a bad buy, it is a bad buy *now*, and
    # "now" is a function of the price against the bank.
    #
    # The ratio is the fact the mask already computes and then throws away: `land_ok` tests
    # `money >= LAND_PRICES[n_land]` and exposes only the boolean, so "costs a third of everything"
    # and "costs 3%" are indistinguishable to the policy. This says what it costs, not whether to
    # buy -- the same side of `CLAUDE.md`'s line as `age` and the nearest-job geometry.
    safe_money = jnp.maximum(farm.money, 1.0)
    next_land = J.LAND_PRICES[jnp.minimum(farm.n_land, J.N_LAND - 1)]
    land_afford = jnp.where(farm.n_land < J.N_LAND,
                            jnp.minimum(next_land / safe_money, 4.0), 0.0)
    next_hire = J.HIRE_COST[jnp.minimum(farm.hires_today, J.MAX_UNITS)]
    hire_afford = jnp.minimum(next_hire / safe_money, 4.0)

    glob = jnp.concatenate(
        [
            (farm.money / MONEY_SCALE).astype(jnp.float32)[..., None],
            (opp_money / MONEY_SCALE).astype(jnp.float32)[..., None],
            # The lead is the quantity the terminal reward actually turns on, so state it directly.
            ((farm.money - opp_money) / MONEY_SCALE).astype(jnp.float32)[..., None],
            jnp.broadcast_to((day / 30.0)[:, None], (b, 2))[..., None],
            jnp.broadcast_to((hour / 24.0)[:, None], (b, 2))[..., None],
            jnp.broadcast_to(prices[:, None, :], (b, 2, J.N_PRODUCTS)),
            jnp.broadcast_to(inventory[:, None, :], (b, 2, J.N_PRODUCTS)),
            jnp.minimum(farm.seeds / 10.0, 5.0).astype(jnp.float32),
            jnp.minimum(farm.shed / 50.0, 3.0).astype(jnp.float32),
            (farm.n_units / 24.0).astype(jnp.float32)[..., None],
            (farm.n_land / 3.0).astype(jnp.float32)[..., None],
            (farm.hires_today / 12.0).astype(jnp.float32)[..., None],
            land_afford.astype(jnp.float32)[..., None],
            hire_afford.astype(jnp.float32)[..., None],
            opponent,
        ],
        axis=-1,
    )
    return tiles, units, glob
