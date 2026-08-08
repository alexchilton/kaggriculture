"""We sell the herd's wheat while the herd stands unfed, and the animals are evicted for it.

## The trace, seed 11, weeds off, the shipped configuration

    d11 h0   14 animals, 14 UNFED, shed wheat 14   ->  SELL WHEAT 7
    d11 h2   money 66,  shed wheat 0
    d11 h3   money 6                               ->  BUY_SEED WHEAT 2
    d11 h4..h14   money 6, shed wheat 0, the same order re-offered twelve hours running
             FEED fires exactly twice in twenty-four hours
    d12 h0   16 animals -> 14

`consecutive_unfed >= 2` removes the animal outright (`kaggriculture.py:786`). FEED is the highest
priority op the router has (`RANK: FEED=0`); it did not fire because it *could not* -- feeding needs
wheat in a hand, a hand draws from the shed, and the shed was empty from hour 2 because we sold it.

Across the season this is not marginal: we finish on 7 cows against the tape's 13, and MILK was the
one product whose price never dropped below base all season.

## The defect

`schedule_agent.py`, the WHEAT branch of the sell block:

    have = max(0, have - max(0, feed_days(day) * alive
                             - ripe_wheat - carried_wheat - drawn - will_buy))

`ripe_wheat` is wheat STANDING IN THE FIELD. It is subtracted from the herd's requirement as though
it were feed in hand, so a field full of unharvested wheat cancels the reserve and the shed's real
stock goes to market. The note defending it says "fourteen ripe tiles feed the herd perfectly well",
which is true only if those tiles are harvested, carried and dropped before the animals go hungry --
and on day 11 none of that happens, because the crew spends the day planting.

`tests/test_the_herd_survives_the_broke_days.py` documents the same offset failing at the other end
of the season, on day 4. This test covers the window that one deliberately does not.

## What this asserts

An outcome, not a mechanism: crossing the days after the crew is at full size, the herd must not
shrink. It does not care whether the fix is a deeper reserve, an earlier harvest or a different sell
row.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

THROUGH = 13


@pytest.fixture(scope="module")
def season():
    """Our own agent, whole season from day 0 -- this is what ships, not the handover fixture."""
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
            cells = [c for r in o0["farms"][0]["tiles"] for c in r if isinstance(c, dict)]
            dawn[t // 24] = {
                "herd": sum(1 for c in cells if c.get("animal")),
                "unfed": sum(1 for c in cells if c.get("animal") and not c.get("fed_today")),
                "wheat": collections.Counter(priv.get("shed") or {}).get("WHEAT", 0),
            }
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return dawn


@pytest.mark.slow
def test_the_herd_never_shrinks(season):
    """The whole thing. An animal lost to hunger is a $400-$500 write-off plus its whole season."""
    peak, worst, day = 0, 0, None
    for d in range(THROUGH + 1):
        peak = max(peak, season[d]["herd"])
        if season[d]["herd"] - peak < worst:
            worst, day = season[d]["herd"] - peak, d
    assert worst >= 0, (
        f"the herd fell {-worst} below its own peak by day {day} -- evicted at "
        f"`consecutive_unfed >= 2`, not sold.\n    herd  "
        + "  ".join(f"d{d}:{season[d]['herd']}" for d in range(THROUGH + 1))
        + "\n    wheat " + "  ".join(f"d{d}:{season[d]['wheat']}" for d in range(THROUGH + 1)))
