"""Why did an op the plan contained not happen? Answer before touching any prize or ranking.

**This script exists because of a repeated, expensive mistake: tuning a DECISION when the defect
was a RESOURCE.** Four separate turn-budget mechanisms were built to get day 4's fertilizer to the
shed early (`RESERVE_THE_TRIP_FOR_THE_ROW`, a land-day variant, an end-near-the-shed ranking term,
a per-product delivery rule). All four were nulls. `RESERVATION_SLIP = 0` was set to stop the sell
offer walking the price and came back byte-identical -- the bunching was never the cap, it was that
the goods reached the shed at h13 instead of h4. On 2026-08-20 a FEED was priced at the care bonus
it releases, which is correct economics, and measured byte-identical because the pen was not losing
a ranking contest, it was standing in an empty shed.

Every one of those changed how the agent CHOOSES. In every one the op never got to choose, because
the thing it consumes was not there.

`ROUTER / PLAN / EXEC` says WHERE an op died. It does not say WHY, and at the EXEC boundary the
available levers are all decision levers, so the diagnosis drifts towards them. This prints the
input instead: for every op the plan contained and the board did not record, the resource that op
consumes, measured at the hour the unit actually arrived.

    python -u scripts/why_the_op_died.py --replay <path> --team tetsuya --day 7
    python -u scripts/why_the_op_died.py --replay <path> --team tetsuya --day 7 --op FEED

Read the `resource at arrival` column first.

  - zero  -> a supply defect. No prize, rank or ordering can fix it. Do not touch one.
  - fine  -> now it is a decision, and a prize or ranking change is on the path.

What each op consumes (`reference/kaggriculture.py`):

    FEED       the ACTING UNIT's carried WHEAT (`_farmer_inventory`, :321; :505-513),
               and it returns SILENTLY when empty
    PLANT      `private["seeds"][crop]`, consumed directly (:417); and the atomic rule at
               :920-931 drops ALL plants of a crop in a turn that exceed the seeds held
    CARE       requires `fed_today` -- an unfed pen is never offered CARE at all
    HARVEST    the tile's own `yield_units` (:449); returns immediately at 0
    WATER      nothing
    BUY_*      money, and the order settles at the END of the hour it is placed
    HIRE       money, and `_do_hire` fails SILENTLY on a thin bank (:691)
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

#: Ops whose input is a per-unit carried item, and the item.
CARRIED = {"FEED": "WHEAT"}
#: Ops whose input is a farm-level pool.
POOLED = {"PLANT": "seeds"}
#: Ops whose input is a FLAG on the tile itself, not a stock anywhere.
#:
#: CARE belongs here and its absence was this script's own first bug -- it reported the CAREs on
#: d7 and d9 as "this one IS a decision" while they were strictly downstream of the FEED that had
#: just failed for want of wheat. `animal_ops` offers CARE only on a pen that is already fed, so an
#: unfed pen is not choosing not to be cared for. Exactly the confusion the script exists to stop,
#: which is the point: encode the dependency, do not rely on remembering it.
TILE_FLAG = {"CARE": "fed_today"}
#: Ops that consume nothing and can never fail for supply.
FREE = {"WATER", "MOVE", "PASS", "NORTH", "SOUTH", "EAST", "WEST"}


def _units(farm):
    return [tuple(farm.get("farmer") or (4, 4))] + [
        tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4)))
        for h in (farm.get("hands") or [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", required=True)
    ap.add_argument("--team", required=True)
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--plan", default=None,
                    help="schedule json; defaults to data/seed_scripts/<team>/schedule.json")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--op", default=None, help="only this op")
    args = ap.parse_args()

    from kaggle_environments import make
    from kagg.search import schedule_agent as A
    from kagg import plan as P

    d = json.loads(pathlib.Path(args.replay).read_text())
    seat = next(i for i, n in enumerate(d["info"]["TeamNames"])
                if args.team.lower() in str(n).lower())
    other = 1 - seat
    planp = args.plan or "data/seed_scripts/%s/schedule.json" % args.team

    planned = {}          # tile -> (unit, stop index, [ops])
    seen = set()
    real = A._solve

    def traced(units, nodes, budget, depots, load, **kw):
        sub = real(units, nodes, budget, depots, load, **kw)
        if kw.get("day") == args.day and args.day not in seen:
            seen.add(args.day)
            for ui, st in enumerate(sub.values() if isinstance(sub, dict) else sub):
                for i, n in enumerate((st or {}).get("route") or []):
                    planned[tuple(n.tile)] = (ui, i, [op for op, _i in n.ops])
        return sub

    A._solve = traced

    cfg = dict(d.get("configuration") or {})
    cfg.pop("steps", None)
    if args.seed is not None:
        cfg["seed"] = args.seed
    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    me = A.make_agent(P.load(planp), me=seat)
    opp = [((f[other] or {}).get("action") or {}) for f in d["steps"][1:]]

    done = collections.Counter()          # (tile, op) -> times the board recorded it
    arrival = {}                          # tile -> (hour, unit, carried, shed, seeds, money)
    hands_max = 0

    for t in range(719):
        if env.done:
            break
        ob = env.state[seat].observation
        day, hour = int(ob.get("day", 0) or 0), int(ob.get("hour", 0) or 0)
        if day > args.day:
            break
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        farm = ob["farms"][seat]
        pr = ob.get("private") or {}
        shed = (pr.get("shed") if isinstance(pr, dict) else None) or farm.get("shed") or {}
        seeds = (pr.get("seeds") if isinstance(pr, dict) else None) or {}
        invs = (pr.get("inventories") if isinstance(pr, dict) else None) or []
        m = me(ob, t)
        acts = [m["farmer"]] + list(m["hands"])[:n[seat]]

        if day == args.day:
            hands_max = max(hands_max, n[seat])
            for u, p in enumerate(_units(farm)):
                if p in planned and p not in arrival and planned[p][0] == u:
                    cell = farm["tiles"][p[1]][p[0]]
                    arrival[p] = (hour, u, dict(invs[u]) if u < len(invs) else {},
                                  dict(shed), dict(seeds),
                                  float(farm.get("money") or 0),
                                  dict(cell) if isinstance(cell, dict) else {})
                if u < len(acts) and acts[u]:
                    done[(p, acts[u][0])] += 1

        st = opp[t] if t < len(opp) else {}
        a = [None, None]
        a[seat] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[seat]],
                   "market": m["market"]}
        a[other] = {"farmer": st.get("farmer") or ["PASS"],
                    "hands": list(st.get("hands") or [])[:n[other]],
                    "market": st.get("market") or []}
        env.step(a)

    print("d%d, seat %d, team %s.  hands that existed: %d\n" % (
        args.day, seat, args.team, hands_max))
    print("%-9s %-6s %-13s %-9s %-7s %s" % (
        "tile", "unit", "op", "happened", "arrived", "RESOURCE AT ARRIVAL"))
    print("-" * 92)
    supply, decision = 0, 0
    for tile, (ui, _i, ops) in sorted(planned.items(), key=lambda kv: kv[1][:2]):
        for op in ops:
            if args.op and op != args.op:
                continue
            if op in FREE:
                continue
            ok = done[(tile, op)] > 0
            if ok:
                continue
            got = arrival.get(tile)
            if got is None:
                if ui > hands_max:
                    note = "unit %d WAS NEVER HIRED" % ui
                else:
                    note = "the unit never reached the tile"
                print("%-9s %-6d %-13s %-9s %-7s %s" % (
                    str(tile), ui, op, "NO", "never", note))
                supply += 1
                continue
            hour, u, carried, shed, seeds, money, cell = got
            if op in TILE_FLAG:
                flag = TILE_FLAG[op]
                have = 1 if cell.get(flag) else 0
                note = "%s on the tile: %s%s" % (
                    flag, bool(cell.get(flag)),
                    "   (so this is downstream of the FEED above, not a decision)"
                    if not cell.get(flag) else "")
            elif op in CARRIED:
                item = CARRIED[op]
                have = int(carried.get(item, 0) or 0)
                note = "%s carried by u%d: %d   (shed %s: %d)" % (
                    item, u, have, item, int(shed.get(item, 0) or 0))
            elif op in POOLED:
                have = sum(int(v or 0) for v in seeds.values())
                note = "seeds held: %s" % ({k: v for k, v in seeds.items() if v} or "NONE")
            elif op.startswith("BUY") or op == "HIRE":
                have = money
                note = "bank: $%.0f" % money
            else:
                have = None
                note = "consumes nothing -- this one IS a decision"
            print("%-9s %-6d %-13s %-9s %-7s %s%s" % (
                str(tile), ui, op, "NO", "h%d" % hour, note,
                "   << SUPPLY" if have == 0 else ""))
            if have == 0:
                supply += 1
            else:
                decision += 1

    print("-" * 92)
    print("%d died for want of the thing they consume. %d had it and still did not run.\n"
          % (supply, decision))
    if supply and not decision:
        print("EVERY failure here is SUPPLY. Do not change a prize, a rank or an ordering:\n"
              "the op never got to choose. Fix when the resource arrives.")
    elif decision:
        print("At least one op had its input and still did not run. That one is a real decision\n"
              "or routing question and a prize/ranking change is on the path for it.")


if __name__ == "__main__":
    main()
