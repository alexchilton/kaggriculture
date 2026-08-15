"""Swap n tiles of one crop for another, on a day the substitute can still finish, and check it got harvested.

## The design, and why each piece is forced

**One process per cell.** Measured 2026-08-15: the same config run four times in one process gave
$134,665, then $94,523 three times -- the FIRST run in a process differs -- and a shift config gave
$92,775 then $89,640 on identical inputs. Any harness that reuses a process measures run order.
This script therefore does exactly ONE measurement per invocation and is driven from outside.

**The swap day is dictated by the substitute's lead time**, not chosen freely. A crop planted too
late cannot complete a cycle before d29, and its tiles are then worth zero however good the crop is:

    TOMATO      first yield d+8,  ONGOING every 1d x4  -> 11 days -> plant by d18
    STRAWBERRY  first yield d+10, ONGOING every 2d x4  -> 16 days -> plant by d13
    MELON       first yield d+10, one-shot to d+12     -> 12 days -> plant by d17
    WHEAT       first yield d+2,  one-shot to d+4      ->  4 days -> plant by d25
    CARROT      first yield d+2,  one-shot to d+3      ->  3 days -> plant by d26

It must also be a day the SOURCE crop is planted, or there is nothing to re-crew. In the shipped
schedule: MELON d0/d6/d7, STRAWBERRY d5/d7/d8/d11/d12, WHEAT d0/d4/d8/d10-d20, CARROT d21-d25.

**Routes go live from the swap day.** `cover._apply_precomputed` keys a stop on `(tile, ops)`, so a
swapped crop drops its stop from the solved route instead of adapting. Measured cost of unsolving
d12-d29: bank -$11,431 on seed 3, but collection stays at 98% and per-crop rates are unchanged
(wheat 97%, strawberry 98%, melon 100%). The executor still gets the harvest in, which is what makes
the comparison legitimate.

**Every cell reports its own collection rate.** That is the check that the number means anything: a
substitute collected at 95% is being served by the crew, and its money figure is about the crop. One
collected at 30% is a routing failure wearing a crop's name.

    python -u scripts/swap_one_crop.py --seed 3 --src WHEAT --dst TOMATO --n 4 --day 12
    python -u scripts/swap_one_crop.py --seed 3            # baseline, no swap
"""
import argparse
import collections
import importlib
import importlib.util
import json
import pathlib
import sys

sys.path.insert(0, ".")

import reference.kaggriculture as KG

REPO = pathlib.Path(__file__).resolve().parent.parent

#: Days by which each crop must be planted to complete a full cycle before the season ends.
LATEST_PLANTING = {}
for _c, _s in KG.CROPS.items():
    _span = (_s["first_yield_day"] + _s["interval"] * (_s["max_yield"] - 1)
             if _s["ongoing"] else _s["max_yield_day"])
    LATEST_PLANTING[_c] = 29 - _span


def parse_shifts(spec):
    """`"WHEAT:TOMATO:1,WHEAT:CARROT:1"` -> `(("WHEAT","TOMATO",1), ("WHEAT","CARROT",1))`.

    Combinations are not the sum of their parts: every crop competes for the same crew turns and the
    same water, so one tomato beside one carrot is a different question from either alone. The
    budgets drain independently and in the order given.
    """
    out = []
    for part in (spec or "").split(","):
        part = part.strip()
        if not part:
            continue
        s, d, n = part.split(":")
        out.append((s.strip().upper(), d.strip().upper(), int(n)))
    return tuple(out)


def run(seed, shifts, day, opponent, geese=0, schedule=None, unsolve_from=None):
    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    C = importlib.import_module("kagg.search.cover")
    PLAN = importlib.import_module("kagg.plan")

    A.CROP_TILE_SHIFTS = tuple(shifts)
    if shifts:
        A.LATE_CROP_FROM_DAY = day
    # **`HERD_GEESE` converts N of the schedule's animals to GOOSE**, earliest first, via
    # `swap_in_geese` at `schedule_agent:4242`. Its 2026-08-11/12 negative verdict was measured
    # BEFORE `c99a8a5` fixed `SELLABLE` on 2026-08-13 -- and `SELLABLE` omitted EGG, so those geese
    # produced a product that could not be sold at all. The verdict is pure cost with zero revenue
    # by construction, and nobody has re-run it since. See `docs/the_goose_is_insurance_2026-08-15.md`.
    A.HERD_GEESE = int(geese)
    # A q4 plan diverges at d9, so its routes must go live from there rather than d12 -- the solved
    # stops from d9 on were built for a 75-tile three-quadrant board and key on `(tile, ops)`.
    unsolved = tuple(range(unsolve_from if unsolve_from is not None else max(12, day), 30))
    C.UNSOLVE_DAYS = unsolved
    C.PRECOMPUTED_ROUTES = {d: v for d, v in C.PRECOMPUTED_ROUTES.items() if d not in unsolved}

    sp = importlib.util.spec_from_file_location("opp", opponent)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    opp = mod.agent

    sched = PLAN.load(str(REPO / (schedule or "data/seed_scripts/kawashigi/schedule.json")))
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)

    grown, collected, weeded = collections.Counter(), collections.Counter(), collections.Counter()
    planted = collections.defaultdict(set)
    prev = {}
    for t in range(719):
        o = env.state[0].observation
        cur, weed_now = {}, {}
        for y, row in enumerate(o["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                k = (x, y)
                if isinstance(c, dict) and c.get("crop"):
                    cur[k] = (c["crop"], c.get("yield_units", 0))
                    planted[c["crop"]].add((x, y, c.get("planted_day")))
                elif c == "WEED" or (isinstance(c, dict) and c.get("kind") == "WEED"):
                    weed_now[k] = True
                    if prev.get(k):
                        weeded[prev[k][0]] += 1
        for k, (crop, u) in cur.items():
            was = prev.get(k)
            if was and was[0] == crop:
                if u > was[1]:
                    grown[crop] += u - was[1]
                elif u < was[1]:
                    collected[crop] += was[1] - u
            elif u:
                grown[crop] += u
        for k, (crop, u) in prev.items():
            if u and cur.get(k, (None,))[0] != crop and not weed_now.get(k):
                collected[crop] += u
        prev = cur
        env.step([me(o, t), opp(env.state[1].observation, t)])
        if env.done:
            break

    return dict(seed=seed, shifts=[list(s) for s in shifts], day=day,
                dsts=sorted({d for _, d, _ in shifts}),
                money=env.steps[-1][0]["reward"], opp_money=env.steps[-1][1]["reward"],
                grown=dict(grown), collected=dict(collected),
                tiles={c: len(v) for c, v in planted.items()}, weeded=dict(weeded))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--src", default=None)
    ap.add_argument("--dst", default=None)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--shifts", default=None,
                    help="SRC:DST:N[,SRC:DST:N...] -- combinations, applied in order")
    ap.add_argument("--day", type=int, default=12)
    ap.add_argument("--schedule", default=None,
                    help="path to a schedule.json, relative to the repo root")
    ap.add_argument("--unsolve-from", type=int, default=None, dest="unsolve_from",
                    help="first day to run with LIVE routes (a q4 plan diverges at d9)")
    ap.add_argument("--geese", type=int, default=0,
                    help="convert N scheduled animals to GOOSE (schedule_agent.HERD_GEESE)")
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    shifts = parse_shifts(a.shifts) if a.shifts else (
        ((a.src, a.dst, a.n),) if a.src and a.dst else ())
    for _, d, _ in shifts:
        if a.day > LATEST_PLANTING.get(d, 29):
            print(f"REFUSED: {d} planted on d{a.day} cannot finish a cycle "
                  f"(latest is d{LATEST_PLANTING[d]})")
            return

    r = run(a.seed, shifts, a.day, a.opponent, geese=a.geese,
            schedule=a.schedule, unsolve_from=a.unsolve_from)
    r["geese"] = a.geese
    if a.json:
        print(json.dumps(r))
        return
    lab = " + ".join(f"{s}->{d} x{n}" for s, d, n in shifts) or "baseline"
    if a.geese:
        lab = (lab + f" + {a.geese} GEESE") if shifts else f"{a.geese} GEESE"
    g, c = r["grown"], r["collected"]
    rate = lambda k: f"{c.get(k,0)/g[k]:.0%}" if g.get(k) else "-"
    print(f"{lab:<40} seed {a.seed}  bank ${r['money']:,.0f}  (opp ${r['opp_money']:,.0f})")
    print(f"  tiles {r['tiles']}")
    print(f"  collected " + "  ".join(f"{k}:{rate(k)}" for k in sorted(g)))
    for d in r["dsts"]:
        print(f"  >>> {d}: grown {g.get(d,0)}  collected {c.get(d,0)}  "
              f"rate {rate(d)}  <-- if this is low the money number is a ROUTING result")


if __name__ == "__main__":
    main()
