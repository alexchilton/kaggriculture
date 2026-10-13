"""Capture the exact inputs to ONE market decision, so it can be replayed without the game.

The market block is a pure function of what it is handed: the observation (board, prices, cash,
crew), the schedule row, and the agent's own carried `state`. Running the whole nine-world gate to
see one hour's orders costs four minutes and, worse, a standalone lookalike harness does NOT
reproduce it -- `scripts/money_ledger.py` showed brunch d7 opening on $55 where the gate opens on
$7, and a cow filling where the gate never even orders one.

So the fixture is captured from INSIDE the gate and replayed against the same agent:

    python -u scripts/market_fixture.py spa_brunch 7 0        # capture
    python -u scripts/market_probe.py   spa_brunch 7 0        # replay, milliseconds, no game

`state` is the agent's own dict and carries counters (`bought`, `hired`, `ordered`, `pins`) that
decide what the turn asks for, so it has to travel with the observation or the replay is a different
turn. Stored as repr and re-read with `ast.literal_eval`, which keeps Counters and tuples honest.
"""
import sys, json, pathlib, runpy, pickle
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TAPE = sys.argv[1] if len(sys.argv) > 1 else "spa_brunch"
DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 7
HOUR = int(sys.argv[3]) if len(sys.argv) > 3 else 0
OUT = ROOT / f"data/fixtures/market_{TAPE}_d{DAY}h{HOUR}.pkl"
OUT.parent.mkdir(parents=True, exist_ok=True)

from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()

grabbed = {}
_mk = SA.make_agent
def mk2(schedule, me=0, router=True):
    inner = _mk(schedule, me, router)
    cell = {}
    def agent(obs):
        if obs.get("day") == DAY and obs.get("hour") == HOUR and not grabbed:
            # Snapshot BEFORE the turn runs, so the replay starts where this turn started.
            grabbed["obs"] = json.loads(json.dumps(obs, default=lambda o: o.__dict__
                                                   if hasattr(o, "__dict__") else str(o)))
            grabbed["schedule"] = schedule
            grabbed["state"] = pickle.dumps(getattr(inner, "state", None), 0) \
                if getattr(inner, "state", None) is not None else None
        return inner(obs)
    agent.inner = inner
    return agent
SA.make_agent = mk2

sys.argv = ["breakdown.py", "--tape", TAPE, "--handover", "7", "--days", str(DAY + 1),
            "--diff", "--seed", "666671489"]
try:
    runpy.run_path(str(ROOT / "scripts/breakdown.py"), run_name="__main__")
except SystemExit:
    pass

if not grabbed:
    print(f"NOTHING CAPTURED at {TAPE} d{DAY} h{HOUR}")
    raise SystemExit(1)
OUT.write_bytes(pickle.dumps({"obs": grabbed["obs"], "schedule": grabbed["schedule"],
                              "tape": TAPE, "day": DAY, "hour": HOUR}))
f = grabbed["obs"]["farms"][0]
print(f"\ncaptured {TAPE} d{DAY} h{HOUR} -> {OUT}")
print(f"  cash {f['money']}  hands {len(f.get('hands') or [])}  "
      f"shed {dict(list((grabbed['obs'].get('private') or {}).get('shed', {}).items())[:6])}")
