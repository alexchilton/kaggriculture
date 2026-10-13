"""Hour 0 of one day, ours against his, on every world. The first turn either matches or it does not.

Runs inside `breakdown` per world so the board and shops are the gate's own, captures the orders we
emit at the hour, and prints his beside them from the recording.

    python -u scripts/h0_across_worlds.py 7 0
"""
import sys, json, collections, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
DAY = int(sys.argv[1]) if len(sys.argv) > 1 else 7
HOUR = int(sys.argv[2]) if len(sys.argv) > 2 else 0
BUYABLE = ("WHEAT", "FERTILIZER")

RUNNER = '''import sys, json, collections, runpy
sys.path.insert(0, {root!r})
from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()
got = {{}}
_mk = SA.make_agent
def mk2(schedule, me=0, router=True):
    inner = _mk(schedule, me, router)
    def agent(obs):
        a = inner(obs)
        if obs.get("day") == {day} and obs.get("hour") == {hour} and not got:
            got["orders"] = [o for o in (a.get("market") or []) if o]
            got["cash"] = obs["farms"][0]["money"]
        return a
    return agent
SA.make_agent = mk2
sys.argv = ["breakdown.py", "--tape", {tape!r}, "--handover", "7", "--days", "{days}",
            "--diff", "--seed", "666671489"]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    try:
        runpy.run_path({bd!r}, run_name="__main__")
    except SystemExit:
        pass
print(json.dumps(got))
'''

sys.path.insert(0, str(ROOT))
import scripts.breakdown as B

def norm(orders):
    c = collections.Counter()
    for o in orders:
        if not o:
            continue
        if o[0] == "BUY_PRODUCT" and len(o) > 1 and o[1] not in BUYABLE:
            continue                                  # discarded by the engine, not a difference
        key = o[0] if o[0] in ("HIRE", "BUY_LAND") else f"{o[0]} {o[1]}"
        c[key] += (int(o[2]) if len(o) > 2 and isinstance(o[2], int) else 1)
    return c

print(f"{'world':14s} {'match':>6}  ours -> his   (d{DAY} h{HOUR})")
worlds = sorted(k for k in B.TAPES if k.startswith("spa"))
ok = 0
for tape in worlds:
    script = ROOT / f"data/logs/h0_{tape}.py"
    script.write_text(RUNNER.format(root=str(ROOT), tape=tape, day=DAY, hour=HOUR,
                                    days=DAY + 1, bd=str(ROOT / "scripts/breakdown.py")))
    r = subprocess.run([str(ROOT / ".venv-sub/bin/python"), "-u", str(script)],
                       capture_output=True, text=True, cwd=str(ROOT))
    try:
        got = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        print(f"{tape:14s} {'ERR':>6}  {r.stdout[-160:]!r} {r.stderr[-160:]!r}")
        continue
    replay, _sch, team = B.TAPES[tape]
    rep = json.loads((ROOT / replay).read_text())
    seat = rep["info"]["TeamNames"].index(team)
    act = (rep["steps"][DAY * 24 + HOUR + 1][seat] or {}).get("action") or {}
    mine, theirs = norm(got.get("orders") or []), norm(act.get("market") or [])
    same = mine == theirs
    ok += same
    if same:
        print(f"{tape:14s} {'YES':>6}  {dict(mine)}")
    else:
        print(f"{tape:14s} {'no':>6}  ours {dict(mine)}")
        print(f"{'':14s} {'':>6}  his  {dict(theirs)}")
print(f"\n{ok}/{len(worlds)} worlds match at d{DAY} h{HOUR}")
