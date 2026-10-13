"""Does the planner do what its plan row says? Row asked, versus what landed on the board.

The d12 board match (`scripts/match_d12.py`) came back with the SAME six axes inside SpaTaro's
interquartile range under two plans that share nothing on the field -- カワシギ's rows and
SpaTaro's differ on every `plants`, `buys` and `hires` entry, and the boards at dawn of d12 differ
by one tile and $400. Either the planner is insensitive to the plan on the field, or the plan is
malformed and being discarded. This tells the two apart.

Our own game is read back with `spataro_landed_schedule.landed_rows`, the same function that built
his rows, so "asked" and "landed" cannot drift apart by definition-shift.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spataro_landed_schedule import landed_rows

ARMS = {"planner_spa":  (ROOT / "submission/planner_spa/main.py", "data/seed_scripts/spataro/schedule.json"),
        "planner_kawa": (ROOT / "submission/planner_pure/main.py", "data/seed_scripts/kawashigi/schedule.json")}
OPP = ROOT / "submission/shop0909/main.py"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="planner_spa")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--days", type=int, default=13)
    args = ap.parse_args()

    path, plan_path = ARMS[args.arm]
    plan = json.loads((ROOT / plan_path).read_text())

    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": args.seed}, debug=False)
    env.run([str(path), str(OPP)])
    got = landed_rows(env.steps, 0)
    print(f"{args.arm}  seed {args.seed}  bank ${env.steps[-1][0]['reward']:,.0f}  "
          f"plan {plan_path}\n")
    print(f"{'d':>2} {'plants asked':>26} {'plants landed':>26}  "
          f"{'hires a/l':>9} {'land a/l':>8} {'builds a/l':>10} {'places a/l':>12}")
    for d in range(args.days):
        row = plan[str(d)]
        a, l = Counter(row.get("plants") or []), Counter(got[d]["plants"])
        f = lambda c: " ".join(f"{k[:4]}{v}" for k, v in sorted(c.items())) or "-"
        print(f"{d:>2} {f(a):>26} {f(l):>26}  "
              f"{row.get('hands', 0):>4}/{got[d]['hires']:<4} "
              f"{row.get('land', 0):>3}/{got[d]['land']:<4} "
              f"{row.get('builds', 0):>4}/{got[d]['builds']:<5} "
              f"{''.join(x[0] for x in (row.get('places') or [])) or '-':>5}/"
              f"{''.join(x[0] for x in got[d]['places']) or '-':<6}")
    tot_a = Counter(c for d in range(args.days) for c in (plan[str(d)].get("plants") or []))
    tot_l = Counter(c for d in range(args.days) for c in got[d]["plants"])
    print(f"\nover days 0..{args.days - 1}:")
    print(f"  asked  {dict(sorted(tot_a.items()))}  total {sum(tot_a.values())}")
    print(f"  landed {dict(sorted(tot_l.items()))}  total {sum(tot_l.values())}")


if __name__ == "__main__":
    main()
