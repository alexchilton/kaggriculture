"""Produce the row is selling must reach the SHED on the day it is harvested -- from d10.

**The defect, traced end to end on 91422988, seed 11, day 10.** The row asks for
`FERTILIZER 12, MELON 18, MILK 6`. Reading `state[0].observation.private` -- which is where the shed
and the unit inventories actually live, not `farms` -- the shed is EMPTY from h1 to h23:

    h12  SHED={}  u4{FERTILIZER:2}  u5{FERTILIZER:2, MILK:3}  u9{MELON:6}
    h16  SHED={}  u4{FERTILIZER:3}  u5{FERTILIZER:2, MILK:3}  u9{MELON:12}
    h23  SHED={}  HANDS={MELON: 12}

u9 harvests twelve melons between h12 and h15 and carries them to dusk. The market reads the shed
and nothing else, so none of it can be sold; the bank sits at $37 from h11 to h20; the d10 wheat
order is never placed; the cow at (4,2) goes unfed on d10 AND d11, and `consecutive_unfed >= 2`
removes it on d13 (`kaggriculture.py:786`).

**Why the obvious fix does not work, and why this one does.** Rule 3 of `cover.materialise` already
ends a tour at the shed, but `cover.plan` only appends it if it happens to fit in the leftover turns.
Charging it for every tour is a measured loss -- HARVEST 325 -> 301, PASS 834 -> 956. Charging it
whenever the tour ends holding something in `wanted` was also tried and did not fix this at all,
because it keyed on `Job.gives`, the predicted QUANTITY, which `predict_yield` returns empty whenever
`yield_units` is still 0 at dawn -- the normal state of a crop that ripens during the day, i.e.
precisely these melons.

`Job.products` is the fix: WHICH product the tile will yield is knowable at dawn even when the
quantity is not. So the reserve fires only for tours that will harvest something today's row sells.

Measured over six seeds, whole 30-day season, animals lost:

    reserve OFF        22 lost   mean $57,253
    reserve from d7     8 lost   mean $53,447
    reserve from d10   10 lost   mean $60,671     <-- shipped

**d10, not d7, and d0-d9 is untouchable.** Alex's instruction and the measurement agree: the opening
is where the money is made, and reserving turns there costs more harvesting and watering than the
herd is worth. At d7 the season loses $7k to save two more animals. The tape loses none, so 10 is
not the floor -- but it is 22 fewer than shipping without it, for +$3,418 a season.
"""
import collections
import importlib
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"


def _thin():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): {k2: v2 for k2, v2 in r.items() if k2 not in TAPE_ONLY}
            for k, r in raw.items()}


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]


def test_the_reserve_reads_the_product_not_the_predicted_quantity():
    """`Job.products` must name a crop whose `yield_units` is still 0. That is the whole fix.

    Red if `products` is dropped or derived from `gives`: a melon tile at dawn predicts nothing, so
    a quantity-based test cannot see it, and the tour never gets its trip home.
    """
    CV = importlib.import_module("kagg.search.cover")

    class N:
        tile = (2, 3)
        ops = (("HARVEST", None),)

    unripe = [[{} for _ in range(10)] for _ in range(10)]
    unripe[3][2] = {"kind": "PLANT", "crop": "MELON", "yield_units": 0}

    assert CV.predict_yield(N, unripe) == {}, (
        "the fixture is wrong: this tile is supposed to predict NOTHING, which is the case the bug "
        "lives in. If it predicts a quantity the test cannot discriminate."
    )
    assert CV.yield_products(N, unripe) == frozenset({"MELON"}), (
        "an unripe melon tile must still declare that it will yield MELON. Without that the reserve "
        "is blind to exactly the tours that strand produce."
    )


def test_the_reserve_never_fires_before_day_ten():
    """d0-d9 must be untouched. Alex: 'you can not regress the earlier days or you already lose.'

    Checked on the constant rather than through a season, because a season test would pass by luck
    on a day that happened to have no wanted harvest.
    """
    CV = importlib.import_module("kagg.search.cover")
    assert CV.RESERVE_FROM_DAY >= 10, (
        f"RESERVE_FROM_DAY is {CV.RESERVE_FROM_DAY}. At d7 the six-seed season measured "
        "$53,447 against $60,671 at d10: the reserve takes its turns out of the harvesting and "
        "watering that funds the whole game."
    )


@pytest.mark.slow
def test_the_herd_survives_better_with_the_reserve_than_without():
    """The season claim, on one seed, both ways. Seed 11 loses 3 animals without and 0 with."""
    from kaggle_environments import make

    CV = importlib.import_module("kagg.search.cover")
    SA = importlib.import_module(MODULE)
    opp = _opponent()

    def herd(f):
        c = collections.Counter()
        for row in f["tiles"]:
            for cell in row:
                if isinstance(cell, dict) and cell.get("animal"):
                    c[cell["animal"]] += 1
        return c

    def losses(from_day):
        was, CV.RESERVE_FROM_DAY = CV.RESERVE_FROM_DAY, from_day
        try:
            env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0},
                       debug=True)
            env.reset(2)
            agent = SA.make_agent(_thin(), 0, router=True)
            prev, lost = collections.Counter(), 0
            for t in range(len(opp)):
                o0 = env.state[0].observation
                a0, a1 = agent(o0), opp[t]
                f = o0["farms"][0]
                if t % 24 == 0:
                    cur = herd(f)
                    lost += sum(max(0, prev[k] - cur[k]) for k in set(prev) | set(cur))
                    prev = cur
                n0 = len(f.get("hands") or [])
                n1 = len(o0["farms"][1].get("hands") or [])
                env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                           "market": a0["market"]},
                          {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                           "market": a1["market"]}])
            return lost
        finally:
            CV.RESERVE_FROM_DAY = was

    off, on = losses(99), losses(10)
    assert on < off, (
        f"seed 11 lost {on} animals with the reserve and {off} without. It was 0 against 3 when "
        "this was written; if they are equal the reserve has stopped reaching the stranded harvest."
    )
