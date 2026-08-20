"""What the crop/herd dials can and cannot actually move, pinned before a search is run on them.

A CEM over `CROP_TILE_SHIFTS` and `HERD_GEESE` is only as good as its bounds, and a bound picked
from a docstring is a guess. Every number in `scripts/cem_allocation.py`'s search space comes from
one of these tests.

The four theories, each with the failure it would have caused:

1. A `WHEAT -> MELON` budget drains in day order from `LATE_CROP_FROM_DAY`, so a budget larger than
   the wheat stops before MELON's last viable planting day buys tiles that cannot finish a cycle
   and are worth zero. The bound has to be the wheat count in that window, not the wheat count.
2. The shift dial cannot REDUCE melon at all: the schedule plants melon on d0/d6/d7 only, and the
   dial starts at d12. A search told to "tune melon tiles" would silently only ever add.
3. The only thing that moves the pre-d12 melon/strawberry split is the melon fork
   (`MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT`), which is why it is in the search space at all.
4. `HERD_GEESE >= 2` was recorded in `scripts/geese_pool_eval.py` as returning a herd of 13 where
   0 and 1 return 14 -- an animal lost per conversion. If that is still true the upper bound is 1.
   `swap_in_geese` has been rewritten since that note, so it is re-measured rather than assumed.
"""
import collections
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEDULE = REPO / "data" / "seed_scripts" / "kawashigi" / "schedule.json"

pytestmark = pytest.mark.skipif(not SCHEDULE.exists(), reason="schedule.json is gitignored data")

#: Last day a crop can be planted and still complete a full yield cycle before the season ends.
#: Derived in `scripts/swap_one_crop.py` from `reference.kaggriculture.CROPS`.
LATEST_PLANTING = {"WHEAT": 25, "CARROT": 26, "MELON": 17, "TOMATO": 18, "STRAWBERRY": 13}


@pytest.fixture(scope="module")
def schedule():
    return {int(k): v for k, v in json.load(open(SCHEDULE)).items()}


def apply_shift(schedule, src, dst, budget, from_day=12):
    """Drain `budget` src->dst stops in day order from `from_day`, exactly as the agent does.

    Mirrors the `CROP_TILE_SHIFTS` block in `schedule_agent.make_agent`: one `_recrew` per day, a
    season-wide budget that drains as it is spent, days visited in ascending order.
    """
    from kagg.search.schedule_agent import _recrew

    left, landed = budget, collections.Counter()
    for day in sorted(schedule):
        if day < from_day or not schedule[day] or left <= 0:
            continue
        _row, spent = _recrew(schedule[day], src, dst, left)
        left -= spent
        if spent:
            landed[day] = spent
    return landed


def test_a_wheat_to_melon_budget_of_24_lands_only_on_days_melon_can_still_finish(schedule):
    landed = apply_shift(schedule, "WHEAT", "MELON", 24)
    assert sum(landed.values()) == 24, landed
    late = {d: n for d, n in landed.items() if d > LATEST_PLANTING["MELON"]}
    assert not late, f"melon planted too late to yield: {late}"


def test_a_wheat_to_melon_budget_of_34_spills_past_melons_last_viable_day(schedule):
    """The bound above is load-bearing, not decorative: one notch up and the tiles are dead."""
    landed = apply_shift(schedule, "WHEAT", "MELON", 34)
    late = {d: n for d, n in landed.items() if d > LATEST_PLANTING["MELON"]}
    assert late, f"expected spill past d{LATEST_PLANTING['MELON']}, got {landed}"


def test_a_wheat_to_tomato_budget_of_14_lands_only_on_days_tomato_can_still_finish(schedule):
    landed = apply_shift(schedule, "WHEAT", "TOMATO", 14)
    assert sum(landed.values()) == 14, landed
    assert not {d: n for d, n in landed.items() if d > LATEST_PLANTING["TOMATO"]}, landed


def test_the_shift_dial_cannot_reduce_melon_at_all(schedule):
    """Melon is planted d0/d6/d7 and the dial starts at d12, so `MELON->WHEAT` is a no-op.

    This is why the melon fork is in the search space: it is the only reachable melon dial.
    """
    landed = apply_shift(schedule, "MELON", "WHEAT", 20)
    assert sum(landed.values()) == 0, landed


def test_only_seven_strawberry_stops_are_reachable_by_the_shift_dial(schedule):
    landed = apply_shift(schedule, "STRAWBERRY", "WHEAT", 40)
    assert sum(landed.values()) == 7, landed


def test_the_far_corner_of_the_search_box_is_still_a_plantable_schedule(schedule):
    """The bounds are safe JOINTLY, not just one at a time, because the budgets drain in order.

    `CROP_TILE_SHIFTS` is applied in list order, so MELON takes the earliest wheat stops, TOMATO the
    next and CARROT whatever is left. At the box corner (24, 14, 24) every tile must still land on a
    day its crop can finish. If this fails the search space contains dead tiles and every number
    taken inside it is diluted by them.
    """
    from kagg.search.schedule_agent import _recrew

    order = (("WHEAT", "MELON", 24), ("WHEAT", "TOMATO", 14), ("WHEAT", "CARROT", 24),
             ("STRAWBERRY", "WHEAT", 7))
    left = [n for _, _, n in order]
    landed = collections.defaultdict(collections.Counter)
    rows = {d: dict(r) for d, r in schedule.items() if r}
    for day in sorted(rows):
        if day < 12:
            continue
        for i, (src, dst, _) in enumerate(order):
            rows[day], spent = _recrew(rows[day], src, dst, left[i])
            left[i] -= spent
            if spent:
                landed[dst][day] += spent

    assert left == [0, 0, 0, 0], f"budget did not drain: {left}"
    for dst, days in landed.items():
        late = {d: n for d, n in days.items() if d > LATEST_PLANTING[dst]}
        assert not late, f"{dst} planted too late to yield: {late}"


def test_turning_the_melon_fork_off_keeps_twenty_melon_and_thirty_four_strawberry(schedule):
    """The fork converts the d6/d7 melon rows once the opponent shows 7+ melon tiles."""
    from kagg.search.schedule_agent import MELON_YIELD_FROM_DAY, _melon_to_strawberry

    def counts(rows):
        c = collections.Counter()
        for r in rows.values():
            c.update((r or {}).get("plants") or [])
        return c

    off = counts(schedule)
    on = counts({d: (_melon_to_strawberry(r or {}) if d >= MELON_YIELD_FROM_DAY else r)
                 for d, r in schedule.items()})
    assert (off["MELON"], off["STRAWBERRY"]) == (20, 34), off
    assert (on["MELON"], on["STRAWBERRY"]) == (12, 42), on


def _herd(rows):
    c = collections.Counter()
    for r in rows.values():
        c.update({k: int(v) for k, v in ((r or {}).get("animals_bought") or {}).items()})
    return c


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4])
def test_swap_in_geese_never_loses_an_animal(schedule, n):
    """`geese_pool_eval.py` recorded a herd of 13 at `HERD_GEESE >= 2` against 14 at 0 and 1.

    If that were still true the CEM's upper bound on this dial would be 1, because 2 and 3 would be
    measuring a lost animal rather than a goose. Measured 2026-08-15: it is NOT still true. The herd
    is 14 at every setting, so the whole range is comparable.
    """
    from kagg.search.schedule_agent import swap_in_geese

    base = _herd(schedule)
    got = _herd(swap_in_geese(schedule, n))
    assert sum(base.values()) == 14, dict(base)
    assert sum(got.values()) == sum(base.values()), (n, dict(base), dict(got))


def test_the_geese_dial_saturates_at_three(schedule):
    """`HERD_GEESE_EARLIEST` gates the 4th goose behind d21, and nothing is bought that late.

    So 4 is byte-identical to 3 and the search's upper bound is 3, not the herd size.
    """
    from kagg.search.schedule_agent import swap_in_geese

    got = [_herd(swap_in_geese(schedule, n))["GOOSE"] for n in range(6)]
    assert got == [0, 1, 2, 3, 3, 3], got
