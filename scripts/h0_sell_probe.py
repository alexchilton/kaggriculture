"""What capped our FERTILIZER offer at d7 h0, per world, against what he offered.

Records `reservation_units`' return inside the gate and prints it beside the quantity we actually
emitted. If emitted == reservation + 1 the `release` top-up is the difference, not the cap.

    python -u scripts/h0_sell_probe.py
"""
import sys, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent

RUNNER = '''import sys, json, runpy, io, contextlib
sys.path.insert(0, {root!r})
from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()
got, res = {{}}, []
_ru = SA.reservation_units
def ru2(prod, *a, **k):
    v = _ru(prod, *a, **k)
    res.append((prod, v))
    return v
SA.reservation_units = ru2
_mk = SA.make_agent
def mk2(schedule, me=0, router=True):
    inner = _mk(schedule, me, router)
    def agent(obs):
        del res[:]
        a = inner(obs)
        if obs.get("day") == 7 and obs.get("hour") == 0 and not got:
            got["orders"] = [o for o in (a.get("market") or []) if o]
            got["res"] = list(res)
            got["shed"] = dict((obs.get("private") or {{}}).get("shed") or {{}})
        return a
    return agent
SA.make_agent = mk2
sys.argv = ["breakdown.py", "--tape", {tape!r}, "--handover", "7", "--days", "8",
            "--diff", "--seed", "666671489"]
with contextlib.redirect_stdout(io.StringIO()):
    try:
        runpy.run_path({bd!r}, run_name="__main__")
    except SystemExit:
        pass
print(json.dumps(got))
'''

sys.path.insert(0, str(ROOT))
import scripts.breakdown as B

print(f"{'world':14s} {'shed':>5} {'ours':>5} {'his':>4} {'reservation_units':>18}")
for tape in sorted(k for k in B.TAPES if k.startswith("spa")):
    s = ROOT / f"data/logs/sp_{tape}.py"
    s.write_text(RUNNER.format(root=str(ROOT), tape=tape, bd=str(ROOT / "scripts/breakdown.py")))
    r = subprocess.run([str(ROOT / ".venv-sub/bin/python"), "-u", str(s)],
                       capture_output=True, text=True, cwd=str(ROOT))
    try:
        got = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        print(f"{tape:14s} ERR {r.stdout[-120:]!r} {r.stderr[-200:]!r}")
        continue
    replay, _sc, team = B.TAPES[tape]
    rep = json.loads((ROOT / replay).read_text())
    seat = rep["info"]["TeamNames"].index(team)
    act = (rep["steps"][7*24+1][seat] or {}).get("action") or {}
    his = sum(int(o[2]) for o in (act.get("market") or [])
              if o and o[0] == "SELL" and o[1] == "FERTILIZER")
    ours = sum(int(o[2]) for o in got.get("orders") or []
               if o and o[0] == "SELL" and o[1] == "FERTILIZER")
    fert = [v for p, v in got.get("res") or [] if p == "FERTILIZER"]
    print(f"{tape:14s} {got.get('shed',{}).get('FERTILIZER',0):>5} {ours:>5} {his:>4} {str(fert):>18}")
