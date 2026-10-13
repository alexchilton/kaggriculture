"""Where are the two farms' holdings ASYMMETRIC? That is the only place denial can pay.

Cratering a book costs the seller too, so it nets out wherever both sides hold the same goods --
which is why the fertilizer strike lost 10/10 on margin: every agent in the sample sells fertilizer
on 84-128 turns, so the damage was shared almost equally.

Denial pays only where WE hold little of a product and THEY hold a lot: crash it and most of the
loss lands in their column. This finds those products, per episode, off the recorded shed levels.

    python -u scripts/holdings_gap.py 107642213 107646523 107399673 107041112 107674019
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def find(ep):
    return next((ROOT / d / f"{ep}.json" for d in DIRS if (ROOT / d / f"{ep}.json").exists()), None)


def main():
    tally = collections.Counter()
    for ep in sys.argv[1:]:
        rep = json.loads(find(int(ep)).read_text())
        teams = rep["info"]["TeamNames"]
        # total shed-units held across the season, per seat -- a proxy for exposure to a book
        held = [collections.Counter(), collections.Counter()]
        peak = [collections.Counter(), collections.Counter()]
        for step in rep["steps"]:
            for seat in range(len(teams)):
                shed = (((step[seat] if seat < len(step) else None) or {})
                        .get("observation") or {}).get("private", {}).get("shed") or {}
                for k, v in shed.items():
                    held[seat][k] += int(v or 0)
                    peak[seat][k] = max(peak[seat][k], int(v or 0))
        print(f"\n=== {ep}: {teams[0]} vs {teams[1]} ===")
        print(f"{'product':12}{'held-turns A':>14}{'held-turns B':>14}{'peak A':>9}{'peak B':>9}"
              f"   asymmetry")
        for p in sorted(set(held[0]) | set(held[1])):
            a, b = held[0][p], held[1][p]
            if a + b == 0:
                continue
            ratio = (max(a, b) + 1) / (min(a, b) + 1)
            flag = ""
            if ratio >= 3:
                flag = f"{teams[0 if a > b else 1][:14]} holds {ratio:.1f}x"
                tally[p] += 1
            print(f"{p:12}{a:>14,}{b:>14,}{peak[0][p]:>9}{peak[1][p]:>9}   {flag}")
    print(f"\nproducts asymmetric (>=3x) in how many episodes: {dict(tally)}")


if __name__ == "__main__":
    main()
