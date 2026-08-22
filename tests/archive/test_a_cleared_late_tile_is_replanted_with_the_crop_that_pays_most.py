"""The late replant must take the best-priced crop, not the first one the budget happens to list.

`plant_prize` already ranks the late season correctly: from d26 a CARROT is worth $70 and a WHEAT
$50, because carrot's `max_yield_day` is 3 against wheat's 4 and only carrot can still finish. The
crop the leader plants in that window in all 16 of his downloaded games is CARROT
(`docs/kawashigi_one_board_2026-08-13.md`).

`build_nodes` picked with `next(...)`, which returns the first crop in the budget's iteration order
with any positive prize -- so wheat won on dict order while pricing $20 lower.
"""
import pytest

from kagg.search import router as R


def test_plant_prize_ranks_carrot_over_wheat_from_day_26():
    """The premise. If this fails the fix below is aimed at the wrong function."""
    assert R.plant_prize("CARROT", 25) < R.plant_prize("WHEAT", 25), "wheat should lead before d26"
    assert R.plant_prize("CARROT", 26) > R.plant_prize("WHEAT", 26), "carrot must lead from d26"
    assert R.plant_prize("CARROT", 27) > R.plant_prize("WHEAT", 27)
    assert R.plant_prize("CARROT", 28) == 0, "nothing is plantable on d28"


@pytest.mark.parametrize("order", [("WHEAT", "CARROT"), ("CARROT", "WHEAT")])
def test_the_replant_takes_carrot_at_day_26_whatever_order_the_budget_lists(order):
    """The defect: the choice must not depend on the budget dict's iteration order."""
    replant = {c: 1 for c in order}
    chosen = R._best_replant_crop(replant, 26)
    assert chosen == "CARROT", (
        "at d26 carrot pays %d and wheat %d, but the budget order picked %s"
        % (R.plant_prize("CARROT", 26), R.plant_prize("WHEAT", 26), chosen))


def test_the_replant_still_takes_wheat_before_the_crossover():
    """Guards the other side: this must not become "always carrot"."""
    assert R._best_replant_crop({"WHEAT": 1, "CARROT": 1}, 22) == "WHEAT"


def test_a_crop_the_season_cannot_finish_is_never_chosen():
    assert R._best_replant_crop({"MELON": 5, "STRAWBERRY": 5}, 26) is None
    assert R._best_replant_crop({"WHEAT": 0, "CARROT": 1}, 26) == "CARROT", "a zero budget is spent"
    assert R._best_replant_crop({"CARROT": 1}, 28) is None, "d28 is past every window"
