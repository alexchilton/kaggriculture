"""Which day does カワシギ emit his last FEED, and how many pens does he feed each day?

Alex: "maybe he doesnt feed on d28 and thats the first non feed and then they die on d29 ...
cos its 2 non feeds to die".

He is right that the escape needs two. `_daily_refresh_animals` (`kaggriculture.py:813-820`) runs
inside `_end_of_day`: a day with `fed_today` False increments `consecutive_unfed`, and the animal
is removed at `>= 2`. So the last two days of an animal's life are both unfed.

**The board read cannot settle which two days those are**, because it depends on whether the final
recorded observation is before or after the last rollover -- an off-by-one I have no right to guess
at. The ACTIONS have no such ambiguity: a FEED is emitted on a turn, and the turn's day is
`t // 24`. So this counts FEED ops, not tiles.

Printed per day: how many FEEDs he emits, how many pens he has standing, and the same for us is not
here -- this is his tape only.
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


def main():
    feeds = collections.defaultdict(list)     # day -> [feeds emitted, per seat]
    pens = collections.defaultdict(list)      # day -> [pens standing, per seat]
    last_feed_day = collections.Counter()
    step_counts = collections.Counter()
    n = 0
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
            n += 1
            steps = r.get("steps") or []
            step_counts[len(steps)] += 1
            per_day = collections.Counter()
            pen_day = {}
            for t, step in enumerate(steps):
                day = t // TPD
                if seat < len(step):
                    act = (step[seat] or {}).get("action") or {}
                    for op in [act.get("farmer")] + list(act.get("hands") or []):
                        if op and op[0] == "FEED":
                            per_day[day] += 1
                obs = (step[0] or {}).get("observation") or {}
                farms = obs.get("farms") or []
                if seat < len(farms):
                    c = sum(1 for row in (farms[seat].get("tiles") or []) for tile in row
                            if isinstance(tile, dict) and tile.get("animal"))
                    pen_day[day] = c
            days = sorted(set(list(per_day) + list(pen_day)))
            for day in days:
                feeds[day].append(per_day.get(day, 0))
                if day in pen_day:
                    pens[day].append(pen_day[day])
            fed_days = [day for day in per_day if per_day[day] > 0]
            if fed_days:
                last_feed_day[max(fed_days)] += 1

    print(f"kawa post-change seats: {n}", flush=True)
    print(f"steps per recording: {dict(step_counts)}")
    print(f"  -> last turn index {max(step_counts) - 1}, which is day {(max(step_counts) - 1) // TPD}")
    print()
    print("HIS LAST DAY WITH ANY FEED")
    print(f"  {'day':>4}{'seats':>7}   share")
    tot = sum(last_feed_day.values()) or 1
    for day in sorted(last_feed_day):
        print(f"  {day:>4}{last_feed_day[day]:>7}   {100.0 * last_feed_day[day] / tot:>5.1f}%")
    print()
    print("FEEDS EMITTED PER DAY (mean over seats), against pens standing")
    print(f"  {'day':>4}{'feeds':>8}{'pens':>8}{'share fed':>11}")
    for day in sorted(feeds):
        fv = feeds[day]
        pv = pens.get(day) or [0]
        mf, mp = sum(fv) / len(fv), sum(pv) / len(pv)
        print(f"  {day:>4}{mf:>8.2f}{mp:>8.2f}{(mf / mp if mp else 0):>10.1%}")


if __name__ == "__main__":
    main()
