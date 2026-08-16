"""d0-d8 ops and buy/sell CADENCE for the leader's two branches and both of ours.

Four columns, accounted identically -- everything is read off the ACTION STREAM, so the same
thing is counted on every side:

    A3   92498144   his melon branch,      MELON 20 / STRAWBERRY 11 at d9, 3 quadrants
    B3   92466371   his strawberry branch, MELON 12 / STRAWBERRY 19 at d9, 3 quadrants
    M+   ours with the d3 fork forced ON   (OPPONENT_MELON = 0)
    M-   ours with the d3 fork forced OFF  (threshold 99)

## Offers are not fills, and this reports OFFERS on purpose

A market order is re-posted every turn until it fills, so summing them counts the same intent
many times -- `feedback_offers_are_not_fills`. This script does NOT sum them. For every market
op it reports the **distinct hours at which an order of that kind was on the book**, which is
the cadence question: WHEN does he commit the bank. Unit ops (PLANT, WATER, ...) are not
re-posted and are counted straight.

    python -u scripts/branch_cadence.py --days 8
"""
import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.search import melon_branch as _MB

UNIT_OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
            "BUILD_PASTURE", "BUILD_COOP", "PLACE", "FERTILIZE")
MARKET_OPS = ("SELL", "BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "BUY_LAND", "HIRE")
TAPES = {"A3": ("data/seed_scripts/kawashigi/92498144.json", "カワシギ"),
         "B3": ("data/seed_scripts/kawashigi/92466371.json", "カワシギ")}


def blank(days):
    return {"ops": [collections.Counter() for _ in range(days + 1)],
            "hours": [collections.defaultdict(set) for _ in range(days + 1)]}


def tally(acc, turn, action, days):
    day, hour = turn // 24, turn % 24
    if day > days:
        return
    for op in [action.get("farmer")] + list(action.get("hands") or []):
        if op and op[0] in UNIT_OPS:
            acc["ops"][day][op[0]] += 1
    for order in action.get("market") or []:
        if order and order[0] in MARKET_OPS:
            acc["hours"][day][order[0]].add(hour)


def from_replay(path, team, days):
    d = json.loads((REPO / path).read_text())
    names = (d.get("info") or {}).get("TeamNames") or []
    seat = names.index(team)
    acc = blank(days)
    for turn, step in enumerate(d["steps"]):
        act = step[seat].get("action")
        if isinstance(act, dict):
            tally(acc, turn, act, days)
    return acc


def from_ours(threshold, days):
    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    _MB.OPPONENT_MELON = threshold
    B.schedule_agent = SA
    replay, team = TAPES["A3"]
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    acc = blank(days)
    opp = lambda: B.tape_policy(str(REPO / replay), team, 1)          # noqa: E731

    def ours():
        a = SA.make_agent(sched, 0)

        def f(o, t):
            act = a(o)
            tally(acc, t, act, days)
            return act
        return f

    B.run(ours, opp, 11, 0.005, stop_day=days + 1)
    return acc


def child(threshold, days):
    import subprocess
    out = subprocess.run([sys.executable, "-u", __file__, "--child", str(threshold), str(days)],
                         capture_output=True, text=True, cwd=str(REPO))
    if out.returncode:
        raise SystemExit(out.stderr[-2000:])
    raw = json.loads(out.stdout)
    return {"ops": [collections.Counter(x) for x in raw["ops"]],
            "hours": [{k: set(v) for k, v in x.items()} for x in raw["hours"]]}


def main():
    if "--child" in sys.argv:
        i = sys.argv.index("--child")
        acc = from_ours(int(sys.argv[i + 1]), int(sys.argv[i + 2]))
        print(json.dumps({"ops": [dict(c) for c in acc["ops"]],
                          "hours": [{k: sorted(v) for k, v in h.items()} for h in acc["hours"]]}))
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=8)
    a = ap.parse_args()
    d = a.days

    cols = {"A3": from_replay(*TAPES["A3"], d), "B3": from_replay(*TAPES["B3"], d),
            "M+": child(0, d), "M-": child(99, d)}

    print("UNIT OPS, d0-d%d      A3 = his melon branch, B3 = his strawberry branch, "
          "M+/- = ours fork on/off\n" % d)
    for op in UNIT_OPS:
        if not any(c["ops"][x][op] for c in cols.values() for x in range(d + 1)):
            continue
        print(f"  {op}")
        for k, c in cols.items():
            print(f"     {k:>4}  " + "".join(f"{c['ops'][x][op]:>5}" for x in range(d + 1)))
        print(f"     {'day':>4}  " + "".join(f"{'d' + str(x):>5}" for x in range(d + 1)))

    print("\n\nBUY / SELL CADENCE -- the HOURS an order of that kind sat on the book\n")
    for op in MARKET_OPS:
        if not any(c["hours"][x].get(op) for c in cols.values() for x in range(d + 1)):
            continue
        print(f"  {op}")
        for k, c in cols.items():
            cells = []
            for x in range(d + 1):
                hs = sorted(c["hours"][x].get(op, ()))
                cells.append("-" if not hs else
                             (f"{hs[0]}-{hs[-1]}" if len(hs) > 2 else ",".join(map(str, hs))))
            print(f"     {k:>4}  " + "".join(f"{v:>8}" for v in cells))
        print(f"     {'day':>4}  " + "".join(f"{'d' + str(x):>8}" for x in range(d + 1)))


if __name__ == "__main__":
    main()
