"""The morning's hire drip must not re-solve the whole day three times.

## The bug

`_router_acts` triggers a FULL replan whenever the crew size changes:

    if state["crew"] != len(live) or not routes:
        sub = _solve([units[u] for u in live], nodes_for(set()), ...)

and hires do not all land at once. `schedule_agent.py:782` records the shape: the money drip
"lands hires 5 / 1 / 1 across hours 0, 1 and 2". So a day that ends with N hands solves the
entire board for 5 units at hour 0, again for 6 at hour 1, and again for 7 at hour 2 -- three
full solves for one day's work, the last two differing from the first by one vehicle.

Nothing was wrong with the plans, so this never showed up as a wrong action. It showed up as a
disqualification. Episode 91023699, submission 55352401, seat 0:

    482 turns played of 719, then TIMEOUT
    419 turns cost ~0s, 36 under 0.5s, 5 between 0.5s and 1s
    22 turns cost more than 1s -- TWELVE at hour 1 and TEN at hour 2, and nothing anywhere else
    overage charged: 30.8s at hour 1 + 30.8s at hour 2 = 61.7s against a 60s bank

`actTimeout` is 1s and `remainingOverageTime` is a 60s bank for the whole episode; the agent is
disqualified the moment it goes negative. It went negative on day 20 and the episode scored
nothing. Every second of that came from re-solving the morning.

The local gate missed it because this machine runs the same solve in 1.3-2.0s where the Kaggle
worker takes 5.0-7.4s. Locally the same season charges 2.7s of overage. The 1s threshold sits
inside our distribution, so a ~3.8x slower box does not cost 3.8x -- it drags a whole cohort of
sub-second turns over the line and costs 22x.

## The fix

A new hand is idle by definition, and `_router_acts` ALREADY has machinery for giving work to an
idle unit without disturbing anyone else -- `nodes_for(busy)` excludes tiles the committed tours
have claimed, and the solve runs over the idle units alone. The crew-change branch bypasses that
and rebuilds everything.

This is the same argument the file already makes one branch lower, about urgent work:

    **Fresh urgent work is an INSERTION, not a rebuild.** Rerunning the whole plan every time a
    PLACE node appeared MEASURED as day 0 `place` 4/4 -> 3/4 and `build_pasture` 8/8 -> 7/8

## What this test does NOT claim

It does not claim the insertion plans as well as the rebuild. A rebuild can move work between all
N vehicles; an insertion can only hand the newcomer what is left. That is a real trade and it is
measured on the season, not here. This test pins the COST -- that one day is solved once at full
width -- and the money is a separate, explicit measurement.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA


@pytest.fixture
def tape():
    from scripts.breakdown import TAPES, TAPE_ONLY

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    return replay, thin, team


def _play(tape, days, monkeypatch):
    """Play `days` days and record the width of every `_solve` call, keyed by (day, hour)."""
    from kaggle_environments import make

    from scripts.breakdown import tape_policy

    replay, thin, team = tape
    calls = []
    real = SA._solve

    def spy(units, nodes, budget, *a, **kw):
        # Width alone is the wrong measure. A seven-unit solve at hour 23 has one turn of budget
        # and costs nothing; a seven-unit solve at hour 1 plans a whole day and is what the Kaggle
        # log charges for. Record both, and let the assertions ask for the product.
        calls.append({"units": len(units), "budget": max(budget) if budget else 0,
                      "nodes": len(nodes)})
        return real(units, nodes, budget, *a, **kw)

    monkeypatch.setattr(SA, "_solve", spy)

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)
    per_turn = []
    for t in range(24 * days):
        o0, o1 = env.state[0].observation, env.state[1].observation
        before = len(calls)
        a0 = ours(o0)
        for c in calls[before:]:
            c["day"], c["hour"] = t // 24, t % 24
        per_turn.append(len(calls) - before)
        a1 = opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return calls


#: A solve is "expensive" when it is both wide and facing most of a day. Those two together are
#: what the Kaggle log charged for: every turn over a second was at hour 1 or hour 2, where the
#: crew is already 5-7 hands and the budget is still 21-23 turns. The same widths at hour 20 cost
#: nothing measurable, because there is almost no day left to plan into.
WIDE, LONG = 4, 18


def _expensive(calls):
    return [c for c in calls if c["units"] >= WIDE and c["budget"] >= LONG]


@pytest.mark.slow
def test_a_whole_day_is_planned_for_the_whole_crew_only_once(tape, monkeypatch):
    """The assertion the timeout rests on.

    One full-width, full-day solve is the plan. Three is the morning being re-planned as each
    hire lands, and it is what spent the 60s bank on the ladder.
    """
    calls = _play(tape, days=8, monkeypatch=monkeypatch)
    per_day = collections.Counter(c["day"] for c in _expensive(calls))
    worst = max(per_day.values(), default=0)
    assert worst <= 1, (
        f"a whole day is planned for the whole crew {worst} times on one day; "
        f"per day: {dict(sorted(per_day.items()))}\n    the expensive solves: "
        + ", ".join(f"d{c['day']}h{c['hour']}:{c['units']}u/{c['budget']}t"
                    for c in _expensive(calls)[:16]))


@pytest.mark.slow
def test_the_expensive_solves_do_not_land_in_the_morning_hire_drip(tape, monkeypatch):
    """Locate the cost, so a fix that MOVES it rather than removing it cannot pass.

    The Kaggle log charges 30.8s at hour 1 and 30.8s at hour 2, and nothing at any other hour.
    Hour 0 is exempt: the day has to be planned once, and at hour 0 the crew is still tiny.
    """
    calls = _play(tape, days=8, monkeypatch=monkeypatch)
    by_hour = collections.Counter(c["hour"] for c in _expensive(calls))
    assert not (by_hour[1] or by_hour[2]), (
        f"expensive solves still land in the morning drip: hour1={by_hour[1]}, "
        f"hour2={by_hour[2]}; full histogram {dict(sorted(by_hour.items()))}")
