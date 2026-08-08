"""The metric, stated exactly: a crop that weeded WHILE IT WAS STILL IN THE JOB LIST.

Counting weed TILES stopped meaning anything the moment two rules landed that manufacture them on
purpose. `LATE_SEASON_TRIAGE` abandons a crop that cannot produce again before day 29, so it weeds --
that is the rule working. `DIG_ONLY_IF_REPLANTING` leaves weeds standing on ground we will never
replant, so they are still there to be counted at dusk on day 29 -- also the rule working. The tape
does both: its final board carries 42 weed tiles against our 8, and it banks more than we do.

Measured over six seasons the raw count went from 55 under the old planner to 126 under this one, and
reading that as "we kill twice as many crops" would have been wrong in a way that is very hard to see.

So the metric is UNINTENTIONAL weeds: at each dawn `schedule_agent._pointless_tiles` says which
ground the plan has written off, and a tile that dies while it is NOT in that set is a crop we meant
to keep and lost. That is the number to drive to zero, and unlike the raw count it cannot be gamed by
abandoning more ground.

This is a gate, not a report -- it fails when a real crop is lost, and says nothing about how much
ground we walked away from on purpose.
"""
import collections
import json
import pathlib

import pytest

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

pytestmark = pytest.mark.slow

#: Losing nothing at all is the goal. This is the ratchet: it may come down, never up.
BUDGET = 12


def _unintentional(seed=11, days=30):
    """(day, tile, crop) for every tile that weeded while the plan still wanted it."""
    from kaggle_environments import make

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    lost, watched = [], {}
    for t in range(24 * days - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // 24, t % 24
        if hour == 0:
            tiles = o0["farms"][0]["tiles"]
            # What did the plan still want at dawn? Everything the schedule has not written off.
            plants_left = any((thin.get(d, {}) or {}).get("plants")
                              for d in range(day, SA.LAST_DAY + 1))
            written_off = SA._pointless_tiles(tiles, day, plants_left)
            for (x, y), crop in list(watched.items()):
                cell = tiles[y][x]
                if isinstance(cell, dict) and cell.get("kind") == "WEED":
                    lost.append((day, (x, y), crop))
            watched = {(x, y): c.get("crop")
                       for y, r in enumerate(tiles) for x, c in enumerate(r)
                       if isinstance(c, dict) and c.get("kind") == "PLANT"
                       and (x, y) not in written_off}
        a0, a1 = agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    return lost


def test_no_crop_we_still_wanted_is_lost_to_thirst():
    """Every tile here was offered as work at dawn and was a WEED by the next one."""
    lost = _unintentional()
    by_day = collections.Counter(d for d, _t, _c in lost)
    by_crop = collections.Counter(c for _d, _t, c in lost)
    assert len(lost) <= BUDGET, (
        f"{len(lost)} crops died while the plan still wanted them (budget {BUDGET}).\n"
        f"  by day:  {dict(sorted(by_day.items()))}\n"
        f"  by crop: {dict(by_crop)}\n"
        f"  first six: {lost[:6]}\n"
        "These are NOT the tiles `_pointless_tiles` wrote off -- those are meant to die and are "
        "excluded. Every one of these is a tile we were still spending turns on.")


def test_the_metric_excludes_ground_we_walked_away_from_on_purpose():
    """The guard that keeps the number honest.

    If this counted every weed it would rise whenever `LATE_SEASON_TRIAGE` or
    `DIG_ONLY_IF_REPLANTING` did their job, and driving it down would mean abandoning less ground --
    the exact opposite of what those rules are for. So the exclusion has to actually exclude
    something, or the metric has silently become the raw count again.
    """
    from kaggle_environments import make

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)
    seen = 0
    for t in range(24 * 26 - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t % 24 == 0:
            tiles = o0["farms"][0]["tiles"]
            plants_left = any((thin.get(d, {}) or {}).get("plants")
                              for d in range(t // 24, SA.LAST_DAY + 1))
            seen = max(seen, len(SA._pointless_tiles(tiles, t // 24, plants_left)))
        a0, a1 = agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    assert seen > 0, (
        "`_pointless_tiles` never wrote off a single tile in 26 days, so the test above is counting "
        "every weed and the exclusion is doing nothing. Check LATE_SEASON_TRIAGE is on.")
