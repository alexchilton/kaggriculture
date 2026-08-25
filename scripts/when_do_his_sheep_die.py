"""On which day does カワシギ stop feeding his sheep, and what is the WOOL book doing then?

Alex: there is no selling animals in this env -- an animal leaves the board only by not being fed.
So the day a sheep vanishes is the day he decided it was not worth a FEED turn any more.

Measured on 2026-08-25 over his post-change tapes: he places 15.01 animals on average and finishes
with 12.20, and **zero cows are ever lost** -- 76 seats, every row. Only sheep go.

What this prints, per game and then aggregated:

    first_drop  -- the first day his SHEEP count falls
    wool_at_drop -- the town's WOOL price on that day, if the recording carries a book
    sheep curve  -- his sheep count per day, so a slow bleed is distinguishable from a cliff

The day is what a rule would key on, and the wool price is what it SHOULD key on if the two do not
line up. Do not read the aggregate alone: a mean of a bimodal thing is a number nothing does.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

KAWA = "カワシギ"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")
TPD = 24


def _herd_by_day(replay, seat):
    """`day -> (cows, sheep)` standing on his board at the LAST turn of each day."""
    out = {}
    steps = replay.get("steps") or []
    for t, step in enumerate(steps):
        obs = (step[0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if seat >= len(farms):
            continue
        c = collections.Counter()
        for row in (farms[seat].get("tiles") or []):
            for tile in row:
                if isinstance(tile, dict) and tile.get("animal"):
                    c[tile["animal"]] += 1
        out[t // TPD] = (c.get("COW", 0), c.get("SHEEP", 0))
    return out


def _wool_price(replay, t):
    """The town's WOOL price at turn `t`, or None if the recording does not carry a book."""
    steps = replay.get("steps") or []
    if t >= len(steps):
        return None
    town = ((steps[t][0] or {}).get("observation") or {}).get("town") or {}
    for key in ("prices", "market", "book"):
        blob = town.get(key)
        if isinstance(blob, dict) and "WOOL" in blob:
            v = blob["WOOL"]
            return float(v.get("price", v)) if isinstance(v, dict) else float(v)
    return None


def main():
    rows, drops, curves = [], collections.Counter(), []
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(r, dict):
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            seat = names.index(KAWA)
            by_day = _herd_by_day(r, seat)
            if not by_day:
                continue
            days = sorted(by_day)
            peak = max(by_day[x][1] for x in days)
            first = None
            for i in range(1, len(days)):
                if by_day[days[i]][1] < by_day[days[i - 1]][1]:
                    first = days[i]
                    break
            end = by_day[days[-1]][1]
            if first is not None:
                drops[first] += 1
                rows.append((first, peak, end, _wool_price(r, first * TPD), f.stem))
            curves.append([by_day[x][1] for x in days])

    print(f"kawa post-change seats with a herd curve: {len(curves)}", flush=True)
    print(f"seats where SHEEP ever fall: {len(rows)}")
    print()
    print("FIRST DAY THE SHEEP COUNT FALLS")
    print(f"  {'day':>4}{'seats':>7}   share")
    n = sum(drops.values()) or 1
    for day in sorted(drops):
        print(f"  {day:>4}{drops[day]:>7}   {100.0 * drops[day] / n:>5.1f}%")
    print()
    if rows:
        peaks = [r[1] for r in rows]
        ends = [r[2] for r in rows]
        firsts = [r[0] for r in rows]
        print(f"  median first-drop day {sorted(firsts)[len(firsts) // 2]}")
        print(f"  mean sheep peak {sum(peaks) / len(peaks):.2f} -> end {sum(ends) / len(ends):.2f}")
        wools = [r[3] for r in rows if r[3] is not None]
        if wools:
            print(f"  WOOL price at the drop: mean {sum(wools) / len(wools):,.1f} "
                  f"min {min(wools):,.1f} max {max(wools):,.1f}   (n={len(wools)})")
        else:
            print("  WOOL price at the drop: the recordings carry no book on the town object")
    print()
    print("MEAN SHEEP COUNT BY DAY (all seats):")
    width = max(len(c) for c in curves)
    for day in range(width):
        vals = [c[day] for c in curves if day < len(c)]
        bar = "#" * int(round(sum(vals) / len(vals)))
        print(f"  d{day:<3}{sum(vals) / len(vals):>6.2f}  {bar}")


if __name__ == "__main__":
    main()
