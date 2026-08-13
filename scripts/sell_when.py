"""Per-product SELL fills per day, ours vs tape, from inside breakdown's own harness.

`Fills.bind_farms` is called once per turn, so it is the turn clock; `Fills.record` is the only
place a commit lands. Both runs live in one process, so rows are split on the turn counter
wrapping past 720.
"""
import collections, sys
sys.path.insert(0, '.')
from kagg.analysis import fills as F

TURN = [-1]
ROWS = []
_bind, _rec = F.Fills.bind_farms, F.Fills.record


def bind(self, farms):
    TURN[0] += 1
    return _bind(self, farms)


def rec(self, op, item, price, farm):
    seat = self._seat(farm)
    if seat == 0 and op == "SELL":
        ROWS.append((TURN[0], item, price))
    return _rec(self, op, item, price, farm)


F.Fills.bind_farms, F.Fills.record = bind, rec
sys.argv = ['breakdown.py'] + sys.argv[1:]
import scripts.breakdown as B
B.main()

runs = [[], []]
prev, which = -1, 0
for t, item, price in ROWS:
    if t < prev:
        which = 1
    prev = t
    runs[which].append((t // 24, item, price))

PROD = ("WHEAT", "STRAWBERRY", "MELON", "MILK", "WOOL", "EGG", "FERTILIZER", "TOMATO", "CARROT")
agg = [collections.defaultdict(lambda: [0, 0.0]) for _ in range(2)]
for i, rows in enumerate(runs):
    for d, item, price in rows:
        cell = agg[i][(d, item)]
        cell[0] += 1
        cell[1] += price

print("\n\n  SELL fills per day, ours/tape   (units, and $ per unit)\n")
hdr = "".join("%14s" % ("d%d" % d) for d in range(18, 30))
for item in PROD:
    if not any((d, item) in agg[i] for i in (0, 1) for d in range(30)):
        continue
    print("  %s\n            %s" % (item, hdr))
    line = "  units   "
    rev = "  $/unit  "
    for d in range(18, 30):
        a = agg[0].get((d, item), [0, 0.0])
        b = agg[1].get((d, item), [0, 0.0])
        line += "%14s" % ("%d/%d" % (a[0], b[0]))
        pa = a[1] / a[0] if a[0] else 0
        pb = b[1] / b[0] if b[0] else 0
        rev += "%14s" % ("%.0f/%.0f" % (pa, pb))
    print(line)
    print(rev)
    print()
for i, name in enumerate(("ours", "tape")):
    tot = sum(v[1] for v in agg[i].values())
    print("  %s total sell revenue  $%.0f" % (name, tot))
