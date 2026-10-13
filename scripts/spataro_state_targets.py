"""SpaTaro's BOARD at dawn, per day, over 179 seasons of submission 56114097.

The flows (`scripts/spataro_plan_rows.py`) say what he did. This says what he HAD, which is the
thing to match: the first effort is to reach his day-12 board, not his bank. A plan that buys the
same animals on different days and arrives at the same herd has matched him; a plan that copies his
purchase dates and arrives somewhere else has not. §9 of the architecture doc measured exactly that
-- `animals_bought` is 70 distinct plans by day 5 while the placement sequence is 10.

Per day, at hour 0: money, owned tiles, planted tiles and their crop mix, animals on the board by
species, EMPTY structures (a pen whose animal starved -- the cull's footprint, since `DIG` cannot
remove a placed animal and `consecutive_unfed >= 2` is the only herd exit,
`reference/kaggriculture.py:817`), crew size, shed contents, and which shops are open.
"""
import argparse, json, statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEASON, TPD = 30, 24
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
ANIMALS = ("COW", "SHEEP", "GOOSE")
STRUCT = {"PASTURE": "COW/SHEEP", "COOP": "GOOSE"}
TEAM = "SpaTaro"


def board(obs, seat):
    farms = obs.get("farms") or []
    if len(farms) <= seat:
        return None
    farm = farms[seat]
    owned = planted = empty_struct = weeds = 0
    crops, animals = Counter(), Counter()
    for row in (farm.get("tiles") or []):
        for t in row:
            if t == "LOCKED":
                continue
            owned += 1
            if not isinstance(t, dict):
                continue
            if "animal" in t:
                animals[t["animal"]] += 1
            elif t.get("kind") in STRUCT:
                empty_struct += 1
            elif t.get("crop"):
                planted += 1
                crops[t["crop"]] += 1
                if t.get("crop") == "WEED":
                    weeds += 1
    town = obs.get("town") or {}
    return {"money": farm.get("money"), "owned": owned, "planted": planted,
            "crops": dict(crops), "animals": dict(animals), "empty_struct": empty_struct,
            "hands": len(farm.get("hands") or []), "weeds": weeds,
            "shops": list(town.get("unlocked_shops") or [])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--ids", default="/tmp/spa_new_ids.txt")
    ap.add_argument("--out", default="data/spataro_state.json")
    ap.add_argument("--days", nargs="+", type=int, default=[3, 6, 9, 12, 15, 20, 25, 29])
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
            days = {}
            for day in range(SEASON):
                i = day * TPD
                if i < len(steps):
                    b = board(steps[i][seat].get("observation") or {}, seat)
                    if b:
                        days[str(day)] = b
            seasons.append({"ep": ep, "bank": r["rewards"][seat], "seed": (r.get("info") or {}).get("seed"),
                            "state": days})
            if len(seasons) % 25 == 0:
                print(f"  {len(seasons)} seasons", flush=True)

    print(f"\n{len(seasons)} seasons of submission 56114097\n", flush=True)
    out = ROOT / args.out
    out.write_text(json.dumps(seasons, separators=(",", ":")))

    def q(vals):
        vals = sorted(vals)
        n = len(vals)
        return vals[n // 4], statistics.median(vals), vals[(3 * n) // 4]

    for day in args.days:
        rows = [s["state"][str(day)] for s in seasons if str(day) in s["state"]]
        if not rows:
            continue
        print(f"--- dawn of day {day}   ({len(rows)} seasons)")
        for key in ("money", "owned", "planted", "animals_total", "empty_struct", "hands"):
            vals = [sum(r["animals"].values()) if key == "animals_total" else r[key] for r in rows]
            a, m, b = q(vals)
            print(f"    {key:14} p25 {a:>9,.0f}  p50 {m:>9,.0f}  p75 {b:>9,.0f}")
        for species in ANIMALS:
            vals = [r["animals"].get(species, 0) for r in rows]
            if max(vals):
                a, m, b = q(vals)
                print(f"    {species:14} p25 {a:>9,.0f}  p50 {m:>9,.0f}  p75 {b:>9,.0f}")
        for crop in CROPS:
            vals = [r["crops"].get(crop, 0) for r in rows]
            if max(vals):
                a, m, b = q(vals)
                print(f"    {crop:14} p25 {a:>9,.0f}  p50 {m:>9,.0f}  p75 {b:>9,.0f}")
        print()
    print(f"wrote {out} ({out.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
