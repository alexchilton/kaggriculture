"""A draw the shed could not fill is taken at the tour's NEXT shed stop, not thrown away.

`materialise` sizes every depot draw off `after[i]` -- the whole remainder of the tour -- and it has no
idea what the shed holds. The executor discovers that at the stop: `take = min(node.pick[item],
shed[item])`, and when the shed comes up short the outstanding want is `del`eted and the tour walks on
without it.

For most of the day that is right. The shed refills off the day's `BUY_PRODUCT` drip, and a hand that
STANDS AND WAITS for it is a measured loss twice over -- both arms are recorded in the block this rule
sits in, and both cost the d6 land parcel. This is the other answer, and it is the tape's: don't wait,
come BACK. The hand keeps working and re-draws when its route next puts it at the shed anyway.

Day 1, seed 11, kawashigi. Four pens, one farmer, 24 turns, and the dawn shed holds **three** wheat
against a four-wheat draw. The row buys 5 more, which land at the end of h04.

    tape    h00 PICKUP  h01 FEED  h03 FEED  h06 FEED   -- three, the shed is empty
            h18 PLACE FERTILIZER + SELL 3 + BUY WHEAT 5
            h19 PICKUP  h21 FEED                       -- the fourth, off the restocked shed
    ours    h00 PICKUP 3 of 4, the 4th want deleted at h01, never asked for again
            h20 COLLECT_FERTILIZER alone -- no wheat, so no FEED, and CARE is only legal on a
            fed pen, so no CARE either

`feed 3/4` and `care 3/4`, and that is the head of the chain: the sheep miss a production night, d6
shears 9 where the tape shears 12, d7 cannot afford its third animal.

The assertion is that the day DRAWS all four -- not that it draws them in one go. One pickup or two is
the tour's business; giving up on the fourth is the defect.
"""
import collections
import importlib

import pytest

import kagg.plan as _PLAN

SEED = 11
DAY = 1


@pytest.fixture(scope="module")
def day_one():
    """WHEAT units PICKUPed by our seat on d1, and the shed level it woke up to."""
    import scripts.breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)

    out = {"drawn": 0, "dawn_shed": None, "hours": []}
    make = SA.make_agent

    def factory():
        inner = make(sched, 0, router=True)

        def play(obs, _t=None):
            act = inner(obs)
            if obs.get("day") != DAY:
                return act
            if obs.get("hour") == 0 and out["dawn_shed"] is None:
                out["dawn_shed"] = int((obs["private"]["shed"] or {}).get("WHEAT", 0))
            for op in [act.get("farmer")] + list(act.get("hands") or []):
                if op and op[0] == "PICKUP" and op[1] == "WHEAT":
                    out["drawn"] += int(op[2]) if len(op) > 2 else 1
                    out["hours"].append(obs.get("hour"))
            return act

        return play

    B.run(factory, lambda: B.tape_policy(replay, team, 1), SEED, 0.0, stop_day=DAY + 1,
          economy=B.env_config(replay), shops=B.recorded_shops(replay))
    return out


def test_the_premise_the_dawn_shed_cannot_cover_the_day(day_one):
    """Guard. If the shed already held four wheat there is no shortfall and nothing to carry."""
    row = _PLAN.load().get(DAY) or {}
    pens = int(row.get("feeds", 0) or 0)
    assert day_one["dawn_shed"] < pens, (
        f"d{DAY} woke to {day_one['dawn_shed']} wheat for {pens} pens -- the draw is no longer short "
        "and this test is measuring nothing")


def test_the_day_draws_a_ration_for_every_pen_it_feeds(day_one):
    row = _PLAN.load().get(DAY) or {}
    pens = int(row.get("feeds", 0) or 0)
    assert day_one["drawn"] >= pens, (
        f"d{DAY} drew {day_one['drawn']} wheat at hours {day_one['hours']} for {pens} pens, off a "
        f"dawn shed of {day_one['dawn_shed']}. The shortfall was deleted at the stop that could not "
        "fill it instead of being carried to the next one -- and the row buys 5 more that land at "
        "h04. The tape draws again at h19 and feeds its fourth pen at h21.")
