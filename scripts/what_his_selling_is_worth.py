"""Is his selling really worth ~$7k more than ours over the solver zone? Exact fills, both seats.

Two numbers have been sitting next to each other without being reconciled:

- "his selling is the main thing different and is 7k more than ours in value for the solver"
- forcing his order quantities onto our board costs $35,741 a season across 12 seeds

Those are compatible only if he gets a better price per unit while selling a total volume that is
too small for our farm. This measures both halves so the claim stops being an assertion:

    units, revenue and $/unit, per seat, per product, over d12-d23 -- from `record_fills`, which
    wraps `_commit_unit` and is the only exact source. Offers are not fills.

Both seats play their own game: our live agent on seat 0, his recorded actions on seat 1. That is
the same setup `scripts/breakdown.py` uses, so the tape column is a REPLAYED Kawashigi and is
poorer than his real one -- we sell into the same book. That is the right comparison here anyway:
the question is what his selling is worth against us, not what it was worth against Leon.

    python -u scripts/what_his_selling_is_worth.py --seed 1240813987 --zone 12-23
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1240813987)
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--zone", default="12-23")
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.zone.split("-"))

    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

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

    with record_fills() as fills:
        env = make("kaggriculture", configuration=dict(cfg, seed=args.seed), debug=False)
        env.reset(2)
        me = SA.make_agent(sched, 0, router=True)
        for t in range(30 * TPD):
            o = env.state[0].observation
            a = me(o, env.configuration)
            at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
            at = at if isinstance(at, dict) else {}
            n0 = len(o["farms"][0].get("hands") or [])
            n1 = len(o["farms"][1].get("hands") or [])
            env.step([
                {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n0], "market": a["market"]},
                {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n1],
                 "market": at.get("market") or []},
            ])
            if env.done:
                break
        farms = env.state[0].observation["farms"]
        banks = (float(farms[0]["money"]), float(farms[1]["money"]))

    # ---- per seat, per product, inside the zone --------------------------------------------
    per = collections.defaultdict(lambda: [0, 0.0])       # (seat, item) -> [units, revenue]
    turns = collections.defaultdict(set)                  # seat -> {(day, hour)}
    lots = collections.defaultdict(collections.Counter)   # seat -> {(day,hour,item): units}
    for seat in (0, 1):
        for day, hour, op, item, price in fills.at_turn(seat, op="SELL"):
            if day is None or not (lo <= day <= hi):
                continue
            per[(seat, item)][0] += 1
            per[(seat, item)][1] += price
            turns[seat].add((day, hour))
            lots[seat][(day, hour, item)] += 1

    print(f"seed {args.seed}   module {args.module}   zone d{lo}-d{hi}")
    print(f"final bank   ours {banks[0]:,.0f}   his (replayed) {banks[1]:,.0f}\n")

    items = sorted({i for (_s, i) in per})
    print(f"{'product':<14}{'ours u':>8}{'ours $':>12}{'ours $/u':>10}"
          f"{'his u':>8}{'his $':>12}{'his $/u':>10}{'his - ours':>13}")
    tot = [[0, 0.0], [0, 0.0]]
    for item in items:
        cells = []
        for seat in (0, 1):
            u, v = per[(seat, item)]
            tot[seat][0] += u
            tot[seat][1] += v
            cells.append((u, v, v / u if u else 0.0))
        print(f"{item:<14}{cells[0][0]:>8}{cells[0][1]:>12,.0f}{cells[0][2]:>10.1f}"
              f"{cells[1][0]:>8}{cells[1][1]:>12,.0f}{cells[1][2]:>10.1f}"
              f"{cells[1][1] - cells[0][1]:>+13,.0f}")
    print(f"{'TOTAL':<14}{tot[0][0]:>8}{tot[0][1]:>12,.0f}"
          f"{tot[0][1] / max(1, tot[0][0]):>10.1f}"
          f"{tot[1][0]:>8}{tot[1][1]:>12,.0f}{tot[1][1] / max(1, tot[1][0]):>10.1f}"
          f"{tot[1][1] - tot[0][1]:>+13,.0f}")

    print(f"\n{'':<14}{'ours':>10}{'his':>10}")
    for label, val in (
        ("turns selling", (len(turns[0]), len(turns[1]))),
        ("units", (tot[0][0], tot[1][0])),
        ("orders filled", (len(lots[0]), len(lots[1]))),
    ):
        print(f"{label:<14}{val[0]:>10,}{val[1]:>10,}")
    for seat, name in ((0, "ours"), (1, "his")):
        n = len(lots[seat])
        mean = sum(lots[seat].values()) / n if n else 0.0
        big = max(lots[seat].values()) if n else 0
        print(f"{'mean lot ' + name:<14}{mean:>10.1f}   (largest single lot {big})")

    if fills.unattributed:
        print(f"\nWARNING: {fills.unattributed} fills could not be attributed to a seat")


if __name__ == "__main__":
    main()
