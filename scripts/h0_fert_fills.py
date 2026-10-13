"""How many of our h0 FERTILIZER units actually TRADE, per world.

An offer is not a fill. We offer the whole shed at d7 h0 and he offers one less on seven of nine
worlds; this says whether the extra unit finds a buyer or is refused by the book. Fertilizer is the
one product the town centre never buys (`reference/kaggriculture.py:114`), so the only demand is the
shops that world unlocked.

    python -u scripts/h0_fert_fills.py
"""
import sys, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent

RUNNER = '''import sys, json, runpy, io, contextlib
sys.path.insert(0, {root!r})
from kagg.search import schedule_agent as SA
from kagg.analysis.fills import record_fills
SA.REPLAY_OPENING_DAYS = ()
got = {{}}
_mk = SA.make_agent
def mk2(schedule, me=0, router=True):
    inner = _mk(schedule, me, router)
    def agent(obs):
        a = inner(obs)
        if obs.get("day") == 7 and obs.get("hour") == 0 and "orders" not in got:
            got["orders"] = [o for o in (a.get("market") or []) if o]
        return a
    return agent
SA.make_agent = mk2
sys.argv = ["breakdown.py", "--tape", {tape!r}, "--handover", "7", "--days", "8",
            "--diff", "--seed", "666671489"]
with record_fills() as fills:
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            runpy.run_path({bd!r}, run_name="__main__")
        except SystemExit:
            pass
got["h0"] = [(e["op"], e["item"]) for e in fills.events
             if e["seat"] == 0 and e["day"] == 7 and e["hour"] == 0]
got["day"] = sum(1 for e in fills.events
                 if e["seat"] == 0 and e["day"] == 7 and e["op"] == "SELL"
                 and e["item"] == "FERTILIZER")
print(json.dumps(got))
'''

sys.path.insert(0, str(ROOT))
import scripts.breakdown as B

print(f"{'world':14s} {'offer':>6} {'filled h0':>10} {'his offer':>10} {'our d7 fert sold':>17}")
for tape in sorted(k for k in B.TAPES if k.startswith("spa")):
    s = ROOT / f"data/logs/ff_{tape}.py"
    s.write_text(RUNNER.format(root=str(ROOT), tape=tape, bd=str(ROOT / "scripts/breakdown.py")))
    r = subprocess.run([str(ROOT / ".venv-sub/bin/python"), "-u", str(s)],
                       capture_output=True, text=True, cwd=str(ROOT))
    try:
        got = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        print(f"{tape:14s} ERR {r.stdout[-100:]!r} {r.stderr[-250:]!r}")
        continue
    offer = sum(int(o[2]) for o in got["orders"]
                if o and o[0] == "SELL" and o[1] == "FERTILIZER")
    filled = sum(1 for op, it in got["h0"] if op == "SELL" and it == "FERTILIZER")
    replay, _sc, team = B.TAPES[tape]
    rep = json.loads((ROOT / replay).read_text())
    seat = rep["info"]["TeamNames"].index(team)
    act = (rep["steps"][7*24+1][seat] or {}).get("action") or {}
    his = sum(int(o[2]) for o in (act.get("market") or [])
              if o and o[0] == "SELL" and o[1] == "FERTILIZER")
    print(f"{tape:14s} {offer:>6} {filled:>10} {his:>10} {got['day']:>17}")
