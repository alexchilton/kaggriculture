"""The day's WHEAT row is bought against the whole bank, not half of it.

The wheat order used to be capped by `short = min(short, int(money * 0.5 // quote))`. That is the
right instinct for a purchase that can wait, and the wrong one for the ration: two unfed days remove
an animal outright (`kaggriculture.py:804`).

On a thin dawn the cap floors to zero. Measured on the kawashigi tape, seed 11, weeds off:

    d1 h00  money $44  quote $28  ->  int(44 * 0.5 // 28) == 0   no order for six hours
    d1                                 then 2 + 1 + 1, landing 3 of a row of 5
    d5 h00  money $113 quote $32  ->  cap 1 against a row of 2

Those one- and two-unit misses are the whole chain. d3's dawn shed holds exactly 2 wheat and the day
feeds exactly 2 of 4; the sheep miss production days; d6 shears 9 where the tape shears 12; and the
$599 that leaves is what d7 needs for its third animal. d7 bought **none** of its `buys {WHEAT: 3}`
row, so d8 opened on an empty shed and three animals were removed overnight.

d7 is the assertion because it is unambiguous -- the row is 3, the tape fills 3, and we filled 0.
The order is already bounded by `owed` (the day's own row), by `BUY_DRIP` and by the env refusing
what the bank cannot cover, so removing the cap cannot outrun the plan.

Fills, never offers: the agent re-posts an order every turn, so counting the action stream would
count one order twenty-four times.
"""
import importlib
import pathlib

import pytest

import kagg.plan as _PLAN

REPO = pathlib.Path(__file__).resolve().parent.parent
SEED = 11
DAY = 7


@pytest.fixture(scope="module")
def wheat_bought():
    """`{day: units of WHEAT actually FILLED by BUY_PRODUCT}` for our seat."""
    import scripts.breakdown as B
    from kagg.analysis.fills import record_fills
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0),
               debug=True)
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    tape = B.tape_policy(replay, team, 1)

    per_day, prev = {}, 0
    with record_fills(env) as fills:
        for t in range((DAY + 1) * 24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            # The shop draw is economy and must come from the recording, not from a seed.
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            a0, a1 = ours(o0), tape(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if t % 24 == 23:
                now = fills.units(0, "BUY_PRODUCT", "WHEAT")
                per_day[t // 24], prev = now - prev, now
    return per_day


def test_the_premise_the_day_has_a_wheat_row_to_buy(wheat_bought):
    """Guard. With no WHEAT on d7's row the assertion below would pass vacuously."""
    row = _PLAN.load().get(DAY) or {}
    assert int((row.get("buys") or {}).get("WHEAT", 0) or 0) > 0, \
        f"d{DAY} no longer buys WHEAT -- this test is measuring nothing"


def test_the_day_buys_the_whole_wheat_row_it_planned(wheat_bought):
    row = _PLAN.load().get(DAY) or {}
    want = int((row.get("buys") or {}).get("WHEAT", 0) or 0)
    got = wheat_bought.get(DAY, 0)
    assert got >= want, (
        f"d{DAY} planned to buy {want} WHEAT and filled {got}. A ration capped at half the dawn bank "
        "floors to zero on a thin day, and the herd starves two days later.")
