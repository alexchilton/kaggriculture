"""`adapter.state_from_obs` + `jax_obs.encode`, in numpy, so a trained net can ship.

    from kagg.rl import numpy_obs as NO
    memo = NO.GameMemo()
    memo.observe(obs, step)
    tiles, units, glob = NO.encode(NO.state_from_obs(obs, privates, step, memo))

WHY THIS EXISTS
---------------
A submission is one self-contained `main.py` and the competition runtime has never had `jax` or
`flax`. `kagg/rl/numpy_policy.py` moved the forward pass; this moves the other half, which is the
bigger one: the observation. Between them the shipped agent can consult the network.

**Nothing here needed jax in the first place.** `kagg/sim/{market,tiles,farm,ops,town}.py` are all
plain numpy over `kaggle_environments`, and every constant `jax_obs` reads is derived from those
same five modules -- `jax_sim` only casts them with `jnp.asarray`. So this file imports the sources
rather than a snapshot of them: there is no generated constants file to fall behind, and a balance
change lands on both paths at once. That mattered on 2026-08-15, when a new `hinge` price shape
would have priced three products at flat base in silence.

**TWO IMPLEMENTATIONS OF ONE ENCODER IS THE TRAP THIS PROJECT HAS ALREADY FALLEN INTO.**
`adapter.py`'s own docstring argues against exactly this file, and it is right on the merits: the
two encoders that already existed disagreed on 23 dead unit slots, silently, for weeks, and it
changed the live farmer's chosen op. The argument loses only because the alternative is not
shipping the net at all. What makes it survivable is that the disagreement is *checked*, on real
boards, by `tests/test_the_numpy_encoder_matches_the_jax_encoder.py`. If that test is not run, this
file is a liability rather than an asset -- the same standing that `numpy_policy.py` has.

So: **do not "improve" anything here.** Every line is a transliteration of `jax_obs.encode` and
`adapter.state_from_obs`, in their order, deliberately keeping the `[B, P, ...]` batch-and-seat
shapes even though play only ever needs one turn of one seat. A shape simplification is a place the
two can differ that the test would have to be rewritten to catch.
"""

import numpy as np

from kagg.sim import farm as F, market as M, ops as O, tiles as T, town as W

# ---- constants, derived the same way `jax_sim` derives them --------------------------------------
BOARD, TILES, TURNS_PER_DAY = T.BOARD, T.TILES, T.TURNS_PER_DAY
EMPTY, LOCKED, WEED, PLANT = T.EMPTY, T.LOCKED, T.WEED, T.PLANT
COOP, PASTURE, NO_ANIMAL = T.COOP, T.PASTURE, T.NO_ANIMAL
CROP_INDEX = T.CROP_INDEX
N_CROPS, N_ITEMS, N_PRODUCTS, N_ANIMALS = F.N_CROPS, M.N_ITEMS, M.N_PRODUCTS, M.N_ANIMALS
MAX_UNITS, N_LAND = F.MAX_UNITS, F.N_LAND
N_SHOPS = W.N_SHOPS
MAX_INSTANCES = max(W.MAX_SHOP_INSTANCES, W.N_SHOPS)
NEVER = np.int32(1 << 24)
SNAPSHOT_DAYS = (1, 3, 5)
SNAPSHOT_WIDTH = 6 + N_CROPS + N_ANIMALS + 3

FIRST_YIELD_DAY = np.asarray(T.FIRST_YIELD_DAY, dtype=np.int32)
ANIMAL_FIRST_YIELD_DAY = np.asarray(T.ANIMAL_FIRST_YIELD_DAY, dtype=np.int32)
ANIMAL_INTERVAL = np.asarray(T.ANIMAL_INTERVAL, dtype=np.int32)
ANIMAL_STRUCTURE = np.asarray(T.ANIMAL_STRUCTURE, dtype=np.int32)
HIRE_COST = np.asarray(F.HIRE_COST, dtype=np.float64)
LAND_PRICES = np.asarray(F.LAND_PRICES, dtype=np.float64)
SHED_TILES = np.asarray(O.SHED_TILES, dtype=np.int32)
INV0 = np.asarray(M.I0, dtype=np.float64)
#: Where `jax_sim.reset` parks every unit, and therefore where an unhired slot must read.
SPAWN_X, SPAWN_Y = (int(v) for v in F.default_spawn())

ANIMAL_INDEX = {name: i for i, name in enumerate(M.ANIMALS)}
ITEM_INDEX, ITEMS, PRODUCTS = M.ITEM_INDEX, M.ITEMS, M.PRODUCTS
_STRUCTURE_KIND = {"COOP": COOP, "PASTURE": PASTURE}

# ---- the feature layout, mirroring `jax_obs` -----------------------------------------------------
N_KINDS = 6
_XS = np.arange(TILES) % BOARD
_YS = np.arange(TILES) // BOARD
N_ANIMAL_KINDS = len(ANIMAL_STRUCTURE)
_OPPONENT_WIDTH = N_KINDS + N_CROPS + N_ANIMAL_KINDS

TILE_FEATURES = N_KINDS + N_CROPS + N_ANIMAL_KINDS + 13
UNIT_FEATURES = 4 + N_ITEMS + 4 * 3
N_DAYS = 30
_TIME_WIDTH = TURNS_PER_DAY + N_DAYS
_SHOP_WIDTH = N_SHOPS
_SNAPSHOT_WIDTH = len(SNAPSHOT_DAYS) * SNAPSHOT_WIDTH
_SHOP_DATE_WIDTH = MAX_INSTANCES
_LATCH_WIDTH = 2
_MEMORY_WIDTH = _SNAPSHOT_WIDTH + _SHOP_DATE_WIDTH + _LATCH_WIDTH

_SNAPSHOT_SCALE = np.concatenate([
    np.full((6,), 100.0), np.full((N_CROPS,), 100.0), np.full((N_ANIMAL_KINDS,), 20.0),
    np.asarray([50_000.0, 24.0, 3.0]),
]).astype(np.float32)

YARN_STORE_INDEX = 3
Q4_LATCH_DAY = 5
MELON_LATCH_DAY = 3
OPPONENT_MELON = 9
CROP_INDEX_MELON = CROP_INDEX["MELON"]

GLOBAL_FEATURES = (3 + 2 + _TIME_WIDTH + _SHOP_WIDTH + N_PRODUCTS * 2 + N_CROPS + N_ITEMS
                   + 3 + 3 + _OPPONENT_WIDTH + _MEMORY_WIDTH)

MONEY_SCALE = 50_000.0
PRICE_SCALE = 250.0
INVENTORY_SCALE = 500.0

HIRE_REBUILD_COST = np.concatenate([
    np.zeros((1,), dtype=np.float32),
    np.cumsum(np.concatenate([np.zeros((1,), dtype=np.float32),
                              HIRE_COST.astype(np.float32)]))[:-1],
])

REHIRE_AFFORD_INDEX = -(1 + _OPPONENT_WIDTH + _MEMORY_WIDTH)
HIRE_AFFORD_INDEX = -(2 + _OPPONENT_WIDTH + _MEMORY_WIDTH)
LAND_AFFORD_INDEX = -(3 + _OPPONENT_WIDTH + _MEMORY_WIDTH)


def _one_hot(x, n):
    return (np.asarray(x)[..., None] == np.arange(n)).astype(np.float32)


# ---- the state ----------------------------------------------------------------------------------
class _Bag:
    """Attribute access over a dict, so `state.farm.money` reads as it does on the jax path.

    A plain class rather than the `NamedTuple`s in `jax_sim`, because those are jax pytrees and
    registering pytrees is the one thing about them this file must not inherit.
    """

    def __init__(self, **kw):
        self.__dict__.update(kw)


def _tile_arrays(tiles):
    """One farm's 10x10 nested tile list -> the flat per-tile arrays.

    A verbatim copy of `adapter._tile_arrays`, which is already pure numpy. Copied rather than
    imported because importing it would pull `adapter` -> `jax_sim` -> `jax` into the submission,
    which is the whole thing this file exists to avoid.
    """
    n = TILES
    out = {
        "kind": np.full(n, EMPTY, dtype=np.int32),
        "crop": np.full(n, -1, dtype=np.int32),
        "planted_day": np.zeros(n, dtype=np.int32),
        "watered_today": np.zeros(n, dtype=np.int32),
        "consecutive_unwatered": np.zeros(n, dtype=np.int32),
        "yield_units": np.zeros(n, dtype=np.int32),
        "max_lifespan_step": np.full(n, -1, dtype=np.int32),
        "fertilized_until_day": np.full(n, -1, dtype=np.int32),
        "animal": np.full(n, -1, dtype=np.int32),
        "placed_day": np.zeros(n, dtype=np.int32),
        "consecutive_unfed": np.zeros(n, dtype=np.int32),
        "fed_today": np.zeros(n, dtype=bool),
        "cared_today": np.zeros(n, dtype=bool),
        "fertilizer_available": np.zeros(n, dtype=bool),
        "pending_care_bonus": np.zeros(n, dtype=np.int32),
    }
    for y, row in enumerate(tiles):
        for x, cell in enumerate(row):
            i = y * BOARD + x
            if cell == "LOCKED":
                out["kind"][i] = LOCKED
                continue
            if cell is None:
                continue
            kind = cell.get("kind")
            if kind == "WEED":
                out["kind"][i] = WEED
            elif kind == "PLANT":
                out["kind"][i] = PLANT
                out["crop"][i] = CROP_INDEX[cell["crop"]]
                out["planted_day"][i] = cell.get("planted_day", 0)
                out["watered_today"][i] = int(bool(cell.get("watered_today")))
                out["consecutive_unwatered"][i] = cell.get("consecutive_unwatered", 0)
                out["yield_units"][i] = cell.get("yield_units", 0)
                out["max_lifespan_step"][i] = cell.get("max_lifespan_step", -1)
                out["fertilized_until_day"][i] = cell.get("fertilized_until_day", -1)
            elif kind in _STRUCTURE_KIND:
                out["kind"][i] = _STRUCTURE_KIND[kind]
                if "animal" in cell:
                    out["animal"][i] = ANIMAL_INDEX[cell["animal"]]
                    out["placed_day"][i] = cell.get("placed_day", 0)
                    out["yield_units"][i] = cell.get("yield_units", 0)
                    out["consecutive_unfed"][i] = cell.get("consecutive_unfed", 0)
                    out["fed_today"][i] = bool(cell.get("fed_today"))
                    out["cared_today"][i] = bool(cell.get("cared_today"))
                    out["fertilizer_available"][i] = bool(cell.get("fertilizer_available"))
                    out["pending_care_bonus"][i] = cell.get("pending_care_bonus", 0)
    return out


def _shop_slots(obs):
    """`unlocked_shops` as slot-indexed shop ids -- NOT `observation["shops"]`, which does not exist
    and which silently produced all-zero drain tables over 5,376 games."""
    index = {name: i for i, name in enumerate(W.SHOPS)}
    town = (obs or {}).get("town") or {}
    names = [n for n in (town.get("unlocked_shops") or []) if n in index]
    return [index[n] for n in names[:MAX_INSTANCES]]


def _seat_summary_from_obs(obs):
    """`[1, P, SNAPSHOT_WIDTH]` -- each seat's own position. Mirrors `adapter._seat_summary_from_obs`.

    Counted off `_tile_arrays` rather than off the cell dicts: a locked tile is the STRING "LOCKED"
    and an empty one is `None`, so filtering to dicts drops both and the EMPTY and LOCKED columns
    come out wrong.
    """
    kinds = [EMPTY, LOCKED, WEED, PLANT, COOP, PASTURE]
    farms = (obs or {}).get("farms") or []
    out = np.zeros((1, 2, SNAPSHOT_WIDTH), dtype=np.float32)
    for p in range(2):
        farm = farms[p] if p < len(farms) else {}
        f = _tile_arrays(farm.get("tiles") or [])
        kind, crop, animal = f["kind"], f["crop"], f["animal"]
        for i, k in enumerate(kinds):
            out[0, p, i] = int((kind == k).sum())
        for ci in range(len(CROP_INDEX)):
            out[0, p, len(kinds) + ci] = int(((kind == PLANT) & (crop == ci)).sum())
        for a in range(N_ANIMALS):
            out[0, p, len(kinds) + len(CROP_INDEX) + a] = int((animal == a).sum())
        tail = len(kinds) + len(CROP_INDEX) + N_ANIMALS
        out[0, p, tail] = float(farm.get("money") or 0)
        out[0, p, tail + 1] = 1.0 + len(farm.get("hands") or [])
        out[0, p, tail + 2] = float(len(farm.get("unlocked_quadrants", ["NW"])) - 1)
    return out


class GameMemo:
    """What an observation stops saying, remembered across the turns of one game.

    Same rules as `adapter.GameMemo`, and `test_the_two_memos_agree` holds them to it: a slot's
    unlock day is the first day it is seen, and the opponent snapshot is latched at hour 0 only,
    only into a slot still holding `NEVER`. Keyed on slot POSITION, not shop name -- 1.32.6 draws
    with replacement, so one shop can hold two slots that opened days apart.
    """

    def __init__(self):
        self._first_seen = {}
        self._snapshot = np.full((1, 2, len(SNAPSHOT_DAYS), SNAPSHOT_WIDTH),
                                 float(NEVER), dtype=np.float32)

    def observe(self, obs, step):
        day = int(step) // TURNS_PER_DAY
        for slot in range(len(_shop_slots(obs))):
            self._first_seen.setdefault(slot, day)
        if step % TURNS_PER_DAY == 0 and day in SNAPSHOT_DAYS:
            d = SNAPSHOT_DAYS.index(day)
            if np.all(self._snapshot[0, :, d] == float(NEVER)):
                self._snapshot[0, :, d] = _seat_summary_from_obs(obs)[0, ::-1]
        return self

    def unlock_days(self):
        days = np.full((1, MAX_INSTANCES), NEVER, dtype=np.int32)
        for slot, day in self._first_seen.items():
            days[0, slot] = day
        return days

    def opp_snapshot(self):
        return self._snapshot.astype(np.float32)


def _unlock_days(obs, memo=None):
    if memo is not None:
        return memo.unlock_days()
    slots = _shop_slots(obs)
    days = np.full((1, MAX_INSTANCES), NEVER, dtype=np.int32)
    days[0, : len(slots)] = 0
    return days


def _unlock_shops(obs):
    slots = _shop_slots(obs)
    ids = np.zeros((1, MAX_INSTANCES), dtype=np.int32)
    ids[0, : len(slots)] = np.asarray(slots, dtype=np.int32)
    return ids


def agent_private_stub():
    """An empty private dict, for the opponent seat a submission cannot see."""
    return {"shed": {}, "seeds": {}, "inventories": [{}]}


def state_from_obs(obs, privates, step=None, memo=None):
    """A batch-of-one state from one turn's observation. Mirrors `adapter.state_from_obs`.

    `step` is explicit because `obs["step"]` is not always there and its absence is silent:
    `kaggle_environments` puts it in seat 0's observation only. Falling back to 0 hands a mid-season
    board to a day-0 counter, and every crop and animal rule is driven by `step // TURNS_PER_DAY` --
    measured on the four DAgger tapes, that forbade 300 of 1,585 HARVEST labels.
    """
    farms = obs["farms"]
    step = int(obs.get("step", 0) or 0) if step is None else int(step)

    tile_fields = [_tile_arrays(farms[p]["tiles"]) for p in range(2)]
    tiles = _Bag(**{
        name: np.stack([tile_fields[0][name], tile_fields[1][name]])[None]
        for name in tile_fields[0]
    })

    money = np.array([[farms[p]["money"] for p in range(2)]], dtype=np.float64)
    seeds = np.zeros((1, 2, N_CROPS), dtype=np.int32)
    shed = np.zeros((1, 2, N_ITEMS), dtype=np.int32)
    carried = np.zeros((1, 2, MAX_UNITS, N_ITEMS), dtype=np.int32)
    # Dead slots parked on the SPAWN tile, matching `jax_sim.reset` and `adapter.state_from_obs`.
    # See the note in `adapter`: zeroing these columns in the encoder instead changed the meaning of
    # three features every checkpoint was fitted on and took movement to 0.000.
    unit_pos = np.zeros((1, 2, MAX_UNITS, 2), dtype=np.int32)
    unit_pos[..., 0] = SPAWN_X
    unit_pos[..., 1] = SPAWN_Y
    n_units = np.ones((1, 2), dtype=np.int32)

    for p in range(2):
        priv = privates[p] or {}
        for crop, i in CROP_INDEX.items():
            seeds[0, p, i] = priv.get("seeds", {}).get(crop, 0)
        for item, i in ITEM_INDEX.items():
            shed[0, p, i] = priv.get("shed", {}).get(item, 0)
        for u, inv in enumerate(priv.get("inventories", [])[:MAX_UNITS]):
            for item, qty in (inv or {}).items():
                if item in ITEM_INDEX:
                    carried[0, p, u, ITEM_INDEX[item]] = qty

        positions = [tuple(farms[p]["farmer"])] + [tuple(h) for h in farms[p].get("hands", [])]
        n_units[0, p] = min(len(positions), MAX_UNITS)
        for u, (x, y) in enumerate(positions[:MAX_UNITS]):
            unit_pos[0, p, u] = (x, y)

    farm = _Bag(
        money=money,
        seeds=seeds,
        shed=shed,
        carried=carried,
        unit_pos=unit_pos,
        n_units=n_units,
        hires_today=np.asarray(
            [[farms[p].get("hires_today", 0) for p in range(2)]], dtype=np.int32),
        n_land=np.asarray(
            [[len(farms[p].get("unlocked_quadrants", ["NW"])) - 1 for p in range(2)]],
            dtype=np.int32),
    )

    return _Bag(
        step_index=np.asarray([step], dtype=np.int32),
        tiles=tiles,
        farm=farm,
        inventory=np.asarray([[obs["market"]["inventory"][item] for item in PRODUCTS]],
                             dtype=np.int32),
        unlock_day=_unlock_days(obs, memo),
        unlock_shop=_unlock_shops(obs),
        opp_snapshot=(memo.opp_snapshot() if memo is not None else np.full(
            (1, 2, len(SNAPSHOT_DAYS), SNAPSHOT_WIDTH), float(NEVER), dtype=np.float32)),
    )


# ---- the encoder ---------------------------------------------------------------------------------
def encode(state):
    """`(tiles, units, glob)`, line for line with `jax_obs.encode`.

    Shapes `[B, P, TILES, TILE_FEATURES]`, `[B, P, MAX_UNITS, UNIT_FEATURES]`,
    `[B, P, GLOBAL_FEATURES]`. Seat `p` sees its own farm in full and the other in aggregate.
    """
    t, farm = state.tiles, state.farm
    day = (state.step_index // TURNS_PER_DAY).astype(np.float32)
    hour = (state.step_index % TURNS_PER_DAY).astype(np.float32)
    day_i = np.clip(state.step_index // TURNS_PER_DAY, 0, N_DAYS - 1)
    hour_i = state.step_index % TURNS_PER_DAY
    hour_1h = _one_hot(hour_i, TURNS_PER_DAY)
    day_1h = _one_hot(day_i, N_DAYS)
    shop_open = np.max(
        _one_hot(state.unlock_shop, N_SHOPS)
        * (state.unlock_day <= day_i[:, None])[..., None].astype(np.float32),
        axis=1)
    day_t = day[:, None, None]
    day_g = day[:, None]                                                   # noqa: F841

    # ---- tiles ---------------------------------------------------------------------------------
    is_plant = t.kind == PLANT
    has_animal = t.animal != NO_ANIMAL
    tiles = np.concatenate(
        [
            _one_hot(t.kind, N_KINDS),
            _one_hot(np.where(is_plant, t.crop, -1), N_CROPS),
            _one_hot(np.where(has_animal, t.animal, -1), N_ANIMAL_KINDS),
            (t.yield_units / 8.0).astype(np.float32)[..., None],
            t.watered_today.astype(np.float32)[..., None],
            (t.consecutive_unwatered / 2.0).astype(np.float32)[..., None],
            np.where(is_plant, (day_t - t.planted_day) / 30.0, 0.0)
            .astype(np.float32)[..., None],
            np.where(has_animal, (day_t - t.placed_day) / 30.0, 0.0)
            .astype(np.float32)[..., None],
            (1.0 / (1.0 + np.where(
                has_animal,
                np.maximum(0, ANIMAL_FIRST_YIELD_DAY[np.maximum(t.animal, 0)]
                           - (day_t - t.placed_day))
                + np.where(
                    (day_t - t.placed_day)
                    >= ANIMAL_FIRST_YIELD_DAY[np.maximum(t.animal, 0)],
                    (-(day_t - t.placed_day
                       - ANIMAL_FIRST_YIELD_DAY[np.maximum(t.animal, 0)]))
                    % np.maximum(ANIMAL_INTERVAL[np.maximum(t.animal, 0)], 1),
                    0),
                1000).astype(np.float32))).astype(np.float32)[..., None],
            (t.fertilized_until_day >= day_t).astype(np.float32)[..., None],
            t.fed_today.astype(np.float32)[..., None],
            t.cared_today.astype(np.float32)[..., None],
            t.fertilizer_available.astype(np.float32)[..., None],
            (t.pending_care_bonus / 4.0).astype(np.float32)[..., None],
            (t.consecutive_unfed / 2.0).astype(np.float32)[..., None],
            (has_animal & (t.consecutive_unfed >= 1)).astype(np.float32)[..., None],
        ],
        axis=-1,
    )

    # ---- units ---------------------------------------------------------------------------------
    live = np.arange(MAX_UNITS)[None, None, :] < farm.n_units[:, :, None]
    pos = farm.unit_pos
    flat = pos[..., 1] * BOARD + pos[..., 0]
    on_shed = (flat[..., None] == SHED_TILES).any(axis=-1)

    def _target(candidate):
        """Signed direction and distance to the nearest tile satisfying `candidate`. [B, P, U, 3]"""
        dx = _XS[None, None, None, :] - pos[..., 0:1]
        dy = _YS[None, None, None, :] - pos[..., 1:2]
        dist = np.abs(dx) + np.abs(dy)
        masked = np.where(candidate[:, :, None, :], dist, 999)
        nearest = np.argmin(masked, axis=-1)[..., None]
        found = np.take_along_axis(masked, nearest, axis=-1) < 999
        take = lambda a: np.take_along_axis(a, nearest, axis=-1)   # noqa: E731
        return np.concatenate([
            np.where(found, take(dx) / (BOARD - 1.0), 0.0),
            np.where(found, take(dy) / (BOARD - 1.0), 0.0),
            np.where(found, 1.0 / (1.0 + take(masked).astype(np.float32)), 0.0),
        ], axis=-1).astype(np.float32)

    is_plant_t = t.kind == PLANT
    needs_water = is_plant_t & ~t.watered_today.astype(bool)
    has_animal_t = t.animal != NO_ANIMAL

    crop_safe_t = np.clip(t.crop, 0, N_CROPS - 1)
    ripe_crop = (is_plant_t & (t.yield_units > 0)
                 & ((day_t - t.planted_day) >= FIRST_YIELD_DAY[crop_safe_t]))
    is_ripe = ripe_crop | (has_animal_t & (t.yield_units > 0))
    needs_feed = has_animal_t & ~t.fed_today.astype(bool)

    # A dead slot reads its SPAWN position, in both encoders -- see the note in `jax_obs.encode`.
    # These three columns are deliberately not gated on `live`: zeroing them changes the meaning of
    # features every checkpoint was fitted on, and `state_from_obs` parks dead slots at spawn so the
    # two paths agree without touching a trained column.
    units = np.concatenate(
        [
            live.astype(np.float32)[..., None],
            (pos[..., 0] / (BOARD - 1.0)).astype(np.float32)[..., None],
            (pos[..., 1] / (BOARD - 1.0)).astype(np.float32)[..., None],
            on_shed.astype(np.float32)[..., None],
            np.minimum(farm.carried / 10.0, 3.0).astype(np.float32),
            _target(needs_water),
            _target(is_ripe),
            _target(needs_feed),
            _target(t.kind == EMPTY),
        ],
        axis=-1,
    )

    # ---- opponent summary ----------------------------------------------------------------------
    kind_counts = np.stack(
        [(t.kind == k).sum(axis=-1) for k in range(N_KINDS)], axis=-1) / 100.0
    crop_counts = np.stack(
        [((t.kind == PLANT) & (t.crop == c)).sum(axis=-1) for c in range(N_CROPS)],
        axis=-1) / 100.0
    animal_counts = np.stack(
        [(t.animal == a).sum(axis=-1) for a in range(N_ANIMAL_KINDS)], axis=-1) / 20.0
    board_summary = np.concatenate(
        [kind_counts, crop_counts, animal_counts], axis=-1).astype(np.float32)
    opponent = board_summary[:, ::-1]
    opp_money = farm.money[:, ::-1]

    # ---- global --------------------------------------------------------------------------------
    prices = (M.price(state.inventory) / PRICE_SCALE).astype(np.float32)
    inventory = ((state.inventory - INV0) / INVENTORY_SCALE).astype(np.float32)
    b = farm.money.shape[0]

    safe_money = np.maximum(farm.money, 1.0)
    next_land = LAND_PRICES[np.minimum(farm.n_land, N_LAND - 1)]
    land_afford = np.where(farm.n_land < N_LAND,
                           np.minimum(next_land / safe_money, 4.0), 0.0)
    next_hire = HIRE_COST[np.minimum(farm.hires_today, MAX_UNITS)]
    hire_afford = np.minimum(next_hire / safe_money, 4.0)
    rehire_afford = np.minimum(
        HIRE_REBUILD_COST[np.clip(farm.n_units, 0, MAX_UNITS)] / safe_money, 4.0)

    # ---- the memory block ------------------------------------------------------------------------
    raw_snap = state.opp_snapshot.astype(np.float32)
    unset = raw_snap >= float(NEVER)
    snapshot = np.where(unset, 0.0, raw_snap / _SNAPSHOT_SCALE)
    snapshot = snapshot.reshape(snapshot.shape[:2] + (_SNAPSHOT_WIDTH,))

    shop_age = np.where(state.unlock_day <= day[:, None],
                        (day[:, None] - state.unlock_day) / float(N_DAYS), 0.0).astype(np.float32)

    _melon_col = 6 + CROP_INDEX_MELON
    _melon_day = SNAPSHOT_DAYS.index(MELON_LATCH_DAY)
    melon_count = np.where(unset[:, :, _melon_day, _melon_col], 0.0,
                           raw_snap[:, :, _melon_day, _melon_col])
    melon_armed = ((melon_count >= OPPONENT_MELON)
                   & (day >= MELON_LATCH_DAY)[:, None]).astype(np.float32)[..., None]
    yarn_by_d5 = ((state.unlock_shop == YARN_STORE_INDEX)
                  & (state.unlock_day <= Q4_LATCH_DAY)).any(axis=-1)
    q4_armed = (yarn_by_d5 & (day >= Q4_LATCH_DAY)).astype(np.float32)

    glob = np.concatenate(
        [
            (farm.money / MONEY_SCALE).astype(np.float32)[..., None],
            (opp_money / MONEY_SCALE).astype(np.float32)[..., None],
            ((farm.money - opp_money) / MONEY_SCALE).astype(np.float32)[..., None],
            np.broadcast_to((day / 30.0)[:, None], (b, 2))[..., None],
            np.broadcast_to((hour / 24.0)[:, None], (b, 2))[..., None],
            np.broadcast_to(hour_1h[:, None, :], (b, 2, TURNS_PER_DAY)),
            np.broadcast_to(day_1h[:, None, :], (b, 2, N_DAYS)),
            np.broadcast_to(shop_open[:, None, :], (b, 2, N_SHOPS)),
            np.broadcast_to(prices[:, None, :], (b, 2, N_PRODUCTS)),
            np.broadcast_to(inventory[:, None, :], (b, 2, N_PRODUCTS)),
            np.minimum(farm.seeds / 10.0, 5.0).astype(np.float32),
            np.minimum(farm.shed / 50.0, 3.0).astype(np.float32),
            (farm.n_units / 24.0).astype(np.float32)[..., None],
            (farm.n_land / 3.0).astype(np.float32)[..., None],
            (farm.hires_today / 12.0).astype(np.float32)[..., None],
            land_afford.astype(np.float32)[..., None],
            hire_afford.astype(np.float32)[..., None],
            rehire_afford.astype(np.float32)[..., None],
            opponent,
            snapshot,
            np.broadcast_to(shop_age[:, None, :], (b, 2, MAX_INSTANCES)),
            melon_armed,
            np.broadcast_to(q4_armed[:, None], (b, 2))[..., None],
        ],
        axis=-1,
    )
    return tiles, units, glob
