"""Extract a winning seat's plan as a (square -> chain) map, read straight off the replay.

Alex's point, and it is decisive: we already reproduce a real $145k season to 0.2%, so the winning
plan is not something to search for -- it is on disk, and the episode observations carry the full
`tiles` grid at every step. So rather than reconstruct positions from the action tape, read the roles
directly and record the day each square took its role.

That output *is* the genome the chain search should be initialised from:

    (x, y) -> {role: PASTURE|COOP|PLANT|EMPTY, animal|crop: ..., day_assigned: int}

plus the season-level parameters: land purchase days, crew size per day, wheat purchased per day and
the sell schedule.

Two facts this exists to correct, both of them mine and both measured wrong today:

- A ranch does **not** cap at the four shed-access tiles. The top seat runs 25 animals. The
  zero-movement shed cell is an optimisation, not a ceiling.
- Land is **not** the dominant lever. Top seats buy ~1.3 parcels around day 9-10 and plant very
  little; they buy wheat and convert it to milk and wool.

    PYTHONPATH=. python3 -u scripts/extract_winner_plan.py --episode 89113699 --seat 1
"""

import argparse
import collections
import json
import pathlib

TURNS_PER_DAY = 24


def tile_role(t):
    """`(role, subject)` for one tile entry, collapsing the reference's mixed representation."""
    if t is None:
        return "EMPTY", None
    if isinstance(t, str):
        return t, None                      # "LOCKED"
    kind = t.get("kind")
    if "animal" in t:
        return "ANIMAL", t["animal"]
    if kind == "PLANT":
        return "PLANT", t.get("crop")
    return kind or "?", None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="89113699")
    ap.add_argument("--seat", type=int, default=1)
    ap.add_argument("--data", default="data")
    a = ap.parse_args()

    path = pathlib.Path(a.data) / f"{a.episode}.json"
    ep = json.loads(path.read_text())
    steps = ep["steps"]
    money = ep["rewards"][a.seat]
    print(f"episode {a.episode} seat {a.seat}: final ${money:,.0f}   {len(steps)} steps\n")

    # ---- when did each square first take each role? ----------------------
    first = {}            # (x, y) -> (role, subject, day)
    history = collections.defaultdict(list)
    crew, land_days, wheat, sells = {}, [], collections.Counter(), collections.defaultdict(collections.Counter)
    animals_live = {}

    for t, step in enumerate(steps):
        obs = step[a.seat].get("observation") or step[0].get("observation")
        day = t // TURNS_PER_DAY
        farms = (obs or {}).get("farms")
        if farms and a.seat < len(farms):
            farm = farms[a.seat]
            crew[day] = 1 + len(farm.get("hands") or [])
            animals_live[day] = sum(
                1 for row in farm["tiles"] for tile in row
                if isinstance(tile, dict) and "animal" in tile)
            for y, row in enumerate(farm["tiles"]):
                for x, tile in enumerate(row):
                    role, subject = tile_role(tile)
                    key = (x, y)
                    if role in ("EMPTY", "LOCKED"):
                        continue
                    if key not in first:
                        first[key] = (role, subject, day)
                    if not history[key] or history[key][-1][:2] != (role, subject):
                        history[key].append((role, subject, day))
        action = step[a.seat].get("action")
        if isinstance(action, dict):
            for order in action.get("market") or []:
                if not order:
                    continue
                if order[0] in ("BUY_LAND", "BUID_LAND"):
                    land_days.append(day)
                elif order[0] == "BUY_PRODUCT" and len(order) >= 3 and order[1] == "WHEAT":
                    wheat[day] += int(order[2])
                elif order[0] == "SELL" and len(order) >= 3:
                    sells[order[1]][day] += int(order[2])

    # ---- the board, as a plan --------------------------------------------
    print("SQUARE -> CHAIN, with the day the square was first committed")
    print("(A=animal pen, P=crop, .=never used, #=stayed locked; digit = day committed / 3)\n")
    print("     " + " ".join(f"{x}" for x in range(10)))
    for y in range(10):
        cells = []
        for x in range(10):
            if (x, y) in first:
                role, subject, day = first[(x, y)]
                mark = {"ANIMAL": "A", "PASTURE": "a", "COOP": "c", "PLANT": "P"}.get(role, "?")
                cells.append(mark)
            else:
                cells.append(".")
        print(f"  {y}  " + " ".join(cells))
    print()

    roles = collections.Counter(r for r, _s, _d in first.values())
    subjects = collections.Counter(s for _r, s, _d in first.values() if s)
    print(f"roles committed: {dict(roles)}")
    print(f"subjects:        {dict(subjects)}")
    print()

    print("ANIMAL PENS -- square, animal, day committed")
    pens = sorted(((d, xy, s) for xy, (r, s, d) in first.items() if r == "ANIMAL"))
    for day, xy, subject in pens:
        print(f"  {xy}  {subject:<6} day {day}")
    print(f"  -> {len(pens)} pens, first day {pens[0][0] if pens else '-'}, "
          f"last day {pens[-1][0] if pens else '-'}")
    print()

    print("CROP TILES -- square, crop, day committed")
    crops = sorted(((d, xy, s) for xy, (r, s, d) in first.items() if r == "PLANT"))
    for day, xy, subject in crops[:20]:
        print(f"  {xy}  {str(subject):<12} day {day}")
    if len(crops) > 20:
        print(f"  ... {len(crops) - 20} more")
    print()

    print("SEASON PARAMETERS")
    print(f"  land purchase days : {sorted(set(land_days)) or '-'}")
    print(f"  crew by day        : " + " ".join(f"{crew.get(d, 0)}" for d in range(30)))
    print(f"  live animals by day: " + " ".join(f"{animals_live.get(d, 0)}" for d in range(30)))
    print(f"  wheat bought/day   : " + " ".join(f"{wheat.get(d, 0)}" for d in range(30)))
    print(f"  total wheat        : {sum(wheat.values())}")
    print()
    print("SELL SCHEDULE (requested units; the 100-unit global shed cap limits what fills)")
    for product, days in sorted(sells.items(), key=lambda kv: -sum(kv[1].values())):
        tot = sum(days.values())
        late = sum(n for d, n in days.items() if d >= 20) / max(tot, 1)
        print(f"  {product:<12} total {tot:>7}   {late:>5.1%} on day 20+   "
              f"first day {min(days)}  last {max(days)}")


if __name__ == "__main__":
    raise SystemExit(main())
