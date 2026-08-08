"""A BUY_PRODUCT WHEAT the market did not fill must be re-offered, or the herd starves.

## The trace, seed 11, Seb's 1.32.6 schedule, weeds off

    d7h01  shedW=0   BUY_PRODUCT/WHEAT/6        ordered six
    d7h02  shedW=1                              ONE filled
    d7h07  shedW=1   SELL/WHEAT/1               and we sold it
    d7h08  shedW=0   ... no further wheat order for the rest of the day
           unfed = 6 animals, every hour through h23

    cow  d6:7  d7:6  d8:5      `consecutive_unfed >= 2`, `kaggriculture.py:786`

On the same day `BUY_SEED/STRAWBERRY` and `BUY_SEED/MELON` are re-offered on all twenty of h02..h21.
Seeds retry; feed does not.

## The cause

`schedule_agent.py:2512`:

    herd = feed_days(day) * alive - fed_today - on_hand - state["ordered"][("feed", "WHEAT")]

`ordered` counts what was OFFERED, never what FILLED, and it accumulates until dawn. Six offered
against a herd need of six leaves `herd <= 0` for every remaining turn of the day, whether or not a
single unit ever arrived. The note directly above it claims "the remainder is re-offered every turn",
which the code cannot do -- an order that fails leaves `on_hand` unchanged AND `ordered` raised.

The seed row already fixed exactly this, and its note records why (line ~2401): "No cross-turn
`ordered` credit on the seed row. A BUY_SEED the env rejects for want of..." -- which is precisely
why strawberry retries all afternoon and wheat is offered once.

`on_hand` is recomputed from the real shed, hands and ripe field on every turn, so an order that
filled is already visible there. Crediting it a second time through `ordered` is the double-count.

## What this asserts

The outcome, not the mechanism: on a day that ends with hungry animals and an empty shed, we must
have asked the market for wheat more than once.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA

DAY = 7


@pytest.fixture(scope="module")
def day7():
    """Per hour on day 7: shed wheat, unfed animals, and whether we asked for wheat."""
    from kaggle_environments import make

    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

    replay, schedule, team = TAPES["seb1326"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)

    hours = {}
    for t in range(24 * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = ours(o0), opp(o1, t)
        if t // 24 == DAY:
            priv = o0.get("private") or {}
            hours[t % 24] = {
                "shed": collections.Counter(priv.get("shed") or {}).get("WHEAT", 0),
                "asked": sum(1 for o in a0["market"]
                             if len(o) > 1 and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT"),
                "unfed": sum(1 for r in o0["farms"][0]["tiles"] for c in r
                             if isinstance(c, dict) and c.get("animal")
                             and not c.get("fed_today")),
            }
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return hours


@pytest.mark.slow
def test_the_premise_is_a_hungry_herd_and_an_empty_shed(day7):
    """If this goes red the day has changed and the headline below is measuring something else."""
    hungry = [h for h in range(24) if day7[h]["unfed"] > 0 and day7[h]["shed"] == 0]
    assert len(hungry) >= 8, (
        f"day {DAY} no longer spends most of itself hungry with an empty shed: {len(hungry)} hours")


@pytest.mark.slow
def test_we_ask_the_market_for_wheat_more_than_once(day7):
    """The whole thing. One unfilled order must not silence the feed chain for a whole day."""
    asked = [h for h in range(24) if day7[h]["asked"]]
    starving = [h for h in range(24) if day7[h]["unfed"] > 0 and day7[h]["shed"] == 0]
    assert len(asked) > 1, (
        f"day {DAY} offered BUY_PRODUCT WHEAT on hours {asked} and nowhere else, while "
        f"{len(starving)} hours passed with hungry animals and an empty shed.\n"
        "    `state['ordered'][('feed','WHEAT')]` counts offers, not fills, so six offered against "
        "a need of six silences the rest of the day.")


@pytest.mark.slow
def test_the_herd_is_fed_by_dusk(day7):
    """The point of the order. An animal unfed at h23 is one day from eviction."""
    assert day7[23]["unfed"] == 0, (
        f"day {DAY} ends with {day7[23]['unfed']} animals unfed; at `consecutive_unfed >= 2` they "
        "are removed and the structure is left empty (`kaggriculture.py:786`)")
