"""How many of today's ARRIVING pens get fed is the tape's number, not a rule of ours.

FEED does exactly two things (`_daily_refresh_animals`, `reference/kaggriculture.py:795-820`): it
resets `consecutive_unfed`, and on a production night it releases `pending_care_bonus`. A pen placed
today has `consecutive_unfed == 0` already and is `first_yield_day` away from producing -- 8 for a
COW, 6 for a SHEEP -- so the ration buys nothing tonight. But it is not waste either: CARE is offered
only on a fed pen, and the banked bonus pays out at the first production night.

So "feed every arrival" and "feed no arrival" are both wrong, and both were measured and lost. The
recorded cadence is neither:

    day       d0   d1   d2   d3   d4   d5   d6   d7   d8
    feeds      2    4    4    4    5    6    6    9   10
    places     4    0    0    1    0    1    0    3    1

d0 places four and feeds two. d3 places one and feeds none of it (its four feeds are the four pens
already standing). d5 places one and feeds it. d7 places three and feeds two. That is a BUDGET --
`feeds` minus the pens already standing -- and no predicate on the animal reproduces it.

`scripts/extract_leader_schedule.py` did not capture FEED at all until this test existed, which is
why the number had to be guessed. Every other quantity a day commits to -- hands, places, seeds,
buys, sells -- came off the tape; this one was left to be re-derived.

d0 is the assertion because it is the cleanest case: every pen on the board arrived today, so the
whole of the day's feeding is the arrival budget, with nothing else mixed in.
"""
import importlib
import pathlib

import pytest

import kagg.plan as _PLAN

REPO = pathlib.Path(__file__).resolve().parent.parent
SEED = 11
DAY = 0


@pytest.fixture(scope="module")
def feeds_by_day():
    """`{day: FEED ops our seat emitted}`, playing the shipped plan against the kawashigi tape."""
    import scripts.breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    B.schedule_agent = SA
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)

    seen = {}
    make = SA.make_agent

    def factory():
        inner = make(sched, 0, router=True)

        def play(obs, _t=None):
            act = inner(obs)
            day = obs.get("day")
            for op in [act.get("farmer")] + list(act.get("hands") or []):
                if op and op[0] == "FEED":
                    seen[day] = seen.get(day, 0) + 1
            return act

        return play

    B.run(factory, lambda: B.tape_policy(replay, team, 1), SEED, 0.0, stop_day=DAY + 1,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))
    return seen


def test_the_premise_the_schedule_records_a_feed_row(feeds_by_day):
    """Guard. Without `feeds` on the row there is no budget and the rule below cannot bind."""
    row = _PLAN.load().get(DAY) or {}
    assert "feeds" in row, (
        "the schedule carries no `feeds` row -- re-run scripts/extract_leader_schedule.py, which "
        "captures FEED and CARE per day")
    assert int(row["feeds"]) > 0


def test_the_day_feeds_the_count_the_tape_fed(feeds_by_day):
    row = _PLAN.load().get(DAY) or {}
    want = int(row.get("feeds", 0) or 0)
    got = feeds_by_day.get(DAY, 0)
    assert got == want, (
        f"d{DAY} fed {got} pens against the tape's {want}. Every pen on d{DAY} arrived today, so "
        "this is entirely the arrival budget -- see router.ARRIVAL_FEED_REMAINING. Feeding more "
        "spends rations the shed needs on d1, which opens on one wheat and makes three shed trips.")
