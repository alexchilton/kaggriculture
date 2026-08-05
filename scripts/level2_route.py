"""Level 2, isolated: does `_path_ops(A, B)` equal the walk the tape actually took from A to B?

The first cut of this test packed each unit's work ops contiguously from turn 1 and compared cells.
It scored 5/114 on day 0 and the reason was a single line of its own output: `PASS 0/680`. The tape
IDLES mid-day -- 680 of its cells are PASS sitting between work ops -- so a contiguous packing shifts
every op after the first gap and the comparison measures alignment, not routing.

So this compares paths directly. For every consecutive pair of work ops on the same (day, unit), take
the tile the unit was on and the tile it acted on next, and diff our router's walk against the moves
the tape actually emitted between them. Nothing about timing is involved.
"""
import collections, json, pathlib, sys
sys.path.insert(0, ".")
from kagg.search import routines as R

TD = 24
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
tape = json.loads(pathlib.Path("data/seed_scripts/new_leader/tape.json").read_text())
sched = json.loads(pathlib.Path("data/seed_scripts/new_leader/schedule.json").read_text())
land_days = sorted(int(k) for k, v in sched.items() if v["land"])
def parcels_on(day):
    return sum(1 for L in land_days if L <= day)

# Per (day, unit): the ordered cells, so we can slice the moves BETWEEN two work ops.
seqs = collections.defaultdict(list)
for r in tape:
    for u, c in enumerate(r["units"]):
        if not c:
            continue
        name = c["arg"] if c["op"] == "MOVE" else c["op"]
        seqs[(r["day"], u)].append((name, tuple(c["tile"]) if c.get("tile") else None))

examples_all = []
exact = differ = 0
same_len = 0
len_gap = collections.Counter()
for key, cells in sorted(seqs.items()):
    # walk the day, collecting (from_tile, to_tile, actual_moves)
    i = 0
    while i < len(cells):
        name, tile = cells[i]
        if name in MOVES:
            src = tile
            got = []
            while i < len(cells) and cells[i][0] in MOVES:
                got.append(cells[i][0])
                i += 1
            dst = cells[i][1] if i < len(cells) else None
            if src and dst:
                want = R._path_ops(src, dst, parcels=parcels_on(key[0]))
                if want == got:
                    exact += 1
                else:
                    differ += 1
                    if len(want) == len(got):
                        same_len += 1
                    len_gap[len(want) - len(got)] += 1
                    examples_all.append((key, src, dst, got, want))
        else:
            i += 1

tot = exact + differ
print("=" * 84)
print("LEVEL 2 -- router only: _path_ops(A,B) vs the walk the tape took from A to B")
print("=" * 84)
print(f"  paths compared : {tot}")
print(f"  exact          : {exact}  ({100*exact/max(tot,1):.2f}%)")
print(f"  differ         : {differ}   of which {same_len} are the same LENGTH (order only)")
print()
print("  length difference (ours - tape):")
for k in sorted(len_gap):
    print(f"     {k:>+3} steps : {len_gap[k]:>5}")
print()
print("  first divergences:")
# Split the two failure modes: same length is an ordering rule, longer is a detour.
order_only, detour = [], []
for key, src, dst, got, want in examples_all:
    (order_only if len(got) == len(want) else detour).append((key, src, dst, got, want))

def axis_first(moves):
    if not moves:
        return "-"
    return "Y" if moves[0] in ("NORTH", "SOUTH") else "X"

import collections as _c
rule = _c.Counter()
for _k, src, dst, got, _w in order_only:
    if src[0] != dst[0] and src[1] != dst[1]:
        rule[axis_first(got)] += 1
print(f"  SAME-LENGTH cases -- which axis the tape moves FIRST when both differ:")
for k, v in rule.most_common():
    print(f"     {k} first : {v}")
print(f"  (ours always does X first: `_axis_ops` emits EAST/WEST then NORTH/SOUTH)")
print()
print("  DETOUR cases (tape walks further than the direct route):")
for key, src, dst, got, want in detour[:6]:
    print(f"    day {key[0]:>2} unit {key[1]}: {src} -> {dst}  tape {len(got)} vs ours {len(want)}")
    print(f"        tape : {got}")
    print(f"        ours : {want}")
