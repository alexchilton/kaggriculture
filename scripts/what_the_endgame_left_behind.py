"""What a finished season left on the board, and what it was worth.

Alex, 2026-08-24, on ladder game 98335212 (lost by $781 of $85,177): *"it gets stuff into the shed
but leaves for instance a heap of sheep out from the end at 200+"*.

`END`-style totals cannot see this. A season that banks $84,396 with four uncollected wool on the
sheep looks identical to one that banks $84,396 with an empty board -- the difference is $800+ and,
in this game, more than the whole losing margin.

So this prints, for each seat: what is still standing on the tiles at the final turn, what the town
would have paid for it, and the last hour at which each item became collectable. The last column is
the one that says whether the miss was *reachable* -- yield that ripened at d29 h23 was never
sellable, and yield that ripened on d28 was.

Usage:
    python -u scripts/what_the_endgame_left_behind.py data/seed_scripts/losses/98335212.json
"""

import json
import pathlib
import sys
from collections import defaultdict

# `reference/kaggriculture.py` is the ground truth for the pairing and for what a shop pays.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))


def _load(path):
    with open(path) as fh:
        return json.load(fh)


def _tiles(step, seat):
    """Non-empty tiles of `seat`, as (row, col, tile-dict).

    **Read each seat's own observation.** `steps[i][0]["observation"]["farms"][1]` is the opponent as
    seat 0 sees it and is not the same object -- indexing it cost one crash before this note existed.
    """
    grid = step[seat]["observation"]["farms"][seat]["tiles"]
    for r, row in enumerate(grid):
        for c, tile in enumerate(row):
            if isinstance(tile, dict):
                yield r, c, tile


# `reference/kaggriculture.py:19-22`. The tile names the ANIMAL; the town pays for its PRODUCT.
ANIMAL_PRODUCT = {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}


def _price(obs, item):
    """What the town pays for one unit of `item` at this moment, from the observation itself."""
    return float(((obs.get("market") or {}).get("prices") or {}).get(item, 0.0))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/seed_scripts/losses/98335212.json"
    rep = _load(path)
    steps = rep["steps"]
    names = [a["Name"] for a in rep["info"]["Agents"]]
    rewards = rep["rewards"]

    print(f"game {rep['info']['EpisodeId']}  seed {rep['info']['seed']}")
    for s, (n, m) in enumerate(zip(names, rewards)):
        print(f"  seat {s}  {n:<20} ${m:>12,.0f}")
    print(f"  margin ${abs(rewards[0] - rewards[1]):,.0f}\n")

    # **When did each tile last become collectable?** Walk the replay once and record, per tile, the
    # last step at which its yield went UP. Yield that appeared in the final hours was never sellable
    # however good the plan was; yield that appeared on d28 was, and that is the actionable half.
    appeared = {}                                   # (seat, r, c) -> (day, hour)
    prev = defaultdict(int)
    for step in steps:
        for seat in (0, 1):
            obs = step[seat]["observation"]
            for r, c, tile in _tiles(step, seat):
                u = tile.get("yield_units") or 0
                if u > prev[(seat, r, c)]:
                    appeared[(seat, r, c)] = (obs["day"], obs["hour"])
                prev[(seat, r, c)] = u

    for seat in (0, 1):
        obs = steps[-1][seat]["observation"]
        print(f"--- seat {seat}  {names[seat]}  ${rewards[seat]:,.0f} ---")
        shed = {k: v for k, v in obs["private"]["shed"].items() if v}
        print(f"  shed at the final turn: {shed or 'empty'}")

        rows = []
        for r, c, tile in _tiles(steps[-1], seat):
            units = tile.get("yield_units") or 0
            if not units:
                continue
            animal = tile.get("animal")
            product = ANIMAL_PRODUCT[animal] if animal else tile.get("crop")
            px = _price(obs, product) if product else 0.0
            day, hour = appeared.get((seat, r, c), (None, None))
            rows.append((r, c, animal or tile.get("crop"), product, units, px, units * px,
                         day, hour))

        if not rows:
            print("  nothing left standing\n")
            continue

        print(f"  {'tile':>7}  {'holding':<10} {'sells as':<10} {'units':>5} {'$/unit':>8} "
              f"{'value':>10}  ripened")
        for r, c, what, product, units, px, val, day, hour in sorted(rows, key=lambda x: -x[6]):
            when = f"d{day} h{hour}" if day is not None else "unknown"
            print(f"  ({r},{c})  {str(what):<10} {str(product):<10} {units:>5} {px:>8,.0f} "
                  f"{val:>10,.0f}  {when}")

        total = sum(x[6] for x in rows)
        reachable = sum(x[6] for x in rows if x[7] is not None and x[7] <= 28)
        print(f"  {sum(x[4] for x in rows)} units on {len(rows)} tiles, "
              f"marked at ${total:,.0f}")
        print(f"  of which ripened on d28 or earlier -- i.e. there WAS time to sell it: "
              f"${reachable:,.0f}")
        print(f"  losing margin was ${abs(rewards[0] - rewards[1]):,.0f}\n")


if __name__ == "__main__":
    main()
