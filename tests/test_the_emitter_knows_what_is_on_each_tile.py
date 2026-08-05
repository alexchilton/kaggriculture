"""The emitter's board and the real board must agree, tile for tile, at every dawn.

`dayplan.Farm` is documented as deliberately not a simulator -- "tracks only what decides which op to
emit, and gets the rest wrong on purpose rather than expensively". That was a reasonable trade when the
gaps were measured in whole quadrants. It is now the binding constraint, because it assumes **every op
succeeds**, and the ops that matter most are the ones that silently do not.

Measured against the tape's own schedule, replaying both sides in the real environment:

    HARVEST verdicts                        OURS    TAPE
    OK                                       149     337
    ZERO YIELD -> the tile never clears        90       0
    nothing there                             47       1

    PLANT verdicts                          OURS
    OCCUPIED                                  58

The tape never wastes a harvest. Half of ours are wasted -- 137 turns a season -- and the two failure
directions are the same defect seen from both ends:

  * `_apply_unit_action` HARVEST returns early on `yield_units <= 0`, and a one-shot crop's yield comes
    ONLY from a WATER inside `[(max_day+1)//2, max_day]` (`_daily_refresh_plants` skips one-shot crops
    entirely). So a tile that missed its window waterings has zero yield, the HARVEST no-ops, and the tile
    is never cleared -- while `emit()` deletes it from `farm.crops` and believes the ground is free. Every
    later planting there fails OCCUPIED, forever.

  * The reverse: a tile our model still holds a crop for has actually cleared or weeded, so we walk to it
    and harvest nothing. 47 of those.

The consequence is the whole remaining gap. Worked tiles flatline at 34 from day 8 while the tape climbs
to 65 on ground we already own, which is 23 strawberry tiles against 40 ($15,480) and no room for the last
four pens ($28,500 in wool, milk and fertilizer). Total farm value tracks the tape to within a few percent
through day 8 and is 39% behind by day 15.

These assert the invariant directly rather than its symptoms, so they stay honest if the model is
rewritten: whatever `Farm` believes about a tile at dawn must be what the board holds.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

pytestmark = pytest.mark.slow

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TPD = R.TURNS_PER_DAY


@pytest.fixture(scope="module")
def verdicts():
    """Every HARVEST and PLANT our tape emits, judged against the board it actually lands on."""
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kaggle_environments import make
    from kagg.search import dayplan
    import build_script_submission as B

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    env = make("kaggriculture", debug=True)
    env.reset(2)
    harvest = collections.Counter()
    plant = collections.Counter()
    where = collections.defaultdict(list)

    for t in range(len(plan)):
        obs = env.state[0].observation
        me = obs["farms"][0]
        board = me["tiles"]
        real = [list(me["farmer"])] + [list(x) for x in (me.get("hands") or [])]
        farmer, hands_, market = plan[t]
        acts = ([farmer] + list(hands_))[:len(real)]

        for u, a in enumerate(acts):
            if not a:
                continue
            x, y = real[u]
            tile = board[y][x]
            if a[0] == "HARVEST":
                if not isinstance(tile, dict):
                    harvest["nothing there"] += 1
                    where["nothing there"].append((t, (x, y)))
                elif tile.get("yield_units", 0) <= 0:
                    harvest["zero yield"] += 1
                    where["zero yield"].append((t, (x, y), tile.get("kind")))
                else:
                    harvest["ok"] += 1
            elif a[0] == "PLANT":
                if tile == "LOCKED":
                    plant["locked"] += 1
                elif tile is not None:
                    plant["occupied"] += 1
                    where["occupied"].append((t, (x, y), tile if isinstance(tile, str)
                                              else tile.get("kind")))
                else:
                    plant["ok"] += 1

        env.step([{"farmer": farmer, "hands": hands_[:len(real)], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break
    return harvest, plant, where


def test_we_never_harvest_a_tile_with_nothing_on_it(verdicts):
    """47 today. Our model holds a crop for a tile that has actually cleared, weeded, or never grew."""
    harvest, plant, where = verdicts
    assert not harvest["nothing there"], (
        f"{harvest['nothing there']} HARVEST ops on an empty tile; first few "
        f"{where['nothing there'][:6]}")


def test_we_never_harvest_a_tile_that_has_produced_nothing(verdicts):
    """90 today, against the tape's zero.

    On a crop this is fatal rather than merely wasteful: HARVEST is what clears a one-shot tile, so a
    zero-yield tile stays occupied for the rest of the season and every replant there no-ops.
    """
    harvest, plant, where = verdicts
    assert not harvest["zero yield"], (
        f"{harvest['zero yield']} HARVEST ops on a tile holding nothing; first few "
        f"{where['zero yield'][:6]}")


def test_we_never_plant_on_ground_that_is_already_taken(verdicts):
    """58 today. The other end of the same disagreement: the model says free, the board says occupied."""
    harvest, plant, where = verdicts
    assert not plant["occupied"], (
        f"{plant['occupied']} PLANT ops onto an occupied tile; first few {where['occupied'][:6]}")
