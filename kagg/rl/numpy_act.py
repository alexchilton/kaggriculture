"""`jax_act` + `jax_masks` + `commit.commit_mask`, in numpy -- the action half of a shippable net.

    from kagg.rl import numpy_act as A, numpy_obs as NO, numpy_policy as NP
    st = NO.state_from_obs(obs, privates, step, memo)
    heads, _v = NP.apply(NP.pack(params), *(A._flat(x) for x in NO.encode(st)))
    masks = A.masks_for(st, bundle_ok)

WHY THIS EXISTS
---------------
Third and last of the numpy ports, after `numpy_policy` (forward pass) and `numpy_obs` (encoder).
The competition runtime has never had jax or flax; between the three files the trained net can be
consulted inside a submission.

Only the PLAY path is here. `sample`, `evaluate`, `_score` and `to_sim_actions` are training-side
and stay in `jax_act`, because nothing in a submission draws from a distribution or computes a
log-prob -- `kagg/agents/neural.py` takes a masked argmax and decodes it. Porting them would be
three hundred lines that no shipped artifact can reach, and each one a place for the two copies to
disagree unnoticed.

WHAT IS DELIBERATELY PRESERVED
------------------------------
Two mask rules here look like bugs and are not, and both were defects that cost real games:

- **Movement is bounds-only; a LOCKED destination is legal.** Three of the four shed-access tiles
  are LOCKED on day 0 and hands spawn on them. Requiring an unlocked destination stranded the hand
  at (5,5) for the whole season -- its label was WEST, the mask made WEST unemittable, and the loss
  was zeroed on it, so it never reached a gradient either.
- **The shed is reachable from a LOCKED tile.** `_apply_unit_action` resolves DROP/PICKUP/PLACE
  above the LOCKED guard (`reference/kaggriculture.py:337-340`); the tile is only a standing
  position. The same three tiles, and it once reduced COMMIT_PICKUP to the single tile (4,4).

**No market legality is enforced.** Not sells, not buys, not hires -- only bundle PADDING. Their
legality depends on the shed, the price and the Fibonacci ladder against a bank the same turn's
sells are still settling into, so a pre-turn mask is wrong in both directions; the environment
declines each cleanly at no cost. Measured: 48.75% of the teacher's own SELL orders have a pre-turn
shed of zero for that product, so a strict mask vetoed bundles the loss had taught on 52% of
sell-turns and handed the probability to the next-ranked bundle -- a live trade nobody chose.

Padding must stay masked. An out-of-range gather is clamped rather than raised, so an unmasked
padding index decodes as the highest real bundle: a confident order with nothing behind it.

`tests/test_the_numpy_masks_match_the_jax_masks.py` is what keeps this honest, on a real board with
the shipped agent driving. Same standing as the other two ports: unrun, this file is a liability.
"""

import numpy as np

from kagg.rl import numpy_obs as NO
from kagg.sim import ops as O

# ---- head layout, identical to `jax_act` ---------------------------------------------------------
UNIT_HEADS = ("op", "crop", "item", "qty")
MARKET_HEADS = ("bundle", "qty_sell", "qty_buy_product", "qty_buy_seed")
ALL_HEADS = UNIT_HEADS + MARKET_HEADS
OP_CONDITIONED_HEADS = ("crop", "item", "qty")
CONDITION_HEADS = ("op",)

#: From `jax_policy`. Stated rather than imported: importing it pulls flax into the submission.
#: `tests/test_the_numpy_masks_match_the_jax_masks.py` asserts these against the originals.
N_BUNDLES = 256
MAX_QTY = 64
UNIT_QTY_BUCKETS = np.arange(1, 17, dtype=np.int32)

# ---- commitment tokens, from `kagg/rl/commit.py` -------------------------------------------------
N_COMMIT = 5
N_OPS = O.N_OPS
N_POLICY_OPS = O.N_OPS + N_COMMIT
FAR = 10_000

_XS = (np.arange(NO.TILES) % NO.BOARD).astype(np.int32)
_YS = (np.arange(NO.TILES) // NO.BOARD).astype(np.int32)


def _flat(x):
    """[B, P, ...] -> [B*P, ...]; both seats run through the network as one batch."""
    return np.asarray(x).reshape(-1, *np.asarray(x).shape[2:])


def _unflat(x, b):
    return np.asarray(x).reshape(b, 2, *np.asarray(x).shape[1:])


# ---- commitment legality --------------------------------------------------------------------------
def _candidates(state):
    """[N_COMMIT, B, P, TILES] bool: tiles worth walking to, per commitment category.

    **Mirrors `unit_op_mask` exactly.** A target pointing at a tile where the arrival op is illegal
    spends the whole walk and fires nothing -- `jax_obs` records that bug being fixed once already,
    where the HARVEST target covered only the crop half and units were pulled toward ripe melons and
    never toward a goose with eggs waiting.
    """
    t = state.tiles
    day = (state.step_index // NO.TURNS_PER_DAY)[:, None, None]
    is_plant = t.kind == NO.PLANT
    has_animal = t.animal != NO.NO_ANIMAL
    crop_safe = np.clip(t.crop, 0, NO.N_CROPS - 1)
    ripe = (is_plant & (t.yield_units > 0)
            & ((day - t.planted_day) >= NO.FIRST_YIELD_DAY[crop_safe]))
    has_seed = (state.farm.seeds.sum(axis=-1) > 0)[..., None]
    is_shed = np.zeros((t.kind.shape[-1],), dtype=bool)
    is_shed[NO.SHED_TILES] = True
    shed_ok = is_shed[None, None, :] & ((state.farm.shed.sum(axis=-1) > 0)[..., None])
    return np.stack([
        is_plant & ~t.watered_today.astype(bool),          # WATER
        ripe | (has_animal & (t.yield_units > 0)),         # HARVEST
        has_animal & ~t.fed_today.astype(bool),            # FEED
        (t.kind == NO.EMPTY) & has_seed,                   # PLANT
        np.broadcast_to(shed_ok, t.kind.shape),            # PICKUP
    ], axis=0)


def _nearest_found(candidate, pos):
    """[B, P, U] bool: is there any candidate tile at all, by the same argmin the jax path uses.

    Ties break toward the lowest flat index. Only `found` is returned -- the target coordinates are
    used by the rollout to walk a commitment forward, which no submission does.
    """
    dx = _XS[None, None, None, :] - pos[..., 0:1].astype(np.int32)
    dy = _YS[None, None, None, :] - pos[..., 1:2].astype(np.int32)
    dist = np.where(candidate[:, :, None, :], np.abs(dx) + np.abs(dy), FAR).astype(np.int32)
    nearest = np.argmin(dist, axis=-1)
    return np.take_along_axis(dist, nearest[..., None], axis=-1)[..., 0] < FAR


def commit_mask(state):
    """[B, P, U, N_COMMIT]: a commitment is legal when a reachable target of that kind exists.

    Legality only -- it says a dry tile exists somewhere, not that watering is the right move.
    """
    cand = _candidates(state)
    live = np.arange(NO.MAX_UNITS)[None, None, :] < state.farm.n_units[:, :, None]
    found = np.stack([_nearest_found(cand[c], state.farm.unit_pos) for c in range(N_COMMIT)],
                     axis=-1)
    return found & live[..., None]


# ---- unit masks -----------------------------------------------------------------------------------
def unit_op_mask(state):
    """[B, P, MAX_UNITS, N_POLICY_OPS] bool: ops that would actually do something for each unit.

    Evaluated on the tile the unit stands on now, before anything this turn has moved.
    """
    t, farm = state.tiles, state.farm
    day = (state.step_index // NO.TURNS_PER_DAY)[:, None, None]

    pos = farm.unit_pos
    x, y = pos[..., 0], pos[..., 1]
    idx = y * NO.BOARD + x

    def g(field):
        return np.take_along_axis(field[:, :, None, :], idx[..., None], axis=-1)[..., 0]

    kind = g(t.kind)
    crop = g(t.crop)
    animal = g(t.animal)
    units_held = g(t.yield_units)
    watered = g(t.watered_today).astype(bool)
    planted = g(t.planted_day)
    fed = g(t.fed_today).astype(bool)
    cared = g(t.cared_today).astype(bool)
    fert_ok = g(t.fertilizer_available).astype(bool)

    has_animal = animal != NO.NO_ANIMAL
    is_plant = kind == NO.PLANT
    empty_structure = ((kind == NO.COOP) | (kind == NO.PASTURE)) & ~has_animal
    # Standing position only -- a LOCKED shed-access tile still reaches the shed.
    on_shed = (idx[..., None] == NO.SHED_TILES).any(axis=-1)

    carried = farm.carried
    carrying_any = carried.sum(axis=-1) > 0
    carrying_wheat = carried[..., O.WHEAT_ITEM] > 0
    carrying_fert = carried[..., O.FERT_ITEM] > 0
    shed_any = (farm.shed.sum(axis=-1) > 0)[:, :, None]
    seeds_any = (farm.seeds.sum(axis=-1) > 0)[:, :, None]

    # Bounds only. A LOCKED destination is legal, or a hand spawning on one is stranded forever.
    def can_move(dx, dy):
        nx, ny = x + dx, y + dy
        return (nx >= 0) & (nx < NO.BOARD) & (ny >= 0) & (ny < NO.BOARD)

    crop_safe = np.clip(crop, 0, NO.N_CROPS - 1)
    ripe_plant = is_plant & (units_held > 0) & ((day - planted) >= NO.FIRST_YIELD_DAY[crop_safe])

    masks = [None] * N_OPS
    masks[O.NOOP] = np.ones_like(has_animal)               # never mask the no-op
    masks[O.NORTH] = can_move(0, -1)
    masks[O.SOUTH] = can_move(0, 1)
    masks[O.EAST] = can_move(1, 0)
    masks[O.WEST] = can_move(-1, 0)
    masks[O.WATER] = is_plant & ~watered
    masks[O.HARVEST] = ripe_plant | (has_animal & (units_held > 0))
    masks[O.PLANT_OP] = (kind == NO.EMPTY) & seeds_any
    masks[O.DIG] = (kind == NO.WEED) | is_plant | empty_structure
    masks[O.PICKUP] = on_shed & shed_any
    masks[O.DROP] = on_shed & carrying_any
    masks[O.PLACE] = (on_shed & carrying_any) | (empty_structure & carrying_any)
    masks[O.FEED] = has_animal & ~fed & carrying_wheat
    masks[O.CARE] = has_animal & ~cared
    masks[O.COLLECT_FERT] = has_animal & fert_ok
    masks[O.FERTILIZE] = is_plant & carrying_fert
    masks[O.BUILD_COOP] = kind == NO.EMPTY
    masks[O.BUILD_PASTURE] = kind == NO.EMPTY

    live = np.arange(NO.MAX_UNITS)[None, None, :] < farm.n_units[:, :, None]
    stacked = np.concatenate([np.stack([np.broadcast_to(m, has_animal.shape) for m in masks],
                                       axis=-1), commit_mask(state)], axis=-1)
    # A dead slot may only NOOP, so its distribution is a point mass and contributes no gradient.
    only_noop = (np.arange(N_POLICY_OPS) == O.NOOP)
    return np.where(live[..., None], stacked, only_noop)


def unit_crop_mask(state):
    """[B, P, MAX_UNITS, N_CROPS]: crops the farm actually holds a seed for."""
    have = state.farm.seeds > 0
    have = np.broadcast_to(have[:, :, None, :],
                           (*state.farm.unit_pos.shape[:3], NO.N_CROPS))
    return np.where(have.any(axis=-1, keepdims=True), have, np.ones_like(have))


def unit_item_mask(state):
    """[B, P, MAX_UNITS, N_ITEMS]: items worth naming for PICKUP or PLACE.

    PICKUP names something in the shed, PLACE something the unit carries; the union serves both.
    """
    carried = state.farm.carried > 0
    in_shed = (state.farm.shed > 0)[:, :, None, :]
    usable = carried | np.broadcast_to(in_shed, carried.shape)
    return np.where(usable.any(axis=-1, keepdims=True), usable, np.ones_like(usable))


def masks_for(state, bundle_ok):
    """Every head's legality mask, in network-flat layout.

    `bundle_ok` is `[N_BUNDLES]` bool -- is index `b` a real vocabulary entry rather than padding.
    REQUIRED, not defaulted: a padding index left selectable decodes as a real bundle nobody chose.
    """
    b = state.farm.money.shape[0]
    op = unit_op_mask(state)
    crop = unit_crop_mask(state)
    item = unit_item_mask(state)
    qty = np.ones((b, 2, NO.MAX_UNITS, len(UNIT_QTY_BUCKETS)), dtype=bool)

    ok = np.asarray(bundle_ok, dtype=bool)
    bundle = np.broadcast_to(ok[None, None, :], (b, 2, ok.shape[0]))

    qty_sell = np.ones((b, 2, NO.N_PRODUCTS, MAX_QTY), dtype=bool)
    qty_buy_product = np.ones((b, 2, NO.N_PRODUCTS, MAX_QTY), dtype=bool)
    qty_buy_seed = np.ones((b, 2, NO.N_CROPS, MAX_QTY), dtype=bool)

    out = {"op": op, "crop": crop, "item": item, "qty": qty, "bundle": bundle,
           "qty_sell": qty_sell, "qty_buy_product": qty_buy_product,
           "qty_buy_seed": qty_buy_seed}
    return {k: _flat(v) for k, v in out.items()}


# ---- conditioning ---------------------------------------------------------------------------------
def _select_slice(heads, keys, index):
    """Gather each named head's slice at `index` along its second-to-last axis.

    A head shaped `[.., C, K]` carries one length-`K` distribution per value of the conditioning
    variable; once that variable is chosen the conditional distribution is the matching slice.
    """
    out = dict(heads)
    for k in keys:
        h = np.asarray(heads[k])
        idx = np.broadcast_to(index, h.shape[:-2])[..., None, None]
        idx = np.broadcast_to(idx, h.shape[:-2] + (1, h.shape[-1]))
        out[k] = np.take_along_axis(h, idx, axis=-2)[..., 0, :]
    return out


def condition_on_op(heads, op):
    """Select each argument head's slice for the chosen op, per unit.

    `crop` is read by PLANT alone, so the op axis buys nothing there. `item` and `qty` are read by
    BOTH PICKUP and PLACE, whose teacher distributions are nearly disjoint (total variation 0.900 --
    you pick up what is on the ground and place what is in hand). Removing that averaging is what
    this is for.
    """
    return _select_slice(heads, OP_CONDITIONED_HEADS, op)


def condition_all(heads, actions):
    """The conditioning step, on the variable the heads read."""
    return condition_on_op(heads, actions["op"])
