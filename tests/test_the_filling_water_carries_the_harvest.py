"""The day-10 melon does not reach the shed late. It is not RIPE until dusk, and that is priced.

Measured, seed 11 day 10, `scripts/when_the_melon_fills.py` (both seats, same 18 melons):

    tile reaches 6/6 (harvestable) at    SEB   (4,2)=h6   (3,1)=h9   (4,1)=h9
                                         OURS  (2,0)=h15  (1,0)=h16  (0,0)=h18

Both sides wake on day 10 with three MELON tiles sitting at **5/6**. MELON is a one-shot
(`max_yield` 6, `max_yield_day` 12) and `_one_shot_is_finished` refuses HARVEST while `room > 0` --
correctly, because HARVEST demolishes the tile. So neither side can harvest until one more WATER
fills it. Ours harvest at h17/h19/h20, which is one to three turns after the fill: the HARVEST is
prompt and the **WATER** is what runs seven hours late. Seven prior arms treated the delivery leg,
which is two steps downstream of this.

The reason the water runs late is a price. `crop_ops` gives an in-window one-shot water
`price * (2 if fertilized else 1)`, i.e. $250 -- the single unit of yield it adds. That is right for
a water with room to spare and wrong for the LAST one, which is also the only thing standing between
the tile and a $1,500 HARVEST. Meanwhile an out-of-window survival water on an immature melon is
priced at `_crop_remaining`, the whole tile, $1,250-$1,500. So the planner ranks insurance on a tile
that cannot yield for two more days **five times above** the one water that unlocks same-day money,
and `plan_routes` -- which sorts by prize and scores by `prize / cost` -- schedules it at dusk.
"""
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import router as RT

import test_router as TR
from test_router import kg                                                   # noqa: F401  (fixture)


def ripe_melon(**kw):
    """A day-10 melon exactly as seed 11 leaves it at dawn: age 10, 5 of 6 units, one water short."""
    return dict(dict(kind="PLANT", crop="MELON", planted_day=0, watered_today=False,
                     consecutive_unwatered=0, yield_units=5, fertilized_until_day=-1), **kw)


def test_the_water_that_fills_a_one_shot_offers_the_harvest_it_unlocks():
    """A visit that fills the tile can harvest it on the next turn, so the node is worth both.

    The tile is at 5/6 and one plain water takes it to 6/6, at which point `_one_shot_is_finished`
    returns True and the HARVEST is legal. The unit is standing there. Nothing else has to happen.
    Yet the node offers WATER alone, so the planner sees $250 where the visit is worth $1,750.
    """
    cell = ripe_melon()
    ops = RT.crop_ops(cell, 10, have_fertilizer=False)
    assert [o for o, _i, _p in ops] == ["WATER", "HARVEST"], (
        f"the filling water must carry its harvest: {ops}")
    # $1,750 for a visit that banks $1,500 -- the WATER already carries the unit it adds, so the
    # full tile bills it twice. That was tried as an arm and MEASURED WORSE (day 10 money -1,548 ->
    # -3,082): the surplus $250 is the only thing breaking the tie against an immature melon's
    # $1,500 survival water. See the comment at the emission site.
    assert [p for _o, _i, p in ops] == [250, 6 * 250], ops


def test_a_filling_water_outranks_survival_water_on_a_tile_that_cannot_yield_yet():
    """The exact day-10 ranking, in one assert.

    (0,0) is ripe and one water from a $1,500 harvest. (1,1) is an age-5 melon whose window has not
    opened: watering it adds no yield at all today and only stops it weeding tonight. The ripe tile
    must be the more valuable node.
    """
    ripe = RT.Node((0, 0), RT.crop_ops(ripe_melon(), 10, have_fertilizer=False))
    immature = dict(kind="PLANT", crop="MELON", planted_day=5, watered_today=False,
                    consecutive_unwatered=1, yield_units=0, fertilized_until_day=-1)
    survival = RT.Node((1, 1), RT.crop_ops(immature, 10, have_fertilizer=False))
    assert [o for o, _i in survival.ops] == ["WATER"], survival.ops
    assert ripe.prize > survival.prize, (
        f"a tile one water from harvest ({ripe}) must outrank insurance on one that cannot yield "
        f"for two more days ({survival})")


def test_the_pair_actually_executes_back_to_back_on_one_stop(kg):
    """A price is only worth having if the stop can spend it, so drive the pair for real.

    `_live_ops` re-derives the ops at the tile every turn, so the unit waters (tile goes to 6/6),
    and on the very next turn `room == 0` makes `_one_shot_is_finished` true and the SAME stop emits
    the HARVEST. Applied here with the reference's own `_apply_unit_action`, no market and no
    opponent, so the only thing that can fail is the pair itself.

    **This test passes with `FILLING_WATER` off too, and that is the point of it.** The other two go
    red when the flag is reverted; this one does not, because `_live_ops` already re-derived HARVEST
    at the tile the turn after the water and the stop was never popped. So the pair was always
    executable and the execution was never the defect -- only the planner's view of what the visit
    was worth, and therefore when it got scheduled. Recorded as a non-discriminating test on purpose,
    so a later session does not read it as cover for the flag.
    """
    board = TR.blank_board()
    # `micro` starts at day 0, so age the tile backwards to reach the same age-10, 5-of-6 state.
    board[0][3] = ripe_melon(planted_day=-10)        # (3,0), four steps from the spawn tile
    trace = []
    tally, farm, private = TR.micro(kg, board, TR.empty_sched(), days=1, hands=0,
                                    shed={}, trace=trace)
    ops = [(h, a) for _d, h, _u, a in trace if a[0] in ("WATER", "HARVEST")]
    assert [a[0] for _h, a in ops] == ["WATER", "HARVEST"], ops
    assert ops[1][0] == ops[0][0] + 1, f"the harvest must be the turn after the water: {ops}"
    assert board[0][3] is None, "HARVEST demolishes a one-shot tile"
    held = int(private["shed"].get("MELON", 0)) + sum(
        int(iv.get("MELON", 0)) for iv in private["inventories"])
    assert held == 6, f"the whole tile must come off in one visit, got {held}"
