"""How many classes would a per-day decision tree have to choose between?

Alex, 2026-08-21: "so is it possible to use a dt on the tetsuya and ryo?? with similar logic or not?"

A tree can only learn a day whose label repeats. The label here is what is left of a target row once
everything the executor generates itself is removed -- `sells`/`buys` (h16 cadence after the land
buy), `places`/`animals_bought` (the herd algorithm reads the live shop draw), `seeds` (buy what you
are about to plant), and the six fields the executor never reads at all. What remains is the crop
multiset.

Three columns, and they answer different questions:

  multiset   distinct crop multisets -- the classes a tree must pick between
  top        share of seats holding the modal multiset -- the majority baseline a tree must BEAT
  cover90    how many classes are needed to cover 90% of seats -- the size of a useful library

A day with `top` near 100% needs no tree: play the modal row. A day with 60 classes and top at 2%
cannot be learned as a class at all, whatever the features.

    python -u scripts/class_counts_per_day.py \\
        kawa=data/target_rows_kawa_norm.json tets=data/target_rows_tets.json
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def per_day(path):
    rows = json.loads(pathlib.Path(path).read_text())
    by_day = collections.defaultdict(collections.Counter)
    for r in rows:
        by_day[r["day"]][tuple(sorted(r["target"].get("plants") or []))] += 1
    return by_day


def main():
    args = [a for a in sys.argv[1:] if "=" in a]
    if not args:
        raise SystemExit(__doc__)
    players = [(a.split("=", 1)[0], per_day(a.split("=", 1)[1])) for a in args]

    hdr = "%4s" % "day"
    for name, _ in players:
        hdr += "  | %-8s %6s %7s" % (name[:8], "top", "cov90")
    print(hdr)
    print("-" * len(hdr))
    for day in range(30):
        line = "%4d" % day
        for _name, bd in players:
            c = bd.get(day)
            if not c:
                line += "  | %8s %6s %7s" % ("-", "-", "-")
                continue
            n = sum(c.values())
            run = need = 0
            for _k, v in c.most_common():
                run += v
                need += 1
                if run >= 0.9 * n:
                    break
            line += "  | %8d %5.0f%% %7d" % (len(c), 100.0 * c.most_common(1)[0][1] / n, need)
        print(line)


if __name__ == "__main__":
    main()
