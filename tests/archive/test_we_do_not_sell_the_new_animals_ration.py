"""The feed reserve counts the animals today's row will PLACE, not just the pens standing at dawn.

Day 4 is where the two collide for the first time. Its schedule row places a COW **and** sells
wheat, and the shed opens holding exactly one ration per existing pen:

    d4 h00   shed WHEAT 6    pens 6    row places ['COW']    row sells {'WHEAT': 49, 'FERTILIZER': 6}

The `sells` row is meant to be paid out of the fourteen-tile wheat HARVEST, which does not reach a
hand until h14 and does not reach the shed until h23. At h00 the only wheat on the board is the
herd's dinner, and we sell one unit of it:

      h00  ours shed 6   mkt: SELL/WHEAT/1  HIRE x7  BUY_ANIMAL/COW/1
           seb  shed 6   mkt:               HIRE x7  BUY_ANIMAL/COW/1
      h01  ours shed 5   mkt: BUY_PRODUCT/WHEAT/1        <- buying back what we just sold
           seb  shed 3   PICKUP/WHEAT/3
      h02  ours shed 6   u0,u1,u5 PICKUP/WHEAT/2 each    <- six drawn, shed 0 until h23
           seb  shed 1   mkt: BUY_PRODUCT/WHEAT/1

Both sides start the day with six wheat and six pens, and both buy exactly one more, because the
day fills a seventh pen. He finishes with seven wheat for seven mouths. We finish with six, having
sold one at dawn and bought the same unit back an hour later -- paying the spread on both legs for
a net of nothing. Six wheat reach the hands, six pens are fed, and `feed 5/7` on d6 has the same
shape one day later.

**The arithmetic, at `schedule_agent.py` in the WHEAT branch of the sell loop:**

    reserve = feed_days(day) * alive - drawn - will_buy

`alive` is a board read -- pens standing right now that `RT.will_be_fed` -- so at h00 on d4 it is
6, not 7. `will_buy` is 1, the purchase the row makes FOR the seventh animal. So the ration bought
to feed the new cow is subtracted from the reserve that protects it, and the day is handed a
sellable surplus of one that does not exist: `6 - (1*6 - 0 - 1) = 1`.

This is not the reverted experiment recorded at `feed_days`. That one targeted the BUY side from
the CUMULATIVE placement rows and over-bought whenever a placement slipped (`place 0/4` on d9/d10).
This reads **today's row only**, and nets off the animals already placed today off the board, so it
can be wrong by at most the day's own placements -- and it is wrong in the safe direction: holding
a spare wheat costs the spread, selling the herd's dinner costs an animal-day and the care chain
that hangs off it.

d1 and d3 also place a COW onto a shed holding exactly one ration per pen and sell nothing, because
neither row names wheat. d4 is the first day both halves are true at once, which is why the defect
sat behind four days of exact grids.
"""
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAY = 4


def _thin():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): {a: b for a, b in r.items() if a not in TAPE_ONLY} for k, r in raw.items()}


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]


@pytest.fixture(scope="module")
def dawn():
    """Board and market offer at `DAY` hour 0, driving the real agent from turn 0.

    Driven end to end rather than by calling the sell block directly: the reserve reads `shed`,
    `invs` and the live tiles, all of which are mid-turn state inside a 1,200-line closure. A unit
    test of the arithmetic would pin the arithmetic and prove nothing about the turn it fires on.
    """
    sched, opp = _thin(), _opponent()
    SA = importlib.import_module(MODULE)
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, 0, router=True)
    out = None
    for t in range(24 * DAY + 1):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp[t]
        if t == 24 * DAY:
            farm, priv = o0["farms"][0], o0["private"]
            out = {
                "market": [o for o in (a0["market"] or []) if o],
                "shed_wheat": int((priv.get("shed") or {}).get("WHEAT", 0)),
                "pens": sum(1 for r in farm["tiles"] for c in r
                            if isinstance(c, dict) and "animal" in c),
                "places": list((sched.get(DAY) or {}).get("places") or []),
            }
            break
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return out


def test_the_premise_holds_the_shed_opens_with_one_ration_per_mouth_and_no_spare(dawn):
    """Runs first. If the shed is not tight at dawn there is no reserve question to answer, and a
    failure in the test below would be measuring something else entirely."""
    assert dawn["pens"] == dawn["shed_wheat"], (
        f"day {DAY} opens with {dawn['shed_wheat']} wheat against {dawn['pens']} pens. The whole "
        "argument is that the shed is EXACTLY tight, so any sale comes out of a pen's dinner."
    )
    assert dawn["places"], (
        f"day {DAY}'s row places no animal, so it cannot be the day a placement's ration is sold. "
        "Either the schedule changed or the wrong tape is loaded."
    )


def test_the_ration_of_an_animal_placed_today_is_not_sold_at_dawn(dawn):
    """The defect. Red today: `SELL WHEAT 1` at d4 h00, bought straight back at h01.

    Asserted against the OFFER, not a fill, because the offer is where the decision is made -- a
    sale that fails for want of a buyer is the same mistake with better luck.
    """
    sells = [o for o in dawn["market"] if o[0] == "SELL" and o[1] == "WHEAT"]
    assert not sells, (
        f"day {DAY} hour 0 offers {sells} out of a shed holding {dawn['shed_wheat']} for "
        f"{dawn['pens']} pens, on a day whose row places {dawn['places']}. The reserve is sized on "
        f"the pens standing at dawn and then discounted by the very purchase made for the new "
        f"animal, so the seventh mouth's ration is sold before it has a pen."
    )
