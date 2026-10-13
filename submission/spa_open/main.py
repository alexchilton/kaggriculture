"""SpaTaro-geometry opening for days 0-6, then PASS. Measurement rig, not a submission."""
import importlib.util, sys
from pathlib import Path


def _source_directory():
    # kaggle_environments execs this source without __file__ defined.
    filename = globals().get("__file__") or _source_directory.__code__.co_filename
    return Path(filename).resolve().parent


_root = _source_directory()
_spec = importlib.util.spec_from_file_location("spa_opening", _root / "spa_opening.py")
_m = importlib.util.module_from_spec(_spec)
sys.modules["spa_opening"] = _m
_spec.loader.exec_module(_m)


def agent(observation, configuration=None):
    me = int(observation["player"])
    if int(observation["day"]) > 6:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    return _m.agent_action(observation, me)
