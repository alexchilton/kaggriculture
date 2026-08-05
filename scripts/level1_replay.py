"""Level 1: the tape's own (turn, unit, op) written straight back out. Must be 100%.

Nothing is inferred here -- every cell is copied. So this tests exactly one thing: whether the
`Script` array layout and `build_script_submission`'s decoding can REPRESENT the tape at all. If this
is not 100% the vocabulary is wrong, and no amount of planning above it can ever be right.

It is the floor the other levels are measured against:

    level 1  exact (turn, unit, op, tile)   -> encode/decode only
    level 2  per-day (unit, tile, op)       -> + ordering and routing
    level 3  per-day (tile, op)             -> + unit assignment
    level 4  per-day counts                 -> + tile placement
"""
import collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import routines as R

TD = 24
tape = json.loads(pathlib.Path("data/seed_scripts/new_leader/tape.json").read_text())
script = R.Script()
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}

unknown = collections.Counter()
written = 0
for r in tape:
    t = r["turn"]
    if t >= script.T:
        break
    for u, c in enumerate(r["units"]):
        if not c or u >= script.U:
            continue
        name = c["op"]
        if name == "MOVE":
            name = c["arg"]
        if name == "PASS":
            continue
        if name not in R.OP:
            unknown[name] += 1
            continue
        crop = c["arg"] if name == "PLANT" and c["arg"] in R.CROPS else None
        item = c["arg"] if name in ("PICKUP", "DROP", "PLACE") and c["arg"] in R.ITEMS else None
        qty = int(c["qty"] or 1) if item else 0
        script.op(t, u, name, item=item, qty=qty, crop=crop)
        written += 1

names = {v: k for k, v in R.OP.items()}
op = np.asarray(script.unit_op)
live = hit = 0
per_op = collections.defaultdict(lambda: [0, 0])
for r in tape:
    t = r["turn"]
    if t >= op.shape[0]:
        break
    for u in range(op.shape[1]):
        c = r["units"][u] if u < len(r["units"]) else None
        want = "PASS"
        if c:
            want = c["arg"] if c["op"] == "MOVE" else c["op"]
        got = names.get(int(op[t, u]), "PASS")
        if want == "PASS" and got == "PASS":
            continue
        live += 1
        per_op[want][1] += 1
        if want == got:
            hit += 1
            per_op[want][0] += 1

print("=" * 78)
print(f"LEVEL 1 -- tape copied straight into the Script arrays")
print("=" * 78)
print(f"  cells written : {written}")
print(f"  strict match  : {hit}/{live}  ({100*hit/max(live,1):.2f}%)")
if unknown:
    print(f"  UNKNOWN OPS   : {dict(unknown)}  <-- not in routines.OP, cannot be represented")
print()
print(f"{'op':>22} {'match':>12}")
for k in sorted(per_op, key=lambda k: -per_op[k][1]):
    h, n = per_op[k]
    flag = "" if h == n else "   <-- LOSSY"
    print(f"{k:>22} {h:>5}/{n:<5} {flag}")
