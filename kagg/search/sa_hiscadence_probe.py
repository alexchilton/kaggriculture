"""DIAGNOSTIC ONLY. Our lawnmower for the work, HIS market cadence verbatim for d4-d10.

The question this answers, and nothing else: do his sweep and his buy/sell cadence work TOGETHER on
our board? If the grid comes right, the pair is proven and the only remaining job is to implement
the cadence properly. If it does not, the planner is what is wrong, not the market code.

d0-d3 and d11+ keep our own market logic, so any change in those columns means the probe leaked.

His cadence is the `orders` field of the derived schedule -- `[hour, op, item, qty]`, read off his
replay. `TAPE_ONLY` strips it before the agent ever sees it, which is why we have never run it.
"""
import collections
import json
import pathlib

from kagg.search import schedule_agent as SA

# breakdown.py reads module-level constants off whatever `--module` names, so mirror the real
# agent's namespace and then shadow `make_agent` below. Nothing here changes the agent itself.
for _n in dir(SA):
    if not _n.startswith("__"):
        globals().setdefault(_n, getattr(SA, _n))

SCHEDULE = pathlib.Path("data/seed_scripts/top_guys/91422988/schedule.json")
FROM_DAY, TO_DAY = 4, 10
TPD = 24


def _cadence():
    """(day, hour) -> [[op, item, qty], ...] exactly as he issued them."""
    raw = json.loads(SCHEDULE.read_text())
    out = collections.defaultdict(list)
    for d, row in raw.items():
        for hour, op, item, qty in (row.get("orders") or []):
            order = [op] if item is None and qty is None else (
                [op] if op == "BUY_LAND" else [op, item, int(qty)])
            out[(int(d), int(hour))].append(order)
    return out


def make_agent(schedule, me=0, router=True):
    inner = SA.make_agent(schedule, me, router=router)
    plan = _cadence()
    turn = {"t": -1}

    def agent(obs, config=None):
        turn["t"] += 1
        act = inner(obs)
        day, hour = divmod(turn["t"], TPD)
        if FROM_DAY <= day <= TO_DAY:
            # Replace the market half wholesale. Unit actions are untouched, so the sweep is ours.
            act = dict(act)
            act["market"] = [list(o) for o in plan.get((day, hour), [])]
        return act

    return agent
