"""His FULL pen layout, in build order, over every recorded season.

`PEN_SPOTS` in `schedule_agent.py` is ten tiles long. He builds a median of 19 pens and up to 35, so
from the eleventh on the siting falls through to `field_order` and the pens scatter into the crop
sweep -- which is how d7's second pasture ends up with no ground at dawn: every empty tile was
already claimed by a PLANT pin, `spot` came back None, and the pen was only sited at the NEXT turn,
by which time `_router_acts` had committed the day's tour and nothing walked to it.

Alex: "by d7 the plan for where the animals are located should be known ... the geometry should then
be fixed and saved somewhere, up to and including the sheep big ones", and "so there are no plants
put where the animals are gonna go".

So this reads the pen ground out of the replays in BUILD ORDER and reports, per slot, the modal tile
and how often he uses it. A slot whose share is high is geometry; a slot whose share is low is his
board reacting, and no constant should claim otherwise.
"""
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(ROOT))
from scripts.spataro_geometry import events, TEAM


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+",
                    default=["data/replays_spa_sub", "data/replays_2026-09-07",
                             "data/replays_2026-09-08", "data/replays_2026-09-09"])
    ap.add_argument("--ids", default="/tmp/spa_new_ids.txt")
    ap.add_argument("--out", default="data/spataro_pen_geometry.json")
    a = ap.parse_args()

    allow = None
    p = Path(a.ids)
    if p.exists():
        allow = {int(x) for x in p.read_text().split()}

    slots = defaultdict(Counter)      # build index -> tile -> seasons
    ever = Counter()                  # tile -> seasons in which it is ever a pen
    day_of = defaultdict(Counter)     # tile -> day it was built
    n, seen = 0, set()
    for d in a.dirs:
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
            seen.add(ep)
            blob = json.loads(f.read_text())
            names = list((blob.get("info") or {}).get("TeamNames") or [])
            seat = names.index(TEAM) if TEAM in names else 0
            ev = [e for e in events(blob["steps"], seat) if e[3] == "BUILD"]
            if not ev:
                continue
            n += 1
            for k, (day, x, y, _k, _w) in enumerate(ev):
                slots[k][(x, y)] += 1
                ever[(x, y)] += 1
                day_of[(x, y)][day] += 1

    print(f"{n} seasons\n")
    print(f"{'slot':>4} {'modal tile':>12} {'share':>7} {'seasons':>8}   runners-up")
    order = []
    for k in sorted(slots):
        c = slots[k]
        tot = sum(c.values())
        (tile, cnt), = c.most_common(1)
        rest = "  ".join(f"{t}:{v}" for t, v in c.most_common(4)[1:])
        print(f"{k:>4} {str(tile):>12} {cnt/tot:6.0%} {tot:>8}   {rest}")
        order.append([list(tile), round(cnt / tot, 3), tot])

    print(f"\ntiles that are EVER a pen, by how many of the {n} seasons use them:")
    for t, c in ever.most_common():
        med = sorted(day_of[t].elements())[len(list(day_of[t].elements())) // 2]
        print(f"  {str(t):>8} {c:4d} seasons {c/n:5.0%}   median build day {med}")

    Path(a.out).write_text(json.dumps(
        {"seasons": n,
         "slots": order,
         "ever": {f"{x},{y}": c for (x, y), c in ever.most_common()}}, indent=1))
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
