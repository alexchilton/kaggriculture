"""Seb gets day 10's melon harvest into the shed and sold. We do not. What does he do differently?

Day 10's schedule row asks for 18 melons. He holds zero at day 11 dawn because he sold them on the
day; ours arrive at day 11 dawn via the overnight sweep, meaning they were still in hands at dusk.
That one day is the $4,000 fourth parcel (banks at d10 dawn: ours 1638, his 3104).

Runs BOTH seats the way `scripts/breakdown.py` does -- the tape in seat 0 against its own opponent,
then our agent in seat 0 against the same opponent -- and prints day 10 hour by hour for each:
melon in the shed, melon in hands, and the HARVEST / DROP / SELL events.

The question this answers is not "are we slower" but WHICH of the three legs differs: harvesting
later, carrying longer before dropping, or dropping in time but never offering the sell.
"""
import json, pathlib, sys, collections
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE
from kaggle_environments import make

DAY, PROD = 10, "MELON"
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
print(f"day {DAY} sells row: {sched[DAY].get('sells')}")


def trace(make_seat0, label):
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = make_seat0()
    opp = tape_policy(replay, team, 1)
    rows, sold = [], 0
    for t in range(24 * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        acts = [a0["farmer"]] + list(a0["hands"] or [])[:n0]
        if t // 24 == DAY:
            shed = int(((o0.get("private") or {}).get("shed") or {}).get(PROD, 0))
            invs = (o0.get("private") or {}).get("inventories") or []
            hands = sum(int((iv or {}).get(PROD, 0)) for iv in invs)
            ev = [f"u{i}:{a[0]}" for i, a in enumerate(acts)
                  if a and a[0] in ("HARVEST", "DROP", "PICKUP")]
            sells = [o for o in (a0["market"] or []) if o and o[0] == "SELL" and o[1] == PROD]
            if shed or hands or ev or sells:
                rows.append(f"  h{t % 24:>2} shed={shed:<3} hands={hands:<3} "
                            f"{' '.join(ev):<46}{'SELL ' + str(sells[0][2]) if sells else ''}")
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    end = int(((env.state[0].observation.get("private") or {}).get("shed") or {}).get(PROD, 0))
    print(f"\n===== {label} =====")
    print("\n".join(rows) or "  (no melon activity at all)")
    print(f"  -> {PROD} in shed at day {DAY + 1} dawn: {end}")
    print(f"  -> money at day {DAY + 1} dawn: {int(env.state[0].observation['farms'][0]['money'])}")


trace(lambda: tape_policy(replay, team, 0), "SEB (the tape)")
trace(lambda: (lambda o, t: SA.make_agent(thin, 0, router=True)(o)) if False else
      (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)), "OURS")
