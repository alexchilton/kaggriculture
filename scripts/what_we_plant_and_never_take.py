"""Per crop, on a downloaded game: what we planted, what we harvested, and what rotted in the ground.

Alex, on the carrot-only validation game: *"it looks like you are planting lots of carrot but then
leaving them in the ground can that be? seems a bit daft"*.

A planting that is never harvested is worse than a planting not made: it spent a seed, a PLANT turn,
and every WATER turn keeping it alive, and it blocks the tile for the rest of the season.

Counted the only way that cannot overcount:

    PLANT ops       a unit op, emitted once per planting.
    HARVEST ops     likewise, on a tile carrying a crop.
    standing        `yield_units` sitting on crop tiles at the last turn, by crop.
    tiles at bell   how many tiles still carry each crop, and how many are WEED.

`BUY_SEED` is a market order and is re-posted every turn, so it is NOT used for the seed count
(`feedback_offers_are_not_fills`). Seed left in the shed is read off the shed at the bell instead.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

US = "alex chilton"
TPD = 24


def main(paths):
    for p in paths:
        f = pathlib.Path(p)
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else 0
        steps = r.get("steps") or []

        planted = collections.Counter()
        harvested = collections.Counter()
        # A PLANT op names the crop; a HARVEST does not, so the tile has to be read.
        for t, step in enumerate(steps):
            if seat >= len(step):
                continue
            act = (step[seat] or {}).get("action") or {}
            obs = (step[0] or {}).get("observation") or {}
            farms = obs.get("farms") or []
            tiles = farms[seat].get("tiles") if seat < len(farms) else None
            for op in [act.get("farmer")] + list(act.get("hands") or []):
                if not op:
                    continue
                if op[0] == "PLANT" and len(op) >= 2:
                    planted[op[1]] += 1
                elif op[0] == "HARVEST" and tiles is not None:
                    harvested["_any"] += 1

        last = (steps[-1][0] or {}).get("observation") or {}
        farms = last.get("farms") or []
        standing, tiles_at_bell, weeds = collections.Counter(), collections.Counter(), 0
        shed = {}
        if seat < len(farms):
            for row in (farms[seat].get("tiles") or []):
                for tile in row:
                    if not isinstance(tile, dict):
                        continue
                    if tile.get("kind") == "WEED":
                        weeds += 1
                    c = tile.get("crop")
                    if c:
                        tiles_at_bell[c] += 1
                        standing[c] += int(tile.get("yield_units", 0) or 0)
            shed = dict((farms[seat].get("shed") or {}))

        opp = 1 - seat
        ours = float(farms[seat].get("money", 0)) if seat < len(farms) else 0.0
        theirs = float(farms[opp].get("money", 0)) if opp < len(farms) else 0.0
        print(f"=== {f.stem}   seats {names}   we are seat {seat}")
        print(f"    ours ${ours:,.0f}  theirs ${theirs:,.0f}  "
              f"{'WIN' if ours > theirs else 'LOSS' if ours < theirs else 'DRAW'}"
              f"   weeds at bell {weeds}")
        print(f"    {'crop':<12}{'planted':>9}{'tiles@bell':>12}{'units standing':>16}")
        for crop in sorted(set(planted) | set(tiles_at_bell)):
            print(f"    {crop:<12}{planted[crop]:>9}{tiles_at_bell[crop]:>12}"
                  f"{standing[crop]:>16}")
        print(f"    total HARVEST ops all season: {harvested['_any']}")
        seedy = {k: v for k, v in shed.items() if k.endswith("_SEED") and v}
        print(f"    seed left in the shed at the bell: {seedy or 'none'}")
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
