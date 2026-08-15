"""A tour routed to a FERTILIZE stop must be carrying FERTILIZER when it gets there.

`_apply_unit_action` fails FERTILIZE **silently** on an empty hand -- `if not _inv_take(inv,
"FERTILIZER", 1): return` (`kaggriculture.py:465`) -- and `_live_ops` re-derives the work at each
stop, so a unit that arrives without any simply emits nothing and walks on. The stop is planned, the
walk to it is paid for, and the fertilize never happens. Nothing anywhere reports it.

Measured on d16, seed 11, tape `victor`: the node set offers **12** FERTILIZE and the day emits **6**.
Nothing was uncovered and the crew finished with 96 turns of priced slack, so this is not a routing
shortfall -- the tours reached the tiles and had no fertilizer in hand. The dawn draw is the gap: we
PICKUP FERTILIZER twice (h01 u8, h02 u3) against the tape's four (h02 u8/u9/u13, h03 u3), and the
tape emits 13 FERTILIZE that day.

It is worth real money, not just an op count. FERTILIZE sets `fertilized_until_day = day + 2`
(`:468`), which doubles the yield each WATER adds for three days -- so a missed fertilize is not one
op, it is every water on that tile for three days at half value.

Scope note: this asserts the PLAN against ITSELF -- what the router routed against what the day
emitted -- so it cannot be satisfied by lowering the target. Matching the tape's 13 is a separate
question; this only says a stop we chose to walk to must fire.
"""

import collections
import importlib
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

DAY = 16
SEED = 11
TPD = 24


@pytest.fixture(scope="module")
def planned_vs_emitted():
    """`(planned, emitted)` FERTILIZE counts for `DAY`, read off the router and the action stream."""
    import breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    DP = SA.DP

    real_plan = DP.plan
    planned = []

    def spy(units, jobs, budget, *a, **kw):
        out, left = real_plan(units, jobs, budget, *a, **kw)
        planned.append(sum(1 for d in out.values() for st in d["route"]
                           for op, _i in (getattr(st, "ops", None) or ())
                           if op == "FERTILIZE"))
        return out, left

    DP.plan = spy
    try:
        replay, schedule, team = B.TAPES["victor"]
        sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
        thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay) or {}, seed=SEED, weedSpawnChance=0.0),
                   debug=True)
        env.reset(2)
        me = SA.make_agent(thin, 0, router=True)
        them = B.tape_policy(replay, team, 1)

        emitted = collections.Counter()
        for t in range(TPD * (DAY + 1)):
            if t % TPD == 0:
                planned.clear()
            obs = env.state[0].observation
            a0 = me(obs, t)
            if t // TPD == DAY:
                n = len(obs["farms"][0].get("hands") or [])
                for act in [a0["farmer"]] + list(a0["hands"] or [])[:n]:
                    if act and act[0] == "FERTILIZE":
                        emitted["FERTILIZE"] += 1
            env.step([a0, them(env.state[1].observation, t)])
        return (planned[0] if planned else 0), emitted["FERTILIZE"]
    finally:
        DP.plan = real_plan


def test_a_fertilize_stop_is_given_the_fertilizer_it_needs(planned_vs_emitted):
    """Every FERTILIZE the router put in a tour is a turn already paid for. It has to fire."""
    planned, emitted = planned_vs_emitted
    assert emitted >= planned, (
        f"day {DAY}: the router routed {planned} FERTILIZE stops and the day emitted {emitted}. "
        f"The {planned - emitted} that did not fire were reached with an empty hand -- "
        "`_inv_take` returns silently (kaggriculture.py:465) and the walk is spent for nothing.")
