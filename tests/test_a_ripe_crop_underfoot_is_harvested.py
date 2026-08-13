"""A hand crossing a ripe crop harvests it instead of walking on.

`underfoot()` in the tour walker exists precisely because "the route is a visit ORDER and
`_live_ops` is consulted at STOPS, so a tile a hand merely crosses is never looked at" -- its own
docstring. It then returned `None` on every tile without an `"animal"`, so only a hungry pen was
ever picked up underfoot and a ripe crop never was.

Measured on the Kawashigi tape, seed 11, day 4. The tape harvests 7; we harvested 6. The pool is not
the problem and neither is the seating -- `dump_day_jobs` shows **7 HARVEST jobs offered**, all
wheat at 3 units each, and `solve_day_offline` reports the shipped planner covering **20/20**. The
tile that goes unharvested is (1,4). Its owner is the last stop of the longest tour (`cost 23`
against a 23-turn budget) and reaches it at h23 with no turn left to work it, while three other
hands cross it and walk on:

    h16  u4@(1,4) -> EAST     h19  u2@(1,4) -> WEST
    h23  u0@(1,4) -> EAST     h23  u2@(1,4) -> EAST

HARVEST only, never WATER: a harvest is one turn for a whole yield and it clears the tile for a
replant, whereas watering a tile another hand is routed to merely moves the turn around.

The assertion is on the count the day emits, not on which hand emits it -- who picks the tile up is
tour shape and is exempt (`matching-the-tape`).
"""
import importlib
import pathlib

import pytest

import kagg.plan as _PLAN

REPO = pathlib.Path(__file__).resolve().parent.parent
SEED = 11
DAY = 4
#: What the tape harvests on `DAY`, read off the recording by `scripts/breakdown.py --tape kawashigi`.
TAPE_HARVESTS = 7


@pytest.fixture(scope="module")
def harvests_by_day():
    """`{day: HARVESTs our seat emitted}`, playing the shipped plan against the Kawashigi tape."""
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
                if op and op[0] == "HARVEST":
                    seen[day] = seen.get(day, 0) + 1
            return act

        return play

    # The shop draw is part of the economy and must be injected from the recording, not derived
    # from a seed -- see `breakdown.recorded_shops`. Without it the herd, and therefore the tour
    # lengths this test is about, are a different game.
    B.run(factory, lambda: B.tape_policy(replay, team, 1), SEED, 0.0, stop_day=DAY + 1,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))
    return seen


def test_the_premise_the_day_offers_more_harvests_than_one_hand_can_reach(harvests_by_day):
    """Guard. If the day stopped offering harvests the assertion below would pass vacuously."""
    assert harvests_by_day.get(DAY, 0) > 0, f"d{DAY} emitted no HARVEST at all -- the pool changed"


def test_the_day_harvests_every_ripe_tile_the_tape_does(harvests_by_day):
    got = harvests_by_day.get(DAY, 0)
    assert got >= TAPE_HARVESTS, (
        f"d{DAY} emitted {got} HARVESTs against the tape's {TAPE_HARVESTS}. The dawn plan offers "
        f"{TAPE_HARVESTS} and the solver covers all of them, so a ripe tile is being walked over "
        "rather than left unplanned -- see HARVEST_WHAT_YOU_STAND_ON.")
