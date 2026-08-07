"""Every number, ours AND the tape's, side by side, for each day. No deltas, no selection.

`scripts/fidelity.py` prints eight scalars as differences, which is right for finding the day a run
parts but wrong for reading what actually happened -- a delta of 0 hides whether both sides had two
cows or twenty, and a summary that shows only the fields that look good is worthless.

This prints the raw pair `ours/tape` for:

    board       money, hands, tiles owned, pens, live crop tiles PER CROP, weeds
    herd        animals standing in a pen PER SPECIES
    shed        units held PER PRODUCT, fertilizer included
    ops         every op either side emitted that day, counted

    python -u scripts/breakdown.py --days 11
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent

TAPES = {
    "seb": ("data/seed_scripts/top_guys/90494364.json",
            "data/seed_scripts/top_guys/90494364/schedule.json", "Seb (allegedly)"),
    "oldleader": ("data/seed_scripts/new_leader/90016067.json",
                  "data/seed_scripts/new_leader/schedule.json", "somewhere after"),
}
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
CROPS = ("WHEAT", "STRAWBERRY", "MELON", "TOMATO", "CARROT")
ANIMALS = ("COW", "SHEEP", "CHICKEN", "GOOSE", "PIG")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
OPS = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
       "DIG", "BUILD", "PLACE", "PICKUP", "DROP", "PASS")


def tape_policy(replay, team, seat_wanted):
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    src = seat if seat_wanted == 0 else 1 - seat
    acts = [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[src] or {} for step in d["steps"][1:])]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    return lambda obs, t: acts[t] if t < len(acts) else idle


def snap(obs, seat):
    farm = obs["farms"][seat]
    n = collections.Counter()
    for r in farm["tiles"]:
        for t in r:
            if t == "LOCKED":
                continue
            n["owned"] += 1
            if not isinstance(t, dict):
                continue
            k = t.get("kind")
            if k == "PLANT":
                n["crop_" + str(t.get("crop"))] += 1
            elif k == "WEED":
                n["weed"] += 1
            else:
                n["pen"] += 1
            if t.get("animal"):
                n["an_" + str(t["animal"])] += 1
    shed = (obs.get("private") or {}).get("shed") or {}
    for p in PRODUCTS:
        n["shed_" + p] = int(shed.get(p, 0) or 0)
    n["money"] = int(farm["money"])
    n["hands"] = len(farm.get("hands") or [])
    return n


def run(make0, opp, seed, weeds):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    days, ops = [], collections.defaultdict(collections.Counter)
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if t % 24 == 0:
            days.append(snap(o0, 0))
        a0, a1 = p0(o0, t), p1(o1, t)
        for a in [a0["farmer"]] + list(a0["hands"] or []):
            if a:
                ops[t // 24][a[0] if a[0] in OPS else "MOVE"] += 1
        for o in (a0["market"] or []):
            if o:
                ops[t // 24][o[0]] += int(o[2]) if len(o) > 2 else 1
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    bad = [(s, env.state[s].status) for s in (0, 1) if env.state[s].status != "DONE"]
    if bad:
        raise RuntimeError(f"seat status {bad}")
    days.append(snap(env.state[0].observation, 0))
    return days, ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=11)
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    his, his_ops = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours, our_ops = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)

    fields = ([("money", "money"), ("hands", "hands"), ("owned", "tiles"), ("pen", "pens"),
               ("weed", "weeds")]
              + [("crop_" + c, c.lower()[:6]) for c in CROPS]
              + [("an_" + x, x.lower()[:6]) for x in ANIMALS]
              + [("shed_" + p, "sh:" + p.lower()[:5]) for p in PRODUCTS])
    live = [(k, lab) for k, lab in fields
            if any(d[k] for d in ours[:args.days + 1]) or any(d[k] for d in his[:args.days + 1])]

    print(f"tape {args.tape}   seed {args.seed}   weeds {args.weeds}   "
          f"CUMULATIVE_SELLS={schedule_agent.CUMULATIVE_SELLS} "
          f"SELL_CARRY_DAYS={schedule_agent.SELL_CARRY_DAYS}")
    print("\n  board, herd and shed at DAWN -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    for k, lab in live:
        cells = "".join(f"{str(ours[d][k]) + '/' + str(his[d][k]):>13}" for d in range(args.days)
                        if d < len(ours) and d < len(his))
        print(f"  {lab:<12}{cells}")

    print("\n  ops emitted that day -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    seen = [o for o in OPS + ("MOVE", "SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL",
                              "BUY_LAND", "HIRE")
            if any(our_ops[d][o] or his_ops[d][o] for d in range(args.days))]
    for o in seen:
        cells = "".join(f"{str(our_ops[d][o]) + '/' + str(his_ops[d][o]):>13}"
                        for d in range(args.days))
        print(f"  {o.lower()[:12]:<12}{cells}")


if __name__ == "__main__":
    main()