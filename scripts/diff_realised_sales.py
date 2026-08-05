"""What each side actually SOLD, per product per day, by diffing the shed across the market phase.

The last attempt at this read `steps[i].observation.private.shed` off the replay and concluded our sells
were 60-90% unfilled. That was wrong: the recorded observation is POST-market, so the tape's own orders
measure identically unfilled. Reading a post-action observation as pre-action state is the same
off-by-one that has now bitten this project four times.

This removes the ambiguity by **replaying both sides in the environment** and reading the shed
immediately before and immediately after each turn. The delta across a turn is production and
consumption plus the market, and the market part is exactly what we ordered -- so

    units_sold(turn, item) = shed_before + deposited - shed_after     is ambiguous, but
    units_sold(turn, item) = min(order, shed_before)                  is not, because `_process_market`
                             quotes per unit against the shed at that moment

and both are computed here so a disagreement is visible rather than assumed.

The question it answers: our buy and sell ORDERS match the tape's exactly, and yet from day 2 we hold
more goods and less money. Either we sell fewer units, or we sell the same units for less.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan, routines as R
import build_script_submission as B

TPD = R.TURNS_PER_DAY
REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"


def tape_plan():
    """The tape's own 720 turns, both seats, from `steps[1:]` -- index 0 is the reset placeholder."""
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    other = 1 - seat
    mine, theirs = [], []
    for step in d["steps"][1:]:
        for src, dst in ((seat, mine), (other, theirs)):
            a = (step[src] or {}).get("action") or {}
            dst.append([a.get("farmer", ["PASS"]) or ["PASS"],
                        list(a.get("hands") or []),
                        list(a.get("market") or [])])
    return mine, theirs


def our_plan():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    return B.build_plan(script.arrays())


def run(mine, theirs, label):
    """Replay `mine` against `theirs` and return realised sales and the bank, per day."""
    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)

    sold = collections.defaultdict(collections.Counter)
    revenue = collections.Counter()
    spend = collections.Counter()
    dawn = {}
    for t in range(min(len(mine), 719)):
        day, hour = divmod(t, TPD)
        obs = env.state[0].observation
        me = obs["farms"][0]
        shed_before = collections.Counter(obs["private"].get("shed") or {})
        money_before = float(me["money"])
        if hour == 0:
            dawn[day] = money_before

        f0, h0, m0 = mine[t]
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        n0 = len(me.get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])

        # what the market could possibly fill for us this turn, given the shed as it stands now
        want = collections.Counter()
        for o in m0:
            if o and o[0] == "SELL":
                want[o[1]] += int(o[2]) if len(o) > 2 else 1
        for item, n in want.items():
            sold[day][item] += min(n, shed_before.get(item, 0))

        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        after = float(env.state[0].observation["farms"][0]["money"])
        d = after - money_before
        # Every turn is either net cash in or net cash out; a turn with both a sell and a buy nets, but
        # the totals still separate revenue from spend well enough to say which side the gap is on.
        if d > 0:
            revenue[day] += d
        else:
            spend[day] -= d
        if env.state[0].status == "DONE":
            break
    return dict(sold=sold, revenue=revenue, spend=spend, dawn=dawn, label=label)


def main():
    tape_mine, tape_theirs = tape_plan()
    A = run(tape_mine, tape_theirs, "tape")
    B_ = run(our_plan(), tape_theirs, "ours")

    print(f"{'day':>4} | {'our dawn':>9} {'tape dawn':>9} {'gap':>8} | "
          f"{'our in':>8} {'tape in':>8} | {'our out':>8} {'tape out':>8} | "
          f"{'our units':>9} {'tape units':>10}")
    for day in range(0, 16):
        a_units = sum(A["sold"][day].values())
        b_units = sum(B_["sold"][day].values())
        print(f"{day:>4} | {B_['dawn'].get(day, 0):>9,.0f} {A['dawn'].get(day, 0):>9,.0f} "
              f"{B_['dawn'].get(day, 0) - A['dawn'].get(day, 0):>8,.0f} | "
              f"{B_['revenue'][day]:>8,.0f} {A['revenue'][day]:>8,.0f} | "
              f"{B_['spend'][day]:>8,.0f} {A['spend'][day]:>8,.0f} | "
              f"{b_units:>9} {a_units:>10}")


if __name__ == "__main__":
    main()
