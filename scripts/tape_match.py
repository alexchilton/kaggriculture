"""How close is tape B to tape A? Per-day, per-op, unit ops and market orders together.

Money is the outcome; this is the target. If B matches A the money follows, and chasing the money
directly is what produced a sweep over sell-lot sizes that moved the bank around without ever asking
whether the tape was right.
"""
import collections, json, pathlib, sys
sys.path.insert(0, "."); sys.path.insert(0, "scripts")
import numpy as np
from kagg.search import dayplan, routines as R

TPD = R.TURNS_PER_DAY
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
d = json.load(open("data/seed_scripts/new_leader/90016067.json"))
seat = d["info"]["TeamNames"].index("somewhere after")
sched = {int(k): v for k, v in
         json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text()).items()}

A_ops, A_mkt = collections.Counter(), collections.Counter()
for t, st in enumerate(d["steps"][1:]):
    day = t // TPD
    act = (st[seat] or {}).get("action") or {}
    for o in [act.get("farmer")] + list(act.get("hands") or []):
        if o and o[0] != "PASS":
            A_ops[(day, o[0])] += 1
    for o in (act.get("market") or []):
        if o:
            A_mkt[(day, o[0])] += int(o[2]) if len(o) > 2 else 1

script, rep = dayplan.emit(sched)
names = {v: k for k, v in R.OP.items()}
op = np.asarray(script.unit_op)
B_ops, B_mkt = collections.Counter(), collections.Counter()
for t in range(op.shape[0]):
    for u in range(op.shape[1]):
        nm = names.get(int(op[t, u]), "PASS")
        if nm != "PASS":
            B_ops[(t // TPD, nm)] += 1
arr = script.arrays()
for t in range(arr["sell"].shape[0]):
    day = t // TPD
    B_mkt[(day, "HIRE")] += int(arr["hire"][t])
    B_mkt[(day, "SELL")] += int(arr["sell"][t].sum())
    B_mkt[(day, "BUY_PRODUCT")] += int(arr["buy_product"][t].sum())
    B_mkt[(day, "BUY_SEED")] += int(arr["buy_seed"][t].sum())
    B_mkt[(day, "BUY_ANIMAL")] += int(arr["buy_animal"][t].sum())
    B_mkt[(day, "BUY_LAND")] += int(arr["buy_land"][t])


def report(A, Bc, title):
    keys = set(A) | set(Bc)
    hit = sum(min(A[k], Bc[k]) for k in keys)
    tot = sum(A.values())
    over = sum(max(0, Bc[k] - A[k]) for k in keys)
    print(f"  {title:<22} {hit:>6}/{tot:<6} {100*hit/max(tot,1):>6.2f}%   over-emitted {over}")
    by = collections.defaultdict(lambda: [0, 0])
    for (day, o), n in A.items():
        by[o][0] += n
    for (day, o), n in Bc.items():
        by[o][1] += n
    for o in sorted(by, key=lambda o: -by[o][0]):
        a, b = by[o]
        if o in MOVES:
            continue
        print(f"      {o:>20} A {a:>6}  B {b:>6}  {b-a:>+7}")


print("=" * 76)
print("TAPE MATCH -- B against A, per day per op")
print("=" * 76)
report(A_ops, B_ops, "unit ops")
print()
report(A_mkt, B_mkt, "market orders")
print(f"\n  refusals: {len(rep['refused'])}")
