"""Which DAY does each crop go into the ground -- ours, kawa's, and the clones'?

Alex, 2026-08-26: *"so would it be adaptable? if we took a few of the one guy and then adapting?"*

`data/logs/makeup.log` found the clone build is kawa's with three edits: melon pinned at **11** on
every shop draw, carrot **12 on early yarn / 20 on late**, and ~131 wheat. Ours carries melon 14-20
and a carrot count that follows no rule.

Whether we can copy that depends entirely on WHEN the plantings happen, because our season is four
different agents:

    d0-d3    authored opening      -- editable
    d4-d11   VERBATIM TAPE REPLAY  -- NOT editable without re-anchoring to a different tape
    d12-d23  solver, from PRECOMPUTED_ROUTES
    d24-d29  live planner

If the melon goes in during d4-d11 it is kawa's melon and the only way to change it is to replace
the tape -- a much bigger job, needing a clone tape plus a re-solve of the d12-d23 routes. If it
goes in from d12 the crop mix is ours to set.

Counted from PLANT ops, which are emitted once per planting. Never from BUY_SEED, a market order
re-posted every turn (`feedback_offers_are_not_fills`).
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
US = "alex chilton"
NEW = "data/seed_scripts/daily_2026-08-26"
OURS = "data/seed_scripts/ours_2026-08-26"
KAWA_DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
             "kawa_2026-08-24", "leaders_2026-08-24")
CROPS = ("WHEAT", "STRAWBERRY", "CARROT", "MELON")
ZONES = (("d0-d3 opening", 0, 3), ("d4-d11 TAPE", 4, 11),
         ("d12-d23 solver", 12, 23), ("d24-d29 planner", 24, 29))


def plants_by_day(replay, seat):
    out = collections.defaultdict(collections.Counter)
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if op and op[0] == "PLANT" and len(op) >= 2:
                out[t // TPD][op[1]] += 1
    return out


def herd(replay, seat):
    last = (replay["steps"][-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    if seat >= len(farms):
        return None, collections.Counter()
    h = collections.Counter()
    for row in (farms[seat].get("tiles") or []):
        for c in row:
            if isinstance(c, dict) and c.get("animal"):
                h[c["animal"]] += 1
    return float(farms[seat].get("money", 0)), h


def gather(pairs):
    acc = collections.defaultdict(lambda: collections.defaultdict(list))
    for replay, seat in pairs:
        pb = plants_by_day(replay, seat)
        for day in range(30):
            for c in CROPS:
                acc[day][c].append(pb.get(day, {}).get(c, 0))
    return acc, len(pairs)


def show(label, acc, n):
    print(f"=== {label}   ({n} seats)")
    print("   day" + "".join(f"{c[:5].lower():>9}" for c in CROPS))
    for day in sorted(acc):
        row = acc[day]
        vals = [sum(row[c]) / max(1, len(row[c])) for c in CROPS]
        if sum(vals) < 0.05:
            continue
        print(f"   {day:>3}" + "".join(f"{v:>9.1f}" for v in vals))
    print("   " + "-" * 40)
    for zlabel, lo, hi in ZONES:
        vals = []
        for c in CROPS:
            s = 0.0
            for day in range(lo, hi + 1):
                v = acc[day][c]
                s += sum(v) / max(1, len(v))
            vals.append(s)
        print(f"   {zlabel:<17}" + "".join(f"{v:>9.1f}" for v in vals))
    print()


def main():
    kawa = []
    for d in KAWA_DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:60]:
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA in names:
                kawa.append((r, names.index(KAWA)))
    clones = []
    for f in sorted(pathlib.Path(NEW).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        for seat in range(min(2, len(names))):
            money, h = herd(r, seat)
            if money is None or money < 125_000:
                continue
            cow, sheep = h.get("COW", 0), h.get("SHEEP", 0)
            if (cow >= 10 and sheep == 4) or (sheep >= 9 and cow <= 7):
                clones.append((r, seat))
    ours = []
    for f in sorted(pathlib.Path(OURS).glob("[0-9]*.json")):
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        ours.append((r, names.index(US) if US in names else 0))

    for label, pairs in (("KAWA", kawa), ("TOP CLONES", clones), ("OURS", ours)):
        acc, n = gather(pairs)
        show(label, acc, n)


if __name__ == "__main__":
    main()
