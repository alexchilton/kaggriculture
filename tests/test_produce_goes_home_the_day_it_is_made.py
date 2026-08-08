"""Milk in a backpack is not money. Carry it home the day it is made.

## The bug

`materialise` decides whether a hand is worth a shed trip like this:

    load = sum(min(max(0, held[p] - after[i][p]), q) for p, q in wanted.items() if q > 0)
    if load >= DELIVER_MIN:

`wanted` is **today's sell row**, transcribed from Seb's board. A product the row does not name
contributes nothing to `load`, so no mid-tour shed stop is ever inserted for it, however much of
it the hand is carrying. It rides around until `_drop_inventories_to_shed` sweeps every hand into
the shed at the rollover (`reference/kaggriculture.py:812`) -- after the market has closed.

So we sell yesterday's production, every day, all season. Measured, seed 11, weeds off:

    d14  h6  shed 0  hand  6      the day's row asks MILK 0
         h8  shed 0  hand 12
         h13 shed 0  hand 15      fifteen milk carried around all day
    d15  h0  shed 15 hand  0      SELL MILK 15   <- exactly what the sweep left
    d16  h0  shed  3 hand  0      SELL MILK  3

against a row asking 24 on both days, which Seb fills on both days. Wool is worse: the d16 row
asks 19, he sells 19, we sell 0. Nothing blocks the sale -- the shed has 60-95 free slots all day
and the market is open. We simply never carry it home in time.

## The fix

Judge the load by what the hand is CARRYING, not by what today's row happens to name. `after[i]`
already subtracts everything the rest of the tour will consume, so feed wheat and fertilizer held
for a later job are excluded by construction -- which is the guard that matters, because counting
the herd's dinner as sellable is what cost day 4 every one of its feeds once before.

`DELIVER_MIN` is untouched. The batching threshold was never the problem and lowering it is a
separate, measured mistake (a threshold of 1 put a shed trip after every stop, since pens sit on
shed-access tiles and a drop there costs no travel).
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import cover as DP


@pytest.fixture(autouse=True)
def _mechanism_on(monkeypatch):
    """These test the MECHANISM, which ships off. See `DELIVER_SURPLUS_NOT_THE_ROW`.

    The defect is real and these reproduce it in milliseconds; the flag is off because the cure
    measured worse than the disease on a full season. Keeping them green under an explicit
    monkeypatch keeps the reproduction alive for the next attempt, and keeps it honest about the
    fact that nothing in the shipped agent behaves this way today.
    """
    monkeypatch.setattr(DP, "DELIVER_SURPLUS_NOT_THE_ROW", True)


def _drops(route):
    return [s for s in route if getattr(s, "depot", False) and s.drop]


def _work(route):
    return [s for s in route if not getattr(s, "depot", False)]


def _filler(n, y=0):
    """Ordinary jobs that need nothing and yield nothing, to give the tour a body."""
    return [DP.Job((x, y), [("WATER", None)]) for x in range(n)]


def test_a_hand_full_of_milk_goes_to_the_shed_even_when_the_row_wants_no_milk():
    """The whole bug in one assertion."""
    work = [DP.Job((0, 3), [("HARVEST", None)], gives={"MILK": DP.DELIVER_MIN})] + _filler(6)
    route = DP.materialise((4, 4), work, carry={}, depots=DP.SHED,
                           wanted={"MELON": 5}, deliver=False)
    assert _drops(route), (
        f"carrying {DP.DELIVER_MIN} MILK through {len(_work(route))} more stops and never once "
        f"went to the shed, because the day's row does not name MILK:\n    {route}")


def test_the_trip_happens_before_the_tour_ends_not_after_it():
    """A drop appended at the end is the overnight sweep by another name.

    `deliver=False` is what makes this test mean anything -- the closing trip is charged
    separately and opportunistically in `plan`, so if the only drop were the closing one this
    assertion could pass while the bug stood.
    """
    work = [DP.Job((0, 3), [("HARVEST", None)], gives={"MILK": 12})] + _filler(6)
    route = DP.materialise((4, 4), work, carry={}, depots=DP.SHED,
                           wanted={}, deliver=False)
    assert _drops(route), "no mid-tour drop at all"
    last_drop = max(i for i, s in enumerate(route) if getattr(s, "depot", False) and s.drop)
    assert any(not getattr(s, "depot", False) for s in route[last_drop:]), (
        f"the only drop is the last stop, so the produce still sits in the hand all day:\n"
        f"    {route}")


def test_a_load_under_the_threshold_still_rides_along():
    """`DELIVER_MIN` is not what is being changed. One egg is not worth a walk."""
    work = [DP.Job((0, 3), [("HARVEST", None)], gives={"MILK": DP.DELIVER_MIN - 1})] + _filler(6)
    route = DP.materialise((4, 4), work, carry={}, depots=DP.SHED,
                           wanted={}, deliver=False)
    assert not _drops(route), f"walked home for {DP.DELIVER_MIN - 1} units:\n    {route}"


def test_the_herds_dinner_is_never_delivered_as_produce():
    """The regression this fix must not reintroduce.

    Wheat drawn for a FEED later in the tour is not surplus, it is the reason for the trip. Once
    before, counting it as sellable turned day 4 into `PICKUP 2, DROP 12, FEED 0, CARE 0` with
    eight animals unfed. `after[i]` is what prevents it, and this test is what proves `after[i]`
    is still doing the work.
    """
    feeds = [DP.Job((x, 4), [("FEED", "WHEAT")], needs={"WHEAT": 1}) for x in range(8)]
    route = DP.materialise((4, 4), feeds, carry={"WHEAT": 8}, depots=DP.SHED,
                           wanted={}, deliver=False)
    assert not _drops(route), (
        f"dropped the wheat the tour's own eight feeds are about to eat:\n    {route}")


def test_produce_is_delivered_and_the_feed_it_travels_with_is_not():
    """Both at once, which is the case the real day actually plays.

    A hand holding tomorrow's feed AND today's milk must lose the milk and keep the wheat.
    """
    work = [DP.Job((0, 3), [("HARVEST", None)], gives={"MILK": 12})]
    work += [DP.Job((x, 4), [("FEED", "WHEAT")], needs={"WHEAT": 1}) for x in range(4)]
    work += _filler(4)
    route = DP.materialise((4, 4), work, carry={"WHEAT": 4}, depots=DP.SHED,
                           wanted={}, deliver=False)
    drops = _drops(route)
    assert drops, f"the milk never went home:\n    {route}"
    # every FEED must still be reachable: the tour may not arrive at one having binned the wheat
    fed = [s for s in _work(route) if any(o == "FEED" for o, _i in s.ops)]
    assert len(fed) == 4, f"lost a feed to the delivery:\n    {route}"


@pytest.mark.slow
@pytest.mark.xfail(reason="DELIVER_SURPLUS_NOT_THE_ROW ships off: the cure measured worse than the disease", strict=False)
def test_the_milk_reaches_the_shed_while_the_market_is_open():
    """End to end. The assertion is about the HOUR, because that is the whole defect.

    `sh:milk` read off a dawn snapshot looks healthy and is worthless -- dawn is the one moment of
    the day the milk is in the shed, because the rollover sweep put it there. What matters is
    whether it is ever in the shed on a turn we could trade it.
    """
    import collections
    import json
    import pathlib

    from kaggle_environments import make

    from kagg.search import schedule_agent as SA
    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)
    midday_shed, hand_peak = 0, 0
    for t in range(24 * 15):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t // 24 == 14 and 1 <= t % 24 <= 22:
            priv = o0.get("private") or {}
            midday_shed = max(midday_shed, int((priv.get("shed") or {}).get("MILK", 0)))
            hand_peak = max(hand_peak, sum(collections.Counter(iv or {}).get("MILK", 0)
                                           for iv in (priv.get("inventories") or [])))
        a0, a1 = ours(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])

    assert hand_peak >= 6, f"day 14 never produced enough milk to test ({hand_peak} in hand)"
    assert midday_shed >= 6, (
        f"day 14 peaked at {hand_peak} MILK in hands and never got more than {midday_shed} into "
        f"the shed between h1 and h22 -- it can only be sold the next morning")

