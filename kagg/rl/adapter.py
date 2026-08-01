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


def state_from_obs(obs, privates):
    """Build a batch-of-one `jax_sim.State` from one turn's observation.

    `obs` is the shared observation (`farms`, `market`, `step`); `privates` is a two-element list of
    each player's private dict. A submission only ever sees its *own* private state, so the caller
    supplies a zeroed stand-in for the opponent -- see `agent_private_stub`. The opponent's shed and
    seeds are not visible in the real game either, so the policy is not losing information it would
    otherwise have; it is losing information it was *trained* with, which is a real distribution
    shift and is recorded in the module docstring of `kagg/agents/neural.py`.
    """
    import jax.numpy as jnp

    farms = obs["farms"]
    step = int(obs.get("step", 0))
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
    unit_pos = np.zeros((1, 2, J.MAX_UNITS, 2), dtype=np.int32)
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
        # Not recoverable from the observation and not needed to act from the current position:
        # `unlock_day` only governs future town drain, and the key only seeds weed spawning.
        unlock_day=jnp.full((1, J.N_SHOPS), J.NEVER, dtype=J._I),
        key=__import__("jax").random.PRNGKey(0),
    )


def agent_private_stub():
    """An empty private dict, for the opponent seat a submission cannot see."""
    return {"shed": {}, "seeds": {}, "inventories": [{}]}
