"""His schedule, off his tape, as the contract. This is the test file that matters.

Every earlier test in this project asserted a property of our own code, so the suite stayed green while
the farm banked $40k against his $141k. And every judgement I made about "matching the winner" compared
one inference off his replay against another inference off the same replay -- which is how a claim that
land, amounts, schedule, buy-time and hires all matched survived for a day while our search was emitting
3 cows and 6 tiles.

`scripts/extract_leader_schedule.py` ends that by reading the schedule off the tape. There is no
inference left in these numbers -- they are counted ops:

    day  dawn $  hands  land  pens built  tiles planted  wheat bought  units sold
      0   3,000      4     0           4             17            49          20
      1      42      4     0           0              1            13          11
      2     141      5     0           0              1            18          14
      3     217      5     0           0              0            10          50
      4     786      6     0           0             10             7          14
      5     621      6     0           2              0            13          39
      6     654      6     0           1              0            24          24
      7   1,719      8     1           0              9            23          44
      8     928     10     0           4              9            20          41
      9   1,409     11     0           1              7            37          45
     10   1,278     12     1           2              5            39          72
     11   3,236     12     0           2             10            33          59
     12   6,828     12     0           0              8            54         358   <- the inflection
     13  14,622     12     0           0             10            75          35
                                       --             ---           ---
                                       14             131           967

Read the crew column. **He runs 4 hands on day 0 and does not reach 12 until day 10.** The hire ladder
is Fibonacci and resets every dawn, so 4 hands is $7/day and 12 is $376/day -- he pays the small number
for the ten days he has no income and the big number only once the herd and the first parcel are
earning. Our plans hire their peak crew from day 0.

Read the plant column too: **17 tiles on day 0**, before any land is bought, and 131 tile-plantings
across the season with a second wave of 31 on day 26. He is not a farm that is built once.

These tests are meant to be red. They are the difference between our schedule and his, stated so that
closing it is measurable.
"""


import pytest

#: **Disabled 2026-08-07: this whole file asserts against the OLD LEADER's tape (`new_leader`).**
#:
#: Kept, not deleted, because it is the record of a specific and expensive mistake. The agent is now
#: matched against Seb's tape (`top_guys/90494364`), and the two tapes play differently -- the case
#: that forced this was watering. `router.py` had been made to water every tile every day on the
#: strength of a table showing "the tape" watering ~1.06 per live tile daily, 18 times on day 1
#: against our 1. That table was measured here, on the old leader, and then applied to Seb:
#:
#:     oldleader  d0 16/17  d1 17/18  d2 18/19  d3 18/19   waters daily
#:     seb        d0 17/17  d1 17/0   d2 17/17  d3 17/14   waters alternate days
#:
#: Seb takes zero weeds through day 7 on the alternate-day cadence, and the every-day rule was
#: costing 17 work turns and ~31 walk turns on day 1 alone for nothing.
#:
#: So these assertions are not wrong about the old leader; they are answers to a question we stopped
#: asking. Left red, they read as regressions and pull work towards the wrong target. Re-enable only
#: by first deciding which tape the number is supposed to describe.
_OLD_LEADER_SKIP = pytest.mark.skip(
    reason="asserts against the OLD LEADER's tape; the agent now targets Seb's -- see banner")

pytestmark = _OLD_LEADER_SKIP
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]


def crew_cost(hands):
    """A crew of `hands` costs this every dawn -- the whole partial sum, not the last rung."""
    return sum(FIB[:hands])


@pytest.fixture(scope="module")
def his():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    return {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}


@pytest.fixture(scope="module")
def ours():
    """Our emitter driven at HIS schedule, so a failure is about the emitter and nothing else."""
    from emit_leader_schedule import build          # noqa: F401  (built lazily by the script)
    return build()


# ------------------------------------------------------------------ his schedule, pinned
def test_his_crew_ramps_from_four_to_twelve(his):
    """The fact our plans get wrong, and it is worth $3,690 over the first ten days on its own."""
    assert his[0]["hands"] == 4, "day 0 crew"
    assert his[10]["hands"] == 12, "day 10 crew"
    early = sum(crew_cost(his[d]["hands"]) for d in range(0, 10))
    flat12 = crew_cost(12) * 10
    assert early < flat12 / 3, (
        f"his first ten days of crew cost ${early:,} against ${flat12:,} for a flat crew of 12")


def test_he_plants_on_day_zero(his):
    """17 tiles and 18 seeds on day 0, before any parcel is bought -- all of it in NW."""
    assert len(his[0]["plants"]) >= 15
    assert sum(his[0]["seeds"].values()) >= 15


def test_his_herd_is_ramped_not_bought_at_once(his):
    """4 pens on day 0 then +2, +1, +4, +1, +2 -- complete by day 11, never bought in one lot.

    Buying 14 at once is insolvent and that was measured: ordered 14, only 8 ever appeared.
    """
    builds = {d: his[d]["builds"] for d in sorted(his) if his[d]["builds"]}
    assert builds[0] == 4
    assert sum(builds.values()) == 14
    assert max(builds) <= 11, f"his last pen is built on day {max(builds)}"


def test_the_inflection_is_a_wheat_dump_not_a_harvest(his):
    """Day 12 sells 358 units and the bank goes $6,828 -> $14,622. 204 of those units are wheat he
    BOUGHT, not grew: 967 units bought across the season against 1,131 sold, of which 319 go to FEED."""
    assert sum(his[12]["sells"].values()) > 300
    assert his[12]["money_dawn"] < his[13]["money_dawn"] / 2
    assert sum(his[d]["buys"].get("WHEAT", 0) for d in his) > 900


# ------------------------------------------------------------------ ours, against his
def test_our_crew_ramps_like_his(his, ours):
    """The single most expensive difference. We imply the crew from the highest unit index in use, so a
    plan whose chains all start on day 0 pays the peak crew for the whole season."""
    for day in (0, 3, 6):
        assert ours["crew"][day] <= his[day]["hands"] + 1, (
            f"day {day}: our crew is {ours['crew'][day]} against his {his[day]['hands']} "
            f"(${crew_cost(ours['crew'][day]):,}/day against ${crew_cost(his[day]['hands']):,})")


def test_we_place_his_fourteen_pens(ours):
    assert ours["pens"] >= 14, f"only {ours['pens']} pens placed of his 14"


def test_we_plant_his_tiles(ours):
    """Not 131 -- that counts replants. But the board he works is ~61 distinct tiles and ours must be
    in that region, not the 6-24 tiles every plan so far has managed."""
    assert ours["tiles"] >= 50, f"only {ours['tiles']} crop tiles placed against his ~61"


def test_our_bank_tracks_his_through_the_ramp(his, ours):
    """The one that decides the season. Every purchase in the reference no-ops silently on an empty
    bank, so a plan that is broke on day 4 has quietly stopped being the plan we wrote."""
    for day in (7, 10, 13):
        assert ours["bank"].get(day, 0) >= his[day]["money_dawn"] * 0.5, (
            f"day {day}: ${ours['bank'].get(day, 0):,.0f} against his ${his[day]['money_dawn']:,.0f}")


def test_his_schedule_through_our_emitter_banks_his_order_of_magnitude(ours):
    """The fork this whole file exists to resolve.

    Driven at his own schedule, if our emitter banks near his $141,256 then the emitter and simulator
    are sound and everything left to fix is the search and the scheduler. If it banks $30k, the
    representation cannot express his farm and no amount of searching will close the gap.
    """
    assert ours["final"] > 100_000, (
        f"his schedule through our emitter banks ${ours['final']:,.0f} against his $141,256")
