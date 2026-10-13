"""What a team actually BUILT, not what it asked for.

Submitted orders are offers. Our own August teardown of the then-leader recorded
"his day-0 SELL orders are speculative over-requests against an empty shed and
mostly no-op", so offer counts say little. The observations carry the realised
state: money, which tiles hold which crop, which hold which animal, how many hands.

If a team runs a small number of base plans behind decorative order traffic, the
realised farm at a day boundary will repeat. If it solves a fresh plan per game,
it will not.
"""
import argparse, json, statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"]
DAYS = [5, 10, 15, 20, 25, 29]


def snapshot(obs, seat):
    farm = obs["farms"][seat]
    crops, animals, planted = Counter(), Counter(), 0
    unlocked = 0
    for row in farm["tiles"]:
        for t in row:
            if t is None or t == "LOCKED":
                continue
            unlocked += 1
            if isinstance(t, dict):
                if t.get("kind") == "PLANT" and t.get("crop"):
                    crops[t["crop"]] += 1; planted += 1
                elif t.get("animal"):
                    animals[t["animal"]] += 1
    return {"money": farm["money"], "hands": len(farm["hands"]),
            "quads": "".join(sorted(farm["unlocked_quadrants"])),
            "tiles": unlocked, "planted": planted,
            "crops": dict(sorted(crops.items())), "animals": dict(sorted(animals.items()))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="SpaTaro")
    args = ap.parse_args()

    seasons = []
    for d in DIRS:
        for f in sorted((ROOT/d).glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            r = json.loads(f.read_text())
            names = r["info"]["TeamNames"]
            if args.team not in names:
                continue
            seat = names.index(args.team)
            snaps = {}
            for day in DAYS:
                step = day*24
                if step < len(r["steps"]):
                    snaps[day] = snapshot(r["steps"][step][seat]["observation"], seat)
            seasons.append({"ep": r["info"]["EpisodeId"], "seat": seat,
                            "bank": r["rewards"][seat], "snaps": snaps})
            print(f"  read ep{r['info']['EpisodeId']} seat{seat}", flush=True)
    print(f"\n{args.team}: {len(seasons)} seasons with full replays\n")
    if not seasons:
        return

    for day in DAYS:
        s = [x["snaps"][day] for x in seasons if day in x["snaps"]]
        if not s:
            continue
        print(f"--- day {day}  ({len(s)} seasons)")
        for key in ("money", "hands", "tiles", "planted"):
            v = sorted(x[key] for x in s)
            print(f"    {key:8} min {v[0]:>9,.0f}  p50 {v[len(v)//2]:>9,.0f}  "
                  f"max {v[-1]:>9,.0f}   distinct {len(set(v))}")
        for key in ("quads", "crops", "animals"):
            c = Counter(json.dumps(x[key], sort_keys=True) for x in s)
            top = c.most_common(3)
            print(f"    {key:8} {len(c)} distinct; most common "
                  f"{top[0][1]}/{len(s)}: {top[0][0][:90]}")
            for val, n in top[1:]:
                print(f"             {n}/{len(s)}: {val[:90]}")
        print()


if __name__ == "__main__":
    main()
