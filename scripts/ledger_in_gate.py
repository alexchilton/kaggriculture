"""Per-hour orders, fills and cash -- measured INSIDE `breakdown`'s own run, not a lookalike.

A standalone harness that calls `breakdown.run` directly does NOT reproduce the gate: on brunch d7
it showed `BUY_ANIMAL COW` filling at hour 0 while the gate reported `fill.buy_animal 0/1` and a
dusk bank of 384. Whatever the difference is, the gate is the thing being matched, so the
instrumentation has to live inside it.

    python -u scripts/ledger_in_gate.py spa_brunch 7
"""
import sys, json, collections, pathlib, runpy
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TAPE = sys.argv[1] if len(sys.argv) > 1 else "spa_brunch"
DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 7
BUYABLE = ("WHEAT", "FERTILIZER")

from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()

seen = {}
_mk = SA.make_agent
def mk2(schedule, me=0, router=True):
    inner = _mk(schedule, me, router)
    def agent(obs):
        a = inner(obs)
        if obs.get("day") == DAY:
            f = obs["farms"][0]
            m = [o for o in (a.get("market") or [])
                 if o and not (o[0] == "BUY_PRODUCT" and len(o) > 1 and o[1] not in BUYABLE)]
            seen[obs["hour"]] = (float(f["money"]), len(f.get("hands") or []),
                                 [" ".join(str(x) for x in o) for o in m])
        return a
    return agent
SA.make_agent = mk2

sys.argv = ["breakdown.py", "--tape", TAPE, "--handover", "7", "--days", str(DAY + 1),
            "--diff", "--seed", "666671489"]
try:
    runpy.run_path(str(ROOT / "scripts/breakdown.py"), run_name="__main__")
except SystemExit:
    pass

import scripts.breakdown as B
row = json.loads((ROOT / B.TAPES[TAPE][1]).read_text())[str(DAY)]
print(f"\n==== {TAPE} d{DAY}  INSIDE the gate ====")
print(f"row: hands {row.get('hands')}  animals {row.get('animals_bought')}  "
      f"sells {row.get('sells')}  buys {row.get('buys')}")
print(f"animal costs {{k: cost}}: " + str({k: v['cost'] for k, v in SA.R.ANIMALS.items()}))
for h in sorted(seen):
    money, hands, orders = seen[h]
    if orders:
        print(f"  h{h:<3} cash {money:>7.0f}  hands {hands}  {orders}")
