"""SpaTaro's seasons as SCHEDULES, and how many distinct plans that leaves.

Counting a tape per day IS the de-jittering that works. Comparing 24-turn action blocks
fails -- all 62 were distinct on every day even after dropping malformed orders, quantities,
hand identity and movement (`scripts/dejitter_blocks.py`). A day collapsed to counts throws
away exactly the noise (which tile, which hand, what order within the turn, the decoy
`BUY_PRODUCT` of produce the engine never sells) and keeps the plan. The planner re-derives
the walk, which was never the plan.

So this is the test his "couple of base tapes" deserves, at the right granularity: how many
distinct schedules do his seasons collapse to?

Reads only submission 56114097 (his current agent, the 224 episodes in
`data/replays_spa_sub` plus whatever of them is already in the daily dumps). Mixing
submissions is what made the earlier 62-season set useless.
"""
import argparse, json, statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEASON, TPD = 30, 24
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
PRODUCTS = CROPS + ("MILK", "WOOL", "EGG", "FERTILIZER")
ANIMALS = ("COW", "SHEEP", "GOOSE")
BUYABLE = ("WHEAT", "FERTILIZER")
TEAM = "SpaTaro"


def row_counts(steps, seat):
    per = {d: dict(plants=Counter(), animals_bought=Counter(), hires=0, land=0,
                   seeds=Counter(), buys=Counter(), sells=Counter(), builds=0, places=0)
           for d in range(SEASON)}
    for i, s in enumerate(steps[1:], start=1):
        r = per[min((i - 1) // TPD, SEASON - 1)]
        a = s[seat].get("action") or {}
        for c in [a.get("farmer") or []] + list(a.get("hands") or []):
            if not c:
                continue
            if c[0] == "PLANT" and len(c) > 1:
                r["plants"][c[1]] += 1
            elif c[0] in ("BUILD_PASTURE", "BUILD_COOP"):
                r["builds"] += 1
            elif c[0] == "PLACE":
                r["places"] += 1
        for o in (a.get("market") or []):
            if not o:
                continue
            q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
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
    return per


def signature(per, upto, fields):
    """A day-range as a hashable plan: only the named count fields, no tiles, no hands."""
    out = []
    for d in range(upto):
        r = per[d]
        out.append(tuple(
            (f, tuple(sorted(r[f].items())) if isinstance(r[f], Counter) else r[f])
            for f in fields))
    return tuple(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--ids", default="/tmp/spa_new_ids.txt",
                    help="episode ids belonging to the one submission")
    ap.add_argument("--out", default="data/spataro_schedules.json")
    args = ap.parse_args()

    allow = None
    p = Path(args.ids)
    if p.exists():
        allow = {int(x) for x in p.read_text().split()}
        print(f"restricting to {len(allow)} episodes of one submission")

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
            names = r.get("info", {}).get("TeamNames") or []
            if TEAM not in names:
                continue
            seen.add(ep)
            seat = names.index(TEAM)
            steps = r["steps"]
            shops, unlocks = [], []
            for i, s in enumerate(steps):
                for x in ((s[seat]["observation"].get("town") or {}).get("unlocked_shops") or []):
                    if x not in shops:
                        shops.append(x)
                        unlocks.append([i // TPD, x])
            seasons.append({"ep": ep, "bank": r["rewards"][seat], "seat": seat,
                            "seed": r["info"].get("seed"), "unlocks": unlocks,
                            "rows": row_counts(steps, seat)})
            if len(seasons) % 25 == 0:
                print(f"  {len(seasons)} seasons", flush=True)
    print(f"\n{len(seasons)} seasons of submission 56114097\n")
    if not seasons:
        return

    FIELDSETS = {
        "full plan": ("plants", "animals_bought", "hires", "land", "seeds", "buys", "sells"),
        "field only": ("plants", "animals_bought", "land", "hires"),
        "herd + land": ("animals_bought", "land"),
        "plants only": ("plants",),
    }
    print(f"{'days':>5}  " + "  ".join(f"{k:>12}" for k in FIELDSETS))
    for upto in (1, 3, 5, 7, 9, 12, 30):
        cells = []
        for fields in FIELDSETS.values():
            c = Counter(signature(s["rows"], upto, fields) for s in seasons)
            cells.append(f"{len(c):>4} ({max(c.values()):>3})")
        print(f"{upto:>5}  " + "  ".join(f"{c:>12}" for c in cells))
    print("\n(distinct schedules, and the largest group, over "
          f"{len(seasons)} seasons)")

    out = ROOT / args.out
    out.write_text(json.dumps(
        [{"ep": s["ep"], "bank": s["bank"], "seed": s["seed"], "unlocks": s["unlocks"],
          "rows": {str(d): {k: (dict(v) if isinstance(v, Counter) else v)
                            for k, v in s["rows"][d].items()} for d in range(SEASON)}}
         for s in seasons], separators=(",", ":")))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
