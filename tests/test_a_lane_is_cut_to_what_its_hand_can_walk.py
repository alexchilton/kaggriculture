"""Day 4 leaves ten crop ops undone, and the crop crew has nowhere near the turns to do them.

`harvest 10/14` and `water 11/17` on d4 are one defect with one cause. Traced through the real
agent at seed 11 against tape 91422988 (`data/logs/probe_stall.log`), the crop sweep is 17 tiles,
each wanting WATER and HARVEST, and three hands are sent at it:

    shed at (4,4)   crop hands [2, 4, 5]

    u2 at (4,5) budget 23  takes 3 tiles -> 23 turns, 0 spare
         REFUSED (0,2): tour would cost 26   (last tile (0,3), step dist 1)
    u4 at (5,4) budget 23  takes 2 tiles -> 12 turns, 11 spare
         REFUSED (2,2): tour would cost 24   (last tile (1,2), step dist 1)
    u5 at (4,5) budget 23  takes 4 tiles -> 22 turns, 1 spare
         REFUSED (2,1): tour would cost 34   (last tile (3,1), step dist 1)

**Every refused tile is one square from the last tile taken and costs twelve turns.** That is not
the walk to the tile; it is `materialise` inserting a round trip to the shed because the hand is
full of harvest. A crop tile does not cost its two ops, it costs two ops plus a share of a
twelve-turn ferry, and the sweep is ~94 materialised turns against the crop crew's 3 x 23 = 69.

So the hands were not idling -- they were full -- and no rule about how the lanes are CUT can
recover this. Two were tried and measured, both against the 17-day grid:

    spill an overflowing lane into the next one   13 -> 12 dropped turns
    cut each lane to what its hand can walk       13 -> 12 dropped turns, and a LOSS overall:
                                                  d0 `place 4/4 -> 3/4` with a sheep left unpenned,
                                                  d6 `tiles 75/75 -> 50/75`, parcel gone

The binding constraint is one level up, at `crew.cover`'s `k_herd`: it splits the hands between the
herd and the crops in proportion to raw JOB turns -- 24 against 31, giving 3 and 3 -- and job turns
are the one measure that omits the ferry. Herd work sits beside the shed and is cheap per op; crop
work has to be carried. Sizing the crews by materialised cost is the untried delta.

**The PLACE/FEED/CARE drops on d1, d3 and d4 are a different thing and are not asserted against.**
They are the `stock` guard in `cover`: three empty pens and one animal in the shed, so two
placements are correctly refused, and `place 1/1` agrees with the tape on both days.

Why this matters past the two rows it costs: a planner that bins work reports a day as undoable
when it is merely under-crewed, so it cannot yet be trusted to tell the search which schedule rows
are executable inside 24 hours -- which is the job it is wanted for next.
"""
import collections
import importlib
import json
import pathlib

import pytest
from kaggle_environments import make

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
MODULE = "kagg.search.schedule_agent_1455mh"
SEED = 11
DAYS = 7

#: The ops this test owns. Herd and structure drops have their own cause (the `stock` guard) and a
#: matching `place` row on the tape, so they are deliberately out of scope.
CROP_OPS = frozenset({"PLANT", "WATER", "HARVEST"})


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])]


@pytest.fixture(scope="module")
def drops():
    """Every real `crew.cover` call the agent makes over d0-d6, with what it dropped and the spare
    budget it dropped it against.

    The planner is wrapped rather than called directly on purpose: the inputs that matter here are
    the live board, the hands' positions and each hand's remaining budget at dawn, and a
    hand-built fixture would be asserting against my arithmetic instead of the agent's.
    """
    DP = importlib.import_module("kagg.search.cover")
    CREW = importlib.import_module("kagg.search.crew")
    SA = importlib.import_module(MODULE)

    raw = json.loads(SCHEDULE.read_text())
    thin = {int(k): {a: b for a, b in v.items() if a not in TAPE_ONLY} for k, v in raw.items()}
    opp = _opponent()

    calls = []
    real = CREW.cover

    def spy(units, jobs, budget, depots=DP.SHED, carry=None, supply=None, deliver=True,
            wanted=None, day=None, rush=False, due=None):
        work, uncovered = real(units, jobs, budget, depots, carry, supply, deliver, wanted, day,
                               rush, due)
        used = {}
        for u, seq in work.items():
            route = DP.materialise(units[u], seq, (carry or {}).get(u) or {},
                                   tuple(depots or DP.SHED), wanted, False, rush, due=due)
            used[u] = DP.turns(units[u], route)
        calls.append({
            "day": day,
            "uncovered": list(uncovered),
            "crop_turns": sum(j.turns for j in uncovered
                              if all(o in CROP_OPS for o, _i in j.ops)),
            "crop_ops": collections.Counter(o for j in uncovered for o, _i in j.ops
                                            if o in CROP_OPS),
            "slack": sum(max(0, budget[u] - used.get(u, 0)) for u in range(len(units))),
            "load": {u: (used.get(u, 0), budget[u]) for u in range(len(units))},
        })
        return work, uncovered

    CREW.cover = spy
    try:
        env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0},
                   debug=True)
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        for t in range(24 * DAYS):
            o0 = env.state[0].observation
            a0, a1 = agent(o0), opp[t]
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    finally:
        CREW.cover = real
    return {c["day"]: c for c in calls}


def test_the_premise_the_crew_planner_actually_ran(drops):
    """Runs first. `crew.ACTIVE_UNTIL_DAY` gates this module off, and a gated-off planner drops
    nothing because it is never called -- which would make every assertion below vacuously true."""
    CREW = importlib.import_module("kagg.search.crew")
    assert CREW.ACTIVE_UNTIL_DAY >= 5, (
        f"crew.ACTIVE_UNTIL_DAY is {CREW.ACTIVE_UNTIL_DAY}, so day 4 is planned by `cover.cover` "
        "and this test measures nothing."
    )
    assert 4 in drops, "no crew.cover call was recorded for day 4."


def test_no_hand_is_left_wholly_idle_on_a_day_that_drops_work(drops):
    """The weakest claim the measurement actually supports, and deliberately not a stronger one.

    The obvious assertion -- "nothing is dropped while the crew holds more spare turns than the
    dropped work costs" -- was written first and is WRONG. Spare turns do not pool: u4 finishing
    with 11 to spare cannot lend them to u5, and the next tile costs 12 because it drags a shed
    ferry with it. Summing slack across hands invents a capacity that no single hand has, and a
    test built on it demands something no cut of the lanes can deliver.

    A hand that does nothing at all is a different and unambiguous claim -- its whole budget was
    available from its own position and went unused.
    """
    offenders = []
    for day, c in sorted(drops.items()):
        idle = [u for u, (used, _b) in c["load"].items() if used == 0]
        if c["crop_turns"] and idle:
            offenders.append((day, dict(c["crop_ops"]), c["crop_turns"], idle, c["load"]))
    assert not offenders, "\n".join(
        f"day {d}: dropped {ops} ({turns} turns) with hands {idle} untouched.\n"
        f"          load per hand (used/budget): "
        + "  ".join(f"u{u}:{a}/{b}" for u, (a, b) in sorted(load.items()))
        for d, ops, turns, idle, load in offenders)


def test_day_four_covers_every_crop_job(drops):
    """The row this is being fixed for, named explicitly so a fix that helps elsewhere and leaves
    d4 alone cannot pass. d4 is the first day the sweep is asked for more than it trivially fits."""
    c = drops[4]
    assert not c["crop_ops"], (
        f"day 4 dropped {dict(c['crop_ops'])} with {c['slack']} spare turns. That is the whole of "
        f"`harvest 10/14` and `water 11/17` on the grid."
    )
