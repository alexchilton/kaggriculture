"""A weed is not one event. It is a dead square for every day that follows it.

Alex, 2026-08-26: *"you forget the lessons tho - a 1 op miss is cumulative dude...or a 1 plant miss
is also or a 1 weed unexpected"*. He is right, and `CLAUDE.md` says it already: *"Never say a
mismatch is 'small'. 40/41 a day compounds."*

`data/logs/weed_source.log` measured the CREATION rate and found it equal -- 1.35 weeds per seat for
us against 1.33 for him over d0-d21 -- and that was reported as closing the question. It does not.
The rates are equal and the TIMING is not:

    kawa   first missed-water weed on d15. Nothing at all in d0-d14, over 15 seats.
    ours   weeds from d3, steady from d7. 0.63 per seat already on the board by d14.

A tile that weeds on d7 is dead for 22 days. The same tile weeding on d22 costs 7. So this counts
the thing that actually compounds:

    tile-days lost      for each weed, the days between it appearing and either being cleared
                        (DIG, or the square becoming something else) or the season ending
    days to clear       how long a weed sits before we deal with it
    replanted           whether the square was put back to work afterwards -- a weed that is dug and
                        re-sown on the next day costs two turns, one that sits until d29 costs the
                        whole remainder

Read at dusk each day, so a tile that appears and is cleared inside one day is not counted -- that
undercounts us, which is the safe direction for a claim that we lose more than he does.
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
LAST = 29


def dusk(replay, seat):
    out = {}
    for t, step in enumerate(replay.get("steps") or []):
        if t % TPD != TPD - 1:
            continue
        farms = ((step[0] or {}).get("observation") or {}).get("farms") or []
        if seat < len(farms):
            out[t // TPD] = farms[seat].get("tiles") or []
    return out


def episodes(replay, seat):
    """One row per weed: (day_it_appeared, days_it_stood, was_replanted)."""
    boards = dusk(replay, seat)
    days = sorted(boards)
    if not days:
        return []
    def kind(d, y, x):
        b = boards[d]
        c = b[y][x] if y < len(b) and x < len(b[y]) else None
        return c if isinstance(c, dict) else None
    rows, open_weed = [], {}
    for d in days:
        b = boards[d]
        for y, row in enumerate(b):
            for x, cell in enumerate(row):
                is_weed = isinstance(cell, dict) and cell.get("kind") == "WEED"
                key = (y, x)
                if is_weed and key not in open_weed:
                    open_weed[key] = d
                elif not is_weed and key in open_weed:
                    start = open_weed.pop(key)
                    after = kind(d, y, x)
                    rows.append((start, d - start, bool(after and after.get("crop"))))
    for key, start in open_weed.items():          # never cleared: stands to the bell
        rows.append((start, LAST - start, False))
    return rows


def report(label, pairs):
    if not pairs:
        print(f"{label}: no seats"); return
    n = len(pairs)
    rows = []
    for replay, seat in pairs:
        rows.extend(episodes(replay, seat))
    if not rows:
        print(f"{label}   ({n} seats): no weeds at all\n"); return
    early = [r for r in rows if r[0] <= 14]
    mid = [r for r in rows if 15 <= r[0] <= 23]
    late = [r for r in rows if r[0] >= 24]
    print(f"{label}   ({n} seats)")
    print(f"   weeds per seat            {len(rows)/n:>7.2f}")
    print(f"   TILE-DAYS LOST per seat   {sum(r[1] for r in rows)/n:>7.2f}")
    print(f"   mean days standing        {sum(r[1] for r in rows)/len(rows):>7.2f}")
    print(f"   replanted afterwards      {100*sum(r[2] for r in rows)/len(rows):>6.1f}%")
    for tag, grp in (("d0-d14 ", early), ("d15-d23", mid), ("d24+   ", late)):
        if grp:
            print(f"   {tag}  {len(grp)/n:>5.2f}/seat   "
                  f"{sum(r[1] for r in grp)/n:>6.2f} tile-days   "
                  f"stands {sum(r[1] for r in grp)/len(grp):>5.1f} days")
        else:
            print(f"   {tag}  {0:>5.2f}/seat")
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
    report("KAWASHIGI", kawa)
    report("OURS", ours)


if __name__ == "__main__":
    main(sys.argv[1:])
