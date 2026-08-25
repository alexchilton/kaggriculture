"""What does カワシギ spend d27-d29 on, and is there strawberry standing when he starves?

Alex: "i assume he only lets them starve if strawberry is better to get in?" -- an assumption worth
testing rather than building on. Two questions, both answerable off the recording:

  1. His op mix on d27, d28 and d29. If the turns freed by not feeding go into HARVEST, that is the
     mechanism. If they go into WATER or PLANT it is something else.
  2. What is standing on his board on those days, by crop. STRAWBERRY is `ongoing`, so it keeps
     producing to the bell and keeps needing a visit; if the seats where he starves most are the
     seats holding most strawberry, the assumption holds.

Cross-tabbed by how many sheep the seat loses, because the claim is specifically that the starving
and the strawberry go together.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

KAWA = "カワシギ"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")
TPD = 24
LATE = (27, 28, 29)


def main():
    ops_by_day = collections.defaultdict(collections.Counter)
    seats_by_day = collections.Counter()
    # sheep lost -> Counter of standing units by crop at d27
    standing = collections.defaultdict(collections.Counter)
    seats_by_lost = collections.Counter()
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(r, dict):
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            seat = names.index(KAWA)
            steps = r.get("steps") or []
            placed = collections.Counter()
            for step in steps:
                if seat >= len(step):
                    continue
                act = (step[seat] or {}).get("action") or {}
                for op in [act.get("farmer")] + list(act.get("hands") or []):
                    if op and len(op) >= 2 and op[0] == "PLACE" and op[1] == "SHEEP":
                        placed["SHEEP"] += 1
            farms_end = ((steps[-1][0] or {}).get("observation") or {}).get("farms") or []
            alive = 0
            if seat < len(farms_end):
                alive = sum(1 for row in (farms_end[seat].get("tiles") or []) for t in row
                            if isinstance(t, dict) and t.get("animal") == "SHEEP")
            lost = placed["SHEEP"] - alive
            seats_by_lost[lost] += 1

            for day in LATE:
                lo, hi = day * TPD, min((day + 1) * TPD, len(steps))
                if lo >= len(steps):
                    continue
                seats_by_day[day] += 1
                for t in range(lo, hi):
                    act = (steps[t][seat] or {}).get("action") or {}
                    for op in [act.get("farmer")] + list(act.get("hands") or []):
                        if op:
                            ops_by_day[day][op[0]] += 1
            t27 = 27 * TPD
            if t27 < len(steps):
                farms = ((steps[t27][0] or {}).get("observation") or {}).get("farms") or []
                if seat < len(farms):
                    for row in (farms[seat].get("tiles") or []):
                        for tile in row:
                            if isinstance(tile, dict) and tile.get("crop"):
                                standing[lost][tile["crop"]] += tile.get("yield_units", 0)
                                standing[lost][tile["crop"] + "_tiles"] += 1

    print("HIS OP MIX ON THE LAST THREE DAYS (mean ops per seat)", flush=True)
    kinds = ["HARVEST", "FEED", "CARE", "WATER", "PLANT", "MOVE", "PICKUP", "DROP",
             "COLLECT_FERTILIZER", "FERTILIZE", "PASS"]
    print(f"  {'op':<20}" + "".join(f"{'d' + str(d):>9}" for d in LATE))
    for k in kinds:
        row = [ops_by_day[d].get(k, 0) / max(1, seats_by_day[d]) for d in LATE]
        if any(v > 0.05 for v in row):
            print(f"  {k:<20}" + "".join(f"{v:>9.2f}" for v in row))
    print()
    print("WHAT IS STANDING ON HIS BOARD AT d27, BY HOW MANY SHEEP THE SEAT LOSES")
    print(f"  {'lost':>5}{'seats':>7}   crop units held (mean per seat)")
    for lost in sorted(standing):
        n = seats_by_lost[lost] or 1
        items = sorted(((k, v) for k, v in standing[lost].items() if not k.endswith("_tiles")),
                       key=lambda kv: -kv[1])
        s = "  ".join(f"{k} {v / n:.1f}" for k, v in items[:6])
        print(f"  {lost:>5}{seats_by_lost[lost]:>7}   {s}")


if __name__ == "__main__":
    main()
