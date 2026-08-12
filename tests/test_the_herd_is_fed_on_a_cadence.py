"""Feed an animal on the nights it pays, and on the night before it starves. Never every night.

`will_be_fed` claimed a cadence and had none:

    if not FEED_ONLY_WHEN_IT_BUYS_SOMETHING or day < FEED_CADENCE_FROM_DAY:
        return True
    if cell["consecutive_unfed"] >= 1:
        return True
    return ((day + 1) - placed_day - first_yield_day) >= 0

`FEED_CADENCE_FROM_DAY` was 7, so d5 and d6 short-circuited to "feed everything"; and from d7 the
last line reads "feed every night once the animal has started producing", which for a producing herd
is also every night. Ours against the tape: 4 5 5 6 7 **7 7 6 6** against 4 5 5 6 7 **3 7 3 7**.

Two rules from `reference/kaggriculture.py`, and nothing else:

    :804      `consecutive_unfed >= 2` and the animal escapes -- the structure stays, the animal is
              gone, and nothing on the board buys it back. So one night in two is always survivable
              and is never optional on the second night.
    :810-816  `base = 1` lands whether or not the pen was fed. Only `pending_care_bonus` reads
              `fed_today`, and it is released on a production night -- `days_since_first % interval`.

So a feed buys something on a production night and buys nothing on any other, except the one thing
it always buys, which is survival. That is two clauses, and it is the whole rule.

The cost of the missing cadence is turns, and d7 is where it bites: 12 jobs short of the tape with
3 turns of slack, while spending 12 unit-turns on FEED and CARE against Seb's 6.
"""
import importlib

import pytest

RT = importlib.import_module("kagg.search.router")
REF = importlib.import_module("reference.kaggriculture") if False else None
ANIMALS = RT.ANIMALS


def _pen(kind, placed_day=0, unfed=0):
    return {"animal": kind, "placed_day": placed_day, "consecutive_unfed": unfed,
            "fed_today": False, "cared_today": False}


def test_a_hungry_pen_is_always_fed():
    """`consecutive_unfed == 1` is the last night before the animal walks off (`:804`)."""
    for kind in ANIMALS:
        assert RT.will_be_fed(_pen(kind, unfed=1), day=5), (
            f"{kind} carrying a miss was not scheduled to eat; one more and it is gone")


def test_a_pen_that_ate_last_night_is_not_fed_again_tonight_for_nothing():
    """A COW has `interval` 2, so the night after a production night buys nothing (`:810-816`)."""
    cow = ANIMALS["COW"]
    off = cow["first_yield_day"] + 1          # one past a production night, not hungry
    assert not RT.will_be_fed(_pen("COW", placed_day=0), day=off), (
        f"COW fed on day {off}: not hungry, not a production night, so the feed buys nothing")


def test_a_pen_is_fed_on_its_production_night():
    """That is the night `pending_care_bonus` is released, and only if `fed_today`."""
    for kind, a in ANIMALS.items():
        day = a["first_yield_day"]
        assert RT.will_be_fed(_pen(kind, placed_day=0), day=day), (
            f"{kind} not fed on its first production night (day {day}), so the care bonus is lost")


def test_an_animal_years_from_yielding_is_not_fed_nightly():
    """A COW placed on d0 first yields on d8. The seven nights before buy nothing but survival, and
    the hunger clause already buys that at half the wheat and half the turns."""
    fed = [d for d in range(ANIMALS["COW"]["first_yield_day"])
           if RT.will_be_fed(_pen("COW", placed_day=0), day=d)]
    assert not fed, (
        f"a COW eight days from its first yield is scheduled to eat on days {fed}")


@pytest.mark.parametrize("kind", sorted(ANIMALS))
def test_no_animal_can_starve_under_the_cadence(kind):
    """Walk the rule forward and check `consecutive_unfed` never reaches 2 (`:804`).

    This is the test that makes the cadence safe rather than merely cheap: a SHEEP has `interval` 3,
    so production nights alone would leave it two nights unfed and it would escape. The hunger
    clause has to catch it, and here it is checked rather than assumed.
    """
    cell = _pen(kind, placed_day=0)
    for day in range(30):
        if RT.will_be_fed(cell, day):
            cell["consecutive_unfed"] = 0
        else:
            cell["consecutive_unfed"] += 1
        assert cell["consecutive_unfed"] < 2, (
            f"{kind} reaches consecutive_unfed {cell['consecutive_unfed']} on day {day} "
            f"and escapes")
