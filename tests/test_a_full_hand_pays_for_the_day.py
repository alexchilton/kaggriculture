"""On a day short of cash, produce already in a hand is money. Take it to the shed.

## The gap this pins

`FUND_THE_DAY_WHEN_SHORT` arms correctly. Day 4 of Seb's 1.32.6 schedule, seed 11, weeds off:

    _days_bill(d4) = 1,458   against a dawn bank of $294      -> short_of_cash is True
    h00   funds = 20 jobs / 14 harvests, givesWHEAT = 42
    h01   funds = 20 jobs / 14 harvests, givesWHEAT = 42
    h16   funds =  0 jobs /  0 harvests, givesWHEAT =  0
    h18-h23 the same

`funds` is a property of a **job** -- "harvest this first and deliver its load on sight rather
than batching to `DELIVER_MIN`". By h16 every harvest is done, so there is no job left to carry
the flag, and nothing looks at the twenty-eight wheat already sitting in the crew's hands.

Traced hour by hour on day 4, our own agent:

    h09  shed 0  hands 20   SELL WHEAT x8    (a hand reaches the shed; it fills)
    h14  shed 0  hands 20   SELL WHEAT x16   (again; it fills)
    h15  shed 0  hands  4
    h17  shed 0  hands 16
    h20  shed 0  hands 24
    h23  shed 0  hands 28   -- and no further delivery, no further order

The market reads the shed and nothing else, so those 28 units are worth nothing until the
overnight sweep banks them at midnight, after the market has closed. The row asked for 49 WHEAT
and we sold 29.

Seb sells his day-4 wheat at **h19, h22 and h23** -- precisely the window in which our funding
rule has expired. He ends d4 having bought the $2,000 parcel; we buy it on d5.

## The rule this asks for

When the day is short of cash and a hand already holds produce the row still wants, that hand
goes to the shed. The job-triggered version cannot see it, because the job is finished.

## The guard that must not be lost

`DROP` is all-or-nothing (`kaggriculture.py:333`) -- it empties the whole hand. A hand carrying
the herd's dinner alongside the day's harvest must not shed both. Dropping wheat the tour still
owes to later FEEDs is exactly the failure that cost eight cows this morning
(`SUPPLY_LIMITS_EVERY_DRAW` in `cover.py` records the numbers). So the test asserts the surplus
goes home AND that the feed the tour still needs does not.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

DAY = 4


@pytest.fixture(scope="module")
def day4_dusk():
    """Play day 4 and report, per hour, what the crew holds and what the shed holds."""
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb1326"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    hours, animals = {}, 0
    for t in range(24 * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t // 24 == DAY:
            priv = o0.get("private") or {}
            hours[t % 24] = {
                "shed": collections.Counter(priv.get("shed") or {}),
                "hands": sum((collections.Counter(iv or {}) for iv in (priv.get("inventories") or [])),
                             collections.Counter()),
            }
            animals = max(animals, sum(1 for row in o0["farms"][0]["tiles"] for c in row
                                       if isinstance(c, dict) and c.get("animal")))
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return hours, animals, sched[DAY]


@pytest.mark.slow
def test_the_day_is_short_of_cash_and_the_row_wants_wheat(day4_dusk):
    """The premise. If this goes red the headline test is about a different day."""
    hours, _animals, row = day4_dusk
    assert SA._days_bill(row) > hours[0]["shed"].get("MONEY", 0) + 1000, (
        f"day {DAY} is not the cash-short day this test is about: bill {SA._days_bill(row)}")
    assert (row.get("sells") or {}).get("WHEAT", 0) >= 20, (
        f"day {DAY}'s row no longer asks for wheat: {row.get('sells')}")


@pytest.mark.slow
def test_the_crew_does_not_carry_the_days_takings_to_midnight(day4_dusk):
    """The whole thing. Wheat the row wants, still in hands at dusk, is money not made.

    The allowance is the herd's feed -- `feed_days(DAY) * animals` -- because that wheat is not
    surplus, it is the reason the hand is carrying anything at all.
    """
    hours, animals, _row = day4_dusk
    allowance = SA.feed_days(DAY) * animals
    held = hours[23]["hands"].get("WHEAT", 0)
    assert held <= allowance, (
        f"day {DAY} ends with {held} WHEAT in the crew's hands against a feed need of "
        f"{allowance} ({animals} animals x {SA.feed_days(DAY)} days). The market reads the shed, "
        f"so those {held - allowance} surplus units earn nothing today.\n"
        f"    hands by hour: "
        + ", ".join(f"h{h}:{hours[h]['hands'].get('WHEAT', 0)}" for h in (9, 14, 15, 17, 20, 23)))


@pytest.mark.slow
def test_the_shed_actually_receives_it(day4_dusk):
    """Delivered, not merely dropped somewhere. The shed is the only thing the market reads."""
    hours, animals, _row = day4_dusk
    best = max(hours[h]["shed"].get("WHEAT", 0) for h in range(15, 24))
    assert best >= 6, (
        f"day {DAY}: the shed never held more than {best} WHEAT at any hour between 15 and 23, "
        f"which is the window the tape sells its harvest in (h19, h22, h23).")
