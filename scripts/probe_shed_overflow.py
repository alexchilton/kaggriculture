"""What the dusk drop DISCARDS, per day, per item, both sides.

`_drop_inventories_to_shed` (`reference/kaggriculture.py:812`) empties every unit inventory into the
shed at dusk and its own docstring says "overflow is discarded". `shedCapacity` defaults to 100 and
`sum(shed.values())` is the whole shed, every product together -- so a large idle stock of ONE
product silently destroys the day's harvest of EVERY other. Nothing in `breakdown.py` can see this:
the harvest row counts the op, the shed row shows the survivors, and the destroyed units appear in
neither.

The same clamp also sits on the `DROP` op (`:470`) and on `PICKUP`'s room check (`:333`), so a full
shed additionally makes a mid-day DROP a no-op.

    python -u scripts/probe_shed_overflow.py
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

LOST = collections.defaultdict(collections.Counter)   # (seat, day) -> item -> discarded
FULL = collections.defaultdict(collections.Counter)   # (seat, day) -> shed total at dusk
CALLS = [0]
DAY = [0]


def install():
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg
    if getattr(kg, "_overflow_probe", False):
        return
    orig_drop = kg._drop_inventories_to_shed
    orig_apply = kg._apply_unit_action

    def drop(private, capacity):
        # `_end_of_day` calls this once per farm in seat order, so call parity is the seat.
        seat = CALLS[0] % 2
        CALLS[0] += 1
        want = collections.Counter()
        for inv in private["inventories"]:
            for item, n in inv.items():
                if n > 0:
                    want[item] += n
        before = sum(private["shed"].values())
        orig_drop(private, capacity)
        after = sum(private["shed"].values())
        moved = after - before
        short = sum(want.values()) - moved
        if short > 0:
            # Which items were lost is order-dependent inside the original; attribute the shortfall
            # to the items present, largest first, which is enough to name the victim.
            for item, n in want.most_common():
                take = min(n, short)
                if take:
                    LOST[(seat, DAY[0])][item] += take
                    short -= take
                if not short:
                    break
        FULL[(seat, DAY[0])]["shed"] = after
        FULL[(seat, DAY[0])]["cap"] = capacity

    def apply_unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
        # A mid-day DROP into a full shed is silently truncated too (`:470`). Count the units the
        # unit was carrying that the clamp refused.
        blocked = 0
        if isinstance(action, list) and action and action[0] == "DROP":
            inv = private["inventories"][idx] if idx < len(private["inventories"]) else {}
            room = max(0, shed_capacity - sum(private["shed"].values()))
            blocked = max(0, sum(inv.values()) - room)
        r = orig_apply(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        if blocked:
            seat = SEAT_NOW[0]
            LOST[(seat, DAY[0])]["_drop_blocked"] += blocked
        return r

    kg._drop_inventories_to_shed = drop
    kg._apply_unit_action = apply_unit
    kg._overflow_probe = True


SEAT_NOW = [0]


def run(make0, opp, seed, weeds):
    from kaggle_environments import make
    install()
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    CALLS[0] = 0
    p0, p1 = make0(), opp()
    for t in range(719):
        DAY[0] = t // 24
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    LOST.clear()
    FULL.clear()
    run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    his_lost = {k: collections.Counter(v) for k, v in LOST.items()}
    his_full = {k: collections.Counter(v) for k, v in FULL.items()}
    LOST.clear()
    FULL.clear()
    a = schedule_agent.make_agent(thin, 0, router=True)
    run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)
    our_lost, our_full = dict(LOST), dict(FULL)

    print(f"dusk DROP overflow  --  tape {args.tape} seed {args.seed} weeds {args.weeds}, "
          f"seat 0 both sides.  shed capacity is the WHOLE shed, all products together.")
    print(f"{'day':>4} | {'shed':>5}{'lost':>5}  {'what we lost':<42} | "
          f"{'shed':>5}{'lost':>5}  {'what the tape lost':<30}")
    ot, ht = collections.Counter(), collections.Counter()
    for d in range(args.days):
        ol = our_lost.get((0, d), collections.Counter())
        hl = his_lost.get((0, d), collections.Counter())
        ot.update(ol)
        ht.update(hl)
        osh = our_full.get((0, d), collections.Counter())["shed"]
        hsh = his_full.get((0, d), collections.Counter())["shed"]
        f = lambda c: " ".join(f"{k.lower()[:6]}:{v}" for k, v in c.most_common())
        print(f"{d:>4} | {osh:>5}{sum(ol.values()):>5}  {f(ol):<42} | "
              f"{hsh:>5}{sum(hl.values()):>5}  {f(hl):<30}")
    print(f"\n  season discarded -- ours {sum(ot.values())}: {dict(ot)}")
    print(f"                      tape {sum(ht.values())}: {dict(ht)}")


if __name__ == "__main__":
    main()
