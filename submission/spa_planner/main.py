"""SpaTaro's days 0-6 verbatim, then our planner continues from the board he left.

Why this is not the splice that scored -167,577: that one handed turn 168 to
Hayashi's TAPE, which replays commands written for the farm his own opening built --
it watered tiles with no crop and sold stock that was not in the shed. The planner
reads the board every turn (see `kagg/search/schedule_agent.py`), so it cannot
mismatch the state it inherits. The prefix is the same idea; the continuation is the
part that has to be reactive.

The schedule is SpaTaro's own per-day flows, median over his seasons in this branch
(`scripts/spataro_schedule.py`), so the planner is asked for his shape rather than
its own.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

SPLIT = 168                      # end of day 6


def _here():
    filename = globals().get("__file__") or _here.__code__.co_filename
    return Path(filename).resolve().parent


_root = _here()
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

_OPENING = json.loads((_root / "opening.json").read_text())

_spec = importlib.util.spec_from_file_location(
    "spa_sched_agent", _root / "kagg" / "search" / "schedule_agent.py")
_sa = importlib.util.module_from_spec(_spec)
sys.modules["spa_sched_agent"] = _sa
_spec.loader.exec_module(_sa)

_SCHEDULES = {
    branch: json.loads((_root / f"schedule_{branch}.json").read_text())
    for branch in ("yarn", "non_yarn")
}
_PLANNERS = {}
_BRANCH = {}


def _branch_for(obs):
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    return "yarn" if "YARN_STORE" in shops[:2] else "non_yarn"


def agent(observation, configuration=None):
    me = int(observation.get("player", 0) or 0)
    step = int(observation["step"])

    if step < SPLIT:
        a = _OPENING[step] or {}
        owned = len((observation.get("farms") or [{}, {}])[me].get("hands") or [])
        return {"farmer": list(a.get("farmer") or ["PASS"]),
                "hands": [list(h) for h in (a.get("hands") or [])[:owned]],
                "market": [list(o) for o in (a.get("market") or [])]}

    # The branch is read once, at the handover, from the town as it stands then.
    if me not in _BRANCH:
        _BRANCH[me] = _branch_for(observation)
    key = (me, _BRANCH[me])
    if key not in _PLANNERS:
        _PLANNERS[key] = _sa.make_agent(_SCHEDULES[_BRANCH[me]], me=me, router=True)
    return _PLANNERS[key](observation, configuration)
