"""Scratch baseline agent, paired with `_price_aware_probe.py` -- same schedule, flag OFF.

Exists so the arena comparison is apples to apples against the exact same `schedule_agent.py`
source (the `submission/main.py` build gate is currently failing for an unrelated reason -- a
concurrent change to this file moved the tape-fidelity number its hard-coded assertion checks --
so this sidesteps rebuilding the bundle just to measure one flag). Delete alongside the probe once
the measurement in `docs/fable_market_selling_2026-08-08.md` is captured.
"""

import json
from pathlib import Path

from kagg.search import schedule_agent as SA

SA.PRICE_AWARE_SELL_CAP = False

_SCHED_PATH = Path(__file__).resolve().parents[2] / "data/seed_scripts/top_guys/90976060/schedule.json"
_SCHED = {int(k): v for k, v in json.loads(_SCHED_PATH.read_text()).items()}
_AGENTS = {}


def agent(obs, config=None):
    me = int(obs.get("player", 0) or 0)
    fresh = int(obs.get("day", 0) or 0) == 0 and int(obs.get("hour", 0) or 0) == 0
    if fresh or me not in _AGENTS:
        _AGENTS[me] = SA.make_agent(_SCHED, me, router=True)
    return _AGENTS[me](obs, config)
