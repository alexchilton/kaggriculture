"""A crop's ground is chosen once, for the whole season, instead of a tile at a time.

`_refresh_pins` picks ground from the days it has already SEEN:

    for d in sorted(sched):
        if d <= day:                              # only days up to TODAY
            want.update(sched[d].get("plants") or [])
    ...
        spot = _next_ground(order, tiles, taken)  # first free tile in sweep order

So it never reserves ground for a crop that is due later, and a crop planted on d0, d3 and d9 is
separated on the board by whatever the OTHER crops claimed on d1 and d2. Measured on our own board
at d6 dawn, seed 11, against tape 91422988 (`probe_blocks`):

    OURS                                 SEB
    STRAWBERRY  10 tiles   6 islands     STRAWBERRY   7 tiles  1 island
    WHEAT        2 tiles   2 islands     WHEAT        7 tiles  2 islands

Six islands over ten tiles is a farm the crop hands cross and re-cross. Every square of it is a
separate walk, and d4 is exactly where the crop crew runs out of turns.

Everything the choice needs -- every day's `plants` and `builds`, and the `land` rows saying when
each quadrant arrives -- is in the schedule before turn 0, so it can be made once, pre-game.

**The matrix is NOT wired into the agent.** It was, on 2026-08-10, and it lost -- see the module
docstring in `kagg/search/board_layout.py` for the measurement. So this asserts the property the
planner is supposed to have and nothing about what the agent currently does, deliberately: the
wiring was deleted rather than left behind a flag.
"""
import importlib
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


@pytest.fixture(scope="module")
def sched():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}


def test_each_crop_reserves_one_unbroken_run_of_the_sweep(sched):
    """Contiguity is asserted ALONG THE SWEEP, not as 4-connectivity on the grid.

    `router.DEPOT_RING_FIRST` is 1, so `field_order` is sorted by distance to the shed and a
    "block" of consecutive sweep tiles is a RING around the shed, not a rectangle. A ring is thin,
    so 4-connectivity scores it as many islands while it is in fact the cheapest possible shape to
    walk in the order the hands actually walk it. Asserting adjacency here would demand a layout
    that fights the router.
    """
    BL = importlib.import_module("kagg.search.board_layout")
    RT = importlib.import_module("kagg.search.router")

    layout = BL.plan_board(sched)
    bought = sum(int((sched[d] or {}).get("land") or 0) for d in sorted(sched))
    # Positions in the PLANTABLE sweep, with the pen squares taken out. Pens are permanent and are
    # sited first, so they sit in the middle of the sweep and split any run measured against the
    # raw `field_order`. That is not the crop being fragmented -- a hand walking the sweep passes
    # the pen either way -- so counting it as a gap would demand a layout that puts every pen at
    # one end of the board, which is the opposite of what a pen wants.
    pens = {t for t, v in layout.items() if v[0] == "BUILD"}
    order = {t: i for i, t in enumerate(t for t in RT.field_order(BL.quads_owned(bought))
                                        if t not in pens)}

    broken = {}
    for crop in {v[1] for v in layout.values() if v[0] == "PLANT"}:
        idx = sorted(order[t] for t, v in layout.items()
                     if v == ("PLANT", crop) and t in order)
        if idx and idx[-1] - idx[0] + 1 != len(idx):
            gaps = [(a, b) for a, b in zip(idx, idx[1:]) if b != a + 1]
            broken[crop] = (len(idx), idx[0], idx[-1], gaps)
    assert not broken, "\n".join(
        f"{c}: {n} tiles spread over sweep positions {lo}..{hi}, broken at {gaps}"
        for c, (n, lo, hi, gaps) in sorted(broken.items()))
