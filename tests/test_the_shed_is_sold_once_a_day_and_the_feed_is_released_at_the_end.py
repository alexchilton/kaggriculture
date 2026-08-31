"""The agent sells the shed once a day, holds the herd's wheat, and lets it go at the end.

    python -u -m pytest tests/test_the_shed_is_sold_once_a_day_and_the_feed_is_released_at_the_end.py -q

WHAT IS BEING SHIPPED, AND THE NUMBERS BEHIND IT
------------------------------------------------
Measured 2026-08-28, 3 seeds, 719 turns, idle opponent, `REPLAY_OPENING_DAYS = ()`
(`data/logs/naive_sell*.log`). The planner's own SELL orders are removed and replaced; everything
else it asks for -- hires, land, seed, feed buys -- is left alone.

    planner's own market                                    150,396
    sell-all EVERY turn, keep 20 wheat                       74,180
    sell-all at h16 only, keep 20 wheat                     145,629
    sell-all at h16, reserve released from d26              147,368

**Cadence is the whole lever.** The same goods, sold once a day instead of every turn, is worth
+$71,449 -- selling every turn walks our own price down, the same mechanism as the wool crash from
$239 to $11 on 57 units. Basket choice is not what matters here; rate is.

**The terminal release is small and real.** +$920 at d28, +$1,739 at d26, on every seed. Past the
last yield the wheat cannot become milk or wool, only cash, so the reserve is dead capital.

The first version of that test released the reserve AND switched to selling every turn, and read as
a loss; isolating the two reversed it. One delta at a time.

THREE PROPERTIES, and each is a way this can silently stop working
-----------------------------------------------------------------
1. Nothing is offered on an off-hour. If the cadence leaks back to every turn the flooding returns
   and $71k goes with it, while every op count and every agreement metric stays identical.
2. The herd's wheat is held before the release day. `consecutive_unfed >= 2` removes the animal
   outright, so selling the feed is not a smaller sale, it is a dead cow.
3. The reserve IS released on and after the release day, or the +$1,739 quietly reverts.
"""
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

TPD = 24


def _agent():
    from kagg import plan as PLAN
    from kagg.search import schedule_agent as SA

    SA.REPLAY_OPENING_DAYS = ()          # the planner arm, the one the numbers were measured on
    return SA, SA.make_agent(PLAN.load(), 0)


def _sells(action):
    return [o for o in (action.get("market") or []) if o and o[0] == "SELL"]


def _play(turns):
    """`{turn: action}` for a real game, planner driving, idle opponent."""
    from kaggle_environments import make

    SA, agent = _agent()
    env = make("kaggriculture", configuration={"seed": 9000, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    out = {}
    for t in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        act = agent(obs)
        out[t] = (act, dict((obs.get("private") or {}).get("shed") or {}))
        env.step([act, {"farmer": ["PASS"], "hands": [], "market": []}])
    return SA, out


def test_nothing_is_offered_on_an_off_hour():
    """Property 1: the cadence. A leak back to every turn costs $71,449 and shows up nowhere else."""
    SA, played = _play(24 * 8)
    offenders = [t for t, (act, _shed) in played.items()
                 if t % TPD != SA.SELL_HOUR and _sells(act)]
    assert not offenders, (
        "SELL offered on %d off-hour turns, first at turn %s (hour %d). Selling every turn walks "
        "our own price down: measured $74,180 against $145,629 for the same goods sold once a day."
        % (len(offenders), offenders[0], offenders[0] % TPD))


def test_the_herd_keeps_its_wheat_before_the_release_day():
    """Property 2: the reserve. Selling the feed is a dead animal, not a smaller sale."""
    SA, played = _play(24 * (SA_RELEASE := 26))
    checked = 0
    for t, (act, shed) in played.items():
        if t // TPD >= SA.SELL_RELEASE_FROM_DAY:
            continue
        for o in _sells(act):
            if o[1] != "WHEAT":
                continue
            checked += 1
            left = int(shed.get("WHEAT", 0) or 0) - int(o[2])
            assert left >= SA.SELL_KEEP_WHEAT, (
                "turn %d (day %d) sells WHEAT %s from a shed holding %s, leaving %d against a "
                "reserve of %d." % (t, t // TPD, o[2], shed.get("WHEAT"), left,
                                    SA.SELL_KEEP_WHEAT))
    if not checked:
        pytest.skip("no WHEAT sale was offered before the release day")


def test_the_reserve_is_released_at_the_end():
    """Property 3: past the last yield the wheat can only become cash."""
    SA, played = _play(24 * 30)
    late = [(t, act, shed) for t, (act, shed) in played.items()
            if t // TPD >= SA.SELL_RELEASE_FROM_DAY and int(shed.get("WHEAT", 0) or 0) > 0]
    if not late:
        pytest.skip("the shed held no wheat on or after the release day")
    freed = [t for t, act, shed in late
             for o in _sells(act)
             if o[1] == "WHEAT"
             and int(shed.get("WHEAT", 0) or 0) - int(o[2]) < SA.SELL_KEEP_WHEAT]
    assert freed, (
        "on and after day %d the shed held wheat on %d turns and never offered more than the "
        "reserve allowed. The terminal release is worth +$1,739 and has reverted."
        % (SA.SELL_RELEASE_FROM_DAY, len(late)))
