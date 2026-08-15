"""The day's wheat row is ordered at hour 0, out of the dawn bank, before the day spends it.

The market block queues SELL, HIRE, BUY_LAND, BUY_ANIMAL, BUY_SEED and only then the schedule's
`buys` row, and it sizes that last order against whatever money is left. On day 0 that is nothing:
the whole $3,000 has gone on four hires and five animals by the time wheat is considered, so the
row dribbles out one unit a turn against an empty bank and stops at four of eleven.

Victor's day 0, hour 0, verbatim -- he puts the wheat FIRST and still fits everything in nine of
his ten slots:

    OURS  HIRE x4  BUY_ANIMAL COW 1  BUY_ANIMAL SHEEP 1 x4
    TAPE  BUY_PRODUCT WHEAT 11  HIRE x4  BUY_ANIMAL COW 1  BUY_ANIMAL SHEEP 4
          BUY_SEED WHEAT 5  BUY_SEED MELON 5

`buy_product 4/11` is not the only row it costs. A FEED consumes one wheat, so with four in the shed
only four of the five animals placed that day can eat: `feed 4/5` and `care 4/5` are the same defect
one step downstream, and every later day inherits the herd's missed night.

The assertion is on the HOUR, not the quantity. How much the bank affords is the affordability
rule's business and `_do_buy_product` fills only what the money covers; what this pins is that the
row is offered while the dawn bank is still intact.
"""
import collections
import kagg.plan as _PLAN
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = _PLAN.SHIPPED_PLAN
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def emitted():
    """`{day: [(hour, qty), ...]}` of every BUY_PRODUCT WHEAT the agent emits."""
    SA = importlib.import_module(MODULE)
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    out = collections.defaultdict(list)
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    for t in range(TPD * DAYS):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp[t]
        for o in (a0.get("market") or []):
            if o and o[0] == "BUY_PRODUCT" and o[1] == "WHEAT":
                out[t // TPD].append((t % TPD, int(o[2])))
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return dict(out)


def _rows():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): int((v.get("buys") or {}).get("WHEAT", 0)) for k, v in raw.items()}


def test_the_premise_some_day_buys_wheat(emitted):
    """Guard. With no wheat row in range the assertion below is vacuous."""
    rows = _rows()
    assert [d for d in range(DAYS) if rows.get(d, 0) > 0], f"no wheat row in d0-d{DAYS - 1}"


@pytest.mark.parametrize("day", range(DAYS))
def test_the_wheat_row_is_offered_at_hour_zero(emitted, day):
    """A day whose row buys wheat offers some of it at hour 0, before the bank is spent."""
    rows = _rows()
    want = rows.get(day, 0)
    if want <= 0:
        pytest.skip(f"d{day} buys no wheat")
    got = emitted.get(day, [])
    assert got, f"d{day} row wants {want} wheat and emitted no order at all"
    first = min(h for h, _q in got)
    assert first == 0, (
        f"d{day} row wants {want} wheat; first order is at h{first:02d}, after the day has already "
        f"spent its dawn bank on hires and animals. Orders: {got}")
