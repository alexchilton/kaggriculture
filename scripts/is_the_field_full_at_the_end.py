"""Do the winners end with a FULL field?

Alex, 2026-08-26: *"there are 2 wins downloaded - i see immediately that the field is full at the
end so..."*

Counted at the LAST recorded step, per seat, on owned ground only:

    owned       100 minus the LOCKED squares -- a locked square is the literal string "LOCKED",
                an empty one is None, and only PLANT and PASTURE cells are dicts. There is no
                `owned` key; a first cut that counted dict cells was counting "squares with
                something on them", which is the quantity this script exists to measure and would
                have made every row 100%.
    used        cells carrying a crop or an animal
    fill        used / owned

Split by whether that seat WON, because the ladder is Elo and a full field in a lost game is not
evidence for anything.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def board(farm):
    locked = crop = animal = standing = 0
    for row in (farm.get("tiles") or []):
        for c in row:
            if c == "LOCKED":
                locked += 1
            elif isinstance(c, dict):
                if c.get("crop"):
                    crop += 1
                    standing += int(c.get("yield_units", 0) or 0)
                elif c.get("animal"):
                    animal += 1
    return 100 - locked, crop, animal, standing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/seed_scripts/daily_2026-08-26")
    args = ap.parse_args()

    rows = []
    for f in sorted(pathlib.Path(args.root).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            rep = json.loads(f.read_text())
        except Exception:                                                      # noqa: BLE001
            continue
        steps = rep.get("steps") or []
        if not steps:
            continue
        obs = (steps[-1][0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) < 2:
            continue
        money = [float(x.get("money", 0)) for x in farms]
        for seat in (0, 1):
            owned, crop, animal, standing = board(farms[seat])
            rows.append(dict(won=money[seat] > money[1 - seat], money=money[seat],
                             owned=owned, used=crop + animal, crop=crop, animal=animal,
                             standing=standing))

    print(f"{len(rows)} seats\n")
    print(f"{'group':<10}{'n':>5}{'owned':>8}{'used':>8}{'fill':>8}"
          f"{'crop':>8}{'pens':>8}{'standing':>10}{'money':>11}")
    for name, sel in (("WON", lambda r: r["won"]), ("LOST", lambda r: not r["won"])):
        g = [r for r in rows if sel(r)]
        if not g:
            continue
        n = len(g)
        avg = lambda k: sum(r[k] for r in g) / n                               # noqa: E731
        print(f"{name:<10}{n:>5}{avg('owned'):>8.1f}{avg('used'):>8.1f}"
              f"{100 * avg('used') / max(1.0, avg('owned')):>7.0f}%"
              f"{avg('crop'):>8.1f}{avg('animal'):>8.1f}{avg('standing'):>10.1f}"
              f"{avg('money'):>11,.0f}")

    # The top of the field, since the winners are not one population.
    top = sorted(rows, key=lambda r: -r["money"])[:20]
    n = len(top)
    avg = lambda k: sum(r[k] for r in top) / n                                 # noqa: E731
    print(f"{'TOP 20 $':<10}{n:>5}{avg('owned'):>8.1f}{avg('used'):>8.1f}"
          f"{100 * avg('used') / max(1.0, avg('owned')):>7.0f}%"
          f"{avg('crop'):>8.1f}{avg('animal'):>8.1f}{avg('standing'):>10.1f}"
          f"{avg('money'):>11,.0f}")


if __name__ == "__main__":
    main()
