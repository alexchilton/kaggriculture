"""A census of the FIELD, read off our own ladder replays. What does everyone plant and sell, and when?

**Why this and not another tape comparison.** Matching Kawashigi harder converges on the field
median, and on 2026-08-16 a downloaded game showed Thomas Tschinkel reproducing his opening 24/24
for eight straight days. You cannot win an Elo ladder by playing the median. The edge is in the
dimensions where the field is HOMOGENEOUS, because those payoffs are contested and the value of
deviating rises with how many people share the convention.

Measured in miniature on d6: the same 12 wool, the same day, `[218,217,215,214,212,209]` at h04 and
`[199,198,197,196,195,194]` at h11. Not a better plan -- an earlier one, into a book nobody had
touched yet. If the whole field holds for the town drain and sells at h16, then h16 is the WORST
hour on the board and h14 is free money.

So this counts, over every opponent in the corpus:

    sell hour histogram, per product   where the book is crowded
    plant counts, per crop             which books are flooded and which are empty
    sell volume, per product           what everyone dumps

Read from the recorded ACTION STREAM of the opponents, not from our simulator, so nothing here can
be an artifact of our own harness. Sell ORDERS are counted, not fills -- an agent re-posts a quota
every turn, so the hour histogram is weighted by orders standing, which is exactly the crowding
this is trying to measure. Volumes are therefore upper bounds and are labelled as such.

    python -u scripts/what_the_field_does.py --dir data/seed_scripts/ladder_2026-08-16b
"""
import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
US = "alex chilton"
CROPS = ("WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO")
PRODUCTS = ("STRAWBERRY", "MILK", "MELON", "WHEAT", "WOOL", "FERTILIZER",
            "CARROT", "TOMATO", "EGG")


def census(folder, include_us=False):
    seen = set()
    plants = collections.Counter()
    sell_hour = collections.defaultdict(collections.Counter)
    sell_units = collections.Counter()
    first_sell_hour = collections.defaultdict(list)
    agents = collections.Counter()
    games = 0
    for p in sorted(glob.glob(str(REPO / folder / "*.json"))):
        try:
            raw = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        if not isinstance(raw, dict) or len(raw.get("steps") or []) < 700:
            continue
        info = raw.get("info") or {}
        names = info.get("TeamNames") or []
        ep = str(info.get("EpisodeId") or pathlib.Path(p).stem)
        if ep in seen:
            continue
        seen.add(ep)
        games += 1
        steps = raw["steps"]
        for seat, who in enumerate(names):
            if who == US and not include_us:
                continue
            agents[who] += 1
            per_day_first = {}
            for t in range(1, len(steps)):
                a = steps[t][seat].get("action")
                if not isinstance(a, dict):
                    continue
                d, h = divmod(t - 1, TPD)
                for u in [a.get("farmer")] + list(a.get("hands") or []):
                    if u and u[0] == "PLANT" and len(u) > 1:
                        plants[u[1]] += 1
                for o in (a.get("market") or []):
                    if o and o[0] == "SELL" and len(o) > 2:
                        sell_hour[o[1]][h] += 1
                        sell_units[o[1]] += int(o[2])
                        k = (d, o[1])
                        if k not in per_day_first:
                            per_day_first[k] = h
                            first_sell_hour[o[1]].append(h)
    return plants, sell_hour, sell_units, first_sell_hour, agents, games


def bar(n, top, width=34):
    return "#" * int(round(width * n / max(1, top)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/seed_scripts/ladder_2026-08-16b")
    ap.add_argument("--include-us", action="store_true")
    a = ap.parse_args()
    plants, sell_hour, sell_units, first, agents, games = census(a.dir, a.include_us)

    print(f"{games} games, {len(agents)} distinct opponents"
          f"{'' if not a.include_us else ' (ours included)'}\n")

    print("=== WHAT THE FIELD PLANTS (plant actions across every opponent)")
    tot = sum(plants.values()) or 1
    for c, n in plants.most_common():
        print(f"   {c:<12} {n:>7,}  {100 * n / tot:>5.1f}%  {bar(n, plants.most_common(1)[0][1])}")
    for c in CROPS:
        if c not in plants:
            print(f"   {c:<12} {0:>7}   0.0%   <- NOBODY GROWS THIS")

    print("\n=== FIRST SELL HOUR OF A DAY, per product (how crowded each hour is)")
    print(f"{'product':>12} {'orders':>8}  " + "".join(f"{h:>3}" for h in range(24)))
    for prod in PRODUCTS:
        hs = first.get(prod) or []
        if not hs:
            continue
        c = collections.Counter(hs)
        peak = c.most_common(1)[0]
        row = "".join(f"{c.get(h, 0) * 100 // max(1, len(hs)):>3}" for h in range(24))
        print(f"{prod:>12} {len(hs):>8,}  {row}   peak h{peak[0]} "
              f"({100 * peak[1] // len(hs)}%)")
    print("   (each cell is the % of that product's day-first sells landing on that hour)")

    print("\n=== SELL VOLUME ORDERED, per product (upper bound: orders, not fills)")
    tot = sum(sell_units.values()) or 1
    for p, n in sell_units.most_common():
        print(f"   {p:<12} {n:>9,}  {100 * n / tot:>5.1f}%")
    for p in PRODUCTS:
        if p not in sell_units:
            print(f"   {p:<12} {0:>9}   0.0%   <- NOBODY SELLS THIS")

    print("\n=== the ten most frequent opponents")
    for who, n in agents.most_common(10):
        print(f"   {who:<34} {n:>3} games")


if __name__ == "__main__":
    main()
