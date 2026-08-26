"""Every weed that appears: was it our own dry crop, or a spawn on bare ground?

Alex: *"is this from not watering or something else??"*, on
`d0-d14 weed-days per seat: kawa 0.0, ours 1.7`.

A tile becomes a WEED two ways, and they are not the same defect:

    our own      a crop tile that went two nights without water. `_daily_refresh_crops` replaces it
                 when `consecutive_unwatered >= 2` (`reference/kaggriculture.py:771`). The crop is
                 destroyed, the square is blocked, and clearing it costs a DIG turn. **This is a
                 missed water and nothing else.**
    spawn        the town seeding bare ground at `weedSpawnChance`, 0.005 on the ladder. Nobody's
                 fault, and unavoidable.

Classified by looking at the SAME tile on the previous day:

    prev is a crop with consecutive_unwatered >= 1   -> our own dry crop (it was on the brink and
                                                       tonight was the second night)
    prev is a crop with consecutive_unwatered == 0   -> a crop that weeded without warning, which
                                                       should be impossible; counted separately so a
                                                       bad reading shows up rather than hiding
    prev is not a crop                               -> spawn

Read at the last turn of each day, so the state is post-rollover and the transition is one night.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
US = "alex chilton"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")


def dusk_boards(replay, seat):
    """`{day: tiles}` at the last turn of each day."""
    out = {}
    for t, step in enumerate(replay.get("steps") or []):
        if t % TPD != TPD - 1:
            continue
        farms = ((step[0] or {}).get("observation") or {}).get("farms") or []
        if seat < len(farms):
            out[t // TPD] = farms[seat].get("tiles") or []
    return out


def classify(replay, seat):
    boards = dusk_boards(replay, seat)
    c = collections.Counter()
    per_day = collections.defaultdict(collections.Counter)
    days = sorted(boards)
    for i in range(1, len(days)):
        day, prev_day = days[i], days[i - 1]
        cur, prev = boards[day], boards[prev_day]
        for y, row in enumerate(cur):
            for x, cell in enumerate(row):
                if not isinstance(cell, dict) or cell.get("kind") != "WEED":
                    continue
                p = prev[y][x] if y < len(prev) and x < len(prev[y]) else None
                if isinstance(p, dict) and p.get("kind") == "WEED":
                    continue                          # already there; count each weed once
                if isinstance(p, dict) and p.get("crop"):
                    dry = int(p.get("consecutive_unwatered", 0) or 0)
                    key = "dry_crop" if dry >= 1 else "crop_no_warning"
                else:
                    key = "spawn"
                c[key] += 1
                per_day[day][key] += 1
    return c, per_day


def run(pairs, label):
    tot = collections.Counter()
    per_day = collections.defaultdict(collections.Counter)
    n = 0
    for replay, seat in pairs:
        n += 1
        c, pd = classify(replay, seat)
        tot.update(c)
        for d, cc in pd.items():
            per_day[d].update(cc)
    if not n:
        print(f"{label}: no seats"); return
    print(f"{label}   ({n} seats)")
    print(f"   {'day':>5}{'dry crop':>11}{'spawn':>9}{'no warning':>13}")
    for d in sorted(per_day):
        r = per_day[d]
        print(f"   {d:>5}{r['dry_crop']/n:>11.2f}{r['spawn']/n:>9.2f}"
              f"{r['crop_no_warning']/n:>13.2f}")
    for lo, hi in ((0, 14), (0, 21), (12, 15)):
        s = collections.Counter()
        for d in range(lo, hi + 1):
            s.update(per_day[d])
        print(f"   d{lo}-d{hi} per seat:  OUR OWN DRY CROP {s['dry_crop']/n:>6.2f}   "
              f"spawn {s['spawn']/n:>5.2f}   no-warning {s['crop_no_warning']/n:>5.2f}")
    print()


def main(our_files):
    kawa = []
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:60]:
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA in names:
                kawa.append((r, names.index(KAWA)))
    ours = []
    for path in our_files:
        f = pathlib.Path(path)
        if f.name.startswith("_"):
            continue
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        ours.append((r, names.index(US) if US in names else 0))
    run(kawa, "KAWASHIGI")
    run(ours, "OURS")


if __name__ == "__main__":
    main(sys.argv[1:])
