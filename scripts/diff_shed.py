"""Shed contents item by item at each dawn, ours against the tape's, plus the day's op census.

`tests/test_the_farm_matches_the_tape_day_by_day.py` reports `day 1: shed 14 against the tape's 16` --
a total, which does not say which item or which op failed to produce it. And the shed drives the money
column downstream: the sell orders match the tape's exactly, so a shed two units short cannot fill
them, and the shortfall compounds into `day 3: money 45 against the tape's 217`.

Prints per day: our shed and the tape's, the item-level difference, and the ops each side ran that day
so a missing item can be traced to a missing op rather than guessed at.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan, routines as R
import build_script_submission as B

TPD = R.TURNS_PER_DAY
REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"


def tape_side():
    """The tape's own shed at each dawn, and its op census per day."""
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    shed, ops = {}, collections.defaultdict(collections.Counter)
    for t, step in enumerate(d["steps"][1:]):
        day, hour = divmod(t, TPD)
        s = step[seat] or {}
        obs = s.get("observation") or {}
        if hour == 0:
            shed[day] = dict((obs.get("private") or {}).get("shed") or {})
        a = s.get("action") or {}
        for op in [a.get("farmer")] + list(a.get("hands") or []):
            if op:
                ops[day][op[0]] += 1
    return shed, ops


def our_side():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)
    shed, ops = {}, collections.defaultdict(collections.Counter)
    for t in range(len(plan)):
        day, hour = divmod(t, TPD)
        st = env.state[0].observation
        if hour == 0:
            shed[day] = dict((st["private"] or {}).get("shed") or {})
        farmer, hands_, market = plan[t]
        n = len(st["farms"][0].get("hands") or [])
        for a in [farmer] + list(hands_[:n]):
            if a and a[0] != "PASS":
                ops[day][a[0]] += 1
        env.step([{"farmer": farmer, "hands": hands_[:n], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break
    return shed, ops


def main():
    a_shed, a_ops = tape_side()
    b_shed, b_ops = our_side()
    for day in range(0, 14):
        if day not in a_shed or day not in b_shed:
            continue
        A, Bd = collections.Counter(a_shed[day]), collections.Counter(b_shed[day])
        if A == Bd:
            print(f"day {day:2d}  shed exact ({sum(A.values())})")
            continue
        short = A - Bd
        over = Bd - A
        print(f"day {day:2d}  ours {sum(Bd.values()):>3} against {sum(A.values()):>3}   "
              f"short {dict(short) or '-'}   over {dict(over) or '-'}")
        if day == 0:
            continue
        pa, pb = a_ops[day - 1], b_ops[day - 1]
        keys = sorted(set(pa) | set(pb))
        print(f"          day {day - 1} ops:  " + "  ".join(
            f"{k}{pb[k]}/{pa[k]}" for k in keys if pb[k] != pa[k]))


if __name__ == "__main__":
    main()
