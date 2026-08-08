"""Drop the produce where the tour is ALREADY standing. Never walk for it.

The defect is the one in `test_produce_goes_home_the_day_it_is_made`: animal produce rides in a
hand all day and reaches the shed only via the rollover sweep, so we sell yesterday's production.
Over the full season we hold ~2x the tape's milk for twelve days and then dump 103 units into one
book on d29, down a price curve that falls monotonically in inventory -- this codebase already
measured that shape once, wool 123 units -> 138 for revenue $29,041 -> $21,811.

`DELIVER_SURPLUS_NOT_THE_ROW` attacked it by sending a full hand home whenever it was full enough.
That measured **-$2,021 and three cows** on the season, because the detour came straight out of
work turns and work turns are feeds.

This is the cheap half of the same idea. `schedule_agent._refresh_pins` sites pens ON the
shed-access tiles by design, so a herd tour is stood on a depot at most of its stops. Where the
detour is FREE, the drop costs one turn and no travel -- and the day has 1,807 idle turns stranded
in remainders across thirteen hands to pay it with.
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import cover as DP


@pytest.fixture(autouse=True)
def _free_drop_only(monkeypatch):
    """The expensive arm OFF, this one ON. Both at once would prove nothing about either."""
    monkeypatch.setattr(DP, "DELIVER_SURPLUS_NOT_THE_ROW", False)
    monkeypatch.setattr(DP, "DROP_WHERE_THE_TOUR_ALREADY_STANDS", True)


def _drops(route):
    return [s for s in route if getattr(s, "depot", False) and s.drop]


def _work(route):
    return [s for s in route if not getattr(s, "depot", False)]


# -------------------------------------------------------------------------------------------------
# The cheap version: drop where the tour ALREADY stands, never a detour for it.
# -------------------------------------------------------------------------------------------------


def test_a_tour_standing_on_a_depot_drops_what_it_carries_for_one_turn():
    """Pens sit ON shed-access tiles by design (`schedule_agent._refresh_pins`), so a herd tour is
    stood on a depot at most of its stops. Dropping there costs one turn and ZERO travel.

    This is the whole difference between this arm and `DELIVER_SURPLUS_NOT_THE_ROW`, which
    measured -$2,021 and three cows: that one inserts a DETOUR whenever the hand is full enough,
    and the detour comes out of work turns. This one only ever fires where the walk is already
    being made, so the produce reaches the shed while the market is open at the cost of a single
    turn -- which the day has 1,807 of, stranded in remainders across thirteen hands.
    """
    work = [DP.Job((4, 4), [("HARVEST", None)], gives={"MILK": 6}),   # (4,4) IS a depot
            DP.Job((4, 5), [("FEED", "WHEAT")], needs={"WHEAT": 1}),  # so is (4,5)
            DP.Job((3, 4), [("WATER", None)])]
    route = DP.materialise((4, 4), work, carry={"WHEAT": 1}, depots=DP.SHED,
                           wanted={}, deliver=False)
    assert _drops(route), (
        f"stood on a depot holding 6 MILK and walked away with it:\n    {route}")


def test_the_free_drop_never_pays_for_travel():
    """The guard that separates this from the arm that lost money.

    A hand full of milk in the far corner, with every depot several steps away, must NOT be sent
    home. It rides to the end of the tour as before -- the closing trip in `plan` is where that
    case is handled, and only if the budget has room for it.
    """
    work = [DP.Job((0, 9), [("HARVEST", None)], gives={"MILK": 30})]
    work += [DP.Job((x, 9), [("WATER", None)]) for x in range(4)]
    route = DP.materialise((0, 9), work, carry={}, depots=DP.SHED,
                           wanted={}, deliver=False)
    assert not _drops(route), (
        f"walked from the far corner to the shed and back for produce nobody asked for:\n"
        f"    {route}")


def test_the_free_drop_does_not_bin_the_feed_the_tour_still_needs():
    """Same guard as always: `after[i]` must keep the herd's dinner out of the drop."""
    work = [DP.Job((4, 4), [("FEED", "WHEAT")], needs={"WHEAT": 1})]
    work += [DP.Job((x, 4), [("FEED", "WHEAT")], needs={"WHEAT": 1}) for x in range(4)]
    route = DP.materialise((4, 4), work, carry={"WHEAT": 5}, depots=DP.SHED,
                           wanted={}, deliver=False)
    fed = [s for s in _work(route) if any(o == "FEED" for o, _i in s.ops)]
    assert len(fed) == 5, f"lost a feed:\n    {route}"
    picks = [s for s in route if getattr(s, "depot", False) and s.pick]
    assert not picks, (
        f"dropped the wheat it was carrying and had to draw it straight back:\n    {route}")


def test_a_hand_still_owing_feed_ahead_never_drops_even_where_it_is_free():
    """`DROP` is ALL-OR-NOTHING (`kaggriculture.py:333`) -- it takes the whole hand.

    So a unit standing on a depot holding six milk AND four wheat for the next four pens cannot
    bank the milk and keep the wheat; dropping puts the lot in the shed and the pens go unfed.
    Planning as though it could cost a cow and two sheep over the season.
    """
    work = [DP.Job((4, 4), [("HARVEST", None)], gives={"MILK": 6})]
    work += [DP.Job((x, 4), [("FEED", "WHEAT")], needs={"WHEAT": 1}) for x in range(4)]
    route = DP.materialise((4, 4), work, carry={"WHEAT": 4}, depots=DP.SHED,
                           wanted={}, deliver=False)
    first_feed = min(i for i, s in enumerate(route)
                     if not getattr(s, "depot", False)
                     and any(o == "FEED" for o, _i in s.ops))
    early = [s for s in route[:first_feed] if getattr(s, "depot", False) and s.drop]
    assert not early, (
        f"dropped the whole hand -- milk AND the four pens' wheat -- before feeding any of "
        f"them:\n    {route}")
