"""Day 4 buys a cow and never places it. Where does it sit, and was a pen free?

`breakdown.py` day 4: buy_animal 1/1, place 0/1, and at day-5 dawn we hold 4 cows to the tape's 5.
So the purchase lands and the placement does not. This prints, for every hour of a chosen day, the
animals in the shed, the animals in each unit's hands, and the count of empty pens -- which
separates "the cow never arrived" from "the cow arrived and no node was built for it" from "the node
was built and never served".
"""
import argparse, collections, json, pathlib, sys
sys.path.insert(0, ".")
from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

ap = argparse.ArgumentParser()
ap.add_argument("--day", type=int, default=4)
ap.add_argument("--seed", type=int, default=11)
args = ap.parse_args()

replay, schedule, team = TAPES["seb"]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def trace(make0, label):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": args.seed, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = make0()
    opp = tape_policy(replay, team, 1)
    print(f"\n--- {label}")
    for t in range(24 * (args.day + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // 24 == args.day:
            shed = o0["private"]["shed"]
            animals = {k: v for k, v in shed.items() if k in ("COW", "SHEEP", "CHICKEN", "GOOSE")}
            inv = o0["private"].get("inventories") or []
            held = {i: {k: v for k, v in (d or {}).items() if k in ("COW", "SHEEP", "CHICKEN", "GOOSE")}
                    for i, d in enumerate(inv)}
            held = {i: d for i, d in held.items() if d}
            free = sum(1 for row in o0["farms"][0]["tiles"] for c in row
                       if isinstance(c, dict) and c.get("kind") in ("PASTURE", "COOP")
                       and not c.get("animal"))
            acts = [a0["farmer"]] + list(a0["hands"] or [])[:n0]
            doing = [f"u{i}:{a[0]}" for i, a in enumerate(acts) if a and a[0] in ("PICKUP", "PLACE", "DROP")]
            mk = [o for o in (a0["market"] or []) if o and o[0] == "BUY_ANIMAL"]
            if animals or held or doing or mk:
                print(f"  hr {t%24:>2} shed={animals} held={held} freepens={free} "
                      f"{' '.join(doing)} {mk if mk else ''}")
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])


agent = schedule_agent.make_agent(thin, 0, router=True)
trace(lambda: (lambda o, t: agent(o)), "OURS")
trace(lambda: tape_policy(replay, team, 0), "TAPE")
