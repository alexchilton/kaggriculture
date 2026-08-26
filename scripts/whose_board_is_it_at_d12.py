"""At the handover to the solver, is our board his board? And who earns more after it?

Three statements have to be reconciled and cannot all be true:

1. d4-d11 replays his tape, so at d12 our board is close to his.
2. His selling is the main difference, and it is worth more than ours over d12-d23.
3. Replaying his sell schedule on our board clamps 271 of 797 units away for lack of stock.

(1) and (3) contradict each other directly. If our shed at d12 holds what his holds, his own orders
fit. This prints the two boards side by side at the handover, per product, and then the bank gained
by each side over d12-d23 -- so "he beats us in the solver" becomes a number instead of a claim.

**His board comes from the raw recording, not from `farms[1]` of our run.** Kawashigi is seat 0 in
his own game; `farms[1]` in our replay is his opponent. Reading the wrong seat has already produced
three wrong diagnoses in this repo.

    python -u scripts/whose_board_is_it_at_d12.py --seed 1240813987
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
TAPE = "data/seed_scripts/kawa_2026-08-24/97466318.json"
HIM = "カワシギ"


def tiles_summary(farm):
    kinds = collections.Counter()
    for row in farm.get("tiles") or []:
        for cell in row:
            if cell is None:
                kinds["(unowned/empty)"] += 1
            elif isinstance(cell, dict):
                kinds[str(cell.get("kind") or cell.get("crop") or "?")] += 1
    return kinds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1240813987)
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--at", type=int, default=12, help="handover day")
    ap.add_argument("--until", type=int, default=24, help="end of the solver zone (exclusive)")
    args = ap.parse_args()

    from kaggle_environments import make

    SA = importlib.import_module(f"kagg.search.{args.module}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads((REPO / TAPE).read_text())
    steps = rec["steps"]
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index(HIM) if HIM in names else 0
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)

    # ---- his own recorded board, from the recording ---------------------------------------
    def his_state(day):
        t = day * TPD
        st = steps[t] if t < len(steps) else steps[-1]
        obs = st[0].get("observation") or {}
        farm = (obs.get("farms") or [{}])[his]
        priv = (st[his].get("observation") or {}).get("private") or {}
        return farm, {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}

    # ---- our board, playing him -------------------------------------------------------------
    env = make("kaggriculture", configuration=dict(cfg, seed=args.seed), debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    ours_at = {}
    for t in range(30 * TPD):
        o = env.state[0].observation
        day, hour = t // TPD, t % TPD
        if hour == 0 and day in (args.at, args.until):
            priv = o.get("private") or {}
            ours_at[day] = (dict(o["farms"][0]),
                            {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()})
        a = me(o, env.configuration)
        at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
        at = at if isinstance(at, dict) else {}
        n0 = len(o["farms"][0].get("hands") or [])
        n1 = len(o["farms"][1].get("hands") or [])
        env.step([
            {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n0], "market": a["market"]},
            {"farmer": at.get("farmer") or ["PASS"], "hands": list(at.get("hands") or [])[:n1],
             "market": at.get("market") or []},
        ])
        if env.done:
            break

    our_farm_a, our_shed_a = ours_at[args.at]
    our_farm_b, our_shed_b = ours_at[args.until]
    his_farm_a, his_shed_a = his_state(args.at)
    his_farm_b, his_shed_b = his_state(args.until)

    print(f"seed {args.seed}   handover d{args.at}   zone d{args.at}-d{args.until - 1}\n")

    print(f"=== the shed at d{args.at} h0 ===")
    print(f"{'product':<14}{'ours':>8}{'his':>8}{'diff':>8}")
    for p in sorted(set(our_shed_a) | set(his_shed_a)):
        o, h = our_shed_a.get(p, 0), his_shed_a.get(p, 0)
        print(f"{p:<14}{o:>8}{h:>8}{o - h:>+8}")
    print(f"{'TOTAL':<14}{sum(our_shed_a.values()):>8}{sum(his_shed_a.values()):>8}"
          f"{sum(our_shed_a.values()) - sum(his_shed_a.values()):>+8}")

    print(f"\n=== the farm at d{args.at} h0 ===")
    print(f"{'':<14}{'ours':>8}{'his':>8}")
    for label, key in (("money", "money"), ("hands", "hands")):
        o = our_farm_a.get(key)
        h = his_farm_a.get(key)
        o = len(o) if isinstance(o, list) else o
        h = len(h) if isinstance(h, list) else h
        print(f"{label:<14}{o if o is not None else '-':>8}{h if h is not None else '-':>8}")
    ot, ht = tiles_summary(our_farm_a), tiles_summary(his_farm_a)
    for k in sorted(set(ot) | set(ht)):
        print(f"{k:<14}{ot.get(k, 0):>8}{ht.get(k, 0):>8}")

    print(f"\n=== what the solver zone earned, d{args.at} -> d{args.until} ===")
    om = float(our_farm_b.get("money", 0)) - float(our_farm_a.get("money", 0))
    hm = float(his_farm_b.get("money", 0)) - float(his_farm_a.get("money", 0))
    print(f"{'':<14}{'ours':>12}{'his':>12}{'his - ours':>13}")
    print(f"{'bank at d' + str(args.at):<14}{float(our_farm_a.get('money', 0)):>12,.0f}"
          f"{float(his_farm_a.get('money', 0)):>12,.0f}"
          f"{float(his_farm_a.get('money', 0)) - float(our_farm_a.get('money', 0)):>+13,.0f}")
    print(f"{'bank at d' + str(args.until):<14}{float(our_farm_b.get('money', 0)):>12,.0f}"
          f"{float(his_farm_b.get('money', 0)):>12,.0f}"
          f"{float(his_farm_b.get('money', 0)) - float(our_farm_b.get('money', 0)):>+13,.0f}")
    print(f"{'GAINED':<14}{om:>12,.0f}{hm:>12,.0f}{hm - om:>+13,.0f}")
    print("\nHis column is his OWN recorded game against Leon, not a replay against us -- he is")
    print("richer there than he would be selling into our book. It is an upper bound on him.")


if __name__ == "__main__":
    main()
