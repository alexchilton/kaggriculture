"""Every unit stands where the emitter believes it stands, on every turn of the season.

The emitter routes by dead reckoning: it knows a unit's spawn tile, it counts the MOVE ops it wrote,
and it assumes the unit arrived. Nothing checks that assumption, and when it breaks the failure is
completely silent -- `_apply_unit_action` **ignores a move onto LOCKED** (`kaggriculture.py:313`)
without spending the turn or reporting anything, and every op after that lands one tile off.

Measured with `scripts/where_do_we_think_we_are.py` on the tape's own schedule: **every one of eleven
units spends 139-505 turns on a tile the emitter does not believe in**, and only 50 of 126 PLANT ops
survive -- 27 refused as LOCKED, 43 as OCCUPIED, because the unit is working its neighbour's tile.

The cause is `_spawn_hand` (`kaggriculture.py:508`), which picks the **minimum-occupancy** shed-access
tile in NWSE order **at the moment the HIRE settles**. It is not a function of the unit index at all.
Hire a whole crew in one turn with the farmer on `(4,4)` and the picks are:

    hand 1 -> (5, 4)   NE     escapable once 1 parcel is bought
    hand 2 -> (4, 5)   SW     escapable once 2 are
    hand 3 -> (5, 5)   SE     **both neighbours locked until then -- cannot move at all**
    hand 4 -> (4, 4)   NW

`routines.spawn_tile` encodes exactly that table, so it is right about a one-turn hire and wrong about
anything else. The tape never hires that way: it orders **two or three hands per turn across hours
1-4**, and keeps the farmer parked on `(4,4)` doing shed and pen work while it does, so each pair
wakes on `(5,4)` and `(4,5)` with `(4,4)` one step away and nothing ever lands on `(5,5)`.

    day 0: [(1, 2), (2, 1), (5, 1)]     post-turn 1: [[4,4], [5,4], [4,5]]
    day 1: [(1, 2), (2, 2), (3, 2)]     post-turn 2: [[4,4], [4,4], [4,4], [5,4], [4,5]]

Reproducing the cadence is not cosmetic fidelity -- it is what makes the spawn tile predictable, and a
predictable spawn tile is the entire basis of dead-reckoned routing.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R


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

pytestmark = [pytest.mark.slow, _OLD_LEADER_SKIP]
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TPD = R.TURNS_PER_DAY
STEP = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


@pytest.fixture(scope="module")
def replayed():
    """Our tape in the real environment, with dead reckoning carried alongside the true positions."""
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kaggle_environments import make
    from kagg.search import dayplan
    import build_script_submission as B

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, report = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    env = make("kaggriculture", debug=True)
    env.reset(2)

    drift = collections.Counter()
    first = {}
    reck = {}

    for t in range(len(plan)):
        day = t // TPD
        me = env.state[0].observation["farms"][0]
        real = [list(me["farmer"])] + [list(h) for h in (me.get("hands") or [])]
        farmer, hands_, market = plan[t]
        acts = [farmer] + list(hands_)

        if t % TPD == 0:                                  # `_end_of_day` sends everyone home
            reck = {u: list(R.spawn_tile(u)) for u in range(len(acts))}

        # A unit that did not exist when the day was planned adopts the position the env gives it --
        # this test is about the emitter's belief being wrong, not about it being absent.
        for u in range(len(real)):
            reck.setdefault(u, list(real[u]))

        for u in range(min(len(real), len(acts))):
            if reck[u] != real[u]:
                drift[u] += 1
                first.setdefault((day, u), (t, tuple(reck[u]), tuple(real[u])))

        for u, a in enumerate(acts):
            if a[0] in STEP and u in reck:
                dx, dy = STEP[a[0]]
                reck[u] = [reck[u][0] + dx, reck[u][1] + dy]

        env.step([{"farmer": farmer, "hands": hands_[:len(real)], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break

    return drift, first


def test_a_hand_wakes_where_the_emitter_thinks_it_does(replayed):
    """The spawn tile itself: a divergence on the first turn a unit acts is a wrong spawn, full stop."""
    drift, first = replayed
    dawn = {(day, u): v for (day, u), v in first.items() if v[0] % TPD <= 1}
    assert not dawn, "units woke somewhere the emitter did not expect:\n  " + "\n  ".join(
        f"day {day} unit {u}: we think {r}, really {a}"
        for (day, u), (t, r, a) in sorted(dawn.items())[:12])


def test_no_unit_ever_stands_where_the_emitter_does_not_believe(replayed):
    """And it must hold for the whole season, not just dawn -- a blocked move mid-tour is the same bug."""
    drift, first = replayed
    assert not drift, (
        "turns spent on a tile the emitter does not believe in, per unit: "
        f"{dict(sorted(drift.items()))}\nfirst divergences:\n  " + "\n  ".join(
            f"day {day} unit {u} turn {t}: we think {r}, really {a}"
            for (day, u), (t, r, a) in sorted(first.items())[:12]))
