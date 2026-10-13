"""Turn by turn against the tape, from the handover on. Where does the planner first part from him?

Run only where the comparison is valid: the same episode whose tape drove days 0-6, on a board
measured identical at the handover (`scripts/handover_state.py` -- money 51 vs 33, planted 33 vs 33,
COW 5 SHEEP 2 both, same crops, same shed). From d7 the planner is on its own with his board and his
bank, so every difference from here is the planner's.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24


def ops(action):
    """The op names a turn issued, unit actions and market orders, ignoring tiles and quantities."""
    out = Counter()
    for c in [action.get("farmer") or []] + list(action.get("hands") or []):
        if c:
            out[c[0]] += 1
    # **Market orders counted in UNITS, not in orders.** An order carries a quantity, and counting
    # orders made a 34-to-6 seed comparison that was 34 single-unit orders against 6 large ones.
    for o in (action.get("market") or []):
        if o:
            q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
            out[f"${o[0]}" + (f" {o[1]}" if len(o) > 1 and o[1] else "")] += q
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="spa_own")
    ap.add_argument("--episode", type=int, default=107068412)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--from-day", type=int, default=7)
    ap.add_argument("--to-day", type=int, default=13)
    args = ap.parse_args()

    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": args.seed}, debug=False)
    env.run([str(ROOT / "submission" / args.arm / "main.py"),
             str(ROOT / "submission/shop0909/main.py")])

    r = json.loads((ROOT / f"data/replays_spa_sub/{args.episode}.json").read_text())
    seat = r["info"]["TeamNames"].index("SpaTaro")

    print(f"{args.arm} seed {args.seed} vs ep {args.episode}, days "
          f"{args.from_day}-{args.to_day - 1}\n")
    print(f"{'day':>4} {'ours':>34}   {'his':>34}")
    tot_o, tot_h = Counter(), Counter()
    for day in range(args.from_day, args.to_day):
        o, h = Counter(), Counter()
        for hour in range(TPD):
            i = day * TPD + hour + 1
            if i < len(env.steps):
                o += ops((env.steps[i][0] or {}).get("action") or {})
            if i < len(r["steps"]):
                h += ops((r["steps"][i][seat] or {}).get("action") or {})
        tot_o += o
        tot_h += h
        f = lambda c: " ".join(f"{k}{v}" for k, v in c.most_common(5) if not k.startswith("$"))
        print(f"{day:>4} {f(o):>34}   {f(h):>34}")

    print(f"\n{'op':<22} {'ours':>7} {'his':>7} {'ratio':>7}")
    for k in sorted(set(tot_o) | set(tot_h), key=lambda x: -(tot_h[x] + tot_o[x])):
        a, b = tot_o[k], tot_h[k]
        print(f"{k:<22} {a:>7} {b:>7} {(a / b if b else 0):>7.2f}")


if __name__ == "__main__":
    main()
