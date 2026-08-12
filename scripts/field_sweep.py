"""Sweep a module flag against a FIELD of recorded ladder opponents, not against ourselves.

`scripts/goose_sweep.py` plays each arm against a frozen copy of our own agent. That answers "what
is best if both sides play it" -- a symmetric equilibrium -- and CLAUDE.md records that the mirror
has already pointed this project the wrong way once (melon 25 -> 12 -> 25). It is worse than merely
uninformative here: a mirror puts TEN cows on both sides of a milk book, gluts it by construction,
and then measures the glut. No real pairing does that -- every opponent in our recordings runs
COW 8 / SHEEP 6 against our COW 10 / SHEEP 4.

**Replaying a recorded opponent is fair in THIS competition specifically.** The top agents submit a
fixed 720-turn script rather than a policy, so a recorded action stream replayed on a fresh board is
not an approximation of the opponent -- it is exactly what they do on the ladder. The usual "a tape
is not their game" caveat applies to reactive agents and largely dissolves for open-loop ones.

What this still is not: the ladder. The field is the opponents we happened to record, weighted by
how often we drew them, and it is a sample of games Alex kept -- which skews to losses. Read it as
"does this change beat these opponents", never as a rating.

    PYTHONPATH=. .venv/bin/python -u scripts/field_sweep.py --flag HERD_GEESE --values 0,2 --seeds 4
"""
import argparse
import collections
import json
import pathlib
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
PLAN = REPO / "data/seed_scripts/victor/schedule.json"
FIELD = REPO / "data/seed_scripts/field"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders",
             "money_dawn", "money_dusk", "bank", "tiles", "weeds")


def _schedule():
    raw = json.loads(PLAN.read_text())
    return {int(k): {kk: vv for kk, vv in row.items() if kk not in TAPE_ONLY}
            for k, row in raw.items()}


def _opponents(limit=None, min_money=0):
    """The recorded field, richest first. Our own seat is excluded, and so are errored games."""
    out = []
    for p in sorted(FIELD.glob("*.json")):
        rec = json.loads(p.read_text())
        if rec["team"] == "alex chilton" or rec.get("their_money") is None:
            continue
        if rec["their_money"] < min_money:
            continue
        out.append((p.name, rec["team"], rec["their_money"]))
    out.sort(key=lambda r: -r[2])
    return out[:limit] if limit else out


def _play(job):
    """One seating of one seed against one recorded opponent."""
    flag, value, seed, opp_file, swapped = job
    from kaggle_environments import make

    from kagg.search import schedule_agent_1455mh as SA

    setattr(SA, flag, value)
    me_seat = 1 if swapped else 0
    me = SA.make_agent(_schedule(), me_seat, router=True)

    acts = json.loads((FIELD / opp_file).read_text())["actions"]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}

    def them(obs, config=None):
        t = int(obs.get("step", 0) or 0)
        if t >= len(acts):
            return idle
        farmer, hands, market = acts[t]
        owned = len((obs.get("farms") or [{}, {}])[1 - me_seat].get("hands") or [])
        return {"farmer": list(farmer), "hands": [list(h) for h in hands[:owned]],
                "market": [list(o) for o in market]}

    pair = (them, me) if swapped else (me, them)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(list(pair))
    final = env.steps[-1]
    mine = float(final[me_seat]["reward"] or 0)
    theirs = float(final[1 - me_seat]["reward"] or 0)
    return value, opp_file, seed, mine, theirs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--flag", required=True,
                    help="module-level name on schedule_agent_1455mh to sweep, e.g. CARROT_LATE")
    ap.add_argument("--values", required=True, help="comma-separated, e.g. 0,1")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--first-seed", type=int, default=1300)
    ap.add_argument("--opponents", type=int, default=24)
    ap.add_argument("--min-money", type=int, default=40000,
                    help="drop the recorded seats that banked less than this; a farm that did "
                         "nothing contests no market and measures nothing")
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()

    values = [int(v) for v in args.values.split(",") if v.strip()]
    seeds = list(range(args.first_seed, args.first_seed + args.seeds))
    field = _opponents(args.opponents, args.min_money)
    jobs = [(args.flag, v, s, f, sw)
            for v in values for s in seeds for f, _t, _m in field for sw in (False, True)]

    print(f"{args.flag} {values} against {len(field)} recorded ladder opponents")
    print(f"seeds {seeds[0]}-{seeds[-1]}, both seatings, weeds at the env default = {len(jobs)} games")
    print(f"field: {', '.join(t for _f, t, _m in field[:8])}"
          f"{' ...' if len(field) > 8 else ''}\n")

    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(_play, jobs))

    per = collections.defaultdict(list)
    per_opp = collections.defaultdict(list)
    for value, opp, seed, mine, theirs in rows:
        per[value].append((mine, theirs))
        per_opp[(value, opp)].append((mine, theirs))

    print(f"  {'value':>6} {'games':>6} {'win':>7} {'draw':>6} {'mean ours':>11} "
          f"{'mean theirs':>12} {'mean margin':>12}")
    for v in values:
        rs = per[v]
        w = sum(1 for m, t in rs if m > t)
        d = sum(1 for m, t in rs if m == t)
        print(f"  {v:>6} {len(rs):>6} {w / len(rs):>6.1%} {d / len(rs):>5.1%} "
              f"{statistics.mean(m for m, _ in rs):>11,.0f} "
              f"{statistics.mean(t for _, t in rs):>12,.0f} "
              f"{statistics.mean(m - t for m, t in rs):>12,.0f}")

    names = {f: t for f, t, _m in field}
    print(f"\n  win rate per opponent")
    print(f"  {'opponent':<26}" + "".join(f"{v:>10}" for v in values))
    for f, t, _m in field:
        cells = []
        for v in values:
            rs = per_opp[(v, f)]
            cells.append(f"{sum(1 for m, th in rs if m > th) / len(rs):>10.0%}" if rs
                         else f"{'-':>10}")
        print(f"  {t[:25]:<26}" + "".join(cells))

    print(f"\n  {time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
