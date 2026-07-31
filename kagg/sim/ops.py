"""Batched unit operations: what a farmer or hand does on the tile it stands on.

Every game in the batch applies the *same-indexed* unit's action simultaneously, with each game
free to choose a different op. So the op dispatch becomes one masked update per op rather than a
branch per unit -- nine cheap vector writes instead of B*U Python branches.

Ports of `_apply_unit_action`. The rules that are easy to get wrong, and are therefore tested:

- **Movement is blocked by the board edge and by LOCKED tiles**, and silently does nothing
  otherwise. A no-op move still burns the unit's action for the turn.
- **WATER carries the yield bonus for non-ongoing crops**, but only inside the window
  `(max_yield_day + 1) // 2 <= age <= max_yield_day`, and only once per day.
- **Fertilizer doubles that bonus**, but only on a day the tile is watered -- basic needs first.
- **HARVEST clears the tile for non-ongoing crops** and leaves ongoing ones standing.
- **DIG does not remove a placed animal.** It clears weeds, plants and *empty* structures only, so
  a pasture with a cow in it is permanent for the season.
- **Everything to do with the shed is position-gated** on the four shed-access tiles, and animals
  are ordinary shed items between `BUY_ANIMAL` and `PLACE`.
"""

import numpy as np

from kagg.sim.market import ITEM_INDEX, N_ITEMS
from kagg.sim.tiles import (
    ANIMAL_STRUCTURE,
    BOARD,
    COOP,
    EMPTY,
    LOCKED,
    MAX_YIELD,
    MAX_YIELD_DAY,
    NO_ANIMAL,
    NO_CROP,
    ONGOING,
    PASTURE,
    PLANT,
    WEED,
)

# Op codes. NOOP covers both PASS and any action that turns out to be illegal.
# The first nine are the crop game; the rest are the animal economy and the logistics that feed it.
(
    NOOP, NORTH, SOUTH, EAST, WEST, WATER, HARVEST, PLANT_OP, DIG,
    PICKUP, DROP, PLACE, FEED, CARE, COLLECT_FERT, FERTILIZE, BUILD_COOP, BUILD_PASTURE,
) = range(18)
N_OPS = 18

WHEAT_ITEM = ITEM_INDEX["WHEAT"]
FERT_ITEM = ITEM_INDEX["FERTILIZER"]
SHED_CAP = 100

# (dx, dy) per op, indexed by op code; y grows downward, matching FARMER_MOVES.
_DX = np.zeros(N_OPS, dtype=np.int64)
_DY = np.zeros(N_OPS, dtype=np.int64)
_DX[EAST], _DX[WEST] = 1, -1
_DY[SOUTH], _DY[NORTH] = 1, -1

# The four inner-corner tiles around the shed, as flat indices. `_is_shed_adjacent` gates DROP,
# PICKUP and the shed-drop half of PLACE.
_HALF = BOARD // 2
SHED_TILES = np.array(
    [(_HALF - 1) * BOARD + (_HALF - 1), (_HALF - 1) * BOARD + _HALF,
     _HALF * BOARD + (_HALF - 1), _HALF * BOARD + _HALF],
    dtype=np.int64,
)


def move(state, pos, ops):
    """Apply movement ops. `pos` is [B, 2] as (x, y); returns the new positions.

    A move off the board or onto a LOCKED tile is silently ignored, exactly as the reference does,
    so the unit stays put and loses the turn.
    """
    pos = np.array(pos, dtype=np.int64, copy=True)
    ops = np.asarray(ops)

    nx = pos[:, 0] + _DX[ops]
    ny = pos[:, 1] + _DY[ops]
    in_bounds = (nx >= 0) & (nx < BOARD) & (ny >= 0) & (ny < BOARD)

    # Clip only for the lookup; out-of-bounds games are masked out immediately after.
    target = np.clip(ny, 0, BOARD - 1) * BOARD + np.clip(nx, 0, BOARD - 1)
    unlocked = state.kind[np.arange(state.batch), target] != LOCKED

    is_move = (ops >= NORTH) & (ops <= WEST)
    legal = is_move & in_bounds & unlocked
    pos[:, 0] = np.where(legal, nx, pos[:, 0])
    pos[:, 1] = np.where(legal, ny, pos[:, 1])
    return pos


def _tile_index(pos):
    return pos[:, 1] * BOARD + pos[:, 0]


def water(state, pos, active, day):
    """Apply WATER where `active`. Returns nothing; mutates `state`.

    The non-ongoing yield bonus is the subtle part: it lands only inside the watering window and
    only once per day, and fertilizer doubles it.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)

    kind = state.kind[games, idx]
    already = state.watered_today[games, idx]
    doable = active & (kind == PLANT) & ~already
    if not doable.any():
        return

    state.watered_today[games, idx] = np.where(doable, True, state.watered_today[games, idx])

    crop = np.where(doable, state.crop[games, idx], 0)
    age = day - state.planted_day[games, idx]
    window_start = (MAX_YIELD_DAY[crop] + 1) // 2
    in_window = (age >= window_start) & (age <= MAX_YIELD_DAY[crop])
    gains = doable & ~ONGOING[crop] & in_window

    fertilized = state.fertilized_until_day[games, idx] >= day
    bonus = np.where(fertilized, 2, 1)
    updated = np.minimum(MAX_YIELD[crop], state.yield_units[games, idx] + bonus)
    state.yield_units[games, idx] = np.where(gains, updated, state.yield_units[games, idx])


def harvest(state, pos, active, day, carried):
    """Apply HARVEST where `active`, adding units to `carried` [B, N_CROPS].

    Non-ongoing crops clear the tile; ongoing crops stay and keep producing. Nothing is harvested
    before `first_yield_day`, which is what stops an immature ongoing crop being stripped.
    """
    from kagg.sim.tiles import FIRST_YIELD_DAY

    games = np.arange(state.batch)
    idx = _tile_index(pos)

    kind = state.kind[games, idx]
    units = state.yield_units[games, idx]
    crop = np.where(kind == PLANT, state.crop[games, idx], 0)
    age = day - state.planted_day[games, idx]

    doable = active & (kind == PLANT) & (units > 0) & (age >= FIRST_YIELD_DAY[crop])
    if not doable.any():
        return carried

    np.add.at(carried, (games[doable], crop[doable]), units[doable])
    state.yield_units[games, idx] = np.where(doable, 0, state.yield_units[games, idx])

    # Harvesting a non-ongoing crop takes the plant with it.
    cleared = doable & ~ONGOING[crop]
    state.kind[games, idx] = np.where(cleared, EMPTY, state.kind[games, idx])
    state.crop[games, idx] = np.where(cleared, NO_CROP, state.crop[games, idx])
    state.max_lifespan_step[games, idx] = np.where(cleared, -1, state.max_lifespan_step[games, idx])
    return carried


def dig(state, pos, active):
    """Apply DIG where `active`: clears weeds, plants and *empty* structures.

    A structure with an animal in it is explicitly skipped by the reference, so a stocked pasture
    cannot be dug up and re-used -- the tile is committed for the rest of the season.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)

    kind = state.kind[games, idx]
    empty_structure = ((kind == COOP) | (kind == PASTURE)) & (state.animal[games, idx] == NO_ANIMAL)
    doable = active & ((kind == WEED) | (kind == PLANT) | empty_structure)

    state.kind[games, idx] = np.where(doable, EMPTY, state.kind[games, idx])
    state.crop[games, idx] = np.where(doable, NO_CROP, state.crop[games, idx])
    state.yield_units[games, idx] = np.where(doable, 0, state.yield_units[games, idx])
    state.max_lifespan_step[games, idx] = np.where(doable, -1, state.max_lifespan_step[games, idx])


def plant(state, pos, active, crop_id, day, turns_per_day=24):
    """Apply PLANT where `active`, on empty tiles only.

    Seed availability is the caller's responsibility: the reference validates PLANT atomically per
    crop across all of a player's units, dropping every request for a crop when they exceed the
    seeds held, and that check needs the whole turn's actions at once.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)

    doable = active & (state.kind[games, idx] == EMPTY)
    if not doable.any():
        return doable

    mask = np.zeros_like(state.kind, dtype=bool)
    mask[games[doable], idx[doable]] = True
    state.plant(mask, crop_id, day, turns_per_day)
    # Returned so the caller can spend a seed only where the plant actually landed. Spending it
    # regardless silently starves the farm over a long episode: a PLANT onto an occupied tile is a
    # no-op in the reference and costs nothing, and getting this wrong cost 0/40 on the parity gate
    # while every unit test still passed.
    return doable


# ---- logistics: the shed, and what units carry -------------------------------------------------


def shed_adjacent(pos):
    """[B] bool: is the unit standing on one of the four shed-access tiles?

    `_is_shed_adjacent` gates DROP, PICKUP and PLACE's shed-drop branch. Note it tests the tile the
    unit is *on*, not adjacency to a separate shed tile -- the shed is the 2x2 block's centre and
    these four tiles are its access points.
    """
    return np.isin(_tile_index(pos), SHED_TILES)


def drop(pos, active, carried_u, shed):
    """DROP: empty this unit's whole inventory into the shed, under the 100-item cap.

    Overflow is **destroyed, not kept**: the reference deletes the inventory entry whether or not
    the whole stack fitted. Items are walked in a fixed order here rather than insertion order,
    which only differs if the cap binds part-way through one unit's load.
    """
    doable = active & shed_adjacent(pos)
    if not doable.any():
        return
    for item in range(N_ITEMS):
        have = np.where(doable, carried_u[:, item], 0)
        if not have.any():
            continue
        room = np.maximum(0, SHED_CAP - shed.sum(axis=1))
        shed[:, item] += np.minimum(have, room)
        carried_u[:, item] = np.where(doable, 0, carried_u[:, item])


def pickup(pos, active, item, qty, carried_u, shed):
    """PICKUP: take up to `qty` of one item out of the shed and into the unit's inventory.

    Unlike DROP this is not capped -- a unit's own inventory is uncapped during the day. Seeds
    never pass through here; PLANT consumes them straight from the farm's seed store.
    """
    doable = active & shed_adjacent(pos) & (qty > 0)
    if not doable.any():
        return
    games = np.arange(len(item))
    available = shed[games, item]
    take = np.where(doable, np.minimum(qty, available), 0)
    take = np.maximum(take, 0)
    np.add.at(shed, (games, item), -take)
    np.add.at(carried_u, (games, item), take)


def place(state, pos, active, item, qty, carried_u, shed, day):
    """PLACE: put an animal into a matching empty structure, or drop `qty` of an item in the shed.

    The reference tries the animal branch first and **falls through** to the shed drop when it does
    not apply, so PLACE-ing a cow while standing by the shed with no empty pasture underfoot simply
    stores the cow. Both halves are needed; only implementing the animal half loses the partial
    drop that agents use to bank produce without emptying a unit.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)
    kind = state.kind[games, idx]

    # Which animal is this item, if any? Animal items sit above the products in the item vocabulary.
    from kagg.sim.market import N_PRODUCTS

    animal_id = item - N_PRODUCTS
    is_animal = active & (animal_id >= 0) & (animal_id < len(ANIMAL_STRUCTURE))
    safe_animal = np.where(is_animal, animal_id, 0)

    on_match = (
        is_animal
        & (kind == ANIMAL_STRUCTURE[safe_animal])
        & (state.animal[games, idx] == NO_ANIMAL)
        & (carried_u[games, item] > 0)
    )
    if on_match.any():
        np.add.at(carried_u, (games[on_match], item[on_match]), -1)
        state.animal[games, idx] = np.where(on_match, safe_animal, state.animal[games, idx])
        state.placed_day[games, idx] = np.where(on_match, day, state.placed_day[games, idx])
        state.yield_units[games, idx] = np.where(on_match, 0, state.yield_units[games, idx])
        state.consecutive_unfed[games, idx] = np.where(
            on_match, 0, state.consecutive_unfed[games, idx])
        state.fed_today[games, idx] = np.where(on_match, False, state.fed_today[games, idx])
        state.cared_today[games, idx] = np.where(on_match, False, state.cared_today[games, idx])
        state.fertilizer_available[games, idx] = np.where(
            on_match, False, state.fertilizer_available[games, idx])
        state.pending_care_bonus[games, idx] = np.where(
            on_match, 0, state.pending_care_bonus[games, idx])

    # Everything that did not become an animal placement falls through to the shed drop.
    dropping = active & ~on_match & shed_adjacent(pos) & (qty > 0)
    if not dropping.any():
        return
    have = carried_u[games, item]
    room = np.maximum(0, SHED_CAP - shed.sum(axis=1))
    take = np.where(dropping, np.minimum(np.minimum(qty, have), room), 0)
    take = np.maximum(take, 0)
    np.add.at(carried_u, (games, item), -take)
    np.add.at(shed, (games, item), take)


# ---- the animal economy ------------------------------------------------------------------------


def build(state, pos, active, structure):
    """BUILD_COOP / BUILD_PASTURE: raise a structure on an empty tile. Free, and instant."""
    games = np.arange(state.batch)
    idx = _tile_index(pos)
    doable = active & (state.kind[games, idx] == EMPTY)
    if not doable.any():
        return
    state.kind[games, idx] = np.where(doable, structure, state.kind[games, idx])
    state.animal[games, idx] = np.where(doable, NO_ANIMAL, state.animal[games, idx])
    state.yield_units[games, idx] = np.where(doable, 0, state.yield_units[games, idx])


def feed(state, pos, active, carried_u):
    """FEED: one WHEAT out of the unit's own inventory, once per animal per day.

    The wheat must be *carried*, not merely in the shed, which is what makes the buy-wheat ->
    PICKUP -> FEED loop the busiest thing a big herd does.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)
    doable = (
        active
        & (state.animal[games, idx] != NO_ANIMAL)
        & ~state.fed_today[games, idx]
        & (carried_u[:, WHEAT_ITEM] > 0)
    )
    if not doable.any():
        return
    carried_u[:, WHEAT_ITEM] -= doable.astype(np.int64)
    state.fed_today[games, idx] = np.where(doable, True, state.fed_today[games, idx])


def care(state, pos, active):
    """CARE: once per animal per day. Banks a bonus that only pays out on a fed production day."""
    games = np.arange(state.batch)
    idx = _tile_index(pos)
    doable = active & (state.animal[games, idx] != NO_ANIMAL) & ~state.cared_today[games, idx]
    state.cared_today[games, idx] = np.where(doable, True, state.cared_today[games, idx])


def collect_fertilizer(state, pos, active, carried_u):
    """COLLECT_FERTILIZER: one FERTILIZER per animal per day, refreshed every night."""
    games = np.arange(state.batch)
    idx = _tile_index(pos)
    doable = (
        active
        & (state.animal[games, idx] != NO_ANIMAL)
        & state.fertilizer_available[games, idx]
    )
    if not doable.any():
        return
    state.fertilizer_available[games, idx] = np.where(
        doable, False, state.fertilizer_available[games, idx])
    carried_u[:, FERT_ITEM] += doable.astype(np.int64)


def fertilize(state, pos, active, carried_u, day):
    """FERTILIZE: spend one carried FERTILIZER on a plant, doubling its watering bonus.

    Active for `day`, `day+1` and `day+2` inclusive, and it only pays on days the tile is actually
    watered -- basic needs first.
    """
    games = np.arange(state.batch)
    idx = _tile_index(pos)
    doable = (
        active & (state.kind[games, idx] == PLANT) & (carried_u[:, FERT_ITEM] > 0)
    )
    if not doable.any():
        return
    carried_u[:, FERT_ITEM] -= doable.astype(np.int64)
    current = state.fertilized_until_day[games, idx]
    state.fertilized_until_day[games, idx] = np.where(doable, np.maximum(current, day + 2), current)


def harvest_animals(state, pos, active, carried_u):
    """HARVEST on an animal tile: take the held units as the animal's product.

    Shares the HARVEST op with crops -- the reference's HARVEST branches on the tile, not the op --
    so this runs alongside `harvest` rather than instead of it.
    """
    from kagg.sim.tiles import ANIMAL_TO_PRODUCT

    games = np.arange(state.batch)
    idx = _tile_index(pos)
    animal = state.animal[games, idx]
    units = state.yield_units[games, idx]

    doable = active & (animal != NO_ANIMAL) & (units > 0)
    if not doable.any():
        return
    product = ANIMAL_TO_PRODUCT[np.where(doable, animal, 0)]
    np.add.at(carried_u, (games[doable], product[doable]), units[doable])
    state.yield_units[games, idx] = np.where(doable, 0, state.yield_units[games, idx])


def daily_refresh_animals(state, current_day):
    """Port of `_daily_refresh_animals`, run at the end of each day.

    Order is load-bearing and follows the reference exactly:

    1. update the unfed streak;
    2. **two consecutive unfed days and the animal escapes**, leaving the bare structure behind;
    3. produce if today is on the interval from `first_yield_day`, capped at `max_held`;
    4. the care bonus is consumed only on a day that both fed and produced, and a fresh one is
       banked only when the animal was both cared for *and* fed;
    5. fertilizer becomes available again, and the daily flags reset.
    """
    from kagg.sim.tiles import (
        ANIMAL_FIRST_YIELD_DAY,
        ANIMAL_INTERVAL,
        ANIMAL_MAX_HELD,
    )

    next_day = current_day + 1
    has_animal = state.animal != NO_ANIMAL
    if not has_animal.any():
        return state

    fed = state.fed_today & has_animal
    state.consecutive_unfed = np.where(
        has_animal,
        np.where(fed, 0, state.consecutive_unfed + 1),
        state.consecutive_unfed,
    )

    escaped = has_animal & (state.consecutive_unfed >= 2)
    state.animal = np.where(escaped, NO_ANIMAL, state.animal)
    state.yield_units = np.where(escaped, 0, state.yield_units)
    state.pending_care_bonus = np.where(escaped, 0, state.pending_care_bonus)
    state.consecutive_unfed = np.where(escaped, 0, state.consecutive_unfed)

    live = has_animal & ~escaped
    a = np.where(live, state.animal, 0)

    days_since = next_day - state.placed_day - ANIMAL_FIRST_YIELD_DAY[a]
    interval = np.maximum(ANIMAL_INTERVAL[a], 1)
    produces = live & (days_since >= 0) & ((days_since % interval) == 0)

    bonus = np.where(produces & fed, state.pending_care_bonus, 0)
    state.yield_units = np.where(
        produces,
        np.minimum(ANIMAL_MAX_HELD[a], state.yield_units + 1 + bonus),
        state.yield_units,
    )
    state.pending_care_bonus = np.where(produces, 0, state.pending_care_bonus)

    banked = live & state.cared_today & fed
    state.pending_care_bonus = np.where(
        banked, state.pending_care_bonus + 1, state.pending_care_bonus)

    state.fertilizer_available = np.where(live, True, state.fertilizer_available)
    state.fed_today = np.where(live, False, state.fed_today)
    state.cared_today = np.where(live, False, state.cared_today)
    return state
