"""Every big thing, every day of the season, ours minus the tape's -- one grid, thirty columns.

Days 0 to 3 have been compared parameter by parameter and the animals now match exactly on days 1, 2
and 3. That says nothing about day 17. A farm can be identical for a week and then quietly diverge on
the day a quadrant is bought, a crop rotation turns over, or the shed fills, and a season total will
average that away into a percentage that looks like a uniform shortfall when it is actually a cliff.

So this prints a matrix: one row per measurable, one column per day, each cell `ours - tape`. A dot is
an exact match. What matters is the shape of a row -- a row of dots with a blot in it is a specific day
to go and read, which is a different investigation from a row that is wrong everywhere.

Rows are grouped by the question they answer:

    herd        alive, pens, placed, escaped        do we keep the same animals, and get them equally early
    field       crop tiles, planted, weeds, lost    do we farm the same ground
    care        WATER, FERTILIZE, COLLECT, DIG      do we maintain it the same way
    animals     FEED, CARE                          do we work the herd the same way
    money       bank at dawn                        the consequence

`fert` counts tiles standing under an active fertilizer bonus at dawn, which is the state that actually
pays -- FERTILIZE ops say what was spent, not what was live when the water landed.
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import router as RT
from kagg.search import schedule_agent
import agent_ladder as L

OPS = ("PLANT", "WATER", "FERTILIZE", "COLLECT_FERTILIZER", "HARVEST", "FEED", "CARE",
       "PLACE", "BUILD_PASTURE", "BUILD_COOP", "DIG", "DROP", "PICKUP")

ROWS = [
    ("herd", [("alive", "animals alive"), ("pens", "pens standing"),
              ("PLACE", "animals placed"), ("escaped", "animals escaped")]),
    ("field", [("crops", "crop tiles"), ("PLANT", "planted"),
               ("weeds", "weeds standing"), ("lost", "crops lost to weeds")]),
    ("care", [("WATER", "watered"), ("FERTILIZE", "fertilized"), ("fert", "tiles under fertilizer"),
              ("COLLECT_FERTILIZER", "fertilizer collected"), ("DIG", "dug")]),
    ("work", [("FEED", "fed"), ("CARE", "cared"), ("HARVEST", "harvested"),
              ("PICKUP", "shed draws"), ("DROP", "shed drops")]),
    ("money", [("money", "bank at dawn ($100s)")]),
]


def run(seed, weeds, make_us=None, tape=None, theirs=None):
    env = L._env(seed, weeds)
    us = make_us() if make_us else None
    rows = collections.defaultdict(collections.Counter)
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        farm = obs["farms"][0]
        tiles = farm["tiles"]
        if hour == 0:
            cells = [c for row in tiles for c in row if isinstance(c, dict)]
            rows[day].update(
                alive=sum(1 for c in cells if "animal" in c),
                pens=sum(1 for c in cells if c.get("kind") in ("PASTURE", "COOP") or "animal" in c),
                crops=sum(1 for c in cells if c.get("kind") == "PLANT"),
                weeds=sum(1 for c in cells if c.get("kind") == "WEED"),
                fert=sum(1 for c in cells if c.get("fertilized_until_day", -1) >= day),
                money=int(farm["money"]) // 100,
            )
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        n0 = len(farm.get("hands") or [])
        for act in [f0, *list(h0)[:n0]]:
            if isinstance(act, list) and act and act[0] in OPS:
                rows[day][act[0]] += 1
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    for d in sorted(rows):
        prev = rows.get(d - 1)
        if prev is None:
            continue
        # `alive` can only fall by escape, and `weeds` can only rise from a crop that went two days dry.
        rows[d]["escaped"] = max(0, prev["alive"] + prev["PLACE"] - rows[d]["alive"])
        rows[d]["lost"] = max(0, rows[d]["weeds"] - prev["weeds"])
    return rows, float(env.state[0].observation["farms"][0]["money"])


def cell(d):
    if d == 0:
        return "  ."
    if abs(d) > 99:
        return "+++" if d > 0 else "---"
    return f"{d:>+3}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", nargs="?", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    args = ap.parse_args()

    mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_rows, tape_money = run(args.seed, args.weeds, tape=mine, theirs=theirs)
    our_rows, our_money = run(args.seed, args.weeds,
                              make_us=lambda: schedule_agent.make_agent(sched, 0, router=True),
                              theirs=theirs)
    days = sorted(set(our_rows) | set(tape_rows))

    print(f"seed {args.seed}   weeds {args.weeds}   tape ${tape_money:,.0f}   ours ${our_money:,.0f} "
          f"({100 * our_money / tape_money:.0f}%)\n")
    print(f"{'':<24}" + "".join(f"{d:>3}" for d in days) + f"{'equal':>8}{'ours':>8}{'tape':>8}")
    for group, metrics in ROWS:
        print(f"  -- {group}")
        for key, label in metrics:
            diffs = [int(our_rows[d][key]) - int(tape_rows[d][key]) for d in days]
            o = sum(int(our_rows[d][key]) for d in days)
            t = sum(int(tape_rows[d][key]) for d in days)
            eq = sum(1 for x in diffs if x == 0)
            print(f"  {label:<22}" + "".join(cell(x) for x in diffs)
                  + f"{eq:>5}/{len(days):<2}{o:>8}{t:>8}")
    print("\n  a dot is an exact match for that day; the number is ours minus the tape's")


if __name__ == "__main__":
    main()
