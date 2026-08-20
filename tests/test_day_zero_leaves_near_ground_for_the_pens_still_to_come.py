"""Day 0 sows the ground day 2 and day 4 need for pens, so those pens land in the far corner.

`_refresh_pins` sites a pen with `_next_ground(order, tiles, taken)` -- the first tile in
`RT.field_order` that is neither built on nor pinned. `field_order` is ALREADY sorted by distance
from the shed:

    (3,4)1 (4,3)1 (2,4)2 (3,3)2 (4,2)2 (1,4)3 (2,3)3 (3,2)3 (4,1)3 (0,4)4 ... (2,0)6 (0,1)7

so `_nearest_ground` and `_next_ground` return the same tile, and `PEN_NEAREST_DEPOT_FROM_DAY` is a
no-op on this board -- `_nearest_ground` fires ONCE in twelve days, and sweeping the gate over
{0, 3, 5, 7, 9, 11, None} gives seven byte-identical seasons. The siting rule is not what puts a pen
in the corner, and neither is a PLANT pin: `pins` is EMPTY at every siting event. What is left is the
board itself.

Measured at d2 and d4 dawn. **The tape column here is read from the raw replay**
(`data/seed_scripts/kawashigi/92498144.json`, seat 0 -- `TeamNames ['カワシギ', 'Yusuke Hayashi']`,
rewards `[149998, 143436]`). It is NOT `farms[1]` of our own run: that seat is Yusuke Hayashi, and
reading it as the tape is a mistake this project has now made three times.

    d2  KAWASHIGI  pens 4  crops 19  free 2  ->  (4,2)d2  (2,4)d2
        OURS       pens 4  crops 19  free 2  ->  (1,0)d7  (0,0)d8

    d4  KAWASHIGI  pens 5  crops 19  free 1  ->  (4,2)d2      5th pen sited on (2,4), distance 2
        OURS       pens 4  crops 19  free 1                   5th pen sited on (0,0), distance 8

Same pen count, same crop count, same number of free squares. The ONLY difference is which two
squares stay free. His day-0 pen block is (4,4)(4,3)(3,4)(3,3) and ours is (4,4)(3,4)(4,3)(2,4) --
the same Manhattan sum of 4, which is what the `PEN_SPOTS` note already measured. He then plants
OUTWARD and holds the inner ring open; we plant the inner ring and hold the corner open.

    d0  pens sited  (4,4) (3,4) (4,3) (2,4)     distance 0, 1, 1, 2
    d2  pen  sited  (1,0)                       distance 7   <- second-worst tile on the board
    d4  pen  sited  (0,0)                       distance 8   <- worst tile on the board
    d6  pens sited  (5,4) (6,4)                 distance 1, 2   (the parcel reopens near ground)

A FEED is a shed round trip, so those two pens cost 14 and 16 turns of walking before any work. d7
reads `feed 6/9` with 48 idle turns: the crew cannot afford them at any hour, and the three unfed
pens are exactly (0,0), (1,0) and (4,3).

The two uses of a square are not comparable and day 0 treats them as if they were. A crop is watered
where it stands and never asks for a second trip; a pen is a round trip EVERY day for the rest of the
season, to feed, to care and to collect. Day 0 must leave near ground for the pens the schedule has
already told it are coming.

The assertion is that every pen is reachable, which is the consequence that breaks. It is not an
assertion about which tile gets which crop -- the tape's own layout is not the target, and its d0
pen block and ours are the same Manhattan sum.
"""
import collections
import importlib

import pytest

import kagg.plan as _PLAN

SEED = 11
LAST_DAY = 7
SHED = (4, 4)


def _d(t):
    return abs(t[0] - SHED[0]) + abs(t[1] - SHED[1])


@pytest.fixture(scope="module")
def sitings():
    """Every pen sited through d7, with any PLANT pins standing at that moment.

    The pin list is recorded and is always EMPTY -- that is the measurement that killed the first
    theory here, which was that a pasture and a strawberry compete for the same pinned square. They
    do not. The ground is gone because it is already sown, so the third element stays in the record
    as evidence rather than as a thing the assertion uses.
    """
    import scripts.breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)

    events = []
    original = SA._refresh_pins

    def spy(state, sc, day, tiles, unlocked, unlocked_shops=()):
        before_pens = set(state.get("pen_for") or {})
        plant_pins = [t for t, v in (state.get("pins") or {}).items() if v[0] == "PLANT"]
        out = original(state, sc, day, tiles, unlocked, unlocked_shops)
        for t in (state.get("pen_for") or {}):
            if t not in before_pens:
                events.append((day, t, sorted(plant_pins)))
        return out

    SA._refresh_pins = spy
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0),
                   debug=True)
        env.reset(2)
        ours = SA.make_agent(sched, 0, router=True)
        opp = B.tape_policy(replay, team, 1)
        for t in range((LAST_DAY + 1) * 24):
            o0, o1 = env.state[0].observation, env.state[1].observation
            o0.town["unlocked_shops"] = list(shops(t))
            a0, a1 = ours(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        SA._refresh_pins = original
    return events


@pytest.fixture(scope="module")
def board():
    """(free tiles, near tiles) on OUR board at d2 dawn -- the turn before d2 sites its pen."""
    import scripts.breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = _PLAN.load(schedule)
    shops = B.recorded_shops(replay)
    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    ours = SA.make_agent(sched, 0, router=True)
    opp = B.tape_policy(replay, team, 1)
    free, near, _crops = [], [], [0]
    for t in range(3 * 24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        o0.town["unlocked_shops"] = list(shops(t))
        if t == 2 * 24:
            _crops[0] = sum(1 for row in o0["farms"][0]["tiles"] for c in row
                            if isinstance(c, dict) and c.get("kind") == "PLANT")
            for y, row in enumerate(o0["farms"][0]["tiles"]):
                for x, c in enumerate(row):
                    if c == "LOCKED":
                        continue
                    if c is None:
                        free.append(((x, y), _d((x, y))))
                    elif _d((x, y)) <= 3:
                        near.append(((x, y), _d((x, y)),
                                     c.get("kind") if isinstance(c, dict) else str(c)))
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return sorted(free, key=lambda e: e[1]), sorted(near, key=lambda e: e[1]), _crops[0]


def test_the_premise_the_schedule_still_has_pens_to_build_after_day_zero(sitings):
    """Guard. If every pen goes up on d0 there is no later pen to keep ground for."""
    sched = _PLAN.load("data/seed_scripts/kawashigi/schedule.json")
    later = {int(d): int(sched[d].get("builds", 0) or 0) for d in sched
             if 0 < int(d) <= LAST_DAY and int(sched[d].get("builds", 0) or 0)}
    assert later, (
        f"the schedule builds no pen between d1 and d{LAST_DAY}, so day 0 owes the board nothing "
        "and this test is measuring nothing")


def test_the_premise_holding_ground_back_did_not_cost_a_planting(board):
    """Guard. Keeping squares open for pens is only free if the row still gets sown.

    This is the risk the reservation carries and the reason it is a preference rather than a lock:
    `_refresh_pins` falls back to the held squares rather than leave a crop unsown. Kawashigi stands
    19 crops at d2 dawn on the same 25-tile board, so anything below that is ground traded away.
    """
    _free, _near, crops = board
    assert crops >= 19, (
        f"d2 dawn stands {crops} crops against Kawashigi's 19 on the same board -- holding ground "
        "back for the pens cost a planting, which is not a trade worth making: a crop in the ground "
        "today beats a pen sited well in two days")


def test_every_pen_can_be_reached_and_returned_from_inside_a_day(sitings):
    """The consequence, stated as the thing that actually breaks: a feed is a shed round trip, so a
    pen at distance 8 costs 16 turns of walking plus the draw and the ops."""
    far = [(d, t, _d(t)) for d, t, _plants in sitings if _d(t) > 4]
    assert not far, (
        f"pens sited beyond a 4-square reach: {far}. A FEED is a round trip from the shed, so a pen "
        f"at distance 8 is 16 turns of walking before any work; d7 reads `feed 6/9` with 48 idle "
        "turns because the crew cannot afford the walk at any hour of the day.")
