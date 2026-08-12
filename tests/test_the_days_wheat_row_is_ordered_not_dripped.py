"""The schedule's wheat row is ordered, not metered one unit per turn.

`BUY_DRIP = 1` caps the schedule row at one unit a turn (`short = min(max(herd, min(owed,
BUY_DRIP)), FEED_TURN_CAP)`), so a row asking for 11 wheat becomes eleven separate orders spread
across the morning. Measured on the Victor grid, seed 11:

    d0 h00  OURS  (no wheat at all -- the slot went to four single-head animal orders)
            TAPE  BUY_PRODUCT WHEAT 11
    d2 h00  OURS  BUY_PRODUCT WHEAT 1     then 1 again at h01..h13, twelve orders
            TAPE  BUY_PRODUCT WHEAT 6

Two costs. The order slots -- ten a turn -- are spent on repeats, which is what pushed d0's seed
rows out of hour 0 entirely. And the wheat arrives through the morning instead of at dawn, so the
feed and the placements that need it wait.

The assertion is BINARY and on the FIRST order of the day: a row asking for more than one unit must
not open with an order of one. It deliberately says nothing about the quantity beyond that -- how
much the bank affords is the existing affordability rule's business, and `_do_buy_product` fills
only what the money covers anyway.

The herd top-up path is a separate mechanism (`FEED_TURN_CAP`, the `herd` term) and is not asserted
here; this is only about the schedule's own `buys` row.
"""
import collections
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = REPO / "data/seed_scripts/victor/schedule.json"
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent_1455mh"
SEED = 11
DAYS = 13
TPD = 24


@pytest.fixture(scope="module")
def emitted():
    """`{day: [(hour, qty), ...]}` for every BUY_PRODUCT WHEAT the agent emits in d0-d12."""
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


def test_the_premise_some_day_buys_more_than_one_wheat(emitted):
    """Guard. If no row in range asks for 2+ wheat the assertion below is vacuous."""
    rows = _rows()
    big = [d for d in range(DAYS) if rows.get(d, 0) > 1]
    assert big, f"no day in d0-d12 buys more than one wheat; rows={rows}"


@pytest.mark.parametrize("day", range(DAYS))
def test_a_wheat_row_is_not_metered_one_unit_per_turn(emitted, day):
    """A day whose row wants N>1 wheat must place at least one order of more than one unit.

    On the LARGEST order of the day, not the first. The first order is not always the row: the herd
    top-up path shares this emission and legitimately asks for one unit when that is all the ration
    needs, so asserting on `got[0]` was asserting which mechanism happened to fire first. d6 opens
    with a herd unit at h00 and sends the row's four at h14; that is the row not being dripped, which
    is what this file is about. The drip defect this replaces produced ALL ones and fails either way.
    """
    rows = _rows()
    want = rows.get(day, 0)
    if want <= 1:
        pytest.skip(f"d{day} buys {want} wheat")
    got = emitted.get(day, [])
    if not got:
        pytest.skip(f"d{day} emitted no wheat order at all -- a different defect")
    assert max(q for _h, q in got) > 1, (
        f"d{day} row wants {want} wheat and every order was a single unit; "
        f"the day emitted {len(got)} orders {got}")
