"""`FEED_RESERVE_YIELDS_TO_OVERFLOW` is documented as a late-season lever and fires from day 0.

## The theory under test

Every comment attached to `FEED_RESERVE_YIELDS_TO_OVERFLOW` (`schedule_agent.py` ~1340-1366,
~2546-2559, ~3109-3121) frames it as a correction for the TURN-BOUND phase: "from day 16 the farm
is TURN-bound with the bank past $10k and nothing to spend it on but feed", "the reserve is a
buffer against a hiccup", "one day of feed for the largest herd this agent runs (19)". Nothing in
the prose says it should touch day 0, when the herd is 4 animals and the dawn bank is measured in
hundreds of dollars.

But the `if FEED_RESERVE_YIELDS_TO_OVERFLOW:` guards in the code carry no day check -- neither the
sell-side `releasable` override nor the buy-side `floor_short` requirement. Both read `alive` and
`shed`, which exist from day 0.

Measured 2026-08-09, full season (agent plays d0-d29, not handed over), seed 11, weeds off, seb1326
schedule: turning the flag on changes the shed/hands/money row on **12 of the first 15 days**,
starting at day 0 -- a wheat purchase against a four-animal herd that does not happen with the flag
off, and `money@d15` moves **2,252 -> 1,931**. `sh:wheat` money never differs on d0-d10 without the
flag; every difference disappears when `day < FEED_DAYS_FROM_DAY` gates the block.

## What this asserts

`snap_wheat_row(day)` -- the shed WHEAT count, hands count and dawn money for the state produced by
the flag ON must equal the flag OFF for every day strictly before `FEED_DAYS_FROM_DAY`. This is a
narrower, mechanical claim than "money is unchanged" and does not depend on believing the discard
count is the right metric -- it only asserts the documented trigger day is where the mechanism
starts, which the code does not currently enforce.
"""

import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

SEED, DAYS = 11, 16  # only the pre-FEED_DAYS_FROM_DAY window matters here


def _play(feed_reserve_yields):
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    _saved_FEED_RESERVE_YIELDS_TO_OVERFLOW = SA.FEED_RESERVE_YIELDS_TO_OVERFLOW

    _saved_FEED_DAYS_FLOOR = SA.FEED_DAYS_FLOOR

    SA.FEED_RESERVE_YIELDS_TO_OVERFLOW = feed_reserve_yields
    SA.FEED_DAYS_FLOOR = 1

    replay, schedule, team = TAPES["seb1326"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    rows = []
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        day, hour = t // 24, t % 24
        if hour == 0:
            priv = o0.get("private") or {}
            shed = priv.get("shed") or {}
            hands = sum(sum((iv or {}).values()) for iv in (priv.get("inventories") or []))
            rows.append(dict(day=day, wheat=int(shed.get("WHEAT", 0)), hands=hands,
                             money=o0["farms"][0]["money"]))
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    try:
        yield rows
    finally:
    
    SA.FEED_RESERVE_YIELDS_TO_OVERFLOW = _saved_FEED_RESERVE_YIELDS_TO_OVERFLOW
    
    SA.FEED_DAYS_FLOOR = _saved_FEED_DAYS_FLOOR



@pytest.fixture(scope="module")
def rows_off():
    return _play(False)


@pytest.fixture(scope="module")
def rows_on():
    return _play(True)


@pytest.mark.slow
def test_the_flag_is_a_noop_before_feed_days_from_day(rows_off, rows_on):
    """Dawn wheat/hands/money must match with the flag on and off, every day before day 16."""
    assert SA.FEED_DAYS_FROM_DAY == 16, "this test is scoped to the documented trigger day"
    early_off = [r for r in rows_off if r["day"] < SA.FEED_DAYS_FROM_DAY]
    early_on = [r for r in rows_on if r["day"] < SA.FEED_DAYS_FROM_DAY]
    diffs = [(o, n) for o, n in zip(early_off, early_on) if o != n]
    assert not diffs, (
        f"{len(diffs)} of {len(early_off)} days before FEED_DAYS_FROM_DAY differ with the flag on, "
        "though every comment attached to it describes a late-season lever:\n" +
        "\n".join(f"    day {o['day']}: OFF {o}  ON {n}" for o, n in diffs))
