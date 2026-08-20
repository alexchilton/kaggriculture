"""A zero-drain product (MELON: no shop stocks it, town centre takes 1/day) is a RACE, not a spread.

The optimiser's `water_fill` sells down to the drain rate and liquidates on d29. For melon that
means trickling 1/day and dumping the rest into a dead book on the last day -- the plan it calls
"optimal" earns LESS than the shipped agent's own front-load, which is how the release table came
to read melon at -$11,929. The release policy must front-load a no-drain product: every unit is
sold the day it reaches the shed, because the book never recovers and waiting only ever meets a
lower price (any opponent flow and the 1/day town tick both push the price down monotonically).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import scripts.optimal_release as OR


ARRIVED = [0] * 30
ARRIVED[10], ARRIVED[11], ARRIVED[16], ARRIVED[17], ARRIVED[18] = 60, 12, 6, 30, 6

#: The book is SHARED, and the race only exists because of the other seat: with no opponent flow
#: the melon book recovers 1/day from the town tick and spreading is harmless. Against a
#: melon-heavy opponent (the recorded tapes sell 114-120), whoever sells first gets the fresh
#: book and whatever is held meets the floor on d29. So the opponent here mirrors our arrivals,
#: which is what the recorded season looks like.
THEIRS = list(ARRIVED)


def test_the_release_plan_for_melon_sells_each_unit_the_day_it_arrives():
    plan = OR.release("MELON", ARRIVED, drain=1)
    assert plan == ARRIVED, (
        f"melon must be front-loaded, not trickled: plan {plan} != arrivals {ARRIVED}")


def test_the_front_loaded_plan_out_earns_the_water_fill_on_a_melon_shaped_season():
    trickle = OR.water_fill(ARRIVED, 1)
    rev_trickle, _ = OR.season("MELON", trickle, THEIRS, 1)
    rev_race, _ = OR.season("MELON", OR.release("MELON", ARRIVED, drain=1), THEIRS, 1)
    assert rev_race > rev_trickle, (
        f"front-load ${rev_race:,} must beat trickle-and-dump ${rev_trickle:,}")


def test_a_drained_product_still_water_fills():
    arrived = [10] * 30
    plan = OR.release("STRAWBERRY", arrived, drain=25)
    assert plan == OR.water_fill(arrived, 25)
