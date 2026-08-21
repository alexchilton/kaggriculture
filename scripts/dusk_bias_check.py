"""Is `dusk` an artifact of reading the board BEFORE hour 23 acts?

`is_the_middle_capacity.py` counts empty tiles in the h23 observation, which is the board as it
stands BEFORE that turn's PLANT lands. If Kawashigi does most of his planting late in the day, that
count is overstated and the whole "he leaves the board half empty" result is a timing artifact.

Two quantities that cannot have that bias:

  min_free   the smallest free-tile count over ALL 24 hourly observations of the day. If the board
             is ever full, this is 0, whatever hour the last plant landed.
  plant_h    the hour distribution of his PLANT ops. If planting is spread through the day rather
             than piled at h23, the h23 read was never going to be far off.

    python -u scripts/dusk_bias_check.py
"""

import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

LO, HI = 14, 27
TURNS_PER_DAY = 24


def main():
    rows = json.loads((REPO / "data/target_rows_kawa_norm.json").read_text())
    seats = {(r["game"], r["seat"]) for r in rows}
    idx = {}
    for p in glob.glob(str(REPO / "data/seed_scripts/**/*.json"), recursive=True):
        idx.setdefault(pathlib.Path(p).stem, p)

    per_day, plant_h = collections.defaultdict(list), collections.Counter()
    for game, seat in sorted(seats):
        path = idx.get(game)
        if not path:
            continue
        rep = json.loads(pathlib.Path(path).read_text())
        acc = {}
        for step in rep.get("steps") or []:
            if seat >= len(step):
                continue
            cell = step[seat]
            obs = cell.get("observation") or {}
            day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)
            if not (LO <= day <= HI):
                continue
            farms = obs.get("farms") or []
            farm = farms[seat] if seat < len(farms) else {}
            free = sum(1 for r in farm.get("tiles") or [] for t in r if t is None)
            rec = acc.setdefault(day, {"min": 10 ** 9, "h23": None, "turns": 0})
            rec["min"] = min(rec["min"], free)
            if hour == TURNS_PER_DAY - 1:
                rec["h23"] = free
            act = cell.get("action")
            if act is None:
                continue
            rec["turns"] += 1
            for u in [act.get("farmer")] + list(act.get("hands") or []):
                if u and str(u[0]) == "PLANT":
                    plant_h[hour] += 1
        for d, r in acc.items():
            if r["turns"] == TURNS_PER_DAY and r["h23"] is not None:
                per_day[d].append(r)

    allr = [r for v in per_day.values() for r in v]
    n = len(allr)
    print("day-rows %d, d%d-d%d\n" % (n, LO, HI))
    print("%4s %6s %10s %10s %12s %12s" % ("day", "n", "min_free", "h23_free", "min==0", "min>=3"))
    for d in sorted(per_day):
        rs = per_day[d]
        k = len(rs)
        print("%4d %6d %10.2f %10.2f %11.1f%% %11.1f%%"
              % (d, k, sum(r["min"] for r in rs) / k, sum(r["h23"] for r in rs) / k,
                 100.0 * sum(1 for r in rs if r["min"] == 0) / k,
                 100.0 * sum(1 for r in rs if r["min"] >= 3) / k))
    print("\nPOOLED  mean min_free %.2f   mean h23_free %.2f"
          % (sum(r["min"] for r in allr) / n, sum(r["h23"] for r in allr) / n))
    print("  min_free == 0 (board full at SOME hour)  %.1f%%"
          % (100.0 * sum(1 for r in allr if r["min"] == 0) / n))
    print("  min_free >= 3                            %.1f%%"
          % (100.0 * sum(1 for r in allr if r["min"] >= 3) / n))

    tot = sum(plant_h.values())
    print("\nPLANT ops by hour, d%d-d%d, %d ops" % (LO, HI, tot))
    for h in sorted(plant_h):
        print("  h%-3d %6d %5.1f%%" % (h, plant_h[h], 100.0 * plant_h[h] / tot))


if __name__ == "__main__":
    main()
