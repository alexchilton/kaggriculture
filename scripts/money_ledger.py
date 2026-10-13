"""One world, one day, hour by hour: every order, what it settled, and the cash before and after.

Built because the nine-world cell count cannot localise anything. It says a field differs; it never
says which hour, which order, or which dollar. Five speculative market changes in a row measured
worse, and none of them was aimed at a hour that had been read.

Money appears here as the MECHANISM under investigation -- whether a purchase the row names can be
paid for when its slot settles -- never as a score. The gate is still the board.

    python -u scripts/money_ledger.py spa_brunch 7
"""
import sys, json, collections, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kagg.search import schedule_agent as SA
SA.REPLAY_OPENING_DAYS = ()
import scripts.breakdown as B, kagg.plan as P

BUYABLE = ("WHEAT", "FERTILIZER")
TAPE = sys.argv[1] if len(sys.argv) > 1 else "spa_brunch"
DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 7

replay, schedule, team = B.TAPES[TAPE]
r = json.loads((ROOT / replay).read_text()); seat = r["info"]["TeamNames"].index(team)
sched = {int(k): {kk: vv for kk, vv in row.items() if kk not in P.TAPE_ONLY}
         for k, row in json.loads((ROOT / schedule).read_text()).items()}
econ = B.env_config(str(ROOT / replay)); shops = B.recorded_shops(str(ROOT / replay))
opp = lambda: B.tape_policy(str(ROOT / replay), r["info"]["TeamNames"][1 - seat], 1)

def run(inner_f, label, out, ev=None):
    def maker():
        inner = inner_f()
        def pol(obs, t):
            a = inner(obs, t)
            if obs.get("day") == DAY:
                f = obs["farms"][0]
                m = [o for o in (a.get("market") or [])
                     if o and not (o[0] == "BUY_PRODUCT" and len(o) > 1 and o[1] not in BUYABLE)]
                out[obs["hour"]] = (float(f["money"]), len(f.get("hands") or []),
                                    [" ".join(str(x) for x in o) for o in m])
            return a
        return pol
    from kagg.analysis.fills import record_fills
    with record_fills() as _f:
        B.run(maker, opp, 666671489, 0.0, stop_day=DAY + 1, economy=econ, shops=shops)
    if ev is not None:
        for e in _f.events:
            if e.get("seat") == 0 and e.get("day") == DAY:
                ev.setdefault(e.get("hour"), collections.Counter())[
                    f"{e['op']} {e.get('item')}"] += 1

his, ours = {}, {}
his_ev, our_ev = {}, {}
run(lambda: B.tape_policy(str(ROOT / replay), team, 0), "his", his, his_ev)
def our_inner():
    ag = SA.make_agent(sched, 0, router=True)
    tp = B.tape_policy(str(ROOT / replay), team, 0)
    return lambda obs, t: ag(obs) if obs.get("day") >= DAY else tp(obs, t)
run(our_inner, "ours", ours, our_ev)

row = sched[DAY]
print(f"==== {TAPE} d{DAY} ====")
print(f"row: hands {row.get('hands')}  animals {row.get('animals_bought')}  "
      f"sells {row.get('sells')}  buys {row.get('buys')}  builds {row.get('builds')}")
print(f"animal costs: " + str({k: v['cost'] for k, v in SA.R.ANIMALS.items()}))
print(f"\n{'h':>3} {'OURS cash':>10} {'hands':>5}  orders")
for h in range(24):
    om, on, oo = ours.get(h, (0, 0, []))
    hm, hn, ho = his.get(h, (0, 0, []))
    if not oo and not ho:
        continue
    print(f"{h:>3} {om:>10.0f} {on:>5}  {oo}")
    print(f"{'':>3} {'':>10} {'':>5}  FILLED {dict(our_ev.get(h, {}))}")
    print(f"    {hm:>10.0f} {hn:>5}  HIS {ho}")
    print(f"{'':>3} {'':>10} {'':>5}  HIS FILLED {dict(his_ev.get(h, {}))}")
