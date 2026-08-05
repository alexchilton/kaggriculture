"""All four levels in one place, each measured at the resolution its own inference allows.

    level 1  exact (turn, unit, op, tile)  encode/decode      metric: cell (turn, unit)
    level 2  per (day, unit) work sequence + routing          metric: path A->B
    level 3  per (day, tile) work items, UNIT inferred        metric: (day, tile, op) multiset
    level 4  per-day counts only, TILE inferred               metric: (day, op) counts

Each level is scored against what it is actually deciding. Grading level 3 cell-by-cell would just
re-measure level 2's router, and grading level 4 by tile would measure a placement nobody claims to
reproduce -- the tape's tiles are one arrangement of many that satisfy the same counts.

Levels 3 and 4 inherit level 2's ceiling: the leader's router is his code and is measurably not
shortest-path (3774 of 3775 of his moves changed position, so the detours are policy, not obstacles).
"""
import collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R

TPD = R.TURNS_PER_DAY
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
tape = json.loads(pathlib.Path("data/seed_scripts/new_leader/tape.json").read_text())
sched = {int(k): v for k, v in
         json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text()).items()}

# ---------------------------------------------------------------- the tape, as facts
tape_by_day_tile = collections.Counter()     # (day, tile, op)
tape_by_day_op = collections.Counter()       # (day, op)
for r in tape:
    for c in r["units"]:
        if not c:
            continue
        nm = c["arg"] if c["op"] == "MOVE" else c["op"]
        if nm in MOVES or nm == "PASS":
            continue
        tape_by_day_op[(r["day"], c["op"])] += 1
        if c.get("tile"):
            tape_by_day_tile[(r["day"], tuple(c["tile"]), c["op"])] += 1

placements = collections.defaultdict(lambda: dict(plants=[], builds=[]))
pending = {}
for r in tape:
    for c in r["units"]:
        if not c or not c.get("tile"):
            continue
        t = tuple(c["tile"])
        if c["op"] == "PLANT":
            placements[r["day"]]["plants"].append((t, c["arg"]))
        elif c["op"] in ("BUILD_PASTURE", "BUILD_COOP"):
            pending[t] = r["day"]
        elif c["op"] == "PLACE" and c["arg"] in R.ANIMAL_NAMES:
            placements[pending.pop(t, r["day"])]["builds"].append((t, c["arg"]))
placements = dict(placements)


def emitted_facts(script):
    names = {v: k for k, v in R.OP.items()}
    D = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    op = np.asarray(script.unit_op)
    by_tile, by_op = collections.Counter(), collections.Counter()
    for u in range(op.shape[1]):
        pos = R.spawn_tile(u)
        for t in range(op.shape[0]):
            day = t // TPD
            if t % TPD == 0:
                pos = R.spawn_tile(u)
            nm = names.get(int(op[t, u]), "PASS")
            if nm in D:
                dx, dy = D[nm]
                nxt = (pos[0] + dx, pos[1] + dy)
                if 0 <= nxt[0] < R.BOARD_SIZE and 0 <= nxt[1] < R.BOARD_SIZE:
                    pos = nxt
                continue
            if nm == "PASS":
                continue
            by_op[(day, nm)] += 1
            by_tile[(day, tuple(pos), nm)] += 1
    return by_tile, by_op


def score(want, got, label):
    keys = set(want) | set(got)
    hit = sum(min(want[k], got[k]) for k in keys)
    tot = sum(want.values())
    extra = sum(max(0, got[k] - want[k]) for k in keys)
    print(f"  {label:<44} {hit:>5}/{tot:<5} {100*hit/max(tot,1):>6.2f}%   (+{extra} not in the tape)")
    return hit, tot


print("=" * 92)
print("LEVEL 3 -- tape's tiles given, emitter infers unit assignment and ordering")
print("=" * 92)
s3, r3 = dayplan.emit(sched, placements=placements)
t3, o3 = emitted_facts(s3)
score(tape_by_day_tile, t3, "(day, tile, op) matched")
score(tape_by_day_op, o3, "(day, op) matched")
print(f"  refusals: {len(r3['refused'])}")

print()
print("=" * 92)
print("LEVEL 4 -- per-day counts only, emitter infers tiles as well")
print("=" * 92)
s4, r4 = dayplan.emit(sched)
t4, o4 = emitted_facts(s4)
score(tape_by_day_tile, t4, "(day, tile, op) matched")
score(tape_by_day_op, o4, "(day, op) matched")
print(f"  refusals: {len(r4['refused'])}")

print()
print("  per-op totals, level 4:")
tape_tot = collections.Counter()
emit_tot = collections.Counter()
for (d, o), n in tape_by_day_op.items():
    tape_tot[o] += n
for (d, o), n in o4.items():
    emit_tot[o] += n
for k in sorted(set(tape_tot) | set(emit_tot), key=lambda k: -tape_tot[k]):
    print(f"    {k:>22} tape {tape_tot[k]:>5}  emitted {emit_tot[k]:>5}  {emit_tot[k]-tape_tot[k]:>+6}")
