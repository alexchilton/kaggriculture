"""SpaTaro's 179 seasons as planner-format schedule rows.

The fields are exactly the ones `kagg/search/schedule_agent.py` reads off a plan row --
`plants` `places` `builds` `land` `hires` `hands` `feeds` `cares` `seeds` `buys` `sells`
`animals_bought` -- plus `money_dawn` and the raw timed `orders` for the market layer.
`plant_tiles` / `build_tiles` are deliberately absent: they are in `breakdown.TAPE_ONLY`,
the planner never reads them, and the walk is what the planner exists to re-derive.

`places` is the list of ANIMAL species placed that day. `PLACE` in the engine
(`reference/kaggriculture.py:377`) is overloaded -- the same op drops produce in the shed when
the unit is shed-adjacent -- so counting every PLACE counts loading trips as herd placements.

One submission only (56114097). Mixing submissions is what made the 62-season set useless.
"""
import argparse, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEASON, TPD = 30, 24
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
PRODUCTS = CROPS + ("MILK", "WOOL", "EGG", "FERTILIZER")
ANIMALS = ("COW", "SHEEP", "GOOSE")
BUYABLE = ("WHEAT", "FERTILIZER")
TEAM = "SpaTaro"


def plan_rows(steps, seat):
    rows = {d: dict(plants=[], places=[], builds=0, land=0, hires=0, hands=0,
                    feeds=0, cares=0, seeds=Counter(), buys=Counter(),
                    sells=Counter(), animals_bought=Counter(), orders=[],
                    money_dawn=None)
            for d in range(SEASON)}
    for i, s in enumerate(steps[1:], start=1):
        day, hour = min((i - 1) // TPD, SEASON - 1), (i - 1) % TPD
        r = rows[day]
        obs = s[seat].get("observation") or {}
        if hour == 0:
            farms = obs.get("farms") or []
            if len(farms) > seat:
                r["money_dawn"] = farms[seat].get("money")
        a = s[seat].get("action") or {}
        for c in [a.get("farmer") or []] + list(a.get("hands") or []):
            if not c:
                continue
            op = c[0]
            if op == "PLANT" and len(c) > 1 and c[1] in CROPS:
                r["plants"].append(c[1])
            elif op in ("BUILD_PASTURE", "BUILD_COOP"):
                r["builds"] += 1
            elif op == "PLACE" and len(c) > 1 and c[1] in ANIMALS:
                r["places"].append(c[1])
            elif op == "FEED":
                r["feeds"] += 1
            elif op == "CARE":
                r["cares"] += 1
        for o in (a.get("market") or []):
            if not o:
                continue
            q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
            r["orders"].append([hour] + list(o))
            if o[0] == "HIRE":
                r["hires"] += 1
            elif o[0] == "BUY_LAND":
                r["land"] += 1
            elif o[0] == "BUY_ANIMAL" and o[1] in ANIMALS:
                r["animals_bought"][o[1]] += q
            elif o[0] == "BUY_SEED" and o[1] in CROPS:
                r["seeds"][o[1]] += q
            elif o[0] == "BUY_PRODUCT" and o[1] in BUYABLE:
                r["buys"][o[1]] += q
            elif o[0] == "SELL" and o[1] in PRODUCTS:
                r["sells"][o[1]] += q
    for r in rows.values():
        # The planner reads `hands` as the day's hire target at hour 0 (schedule_agent.py:5284).
        # On every plan on disk `hands == hires`, so carry his hire count into both.
        r["hands"] = r["hires"]
        for k in ("seeds", "buys", "sells", "animals_bought"):
            r[k] = dict(r[k])
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--ids", default="/tmp/spa_new_ids.txt")
    ap.add_argument("--out", default="data/spataro_plan_rows.json")
    args = ap.parse_args()

    allow = None
    p = Path(args.ids)
    if p.exists():
        allow = {int(x) for x in p.read_text().split()}
        print(f"restricting to {len(allow)} episodes of one submission", flush=True)

    seasons, seen = [], set()
    for d in args.dirs:
        folder = ROOT / d
        if not folder.exists():
            continue
        for f in sorted(folder.glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            try:
                ep = int(f.stem)
            except ValueError:
                continue
            if ep in seen or (allow is not None and ep not in allow):
                continue
            r = json.loads(f.read_text())
            names = (r.get("info") or {}).get("TeamNames") or []
            if TEAM not in names:
                continue
            seen.add(ep)
            seat = names.index(TEAM)
            steps = r["steps"]
            shops, unlocks = [], []
            for i, s in enumerate(steps):
                town = (s[seat]["observation"].get("town") or {})
                for x in (town.get("unlocked_shops") or []):
                    if x not in shops:
                        shops.append(x)
                        unlocks.append([i // TPD, x])
            seasons.append({"ep": ep, "bank": r["rewards"][seat], "seat": seat,
                            "opponent": names[1 - seat] if len(names) == 2 else None,
                            "seed": (r.get("info") or {}).get("seed"),
                            "unlocks": unlocks, "rows": plan_rows(steps, seat)})
            if len(seasons) % 25 == 0:
                print(f"  {len(seasons)} seasons", flush=True)
    print(f"\n{len(seasons)} seasons of submission 56114097", flush=True)
    out = ROOT / args.out
    out.write_text(json.dumps(
        [{k: v for k, v in s.items() if k != "rows"} |
         {"rows": {str(d): s["rows"][d] for d in range(SEASON)}} for s in seasons],
        separators=(",", ":")))
    print(f"wrote {out} ({out.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
