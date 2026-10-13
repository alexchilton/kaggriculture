"""Replay ONE captured market decision, with no game running.

    python -u scripts/market_probe.py spa_brunch 7 0

Prints the orders the market block emits for that exact turn. Iterating on the market rules costs
milliseconds here instead of four minutes on the nine-world gate, and the inputs are the gate's own
because `scripts/market_fixture.py` captured them from inside it.

**What this CAN answer:** what the block decides, given a state. Slot order, which orders are
emitted at all, what a funding test refuses.

**What it CANNOT answer:** what the engine then settles, or anything downstream on the board. A
decision that looks right here still has to be measured on the gate -- this narrows where to look,
it does not replace the measurement.
"""
import sys, pathlib, pickle
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TAPE = sys.argv[1] if len(sys.argv) > 1 else "spa_brunch"
DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 7
HOUR = int(sys.argv[3]) if len(sys.argv) > 3 else 0
fx = pickle.loads((ROOT / f"data/fixtures/market_{TAPE}_d{DAY}h{HOUR}.pkl").read_bytes())

from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()
agent = SA.make_agent(fx["schedule"], 0, router=True)
act = agent(fx["obs"])

obs = fx["obs"]; f = obs["farms"][0]
row = fx["schedule"].get(DAY) or fx["schedule"].get(str(DAY)) or {}
print(f"==== {TAPE} d{DAY} h{HOUR}  (replayed, no game) ====")
print(f"cash {f['money']}  hands {len(f.get('hands') or [])}  "
      f"shed_wheat {(obs.get('private') or {}).get('shed', {}).get('WHEAT')}")
print(f"row: hands {row.get('hands')}  animals {row.get('animals_bought')}  "
      f"sells {row.get('sells')}  buys {row.get('buys')}  seeds {row.get('seeds')}")
print(f"prices: {(obs.get('market') or {}).get('prices')}")
print(f"\nORDERS EMITTED:")
for o in (act.get("market") or []):
    print(f"   {' '.join(str(x) for x in o)}")
