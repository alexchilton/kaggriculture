"""Parse every replay ONCE into a compact per-turn cache.

The first clonability sweep timed out at ten minutes because it re-read 600 JSON files for every
player. Each replay is ~500KB of nested dicts and eight fields are wanted from it. Parse once,
cache, reuse.

    python -u scripts/cache_turns.py --dirs data/seed_scripts/downloads_2026-08-20 \
        data/seed_scripts/downloads_2026-08-19 --out data/il/turns_cache.jsonl

One line per turn:
    {g: game id, t: team, d: day, h: hour, s: [shops], op: farmer op,
     x, y: farmer position, u: tile kind under the farmer, b: [[op,item],...] market bundle}

**`u` is what the farmer is STANDING ON, and it is the whole point of this cache.** FEED, CARE and
COLLECT_FERTILIZER only fire on a pen; HARVEST only on a ripe tile. Nothing in the shop draw encodes
that, which is why every shop-keyed attempt at the unit op measured as noise -- see the addendum in
`docs/the_market_is_one_token_not_nine_heads_2026-08-20.md`. Both seats are cached, so any player in
the file can be used as a teacher without re-parsing.
"""

import argparse
import json
import pathlib


def tile_kind(cell):
    """A coarse label for what occupies a tile: enough to explain the op, small enough to key on."""
    if cell is None:
        return "."
    if isinstance(cell, dict):
        if "animal" in cell:
            return "A:%s:%d" % (cell["animal"], int(cell.get("yield_units", 0) or 0) > 0)
        kind = cell.get("kind")
        if kind == "PLANT":
            return "P:%s:%d" % (cell.get("crop"), int(cell.get("yield_units", 0) or 0) > 0)
        return str(kind)
    return str(cell)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths.extend(sorted(pathlib.Path(d).glob("*.json")))

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    turns = files = 0
    with out.open("w") as fh:
        for p in paths:
            try:
                d = json.loads(p.read_text())
            except Exception:                                      # noqa: BLE001
                continue
            names = [str(n) for n in ((d.get("info") or {}).get("TeamNames") or [])]
            steps = d.get("steps") or []
            files += 1
            for seat, team in enumerate(names):
                for i, step in enumerate(steps):
                    if i == 0:
                        continue
                    prev = (steps[i - 1][seat] or {}).get("observation") or {}
                    if "day" not in prev or "farms" not in prev:
                        continue
                    farm = (prev.get("farms") or [None, None])[seat] or {}
                    tiles = farm.get("tiles") or []
                    pos = farm.get("farmer") or [4, 4]
                    try:
                        x, y = int(pos[0]), int(pos[1])
                        under = tile_kind(tiles[y][x])
                    except Exception:                              # noqa: BLE001
                        x = y = -1
                        under = "?"
                    act = (step[seat] or {}).get("action") or {}
                    fa = act.get("farmer")
                    mk = act.get("market") or []
                    fh.write(json.dumps({
                        "g": p.stem, "t": team,
                        "d": int(prev.get("day", 0) or 0), "h": int(prev.get("hour", 0) or 0),
                        "s": sorted(str(v) for v in
                                    ((prev.get("town") or {}).get("unlocked_shops") or [])),
                        "op": (fa[0] if fa else "-"), "x": x, "y": y, "u": under,
                        "b": sorted([str(o[0]), str(o[1]) if len(o) > 1 else ""]
                                    for o in mk if isinstance(o, (list, tuple)) and o),
                    }) + "\n")
                    turns += 1
            if files % 150 == 0:
                print("  %d files, %d turns" % (files, turns), flush=True)
    print("%s  %d files, %d turns" % (out, files, turns))


if __name__ == "__main__":
    main()
