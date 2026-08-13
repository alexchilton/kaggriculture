"""We stand 2 fewer SHEEP than the tape on every day from d10 to d29. Where do they go?

`breakdown.py`'s `sheep` row is `an_SHEEP` (breakdown.py:249) -- animals STANDING ON THE BOARD at
end of day, not an op count. It reads +1 at d6, blank d7-d9, then -2 flat from d10 through d29.

That does not obviously reconcile with `buy_animal +3`: we BUY more animals than the tape and end up
standing fewer sheep. Four things can produce that and they are different bugs:

  (a) we buy fewer SHEEP specifically (and more of something else)
  (b) we buy them and they never get placed -- they sit in the shed
  (c) we place them and they die of starvation
  (d) we never build the pasture to put them in

This prints, per day, for BOTH seats: sheep standing, sheep in the shed, empty pens, total pens, and
the SHEEP buy/place op counts. The column that first diverges names the bug.
"""
import json
import pathlib
import sys

sys.path.insert(0, "/Users/alexchilton/DataspellProjects/kaggriculture")

from kaggle_environments import make

from kagg.search import schedule_agent as SA
from scripts.breakdown import DEFAULT_TAPE, TAPES, TAPE_ONLY, tape_policy

DAYS = 30
replay, schedule, team = TAPES[DEFAULT_TAPE]
sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def census(obs):
    """Sheep standing, sheep in shed, empty pens, total pens -- all at the moment of the call."""
    farm = obs["farms"][0]
    priv = obs.get("private") or {}
    standing = empty = pens = 0
    for row in farm["tiles"]:
        for cell in row:
            if not isinstance(cell, dict):
                continue
            if cell.get("kind") in ("PASTURE", "COOP"):
                pens += 1
                if cell.get("animal") == "SHEEP":
                    standing += 1
                elif not cell.get("animal"):
                    empty += 1
    shed = int((priv.get("shed") or {}).get("SHEEP", 0))
    carried = sum(int((iv or {}).get("SHEEP", 0)) for iv in (priv.get("inventories") or []))
    return standing, shed + carried, empty, pens


def run(make_seat0, label):
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    p0 = make_seat0()
    opp = tape_policy(replay, team, 1)
    rows, bought, placed = {}, {}, {}
    for t in range(24 * DAYS - 1):
        day = t // 24
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for o in (a0["market"] or []):
            if o and o[0] == "BUY_ANIMAL" and o[1] == "SHEEP":
                bought[day] = bought.get(day, 0) + 1
        for act in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
            if act and act[0] == "PLACE" and len(act) > 1 and act[1] == "SHEEP":
                placed[day] = placed.get(day, 0) + 1
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
        if t % 24 == 23:
            rows[day] = census(env.state[0].observation)
    print(f"\n===== {label} =====")
    print("  day  standing  in_shed  empty_pens  pens  buy_offers  place_ops")
    for d in sorted(rows):
        st, sh, em, pn = rows[d]
        print(f"  d{d:<3} {st:>7}  {sh:>7}  {em:>10}  {pn:>4}  {bought.get(d, 0):>10}  "
              f"{placed.get(d, 0):>9}")
    return rows


ours = run(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)), "OURS")
his = run(lambda: tape_policy(replay, team, 0), "SEB (the tape)")

print("\n===== OURS MINUS TAPE (standing, in_shed, empty_pens, pens) =====")
print("  day  standing  in_shed  empty_pens  pens")
for d in sorted(set(ours) & set(his)):
    delta = tuple(a - b for a, b in zip(ours[d], his[d]))
    if any(delta):
        print(f"  d{d:<3} {delta[0]:>7}  {delta[1]:>7}  {delta[2]:>10}  {delta[3]:>4}")
