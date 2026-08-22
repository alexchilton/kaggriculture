"""Legality masks for every action head.

`CLAUDE.md` draws the line this module has to respect: **masking illegal ops is a legality fact and
is blessed; masking to force a good action is a quality judgment and is what capped Orbit Wars.**
So everything here answers "would the reference environment silently no-op this?", and nothing here
answers "is this a good idea?".

Two consequences that look like bugs and are not:

- **NOOP is always legal.** Never mask it. Masking the no-op to force the policy to act is the
  exact mistake the post-mortem names, and it is how a policy learns to thrash instead of wait.
- **A masked-out op is one the environment would have ignored anyway**, so masking costs nothing in
  expressiveness. It only removes gradient spent on actions that provably do nothing, which is the
  scarce resource over a 720-step episode.

The market masks are affordability and stock, which are facts too: the reference refuses a buy the
bank cannot cover and a sale the shed cannot supply, and abandons the rest of that order when it
does.
"""

import jax.numpy as jnp

from kagg.rl import commit
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

# The primitive ops this file builds masks for. The commit tokens are appended by `unit_op_mask`
# from `commit.commit_mask`; `N_OPS` deliberately still means "the simulator's ops" here.
N_OPS = O.N_OPS


def unit_op_mask(state):
    """[B, P, MAX_UNITS, N_OPS] bool: which ops would actually do something for each unit.

    Evaluated on the tile the unit is standing on *now*, before anything this turn has moved.
    """
    t, farm = state.tiles, state.farm
    # `[B]`, per game -- every value gathered below is `[B, P, U]`, so it needs two trailing axes.
    day = (state.step_index // J.TURNS_PER_DAY)[:, None, None]

    pos = farm.unit_pos                                    # [B, P, U, 2]
    x, y = pos[..., 0], pos[..., 1]
    idx = y * J.BOARD + x

    def g(field):
        return jnp.take_along_axis(field[:, :, None, :], idx[..., None], axis=-1)[..., 0]

    kind = g(t.kind)
    crop = g(t.crop)
    animal = g(t.animal)
    units_held = g(t.yield_units)
    watered = g(t.watered_today)
    planted = g(t.planted_day)
    fed = g(t.fed_today)
    cared = g(t.cared_today)
    fert_ok = g(t.fertilizer_available)

    has_animal = animal != J.NO_ANIMAL
    is_plant = kind == J.PLANT
    empty_structure = ((kind == J.COOP) | (kind == J.PASTURE)) & ~has_animal
    # **Standing position only. A LOCKED shed-access tile still reaches the shed.**
    #
    # This used to also require `kind != J.LOCKED`. The reference does not, and says why
    # (`reference/kaggriculture.py:337-340`):
    #
    #     # Shed operations resolve before the LOCKED guard. They use the tile only as
    #     # a standing position -- the shed itself is always owned -- and three of the
    #     # four shed-access tiles start LOCKED, so guarding them first would make the
    #     # shed unreachable from those tiles.
    #
    # `_apply_unit_action` handles DROP, PICKUP and PLACE above `if tile == "LOCKED": return`, and
    # each tests `_is_shed_adjacent` and nothing else about the tile. `jax_sim.py:683` already
    # agreed; only this mask did not, and the parity gate compares the simulators, never the mask.
    # Same defect and same three tiles as the movement one above.
    # `tests/test_a_hand_can_use_the_shed_from_a_locked_tile.py`.
    on_shed = (idx[..., None] == J.SHED_TILES).any(axis=-1)

    carried = farm.carried                                  # [B, P, U, N_ITEMS]
    carrying_any = carried.sum(axis=-1) > 0
    carrying_wheat = carried[..., J.WHEAT_ITEM] > 0
    carrying_fert = carried[..., J.FERT_ITEM] > 0
    shed_any = (farm.shed.sum(axis=-1) > 0)[:, :, None]
    seeds_any = (farm.seeds.sum(axis=-1) > 0)[:, :, None]

    # **Movement is bounds-only. A LOCKED destination is legal.**
    #
    # This used to also require `t.kind[target] != J.LOCKED`, which the reference does not
    # (`reference/kaggriculture.py:326-331`), and the reference says why in a comment written for
    # exactly this case:
    #
    #     # Movement onto LOCKED tiles is allowed: a hand can spawn on a locked
    #     # shed-access tile, and blocking movement would strand it there forever.
    #     # Tile operations (PLANT, WATER, etc.) still no-op on LOCKED tiles.
    #
    # The NW quadrant is `x < 5, y < 5`, so three of the four shed-access tiles -- (5,4), (4,5),
    # (5,5) -- are LOCKED on day 0, and hands spawn on them. For the hand at (5,5) every neighbour
    # is LOCKED, so the old rule stranded it for the entire season.
    #
    # Measured cost, tape 92498144 turn 1: the teacher's label for that hand is WEST, and the mask
    # made it unemittable. `greedy_action` argmaxes over `_masked_logits`, so WEST carried -1e9;
    # `bc_dagger.py:226` zeroes the loss on labels the mask calls illegal, so it never reached the
    # gradient either. The checkpoint read 162 of 163 ops exact with `WEST 24/25 = 0.960`, frozen
    # for ten rounds in a four-game run and sixteen in a single-game run -- and that one stranded
    # hand dragged whole-season op agreement to ~0.78 once the net drove.
    #
    # This is the class of defect the 300-episode parity gate cannot catch: it tests `game.py` and
    # `jax_sim.py` against the reference, and the masks are RL-side only.
    # `tests/test_a_hand_can_walk_off_the_tile_it_spawned_on.py`.
    def can_move(dx, dy):
        nx, ny = x + dx, y + dy
        return (nx >= 0) & (nx < J.BOARD) & (ny >= 0) & (ny < J.BOARD)

    crop_safe = jnp.clip(crop, 0, J.N_CROPS - 1)
    ripe_plant = is_plant & (units_held > 0) & ((day - planted) >= J.FIRST_YIELD_DAY[crop_safe])

    masks = [None] * N_OPS
    masks[O.NOOP] = jnp.ones_like(has_animal)               # never mask the no-op
    masks[O.NORTH] = can_move(0, -1)
    masks[O.SOUTH] = can_move(0, 1)
    masks[O.EAST] = can_move(1, 0)
    masks[O.WEST] = can_move(-1, 0)
    masks[O.WATER] = is_plant & ~watered
    masks[O.HARVEST] = ripe_plant | (has_animal & (units_held > 0))
    masks[O.PLANT_OP] = (kind == J.EMPTY) & seeds_any
    masks[O.DIG] = (kind == J.WEED) | is_plant | empty_structure
    masks[O.PICKUP] = on_shed & shed_any
    masks[O.DROP] = on_shed & carrying_any
    # PLACE is legal either as an animal placement or as a partial drop by the shed.
    masks[O.PLACE] = (on_shed & carrying_any) | (empty_structure & carrying_any)
    masks[O.FEED] = has_animal & ~fed & carrying_wheat
    masks[O.CARE] = has_animal & ~cared
    masks[O.COLLECT_FERT] = has_animal & fert_ok
    masks[O.FERTILIZE] = is_plant & carrying_fert
    masks[O.BUILD_COOP] = kind == J.EMPTY
    masks[O.BUILD_PASTURE] = kind == J.EMPTY

    live = J._ARANGE_UNITS[None, None, :] < farm.n_units[:, :, None]
    # **The commit tokens are appended, and they are legality just as the primitives are.**
    # `commit_mask` says a target of that kind exists somewhere reachable -- not that walking to it
    # is worth doing. A unit may always decline; nothing here forces a commitment.
    stacked = jnp.concatenate([jnp.stack(masks, axis=-1), commit.commit_mask(state)], axis=-1)
    # A dead slot may only NOOP, so its distribution is a point mass and contributes no gradient.
    only_noop = (jnp.arange(commit.N_POLICY_OPS) == O.NOOP)
    return jnp.where(live[..., None], stacked, only_noop)


def unit_crop_mask(state):
    """[B, P, MAX_UNITS, N_CROPS]: crops the farm actually holds a seed for."""
    have = state.farm.seeds > 0                                  # [B, P, N_CROPS]
    have = jnp.broadcast_to(have[:, :, None, :], (*state.farm.unit_pos.shape[:3], J.N_CROPS))
    # If nothing is held the PLANT op is already masked out; keep a valid distribution anyway.
    return jnp.where(have.any(axis=-1, keepdims=True), have, jnp.ones_like(have))


def unit_item_mask(state):
    """[B, P, MAX_UNITS, N_ITEMS]: items worth naming for PICKUP or PLACE.

    A PICKUP names something in the shed; a PLACE names something the unit is carrying. The union
    keeps one head serving both ops, and an item in neither place would be a silent no-op.
    """
    carried = state.farm.carried > 0                              # [B, P, U, N_ITEMS]
    in_shed = (state.farm.shed > 0)[:, :, None, :]
    usable = carried | jnp.broadcast_to(in_shed, carried.shape)
    return jnp.where(usable.any(axis=-1, keepdims=True), usable, jnp.ones_like(usable))


def market_masks(state, sell_buckets, buy_buckets):
    """Masks for the market heads: what the shed can supply and the bank can cover.

    `sell_buckets` and `buy_buckets` are the quantity ladders the policy chooses from. A bucket is
    legal when the farm could actually fill it; the reference abandons the remainder of an order
    the moment one unit fails, so offering more than is held throws the rest of the order away.
    """
    farm = state.farm
    shed = farm.shed[..., : J.N_PRODUCTS]                          # [B, P, N_PRODUCTS]
    sell_ok = shed[..., None] >= sell_buckets                      # [B, P, N_PRODUCTS, K]
    sell_ok = sell_ok.at[..., 0].set(True)                         # offering nothing is always legal

    prices = J.price(state.inventory)[:, None, :]                  # [B, 1, N_PRODUCTS]
    afford = (farm.money[..., None] / jnp.maximum(prices, 1.0))[..., None] >= buy_buckets
    buy_ok = afford & J.BUYABLE[None, None, :, None]
    buy_ok = buy_ok.at[..., 0].set(True)

    seed_cost = J.SEED_COST[None, None, :, None]
    seed_ok = (farm.money[..., None, None] / seed_cost) >= buy_buckets[None, None, None, :]
    seed_ok = seed_ok.at[..., 0].set(True)

    animal_ok = farm.money[..., None] >= J.ANIMAL_COST[None, None, :]
    hire_ok = farm.money >= J.HIRE_COST[jnp.minimum(farm.hires_today, J.MAX_UNITS)]
    land_ok = (farm.n_land < J.N_LAND) & (
        farm.money >= J.LAND_PRICES[jnp.minimum(farm.n_land, J.N_LAND - 1)])

    return {
        "sell": sell_ok,
        "buy_product": buy_ok,
        "buy_seed": seed_ok,
        "buy_animal": jnp.stack([jnp.ones_like(animal_ok), animal_ok], axis=-1),
        "hire": jnp.stack([jnp.ones_like(hire_ok), hire_ok], axis=-1),
        "buy_land": jnp.stack([jnp.ones_like(land_ok), land_ok], axis=-1),
    }
