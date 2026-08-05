"""Feeding does not gate production. It prevents escape, and it banks the care bonus.

`reference/kaggriculture.py:774-802`, read carefully, says three separate things:

  - `:786`  `consecutive_unfed >= 2` -> the animal ESCAPES and the structure is left empty. So
            feeding every other day is the floor, and missing two in a row is unrecoverable.
  - `:791`  production fires on `days_since_first % interval == 0` **whether or not the animal was
            fed that day**. Feeding is not what makes milk.
  - `:794`  the accumulated `pending_care_bonus` is only consumed `if tile["fed_today"]`, and
    `:798`  it only accumulates on a day that was both cared for AND fed.

So the herd is worth servicing on its production days and worth keeping alive in between, and a flat
daily FEED + CARE on every pen buys nothing on the days that are neither. Measured against the tape,
that flat cadence was the only thing we OVER-produced: CARE 355 against 308, FEED 355 against 319,
while WATER ran short -- and pen tasks outrank crop tasks in the packer, so the redundant visits were
being paid for out of the watering that carries the yield.

Intervals, from `ANIMALS`: GOOSE 1, COW 2, SHEEP 3, with first yields on day 4, 8 and 6.
"""

import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

FIRST = {"GOOSE": 4, "COW": 8, "SHEEP": 6}
INTERVAL = {"GOOSE": 1, "COW": 2, "SHEEP": 3}


def _service(animal, days=24):
    """Which days `_tasks_for_day` feeds and cares for one pen placed on day 0."""
    from kagg.search import dayplan

    farm = dayplan.Farm()
    tile = (4, 4)
    farm.pens[tile] = dict(animal=animal, placed=0, last_feed=0)
    fed, cared = [0], []
    for day in range(1, days):
        tasks = dayplan._tasks_for_day(farm, day, [], [], fertilize=False)
        this = next((t for t in tasks if t["tile"] == tile), None)
        if this and "FEED" in this["ops"]:
            fed.append(day)
            farm.pens[tile]["last_feed"] = day
        if this and "CARE" in this["ops"]:
            cared.append(day)
    return fed, cared


@pytest.mark.parametrize("animal", ["GOOSE", "COW", "SHEEP"])
def test_an_animal_is_never_unfed_two_days_running(animal):
    """The floor, and the one that is unrecoverable if broken -- the animal is gone and the pen is
    an empty structure for the rest of the season."""
    fed, _cared = _service(animal)
    gaps = [(a, b) for a, b in zip(fed, fed[1:]) if b - a > 2]
    assert not gaps, f"{animal}: fed on {fed}; gaps of more than two days at {gaps}"


@pytest.mark.parametrize("animal", ["GOOSE", "COW", "SHEEP"])
def test_a_production_day_is_always_a_fed_day(animal):
    """`pending_care_bonus` is consumed only `if tile["fed_today"]` (`kaggriculture.py:794`), so an
    unfed production day throws away every care turn banked since the last one."""
    fed, _cared = _service(animal)
    prod = [d for d in range(FIRST[animal], 24)
            if (d - FIRST[animal]) % INTERVAL[animal] == 0]
    missed = [d for d in prod if d not in fed]
    assert not missed, (
        f"{animal}: produces on {prod}, fed on {fed}, unfed production days {missed} -- "
        f"the care bonus banked for each of those is discarded")


@pytest.mark.parametrize("animal", ["GOOSE", "COW", "SHEEP"])
def test_the_herd_is_fed_every_day_after_all(animal):
    """**This test asserted the opposite and the tape proved it wrong.**

    The reasoning looked sound: production does not require feeding, so a daily visit to every pen is
    guaranteed work that mostly buys nothing, and the packer ranks it above the watering that does.
    Cutting to "every other day, plus production days" was implemented and measured, and it took unit
    op fidelity from 74.69% to 66.42% -- FEED fell to 122 against the tape's 319 and CARE to 122
    against 308.

    The tape feeds 319 times across roughly 343 animal-days. It feeds daily. Whatever the mechanism
    argument says about production, the winner services its herd every day, and the CARE/FEED
    over-production of +47/+36 was never worth the eight points of fidelity that chasing it cost.

    Kept as a test rather than deleted, because the tempting argument is written down in
    `docs/fable_emitter_task_generation_2026-08-05.md` and will look just as sound next time.
    """
    fed, cared = _service(animal, days=24)
    assert len(fed) >= 22, (
        f"{animal}: fed on {len(fed)} of 23 days; the tape feeds ~every day (319 feeds over ~343 "
        f"animal-days) and cutting the cadence cost 8 points of tape fidelity")
    assert len(cared) <= len(fed), (
        f"{animal}: cared {len(cared)} times but fed {len(fed)} -- a CARE on an unfed day banks "
        f"nothing (`kaggriculture.py:798` requires cared_today AND fed_today)")
