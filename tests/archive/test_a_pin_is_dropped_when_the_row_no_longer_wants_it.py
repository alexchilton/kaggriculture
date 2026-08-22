"""`_refresh_pins` must drop a PLANT pin the cumulative row no longer wants.

The sweep at the top of `_refresh_pins` pops a pin for exactly three reasons: the tile filled, the
crop expired (`plant_prize <= 0`), or the land was lost. There is no rule for *the row is already
met*, and the seating loop below it only ever ADDS -- `range(qty - planted - live)` is empty when the
count is negative, it never removes. So a pin can only leave by being spent or invalidated.

That is stable while OUR units are the only thing that plants. It leaks the moment anything else
fills the ground, which is what a replayed day is: the planner is driven every turn and its answer
thrown away, so it pins `(4,8)` while the tape sows `(7,3)`. The tape's crop credits
`state["planted"]`, the pin on `(4,8)` is still empty ground, and nothing reconciles the two.

Measured 2026-08-18, strawberry arm, own seed 70683142, replay d4-d11:

    d10 dawn   want 19  planted 19  PLANT pins 1                       surplus 1
    d12 dawn   want 39  planted 37  PLANT pins 4 at (3,8) (4,8) (3,9) (4,9)   surplus 2

d12's row asks for 2 strawberry and the board plants 4. Each one drags a chained WATER
(`router.PLANT_THEN_WATER`), and each is a tile still standing at d29 for a harvest we never reach.
"""
import collections

import pytest

from kagg.search import schedule_agent as SA


@pytest.fixture
def board():
    """An empty NW quadrant, and the crop counts the strawberry arm carries into d12."""
    n = SA.R.BOARD_SIZE if hasattr(SA.R, "BOARD_SIZE") else 10
    tiles = [[None] * n for _ in range(n)]
    unlocked = {SA.R.quadrant_of(0, 0)}
    # Four strawberry pins standing, on ground the sweep will not reclaim.
    spots = [t for t in SA.RT.field_order(unlocked)][:4]
    pins = {tuple(t): ("PLANT", "STRAWBERRY", SA.RT.plant_prize("STRAWBERRY", 12)) for t in spots}
    state = {"pins": pins,
             "planted": collections.Counter({"STRAWBERRY": 37, "WHEAT": 27, "MELON": 12}),
             "bought": collections.Counter(),
             "pen_for": {}}
    # Cumulative rows to d12: the tape has met all but two of the strawberry.
    sched = {0: {"plants": ["STRAWBERRY"] * 37}, 12: {"plants": ["STRAWBERRY"] * 2}}
    return state, sched, tiles, unlocked


def test_the_row_is_already_met_so_the_surplus_pins_go(board):
    """39 asked cumulatively, 37 in the ground: two pins may stand, not four."""
    state, sched, tiles, unlocked = board
    pins = SA._refresh_pins(state, sched, 12, tiles, unlocked)
    straw = collections.Counter(v[1] for v in pins.values() if v[0] == "PLANT")["STRAWBERRY"]
    assert straw == 2, (
        f"{straw} strawberry pinned against a row that still wants 2; a pin the row no longer "
        "wants is never dropped, so the day plants it anyway")


def test_a_pin_the_row_still_wants_is_kept(board):
    """The trim must not eat live commitments -- pinning exists to stop the ground wandering."""
    state, sched, tiles, unlocked = board
    state["planted"] = collections.Counter({"STRAWBERRY": 35})
    sched = {0: {"plants": ["STRAWBERRY"] * 39}}
    pins = SA._refresh_pins(state, sched, 12, tiles, unlocked)
    straw = collections.Counter(v[1] for v in pins.values() if v[0] == "PLANT")["STRAWBERRY"]
    assert straw == 4, f"{straw} pinned where the row wants 4 outstanding"
