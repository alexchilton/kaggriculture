"""Every unit's action, every turn, for one day. The per-turn table is what finds these, not reasoning.

Season aggregates said PICKUP 62 on day 0 against a crew of five to eight -- roughly half of every turn
the farm had spent walking to the shed and drawing one thing. Two candidate causes survive the unit
tests (a partial draw that never completes, and a replan re-issuing a draw each time a hand is hired),
and they are distinguishable only by looking at the turns.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import schedule_agent
import agent_ladder as L


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    want_day = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    _mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    env = L._env(seed, 0.0)
    us = schedule_agent.make_agent(sched, 0, router=True)
    tally = collections.Counter()
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        if day > want_day:
            break
        farm = obs["farms"][0]
        ours = us(obs)
        if day == want_day:
            pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
            acts = [ours["farmer"], *ours["hands"]][:len(pos)]
            cells = []
            for (x, y), a in zip(pos, acts):
                op = a[0] if isinstance(a, list) and a else "?"
                tally[op] += 1
                cells.append(f"{x}{y}:{op[:5]}")
            invs = obs["private"].get("inventories") or []
            carry = collections.Counter()
            for iv in invs:
                carry.update(iv)
            print(f"  h{hour:>2} ${int(farm['money']):>6} shed{dict(obs['private'].get('shed') or {})}"
                  f" carry{dict(carry)}")
            print(f"        {' '.join(cells)}")
            if ours["market"]:
                print(f"        market {ours['market']}")
        n0 = len(farm.get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": ours["farmer"], "hands": list(ours["hands"])[:n0],
                   "market": ours["market"]},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    print(f"\n  day {want_day} ops: {dict(tally)}")


if __name__ == "__main__":
    main()
