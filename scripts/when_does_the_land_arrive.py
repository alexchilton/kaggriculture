"""Which day each parcel is actually paid for, against the day the schedule asked for it.

Seb buys land on days 4, 6 and 10 and finishes the season owning all four quadrants. The original
leader buys two parcels, on days 7 and 10, and finishes with three. That is not a small difference:

    tiles           75 against 100
    crew            the hand that wakes on (5,5) has all four orthogonal neighbours locked and cannot
                    move at all until a SECOND quadrant exists (`kaggriculture.py:313`). Seb owns NE
                    from day 4, so his full crew works from day 4; on the original plan one hand in
                    four is dead until day 7.

So the target for the agent is not "buy the land eventually", it is **day 4, day 6, day 10**. The
agent's land rule treats the schedule's day as a FLOOR and buys the first turn it can pay, which
means a plan that says day 4 is silently satisfied on day 9 if the bank is thin -- and nothing in the
season totals would ever show it.

This prints, per parcel: the day the schedule wanted it, the day and hour we actually paid, the bank
at the scheduled dawn, and the slip. A slip is an executor failure to fund the plan on time, which is
a different problem from routing and needs a different fix.
"""

import argparse
import collections
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import routines as R
from kagg.search import schedule_agent
import agent_ladder as L


def run(seed, weeds, sched, theirs):
    """Play one season; return (wanted_days, [(day, hour, bank_before)], per-day quadrant count)."""
    env = L._env(seed, weeds)
    us = schedule_agent.make_agent(sched, 0, router=True)
    paid, owned, dawn_bank = [], {}, {}
    prev = 1
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        farm = obs["farms"][0]
        n_q = len(farm.get("unlocked_quadrants") or ["NW"])
        if hour == 0:
            owned[day] = n_q
            dawn_bank[day] = int(farm["money"])
        if n_q > prev:
            # The parcel landed at the END of the previous turn, so this is the first observation of it.
            paid.append((day, hour, int(farm["money"])))
            prev = n_q
        a = us(obs)
        n0 = len(farm.get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": a["farmer"], "hands": list(a["hands"])[:n0], "market": a["market"]},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    return paid, owned, dawn_bank


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schedule", default="data/seed_scripts/new_leader/schedule.json")
    ap.add_argument("--seeds", default="11,22,33,44,55,66,77,88,99,101,202,303")
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    sched = {int(k): v for k, v in json.loads(pathlib.Path(args.schedule).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []
    wanted = [d for d in sorted(sched) for _ in range(int(sched[d].get("land", 0) or 0))]
    _mine, theirs = L.tape_plans()

    print(f"schedule {args.schedule}")
    print(f"  parcels wanted on days {wanted}   ({len(wanted)} parcels, "
          f"{len(wanted) + 1} quadrants at plan)\n")
    print(f"{'seed':>5}  {'parcel days paid':<28}{'slip vs plan':<16}{'quadrants at day 29':>20}")
    slips = collections.defaultdict(list)
    finals = []
    for seed in [int(s) for s in args.seeds.split(",")]:
        paid, owned, _bank = run(seed, args.weeds, sched, theirs)
        got = [d for d, _h, _m in paid]
        slip = [got[i] - wanted[i] if i < len(got) else None for i in range(len(wanted))]
        for i, s in enumerate(slip):
            if s is not None:
                slips[i].append(s)
        final = owned.get(max(owned), 1) if owned else 1
        finals.append(final)
        pretty = ", ".join(f"d{d}h{h}" for d, h, _m in paid) or "never"
        print(f"{seed:>5}  {pretty:<28}{str(slip):<16}{final:>20}")
    print()
    for i in sorted(slips):
        v = slips[i]
        print(f"  parcel {i + 1}  wanted day {wanted[i]:<3} mean slip {statistics.mean(v):>+5.1f} days"
              f"   bought in {len(v)}/{len(finals)} seasons")
    for i in range(len(wanted)):
        if i not in slips:
            print(f"  parcel {i + 1}  wanted day {wanted[i]:<3} NEVER BOUGHT in any season")
    print(f"\n  quadrants at season end: mean {statistics.mean(finals):.2f} of "
          f"{len(wanted) + 1} planned")


if __name__ == "__main__":
    main()
