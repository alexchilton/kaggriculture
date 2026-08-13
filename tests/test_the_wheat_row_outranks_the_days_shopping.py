"""At hour 0 the day's wheat row sits ahead of the hires, the animals and the seeds.

`buy_product` is an exact FILL, not an offer. `_process_market` walks a turn's orders slot by slot
and `_do_buy_product` re-checks the bank per unit (`kaggriculture.py:666-673`), so an order in a
late slot is paid for out of whatever the earlier slots left behind.

Measured on the Victor grid, seed 11, day 0 hour 0 -- identical quantity, different slot:

    OURS  HIRE x4  BUY_ANIMAL COW 1  BUY_ANIMAL SHEEP 4  BUY_SEED MELON 5
          BUY_SEED WHEAT 5  BUY_PRODUCT WHEAT 11          -> 5 of 11 clear
    TAPE  BUY_PRODUCT WHEAT 11  HIRE x4  BUY_ANIMAL COW 1  BUY_ANIMAL SHEEP 4
          BUY_SEED WHEAT 5  BUY_SEED MELON 5              -> 11 of 11 clear

He spends slot 1 on the wheat against the full $3,000; we reach it in slot 9 with $600 of estimate
and $130-odd of real bank left. A FEED eats one wheat, so the shortfall is what caps the herd's
first night.

**SELLs are exempt and must stay in front.** A SELL settles before any atomic order in a later slot
(`schedule_agent:3062`), which is what lets a thin day fund its own purchases -- the tape buys a
$1,000 parcel on a $718 bank that way. This only reorders the wheat against HIRE, BUY_ANIMAL and
BUY_SEED.

Hour 0 only. `HIRE_FIRST` is about the hour a hand is bought, not its slot within that hour, and
`_hire_cost` is a per-DAY fibonacci counter so the crew costs the same wherever in the turn it sits.
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
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 12
TPD = 24
BEHIND = ("HIRE", "BUY_ANIMAL", "BUY_SEED")


@pytest.fixture(scope="module")
def dawn_orders():
    """`{day: [order, ...]}` as emitted at hour 0."""
    SA = importlib.import_module(MODULE)
    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    out = {}
    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    for t in range(TPD * DAYS):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp[t]
        if t % TPD == 0:
            out[t // TPD] = [list(o) for o in (a0.get("market") or []) if o]
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return out


def test_the_premise_a_dawn_turn_buys_wheat_alongside_other_shopping(dawn_orders):
    """Guard. With no turn holding both a wheat buy and a hire/animal/seed this is vacuous."""
    days = [d for d, os in dawn_orders.items()
            if any(o[0] == "BUY_PRODUCT" and o[1] == "WHEAT" for o in os)
            and any(o[0] in BEHIND for o in os)]
    assert days, f"no dawn turn in d0-d{DAYS - 1} buys wheat next to a hire, animal or seed"


@pytest.mark.parametrize("day", range(DAYS))
def test_the_wheat_row_is_queued_before_the_hires_and_animals(dawn_orders, day):
    """The wheat order precedes every HIRE, BUY_ANIMAL and BUY_SEED in the same turn."""
    orders = dawn_orders.get(day) or []
    wheat = [i for i, o in enumerate(orders) if o[0] == "BUY_PRODUCT" and o[1] == "WHEAT"]
    others = [i for i, o in enumerate(orders) if o[0] in BEHIND]
    if not wheat or not others:
        pytest.skip(f"d{day} h00 has no wheat buy alongside other shopping")
    assert min(wheat) < min(others), (
        f"d{day} h00 queues wheat at slot {min(wheat)}, behind "
        f"{orders[min(others)][0]} at slot {min(others)}. Orders: "
        + " ".join(f"{o[0]}{'/' + str(o[1]) if len(o) > 1 else ''}"
                   f"{'x' + str(o[2]) if len(o) > 2 else ''}" for o in orders))
