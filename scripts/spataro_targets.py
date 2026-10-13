"""SpaTaro's board, per day, as targets a planner can be asked to hit.

Not a tape. His 62 openings reach 37 distinct states at turn 168 and share almost
no turns, so there is nothing to replay. What IS stable is the board he arrives at:
animals by species, crops by type, land, hires.

Keyed on the one latch that measured real signal -- a YARN_STORE in the first two
shops (peak sheep p50 10 with, 2 without). Quartiles are the tolerance: a planner
that lands inside them is playing his shape.

    .venv-sub/bin/python -u scripts/spataro_targets.py
"""
import json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"]
CROPS = ("MELON", "WHEAT", "STRAWBERRY", "CARROT", "TOMATO")
OUT = ROOT / "data" / "spataro_targets.json"


def board(obs, seat):
    f = obs["farms"][seat]
    c, a, free, struct = defaultdict(int), defaultdict(int), 0, 0
    for row in f["tiles"]:
        for t in row:
            if t is None:
                free += 1
            elif isinstance(t, dict):
                if t.get("animal"):
                    a[t["animal"]] += 1
                elif t.get("kind") == "PLANT" and t.get("crop"):
                    c[t["crop"]] += 1
                elif t.get("kind") in ("PASTURE", "COOP"):
                    struct += 1
    return {**{f"crop_{k}": c[k] for k in CROPS},
            **{f"animal_{k}": a[k] for k in ("COW", "SHEEP", "GOOSE")},
            "planted": sum(c.values()), "free": free, "empty_struct": struct,
            "quads": len(f["unlocked_quadrants"]), "money": f["money"]}


def main():
    seasons = []
    for d in DIRS:
        for f in sorted((ROOT/d).glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            r = json.loads(f.read_text())
            if "SpaTaro" not in r["info"]["TeamNames"]:
                continue
            seat = r["info"]["TeamNames"].index("SpaTaro")
            st = r["steps"]
            shops = []
            for s in st:
                for x in ((s[0]["observation"].get("town") or {}).get("unlocked_shops") or []):
                    if x not in shops:
                        shops.append(x)
                if len(shops) >= 2:
                    break
            seasons.append({"yarn": "YARN_STORE" in shops[:2],
                            "days": {day: board(st[day*24][seat]["observation"], seat)
                                     for day in range(0, 30) if day*24 < len(st)}})
    print(f"{len(seasons)} seasons: "
          f"{sum(1 for s in seasons if s['yarn'])} yarn, {sum(1 for s in seasons if not s['yarn'])} non-yarn\n")

    table = {}
    for yarn in (True, False):
        g = [s for s in seasons if s["yarn"] == yarn]
        lab = "yarn" if yarn else "non_yarn"
        table[lab] = {}
        keys = ["animal_COW", "animal_SHEEP", "crop_MELON", "crop_WHEAT",
                "crop_STRAWBERRY", "crop_CARROT", "planted", "quads"]
        print(f"=== {lab}  (n={len(g)})")
        print("day " + " ".join(f"{k.replace('animal_','').replace('crop_',''):>12}" for k in keys))
        for day in range(0, 30):
            vals = [s["days"][day] for s in g if day in s["days"]]
            if not vals:
                continue
            row = {}
            cells = []
            for k in keys:
                v = sorted(x[k] for x in vals)
                q1, med, q3 = v[len(v)//4], v[len(v)//2], v[(3*len(v))//4]
                row[k] = {"q1": q1, "median": med, "q3": q3}
                cells.append(f"{med:>4} [{q1:>2}-{q3:>2}]".rjust(12))
            table[lab][day] = row
            print(f"{day:>3} " + " ".join(cells))
        print()
    OUT.write_text(json.dumps(table, indent=1))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
