"""Strict cell match: PASS==PASS is not a match, it is an empty row.

The earlier metric counted every idle unit-turn as a hit, so day 0 read 220/312 = 71% when 192 of
those cells were two blanks agreeing with each other. Excluding them the same day is 28/120 = 23%.
A test that scores 71% for doing nothing is not a test.

This counts only cells where the tape or the emitter did something, and prints the turn-by-turn
sequence for one unit so the divergence is visible rather than aggregated.
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R

ap = argparse.ArgumentParser()
ap.add_argument("--day", type=int, default=0)
ap.add_argument("--unit", type=int, default=-1, help="-1 = summary for all units")
a = ap.parse_args()
TD = 24

tape = json.loads(pathlib.Path("data/seed_scripts/new_leader/tape.json").read_text())
sched = {int(k): v for k, v in
         json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text()).items()}

placements = collections.defaultdict(lambda: dict(plants=[], builds=[]))
pending = {}
for r in tape:
    for c in r["units"]:
        if not c or not c.get("tile"):
            continue
        tile = tuple(c["tile"])
        if c["op"] == "PLANT":
            placements[r["day"]]["plants"].append((tile, c["arg"]))
        elif c["op"] in ("BUILD_PASTURE", "BUILD_COOP"):
            pending[tile] = r["day"]
        elif c["op"] == "PLACE" and c["arg"] in R.ANIMAL_NAMES:
            placements[pending.pop(tile, r["day"])]["builds"].append((tile, c["arg"]))

script, rep = dayplan.emit(sched, placements=dict(placements))
names = {v: k for k, v in R.OP.items()}
op = np.asarray(script.unit_op)

def t_cell(t, u):
    if t >= len(tape):
        return "PASS", None
    c = tape[t]["units"][u] if u < len(tape[t]["units"]) else None
    if not c:
        return "PASS", None
    return ({"MOVE": c["arg"]}.get(c["op"], c["op"]),
            tuple(c["tile"]) if c.get("tile") else None)

def e_cell(t, u):
    if t >= op.shape[0] or u >= op.shape[1]:
        return "PASS"
    return names.get(int(op[t, u]), "PASS")

print("=" * 88)
print(f"DAY {a.day} STRICT MATCH -- PASS/PASS excluded")
print("=" * 88)
print(f"{'unit':>5} {'tape ops':>9} {'emitted':>9} {'match':>7} {'strict %':>9}")
tot_live = tot_hit = 0
for u in range(13):
    live = hit = t_ops = e_ops = 0
    for t in range(a.day * TD, (a.day + 1) * TD):
        h, _ = t_cell(t, u)
        e = e_cell(t, u)
        if h != "PASS":
            t_ops += 1
        if e != "PASS":
            e_ops += 1
        if h == "PASS" and e == "PASS":
            continue
        live += 1
        if h == e:
            hit += 1
    if live:
        print(f"{u:>5} {t_ops:>9} {e_ops:>9} {hit:>4}/{live:<4} {100*hit/live:>8.0f}%")
    tot_live += live; tot_hit += hit
print(f"{'ALL':>5} {'':>9} {'':>9} {tot_hit:>4}/{tot_live:<4} "
      f"{100*tot_hit/max(tot_live,1):>8.0f}%")

if a.unit >= 0:
    u = a.unit
    print()
    print(f"UNIT {u}, TURN BY TURN")
    print(f"{'turn':>5} {'TAPE':>22} {'tile':>10} {'EMITTED':>22} {'':>3}")
    for t in range(a.day * TD, (a.day + 1) * TD):
        h, tile = t_cell(t, u)
        e = e_cell(t, u)
        mark = "" if h == e else "  <-- differs"
        print(f"{t % TD:>5} {h:>22} {str(tile):>10} {e:>22} {mark}")
