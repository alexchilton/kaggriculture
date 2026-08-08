"""Day 4 has the wheat, the hands and the hours, and feeds two animals in seven.

## Why day 4

It is the first day the two sides part on anything that matters. Everything before it is
identical -- same pens, same plants, same hires, same tiles. Read off
`data/logs/breakdown_d0_d16_seb1326.log`, seed 11, weeds off, against Seb's 1.32.6 tape:

    d4        ours/tape
    feed        2/7        the pens hold six animals; we feed two
    care        2/7
    sh:wheat   32/7        we END the day holding thirty-two wheat
    pickup      2/3
    idle       70/35       and we have double his spare turns
    work       47/62
    buy_land    0/1        he buys the second parcel today; we buy it on d5

Measured here rather than read off that table: the shed opens day 4 with **6 wheat for 6 animals**
-- exactly enough, not spare -- and the 32 arrives during the day, from the fourteen-tile wheat
harvest. So the feed is tight at dawn and plentiful by mid-morning.

What is never tight is time. Seventy unit-turns go unused, and `PICKUP` is unbounded per item
(`kaggriculture.py:340`), so ONE draw can carry the whole shed. We make two draws and reach two
pens.

**CARE settles the argument.** It draws nothing from the shed at all, so no supply story can
excuse it, and we do it twice for six animals with seventy turns to spare.

## What it costs

`consecutive_unfed >= 2` evicts the animal (`kaggriculture.py:786`). Feeds run 2/7, 7/3, 3/7, 2/3
across d4-d7, and on d7 our cows drop 5 -> 3 while his hold at 5. That gap never closes:

    cow    d7 3/5   d9 5/7   d11 7/11   d13 8/13   d14 5/13   d16 5/13

By d16 we have 5 cows and 7 sheep against his 13 and 8, and the money reads $7,293 against
$15,026. Every one of those cows is milk at $271 that we never produce and never sell.

## The theory this test pins

**The day-4 tour never routes the wheat to the pens.** Not that we lack wheat, and not that we
lack time -- both are disproved by the row above. So the assertion is about the OP COUNT on a day
whose supply and budget are known good, and it fails today.

Deliberately NOT asserted here: money, land timing, or the herd at d16. Those are consequences,
and a test that asserts a consequence three days downstream cannot tell you which day broke.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

DAY = 4


def _play_to(day, tape="seb1326", seed=11):
    """Play up to and including `day`, returning that day's op counts and the dawn board."""
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES[tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    ops = collections.Counter()
    dawn = None
    for t in range(24 * (day + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t == 24 * day:
            priv = o0.get("private") or {}
            dawn = {
                "shed": collections.Counter(priv.get("shed") or {}),
                "animals": sum(1 for row in o0["farms"][0]["tiles"] for c in row
                               if isinstance(c, dict) and c.get("animal")),
                "hands": 1 + len(o0["farms"][0].get("hands") or []),
            }
        a0, a1 = ours(o0), opp(o1, t)
        if t // 24 == day:
            n0 = len(o0["farms"][0].get("hands") or [])
            for act in [a0["farmer"]] + list(a0["hands"])[:n0]:
                ops[(act or ["PASS"])[0]] += 1
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return ops, dawn


@pytest.fixture(scope="module")
def day4():
    return _play_to(DAY)


@pytest.mark.slow
def test_the_shed_and_the_budget_are_not_the_excuse(day4):
    """Establish the premise before asserting the failure.

    If this ever goes red the headline test below is testing something else, and its failure would
    be about supply rather than routing.
    """
    ops, dawn = day4
    assert dawn["animals"] >= 6, f"day {DAY} does not have the herd this test is about: {dawn}"
    # **Dawn wheat is 6 for 6 animals -- exactly enough, not spare.** The 32 in the breakdown
    # table is the END of day 4, after the day's fourteen-tile wheat harvest lands. So supply is
    # tight at dawn and abundant by mid-morning, and neither state excuses the CARE count below.
    assert dawn["shed"]["WHEAT"] >= dawn["animals"], (
        f"day {DAY} opened with {dawn['shed']['WHEAT']} wheat for {dawn['animals']} animals -- "
        f"this is a SUPPLY failure, not the routing one this file is about")
    assert ops["HARVEST"] >= 14, (
        f"day {DAY} is meant to harvest the wheat block that refills the shed; got "
        f"{ops['HARVEST']} harvests")
    assert ops["PASS"] >= dawn["animals"], (
        f"day {DAY} had only {ops['PASS']} idle unit-turns; there was no spare capacity to route")


@pytest.mark.slow
def test_every_animal_is_fed_on_day_four(day4):
    """The whole thing in one assertion. Tape feeds 7 of 7; we feed 2."""
    ops, dawn = day4
    assert ops["FEED"] >= dawn["animals"], (
        f"day {DAY}: {ops['FEED']} FEEDs for {dawn['animals']} animals, with "
        f"{dawn['shed']['WHEAT']} wheat in the shed and {ops['PASS']} idle unit-turns "
        f"across {dawn['hands']} units. The tape feeds all {dawn['animals']}.\n"
        f"    ops: {dict(ops.most_common())}")


@pytest.mark.slow
def test_every_animal_is_cared_for_on_day_four(day4):
    """CARE needs no wheat at all, so it cannot even be argued as a supply problem.

    It is worth its own assertion because CARE correlates with money at +0.441 across 312 real
    leaderboard seats -- second only to FEED -- and it is free.
    """
    ops, dawn = day4
    assert ops["CARE"] >= dawn["animals"], (
        f"day {DAY}: {ops['CARE']} CAREs for {dawn['animals']} animals with {ops['PASS']} idle "
        f"unit-turns. CARE draws nothing from the shed; there is no supply argument for this one.")
