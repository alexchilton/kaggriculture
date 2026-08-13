"""Where a season's unit-turns go, and how much of the walking is the LAYOUT rather than the work.

The routing question this answers is not "do we walk too much" -- `breakdown.py` already prints
`mv/wk` -- but "is the walking a property of WHERE we put things". A tile is visited once per day it
wants service, and a pen wants service every day for the rest of the season while a wheat wants four
visits total. So the same set of contents, placed differently, costs a different number of turns
before any router runs.

Per tile that ever held anything this reports: what it held, how many WORK turns landed on it, and
its Manhattan distance to the nearest depot (shed-access cell) we own. From that:

    service demand  = sum over work visits of dist(tile, nearest owned depot)

which is a lower bound on the walking the layout DEMANDS -- every visit has to be reached from
somewhere, and the depot ring is where units spawn, where feed is drawn and where product is
dropped. The counterfactual is the rearrangement bound: hold the multiset of per-tile visit counts
and the multiset of tile distances fixed, and pair them optimally (most-visited tile onto the
nearest ground). Anything above that bound is attributable to placement and nothing else.

    python -u scripts/where_the_walking_goes.py --seed 11 --tape seb
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import routines as R
from kagg.search import schedule_agent
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, MOVES, WORK, tape_policy

SHED = [tuple(t) for t in R.shed_access_tiles()]


def _owned_depots(farm):
    tiles = farm["tiles"]
    return [t for t in SHED if tiles[t[1]][t[0]] != "LOCKED"] or [(4, 4)]


def _label(cell):
    if not isinstance(cell, dict):
        return None
    k = cell.get("kind")
    if k == "PLANT":
        return str(cell.get("crop"))
    if k == "WEED":
        return "WEED"
    if cell.get("animal"):
        return f"{k}:{cell['animal']}"
    return str(k)


def run(make0, opp, seed, weeds):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()

    visits = collections.Counter()          # tile -> work turns landed on it
    dsum = collections.Counter()            # tile -> sum of depot distance over those visits
    ops_at = collections.defaultdict(collections.Counter)   # tile -> op -> n
    held = collections.defaultdict(set)     # tile -> labels it ever carried
    budget = collections.Counter()          # _work / _move / _pass / _turns
    first_seen = {}                         # tile -> day it first held anything

    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        farm = o0["farms"][0]
        depots = _owned_depots(farm)
        day = t // 24
        for y, row in enumerate(farm["tiles"]):
            for x, cell in enumerate(row):
                lab = _label(cell)
                if lab:
                    held[(x, y)].add(lab)
                    first_seen.setdefault((x, y), day)
        pos = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        acts = [a0["farmer"]] + list(a0["hands"] or [])[:n0]
        for i, a in enumerate(acts):
            if not a:
                continue
            op = a[0]
            budget["_turns"] += 1
            if op in MOVES:
                budget["_move"] += 1
            elif op in WORK:
                budget["_work"] += 1
                tile = pos[i] if i < len(pos) else None
                if tile is not None:
                    visits[tile] += 1
                    dsum[tile] += min(abs(tile[0] - d[0]) + abs(tile[1] - d[1]) for d in depots)
                    ops_at[tile][op] += 1
            else:
                budget["_pass"] += 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break

    fin = env.state[0].observation["farms"][0]
    money = int(fin["money"])
    depots = _owned_depots(fin)
    dist_of = {}
    for y, row in enumerate(fin["tiles"]):
        for x, cell in enumerate(row):
            if cell == "LOCKED":
                continue
            if (x, y) in SHED:
                dist_of[(x, y)] = 0
                continue
            dist_of[(x, y)] = min(abs(x - d[0]) + abs(y - d[1]) for d in depots)
    return dict(visits=visits, dsum=dsum, ops=ops_at, held=held, budget=budget,
                money=money, dist=dist_of, first=first_seen)


def report(name, r):
    visits, dist = r["visits"], r["dist"]
    tiles = sorted(set(visits) | set(r["held"]),
                   key=lambda t: (-visits[t], dist.get(t, 99)))
    print(f"\n=== {name}   bank ${r['money']:,}   "
          f"unit-turns {r['budget']['_turns']}  work {r['budget']['_work']}  "
          f"move {r['budget']['_move']}  idle {r['budget']['_pass']}  "
          f"mv/wk {r['budget']['_move'] / max(1, r['budget']['_work']):.2f}")
    print(f"  {'tile':>8} {'d':>3} {'visits':>7} {'v*d':>6}  {'day':>3}  contents")
    tot_v = tot_d = 0
    for t in tiles:
        v, d = visits[t], dist.get(t, 99)
        tot_v += v
        tot_d += r["dsum"][t]
        lab = ",".join(sorted(r["held"][t])) or "-"
        print(f"  {str(t):>8} {d:>3} {v:>7} {r['dsum'][t]:>6}  {r['first'].get(t, -1):>3}  {lab}")

    # The rearrangement bound: same visit counts, same available ground, paired optimally.
    counts = sorted(visits.values(), reverse=True)
    ground = sorted(d for t, d in dist.items() if t not in SHED)
    # shed cells are distance 0 and there are four of them; they can absorb the four biggest.
    ground = [0] * sum(1 for t in dist if t in SHED) + ground
    bound = sum(c * g for c, g in zip(counts, ground))
    print(f"\n  {name}: {tot_v} work visits, service demand (sum v*d) = {tot_d}")
    print(f"  {name}: rearrangement bound on the SAME visit multiset and the SAME ground = {bound}")
    print(f"  {name}: attributable to placement = {tot_d - bound} depot-steps "
          f"({(tot_d - bound) / max(1, tot_d):.0%} of demand)")
    # By content class, since that is the thing the assignment would sort on.
    by = collections.Counter()
    nby = collections.Counter()
    for t in tiles:
        lab = ",".join(sorted(r["held"][t])) or "-"
        by[lab] += visits[t]
        nby[lab] += 1
    print(f"\n  visits by content class ({name}):")
    for lab, v in by.most_common():
        print(f"    {lab:<44} {nby[lab]:>3} tiles  {v:>5} visits  {v / max(1, nby[lab]):>6.1f} per tile")
    return tot_d, bound


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default=DEFAULT_TAPE, choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    print(f"seed {args.seed}  weeds {args.weeds}  tape {args.tape}")
    his = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)

    hd, hb = report("TAPE", his)
    od, ob = report("OURS", ours)
    print(f"\nHEADLINE  service demand  ours {od}  tape {hd}")
    print(f"          bound           ours {ob}  tape {hb}")
    print(f"          placement waste ours {od - ob}  tape {hd - hb}")


if __name__ == "__main__":
    main()
