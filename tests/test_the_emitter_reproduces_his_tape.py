"""Schedule in, tape out. The emitter's contract, written against his tape and nothing else.

Every other test in this project asserts a property of our own code, which is how the suite stayed
green while the farm banked $22k against his $141k. This file asserts one thing: **given his
schedule, our emitter must produce his tape.** Both sides are counted off
`data/seed_scripts/new_leader/90016067.json` -- there is no inference and no target I chose.

His tape, censused (`scripts/measure_his_op_budget.py`):

    op                    count     share
    NORTH/WEST/SOUTH/EAST 4,120     56.4%      walk
    WATER                   851     11.6%
    PICKUP                  339      4.6%
    HARVEST                 338      4.6%
    FEED                    319      4.3%
    COLLECT_FERTILIZER      318      4.3%
    CARE                    308      4.2%
    PLANT                   131      1.8%
    FERTILIZE               107      1.5%
    DROP                     80      1.1%
    PLACE                    27      0.4%
    DIG                      25      0.3%
    BUILD_PASTURE            14      0.2%
    PASS                    357      4.9%      <- he idles 5% of the season

Ours at the same schedule, before this file existed:

    HARVEST  607 (+269)   WATER 618 (-233)   PICKUP 187 (-152)   FEED 173 (-146)
    FERTILIZE  0 (-107)   PLANT  98 (-33)    DROP    0 (-80)

Two facts from that census have to be read together, because on their own each one points at the
wrong fix:

  - **We leave 6-11 of 23 work turns idle per hand per day** -- 11.5/hand on day 3 against his 17.7.
  - **We refuse 12 of his plantings anyway**, including all 31 tiles of his day-26 second wave.

Idle capacity and refused work at the same time is not a capacity problem. It is an *assignment*
problem: `grow()` and `ranch()` reserve a unit for one job for the whole season, so a hand with 11
free turns on day 4 still refuses the day-4 job because its day-20 is full. Measured directly
(`scripts/measure_refusal_day.py`): of the twelve refusals exactly one is a turn-claim failure, on
day 12, with **205 free turns sitting unused across the crew that same day**. The other eleven are
`cluster()` running out of contiguous ground, because a chain owns its tiles for the season and
never gives them back -- while his 131 plantings run over ~61 tiles, replanting each one as it
clears.

So the fix is not a bigger crew, a different mix, or a better search. It is that the emitter must
assign **ops to hands per day** instead of jobs to hands per season. These tests are the contract for
that, and they are meant to be red until it exists.
"""

import collections
import json
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"
TD = 24
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


# --------------------------------------------------------------------------- his tape, counted
@pytest.fixture(scope="module")
def his():
    """His op census, read off the replay. Nothing here is a target I picked."""
    if not REPLAY.exists():
        pytest.skip(f"{REPLAY} missing")
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    hist = collections.Counter()
    per_day = collections.defaultdict(collections.Counter)
    hands = {}
    for t, step in enumerate(d["steps"]):
        day = t // TD
        s = step[seat] or {}
        farms = (s.get("observation") or {}).get("farms") or []
        if len(farms) > seat:
            hands[day] = max(hands.get(day, 0), len(farms[seat].get("hands") or []) + 1)
        act = s.get("action") or {}
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if not op:
                continue
            hist[op[0]] += 1
            per_day[day][op[0]] += 1
    return dict(hist=hist, per_day=per_day, hands=hands)


@pytest.fixture(scope="module")
def schedule():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    return {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}


# --------------------------------------------------------------------------- ours, same schedule
@pytest.fixture(scope="module")
def ours(schedule):
    """His schedule through our emitter, censused identically. A failure here is the emitter's."""
    from kagg.search import dayplan

    script, report = dayplan.emit(schedule)
    names = {v: k for k, v in R.OP.items()}
    hist = collections.Counter()
    per_day = collections.defaultdict(collections.Counter)
    busy = collections.defaultdict(set)
    op = np.asarray(script.unit_op)
    for t in range(op.shape[0]):
        day = t // R.TURNS_PER_DAY
        for u in range(op.shape[1]):
            nm = names.get(int(op[t, u]), "PASS")
            hist[nm] += 1
            per_day[day][nm] += 1
            if nm != "PASS":
                busy[day].add(u)
    return dict(script=script, report=report, hist=hist, per_day=per_day,
                hands={d: len(v) for d, v in busy.items()})


# --------------------------------------------------------------------------- the contract
def test_the_emitter_refuses_nothing_his_schedule_asks_for(ours):
    """Twelve refusals today, including every one of his 31 day-26 wheat tiles.

    Eleven of them are ground, not turns: a chain holds its tiles for the season, so once the board
    is parcelled out there is nowhere to put the second wave. He replants -- 131 plantings on ~61
    tiles -- which is only expressible if a tile can be handed back when its crop clears.
    """
    assert not ours["report"]["refused"], (
        f"{len(ours['report']['refused'])} refusals: {ours['report']['refused'][:6]}")


def test_we_plant_every_tile_his_schedule_asks_for(schedule, ours):
    """131 tile-plantings, counted. Ours was 98, and the 33 missing are the second wave."""
    want = sum(len(r["plants"]) for r in schedule.values())
    assert ours["hist"]["PLANT"] >= want * 0.95, (
        f"{ours['hist']['PLANT']} PLANT ops against his {want}")


def test_our_hands_are_as_busy_as_his(his, ours):
    """The measurement that names the bug: 11.5 turns per hand on day 3 against his 17.7, while
    twelve jobs are refused. Idle hands and refused work at once is an assignment failure."""
    slack = []
    for day in range(1, 14):
        oh, hh = ours["hands"].get(day, 0), his["hands"].get(day, 0)
        if not hh:
            continue
        ot = sum(v for k, v in ours["per_day"][day].items() if k != "PASS")
        ht = sum(v for k, v in his["per_day"][day].items() if k != "PASS")
        ours_per, his_per = ot / max(oh, 1), ht / max(hh, 1)
        if ours_per < his_per * 0.85:
            slack.append(f"day {day}: {ours_per:.1f} turns/hand against his {his_per:.1f}")
    assert not slack, "hands idling while work is refused:\n  " + "\n  ".join(slack)


def test_we_do_not_burn_turns_harvesting_nothing(his, ours):
    """HARVEST is a silent no-op when nothing is ready, so emitting it daily costs a turn and hides.

    607 against his 338: 269 turns a season -- more than a hand's whole day-0 -- spent on tiles with
    nothing on them, while the same crew refuses his plantings for want of turns.
    """
    assert ours["hist"]["HARVEST"] <= his["hist"]["HARVEST"] * 1.25, (
        f"{ours['hist']['HARVEST']} HARVEST against his {his['hist']['HARVEST']}")


def test_we_feed_the_herd_as_often_as_he_does(his, ours):
    """FEED 173 against his 319. An unfed animal produces nothing and eventually escapes, so this is
    not a yield tax -- it is the herd quietly not being a herd."""
    assert ours["hist"]["FEED"] >= his["hist"]["FEED"] * 0.9, (
        f"{ours['hist']['FEED']} FEED against his {his['hist']['FEED']}")


def test_we_water_as_much_as_he_does(his, ours):
    """WATER 618 against his 851. Two consecutive dry days kill a tile outright."""
    assert ours["hist"]["WATER"] >= his["hist"]["WATER"] * 0.85, (
        f"{ours['hist']['WATER']} WATER against his {his['hist']['WATER']}")


def test_the_crops_are_actually_fertilized(his, ours):
    """0 against his 107, all season, on every plan we have ever emitted.

    Fertilizer doubles a watered tile's yield and his herd collects 318 units for free. Applying
    none of it is the single largest unexploited item on the census.
    """
    assert ours["hist"]["FERTILIZE"] >= his["hist"]["FERTILIZE"] * 0.5, (
        f"{ours['hist']['FERTILIZE']} FERTILIZE against his {his['hist']['FERTILIZE']}")


def test_we_do_not_walk_more_than_he_does(his, ours):
    """Sanity, and it is the theory this file rules OUT rather than in.

    Ours is 1.49 walk turns per work turn against his 1.44 -- near-identical. Routing is not where
    the season is lost, and a "fix" that improves this ratio while doing less work is a regression.
    """
    def ratio(h):
        mv = sum(v for k, v in h.items() if k in MOVES)
        work = sum(v for k, v in h.items() if k not in MOVES and k != "PASS")
        return mv / max(work, 1)
    assert ratio(ours["hist"]) <= ratio(his["hist"]) * 1.15, (
        f"{ratio(ours['hist']):.2f} walk turns per work turn against his {ratio(his['hist']):.2f}")


def test_our_crew_is_never_larger_than_his(schedule, ours):
    """The hire ladder resets every dawn and is Fibonacci: 12 hands is $376/day, 16 is $2,583.

    Ours reached 16 by day 13 where his stays at 12 -- $2,207 a day for a farm that does less work.
    """
    hire = np.asarray(ours["script"].hire)
    over = []
    for day in range(R.SEASON_DAYS):
        t = day * R.TURNS_PER_DAY
        if t >= len(hire):
            break
        # Against hires ORDERED, not hands owned -- the tape orders 6 on day 1 and holds 4, because
        # a HIRE on an empty bank is a silent no-op (`_do_hire`).
        if int(hire[t]) > schedule[day]["hires"]:
            over.append(f"day {day}: {int(hire[t])} against the tape's {schedule[day]['hires']}")
    assert not over, "crew larger than his:\n  " + "\n  ".join(over[:8])
