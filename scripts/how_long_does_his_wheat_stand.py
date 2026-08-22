"""How many days does each of his wheat tiles stand before he harvests it?

This decides whether a WHEAT -> CARROT swap is possible at all, and on how many tiles.

`reference/kaggriculture.py:224` gives a non-ongoing crop a lifespan of `planted_day +
max_yield_day + 1` days, and `:759-766` then removes one `yield_unit` every two steps past it and
turns the tile into a **WEED** when the units run out:

    WHEAT   max_yield_day 4   lifespan planted+5   6 units to lose  -> weed 12 turns after
    CARROT  max_yield_day 3   lifespan planted+4   4 units to lose  -> weed  8 turns after

So a carrot on a tile he harvests at planted+4 is fine, and one on a tile he harvests at planted+5
is already decaying -- and at planted+5 plus 8 turns it is a weed. That is the same `weed x21`
signature the d8 hire bug produced, which is a good reason not to guess.

This reads the board rather than the action stream, because PLANT carries no coordinates -- the unit
plants where it stands. A tile's `planted_day` is in the observation, so the gap is the day the tile
stops carrying that crop minus the day it was sown.

    python -u scripts/how_long_does_his_wheat_stand.py
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TAPES = (("melon q3", "data/seed_scripts/kawashigi/92498144.json"),
         ("straw q3", "data/seed_scripts/kawashigi/92466371.json"),
         ("q4      ", "data/seed_scripts/downloads_2026-08-13/91907974.json"))

#: Carrot is a candidate only where he lifts the wheat by this many days after sowing. At +5 the
#: carrot has been decaying for a day; past that it is a weed.
CARROT_SAFE_GAP = 4


def gaps(path, team="カワシギ", crop="WHEAT"):
    """`[(planted_day, gone_day)]` for every tile of `crop`, read off the dawn boards."""
    d = json.loads(pathlib.Path(path).read_text())
    seat = d["info"]["TeamNames"].index(team)
    seen = {}                                        # (y, x, planted_day) -> last day still there
    for day in range(30):
        idx = day * 24
        if idx >= len(d["steps"]):
            break
        farms = ((d["steps"][idx][seat].get("observation") or {}).get("farms") or [])
        if len(farms) <= seat:
            continue
        for y, row in enumerate(farms[seat].get("tiles") or []):
            for x, c in enumerate(row):
                if isinstance(c, dict) and c.get("crop") == crop:
                    seen[(y, x, c.get("planted_day"))] = day
    return [(pd, last) for (y, x, pd), last in seen.items() if pd is not None]


def main():
    for name, path in TAPES:
        rows = gaps(path)
        # A tile seen at dawn on `last` and not the next dawn was lifted during `last` or `last+1`.
        dist = collections.Counter(last - pd + 1 for pd, last in rows)
        late = [(pd, last) for pd, last in rows if pd >= 18]
        late_dist = collections.Counter(last - pd + 1 for pd, last in late)
        print("=== %s  %s ===" % (name, pathlib.Path(path).stem))
        print("  %d wheat tiles; days standing (planted -> last seen +1):" % len(rows))
        for g in sorted(dist):
            mark = "  <- carrot safe" if g <= CARROT_SAFE_GAP else ""
            print("     %2d days  %4d tiles%s" % (g, dist[g], mark))
        safe = sum(n for g, n in dist.items() if g <= CARROT_SAFE_GAP)
        print("  carrot-safe: %d of %d (%.0f%%)" % (safe, len(rows), 100.0 * safe / max(1, len(rows))))
        if late:
            lsafe = sum(n for g, n in late_dist.items() if g <= CARROT_SAFE_GAP)
            print("  sown d18+: %d tiles, %d carrot-safe -> %s"
                  % (len(late), lsafe, dict(sorted(late_dist.items()))))
        print()


if __name__ == "__main__":
    main()
