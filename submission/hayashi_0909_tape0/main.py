"""Replay one fixed tape verbatim. Used to price a single tape edit."""
import json
from pathlib import Path
_F = Path(__file__).resolve().parent if "__file__" in globals() else Path((lambda: None).__code__.co_filename).resolve().parent
_T = json.loads((_F / "tape.json").read_text())
def agent(observation, configuration=None):
    step = int(observation["step"])
    if step >= len(_T): return {"farmer": ["PASS"], "hands": [], "market": []}
    a = _T[step] or {}
    me = int(observation.get("player", 0) or 0)
    owned = len((observation.get("farms") or [{}, {}])[me].get("hands") or [])
    return {"farmer": list(a.get("farmer") or ["PASS"]),
            "hands": [list(h) for h in (a.get("hands") or [])[:owned]],
            "market": [list(o) for o in (a.get("market") or [])]}
