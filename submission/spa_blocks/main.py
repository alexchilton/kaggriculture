"""Splice SpaTaro's nearest day-block when the board is one he has played; else PASS.

Exact matching is dead: his 62 day-blocks are all distinct on every day even after the
jitter is stripped (no quantities, no malformed orders, hands sorted, movement dropped --
`scripts/dejitter_blocks.py`). So the block is chosen by nearest board at dawn and
committed for the day, and the point of this rig is to measure how much of a borrowed day
actually LANDS rather than whether it is identical to anything.

PASS is the fallback here on purpose -- it isolates the splice. The planner goes in only
once the landing rate says a borrowed day is worth executing at all.
"""
import json, os, sys
from pathlib import Path


def _here():
    f = globals().get("__file__") or _here.__code__.co_filename
    return Path(f).resolve().parent


_root = _here()
_LIB = json.loads((_root / "spataro_blocks.json").read_text())
_COLS, _SCALE, _DAYS = _LIB["columns"], _LIB["scale"], _LIB["days"]
EXCLUDE_GAME = os.environ.get("SPA_EXCLUDE", "")
MAX_DIST = float(os.environ.get("SPA_MAX_DIST", "0.5"))
_CHOSEN, _REPORT = {}, {"spliced": 0, "passed": 0, "dists": []}


def _features(obs, me):
    farm = obs["farms"][me]
    crops, animals = {}, {}
    empty = weeds = thirsty = 0
    for row in farm["tiles"]:
        for t in row:
            if t is None:
                empty += 1
            elif isinstance(t, dict):
                if t.get("animal"):
                    animals[t["animal"]] = animals.get(t["animal"], 0) + 1
                elif t.get("kind") == "PLANT" and t.get("crop"):
                    crops[t["crop"]] = crops.get(t["crop"], 0) + 1
                    if not t.get("watered_today"):
                        thirsty += 1
                elif t.get("kind") == "WEED":
                    weeds += 1
    x = {f"my_crop_{c}": crops.get(c, 0)
         for c in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")}
    x.update({f"my_animal_{a}": animals.get(a, 0) for a in ("COW", "SHEEP", "GOOSE")})
    x["my_empty"] = empty
    x["my_weeds"] = weeds
    x["my_thirsty"] = thirsty
    x["my_hands"] = len(farm["hands"])
    x["my_quadrants"] = len(farm["unlocked_quadrants"])
    for c in ("WHEAT", "MELON", "STRAWBERRY", "CARROT"):
        x[f"my_seed_{c}"] = obs["private"]["seeds"].get(c, 0)
    for p in ("WHEAT", "FERTILIZER"):
        x[f"my_shed_{p}"] = obs["private"]["shed"].get(p, 0)
    return x


def agent(observation, configuration=None):
    me = int(observation.get("player", 0) or 0)
    step, day, hour = int(observation["step"]), int(observation["day"]), int(observation["hour"])
    key = (me, day)
    if hour == 0 or key not in _CHOSEN:
        cands = _DAYS.get(str(day)) or []
        x = _features(observation, me)
        best, bd = None, None
        for c in cands:
            d = sum(abs(x.get(k, 0) - c["x"].get(k, 0)) / _SCALE[k] for k in _COLS) / len(_COLS)
            if bd is None or d < bd:
                best, bd = c, d
        _CHOSEN[key] = (best, bd) if best is not None and bd is not None and bd <= MAX_DIST else (None, bd)
        if bd is not None:
            _REPORT["dists"].append(round(bd, 3))
    block, _ = _CHOSEN[key]
    if block is None:
        _REPORT["passed"] += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}
    _REPORT["spliced"] += 1
    a = block["block"][min(hour, len(block["block"]) - 1)] or {}
    owned = len(observation["farms"][me]["hands"])
    return {"farmer": list(a.get("farmer") or ["PASS"]),
            "hands": [list(h) for h in (a.get("hands") or [])[:owned]],
            "market": [list(o) for o in (a.get("market") or [])]}


agent.telemetry = _REPORT
