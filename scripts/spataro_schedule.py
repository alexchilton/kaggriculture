"""SpaTaro's per-day flows, rendered as a schedule our planner accepts.

His turns cannot be copied -- 37 distinct openings reaching 37 distinct states. But
`schedule_agent` takes "counts per day, no tile coordinates", which is exactly the
level at which he IS consistent. So the flows are lifted instead of the turns, and
the planner is left to find the walk.

One schedule per latch: a YARN_STORE in the first two shops or not. Values are the
median over his seasons in that branch, so the schedule is his typical game rather
than any single one of them.

    .venv-sub/bin/python -u scripts/spataro_schedule.py
    -> data/spataro_schedule_yarn.json, data/spataro_schedule_non_yarn.json
"""
import json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"]
SEASON, TPD = 30, 24
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
PRODUCTS = CROPS + ("MILK", "WOOL", "EGG", "FERTILIZER")
ANIMALS = ("COW", "SHEEP", "GOOSE")


def flows(steps, seat):
    """Per-day counts of what the agent ORDERED and PLANTED."""
    per = {d: dict(plants=[], animals_bought={}, hires=0, land=0,
                   seeds={}, buys={}, sells={}, places=[], builds=0)
           for d in range(SEASON)}
    for i, s in enumerate(steps[1:], start=1):
        day = min((i - 1) // TPD, SEASON - 1)
        a = s[seat].get("action") or {}
        r = per[day]
        for c in [a.get("farmer") or []] + list(a.get("hands") or []):
            if not c:
                continue
            if c[0] == "PLANT" and len(c) > 1:
                r["plants"].append(c[1])
            elif c[0] in ("BUILD_PASTURE", "BUILD_COOP"):
                r["builds"] += 1
            elif c[0] == "PLACE":
                r["places"].append(c[1] if len(c) > 1 else None)
        for o in (a.get("market") or []):
            if not o:
                continue
            q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
            if o[0] == "HIRE":
                r["hires"] += 1
            elif o[0] == "BUY_LAND":
                r["land"] += 1
            elif o[0] == "BUY_ANIMAL" and o[1] in ANIMALS:
                r["animals_bought"][o[1]] = r["animals_bought"].get(o[1], 0) + q
            elif o[0] == "BUY_SEED" and o[1] in CROPS:
                r["seeds"][o[1]] = r["seeds"].get(o[1], 0) + q
            elif o[0] == "BUY_PRODUCT" and o[1] in ("WHEAT", "FERTILIZER"):
                r["buys"][o[1]] = r["buys"].get(o[1], 0) + q
            elif o[0] == "SELL" and o[1] in PRODUCTS:
                r["sells"][o[1]] = r["sells"].get(o[1], 0) + q
    return per


def main():
    branch = defaultdict(list)
    for d in DIRS:
        for f in sorted((ROOT/d).glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            r = json.loads(f.read_text())
            if "SpaTaro" not in r["info"]["TeamNames"]:
                continue
            seat = r["info"]["TeamNames"].index("SpaTaro")
            shops = []
            for s in r["steps"]:
                for x in ((s[0]["observation"].get("town") or {}).get("unlocked_shops") or []):
                    if x not in shops:
                        shops.append(x)
                if len(shops) >= 2:
                    break
            branch["yarn" if "YARN_STORE" in shops[:2] else "non_yarn"].append(flows(r["steps"], seat))
            # hands: the crew actually present, read off the board at dawn
            per = branch["yarn" if "YARN_STORE" in shops[:2] else "non_yarn"][-1]
            for day in range(SEASON):
                k = day*TPD + 12           # midday, after the day's hires have landed
                if k < len(r["steps"]):
                    per[day]["hands"] = len(r["steps"][k][seat]["observation"]["farms"][seat]["hands"])

    def med(vals):
        return int(round(statistics.median(vals))) if vals else 0

    for lab, seasons in branch.items():
        rows = {}
        for day in range(SEASON):
            rs = [s[day] for s in seasons]
            plants = {}
            for c in CROPS:
                n = med([sum(1 for x in r["plants"] if x == c) for r in rs])
                if n:
                    plants[c] = n
            row = dict(
                plants=[c for c, n in plants.items() for _ in range(n)],
                animals_bought={a: n for a in ANIMALS
                                if (n := med([r["animals_bought"].get(a, 0) for r in rs]))},
                builds=med([r["builds"] for r in rs]),
                places=[], hires=med([r["hires"] for r in rs]),
                hands=med([r.get("hands", 0) for r in rs]),
                land=med([r["land"] for r in rs]),
                seeds={c: n for c in CROPS if (n := med([r["seeds"].get(c, 0) for r in rs]))},
                buys={p: n for p in ("WHEAT", "FERTILIZER")
                      if (n := med([r["buys"].get(p, 0) for r in rs]))},
                sells={p: n for p in PRODUCTS if (n := med([r["sells"].get(p, 0) for r in rs]))},
                money_dawn=None, plant_tiles=[], build_tiles=[], land_turns=[], orders=[])
            rows[str(day)] = row
        out = ROOT / f"data/spataro_schedule_{lab}.json"
        out.write_text(json.dumps(rows, indent=1))
        print(f"{lab}: n={len(seasons)} seasons -> {out}")
        print(f"{'day':>3} {'hands':>5} {'hires':>5} {'land':>4} {'animals':>18} "
              f"{'plants':>26} {'buys WHEAT':>10}")
        for day in range(12):
            r = rows[str(day)]
            pl = ",".join(f"{c}x{r['plants'].count(c)}" for c in dict.fromkeys(r["plants"]))
            print(f"{day:>3} {r['hands']:>5} {r['hires']:>5} {r['land']:>4} "
                  f"{str(r['animals_bought']):>18} {pl:>26} {r['buys'].get('WHEAT',0):>10}")
        print()


if __name__ == "__main__":
    main()
