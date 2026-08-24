"""We match カワシギ exactly on some towns and break at d5/d8/d9 on others. What differs?

Alex, 2026-08-24: *"if it doesn't match then it means there is an extra condition or tape or an
error in our logic."*

`scripts/the_grid_vs_his_grid.py` gives the first day our board differs from his, playing our agent
in his seat on each game's OWN seed -- so the town, the shop draw and the opponent are that game's
real ones. That run splits his games into groups by first-divergence day.

This lines the groups up against what the agent can actually SEE early, to find the condition it is
reading wrong:

    shops d3/d5    which shops the town had unlocked on the two days his branches are known to
                   read (`project_kaggriculture_leader_replans_on_shops`: a fixed opening ending
                   at the d3 first unlock; `project_kaggriculture_only_two_bits_vary`: melon
                   count >= 9 at d3 and the yarn store at d5)
    melon d3       tiles of MELON standing at d3 -- the other known branch
    quadrants      how much land is unlocked, which changes what a route can reach

Reads the first-divergence days from the grid log rather than recomputing them, so this is cheap
and cannot disagree with the run it is explaining.
"""

import argparse
import collections
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "reference"))

TPD = 24
LINE = re.compile(r"^\s*(\d+)\s+first differs d(\d+|-)\s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default="data/logs/grid_all_kawa.log")
    ap.add_argument("--who", default="カワシギ")
    a = ap.parse_args()

    import kaggriculture as KG

    first = {}
    for line in (REPO / a.log).read_text().splitlines():
        m = LINE.match(line)
        if m:
            first[m.group(1)] = int(m.group(2)) if m.group(2) != "-" else None

    import glob
    files = {}
    for d in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
              "leaders_2026-08-24", "kawa_2026-08-24", "losses", "top_guys", "top2",
              "field_leaders", "new_leader", "ladder", "our_games"):
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)
    for f in glob.glob("/Users/alexchilton/Downloads/*.json"):
        files.setdefault(pathlib.Path(f).stem, f)

    rows = []
    for ep, day in sorted(first.items(), key=lambda kv: (kv[1] is None, kv[1])):
        f = files.get(ep)
        if f is None:
            continue
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        steps = rec["steps"]

        def at(d):
            return steps[min(d * TPD, len(steps) - 1)][seat]["observation"]

        def shops(d):
            return sorted((at(d).get("town") or {}).get("unlocked_shops") or [])

        def melon(d):
            farm = at(d)["farms"][seat]
            return sum(1 for row in (farm.get("tiles") or []) for t in row
                       if isinstance(t, dict) and t.get("crop") == "MELON")

        s3, s5 = shops(3), shops(5)
        rows.append({
            "ep": ep, "day": day, "seed": (rec.get("info") or {}).get("seed"),
            "s3": s3, "s5": s5, "melon3": melon(3), "melon5": melon(5),
            "yarn5": any("YARN" in x or "KNIT" in x or "WOOL" in (KG.SHOPS.get(x) or [])
                         for x in s5),
            "quad": len(at(5)["farms"][seat].get("unlocked_quadrants") or []) or None,
        })

    print(f"{len(rows)} games. grouped by the day our board first differs from his.\n")
    print(f"{'first':>5} {'episode':>10} {'melon d3':>9} {'yarn d5':>8} {'quad':>5}  shops at d5")
    for r in rows:
        print(f"d{str(r['day']):<4} {r['ep']:>10} {r['melon3']:>9} "
              f"{str(r['yarn5']):>8} {str(r['quad']):>5}  {', '.join(r['s5'])[:70]}")

    print("\nDOES ANY EARLY-VISIBLE FACT SEPARATE THE GROUPS?\n")
    by = collections.defaultdict(list)
    for r in rows:
        by[r["day"]].append(r)
    for day in sorted(by, key=lambda d: (d is None, d)):
        g = by[day]
        m3 = collections.Counter(r["melon3"] for r in g)
        yarn = collections.Counter(r["yarn5"] for r in g)
        nshop = collections.Counter(len(r["s5"]) for r in g)
        shopset = collections.Counter()
        for r in g:
            for s in r["s5"]:
                shopset[s] += 1
        print(f"  first differs d{day}  n={len(g)}")
        print(f"      melon at d3 : {dict(m3)}")
        print(f"      yarn at d5  : {dict(yarn)}")
        print(f"      #shops d5   : {dict(nshop)}")
        print(f"      shops seen  : "
              + ", ".join(f"{k} {v}/{len(g)}" for k, v in shopset.most_common(8)))
        print()


if __name__ == "__main__":
    main()
