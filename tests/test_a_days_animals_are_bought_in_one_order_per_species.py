"""Four sheep are one order, not four.

`maxMarketOrdersPerTurn` is 10 (`kaggriculture.py:538`) and `_parse_order` accepts any `n > 0`
(`:626-635`), committing one animal per unit-iteration of the lockstep loop. So `BUY_ANIMAL SHEEP 4`
buys four sheep in ONE slot, and the agent was spending four.

Measured on the Victor grid, seed 11, day 0 hour 0:

    OURS  HIRE HIRE HIRE HIRE  BUY_ANIMAL COW 1  BUY_ANIMAL SHEEP 1 x4          9 of 10 slots
    TAPE  BUY_PRODUCT WHEAT 11  HIRE x4  BUY_ANIMAL COW 1  BUY_ANIMAL SHEEP 4
          BUY_SEED WHEAT 5  BUY_SEED MELON 5                                    9 of 10 slots

He fits the wheat and both seed rows into the same turn; we push them to h01 and later. The day's
whole divergence follows -- `place 4/5`, `sheep 3/4`, `feed 4/5`, `care 4/5`, `sell 0/6`,
`buy_product 4/11`.

The assertion is on SLOTS PER SPECIES, not on the quantity: how many head the bank affords is the
existing affordability rule's business and is not what this changes.
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
    """`{(day, hour): [market order, ...]}` for d0-d12 of the real agent on the real board."""
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
        out[(t // TPD, t % TPD)] = [list(o) for o in (a0.get("market") or []) if o]
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return out


def test_the_premise_a_day_buys_more_than_one_of_some_species(emitted):
    """Guard. If no turn ever buys 2+ of a species the assertion below is vacuous."""
    most = 0
    for orders in emitted.values():
        c = collections.Counter(o[1] for o in orders if o[0] == "BUY_ANIMAL")
        most = max([most] + [sum(int(o[2]) for o in orders
                                 if o[0] == "BUY_ANIMAL" and o[1] == s) for s in c])
    assert most >= 2, f"no turn bought 2+ head of any species in d0-d12; most was {most}"


@pytest.mark.parametrize("day", range(DAYS))
def test_a_turns_animal_purchases_take_one_slot_per_species(emitted, day):
    """One BUY_ANIMAL order per species per turn. Four sheep is `SHEEP 4`, not `SHEEP 1` x4."""
    bad = []
    for hour in range(TPD):
        orders = emitted.get((day, hour), [])
        slots = collections.Counter(o[1] for o in orders if o[0] == "BUY_ANIMAL")
        for species, n in slots.items():
            if n > 1:
                head = sum(int(o[2]) for o in orders
                           if o[0] == "BUY_ANIMAL" and o[1] == species)
                bad.append(f"d{day} h{hour:02d}: {n} separate {species} orders for {head} head, "
                           f"in a turn using {len(orders)} of 10 slots")
    assert not bad, "\n".join(bad)
