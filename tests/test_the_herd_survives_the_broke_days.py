"""The feed reserve must survive the harvest that discharges it.

## The chain, measured on Seb's 1.32.6 schedule, seed 11, weeds off

    d4   buy the $1,000 parcel                        -> d5 dawn broke
    d5   spend the remainder on 15 seeds              -> d6 dawn $46
    d6   `short = min(short, money * 0.5 // quote)` = 23 // 30 = 0   -- buys NO wheat
         sh:wheat 0, so no PICKUP is possible and FEED cannot fire
    d7   feed 0/3   care 0/3   pickup 0/3
         `consecutive_unfed >= 2` (`kaggriculture.py:786`) evicts
    cow  5 -> 4 -> 3

The tape crosses the same two broke days -- its own d5 bank ends at $0 -- and loses nothing,
because it is holding a reserve: `sh:wheat 7/7/7/7/7` across d4 to d8, bought on d3 and never sold.

## The defect

`schedule_agent.py:2032` nets the reserve down by `ripe_wheat`:

    have = max(0, have - max(0, feed_days(day) * alive
                             - ripe_wheat - carried_wheat - drawn - will_buy))

`ripe_wheat` is wheat STANDING IN THE FIELD, and the note defending it says "fourteen ripe tiles
feed the herd perfectly well". That is true of the day it is measured on and false of the day after,
because day 4 is the day the field is harvested: wheat tiles run 14 -> 3. The stock that cancels the
reserve is the same stock the sell order then ships. The reserve covers `feed_days(day)` days; the
offset is only good for one of them.

## What this test asserts

Not a mechanism -- an outcome. The herd does not shrink while crossing the broke days, and the shed
is not empty at the dawn on which the bank cannot buy its way out. Either a deeper reserve, a
different sell row or an earlier purchase would satisfy it; the test does not care which.

## What it deliberately does NOT assert

That the d4 parcel still lands. `test_a_short_day_banks_the_hand_before_it_works` owns that, and
the two pull in opposite directions on purpose -- selling less wheat on d4 is exactly what would
cost the parcel. Both must be green at once or the change has just moved the problem.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

THROUGH = 8


@pytest.fixture(scope="module")
def season():
    """Play days 0..THROUGH and report the herd and the shed at each dawn."""
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb1326"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    dawn = {}
    for t in range(24 * (THROUGH + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t % 24 == 0:
            priv = o0.get("private") or {}
            dawn[t // 24] = {
                "shed": collections.Counter(priv.get("shed") or {}),
                "herd": sum(1 for row in o0["farms"][0]["tiles"] for c in row
                            if isinstance(c, dict) and c.get("animal")),
            }
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return dawn


@pytest.mark.slow
def test_the_herd_does_not_shrink_across_the_broke_days(season):
    """The whole thing. An animal lost to hunger is a $400-$500 write-off plus its whole season."""
    peak, worst, day = 0, None, None
    for d in range(THROUGH + 1):
        peak = max(peak, season[d]["herd"])
        if worst is None or season[d]["herd"] - peak < worst:
            worst, day = season[d]["herd"] - peak, d
    assert worst >= 0, (
        f"the herd fell {-worst} below its own peak by day {day}. "
        "Animals are evicted at `consecutive_unfed >= 2`, so this is starvation, not sale.\n    "
        + "  ".join(f"d{d}:{season[d]['herd']}" for d in range(THROUGH + 1)))


@pytest.mark.slow
def test_the_shed_is_not_empty_on_the_dawn_the_bank_cannot_rescue(season):
    """Day 6 opens at about $46. With an empty shed there is no recovery available that day."""
    have = season[6]["shed"].get("WHEAT", 0)
    assert have > 0, (
        "day 6 opens with an empty shed and a bank too thin to buy "
        "(`short = min(short, money * 0.5 // quote)` rounds to zero), so no animal can be fed.\n    "
        + "  ".join(f"d{d}:{season[d]['shed'].get('WHEAT', 0)}" for d in range(THROUGH + 1)))
