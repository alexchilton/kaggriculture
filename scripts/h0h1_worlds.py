"""Our d7 h0 and h1, per world: what we offer, and the shed before and after.

One gate run per world, capturing both turns, so the h0 question ("did our whole fertilizer offer
fill, or did the book cap it?") and the h1 comparison come out of the same pass. His side is read
from the recording, whose observation at step i is the state AFTER step i-1.

    python -u scripts/h0h1_worlds.py
"""
import sys, json, collections, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
BUYABLE = ("WHEAT", "FERTILIZER")

RUNNER = '''import sys, json, runpy, io, contextlib
sys.path.insert(0, {root!r})
from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()
got = {{}}
_mk = SA.make_agent
def mk2(schedule, me=0, router=True):
    inner = _mk(schedule, me, router)
    def agent(obs):
        a = inner(obs)
        d, h = obs.get("day"), obs.get("hour")
        if d == 7 and h in (0, 1, 2) and str(h) not in got:
            got[str(h)] = {{"orders": [o for o in (a.get("market") or []) if o],
                           "shed": dict((obs.get("private") or {{}}).get("shed") or {{}})}}
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


def norm(orders):
    c = collections.Counter()
    for o in orders:
        if not o:
            continue
        if o[0] == "BUY_PRODUCT" and len(o) > 1 and o[1] not in BUYABLE:
            continue
        key = o[0] if o[0] in ("HIRE", "BUY_LAND") else f"{o[0]} {o[1]}"
        c[key] += (int(o[2]) if len(o) > 2 and isinstance(o[2], int) else 1)
    return c


for tape in sorted(k for k in B.TAPES if k.startswith("spa")):
    s = ROOT / f"data/logs/hh_{tape}.py"
    s.write_text(RUNNER.format(root=str(ROOT), tape=tape, bd=str(ROOT / "scripts/breakdown.py")))
    r = subprocess.run([str(ROOT / ".venv-sub/bin/python"), "-u", str(s)],
                       capture_output=True, text=True, cwd=str(ROOT))
    try:
        got = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        print(f"{tape:14s} ERR {r.stdout[-100:]!r} {r.stderr[-250:]!r}", flush=True)
        continue
    replay, _sc, team = B.TAPES[tape]
    rep = json.loads((ROOT / replay).read_text())
    seat = rep["info"]["TeamNames"].index(team)
    print(f"\n=== {tape} ===", flush=True)
    for h in (0, 1, 2):
        mine = got.get(str(h)) or {}
        act = (rep["steps"][7 * 24 + h + 1][seat] or {}).get("action") or {}
        his_shed = (((rep["steps"][7 * 24 + h][seat] or {}).get("observation") or {})
                    .get("private") or {}).get("shed") or {}
        a, bq = norm(mine.get("orders") or []), norm(act.get("market") or [])
        print(f"  h{h} {'MATCH' if a == bq else 'no   '}", flush=True)
        print(f"     ours {dict(a)}", flush=True)
        print(f"     his  {dict(bq)}", flush=True)
        print(f"     shed ours FERT {mine.get('shed', {}).get('FERTILIZER')} "
              f"WHEAT {mine.get('shed', {}).get('WHEAT')}   "
              f"his FERT {his_shed.get('FERTILIZER')} WHEAT {his_shed.get('WHEAT')}", flush=True)
