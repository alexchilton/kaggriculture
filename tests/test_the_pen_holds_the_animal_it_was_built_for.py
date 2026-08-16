"""A pen is built FOR an animal. Place that animal in it.

## The bug

`_refresh_pins` sites pens one at a time and stamps each one with the animal the schedule's
`places` row asked for -- `pins[spot] = ("BUILD", a, cost)`. The near ground is pinned first, so
the row's ORDER decides which animal gets the short walk. Seb's day-0 row is

    places: ['SHEEP', 'SHEEP', 'COW', 'COW']

sheep first, and his board reads exactly that: `SHEEP@(4,4)` at distance 0 from a depot and
`SHEEP@(4,3)` at distance 1.

Ours does not, because the moment the pen is BUILT the pin pops -- the tile is no longer `None`,
so `_refresh_pins` drops it -- and the animal is then re-derived from scratch by `build_nodes`,
which walks `R.ANIMAL_NAMES = ["GOOSE", "COW", "SHEEP"]` and takes the first match in the shed.
COW precedes SHEEP, so a COW wins every PASTURE, every time. Measured, seed 11, weeds off:

    Seb   SHEEP@(4,4)d0  SHEEP@(4,3)d1  COW@(3,3)d2  COW@(2,3)d3    sheep walk 0 + 1 = 1
    ours  COW@(4,4)d0    SHEEP@(3,4)d1  COW@(2,4)d2  SHEEP@(1,4)d3  sheep walk 1 + 3 = 4

The two blocks are the SAME total distance -- 22 either way at day 0 -- so this is not a shape
problem and no siting rule fixes it. It is an identity problem: the pen remembers nothing.

The cost lands on day 6, the first wool harvest, where the sheep sit three steps from the shed
instead of one and the wool has to be carried in rather than dropped where it stands.

## What this is NOT

`build_nodes` already documents a REJECTED fix: rank the tied animals by same-turn value.
That measured **-$5,676** on the 12-seed ladder, because the season wants 8 COW against 6 SHEEP
and a value rank reallocates far more pastures than the one it was diagnosed on.

This is the opposite of that. It ranks nothing and prices nothing. It honours the assignment the
schedule already made and `_refresh_pins` already recorded, and it falls straight back to the old
`ANIMAL_NAMES` order for any pen that has no reservation.
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import router as RT


def _place(nodes, tile):
    for n in nodes:
        if tuple(n.tile) == tile:
            return [(o, i) for o, i in n.ops if o == "PLACE"]
    return []


def test_a_pen_reserved_for_a_sheep_gets_the_sheep_not_the_first_name_in_the_list():
    """The whole bug in one assertion: COW precedes SHEEP in `ANIMAL_NAMES`."""
    board = [[None] * 5 for _ in range(5)]
    board[4][4] = {"kind": "PASTURE"}
    nodes = RT.build_nodes(board, day=0, shed={"COW": 1, "SHEEP": 1}, carried={},
                           unlocked=("NW",), pinned={}, hour=0,
                           pen_for={(4, 4): "SHEEP"})
    assert _place(nodes, (4, 4)) == [("PLACE", "SHEEP")]


def test_an_unreserved_pen_still_takes_the_old_order():
    """The fallback is the shipped behaviour, unchanged. Nothing else may move."""
    board = [[None] * 5 for _ in range(5)]
    board[4][4] = {"kind": "PASTURE"}
    nodes = RT.build_nodes(board, day=0, shed={"COW": 1, "SHEEP": 1}, carried={},
                           unlocked=("NW",), pinned={}, hour=0, pen_for={})
    assert _place(nodes, (4, 4)) == [("PLACE", "COW")]


def test_a_reservation_the_shed_cannot_fill_falls_back_rather_than_stalling():
    """A pen reserved for a SHEEP with no SHEEP anywhere must not sit empty holding the slot.

    The rejected value-rank fix and this one share one failure mode -- refusing an available
    animal because a better one is imagined -- and that is what left a SHEEP idle in the shed for
    three days. A reservation is a preference, never a lock.
    """
    board = [[None] * 5 for _ in range(5)]
    board[4][4] = {"kind": "PASTURE"}
    nodes = RT.build_nodes(board, day=0, shed={"COW": 1}, carried={},
                           unlocked=("NW",), pinned={}, hour=0,
                           pen_for={(4, 4): "SHEEP"})
    assert _place(nodes, (4, 4)) == [("PLACE", "COW")]


def test_a_reservation_cannot_put_an_animal_in_the_wrong_structure():
    """GOOSE needs a COOP. Reserving a PASTURE for one must be ignored, not obeyed."""
    board = [[None] * 5 for _ in range(5)]
    board[4][4] = {"kind": "PASTURE"}
    nodes = RT.build_nodes(board, day=0, shed={"GOOSE": 1, "COW": 1}, carried={},
                           unlocked=("NW",), pinned={}, hour=0,
                           pen_for={(4, 4): "GOOSE"})
    assert _place(nodes, (4, 4)) == [("PLACE", "COW")]


def test_a_reservation_is_honoured_from_a_hand_as_well_as_from_the_shed():
    """`build_nodes` gates on `shed or carried`; the reservation must read both."""
    board = [[None] * 5 for _ in range(5)]
    board[4][4] = {"kind": "PASTURE"}
    nodes = RT.build_nodes(board, day=0, shed={"COW": 1}, carried={"SHEEP": 1},
                           unlocked=("NW",), pinned={}, hour=0,
                           pen_for={(4, 4): "SHEEP"})
    assert _place(nodes, (4, 4)) == [("PLACE", "SHEEP")]


@pytest.mark.slow
def test_the_pen_nearest_the_shed_holds_a_sheep_by_the_end_of_day_zero():
    """End to end, on the real board: Seb's row says SHEEP first, so (4,4) is a SHEEP.

    This is the assertion the whole change exists for. The unit tests above prove the mechanism;
    only this one proves it survives the schedule, the pins and the executor.
    """
    import json
    import pathlib

    from kaggle_environments import make

    from kagg.search import schedule_agent as SA
    from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE

    replay, schedule, team = TAPES[DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    assert (sched[0].get("places") or [])[0] == "SHEEP", "the row this test rests on changed"
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = tape_policy(replay, team, 1)
    for t in range(24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])

    tiles = env.state[0].observation["farms"][0]["tiles"]
    cell = tiles[4][4]
    assert isinstance(cell, dict), f"(4,4) is not a pen at all: {cell!r}"
    assert cell.get("animal") == "SHEEP", f"(4,4) holds {cell.get('animal')!r}, not SHEEP"
