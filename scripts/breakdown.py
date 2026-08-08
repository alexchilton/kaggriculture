"""Every number, ours AND the tape's, side by side, for each day. No deltas, no selection.

`scripts/fidelity.py` prints eight scalars as differences, which is right for finding the day a run
parts but wrong for reading what actually happened -- a delta of 0 hides whether both sides had two
cows or twenty, and a summary that shows only the fields that look good is worthless.

This prints the raw pair `ours/tape` for:

    board       money, hands, tiles owned, pens, live crop tiles PER CROP, weeds
    herd        animals standing in a pen PER SPECIES
    shed        units held PER PRODUCT, fertilizer included
    ops         every op either side emitted that day, counted -- EXCEPT sell, buy_product,
                buy_animal and buy_seed, which are FILLS (see below), not raw counts of what
                was emitted

    An emitted order is not a landed one: our agent re-offers an order every turn until it lands,
    because the env silently refuses one it can't afford, so counting emissions inflates any row
    that gets re-offered. sell/buy_product/buy_animal settle straight against `private["shed"]`
    (`_commit_unit` in `reference/kaggriculture.py`), so a turn's shed delta IS the fill -- PROVIDED
    no DROP/PICKUP/PLACE for that item also fired that turn (they touch the same field). Turns where
    that can't be guaranteed are dropped, not guessed, so these three rows are a LOWER BOUND, with
    the fraction of clean turns printed as "fill coverage". buy_seed is the same idea against
    `private["seeds"]`, which only DROP/PICKUP/PLACE never touch, so it has no coverage caveat.

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
    # Seb on the REBALANCED economy (townCenterSellInterval 24), banking $128,518 against
    # kakuteki's $70,886. The first tape we have of a top player on the game now being played.
    # Against `seb` below he moves the second parcel to day 6, builds 21 pens instead of 19,
    # and re-cuts the herd from wool to milk: MILK 179 -> 303, WOOL 230 -> 104, MELON 132 -> 96.
    "seb1326": ("data/seed_scripts/top_guys/90976060.json",
                "data/seed_scripts/top_guys/90976060/schedule.json", "Seb (allegedly)"),
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


#: Market ops that settle straight against `private["shed"]` inside `_commit_unit` -- confirmed by
#: reading `reference/kaggriculture.py` rather than assumed. SELL takes from shed, BUY_PRODUCT and
#: BUY_ANIMAL add to shed; BUY_SEED touches `private["seeds"]` instead (handled separately, below).
SHED_MARKET_OPS = ("SELL", "BUY_PRODUCT", "BUY_ANIMAL")
#: Unit-phase ops that ALSO move product across the shed boundary, so a shed delta on a turn where
#: one of these fired cannot be attributed to a market order with confidence:
#:   DROP    -- dumps the WHOLE inventory of the acting unit into the shed; which items and how much
#:              is not visible from the action alone, so it taints every item, not just one.
#:   PICKUP  -- moves a named item shed -> inventory; taints that one item.
#:   PLACE   -- normally places an animal onto a matching empty structure and never touches the shed,
#:              but falls back to a shed drop of the named item if the tile is not a valid structure
#:              (`_apply_unit_action`, the `PLACE` branch) -- which branch fired is not visible from
#:              the action either, so it taints that one item too.
#: HARVEST, FEED, COLLECT_FERTILIZER and CARE never touch `private["shed"]` directly -- they read or
#: write the acting unit's own inventory (`_farmer_inventory`) or tile state, and reach the shed only
#: via a later DROP. So, unlike the identity `total_after = total_before + produced - consumed +
#: bought - sold` this docstring originally assumed, production and consumption are NOT confounders
#: for a shed-only reading -- only DROP/PICKUP/PLACE are, because those are the only other ops that
#: touch the same field SELL/BUY_PRODUCT/BUY_ANIMAL commit against.


def run(make0, opp, seed, weeds):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    days, ops = [], collections.defaultdict(collections.Counter)
    fill_clean, fill_total = collections.Counter(), collections.Counter()
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
        drop_any = False
        taint_items = set()
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
                if op == "DROP":
                    drop_any = True
                elif op in ("PICKUP", "PLACE") and len(a) > 1:
                    taint_items.add(a[1])
        # **SELL / BUY_PRODUCT / BUY_ANIMAL are counted below as FILLS, from the shed delta.** What
        # follows is only the ops the shed delta can't explain: HIRE, BUY_LAND, and anything else
        # not in SHED_MARKET_OPS -- those are still OFFERS (an unaffordable HIRE is silent, same as
        # the original BUY_SEED bug, but fixing them is out of scope here).
        shed_orders = collections.defaultdict(set)  # item -> {op types offered for it this turn}
        for o in (a0["market"] or []):
            if not o:
                continue
            op = o[0]
            if op == "BUY_SEED" or op in SHED_MARKET_OPS:
                if op in SHED_MARKET_OPS and len(o) > 1:
                    shed_orders[o[1]].add(op)
                continue
            ops[t // 24][op] += int(o[2]) if len(o) > 2 else 1
        seeds_before = dict((o0.get("private") or {}).get("seeds") or {})
        shed_before = dict((o0.get("private") or {}).get("shed") or {})
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        # BUY_SEED as a FILL. Seeds move in exactly two ways -- a buy raises them, a PLANT lowers
        # them -- so a rise across the step is a purchase that actually landed. A buy and a plant
        # in the same turn nets out, so this can under-count by the plants of that turn; that is a
        # bounded error and vastly better than reporting 48 for a day that bought none.
        priv_after = env.state[0].observation.get("private") or {}
        seeds_after = priv_after.get("seeds") or {}
        for crop, after in seeds_after.items():
            gained = int(after) - int(seeds_before.get(crop, 0))
            if gained > 0:
                ops[t // 24]["BUY_SEED"] += gained
        # SELL / BUY_PRODUCT / BUY_ANIMAL as FILLS. A turn is clean for an item only if (a) no DROP
        # fired anywhere this turn (it taints every item, not just one), (b) no PICKUP or PLACE fired
        # for that same item, and (c) exactly one op type was offered for that item -- if two of the
        # three were offered for the same item on the same turn we cannot split one shed delta between
        # them. On a clean turn the delta IS the fill: SELL only ever decreases shed[item], BUY_PRODUCT
        # / BUY_ANIMAL only ever increase it (`_commit_unit`), so there is nothing left to attribute it
        # to. Dirty turns are dropped, not guessed -- undercounts, coverage reported alongside.
        shed_after = dict(priv_after.get("shed") or {})
        for item, optypes in shed_orders.items():
            op = next(iter(optypes))
            fill_total[op] += 1
            if drop_any or item in taint_items or len(optypes) != 1:
                continue
            delta = int(shed_after.get(item, 0)) - int(shed_before.get(item, 0))
            fill = -delta if op == "SELL" else delta
            # A clean turn's delta should never run the wrong way (SELL can't raise shed, a buy
            # can't lower it) -- `max(0, ...)` is a floor against a broken assumption, not expected
            # behaviour, so a nonzero clip here would mean SHED_MARKET_OPS/taint logic above is wrong.
            ops[t // 24][op] += max(0, fill)
            fill_clean[op] += 1
        if env.state[0].status == "DONE":
            break
    bad = [(s, env.state[s].status) for s in (0, 1) if env.state[s].status != "DONE"]
    if bad:
        raise RuntimeError(f"seat status {bad}")
    days.append(snap(env.state[0].observation, 0))
    # **Day N is the state at the END of day N, not its dawn.** `days` is collected at each dawn plus
    # one final snapshot, so `days[N + 1]` is the board after day N's actions -- which is what lines
    # up with the op counts, which are that day's actions. Reading a dawn snapshot beside the same
    # column's ops means reading YESTERDAY'S outcome next to TODAY'S work, and it caused a real
    # misreading: `money` at d12 is the result of d11, so the d10 land purchase showed up a column
    # late and a step change got attributed to the wrong day twice.
    return days[1:], ops, (fill_clean, fill_total)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=11)
    ap.add_argument("--no-moves", action="store_true",
                    help="hide the NORTH/SOUTH/EAST/WEST rows; `move` still shows their sum")
    ap.add_argument("--diff", action="store_true",
                    help="list EVERY field that differs, per day, instead of the wide tables")
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    his, his_ops, his_cov = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours, our_ops, our_cov = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)

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
    print("  state rows (money, tiles, pens, crops, sh:*) are the board at the END of that day; "
          "op rows are that day's actions.")
    print("  op rows sell/buy_product/buy_animal/buy_seed are FILLS (units that actually changed "
          "hands, read off the shed/seeds delta) -- every other op row, including hire and "
          "buy_land, is still an OFFER (what was emitted, whether or not the env accepted it).")
    print("  sell/buy_product/buy_animal are read only on turns clean of DROP/PICKUP/PLACE for that "
          "item (see coverage below) -- a dirty turn contributes ZERO, so these three rows are a "
          "LOWER BOUND on the true fill count, not an estimate of it.")

    def cov(c):
        clean, total = c
        parts = []
        for op in SHED_MARKET_OPS:
            n, d = clean[op], total[op]
            parts.append(f"{op.lower()}={n}/{d}" + (f" ({n / d:.0%})" if d else " (n/a)"))
        return "  ".join(parts)

    print(f"  fill coverage (clean turns / turns an order was offered) -- ours: {cov(our_cov)}")
    print(f"                                                              tape: {cov(his_cov)}")

    if args.diff:
        # Every field that is not identical, per day. The wide tables above are for reading what
        # happened; this is for answering "is it exact yet", where a single unrecorded row is the
        # whole answer and eyeballing a 20x11 grid is how a mismatch gets called a match.
        ops_all = sorted(set(OPS) | {"OTHER", "SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL",
                                     "BUY_LAND", "HIRE"})
        budget = (("_turns", "unit-turns"), ("_work", "work"), ("_move", "move"), ("_pass", "idle"))
        compass = {"NORTH", "SOUTH", "EAST", "WEST"}
        rows = ([("state", lab, [(ours[d][k], his[d][k]) for d in range(args.days)])
                 for k, lab in fields]
                + [("op", o.lower(), [(our_ops[d][o], his_ops[d][o]) for d in range(args.days)])
                   for o in ops_all if not (args.no_moves and o in compass)]
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