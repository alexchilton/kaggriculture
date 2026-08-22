"""The day we buy a quadrant, the dawn plan must already be working it.

The day is planned ONCE, at hour 0 (`_router_acts`: "The plan is built ONCE, at dawn, and then only
walked"). The env applies unit actions BEFORE the market phase (`kaggriculture.py:922` then `:928`),
so a `BUY_LAND` emitted at hour 0 settles at the END of hour 0 and the parcel is not in
`farm["unlocked_quadrants"]` when the plan that governs the whole day is built. Twenty-five tiles
arrive and no job is ever generated on any of them.

This is the same argument the file already makes for hires, and `_router_acts`'s own docstring states
it: "a hand bought at hour 0 first acts at hour 1, and a planner that waits to see it plans hour 0
for the pre-hire crew and then throws that plan away." `arriving` fixes it for hires. Nothing fixes
it for land.

**Measured on the Victor grid (`scripts/breakdown.py --tape victor`), seed 11, day 10** -- the day
his schedule buys the second parcel at hour 0 and plants 23 tiles, 18 of them in the new quadrant:

    plant       ours  1   tape 23
    water       ours 18   tape 43
    idle turns  ours 128  tape 78      <- on an identical crew, 341 unit-turns against his 339

Fourteen hands hired and 128 unit-turns spent standing still, on the one day the board grows by half.

**Which quadrant arrives is not a guess.** `LAND_ORDER = ["NE", "SW", "SE"]` and
`_do_buy_land` takes `LAND_ORDER[len(unlocked) - 1]` (`kaggriculture.py:699-708`) -- fully
deterministic, so the dawn plan can name the parcel before the market opens.

**Scope of the assertion.** Only days where the quadrant set ACTUALLY grew are checked. A `BUY_LAND`
that never settles -- `_do_buy_land` returns silently on a short bank, and `_process_market`
truncates the turn's queue at `maxMarketOrdersPerTurn` -- must NOT be planned around, or the routes
are orphaned onto locked ground for the rest of the season. That failure is the subject of
`scripts/did_the_land_arrive.py` and it is the reason this test reads the outcome rather than the
schedule's `land` column.

**Two mechanisms, not one, and only the first is fixed.** Measured dawn banks against the parcel
price on this schedule:

    d 6   dawn $  432   parcel $1,000   funded by the DAY'S OWN SALES
    d10   dawn $4,058   parcel $2,000   certain before the market opens

`_land_this_turn` predicted only the second, and the first was carried here as an xfail. **Both are
now asserted (`SELLS_FUND_THE_DAWN_PARCEL`, 2026-08-11.)** The plan and the buyer must apply the
same test: the market block has always bought on `money + pending`, because the day's sales settle
in earlier order slots, so reading `money` alone here made the plan strictly more pessimistic than
the code doing the buying. On d6 we take the parcel at h13 -- three hours EARLIER than the tape --
and still left 42 unit-turns idle, because the only plan the day gets was built as though the ground
were never coming.

The revenue is the schedule's own `sells` row at the day's opening prices, deliberately not a guess
at what the shed might yield: the row is the plan's statement of what the day sells, and if it does
not hold the day was already wrong.

The orphaned-route failure the old note feared did NOT materialise here, and that was measured
rather than argued: d6 records **zero refused moves** across the whole day (a MOVE into a locked
quadrant is refused at `kaggriculture.py:313` and would show as a unit that ordered a move and did
not change square). d6 pens 6/8 -> 8/8, build 0/2 -> 2/2, place 0/1 -> 1/1, feed and care 6/7 -> 7/7.

What it DOES cost is watering, and that is a job-priority defect rather than a routing one: d6 water
11/12 -> 7/12 and three tiles weed, melon 5/5 -> 3/5. The crew now has 50 tiles of work and the same
turns, and it spends them on the new ground.
"""
import collections
import kagg.plan as _PLAN
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top2/91854176.json"
SCHEDULE = _PLAN.SHIPPED_PLAN
TEAM = "Victor @ Tufa Labs"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent"
SEED = 11
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def played():
    """Play d0-d11 of the Victor schedule, capturing each day's DAWN plan and the land it got.

    Returns `(dawn_jobs, gained)`:

      - `dawn_jobs[day]`  the tiles offered to the day's first `crew.cover` call. The dawn call is
        the one that matters -- the day is planned once, so a tile absent there is a tile absent all
        day.
      - `gained[day]`     quadrants the farm owns at dusk that it did not own at dawn.

    `STRICT_FEASIBILITY` is forced off: the raise is a dev instrument and a day that aborts mid-plan
    yields nothing to inspect.
    """
    SA = importlib.import_module(MODULE)
    CREW = importlib.import_module("kagg.search.crew")

    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    opp = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
            "hands": list((s.get("action") or {}).get("hands") or []),
            "market": list((s.get("action") or {}).get("market") or [])}
           for s in (step[1 - seat] or {} for step in d["steps"][1:])]

    dawn_jobs, dawn_seen = {}, set()
    at_dawn, at_dusk, dawn_bank = {}, {}, {}
    now = {"day": 0}
    real_cover, real_strict = CREW.cover, CREW.STRICT_FEASIBILITY

    def spy(units, jobs, budget, *a, **kw):
        if now["day"] not in dawn_seen:
            dawn_seen.add(now["day"])
            dawn_jobs[now["day"]] = [tuple(j.tile) for j in jobs]
        return real_cover(units, jobs, budget, *a, **kw)

    CREW.cover, CREW.STRICT_FEASIBILITY = spy, False
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(TPD * DAYS):
            day, now["day"] = t // TPD, t // TPD
            o0 = env.state[0].observation
            quads = set(o0["farms"][0].get("unlocked_quadrants") or ["NW"])
            if t % TPD == 0:
                at_dawn[day] = set(quads)
                dawn_bank[day] = float(o0["farms"][0]["money"])
            at_dusk[day] = set(quads)
            a0, a1 = agent(o0), opp[t]
            env.step([a0, a1])
    finally:
        CREW.cover, CREW.STRICT_FEASIBILITY = real_cover, real_strict

    gained = {day: at_dusk[day] - at_dawn[day] for day in at_dawn}
    # Affordable at dawn == the parcel is CERTAIN before the market opens. `LAND_PRICES` is indexed
    # by how many extra quadrants are already owned, exactly as `_do_buy_land` indexes it.
    from kagg.search import routines as R
    certain = {day: (len(at_dawn[day]) - 1 < len(R.LAND_PRICES)
                     and dawn_bank[day] >= R.LAND_PRICES[len(at_dawn[day]) - 1])
               for day in at_dawn}
    return dawn_jobs, gained, certain, dawn_bank


def test_a_parcel_is_bought_within_the_days_played(played):
    """Guard the fixture. If nothing is ever bought the assertions below pass vacuously."""
    _dawn_jobs, gained, _certain, _bank = played
    days = [d for d, g in gained.items() if g]
    assert days, ("no quadrant was bought in d0-d11, so the tests below prove nothing -- "
                  f"gained={gained}")


def test_both_kinds_of_land_day_occur_in_the_days_played(played):
    """Guard the split. If every land day were `certain`, the xfail below would prove nothing."""
    _dawn_jobs, gained, certain, bank = played
    land_days = sorted(d for d, g in gained.items() if g)
    kinds = {certain[d] for d in land_days}
    assert kinds == {True, False}, (
        "this file asserts one thing about parcels affordable at dawn and another about parcels "
        f"funded by the day's sales; the run produced only {kinds}. land days={land_days} "
        f"banks={ {d: bank[d] for d in land_days} }")


def _offered_on_new_ground(dawn_jobs, gained, day):
    from kagg.search import routines as R
    new = gained[day]
    return [t for t in dawn_jobs.get(day, []) if R.quadrant_of(t[0], t[1]) in new]


@pytest.mark.parametrize("day", range(DAYS))
def test_the_dawn_plan_offers_work_on_a_parcel_it_can_already_afford(played, day):
    """A quadrant whose purchase is CERTAIN at dawn must appear in that dawn's plan.

    Not "some work happened there eventually" -- the day is planned once, so the dawn call is the
    only chance the ground gets.
    """
    from kagg.search import routines as R

    dawn_jobs, gained, certain, bank = played
    if not gained.get(day):
        pytest.skip(f"d{day} bought no land")
    if not certain[day]:
        pytest.skip(f"d{day} funded its parcel from the day's sales (dawn bank ${bank[day]:,.0f})")
    offered = _offered_on_new_ground(dawn_jobs, gained, day)
    planned = dawn_jobs.get(day, [])
    assert offered, (
        f"d{day} bought {sorted(gained[day])} on a dawn bank of ${bank[day]:,.0f} and the dawn plan "
        f"offered no job on it. {len(planned)} jobs were planned, all on "
        f"{sorted(set(R.quadrant_of(*t) for t in planned))}. The parcel settles at the END of "
        "hour 0, after the plan that governs the whole day is built.")


@pytest.mark.parametrize("day", range(DAYS))
def test_the_dawn_plan_offers_work_on_a_parcel_funded_by_the_days_sales(played, day):
    """The other half: a parcel the standing bank cannot cover but the day's `sells` row can.

    Was an xfail until `SELLS_FUND_THE_DAWN_PARCEL`. Kept as its own case rather than folded into
    the test above, because the two halves fail for different reasons and only one of them is a
    forecast.
    """
    from kagg.search import routines as R

    dawn_jobs, gained, certain, bank = played
    if not gained.get(day) or certain[day]:
        pytest.skip(f"d{day} is not a sales-funded land day")
    planned = dawn_jobs.get(day, [])
    assert _offered_on_new_ground(dawn_jobs, gained, day), (
        f"d{day} bought {sorted(gained[day])} on a dawn bank of ${bank[day]:,.0f} and the dawn plan "
        f"offered no job on it. {len(planned)} jobs were planned, all on "
        f"{sorted(set(R.quadrant_of(*t) for t in planned))}.")
