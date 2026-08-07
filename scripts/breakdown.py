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
    # Downloaded 2026-08-07 21:16. Seb WINS this one 143,772 to Leon Christians' 127,114 and holds all
    # four quadrants to Leon's three. A materially more aggressive plan than `seb` below: land on days
    # 4, 6 and 10 against 5, 9 and 11, and 23 pens against ~15.
    # Its `configuration` records `townCenterSellInterval = 12`, i.e. it was played on the PRE-rebalance
    # economy -- same as the ladder, which had not picked up 1.32.6 as of that evening. Check that field
    # on any future download before trusting a comparison against it.
    "seb2": ("data/seed_scripts/top_guys/90751101.json",
             "data/seed_scripts/top_guys/90751101/schedule.json", "Seb (allegedly)"),
    "seb": ("data/seed_scripts/top_guys/90494364.json",
            "data/seed_scripts/top_guys/90494364/schedule.json", "Seb (allegedly)"),
    "oldleader": ("data/seed_scripts/new_leader/90016067.json",
                  "data/seed_scripts/new_leader/schedule.json", "somewhere after"),
}
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
CROPS = ("WHEAT", "STRAWBERRY", "MELON", "TOMATO", "CARROT")
ANIMALS = ("COW", "SHEEP", "CHICKEN", "GOOSE", "PIG")
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
#: The env's unit vocabulary, read off `reference/kaggriculture.py` rather than remembered: four
#: `FARMER_MOVES` plus fourteen work ops. This tuple listed `"BUILD"`, which matches nothing -- the
#: real ops are `BUILD_COOP` and `BUILD_PASTURE` -- so every build was falling into the catch-all and
#: being reported as a MOVE. Anything still unrecognised now lands in `OTHER`, loudly, instead of
#: inflating the one row the routing argument rests on.
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
WORK = ("PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
        "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "PICKUP", "DROP")
OPS = WORK + ("PASS",) + MOVES


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
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        # **Count what the env EXECUTES, not what the policy emitted.** `env.step` truncates to the
        # hands actually owned, and a replayed tape can emit more hand slots than it has units --
        # the reference ignores the surplus for movement and work. Counting the untruncated list
        # credited the tape with turns it never took, which is the one number the routing argument
        # divides by. Same list the step below sends, or the comparison is against a fiction.
        for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if a:
                op = a[0]
                ops[t // 24][op if op in OPS else "OTHER"] += 1
                # Turn budget. Every unit that acted spent a turn, and it went to exactly one of three
                # places: walking, working, or nothing. This is the denominator the routing question
                # actually needs -- a raw MOVE count says nothing without the work it bought.
                ops[t // 24]["_turns"] += 1
                ops[t // 24]["_move" if op in MOVES else
                             "_pass" if op == "PASS" else "_work"] += 1
        for o in (a0["market"] or []):
            if o:
                ops[t // 24][o[0]] += int(o[2]) if len(o) > 2 else 1
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
    ap.add_argument("--diff", action="store_true",
                    help="list EVERY field that differs, per day, instead of the wide tables")
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
          f"SELL_CARRY_DAYS={schedule_agent.SELL_CARRY_DAYS} "
          f"HIRE_FIRST={schedule_agent.HIRE_FIRST}")

    if args.diff:
        # Every field that is not identical, per day. The wide tables above are for reading what
        # happened; this is for answering "is it exact yet", where a single unrecorded row is the
        # whole answer and eyeballing a 20x11 grid is how a mismatch gets called a match.
        ops_all = sorted(set(OPS) | {"OTHER", "SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL",
                                     "BUY_LAND", "HIRE"})
        budget = (("_turns", "unit-turns"), ("_work", "work"), ("_move", "move"), ("_pass", "idle"))
        rows = ([("state", lab, [(ours[d][k], his[d][k]) for d in range(args.days)])
                 for k, lab in fields]
                + [("op", o.lower(), [(our_ops[d][o], his_ops[d][o]) for d in range(args.days)])
                   for o in ops_all]
                # Derived: `idle` IS the `pass` op, `move` is the four directions summed, `work` the
                # work ops summed, `unit-turns` all three. Kept because they are the readable summary,
                # flagged because counting them alongside their own parts double-counts the total.
                + [("=sum", lab, [(our_ops[d][k], his_ops[d][k]) for d in range(args.days)])
                   for k, lab in budget])

        live = [(k, lab, c) for k, lab, c in rows if any(o != h for o, h in c)]
        live.sort(key=lambda r: (r[0] == "=sum", -abs(sum(o - h for o, h in r[2]))))
        indep = sum(sum(1 for o, h in c if o != h) for k, lab, c in live if k != "=sum")
        derived = sum(sum(1 for o, h in c if o != h) for k, lab, c in live if k == "=sum")

        print(f"\n  ours MINUS tape, days 0-{args.days - 1}.  blank = identical.\n")
        head = "".join(f"{('d' + str(d)):>7}" for d in range(args.days))
        print(f"  {'field':<20}{head}{'days':>6}{'total':>8}")
        print(f"  {'-' * (20 + 7 * args.days + 14)}")
        for kind, lab, cells in live:
            if kind == "=sum":
                print(f"  {'-' * (20 + 7 * args.days + 14)}")
            body = "".join(f"{'' if o == h else f'{o - h:+d}':>7}" for o, h in cells)
            n = sum(1 for o, h in cells if o != h)
            print(f"  {lab:<20}{body}{n:>6}{sum(o - h for o, h in cells):>+8}")
        print(f"\n  {indep} independent differing cells; the {derived} below the rule are derived "
              f"(idle IS pass, move is n/s/e/w summed, work the work ops, unit-turns all three).")

        # **Exact means zero. There is no "essentially exact".** This verdict exists because the
        # summary written above a table is where a 67-cell gap got called "near-exact" -- twice. A day
        # counts only if EVERY independent field matches, and the headline is the count, not an
        # adjective. If a number has to be described rather than shown, it is not a match.
        per_day = [sum(1 for k, lab, c in live if k != "=sum" and c[d][0] != c[d][1])
                   for d in range(args.days)]
        exact = [d for d, n in enumerate(per_day) if n == 0]
        print("\n  per-day differing cells: "
              + "  ".join(f"d{d}={n}" for d, n in enumerate(per_day)))
        # The denominator matters as much as the count: "67 cells differ" reads very differently
        # against 210 tracked cells than against 80. Fields that are zero on both sides all season
        # are not evidence of agreement, so they are excluded from the base.
        base = [(k, lab, c) for k, lab, c in rows
                if k != "=sum" and any(o or h for o, h in c)]
        cells = len(base) * args.days
        rowsdiff = sum(1 for k, lab, c in base if any(o != h for o, h in c))
        print(f"  VERDICT: {'EXACT' if indep == 0 else 'NOT EXACT'} -- "
              f"{len(exact)}/{args.days} days exact, "
              f"{rowsdiff}/{len(base)} tracked fields differ somewhere, "
              f"{indep}/{cells} cells differ.")
        return
    print("\n  board, herd and shed at DAWN -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    for k, lab in live:
        cells = "".join(f"{str(ours[d][k]) + '/' + str(his[d][k]):>13}" for d in range(args.days)
                        if d < len(ours) and d < len(his))
        print(f"  {lab:<12}{cells}")

    print("\n  ops emitted that day -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    seen = [o for o in OPS + ("OTHER", "SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL",
                              "BUY_LAND", "HIRE")
            if any(our_ops[d][o] or his_ops[d][o] for d in range(args.days))]
    for o in seen:
        cells = "".join(f"{str(our_ops[d][o]) + '/' + str(his_ops[d][o]):>13}"
                        for d in range(args.days))
        print(f"  {o.lower()[:12]:<12}{cells}")

    # Where the day's unit-turns went. `move` on its own is not a verdict: walking to do more work is
    # not the same failure as walking further to do the same work. `mv/wk` separates them -- it is the
    # movement each side paid per unit of work done, so a higher number is strictly worse routing.
    print("\n  turn budget -- ours/tape\n")
    print(f"  {'':<12}" + "".join(f"{('d' + str(d)):>13}" for d in range(args.days)))
    for key, lab in (("_turns", "unit-turns"), ("_work", "work"), ("_move", "move"),
                     ("_pass", "idle")):
        cells = "".join(f"{str(our_ops[d][key]) + '/' + str(his_ops[d][key]):>13}"
                        for d in range(args.days))
        print(f"  {lab:<12}{cells}")
    for lab, src in (("mv/wk", None),):
        cells = ""
        for d in range(args.days):
            o = our_ops[d]["_move"] / max(1, our_ops[d]["_work"])
            h = his_ops[d]["_move"] / max(1, his_ops[d]["_work"])
            cells += f"{f'{o:.2f}/{h:.2f}':>13}"
        print(f"  {lab:<12}{cells}")
    tot = lambda c: (sum(c[d]["_move"] for d in range(args.days)),
                     sum(c[d]["_work"] for d in range(args.days)),
                     sum(c[d]["_pass"] for d in range(args.days)))
    om, ow, op_ = tot(our_ops)
    hm, hw, hp = tot(his_ops)
    print(f"\n  days 0-{args.days - 1} totals   work {ow}/{hw}   move {om}/{hm}   idle {op_}/{hp}"
          f"   mv/wk {om / max(1, ow):.2f}/{hm / max(1, hw):.2f}")


if __name__ == "__main__":
    main()