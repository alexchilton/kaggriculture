"""Is a player's mid-season a single crop with a varying count, or a real crop mix?

Alex, 2026-08-21: "ok and do we have the ryo and tets enough to see the similar algo".

Measured on カワシギ (228 seats), the mid-season is not a plan at all. Days 14, 16, 18, 20 and 27 are
100% WHEAT and the only thing that differs between seasons is HOW MANY -- a contiguous unimodal run
of counts, which is the signature of a capacity variable rather than a decision. Days 22-26 add 1-2
CARROT and nothing else.

If Ryo and tetsuya show the same shape, the mid-season needs no row library and no tree for any of
them: it is the greedy planner with the crop pinned. If they show a real mix, the wheat-fill is
Kawashigi's alone and does not generalise -- which matters, because Ryo is already known to differ
(no geese, Q3 not Q4, wheat 70% / carrot 54% / tomato 25%).

Three columns decide it:

  crops      how many distinct crop NAMES the day uses across all seasons
  purity     share of all plants that are the day's single most common crop
  counts     how many distinct multisets remain once the count is ignored --
             1 means the day is one crop mix scaled up and down, i.e. a scalar

    python -u scripts/crop_shape_by_day.py --targets data/target_rows_kawa_norm.json --label kawa
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def shape(multiset):
    """The crop mix with the scale divided out: sorted (crop, share-rank) ignoring magnitude.

    WHEAT:5 and WHEAT:11 both become ('WHEAT',). CARROT:1 WHEAT:9 and CARROT:2 WHEAT:6 both become
    ('CARROT', 'WHEAT'). So a day whose seasons differ only in size collapses to ONE shape.
    """
    return tuple(sorted(set(multiset)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True)
    ap.add_argument("--label", required=True)
    args = ap.parse_args()

    rows = json.loads(pathlib.Path(args.targets).read_text())
    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(list(r["target"].get("plants") or []))

    print("%s -- %d day-rows over %d seats\n"
          % (args.label, len(rows), len({(r["game"], r["seat"]) for r in rows})))
    print("%4s %7s %8s %7s %8s %8s  %s"
          % ("day", "seats", "multiset", "shapes", "purity", "n range", "top crop mix"))
    for day in sorted(by_day):
        ms = by_day[day]
        if not ms:
            continue
        multisets = collections.Counter(tuple(sorted(m)) for m in ms)
        shapes = collections.Counter(shape(m) for m in ms)
        crops = collections.Counter()
        for m in ms:
            crops.update(m)
        total = sum(crops.values())
        purity = (crops.most_common(1)[0][1] / total) if total else 1.0
        sizes = [len(m) for m in ms]
        top = shapes.most_common(1)[0][0]
        print("%4d %7d %8d %7d %7.0f%% %4d-%-3d  %s"
              % (day, len(ms), len(multisets), len(shapes), 100 * purity,
                 min(sizes), max(sizes),
                 "+".join(c[:4] for c in top) if top else "(none)"))

    print("\nSEASON CROP TOTALS")
    crops = collections.Counter()
    for ms in by_day.values():
        for m in ms:
            crops.update(m)
    tot = sum(crops.values()) or 1
    for c, n in crops.most_common():
        print("  %-8s %7d  %5.1f%%" % (c, n, 100.0 * n / tot))


if __name__ == "__main__":
    main()
