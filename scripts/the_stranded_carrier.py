"""Two fertilizer sit in hands from mid-afternoon on day 6 and reach the shed only overnight.

`test_the_afternoons_collections_reach_the_shed_before_the_market_closes` is xfailed on that. The
delivery-threshold fix for it was measured and rejected (see `MIN_SELL_ROW_DROP`), and the claim
left behind was that the real defect is upstream -- a carrier that stops working and never goes
home. This prints, for every hour of day 6, each unit's tile, what it is holding, and the action it
submitted, so that claim can be checked rather than asserted.

The depot ring is exactly (4,4), (4,5), (5,4), (5,5). A unit at (4,3) is ADJACENT to it, not on it,
and cannot DROP there -- worth stating because the first pass at this got that wrong.
"""
import json, pathlib, sys
sys.path.insert(0, ".")
from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy, DEFAULT_TAPE
from kaggle_environments import make

DAY = 6
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
env.reset(2)
agent = SA.make_agent(thin, 0, router=True)
opp = tape_policy(replay, team, 1)

print(f"depots = {sorted(SA.SHED)}   row for day {DAY} = {sched[DAY].get('orders')}")

for t in range(24 * (DAY + 1)):
    o0, o1 = env.state[0].observation, env.state[1].observation
    a0, a1 = agent(o0), opp(o1, t)
    n0 = len(o0["farms"][0].get("hands") or [])
    n1 = len(o0["farms"][1].get("hands") or [])
    acts = list(a0["hands"])[:n0]

    if t // 24 == DAY:
        # Unit 0 is the farmer; `hands` and `inventories` both run farmer-first.
        units = [o0["farms"][0].get("farmer")] + list(o0["farms"][0].get("hands") or [])
        invs = o0["private"].get("inventories") or []
        allacts = [a0["farmer"]] + acts
        cells = []
        for i, h in enumerate(units):
            if h is None:
                continue
            pos = tuple(h[:2]) if isinstance(h, (list, tuple)) else (h.get("x"), h.get("y"))
            inv = {k: v for k, v in (invs[i] or {}).items() if v} if i < len(invs) else {}
            act = allacts[i] if i < len(allacts) else None
            op = (act[0] if act else "-")
            mark = "@" if pos in SA.SHED else " "
            cells.append(f"u{i}{mark}{pos[0]},{pos[1]} {op:<8}{inv if inv else ''}")
        sells = [o for o in (a0["market"] or []) if o and o[0] == "SELL"]
        print(f"h{t % 24:>2} shed_fert={int(o0['private']['shed'].get('FERTILIZER', 0)):<3} "
              f"| " + " | ".join(cells) + (f"  SELL {sells}" if sells else ""))

    env.step([{"farmer": a0["farmer"], "hands": acts, "market": a0["market"]},
              {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
