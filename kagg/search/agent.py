"""Driving a searched plan inside the real `kaggle_environments` environment.

The point of this module is that it contains **no** decision logic. It converts one observation
dict into the same :class:`~kagg.search.executor.View` the batched simulator produces, calls the
same `decide`, and converts the result back into the action dict the environment wants. If the
searched behaviour and the played behaviour ever disagree, it is a bug here or a genuine
simulator divergence -- never a second copy of the strategy that drifted.

The emitted market order list is a **fixed 8-slot layout**, padded with ``["SELL", crop, 0]``
where a slot is unused. `_parse_order` rejects a zero quantity while the slot itself still lines
up, which is what makes the reference's slot-paired settlement agree with the simulator's
product-paired settlement. See `kagg.search.executor` for why that matters.
"""

import json
import os
from pathlib import Path

import numpy as np

from kagg.search import executor as X
from kagg.search.plan import CROP_NAMES, N_CROPS, decode

DEFAULT_PLAN = Path(__file__).with_name("best_plan.json")


def plan_path():
    """Which plan file `agent` plays.

    Overridable by ``KAGG_SEARCH_PLAN`` so that a plan can be measured in the arena without
    overwriting the saved one. The environment variable is read per call rather than cached
    because the arena runs matches in freshly spawned worker processes.
    """
    return Path(os.environ.get("KAGG_SEARCH_PLAN", DEFAULT_PLAN))

OP_NAMES = {
    0: "PASS", 1: "NORTH", 2: "SOUTH", 3: "EAST", 4: "WEST",
    5: "WATER", 6: "HARVEST", 8: "DIG",
}
PLANT_OP = 7

_KIND = {"WEED": X.WEED, "PLANT": X.PLANT, "COOP": X.COOP, "PASTURE": X.PASTURE}


def observation_view(obs):
    """Build a batch-of-one View from a live observation."""
    me = obs.get("player", 0)
    farm = obs["farms"][me]
    private = obs.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    seeds = private.get("seeds", {}) or {}
    prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
    board = farm["tiles"]

    kind = np.zeros((1, X.TILES), dtype=np.int64)
    crop = np.full((1, X.TILES), -1, dtype=np.int64)
    planted = np.zeros((1, X.TILES), dtype=np.int64)
    watered = np.zeros((1, X.TILES), dtype=bool)
    units = np.zeros((1, X.TILES), dtype=np.int64)

    for i, (x, y) in enumerate(X.ORDER):
        cell = board[y][x]
        if cell == "LOCKED":
            kind[0, i] = X.LOCKED
            continue
        if cell is None:
            kind[0, i] = X.EMPTY
            continue
        kind[0, i] = _KIND.get(cell.get("kind"), X.EMPTY)
        if cell.get("kind") == "PLANT":
            crop[0, i] = CROP_NAMES.index(cell["crop"])
            planted[0, i] = cell.get("planted_day", 0)
            watered[0, i] = bool(cell.get("watered_today"))
        units[0, i] = cell.get("yield_units", 0)

    positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm.get("hands", [])]
    unit_ord = np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64)
    for u, (x, y) in enumerate(positions[: X.MAX_EXEC_UNITS]):
        unit_ord[0, u] = X.ORD_OF_TILE[y * X.BOARD + x]

    return X.View(
        day=int(obs.get("day", 0)),
        hour=int(obs.get("hour", 0)),
        kind=kind,
        crop=crop,
        planted_day=planted,
        watered=watered,
        yield_units=units,
        unit_ord=unit_ord,
        n_units=np.array([min(len(positions), X.MAX_EXEC_UNITS)]),
        money=np.array([float(farm["money"])]),
        seeds=np.array([[int(seeds.get(c, 0)) for c in CROP_NAMES]]),
        shed=np.array([[int(shed.get(c, 0)) for c in CROP_NAMES]]),
        prices=np.array([[int(prices.get(c, 0)) for c in CROP_NAMES]]),
        n_land=np.array([len(farm.get("unlocked_quadrants", ["NW"])) - 1]),
    )


def _unit_action(op, crop):
    if op == PLANT_OP:
        return ["PLANT", CROP_NAMES[int(crop)]]
    return [OP_NAMES.get(int(op), "PASS")]


def to_action(obs, decision, n_units):
    """Turn one game's Decision into the environment's action dict."""
    hour = int(obs.get("hour", 0))
    units = [_unit_action(decision.unit_op[0, u], decision.unit_crop[0, u])
             for u in range(n_units)]

    market = [["SELL", CROP_NAMES[c], int(decision.sell[0, c])] for c in range(N_CROPS)]
    buying = hour % N_CROPS
    market.append(["BUY_SEED", CROP_NAMES[buying], int(decision.buy_seed[0, buying])])
    market.append(["HIRE"] if bool(decision.hire[0]) else ["SELL", CROP_NAMES[0], 0])
    market.append(["BUY_LAND"] if bool(decision.buy_land[0]) else ["SELL", CROP_NAMES[0], 0])

    return {"farmer": units[0], "hands": units[1:], "market": market}


def make_agent(genome):
    """An agent closure bound to one genome."""
    plan = decode(np.asarray(genome)[None, :])

    def _agent(obs, config=None):
        view = observation_view(obs)
        decision = X.decide(view, plan)
        return to_action(obs, decision, int(view.n_units[0]))

    return _agent


def load_best(path=None):
    with open(path or plan_path()) as handle:
        return np.array(json.load(handle)["genome"], dtype=np.int64)


def save_best(genome, meta=None, path=None):
    payload = {"genome": [int(v) for v in genome]}
    payload.update(meta or {})
    with open(path or plan_path(), "w") as handle:
        json.dump(payload, handle, indent=1)


_AGENT = None
_AGENT_PATH = None


def agent(obs, config=None):
    """Module entry point, so the searched plan can be used as a pool spec or submitted."""
    global _AGENT, _AGENT_PATH
    path = plan_path()
    if _AGENT is None or _AGENT_PATH != path:
        _AGENT, _AGENT_PATH = make_agent(load_best(path)), path
    return _AGENT(obs, config)
