"""A hand that reaches the shed on the final turn has no turn left to DROP, and loses its load.

`must_walk_home_now` budgets `dist + 1` -- the walk plus one turn to drop -- and fires on the last
hour where that still fits. That is exactly right if the hand starts walking on the hour the rule
fires. It does not: the executor re-derives work at each stop, so the current stop finishes first
and the walk begins a turn late.

Measured on ladder game `93346440`, our seat, day 29 (`data/logs/who_never_came_home.log`):

    hr   u4          u5           u7          u8
    21   (2,4):3     (7,4):12     (7,4):4     (2,3):11
    22   (3,4):3     (6,4):12     (6,4):4     (2,4):11
    23   (4,4):3     (5,4):12     (5,4):4     (3,4):11

u4, u5 and u7 each STAND ON a depot tile at h23 holding a load, and u8 is one tile short. Arriving
is the h23 action; the DROP needs a turn that does not exist. 3 + 12 + 4 + 11 = 30 units, which is
the whole of that game's carried total, worth $2,334 at its closing book.

u5 is the clean case. It is at (7,1) at h18, five tiles from the depot at (5,4), so `need` is 6 and
`24 - 18 == 6` fires the rule exactly then -- yet it does not move until h19 and arrives at h23.
One turn of slack is the difference between banking 12 units and discarding them.

This pins the bound, not the routing: nothing here says which hand goes home or what it carries.
"""
import importlib

import pytest

A = importlib.import_module("kagg.search.schedule_agent")
RT = importlib.import_module("kagg.search.router")
R = importlib.import_module("kagg.search.routines")

LAST_DAY = R.SEASON_DAYS - 1
DEPOT = (5, 4)
LOADED = {"WOOL": 4}


def test_the_premise_that_a_drop_costs_its_own_turn():
    """If a DROP were free on arrival this whole test is aimed at nothing."""
    assert A.must_walk_home_now(LAST_DAY, 23, (5, 5), LOADED, [DEPOT]) is not None


def test_a_hand_five_tiles_out_leaves_by_hour_seventeen():
    """u5's case. At h18 the old bound fires and the hand still arrives on the final turn."""
    pos = (7, 1)                       # |7-5| + |1-4| = 5 tiles from the depot
    assert RT.dist(pos, DEPOT) == 5, "the fixture moved; re-read the distance before trusting this"
    assert A.must_walk_home_now(LAST_DAY, 17, pos, LOADED, [DEPOT]) is True, (
        "a hand five tiles from the shed was not sent home at h17. Firing at h18 is what left u5 "
        "standing on the depot at h23 holding 12 units: the executor finishes its current stop "
        "first, so the walk starts a turn after the rule fires.")


def test_a_hand_one_tile_out_leaves_by_hour_nineteen():
    """The short case, so the slack is not a blanket 'go home early'."""
    pos = (5, 5)
    assert RT.dist(pos, DEPOT) == 1
    assert A.must_walk_home_now(LAST_DAY, 19, pos, LOADED, [DEPOT]) is True
    assert A.must_walk_home_now(LAST_DAY, 17, pos, LOADED, [DEPOT]) is False, (
        "a hand one tile from the shed was sent home at h17, giving up six turns of work it could "
        "still have done")


def test_an_empty_hand_never_walks():
    assert A.must_walk_home_now(LAST_DAY, 17, (7, 1), {}, [DEPOT]) is False
    assert A.must_walk_home_now(LAST_DAY, 17, (7, 1), {"WOOL": 0}, [DEPOT]) is False


@pytest.mark.parametrize("day", [10, 20, 27, 28])
def test_no_earlier_day_walks(day):
    """Every day but the last banks the load for free at the rollover, so this must never fire."""
    assert A.must_walk_home_now(day, 17, (7, 1), LOADED, [DEPOT]) is False, (
        f"d{day} sent a loaded hand home; `_drop_inventories_to_shed` banks it free at the rollover")


def test_the_slack_is_named_and_is_three_turns():
    """A constant, so the next session can see what it buys rather than re-deriving it.

    **Three, not one, and the difference is the SELL rather than the DROP.** One turn covers the
    stop the executor finishes before the walk begins. The other two exist because the agent sizes
    its market orders from the shed it observed at the START of the turn: a load dropped at h23 is
    never offered, so it sits in the shed and is discarded exactly like a load left in a hand.

    Seed 3, d29 shed trace: the shed sells out completely at h17, stays empty, and the delivered
    load lands at h23 -- 45 units worth $3,164, unsold. Measured at slack 0/1/2/3:

        slack   seed 3               seed 7              seed 11
            0   $130,132 hands 54    $51,399 hands 22    $80,265 hands 35
            1   $130,132 shed  45    $50,716 shed  38    $80,185 shed  36
            2   $132,073 shed  14    $51,289 shed  16    $80,839 shed   5
            3   $133,234 clean       $51,413 clean       $80,640 clean

    Slack 1 is a REGRESSION on seed 7 ($51,399 -> $50,716): it moves the loss from hands to shed
    and gives up work to do it. Only 3 empties both.
    """
    assert getattr(A, "LAST_DAY_WALK_SLACK", None) == 3, (
        "LAST_DAY_WALK_SLACK should be 3: one turn for the stop in progress, two more so the load "
        "is in the shed before the last SELL is sized")
