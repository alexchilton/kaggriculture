"""Does the SCHEDULE ask for as many plants as the tape made, or does the executor under-deliver?

The harvest gap traced back to planted area: from day 7 we carry 11-26 fewer crop tiles than the
tape all season, on land we already own (`tiles_owned` matches exactly through the day-5 purchase).
Two completely different bugs produce that, and they need opposite fixes:

    the schedule under-asks     `dayplan`/the extractor lost plantings on the way out of the tape.
                                Nothing the executor does can recover them.
    the executor under-delivers the `plants` rows are right and `_refresh_pins` / `_live_ops` /
                                the seed order refuse to turn them into PLANT ops.

Column 1 (schedule) needs no simulation at all -- it is the extracted plan read straight off disk
against the tape's own recorded PLANT actions. Only if those agree is a run needed.

    python -u scripts/why_the_land_is_bare.py
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

TAPES = [
    ("leader", "data/seed_scripts/new_leader/90016067.json",
     "data/seed_scripts/new_leader/schedule.json", "somewhere after"),
    ("seb", "data/seed_scripts/top_guys/90494364.json",
     "data/seed_scripts/top_guys/90494364/schedule.json", "Seb (allegedly)"),
]


def tape_plants(replay, team):
    """PLANT actions per day in the tape, for `team`'s seat. Farmer and hands both count."""
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    per_day = collections.Counter()
    crops = collections.Counter()
    for t, step in enumerate(d["steps"][1:]):
        act = (step[seat] or {}).get("action") or {}
        for a in [act.get("farmer") or ["PASS"]] + list(act.get("hands") or []):
            if a and a[0] == "PLANT":
                per_day[t // 24] += 1
                crops[a[1] if len(a) > 1 else "?"] += 1
    return per_day, crops


def sched_plants(schedule):
    """`plants` rows per day in the extracted schedule."""
    s = json.loads(pathlib.Path(schedule).read_text())
    per_day, crops = collections.Counter(), collections.Counter()
    for k, row in s.items():
        for c in (row.get("plants") or []):
            per_day[int(k)] += 1
            crops[c] += 1
    return per_day, crops


def main():
    for name, replay, schedule, team in TAPES:
        if not pathlib.Path(schedule).exists():
            print(f"{name}: no schedule at {schedule}\n")
            continue
        tp, tc = tape_plants(replay, team)
        sp, sc = sched_plants(schedule)
        print(f"== {name}   {pathlib.Path(replay).name}   plants per day, schedule vs tape\n")
        print(f"  {'day':>5}{'schedule':>10}{'tape':>8}{'delta':>8}"
              f"{'sched cum':>11}{'tape cum':>10}")
        cs = ct = 0
        for d in range(31):
            if not (sp[d] or tp[d]):
                continue
            cs += sp[d]
            ct += tp[d]
            print(f"  {d:>5}{sp[d]:>10}{tp[d]:>8}{sp[d] - tp[d]:>+8d}{cs:>11}{ct:>10}")
        print(f"\n  season   schedule {sum(sp.values()):>4}   tape {sum(tp.values()):>4}")
        print("\n  by crop" + "".join(f"{c[:6]:>9}" for c in sorted(set(sc) | set(tc))))
        print("  sched  " + "".join(f"{sc[c]:>9}" for c in sorted(set(sc) | set(tc))))
        print("  tape   " + "".join(f"{tc[c]:>9}" for c in sorted(set(sc) | set(tc))))
        print()


if __name__ == "__main__":
    main()