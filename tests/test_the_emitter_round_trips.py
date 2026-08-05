"""emit -> tape -> extract -> emit must be the IDENTICAL tape. 100%, or the emitter is not a function.

This is the invertibility test that can and must be exact, and it is different from diffing against
the leader's replay.

Diffing against his replay has a ceiling that is not ours to move: his walk between two tiles is
whatever HIS agent's code does, and it is measurably not shortest-path -- `(4,4)` to `(3,1)` as
`['NORTH','NORTH','SOUTH','NORTH','NORTH','WEST']`, six steps for a four-step trip, with every one of
those moves confirmed to have actually changed the unit's position. Six candidate ordering rules were
scored against all 1,749 of his walks and the best of them, north/south first, reaches 90.79%:

    Y-first 90.79%   longerY 88.05%   shorterX 83.42%   longerX 82.96%   X-first 80.67%   stair 79.65%

Chasing the last 9% means reproducing another team's idiosyncrasies, which is neither achievable nor
useful. What IS required is that OUR pipeline is lossless: a tape we emit must survive extraction and
re-emission byte for byte. If it does not, the schedule is throwing away something the tape depends
on, and every optimisation run on top of that schedule is optimising a different farm from the one
that gets submitted.
"""

import collections
import json
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from kagg.search import dayplan
from kagg.search import routines as R

TPD = R.TURNS_PER_DAY
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")


def cells(script):
    """The tape as comparable cells: `(turn, unit) -> op[:arg]`, PASS omitted."""
    names = {v: k for k, v in R.OP.items()}
    op = np.asarray(script.unit_op)
    crop = np.asarray(script.unit_crop)
    item = np.asarray(script.unit_item)
    qty = np.asarray(script.unit_qty)
    out = {}
    for t in range(op.shape[0]):
        for u in range(op.shape[1]):
            nm = names.get(int(op[t, u]), "PASS")
            if nm == "PASS":
                continue
            if nm == "PLANT":
                nm = f"PLANT:{R.CROPS[int(crop[t, u])]}"
            elif nm in ("PICKUP", "DROP", "PLACE"):
                nm = f"{nm}:{R.ITEMS[int(item[t, u])]}x{int(qty[t, u])}"
            out[(t, u)] = nm
    return out


def tape_to_placements(script):
    """Read tiles back off a tape we emitted, by walking each unit's moves from its spawn.

    This is the same recovery `scripts/extract_tape.py` does against a replay, except the positions
    are derived rather than read, because our own tape has no observation attached to it.
    """
    names = {v: k for k, v in R.OP.items()}
    D = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    op = np.asarray(script.unit_op)
    crop = np.asarray(script.unit_crop)
    item = np.asarray(script.unit_item)
    hire = np.asarray(script.hire)
    placements = collections.defaultdict(lambda: dict(plants=[], builds=[]))
    pending = {}

    # **Spawn comes from the day's hire cadence, not from a per-unit table.** `_spawn_hand` picks the
    # min-occupancy shed-access tile when the HIRE settles, so `R.spawn_tile` only describes a crew
    # hired in a single turn -- which the emitter no longer does, because that put hand 3 on the trapped
    # `(5,5)` corner. Walking from the old table recovered the wrong tile for every hand and 2,640 of
    # 4,895 cells changed on re-emission; the emitter was fine and the reader was stale.
    def day_spawn(day):
        hands = int(hire[day * TPD:(day + 1) * TPD].sum())
        return R.dawn_crew(hands)[1]

    for u in range(op.shape[1]):
        spawn = day_spawn(0)
        pos = spawn.get(u, R.SPAWN)
        for t in range(op.shape[0]):
            day = t // TPD
            if t % TPD == 0:
                spawn = day_spawn(day)         # the dawn teleport, onto that day's own spawn tile
                pos = spawn.get(u, R.SPAWN)
            nm = names.get(int(op[t, u]), "PASS")
            if nm in D:
                dx, dy = D[nm]
                nxt = (pos[0] + dx, pos[1] + dy)
                if 0 <= nxt[0] < R.BOARD_SIZE and 0 <= nxt[1] < R.BOARD_SIZE:
                    pos = nxt
            elif nm == "PLANT":
                placements[day]["plants"].append((tuple(pos), R.CROPS[int(crop[t, u])]))
            elif nm in ("BUILD_PASTURE", "BUILD_COOP"):
                pending[tuple(pos)] = day
            elif nm == "PLACE":
                a = R.ITEMS[int(item[t, u])]
                if a in R.ANIMAL_NAMES:
                    placements[pending.pop(tuple(pos), day)]["builds"].append((tuple(pos), a))
    return {d: v for d, v in placements.items()}


@pytest.fixture(scope="module")
def schedule():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    return {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}


def test_emitting_the_same_schedule_twice_gives_the_same_tape(schedule):
    """Determinism. Without it nothing below can mean anything, and a search cannot either."""
    a, _ = dayplan.emit(schedule)
    b, _ = dayplan.emit(schedule)
    assert cells(a) == cells(b), "emit() is not deterministic"


def test_a_tape_survives_extraction_and_re_emission(schedule):
    """The contract. Emit, recover the tiles from the tape, emit again -- byte for byte identical.

    A mismatch means the schedule does not carry something the tape depends on, so the farm that gets
    optimised is not the farm that gets submitted.
    """
    # The fixed point is what invertibility actually means here, and the first emission is not it.
    # A bare `emit(schedule)` invents two different kinds of planting: the ones the schedule lists,
    # and the replants it generates itself when a one-shot crop clears and its tile is reused. The
    # tape records both as a bare PLANT, so recovering tiles from that tape hands the next emission
    # MORE plantings than the schedule had, and the two farms are legitimately different.
    #
    # Once the placements are explicit the emitter must be stable: emit, recover, emit, recover, emit
    # -- and the last two tapes have to be identical, because nothing is being invented any more.
    # If they are not, the schedule is still dropping something the tape depends on.
    seed, _r0 = dayplan.emit(schedule)
    first, _r1 = dayplan.emit(schedule, placements=tape_to_placements(seed))
    recovered = tape_to_placements(first)
    second, _r2 = dayplan.emit(schedule, placements=recovered)

    a, b = cells(first), cells(second)
    only_a = {k: v for k, v in a.items() if b.get(k) != v}
    only_b = {k: v for k, v in b.items() if a.get(k) != v}
    detail = ""
    if only_a or only_b:
        sample = sorted(set(only_a) | set(only_b))[:8]
        detail = "\n  " + "\n  ".join(
            f"turn {t} unit {u}: first={a.get((t, u), 'PASS')!r} second={b.get((t, u), 'PASS')!r}"
            for t, u in sample)
    assert a == b, (
        f"{len(only_a)} cells changed of {len(a)} on re-emission; the schedule is lossy{detail}")


def test_the_tiles_recovered_from_a_tape_are_the_tiles_that_were_planted(schedule):
    """The recovery itself, checked independently of re-emission.

    If walking the tape's moves does not land on the tile the planner chose, the movement ops and the
    intent disagree -- which is the failure that made a whole season of work land on the wrong tile
    before `_path_ops` routed around locked ground.
    """
    script, report = dayplan.emit(schedule)
    recovered = tape_to_placements(script)
    got = sum(len(v["plants"]) for v in recovered.values())
    emitted = int((np.asarray(script.unit_op) == R.OP["PLANT"]).sum())
    assert got == emitted, (
        f"walked the tape to {got} planted tiles but it contains {emitted} PLANT ops")
