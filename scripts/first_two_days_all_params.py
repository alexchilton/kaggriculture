"""Everything about days 0 and 1, ours beside the tape's, turn by turn and then totalled.

A season diverges the way compound interest diverges: the farms are the same size on day 0 and 25%
apart by day 29, and every per-day table so far shows the gap already open by day 2. So the useful
comparison is not the season, it is the first forty-eight turns with nothing aggregated away --
because on day 0 both farms start on the identical board with $3,000 and one farmer, and any
difference there is a pure decision difference, not a consequence of being poorer.

Prints, for each of day 0 and day 1:

    per turn      every unit's position and action for both farms, side by side, plus money, shed,
                  carried inventory and the market orders actually submitted
    totals        op counts, moves, distance walked, tiles touched, crops in the ground, seeds bought,
                  money spent and money banked

`--turns` trims the per-turn dump; the totals always cover the whole day.
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

MOVES = ("NORTH", "SOUTH", "EAST", "WEST")


def _fmt_units(pos, acts):
    return " ".join(f"{x}{y}:{(a[0] if isinstance(a, list) and a else 'PASS')[:5]}"
                    f"{'/' + str(a[1]) if isinstance(a, list) and len(a) > 1 else ''}"
                    for (x, y), a in zip(pos, acts))


def _census(tiles):
    c = collections.Counter()
    for row in tiles:
        for cell in row:
            if isinstance(cell, dict):
                c["animal" if "animal" in cell else cell.get("kind", "?")] += 1
    return c


def run(seed, days, make_us=None, tape=None, theirs=None):
    """Play `days` days, capturing a full per-turn record of seat 0."""
    env = L._env(seed, 0.0)
    us = make_us() if make_us else None
    log = collections.defaultdict(list)
    tot = collections.defaultdict(collections.Counter)
    for t in range(days * RT.TPD):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        if day >= days:
            break
        farm, priv = obs["farms"][0], obs["private"]
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        acts = [f0, *list(h0)][:len(pos)]
        carry = collections.Counter()
        for iv in priv.get("inventories") or []:
            carry.update({k: v for k, v in iv.items() if v})
        log[day].append(dict(hour=hour, money=int(farm["money"]), units=_fmt_units(pos, acts),
                             shed={k: v for k, v in (priv.get("shed") or {}).items() if v},
                             seeds={k: v for k, v in (priv.get("seeds") or {}).items() if v},
                             carry=dict(carry), market=[list(o) for o in m0]))
        for act in acts:
            if not (isinstance(act, list) and act):
                continue
            tot[day][act[0]] += 1
            if act[0] in MOVES:
                tot[day]["_moves"] += 1
            elif act[0] != "PASS":
                tot[day]["_work"] += 1
        for o in m0:
            # `mktoffered:` rather than `mkt:`, because these are ORDER quantities: the row
            # is what the arm asked the market for, not what it got.
            tot[day]["mktoffered:" + "_".join(str(p) for p in o[:2])] += (
                int(o[2]) if len(o) > 2 else 1)
        tot[day]["_units"] = max(tot[day]["_units"], len(pos))
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:len(pos) - 1], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if hour == RT.TPD - 1:
            end = env.state[0].observation
            tot[day]["_money_end"] = int(end["farms"][0]["money"])
            for k, v in _census(end["farms"][0]["tiles"]).items():
                tot[day]["tile:" + k] = v
        if env.state[0].status == "DONE":
            break
    return log, tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", nargs="?", type=int, default=11)
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--turns", type=int, default=RT.TPD, help="per-turn rows to print per day")
    # Day 0 starts identical for both farms -- same board, same $3,000 -- so comparing our day 0
    # against a CLOSED-LOOP player's recorded day 0 is still fair even though replaying his later
    # turns on our seed is not. Seb diverges from himself at turn 96; day 0 is turn 0-23.
    ap.add_argument("--replay", default=str(L.REPLAY))
    ap.add_argument("--team", default=L.TEAM)
    ap.add_argument("--schedule", default=str(L.SCHEDULE))
    args = ap.parse_args()

    mine, theirs = L.tape_plans(pathlib.Path(args.replay), args.team)
    sched = {int(k): v for k, v in json.loads(pathlib.Path(args.schedule).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_log, tape_tot = run(args.seed, args.days, tape=mine, theirs=theirs)
    our_log, our_tot = run(args.seed, args.days,
                           make_us=lambda: schedule_agent.make_agent(sched, 0, router=True),
                           theirs=theirs)

    for day in range(args.days):
        print(f"\n{'=' * 118}\nDAY {day}\n{'=' * 118}")
        for o, t in zip(our_log[day][:args.turns], tape_log[day][:args.turns]):
            print(f"  h{o['hour']:>2}  OURS ${o['money']:>6}  {o['units']}")
            if o["market"]:
                print(f"        market {o['market']}")
            if o["shed"] or o["carry"] or o["seeds"]:
                print(f"        shed{o['shed']} seeds{o['seeds']} carry{o['carry']}")
            print(f"       TAPE ${t['money']:>6}  {t['units']}")
            if t["market"]:
                print(f"        market {t['market']}")
            if t["shed"] or t["carry"] or t["seeds"]:
                print(f"        shed{t['shed']} seeds{t['seeds']} carry{t['carry']}")
            print()

        o, t = our_tot[day], tape_tot[day]
        keys = sorted(set(o) | set(t))
        print(f"  {'DAY ' + str(day) + ' TOTALS':<34} {'ours':>10} {'tape':>10}   diff")
        for k in keys:
            if o[k] == t[k]:
                continue
            print(f"  {k:<34} {o[k]:>10} {t[k]:>10}   {o[k] - t[k]:+}")
        same = [k for k in keys if o[k] == t[k] and o[k]]
        print(f"  identical: {', '.join(f'{k}={o[k]}' for k in same) or '(none)'}")
        print(f"  DIFFERENCES: {sum(1 for k in keys if o[k] != t[k])} of {len(keys)} parameters")


if __name__ == "__main__":
    main()
