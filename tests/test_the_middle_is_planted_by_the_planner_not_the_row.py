"""The mid-season row must not decide how much wheat goes in the ground.

Measured 2026-08-21 (`docs/the_middle_is_not_board_capacity_2026-08-21.md`): Kawashigi's d14-d27
wheat count is not board capacity -- he ends 85.7% of those days with empty, affordable, unlocked
ground. What binds is his TURN budget: 1.8% idle, 53.6% of the budget walking, 31.9% of the work
watering. The count is a property of his routing.

So the design for the middle is: pin the CROP to wheat, and let our own router's turn budget set the
COUNT. These tests pin the three ways a row can quietly take that decision back off the planner.

Theory 1  a row that lists N wheat caps the day at N plants, because `_router_acts` sites one PLANT
          pin per entry in `row["plants"]` on ground the board says is empty. A row shorter than the
          board is the row deciding, not the planner.
Theory 2  a `seeds` order on those days floors the BUY_SEED emission above what the pins justify
          (`schedule_agent.py:5200`, `_row_q` is a floor). Under `router=True` `want_seed` is the
          remaining PLANT pins, which is exactly right, and a row order can only overshoot it.
Theory 3  any crop other than WHEAT in the middle is a crop the measurement says he does not plant
          there -- except the 1-2 CARROT on d21-d26, which is a separate open question and is NOT
          claimed here.

Theory 4 and 5 pin the library ends: d0-d13 and d28-d29 play a REAL row that exists in the library
for that day, chosen as the modal row under the executor's own label. A synthesised row would be a
plan nobody ever played.
"""

import collections
import json
import pathlib

import pytest

from kagg.search import kawa_rows

LIBRARY_DAYS = kawa_rows.library_days()
PLANNER_DAYS = kawa_rows.mid_season()

#: Alex, 2026-08-21: "till d12 it should just be tape matching". Strict for every boundary the A/B
#: is allowed to reach, so this range is asserted independently of `MID_SEASON_FROM`.
STRICT_DAYS = tuple(range(0, 13))


@pytest.fixture(scope="module")
def schedule():
    if not kawa_rows.LIBRARY.exists():
        pytest.skip("row library %s is not on disk (data/ is gitignored)" % kawa_rows.LIBRARY)
    return kawa_rows.build()


@pytest.fixture(scope="module")
def library():
    if not kawa_rows.LIBRARY.exists():
        pytest.skip("row library %s is not on disk (data/ is gitignored)" % kawa_rows.LIBRARY)
    return json.loads(kawa_rows.LIBRARY.read_text())


def test_the_schedule_covers_every_day_of_the_season(schedule):
    assert sorted(schedule) == list(range(30))


@pytest.mark.parametrize("day", PLANNER_DAYS)
def test_a_mid_season_row_cannot_cap_the_plant_count(schedule, day):
    """Theory 1. The row must offer at least a whole board, so the pins and the tour bind first."""
    plants = schedule[day].get("plants") or []
    assert len(plants) >= kawa_rows.BOARD_TILES, (
        "day %d offers only %d plantings; the board has %d tiles, so this row -- not the router's "
        "turn budget -- is what sets the count" % (day, len(plants), kawa_rows.BOARD_TILES))


@pytest.mark.parametrize("day", PLANNER_DAYS)
def test_a_mid_season_row_orders_no_seed_of_its_own(schedule, day):
    """Theory 2. Seed follows the PLANT pins; a row order can only floor it too high."""
    assert not (schedule[day].get("seeds") or {}), (
        "day %d carries a seeds order %r, which floors BUY_SEED above the pins"
        % (day, schedule[day].get("seeds")))


@pytest.mark.parametrize("day", PLANNER_DAYS)
def test_the_middle_plants_wheat_and_only_wheat(schedule, day):
    """Theory 3."""
    assert set(schedule[day].get("plants") or []) == {"WHEAT"}, (
        "day %d plants %r" % (day, sorted(set(schedule[day].get("plants") or []))))


@pytest.mark.parametrize("day", LIBRARY_DAYS)
def test_a_library_day_plays_a_row_somebody_actually_played(schedule, library, day):
    """Theory 4. The row must be identical to a recorded row for that day, field for field."""
    real = [kawa_rows.only_animals_get_placed(r["target"]) for r in library if r["day"] == day]
    assert real, "no library rows for day %d" % day
    assert schedule[day] in real, "day %d plays a row that is in no recorded season" % day


@pytest.mark.parametrize("day", LIBRARY_DAYS)
def test_a_library_day_plays_the_MODAL_row(schedule, library, day):
    """Theory 5. Modal under the executor's label -- the simplest thing that can work.

    Not the modal *row*: two seasons that differ only in a field the executor never reads are the
    same plan, and splitting them would pick a minority row as the mode.

    Ties are broken on the label that sorts first, matching `kawa_rows.modal_row`.
    `Counter.most_common` breaks them on insertion order, which is a property of the file rather
    than of the data, and it disagreed here at d28 -- where the largest class is 2 of 228.
    """
    real = [r["target"] for r in library if r["day"] == day]
    counts = collections.Counter(kawa_rows.label(r, day) for r in real)
    top = max(sorted(counts), key=lambda k: counts[k])
    mine = kawa_rows.label(schedule[day], day)
    assert mine == top, (
        "day %d plays label %s (%d of %d seasons); the mode is %s (%d of %d)"
        % (day, mine, counts[mine], len(real), top, counts[top], len(real)))


@pytest.mark.parametrize("day", STRICT_DAYS)
def test_the_greedy_wheat_fill_never_reaches_the_strict_days(schedule, library, day):
    """Alex, 2026-08-21: "till d12 it should just be tape matching".

    Not as a fallback, not as a top-up, not to use spare turns. The wheat fill is identifiable by
    its length -- it asks for a whole board -- so this catches it whatever the boundary is set to.
    """
    row = schedule[day]
    assert len(row.get("plants") or []) < kawa_rows.BOARD_TILES, (
        "day %d has been wheat-filled; d0-d12 must be strict rows" % day)
    real = [kawa_rows.only_animals_get_placed(r["target"]) for r in library if r["day"] == day]
    assert row in real, "day %d is not a row anybody played" % day


def test_the_boundary_only_ever_moves_the_middle(library):
    """The two boundaries under test differ on d13 and nowhere else.

    A measurement of "d13 in the middle vs d13 in the library" is only about d13 if the rest of the
    season is byte-identical between the two schedules. This is the guard on that.
    """
    early = kawa_rows.build(mid_from=13)
    late = kawa_rows.build(mid_from=14)
    differ = sorted(d for d in early if early[d] != late[d])
    assert differ == [13], "the two boundaries differ on days %r, not just d13" % differ


@pytest.mark.parametrize("day", range(30))
def test_a_places_row_names_only_animals(schedule, day):
    """`PLACE` is two different ops and the extractor recorded them as one.

    `_apply_unit_action`'s PLACE branch places an animal onto a matching empty structure, and falls
    back to dropping the named item into the shed when the tile is not one. Kawashigi uses the
    second form constantly, so `scripts/extract_target_rows.py` -- which appends `u[1]` verbatim --
    produced `places` lists that are mostly PRODUCTS:

        STRAWBERRY 2794   WOOL 2218   COW 1936   MELON 1653   SHEEP 1496
        FERTILIZER 1204   MILK 1039

    `schedule_agent._outstanding_places` reads every entry as `R.ANIMALS[a]["first_yield_day"]`, so
    a product in that list is a `KeyError` on the first turn of the day -- which is exactly how this
    was found, `KeyError: 'FERTILIZER'` at `schedule_agent.py:3862` on d1.

    A shed drop is work the router re-derives from the live board. It is not part of the plan.
    """
    from kagg.search.schedule_agent import R
    places = schedule[day].get("places") or []
    strays = sorted({p for p in places if p not in R.ANIMALS})
    assert not strays, "day %d places %r, which are not animals" % (day, strays)


def test_the_library_row_keeps_its_herd_because_the_executor_substitutes_it(schedule):
    """The species is not ours to choose in the row; `_herd_split` reads the live shop draw.

    `schedule_agent._herd_through_day` walks `animals_bought` in day order and re-labels COW/SHEEP
    against the split `_herd_split` computes from `unlocked_shops`. So the row must still carry a
    real species -- blanking it to a token would leave that walk with nothing to re-label.
    """
    bought = collections.Counter()
    for day in sorted(schedule):
        for animal, qty in (schedule[day].get("animals_bought") or {}).items():
            bought[animal] += int(qty or 0)
    assert bought, "no animals bought anywhere in the season"
    assert set(bought) <= {"COW", "SHEEP", "GOOSE"}, "unknown species in the herd rows: %r" % bought
