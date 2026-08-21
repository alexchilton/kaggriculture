"""He left tiles empty and could afford the seed. Could he have REACHED them?

`is_the_middle_capacity.py` shows Kawashigi ends 91.8% of mid-season days with empty unlocked
tiles on the board -- a mean of 7.48 -- and that in 100% of those days his dawn bank covered a
WHEAT seed ($10) for every one of them. Two objections remain, and both are about turns, not tiles:

  1. He may have had no spare unit-turns. A PLANT costs an action and the walk to get there.
  2. The tiles may have opened too late in the day to be worth a trip.

This counts the work he actually did, per unit-turn, straight off the recorded actions. A unit-turn
is one unit acting on one hour, so the day's budget is `units * 24`. `PASS` and a missing action are
idle; NORTH/SOUTH/EAST/WEST are travel; everything else is work.

If the idle count alone exceeds the tiles left empty at dusk, reachability cannot be the
explanation: he had units standing still while plantable, affordable ground sat empty.

    python -u scripts/did_he_have_the_turns.py --lo 14 --hi 27
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TURNS_PER_DAY = 24
TRAVEL = frozenset(("NORTH", "SOUTH", "EAST", "WEST"))


def index_replays():
    idx = {}
    for p in glob.glob(str(REPO / "data/seed_scripts/**/*.json"), recursive=True):
        idx.setdefault(pathlib.Path(p).stem, p)
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default="data/target_rows_kawa_norm.json")
    ap.add_argument("--lo", type=int, default=14)
    ap.add_argument("--hi", type=int, default=27)
    a = ap.parse_args()

    rows = json.loads((REPO / a.targets).read_text())
    seats = {(r["game"], r["seat"]) for r in rows}
    idx = index_replays()

    per_day = collections.defaultdict(list)
    for game, seat in sorted(seats):
        path = idx.get(game)
        if not path:
            continue
        rep = json.loads(pathlib.Path(path).read_text())
        acc = {}
        for step in rep.get("steps") or []:
            if seat >= len(step):
                continue
            cell = step[seat]
            obs = cell.get("observation") or {}
            day = int(obs.get("day", 0) or 0)
            hour = int(obs.get("hour", 0) or 0)
            if day < a.lo or day > a.hi:
                continue
            rec = acc.setdefault(day, {"idle": 0, "travel": 0, "work": 0, "plant": 0,
                                       "water": 0, "budget": 0, "turns": 0, "dusk": 0})
            act = cell.get("action")
            farms = obs.get("farms") or []
            farm = farms[seat] if seat < len(farms) else {}
            if hour == TURNS_PER_DAY - 1:
                rec["dusk"] = sum(1 for r in farm.get("tiles") or [] for t in r if t is None)
            if act is None:
                continue
            rec["turns"] += 1
            units = [act.get("farmer")] + list(act.get("hands") or [])
            # The crew is whatever the action drives; a unit that exists always gets a slot.
            rec["budget"] += len(units)
            for u in units:
                op = str(u[0]) if u else "PASS"
                if op == "PASS":
                    rec["idle"] += 1
                elif op in TRAVEL:
                    rec["travel"] += 1
                else:
                    rec["work"] += 1
                    if op == "PLANT":
                        rec["plant"] += 1
                    elif op == "WATER":
                        rec["water"] += 1
        for day, rec in acc.items():
            if rec["turns"] == TURNS_PER_DAY:
                per_day[day].append(rec)

    print("Unit-turns per day. budget = units * 24. idle = PASS.\n")
    print("%4s %5s %8s %8s %8s %8s %7s %7s %9s %10s"
          % ("day", "n", "budget", "idle", "travel", "work", "plant", "water", "dusk", "idle>dusk"))
    tot = collections.Counter()
    allrecs = []
    for day in sorted(per_day):
        rs = per_day[day]
        k = len(rs)
        allrecs += rs

        def m(f):
            return sum(r[f] for r in rs) / k
        beats = 100.0 * sum(1 for r in rs if r["idle"] > r["dusk"]) / k
        print("%4d %5d %8.1f %8.1f %8.1f %8.1f %7.2f %7.2f %9.2f %9.1f%%"
              % (day, k, m("budget"), m("idle"), m("travel"), m("work"), m("plant"), m("water"),
                 m("dusk"), beats))
        for f in ("budget", "idle", "travel", "work", "plant", "water", "dusk"):
            tot[f] += sum(r[f] for r in rs)

    n = len(allrecs)
    print("\nPOOLED d%d-d%d, %d day-rows" % (a.lo, a.hi, n))
    print("  mean idle unit-turns per day        %.2f" % (tot["idle"] / n))
    print("  mean tiles empty at dusk            %.2f" % (tot["dusk"] / n))
    print("  idle turns >= tiles left empty      %.1f%% of days"
          % (100.0 * sum(1 for r in allrecs if r["idle"] >= r["dusk"]) / n))
    print("  idle turns >= 2x tiles left empty   %.1f%% of days"
          % (100.0 * sum(1 for r in allrecs if r["idle"] >= 2 * r["dusk"]) / n))
    print("  days with ZERO idle turns           %.1f%%"
          % (100.0 * sum(1 for r in allrecs if r["idle"] == 0) / n))
    print("  idle share of budget                %.1f%%" % (100.0 * tot["idle"] / tot["budget"]))
    print("  travel share of budget              %.1f%%" % (100.0 * tot["travel"] / tot["budget"]))
    print("  WATER share of all work             %.1f%%" % (100.0 * tot["water"] / tot["work"]))
    print("  PLANT share of all work             %.1f%%" % (100.0 * tot["plant"] / tot["work"]))


if __name__ == "__main__":
    main()
