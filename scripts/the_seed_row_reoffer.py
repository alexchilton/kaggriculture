"""Is `buy_seed +42` on day 6 forty-two extra seeds, or the same order counted many times?

`scripts/breakdown.py` tallies market orders with `ops[day][o[0]] += int(o[2])` -- the QUANTITY of
every order EMITTED, every turn. Our seed row is deliberately re-offered each turn until it lands
(`schedule_agent.py`, the `short = qty - seeds[crop]` loop) because a BUY_SEED the env rejects for
want of funds is silent. The tape offers each order once. So an unfunded re-offer inflates the
tally without buying anything.

Two hints that +42 is not real spend: day 6's money column is blank, and `plant` is -1 for the
whole season.

Prints, per turn of day 6: our bank, the BUY_SEED orders we emit, and the seeds actually held --
so a re-offer that never lands is visible as a repeated order with a flat seed count.
"""
import json, pathlib, sys, collections
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy
from kaggle_environments import make

DAY = 6
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
env.reset(2)
agent = SA.make_agent(thin, 0, router=True)
opp = tape_policy(replay, team, 1)

ours = collections.Counter()
his = collections.Counter()

for t in range(24 * (DAY + 1)):
    o0, o1 = env.state[0].observation, env.state[1].observation
    a0, a1 = agent(o0), opp(o1, t)
    n0 = len(o0["farms"][0].get("hands") or [])
    n1 = len(o0["farms"][1].get("hands") or [])

    if t // 24 == DAY:
        seeds = (o0.get("private") or {}).get("seeds") or {}
        mine = [o for o in (a0["market"] or []) if o and o[0] == "BUY_SEED"]
        theirs = [o for o in (a1["market"] or []) if o and o[0] == "BUY_SEED"]
        for o in mine:
            ours[o[1]] += int(o[2])
        for o in theirs:
            his[o[1]] += int(o[2])
        if mine or theirs:
            print(f"h{t % 24:>2} bank={int(o0['farms'][0]['money']):<6} seeds={dict(seeds)}")
            if mine:
                print(f"      ours {mine}")
            if theirs:
                print(f"      tape {theirs}")

    env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
              {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

end = (env.state[0].observation.get("private") or {}).get("seeds") or {}
print(f"\nBUY_SEED units OFFERED on day {DAY}:  ours {dict(ours)} = {sum(ours.values())}")
print(f"                                    tape {dict(his)} = {sum(his.values())}")
print(f"                       difference:  {sum(ours.values()) - sum(his.values())}")
print(f"seeds actually HELD at day {DAY} dusk, our seat: {dict(end)}")
