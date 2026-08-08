"""Scratch probe agent for measuring `PRICE_AWARE_SELL_CAP` on pool win rate.

NOT part of the shipped submission. Built to give `kagg.arena.pool.evaluate` a picklable spec that
runs the schedule_agent planner with the flag forced ON, so it can be compared against
`submission/main.py` (flag OFF, the shipped default) under the SAME opponent pool.
`docs/fable_market_selling_2026-08-08.md` records the result; delete this file once that
measurement is captured, per CLAUDE.md's "do not commit" and general repo-hygiene rules.
"""

import json
from pathlib import Path

from kagg.search import schedule_agent as SA

SA.PRICE_AWARE_SELL_CAP = True

_SCHED_PATH = Path(__file__).resolve().parents[2] / "data/seed_scripts/top_guys/90976060/schedule.json"
_SCHED = {int(k): v for k, v in json.loads(_SCHED_PATH.read_text()).items()}
_AGENTS = {}


def agent(obs, config=None):
    me = int(obs.get("player", 0) or 0)
    fresh = int(obs.get("day", 0) or 0) == 0 and int(obs.get("hour", 0) or 0) == 0
    if fresh or me not in _AGENTS:
        _AGENTS[me] = SA.make_agent(_SCHED, me, router=True)
    return _AGENTS[me](obs, config)
