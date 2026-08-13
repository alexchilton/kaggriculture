"""The starving pen is already priced to prevent its own escape. So why is it never served?

`router.animal_ops` gates the whole FEED op on `have_wheat`:

    if not fed and have_wheat:
        hungry = cell.get("consecutive_unfed", 0) >= 1
        prize = MANDATORY + price + ((a["cost"] + _animal_remaining(cell, day)) if hungry else 0)

A pen at `consecutive_unfed >= 1` therefore already carries the escape-prevention bonus, and the
trace still shows (8,0) sitting at 1 for the whole of day 16 and escaping at dusk. So the prize is
not the binding constraint. `have_wheat` is the candidate: with no wheat the FEED node is not built
at ALL, and an op that does not exist cannot be outbid at any price.

`sh:wheat` runs -139 against the tape, so this is worth checking rather than assuming.

Prints, for each turn of days 15-18: wheat in the shed, wheat carried by units, how many pens are
hungry, and how many of them are at consecutive_unfed >= 1 (one day from escaping).
"""
import json
import pathlib
import sys

sys.path.insert(0, "/Users/alexchilton/DataspellProjects/kaggriculture")

from kaggle_environments import make

from kagg.search import schedule_agent as SA
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy

LO, HI = 15, 18
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def run(make_seat0, label):
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = make_seat0()
    opp = tape_policy(replay, team, 1)
    print(f"\n===== {label} =====")
    print("  day  hour  shed_WHEAT  carried_WHEAT  hungry  at_risk(unfed>=1)  FEED_emitted")
    for t in range(24 * (HI + 1) - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        day, hour = t // 24, t % 24
        if LO <= day <= HI and hour % 4 == 0:
            priv = o0.get("private") or {}
            shed = int((priv.get("shed") or {}).get("WHEAT", 0))
            carried = sum(int((iv or {}).get("WHEAT", 0)) for iv in (priv.get("inventories") or []))
            hungry = at_risk = 0
            for row in o0["farms"][0]["tiles"]:
                for c in row:
                    if isinstance(c, dict) and c.get("animal") and not c.get("fed_today"):
                        hungry += 1
                        at_risk += int(c.get("consecutive_unfed", 0)) >= 1
            feeds = sum(1 for act in [a0["farmer"]] + list(a0["hands"] or [])[:n0]
                        if act and act[0] == "FEED")
            flag = "   <-- NO WHEAT, no FEED node buildable" if not (shed + carried) and at_risk else ""
            print(f"  d{day:<3} h{hour:<4} {shed:>10}  {carried:>13}  {hungry:>6}  {at_risk:>17}  "
                  f"{feeds:>12}{flag}")
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break


run(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)), "OURS")
run(lambda: tape_policy(replay, team, 0), "SEB (the tape)")
