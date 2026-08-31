"""What we leave standing, and whether it was ever collectable. Ours against theirs.

Measured across six downloaded losses: we finish holding **28-42 units** on the board, they finish
holding **2-9**. Every game. That is not noise and it is not a tie-breaker -- four of the six
margins are under $3,560.

The question this answers is which of three things it is, because they need different fixes:

    ripened too late      the tile produced on d29 and no route could have reached it.
                          Fix is upstream: do not plant something that ripens after the last
                          sellable turn.
    too far               it ripened in time but sits far from the shed, so collecting it costs
                          more turns than it pays. Fix is WHERE we plant in d24-d26.
    reachable and missed  ripe by d28, close to home, and still there at the close.
                          Fix is the routing or the prize.

Distance is Chebyshev to the nearest depot cell, because a unit moves one square per turn in four
directions and the board's depot is a block -- so `max(|dr|, |dc|)` is the turn cost of the walk,
and a round trip is twice that plus a turn to DROP.

Reads recorded tapes only. No simulation, so nothing here depends on our agent reproducing anything,
and there is no seed to get wrong.

    python -u scripts/why_the_field_is_not_cleared.py
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TPD = 24
US = "alex chilton"
ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}
GAMES = ("98495047", "98460892", "98494953", "98499540", "98501831", "98428765")


def _find(ep):
    hits = list((REPO / "data/seed_scripts").rglob(f"{ep}.json"))
    return hits[0] if hits else None


def _tiles(step, seat):
    grid = step[seat]["observation"]["farms"][seat]["tiles"]
    for r, row in enumerate(grid):
        for c, tile in enumerate(row):
            if isinstance(tile, dict):
                yield r, c, tile


def _depots(step, seat):
    """Cells a DROP lands on. Read from the board rather than assumed: a test once hard-coded one
    depot at (5,4) and the real board has four, the nearest being (4,5)."""
    out = []
    for r, c, tile in _tiles(step, seat):
        kind = (tile.get("kind") or "").upper()
        if "SHED" in kind or "DEPOT" in kind or tile.get("is_depot"):
            out.append((r, c))
    return out


def dist(pos, depots):
    if not depots:
        return None
    return min(max(abs(pos[0] - d[0]), abs(pos[1] - d[1])) for d in depots)


def main():
    per_seat = {"ours": collections.Counter(), "theirs": collections.Counter()}
    value = {"ours": collections.Counter(), "theirs": collections.Counter()}
    rows = []

    for ep in GAMES:
        path = _find(ep)
        if path is None:
            print(f"{ep}: not downloaded", flush=True)
            continue
        rec = json.loads(path.read_text())
        names = rec["info"]["TeamNames"]
        if US not in names:
            continue
        seat = names.index(US)
        steps = rec["steps"]
        last = steps[-1]
        px = (last[0]["observation"].get("market") or {}).get("prices") or {}

        # The day each tile's yield last INCREASED is the day it became collectable.
        appeared = {}
        prev = collections.Counter()
        for i, step in enumerate(steps):
            for s in (0, 1):
                for r, c, tile in _tiles(step, s):
                    u = tile.get("yield_units") or 0
                    if u > prev[(s, r, c)]:
                        appeared[(s, r, c)] = step[s]["observation"]["day"]
                    prev[(s, r, c)] = u

        for s, who in ((seat, "ours"), (1 - seat, "theirs")):
            depots = _depots(last, s)
            for r, c, tile in _tiles(last, s):
                units = tile.get("yield_units") or 0
                if not units:
                    continue
                animal = tile.get("animal")
                product = ANIMAL_PRODUCT[animal] if animal else tile.get("crop")
                price = float(px.get(product, 0) or 0)
                d = dist((r, c), depots)
                ripe = appeared.get((s, r, c))
                if ripe is None or ripe >= 29:
                    bucket = "ripened d29 -- never sellable"
                elif d is not None and d > 6:
                    bucket = f"ripe d{ripe}, but {d} squares out"
                else:
                    bucket = f"ripe d{ripe}, {d} squares out -- REACHABLE"
                per_seat[who][bucket] += units
                value[who][bucket] += units * price
                if who == "ours":
                    rows.append((ep, (r, c), product, units, price, ripe, d))

    for who in ("ours", "theirs"):
        tot = sum(per_seat[who].values())
        totv = sum(value[who].values())
        print(f"\n=== {who}: {tot} units left standing, ${totv:,.0f} ===")
        for bucket, units in per_seat[who].most_common():
            print(f"  {units:>4} units  ${value[who][bucket]:>8,.0f}   {bucket}")

    print("\nreachable leftovers, ours, worst first:")
    reach = [r for r in rows if r[5] is not None and r[5] < 29 and r[6] is not None and r[6] <= 6]
    reach.sort(key=lambda r: -(r[3] * r[4]))
    print(f"  {'game':>10} {'tile':>8} {'product':<11} {'units':>5} {'$/u':>6} "
          f"{'ripe':>5} {'dist':>5} {'value':>8}")
    for ep, pos, product, units, price, ripe, d in reach[:15]:
        print(f"  {ep:>10} {str(pos):>8} {product:<11} {units:>5} {price:>6.0f} "
              f"d{ripe:<4} {d:>5} ${units * price:>7,.0f}")


if __name__ == "__main__":
    main()
