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
    day = (state.step_index // J.TURNS_PER_DAY).astype(jnp.float32)
    hour = (state.step_index % J.TURNS_PER_DAY).astype(jnp.float32)

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
            jnp.where(is_plant, (day[None, None, None] - t.planted_day) / 30.0, 0.0)
            .astype(jnp.float32)[..., None],
            (t.fertilized_until_day >= day).astype(jnp.float32)[..., None],
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
    units = jnp.concatenate(
        [
            live.astype(jnp.float32)[..., None],
            (pos[..., 0] / (J.BOARD - 1.0)).astype(jnp.float32)[..., None],
            (pos[..., 1] / (J.BOARD - 1.0)).astype(jnp.float32)[..., None],
            on_shed.astype(jnp.float32)[..., None],
            jnp.minimum(farm.carried / 10.0, 3.0).astype(jnp.float32),
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
    glob = jnp.concatenate(
        [
            (farm.money / MONEY_SCALE).astype(jnp.float32)[..., None],
            (opp_money / MONEY_SCALE).astype(jnp.float32)[..., None],
            # The lead is the quantity the terminal reward actually turns on, so state it directly.
            ((farm.money - opp_money) / MONEY_SCALE).astype(jnp.float32)[..., None],
            jnp.broadcast_to(day / 30.0, (b, 2))[..., None],
            jnp.broadcast_to(hour / 24.0, (b, 2))[..., None],
            jnp.broadcast_to(prices[:, None, :], (b, 2, J.N_PRODUCTS)),
            jnp.broadcast_to(inventory[:, None, :], (b, 2, J.N_PRODUCTS)),
            jnp.minimum(farm.seeds / 10.0, 5.0).astype(jnp.float32),
            jnp.minimum(farm.shed / 50.0, 3.0).astype(jnp.float32),
            (farm.n_units / 24.0).astype(jnp.float32)[..., None],
            (farm.n_land / 3.0).astype(jnp.float32)[..., None],
            (farm.hires_today / 12.0).astype(jnp.float32)[..., None],
            opponent,
        ],
        axis=-1,
    )
    return tiles, units, glob
