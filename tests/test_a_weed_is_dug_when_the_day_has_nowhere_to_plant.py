"""A weed on owned ground is dug when the day's planting row cannot find ground.

Seed 11, tape victor, day 11. `(7,1)` is LOCKED until d6 and spawns a WEED the moment the quadrant
unlocks -- `weedSpawnChance` is the env default here, and the tile was never planted, so this is
ground we paid for and lost, not a crop we let die.

`router.crop_ops` offers a DIG on a WEED only where `tile in plantable`, and `_plantable` is built
from PLANT pins, which `_refresh_pins` only ever sites on EMPTY squares. A weed is therefore never
plantable, so never dug, so the square stays dead for the whole season -- it is still a weed on d29.

That square is the eleventh planting spot on d11. The schedule's d11 row asks for eleven plantings
(5 STRAWBERRY, 2 MELON, 4 WHEAT); the board offers six empty squares plus four tiles a harvest
clears. One short, and strawberry is the crop that loses the race because `_refresh_pins` allocates
crop by crop and breaks when `_next_ground` returns nothing.

Measured on the d8-d18 grid, ours/tape, before and after `DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND`:

    d11        before      after
    weeds       1/0         0/0
    strawb     35/36       36/36
    water      40/41       41/41
    sell       17/18       18/18

The gate must stay narrow: ungated, digs measured `dig 5/0` on d5 against a tape that digs nothing
all season, plus strays on d12-d14. `_replant` non-empty is exactly "the row wants ground it could
not find", which is when a weed square is worth its turn.
"""
import json
import pathlib

import pytest
from kaggle_environments import make

import scripts.breakdown as B
from kagg.search import schedule_agent_1455mh as SA

SEED = 11
DAY = 11


def _play(day, dig):
    replay, schedpath, team = B.TAPES["victor"]
    sched = json.loads(pathlib.Path(schedpath).read_text())
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=SEED), debug=True)
    env.reset(2)
    before = SA.DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND
    SA.DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND = dig
    try:
        me = SA.make_agent(sched, 0, router=True)
        them = B.tape_policy(replay, team, 1)
        for t in range(24 * (day + 1)):
            env.step([me(env.state[0].observation, None), them(env.state[1].observation, t)])
    finally:
        SA.DIG_A_WEED_WHEN_THE_ROW_IS_SHORT_OF_GROUND = before
    farm = env.state[0].observation["farms"][0]
    cells = [c for row in farm["tiles"] for c in row]
    return {
        "strawberry": sum(1 for c in cells if isinstance(c, dict)
                          and c.get("kind") == "PLANT" and c.get("crop") == "STRAWBERRY"),
        "weeds": sum(1 for c in cells if isinstance(c, dict) and c.get("kind") == "WEED"),
    }


@pytest.fixture(scope="module")
def outcome():
    return _play(DAY, dig=True), _play(DAY, dig=False)


def test_the_weed_square_is_reclaimed(outcome):
    """The spawned weed at (7,1) is gone by the end of d11 -- the tape's `weeds 0` on that day."""
    on, off = outcome
    assert on["weeds"] == 0, f"expected no weed standing at the end of d11, got {on['weeds']}"
    assert off["weeds"] == 1, (
        "REVERT CHECK: with the flag off the weed must still be standing, otherwise this test "
        f"is not measuring the fix. Got {off['weeds']}."
    )


def test_the_reclaimed_square_carries_the_fifth_strawberry(outcome):
    """36/36 against the tape, where before the square was dead and we planted 35."""
    on, off = outcome
    assert on["strawberry"] == 36, (
        f"expected 36 strawberries at the end of d11 (the tape's count), got {on['strawberry']}"
    )
    assert off["strawberry"] == 35, (
        "REVERT CHECK: with the flag off we must still be one strawberry short, otherwise the "
        f"square was never the binding constraint. Got {off['strawberry']}."
    )
