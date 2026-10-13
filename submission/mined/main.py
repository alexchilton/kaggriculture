"""Replay one mined stream verbatim. No routing, no repairs -- the null model.

This exists to answer one question: does a top agent's recorded season still bank
when it is replayed blind? Those agents re-decide every turn against the opponent
in front of them, so a recording is a best response to a board that will not be
there next time. If a replayed stream holds up, mining tapes from the top of the
ladder is a live idea. If it collapses, it is not.

The stream file is chosen by MINED_STREAM below.
"""
import json
import os
from pathlib import Path

_FOLDER = Path(__file__).resolve().parent if "__file__" in globals() else Path(
    (lambda: None).__code__.co_filename).resolve().parent
MINED_STREAM = os.environ.get("MINED_STREAM", "SpaTaro_best.json")
_TAPE = json.loads((_FOLDER / MINED_STREAM).read_text())


def agent(observation, configuration=None):
    step = int(observation["step"])
    if step >= len(_TAPE):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    a = _TAPE[step] or {}
    me = int(observation.get("player", 0) or 0)
    # Sending more hand actions than we own blocks plants no real agent could block:
    # the reference ignores a surplus unit action for work but still counts it in the
    # atomic-PLANT rule.
    owned = len((observation.get("farms") or [{}, {}])[me].get("hands") or [])
    return {"farmer": list(a.get("farmer") or ["PASS"]),
            "hands": [list(h) for h in (a.get("hands") or [])[:owned]],
            "market": [list(o) for o in (a.get("market") or [])]}
