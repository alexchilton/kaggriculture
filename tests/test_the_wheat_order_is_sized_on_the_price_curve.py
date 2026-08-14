"""The ration is sized on what n units actually COST, not on n times the sticker price.

`market_price` moves per unit inside a single order -- that is stated twice in `schedule_agent`'s own
comments, as the reason `BUY_DRIP` exists -- but the money guard on the wheat row does not use it. It
reads `short = min(short, int(money // quote))`, where `quote` is the one price the observation
publishes. On a book that steepens, `n * quote` understates the bill and the last unit of the order
silently fails to fill.

That would be survivable on its own. It is not, because `state["ordered"]` is credited when the order
is QUEUED: an order that only partly fills still closes the row, so the day never re-offers the
remainder.

Measured on day 1, seed 11, kawashigi -- offered against FILLED, never against offers:

    h04   bank $13   price $28   offered 4   filled 3
    h11   bank $26   price $29   offered 1   filled 1

The bank at h04 is $13. The agent counts its own same-turn FERTILIZER sale, which settles first from
an earlier order slot, so the purse is really $113 and `113 // 28 == 4`. The true bill for four is
`28 + 29 + 30 + 31 == 118`. Three fill, $26 is left -- which is exactly the bank the h11 row opens on,
and the arithmetic that confirms the diagnosis. `ordered` was credited 4 of 5, so h11 asked for one
more instead of two, and the fifth wheat was never re-offered.

The fifth wheat is not a rounding error. d1 now feeds four pens, which eats a ration the shed was
carrying into d3: dawn wheat on d2 and d3 both fall 4 -> 3 against a `feeds` row of 4, so d3 drops to
`feed 3/4`, a sheep misses a production night, d6 shears one fewer, d7 opens $200 down and fills
`buy_product 0/3`, and d8 starves.
"""
import importlib

import pytest

import kagg.plan as _PLAN

SEED = 11
DAY = 1


@pytest.fixture(scope="module")
def wheat():
    """`(offered, filled)` units of WHEAT bought by our seat on d1. Fills, never offers."""
    import scripts.breakdown as B
    from kagg.analysis.fills import record_fills
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    tape = B.tape_policy(replay, team, 1)

    offered, before = 0, 0
    with record_fills(env) as fills:
        for t in range((DAY + 1) * 24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            if t == DAY * 24:
                before = fills.units(0, "BUY_PRODUCT", "WHEAT")
            a0, a1 = ours(o0), tape(o1, t)
            if t // 24 == DAY:
                offered += sum(int(o[2]) for o in (a0.get("market") or [])
                               if o and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT")
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        return offered, fills.units(0, "BUY_PRODUCT", "WHEAT") - before


def test_the_premise_day_one_has_a_wheat_row(wheat):
    """Guard. With no WHEAT on d1's row the assertion below would pass vacuously."""
    row = _PLAN.load().get(DAY) or {}
    assert int((row.get("buys") or {}).get("WHEAT", 0) or 0) > 0, \
        f"d{DAY} no longer buys WHEAT -- this test is measuring nothing"


def test_the_day_fills_the_whole_wheat_row_it_offered(wheat):
    row = _PLAN.load().get(DAY) or {}
    want = int((row.get("buys") or {}).get("WHEAT", 0) or 0)
    offered, filled = wheat
    assert filled >= want, (
        f"d{DAY} offered {offered} WHEAT and FILLED {filled} against a row of {want}. The order was "
        "sized at n x the sticker price; the book steepens inside the order, so the last unit did not "
        "fill -- and `state[\"ordered\"]` counts orders queued, not units filled, so the row closed "
        "anyway and the shortfall was never re-offered.")
