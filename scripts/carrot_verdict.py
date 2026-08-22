"""Which carrot rule, and does it survive the town it was conditioned on?

    .venv/bin/python -u scripts/carrot_verdict.py [rows.csv]

`land_grid_verdict.py` answers "which arm wins". That is not enough here, because the carrot arms
ARE the rule: `cond_carrot_d{drain_min}_o{opp_max}` fires only when the town's carrot drain is at
least `drain_min` and the opponent holds at most `opp_max` carrot tiles. So the arm table IS the
threshold sweep, and the thing to check is whether the winner is a real conditional or just the arm
that happened to fire on the friendliest sample.

The prior, measured 2026-08-22 on 528 configurations before this run:

    town CA>=4  opp CA 1-14   n=125   mean +1143   75% improved
    town CA>=4  mirror        n= 25   mean +1659   92% improved
    town CA>=4  opp CA=0      n=100   mean  +273   46% improved
    town CA>=4  opp CA 15+    n= 25   mean  -510   28% improved
    town CA<4   every bucket                       negative, 0-11% improved
    unconditional                     -$237, because the losing towns cancel the winning ones

That is thin -- the note on it says "3 towns and 57 seasons". Tonight is 12,096 seasons across 12
arms, so it is refinement of a measured effect, not a rediscovery.

**Three things this prints that a plain win-rate table does not.**

1. **How often each rule FIRED.** A conditional arm that never fires is identical to control and its
   win rate is control's. `n diff` is the fire count, and an arm with a tiny one cannot be trusted
   however good its rate looks.
2. **The town-drain bucket.** `drain_CARROT` is in every row. The whole claim is that carrot pays
   where the town drains it, so the win rate must be split on that or it is the unconditional
   average again -- which measured -$237.
3. **Static against conditional.** `carrot2_d25d27` and `carrot4_d25d27` swap unconditionally. If a
   conditional arm cannot beat those, the condition is costing more than it saves.

Written 2026-08-22 while the sweep ran, so the answer is one command when it lands.
"""
import collections
import csv
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT = REPO / "data/logs/carrot_refine_rows_2026-08-22.csv"


def cell(r):
    return (r["town"], r["opponent"], r["seed"])


def won(r):
    return int(r["ours"]) > int(r["theirs"])


def main():
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        sys.exit(f"no rows at {path}")
    with open(path, newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("arm")]
    if not rows:
        sys.exit(f"{path} has no rows yet")

    by_arm = collections.defaultdict(dict)
    for r in rows:
        by_arm[r["arm"]][cell(r)] = r
    if "control" not in by_arm:
        sys.exit("no control arm; nothing to compare against")
    control = by_arm["control"]

    done = len(rows)
    print(f"{path}\n{done} rows, {len(by_arm)} arms, {len(control)} control cells"
          f"{'   (SWEEP STILL RUNNING -- partial)' if done < 12096 else ''}\n")

    print("%-22s %7s %9s %11s %8s %14s" %
          ("arm", "fired", "arm win%", "control win%", "swing", "mean delta $"))
    ranked = []
    for arm in sorted(by_arm):
        if arm == "control":
            continue
        diff = [(a, control[k]) for k, a in by_arm[arm].items()
                if k in control and int(a["ours"]) != int(control[k]["ours"])]
        if not diff:
            print("%-22s %7d %9s %11s %8s %14s" % (arm, 0, "-", "-", "-", "never fired"))
            continue
        aw = 100.0 * sum(won(a) for a, _ in diff) / len(diff)
        cw = 100.0 * sum(won(c) for _, c in diff) / len(diff)
        dm = sum(int(a["ours"]) - int(c["ours"]) for a, c in diff) / len(diff)
        ranked.append((aw - cw, arm, len(diff), aw, cw, dm))
        print("%-22s %7d %8.1f%% %10.1f%% %+8.1f %+14.0f" % (arm, len(diff), aw, cw, aw - cw, dm))

    if not ranked:
        print("\nNo arm changed a season yet.")
        return

    ranked.sort(reverse=True)
    swing, arm, n, aw, cw, dm = ranked[0]
    print(f"\nBest on win rate: {arm}   {aw:.1f}% vs {cw:.1f}%   ({swing:+.1f} points, "
          f"{n} seasons where it fired, mean bank {dm:+.0f})")
    if swing <= 0:
        print("  -- control wins. No carrot rule pays on this grid.")

    # ---- the conditioning the whole claim rests on -------------------------------------------
    print("\nBy TOWN carrot drain, best arm only. The claim is that carrot pays where the town")
    print("drains it; unconditionally the same swap measured -$237.\n")
    print("%-14s %9s %10s %10s %14s" % ("town drain", "fired", "arm win%", "ctrl win%", "mean delta $"))
    buckets = collections.defaultdict(list)
    for k, a in by_arm[arm].items():
        if k not in control or int(a["ours"]) == int(control[k]["ours"]):
            continue
        d = int(a.get("drain_CARROT", 0) or 0)
        buckets["CA 0-3" if d < 4 else ("CA 4-6" if d < 7 else "CA 7+")].append((a, control[k]))
    for b in ("CA 0-3", "CA 4-6", "CA 7+"):
        pairs = buckets.get(b) or []
        if not pairs:
            print("%-14s %9d %10s %10s %14s" % (b, 0, "-", "-", "-"))
            continue
        aw_ = 100.0 * sum(won(a) for a, _ in pairs) / len(pairs)
        cw_ = 100.0 * sum(won(c) for _, c in pairs) / len(pairs)
        dm_ = sum(int(a["ours"]) - int(c["ours"]) for a, c in pairs) / len(pairs)
        print("%-14s %9d %9.1f%% %9.1f%% %+14.0f" % (b, len(pairs), aw_, cw_, dm_))

    static = [r for r in ranked if not r[1].startswith("cond_")]
    cond = [r for r in ranked if r[1].startswith("cond_")]
    if static and cond:
        print(f"\nBest STATIC   {static[0][1]:<22} {static[0][0]:+.1f} points over {static[0][2]}")
        print(f"Best CONDITIONAL {cond[0][1]:<19} {cond[0][0]:+.1f} points over {cond[0][2]}")
        if cond[0][0] <= static[0][0]:
            print("  -- the condition is not paying for itself; the static swap is as good or better.")


if __name__ == "__main__":
    main()
