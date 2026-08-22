"""A one-tile ask the schedule dated to today must not lose every tile to the season-long ask.

`_replant` is a CUMULATIVE budget -- every `plants` row up to today, less what is planted and
pinned -- so on any late day it holds a large standing WHEAT figure alongside whatever small,
dated request the schedule made for today. `_best_replant_crop` ranked it purely by
`plant_prize`, and wheat prices $75 against carrot's $70 right up to d26:

    day       d21  d22  d23  d24  d25  d26  d27
    WHEAT      75   75   75   75   75   50   25
    CARROT     70   70   70   70   70   70   35

So wheat won every cleared tile on d21-d25 and carrot only ever got ground once wheat's prize
COLLAPSED. Measured on seed 11 with the leader's own carrot shape in the schedule -- one tile a day
on d21-d26 -- not one of the six landed inside its window:

    schedule asks   d21 d22 d23 d24 d25 d26
    actually planted             d26 (1), d27 (5)

A carrot sown on d26 reaches `max_yield_day` 3 on d29 and one sown on d27 never yields at all, so
all six were dead on arrival. The arm read -$837 and that number is six wasted seeds, not carrot.

The leader plants carrot on d21-d26 in all 66 downloaded games, 1-2 a day, BESIDE 4-11 wheat on the
same days (`docs/kawashigi_one_board_2026-08-13.md`). He is not choosing carrot over wheat on price
-- he is planting both, and the dated ask is what the schedule is FOR. A prize comparison between a
crop the plan wants today and a crop the plan wants eventually is a category error: the standing
budget is never exhausted, so it wins forever.
"""
import pytest

from kagg.search import router as R


def test_plant_prize_really_does_rank_wheat_over_carrot_before_the_crossover():
    """The premise. If wheat did not outrank carrot here there would be nothing to fix."""
    for day in (21, 22, 23, 24, 25):
        assert R.plant_prize("WHEAT", day) > R.plant_prize("CARROT", day), day
    assert R.plant_prize("CARROT", 26) > R.plant_prize("WHEAT", 26), "the crossover is d26"


@pytest.mark.parametrize("day", [21, 22, 23, 24, 25])
def test_a_crop_dated_to_today_takes_the_cleared_tile(day):
    """The defect: one carrot against a standing wheat budget, on a day the schedule asked for it.

    **`dated` carries the WHOLE row, not just the small ask, and the first version of this test did
    not.** It passed `dated={"CARROT": 1}` and went green while the agent, which passes the real
    row `{"WHEAT": 9, "CARROT": 1}`, was still byte-identical: the fix returned the first positive
    entry, so wheat won exactly as before. A test that hands the code a tidier input than the caller
    does is not testing the caller -- the standing `SCRIPT_OPS` lesson in CLAUDE.md, again.
    """
    replant = {"WHEAT": 60, "CARROT": 1}
    chosen = R._best_replant_crop(replant, day, dated={"WHEAT": 9, "CARROT": 1})
    assert chosen == "CARROT", (
        "the schedule asked for a carrot on d%d and there are 60 wheat outstanding; wheat prices "
        "%d against carrot's %d, so ranking on prize alone starves the dated ask forever -- "
        "we chose %s" % (day, R.plant_prize("WHEAT", day), R.plant_prize("CARROT", day), chosen))


def test_the_dated_row_is_served_scarcest_first():
    """The mechanism, stated directly: it is the COUNT that orders the row, not the price."""
    assert R._best_replant_crop({"WHEAT": 60, "CARROT": 3}, 22,
                                dated={"WHEAT": 9, "CARROT": 3}) == "CARROT"
    assert R._best_replant_crop({"WHEAT": 60, "CARROT": 3}, 22,
                                dated={"WHEAT": 2, "CARROT": 3}) == "WHEAT", (
        "when wheat is the smaller ask of the two it is the one at risk of being starved")


def test_the_standing_budget_still_takes_every_other_tile():
    """The other side: this must not become "always carrot".

    The dated ask is ONE tile. Once it is met the day's remaining cleared ground is wheat's, which
    is exactly what he does -- 1-2 carrot beside 4-11 wheat on the same day.
    """
    assert R._best_replant_crop({"WHEAT": 60, "CARROT": 1}, 22, dated={}) == "WHEAT"
    assert R._best_replant_crop({"WHEAT": 60, "CARROT": 0}, 22, dated={"CARROT": 1}) == "WHEAT", (
        "a dated ask with nothing left in the budget must not block the standing one")


def test_a_dated_crop_the_season_cannot_finish_is_still_refused():
    """Urgency does not override the window. A carrot dated to d28 can never yield."""
    assert R._best_replant_crop({"CARROT": 1}, 28, dated={"CARROT": 1}) is None
    assert R._best_replant_crop({"WHEAT": 5, "CARROT": 1}, 27, dated={"CARROT": 1}) == "CARROT", (
        "d27 still finishes a carrot (max_yield_day 3 lands d30... no: prize is nonzero), so it "
        "stays eligible while its prize is positive")


def test_the_default_is_unchanged_when_nothing_is_dated():
    """`dated` defaults to empty, so every existing call site keeps its old ranking exactly."""
    assert R._best_replant_crop({"WHEAT": 1, "CARROT": 1}, 22) == "WHEAT"
    assert R._best_replant_crop({"WHEAT": 1, "CARROT": 1}, 26) == "CARROT"
