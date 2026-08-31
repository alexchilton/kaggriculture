"""Bridge the reference environment's dict observation into a `jax_sim.State`.

The policy plays on `jax_sim.State` arrays; the real environment, every heuristic agent and any
Kaggle submission all speak nested dicts -- `farm["tiles"][y][x]`, `private["shed"]`,
`market["prices"]`. Without a bridge a trained checkpoint cannot be scored against `contrarian` and
cannot be submitted, so it is the last structural gap between "the loss went down" and "it plays".

**The design decision that matters: this builds a `State`, it does not build features.**

The tempting shortcut is a second encoder going straight from dicts to the `[tiles, units, glob]`
tensors the network wants. That creates two encoders which must agree forever, and they will not:
this project has already been bitten by a parity gate that tested a subset while reporting
coverage, and by a JAX port that silently fell a commit behind the numpy sim. Reconstructing the
`State` and then calling the *same* `jax_obs.encode` that training uses makes agreement structural
rather than a thing to maintain.

It also makes the bridge testable in the way the rest of the project already tests things: build a
`State` from the environment's dict, step both forward with identical actions, and assert they stay
equal. That is the parity harness pattern, and it is why `test_adapter.py` exists.

Not reconstructed, because the observation does not contain them and they do not affect play from
the current position: `unlock_day` (the schedule is a per-episode RNG artifact) and the PRNG key.
"""

import numpy as np

from kagg.sim import jax_sim as J
from kagg.sim.market import ANIMALS, ITEM_INDEX, ITEMS, PRODUCTS
from kagg.sim.tiles import COOP, CROP_INDEX, EMPTY, LOCKED, PASTURE, PLANT, WEED

ANIMAL_INDEX = {name: i for i, name in enumerate(ANIMALS)}
_STRUCTURE_KIND = {"COOP": COOP, "PASTURE": PASTURE}


def _tile_arrays(tiles, day):
    """One farm's 10x10 nested tile list -> the flat per-tile arrays `Tiles` holds.

    Field names deliberately track `kaggriculture`'s own tile dict keys, so a reader can check this
    against the environment source without translating.
    """
    n = J.TILES
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
            i = y * J.BOARD + x
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
    """`unlocked_shops` as slot-indexed shop ids, truncated to `MAX_INSTANCES`.

    `observation["town"]["unlocked_shops"]` is the list -- NOT `observation["shops"]`, which does not
    exist and which silently produced all-zero drain tables over 5,376 games.
    """
    from kagg.sim.town import SHOPS

    index = {name: i for i, name in enumerate(SHOPS)}
    town = (obs or {}).get("town") or {}
    names = [n for n in (town.get("unlocked_shops") or []) if n in index]
    return [index[n] for n in names[: J.MAX_INSTANCES]]


def _seat_summary_from_obs(obs):
    """`[1, P, SNAPSHOT_WIDTH]` -- each seat's own position, from the dict observation.

    **Must produce the same columns in the same order as `jax_sim.seat_summary`**, which builds it
    from `Tiles`/`Farm` arrays on the training path. Two implementations of one layout is exactly the
    kind of pair that drifts, so `test_the_two_ways_a_board_becomes_a_snapshot_agree` compares them
    on a real board. The alternative -- routing this through `state_from_obs` -- is circular, since
    the snapshot is one of the things `state_from_obs` has to produce.
    """
    # **Counted off `_tile_arrays`, not off the cell dicts.** A second parser here was wrong within
    # the hour: a locked tile is the STRING "LOCKED" and an empty one is `None`, so filtering to
    # dicts dropped both and the EMPTY and LOCKED columns disagreed with `jax_sim.seat_summary`.
    # `_tile_arrays` is the one place that knows the observation's three cell encodings.
    kinds = [EMPTY, LOCKED, WEED, PLANT, COOP, PASTURE]
    farms = (obs or {}).get("farms") or []
    out = np.zeros((1, 2, J.SNAPSHOT_WIDTH), dtype=np.float32)
    for p in range(2):
        farm = farms[p] if p < len(farms) else {}
        f = _tile_arrays(farm.get("tiles") or [], 0)
        kind, crop, animal = f["kind"], f["crop"], f["animal"]
        for i, k in enumerate(kinds):
            out[0, p, i] = int((kind == k).sum())
        for ci in range(len(CROP_INDEX)):
            out[0, p, len(kinds) + ci] = int(((kind == PLANT) & (crop == ci)).sum())
        for a in range(J.N_ANIMALS):
            out[0, p, len(kinds) + len(CROP_INDEX) + a] = int((animal == a).sum())
        tail = len(kinds) + len(CROP_INDEX) + J.N_ANIMALS
        out[0, p, tail] = float(farm.get("money") or 0)
        out[0, p, tail + 1] = 1.0 + len(farm.get("hands") or [])
        out[0, p, tail + 2] = float(len(farm.get("unlocked_quadrants", ["NW"])) - 1)
    return out


class GameMemo:
    """What an observation stops saying, remembered across the turns of one game.

    Two things live here, and they are the same problem: a turn's observation describes the board
    *now*, and both the shop dates and the opponent's position on the days we commit are facts about
    a board that has since moved on. An agent sees every turn of its own game, so it can watch.

    Held together in one object because every caller needs both and a second memo would be a second
    thing to forget to pass.

    **An observation says which shops are open. It never says when they opened.** `jax_sim` carries
    the true day in `unlock_day` (3, 6, 9 ... -- the town opens one slot at the end of every third
    day, `kaggriculture.py:886`), and the adapter used to stamp 0 on everything it found open. That
    is correct for the drain, which only ever asks `unlock_day <= day`, and wrong as a date: through
    the adapter a slot that opened on day 12 is indistinguishable from one that opened on day 3.

    `unlocked_shops` is append-only, so an agent that sees every turn of its own game can recover the
    dates by watching: the first turn a slot exists is the day that slot opened.

    Keyed on the slot POSITION, not the shop name. 1.32.6 draws with replacement, so one shop can
    hold two slots that opened days apart, and `_drain` treats them as independent consumers.

    A clock that joins mid-game dates everything it finds already open from the turn it started.
    That is unknowable from the observation and no worse than the 0 it replaces -- `curriculum.py`
    resumes from recorded boards and overwrites the whole schedule for exactly this reason.
    """

    def __init__(self):
        self._first_seen = {}
        self._snapshot = np.full((1, 2, len(J.SNAPSHOT_DAYS), J.SNAPSHOT_WIDTH),
                                 float(J.NEVER), dtype=np.float32)

    def observe(self, obs, step):
        """Record this turn. Returns self, so it can be chained onto a call."""
        day = int(step) // J.TURNS_PER_DAY
        for slot in range(len(_shop_slots(obs))):
            self._first_seen.setdefault(slot, day)

        # Hour 0 only, and only into a slot still holding NEVER -- the same rule
        # `jax_sim._latch_opponent` follows, so a game that joins late keeps the gap rather than
        # back-filling it from a board the deciding agent never saw.
        if step % J.TURNS_PER_DAY == 0 and day in J.SNAPSHOT_DAYS:
            d = J.SNAPSHOT_DAYS.index(day)
            if np.all(self._snapshot[0, :, d] == float(J.NEVER)):
                self._snapshot[0, :, d] = _seat_summary_from_obs(obs)[0, ::-1]
        return self

    def unlock_days(self):
        """`[1, MAX_INSTANCES]` of unlock days, `NEVER` for a slot not yet seen."""
        import jax.numpy as jnp

        days = np.full((1, J.MAX_INSTANCES), J.NEVER, dtype=np.int32)
        for slot, day in self._first_seen.items():
            days[0, slot] = day
        return jnp.asarray(days, dtype=J._I)

    def opp_snapshot(self):
        """`[1, P, len(SNAPSHOT_DAYS), SNAPSHOT_WIDTH]`, each seat's view of the other."""
        import jax.numpy as jnp

        return jnp.asarray(self._snapshot, dtype=jnp.float32)


def _unlock_days(obs, memo=None):
    import jax.numpy as jnp

    if memo is not None:
        return memo.unlock_days()
    slots = _shop_slots(obs)
    days = np.full((1, J.MAX_INSTANCES), J.NEVER, dtype=np.int32)
    days[0, : len(slots)] = 0
    return jnp.asarray(days, dtype=J._I)


def _unlock_shops(obs):
    import jax.numpy as jnp

    slots = _shop_slots(obs)
    ids = np.zeros((1, J.MAX_INSTANCES), dtype=np.int32)
    ids[0, : len(slots)] = np.asarray(slots, dtype=np.int32)
    return jnp.asarray(ids, dtype=J._I)


def state_from_obs(obs, privates, step=None, memo=None):
    """Build a batch-of-one `jax_sim.State` from one turn's observation.

    `obs` is the shared observation (`farms`, `market`, `step`); `privates` is a two-element list of
    each player's private dict. A submission only ever sees its *own* private state, so the caller
    supplies a zeroed stand-in for the opponent -- see `agent_private_stub`. The opponent's shed and
    seeds are not visible in the real game either, so the policy is not losing information it would
    otherwise have; it is losing information it was *trained* with, which is a real distribution
    shift and is recorded in the module docstring of `kagg/agents/neural.py`.

    **`step` is explicit because `obs["step"]` is not always there, and its absence is silent.**
    `kaggle_environments` puts `step` in seat 0's observation only, and some replays carry `None`.
    Falling back to 0 hands the simulator a mid-season board under a day-0 counter, and every crop
    and animal rule is driven by `step_index // TURNS_PER_DAY`.

    Measured 2026-08-22 on the four DAgger tapes at true turn 100: the three seat-0 tapes resolved
    to day 4 and the one seat-1 tape to day 0, for all 720 turns. The mask that suffers most is
    HARVEST -- `(day - planted_day) >= FIRST_YIELD_DAY` goes negative, so nothing is ever ripe --
    and 300 of the 1585 HARVEST labels in that training set were forbidden as a result, 301 of the
    307 total offenders on that single tape. Unemittable and zero-weighted in the loss, so it shows
    up nowhere except as an op that never improves.

    A caller that knows which turn it is on should say so; it overrides the observation. Callers
    that pass nothing keep the old behaviour. `curriculum.py:114` reached the same conclusion
    independently and worked around it locally with `_with_step_index`.

    **`shop_clock` is the same argument for the shop schedule.** An observation says which shops are
    open and never when they opened, so without one every open slot is dated day 0 -- fine for the
    drain, and unusable for anything that reads the day as a date. Any caller that walks a game turn
    by turn should keep a `ShopClock` and pass it; see that class for why the observation alone
    cannot answer this.
    """
    import jax.numpy as jnp

    farms = obs["farms"]
    step = int(obs.get("step", 0) or 0) if step is None else int(step)
    day = step // J.TURNS_PER_DAY

    tile_fields = [_tile_arrays(farms[p]["tiles"], day) for p in range(2)]
    tiles = J.Tiles(**{
        name: jnp.asarray(np.stack([tile_fields[0][name], tile_fields[1][name]])[None],
                          dtype=(bool if tile_fields[0][name].dtype == bool else J._I))
        for name in tile_fields[0]
    })

    money = np.array([[farms[p]["money"] for p in range(2)]], dtype=np.float64)
    seeds = np.zeros((1, 2, len(CROP_INDEX)), dtype=np.int32)
    shed = np.zeros((1, 2, len(ITEMS)), dtype=np.int32)
    carried = np.zeros((1, 2, J.MAX_UNITS, len(ITEMS)), dtype=np.int32)
    # **Dead slots are parked on the SPAWN tile, matching `jax_sim.reset` -- not left at (0, 0).**
    #
    # `live` is 0 for these either way, so nothing legal changes. But the transformer attends over
    # all 24 unit tokens, and 23 of them differing on x, y and on_shed between training and play is
    # a real observation mismatch: measured 2026-08-28, the LIVE farmer's op came out 1 through
    # `jax_sim` and 17 through this path on the same board.
    #
    # Fixed HERE rather than by zeroing those columns in `jax_obs`, which is what was tried first.
    # Zeroing changes the MEANING of three features every checkpoint was fitted on, and
    # `migrate_params` cannot repair that -- it pads new columns, it does not re-fit moved ones. The
    # run that followed put movement at exactly 0.000 over 35,817 labels. See the note in
    # `jax_obs.encode`'s unit block.
    unit_pos = np.zeros((1, 2, J.MAX_UNITS, 2), dtype=np.int32)
    unit_pos[..., 0] = int(J.SPAWN_X)
    unit_pos[..., 1] = int(J.SPAWN_Y)
    n_units = np.ones((1, 2), dtype=np.int32)

    for p in range(2):
        priv = privates[p] or {}
        for crop, i in CROP_INDEX.items():
            seeds[0, p, i] = priv.get("seeds", {}).get(crop, 0)
        for item, i in ITEM_INDEX.items():
            shed[0, p, i] = priv.get("shed", {}).get(item, 0)
        # A unit's carried inventory is `private["inventories"][idx]`, index 0 being the farmer.
        for u, inv in enumerate(priv.get("inventories", [])[: J.MAX_UNITS]):
            for item, qty in (inv or {}).items():
                if item in ITEM_INDEX:
                    carried[0, p, u, ITEM_INDEX[item]] = qty

        positions = [tuple(farms[p]["farmer"])] + [tuple(h) for h in farms[p].get("hands", [])]
        n_units[0, p] = min(len(positions), J.MAX_UNITS)
        for u, (x, y) in enumerate(positions[: J.MAX_UNITS]):
            unit_pos[0, p, u] = (x, y)

    farm = J.Farm(
        money=jnp.asarray(money, dtype=J._F),
        seeds=jnp.asarray(seeds, dtype=J._I),
        shed=jnp.asarray(shed, dtype=J._I),
        carried=jnp.asarray(carried, dtype=J._I),
        unit_pos=jnp.asarray(unit_pos, dtype=J._I),
        n_units=jnp.asarray(n_units, dtype=J._I),
        hires_today=jnp.asarray(
            [[farms[p].get("hires_today", 0) for p in range(2)]], dtype=J._I),
        n_land=jnp.asarray(
            [[len(farms[p].get("unlocked_quadrants", ["NW"])) - 1 for p in range(2)]], dtype=J._I),
    )

    inventory = jnp.asarray(
        [[obs["market"]["inventory"][item] for item in PRODUCTS]], dtype=J._I)

    return J.State(
        step_index=jnp.asarray([step], dtype=J._I),
        tiles=tiles,
        farm=farm,
        inventory=inventory,
        # **Which shops are ALREADY trading, read off the observation.**
        #
        # This used to be all-NEVER, on the reasoning that "the unlock schedule only governs future
        # town drain". That was wrong in a way that mattered: `jax_obs.encode` now emits a bit per
        # unlocked shop, and the `q4_branch` latch choosing which of four tapes the agent replays is
        # exactly "the yarn store is unlocked" (`q4_branch.py:242`). Left stubbed, that feature reads
        # all-zero on every reference-environment rollout -- silently, and only on this path, so the
        # jax_sim path would look fine.
        #
        # What is reconstructed is "unlocked by now", not the true unlock DAY, which the observation
        # does not carry: an open shop is given day 0 and a closed one NEVER. That is exact for the
        # feature and wrong for forward drain simulation, which is safe here because `state_from_obs`
        # builds features for the current turn and is never stepped. `unlocked_shops` may name the
        # same shop twice and each instance drains independently, so slots are filled in order
        # rather than deduplicated.
        unlock_day=_unlock_days(obs, memo),
        unlock_shop=_unlock_shops(obs),
        key=__import__("jax").random.PRNGKey(0),
        # All-NEVER without a memo, which is the honest answer: a single observation cannot say what
        # the opponent held on day 3. `jax_obs` reads NEVER as "not decided" and emits zeros, so a
        # caller that does not watch the game gets no snapshot rather than a wrong one.
        opp_snapshot=(memo.opp_snapshot() if memo is not None else jnp.full(
            (1, 2, len(J.SNAPSHOT_DAYS), J.SNAPSHOT_WIDTH), float(J.NEVER), dtype=jnp.float32)),
    )


def agent_private_stub():
    """An empty private dict, for the opponent seat a submission cannot see."""
    return {"shed": {}, "seeds": {}, "inventories": [{}]}
