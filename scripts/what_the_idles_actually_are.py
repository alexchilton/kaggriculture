"""A PASS is not one thing. Split the idle turns by WHEN and by WHO, ours against the tape.

`breakdown.py` prints `idle` and `pass` as the same row, so the idle turns are explicit `PASS`
actions the agent emits -- not missing actions and not refused ops. That says nothing about why.

There are three very different reasons a unit passes, and they want different fixes:

    parked      the unit passed the WHOLE day. It was hired and never given a job at all.
    finished    a tail of passes at the end of the day after real work. The route ran out.
    stalled     passes in the MIDDLE of a day, between two working turns. The route had a
                gap -- this is the signature `_apply_precomputed` dropping a stop would leave.

Counted per unit-day, ours and the tape's, on each tape's own seed. A hired hand that parks all day
still costs its fibonacci hire price, so `parked` is money as well as turns.

Run on both arms:

    python -u scripts/what_the_idles_actually_are.py --tape kawashigi  --seed 1240813987
    python -u scripts/what_the_idles_actually_are.py --tape kawa_straw --seed 468411728
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
ZONES = (("d0-d3", 0, 3), ("d4-d11 tape", 4, 11),
         ("d12-d23 solver", 12, 23), ("d24-d29 planner", 24, 29))


def classify(day_actions):
    """`day_actions` is a list of ops for ONE unit over one day, in turn order."""
    ops = [a for a in day_actions]
    if not ops:
        return None
    work = [i for i, o in enumerate(ops) if o not in ("PASS", None)]
    if not work:
        return "parked", len(ops)
    tail = len(ops) - 1 - work[-1]
    gaps = sum(1 for i in range(work[0], work[-1]) if ops[i] in ("PASS", None))
    lead = work[0]
    return None, (lead, gaps, tail)


def collect(steps, seat):
    """Returns per-zone Counter of parked/stalled/finished/leading PASS turns."""
    out = {z: collections.Counter() for z, _a, _b in ZONES}
    # unit index -> list of ops, per day
    for day in range(30):
        per_unit = collections.defaultdict(list)
        for h in range(TPD):
            t = day * TPD + h
            if t >= len(steps):
                break
            a = steps[t][seat].get("action")
            if not isinstance(a, dict):
                continue
            acts = [a.get("farmer")] + list(a.get("hands") or [])
            for i, act in enumerate(acts):
                per_unit[i].append((act or ["PASS"])[0])
        zone = next((z for z, lo, hi in ZONES if lo <= day <= hi), None)
        if zone is None:
            continue
        for _i, ops in per_unit.items():
            r = classify(ops)
            if r is None:
                continue
            kind, payload = r
            if kind == "parked":
                out[zone]["parked_units"] += 1
                out[zone]["parked_turns"] += payload
            else:
                lead, gaps, tail = payload
                out[zone]["worked_units"] += 1
                out[zone]["lead"] += lead
                out[zone]["stalled"] += gaps
                out[zone]["finished"] += tail
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="kawashigi")
    ap.add_argument("--seed", type=int, default=1240813987)
    a = ap.parse_args()

    import breakdown as B
    ours_steps, tape_steps = None, None

    # Drive the same pairing breakdown.py uses: our agent on the seed, the tape's own actions.
    tape_path, sched_path, team = B.TAPES[a.tape]
    rec = json.loads((REPO / tape_path).read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index(team) if team in names else 0
    tape_steps = rec["steps"]

    import us_in_his_seat as U                                                # noqa: F401
    from kaggle_environments import make
    import importlib
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / sched_path).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=a.seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, 0)
    ours_steps = []
    for t in range(30 * TPD):
        o = env.state[0].observation
        n = len(o["farms"][0].get("hands") or [])
        act = agent(o)
        mine = {"farmer": act["farmer"], "hands": list(act["hands"] or [])[:n],
                "market": act["market"]}
        at = tape_steps[t + 1][his].get("action") if t + 1 < len(tape_steps) else None
        yours = at if isinstance(at, dict) else {"farmer": ["PASS"], "hands": [], "market": []}
        n2 = len(o["farms"][1].get("hands") or [])
        yours = {"farmer": yours.get("farmer") or ["PASS"],
                 "hands": list(yours.get("hands") or [])[:n2],
                 "market": yours.get("market") or []}
        ours_steps.append([{"action": mine}, {"action": yours}])
        env.step([mine, yours])
        if env.done:
            break

    mine_c = collect(ours_steps, 0)
    his_c = collect([[{"action": (s[his].get("action") if isinstance(s[his].get("action"), dict)
                                 else {})}] for s in tape_steps], 0)

    print(f"tape {a.tape}  seed {a.seed}\n")
    print(f"{'zone':<17} {'parked units':>14} {'parked turns':>14} {'lead':>8} "
          f"{'STALLED':>9} {'finished':>10}")
    print("  ours / tape")
    for z, _lo, _hi in ZONES:
        m, h = mine_c[z], his_c[z]
        print(f"{z:<17} {str(m['parked_units'])+'/'+str(h['parked_units']):>14} "
              f"{str(m['parked_turns'])+'/'+str(h['parked_turns']):>14} "
              f"{str(m['lead'])+'/'+str(h['lead']):>8} "
              f"{str(m['stalled'])+'/'+str(h['stalled']):>9} "
              f"{str(m['finished'])+'/'+str(h['finished']):>10}")


if __name__ == "__main__":
    main()
