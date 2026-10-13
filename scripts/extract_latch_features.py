"""Features SpaTaro could have latched on, and the plan variants to explain.

Features are only things observable to it BEFORE the plan shows up in the ground:
the shop draw and its unlock day, its own and the opponent's cash, what the
opponent has already sold, the market book, and the seat.

Targets are realised state, because offers are over-requests (see the August
teardown in docs/history/the_field.md).

If nothing here explains the variation, the variation is internal -- which is what
a wall-clock-bounded solve at turn 0 would produce.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"]
TEAM = "SpaTaro"
PRODUCTS = ("WHEAT", "MELON", "STRAWBERRY", "CARROT", "MILK", "WOOL", "EGG", "FERTILIZER")


def tiles_of(obs, seat):
    crops, animals = {}, {}
    for row in obs["farms"][seat]["tiles"]:
        for t in row:
            if isinstance(t, dict):
                if t.get("kind") == "PLANT" and t.get("crop"):
                    crops[t["crop"]] = crops.get(t["crop"], 0) + 1
                elif t.get("animal"):
                    animals[t["animal"]] = animals.get(t["animal"], 0) + 1
    return crops, animals


def main():
    rows = []
    for d in DIRS:
        for f in sorted((ROOT/d).glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            r = json.loads(f.read_text())
            names = r["info"]["TeamNames"]
            if TEAM not in names:
                continue
            seat = names.index(TEAM); opp = 1 - seat
            steps = r["steps"]

            shops_at, first_unlock_day = [], None
            for i, s in enumerate(steps):
                u = (s[0]["observation"].get("town") or {}).get("unlocked_shops") or []
                if u and first_unlock_day is None:
                    first_unlock_day = i // 24
                for x in u:
                    if x not in shops_at:
                        shops_at.append(x)
                if len(shops_at) >= 2 and i >= 72:
                    break

            def at(step):
                return steps[step] if step < len(steps) else steps[-1]

            o3 = at(72)[seat]["observation"]
            opp3 = at(72)[opp]["observation"]
            o1 = at(24)[seat]["observation"]
            sold_by_opp = 0
            for s in steps[:73]:
                a = s[opp].get("action") or {}
                for o in (a.get("market") or []):
                    if o and o[0] == "SELL":
                        sold_by_opp += o[2] if len(o) > 2 and isinstance(o[2], int) else 1

            c5, a5 = tiles_of(at(120)[seat]["observation"], seat)
            c10, a10 = tiles_of(at(240)[seat]["observation"], seat)

            feat = {"world_a": shops_at[0] if shops_at else "NONE",
                    "world_b": shops_at[1] if len(shops_at) > 1 else "NONE",
                    "first_unlock_day": first_unlock_day if first_unlock_day is not None else -1,
                    "seat": seat,
                    "own_money_d1": o1["farms"][seat]["money"],
                    "own_money_d3": o3["farms"][seat]["money"],
                    "opp_money_d3": opp3["farms"][opp]["money"],
                    "opp_sold_by_d3": sold_by_opp}
            for p in PRODUCTS:
                feat[f"inv_{p}_d1"] = o1["market"]["inventory"].get(p, 0)
                feat[f"inv_{p}_d3"] = o3["market"]["inventory"].get(p, 0)
                feat[f"price_{p}_d3"] = o3["market"]["prices"].get(p, 0)

            rows.append({"episode": r["info"]["EpisodeId"], "features": feat,
                         "targets": {
                             "d5_MELON": c5.get("MELON", 0),
                             "d5_STRAWBERRY": c5.get("STRAWBERRY", 0),
                             "d5_WHEAT": c5.get("WHEAT", 0),
                             "d5_planted": sum(c5.values()),
                             "d5_COW": a5.get("COW", 0),
                             "d5_SHEEP": a5.get("SHEEP", 0),
                             "d10_COW": a10.get("COW", 0),
                             "d10_SHEEP": a10.get("SHEEP", 0),
                             "d10_WHEAT": c10.get("WHEAT", 0),
                             "d10_STRAWBERRY": c10.get("STRAWBERRY", 0),
                             "bank": r["rewards"][seat]}})
            print(f"  ep{r['info']['EpisodeId']} seat{seat} world={feat['world_a']}|{feat['world_b']}", flush=True)

    out = ROOT/"data/logs/spataro_latch_rows.json"
    out.write_text(json.dumps(rows, indent=1))
    print(f"\nwrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
