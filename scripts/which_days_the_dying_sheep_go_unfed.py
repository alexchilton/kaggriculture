"""For each sheep カワシギ loses, which days did that pen actually go unfed?

Alex: "u didnt check" -- and he is right. The previous claim was that he stops feeding at d27, and
what was measured is only that his last day with any FEED is d28. d27 was then inferred from the
escape rule (`consecutive_unfed >= 2`, `kaggriculture.py:817`). That inference does not follow: the
same tape feeds only 56-90% of its pens on most days from d13 onward and loses nothing, so a pen
being unfed on d27 says nothing about whether it is one of the pens that dies.

`consecutive_unfed` is carried on the tile in the observation, so the trajectory of each individual
pen is readable directly -- no inference, no attributing FEED ops to tiles.

Per seat, per sheep tile, this walks the last turn of each day and records `consecutive_unfed`.
A pen that vanishes is followed back to the last day it was standing.

Printed:
    for the sheep that DIE      -- the day their counter first goes to 1, and the day it reaches 2
    for the sheep that SURVIVE  -- how high their counter ever gets, so a cadence that runs at 1 all
                                  season is distinguishable from a pen that is fed every day
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
    first_one = collections.Counter()      # day the counter first hits 1, for pens that die
    hit_two = collections.Counter()        # day the counter reaches 2 (the escape)
    last_seen = collections.Counter()      # last day the dying pen is on the board
    surv_max = collections.Counter()       # highest counter a SURVIVING sheep ever reaches
    n_die = n_live = n_seats = 0
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
            n_seats += 1
            steps = r.get("steps") or []
            # tile -> {day: consecutive_unfed} for every day the tile holds a SHEEP
            track = collections.defaultdict(dict)
            for t in range(TPD - 1, len(steps), TPD):
                day = t // TPD
                farms = ((steps[t][0] or {}).get("observation") or {}).get("farms") or []
                if seat >= len(farms):
                    continue
                for y, row in enumerate(farms[seat].get("tiles") or []):
                    for x, tile in enumerate(row):
                        if isinstance(tile, dict) and tile.get("animal") == "SHEEP":
                            track[(y, x)][day] = int(tile.get("consecutive_unfed", 0))
            days_all = sorted({dd for v in track.values() for dd in v})
            if not days_all:
                continue
            end = days_all[-1]
            for tile, series in track.items():
                ds = sorted(series)
                if ds[-1] < end:                       # the pen vanished before the bell
                    n_die += 1
                    last_seen[ds[-1]] += 1
                    ones = [dd for dd in ds if series[dd] >= 1]
                    twos = [dd for dd in ds if series[dd] >= 2]
                    if ones:
                        first_one[ones[0]] += 1
                    if twos:
                        hit_two[twos[0]] += 1
                else:
                    n_live += 1
                    surv_max[max(series.values())] += 1

    print(f"kawa post-change seats: {n_seats}", flush=True)
    print(f"sheep pens that vanish: {n_die}   pens that survive: {n_live}")
    print()
    print("DYING SHEEP -- first day `consecutive_unfed` reaches 1 (the first missed feed)")
    print(f"  {'day':>4}{'pens':>7}   share")
    tot = sum(first_one.values()) or 1
    for day in sorted(first_one):
        print(f"  {day:>4}{first_one[day]:>7}   {100.0 * first_one[day] / tot:>5.1f}%")
    print()
    print("DYING SHEEP -- last day the pen is still on the board")
    print(f"  {'day':>4}{'pens':>7}   share")
    tot = sum(last_seen.values()) or 1
    for day in sorted(last_seen):
        print(f"  {day:>4}{last_seen[day]:>7}   {100.0 * last_seen[day] / tot:>5.1f}%")
    print()
    print("SURVIVING SHEEP -- highest `consecutive_unfed` ever reached")
    print(f"  {'max':>4}{'pens':>7}   share")
    tot = sum(surv_max.values()) or 1
    for k in sorted(surv_max):
        print(f"  {k:>4}{surv_max[k]:>7}   {100.0 * surv_max[k] / tot:>5.1f}%")
    print()
    print("Reading: if the dying pens' first missed feed clusters on ONE day, that day is his stop.")
    print("If surviving pens also sit at 1 regularly, the cadence is real and 'unfed' alone proves")
    print("nothing -- only the SECOND consecutive miss does.")


if __name__ == "__main__":
    main()
