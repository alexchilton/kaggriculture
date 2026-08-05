"""The leader's schedule, read off his tape, as the ground truth our scheduler must be diffed against.

Alex's question, and it is the one that has been missing all along: **what should the schedule be?**
Every judgement in this project so far has compared our output against a number I inferred from his
replay -- 14 pens, land on 7 and 10, 12 hands -- and inferences are where the errors came from. His
720-turn tape contains the actual schedule. This extracts it.

What a "schedule" is, precisely: for each day, what capacity comes online and what it cost.

    BUILD_PASTURE / BUILD_COOP   a pen is raised on a tile
    PLACE                        an animal goes into it
    BUY_ANIMAL                   the animal is paid for
    PLANT                        a crop tile comes online
    BUY_LAND                     a quadrant unlocks
    HIRE                         the crew for that day
    money at dawn                what all of it had to be funded from

Two outputs. A human-readable table, and a JSON `data/seed_scripts/new_leader/schedule.json` that a
diff can be written against, so "does our schedule match his" becomes a test rather than an opinion.

Note on turns: the raw tape is 720 steps over 30 days, so 24 turns a day, and turn 0 of each day is the
market phase. `routines.TURNS_PER_DAY` is the same 24 with 23 work turns.
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

ap = argparse.ArgumentParser()
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--team", default="somewhere after")
ap.add_argument("--out", default="data/seed_scripts/new_leader/schedule.json")
args = ap.parse_args()

TD = 24
BUILD = {"BUILD_PASTURE", "BUILD_COOP"}

d = json.load(open(args.replay))
seat = d["info"]["TeamNames"].index(args.team)

day_rows = collections.defaultdict(lambda: dict(
    builds=[], places=[], plants=[], animals_bought=collections.Counter(),
    seeds=collections.Counter(), land=0, hires=0, sells=collections.Counter(),
    buys=collections.Counter(), money_dawn=None, hands=0))

for t, step in enumerate(d["steps"]):
    day, hour = divmod(t, TD)
    row = day_rows[day]
    s = step[seat] or {}
    obs = s.get("observation") or {}
    farms = obs.get("farms") or []
    if hour == 0 and len(farms) > seat:
        row["money_dawn"] = float(farms[seat]["money"])
    if len(farms) > seat:
        row["hands"] = max(row["hands"], len(farms[seat].get("hands") or []))

    a = s.get("action") or {}
    ops = [a.get("farmer")] + list(a.get("hands") or [])
    for op in ops:
        if not op:
            continue
        if op[0] in BUILD:
            row["builds"].append(op[0])
        elif op[0] == "PLACE":
            row["places"].append(op[1] if len(op) > 1 else "?")
        elif op[0] == "PLANT":
            row["plants"].append(op[1] if len(op) > 1 else "?")
    for o in (a.get("market") or []):
        if not o:
            continue
        n = int(o[2]) if len(o) > 2 else 1
        if o[0] == "BUY_ANIMAL":
            row["animals_bought"][o[1]] += n
        elif o[0] == "BUY_SEED":
            row["seeds"][o[1]] += n
        elif o[0] == "BUY_PRODUCT":
            row["buys"][o[1]] += n
        elif o[0] == "SELL":
            row["sells"][o[1]] += n
        elif o[0] == "BUY_LAND":
            row["land"] += 1
        elif o[0] == "HIRE":
            row["hires"] += 1

n_days = max(day_rows) + 1
print("=" * 118)
print(f"THE LEADER'S SCHEDULE -- {args.team}, episode {pathlib.Path(args.replay).stem}")
print("=" * 118)
print(f"{'day':>4} {'dawn $':>9} {'hands':>6} {'hire':>5} {'land':>5} | "
      f"{'built':>6} {'placed':>6} {'animals bought':>22} | {'planted':>8} {'seeds':>6} | "
      f"{'wheat buy':>10} {'sold units':>11}")

cum_pens = cum_tiles = 0
for day in range(n_days):
    r = day_rows[day]
    cum_pens += len(r["places"])
    cum_tiles += len(r["plants"])
    animals = " ".join(f"{k}x{v}" for k, v in sorted(r["animals_bought"].items())) or ""
    print(f"{day:>4} {(r['money_dawn'] if r['money_dawn'] is not None else 0):>9,.0f} "
          f"{r['hands']:>6} {r['hires']:>5} {r['land']:>5} | "
          f"{len(r['builds']):>6} {len(r['places']):>6} {animals:>22} | "
          f"{len(r['plants']):>8} {sum(r['seeds'].values()):>6} | "
          f"{r['buys'].get('WHEAT', 0):>10} {sum(r['sells'].values()):>11}")

print()
print(f"{'cumulative':>14}: {cum_pens} pens placed, {cum_tiles} tile-plantings, "
      f"land bought on days {[dd for dd in range(n_days) if day_rows[dd]['land']]}")
print(f"{'peak crew':>14}: {max(r['hands'] for r in day_rows.values())} hands")
print(f"{'first pen':>14}: day {min((dd for dd in range(n_days) if day_rows[dd]['places']), default=-1)}")
print(f"{'first plant':>14}: day {min((dd for dd in range(n_days) if day_rows[dd]['plants']), default=-1)}")

out = {str(day): dict(
    money_dawn=day_rows[day]["money_dawn"],
    hands=day_rows[day]["hands"],
    hires=day_rows[day]["hires"],
    land=day_rows[day]["land"],
    builds=len(day_rows[day]["builds"]),
    places=day_rows[day]["places"],
    plants=day_rows[day]["plants"],
    animals_bought=dict(day_rows[day]["animals_bought"]),
    seeds=dict(day_rows[day]["seeds"]),
    buys=dict(day_rows[day]["buys"]),
    sells=dict(day_rows[day]["sells"]),
) for day in range(n_days)}
pathlib.Path(args.out).write_text(json.dumps(out, indent=1))
print()
print(f"wrote {args.out} -- the target a generated schedule can be diffed against")
