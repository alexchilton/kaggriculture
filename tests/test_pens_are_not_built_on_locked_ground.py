"""Three of the four shed-access tiles are in quadrants that start LOCKED.

`R.shed_access_tiles()` is `[(4,4), (5,4), (4,5), (5,5)]` -- the ring around the shed, and the only
cells where PICKUP, DROP and a shed PLACE work. But the board's quadrant split puts

    (4,4) NW  needs 0 parcels     <- the only one legal on day 0
    (5,4) NE  needs 1 parcel
    (4,5) SW  needs 2 parcels
    (5,5) SE  needs 3 parcels

and the day planner reached for them in order without checking, because they are the ideal ground for
a herd that draws wheat daily.

Measured consequence, day 0: three of the four pens were built on locked ground, so BUILD_PASTURE,
PLACE, FEED and CARE all silently no-oped -- while the animals had already been paid for. The farm
held 2 pens on day 1 against the tape's 4, and never caught up: 5 pens by day 29 against 14.

It is the same defect class as every other one in this project. `ops.py:86` ignores a move onto
LOCKED, `_apply_unit_action` bails before PLANT, and nothing anywhere raises.
"""

import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


def test_only_one_shed_tile_is_usable_on_day_zero():
    """Pinned so the fix below is not calibrated to folklore."""
    needs = {t: R.land_purchases_for(t) for t in R.shed_access_tiles()}
    assert needs[(4, 4)] == 0
    assert sorted(needs.values()) == [0, 1, 2, 3], needs


@pytest.fixture(scope="module")
def targets():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    import collections

    from kagg.search import dayplan

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    out = collections.defaultdict(list)
    orig = dayplan._tasks_for_day

    def spy(farm, day, plant_orders, build_orders, fertilize, replant=None):
        for tile, crop in plant_orders:
            out[day].append((tuple(tile), "plant", crop))
        for tile, animal in build_orders:
            out[day].append((tuple(tile), "build", animal))
        return orig(farm, day, plant_orders, build_orders, fertilize, replant)

    dayplan._tasks_for_day = spy
    try:
        dayplan.emit(sched)
    finally:
        dayplan._tasks_for_day = orig
    return dict(out), sched


def test_nothing_is_ever_placed_on_ground_the_farm_does_not_own(targets):
    """The contract, across the whole season and both kinds of placement."""
    out, sched = targets
    land_days = sorted(d for d, r in sched.items() if r["land"])

    def parcels_on(day):
        return sum(1 for L in land_days if L <= day)

    wrong = []
    for day in sorted(out):
        owned = parcels_on(day)
        for tile, kind, what in out[day]:
            need = R.land_purchases_for(tile)
            if need > owned:
                wrong.append(
                    f"day {day}: {kind} {what} at {tile} needs {need} parcels, farm owns {owned}")
    assert not wrong, (
        f"{len(wrong)} placements on locked ground -- every op aimed at them no-ops silently:\n  "
        + "\n  ".join(wrong[:10]))
