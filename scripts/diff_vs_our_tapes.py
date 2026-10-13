"""How far a team's recorded seasons follow OUR shipped 13 tapes, turn by turn.

Our current release (submission 56158924, 2673.0) is a 13-tape Hayashi-derived build. Several
ladder teams are the same lineage, so the useful question is not "is it a tape" but "where does
theirs stop agreeing with ours" -- that turn is the edit, and the edit is what their rating buys.

    python -u scripts/diff_vs_our_tapes.py mtmr_s1
    python -u scripts/diff_vs_our_tapes.py "Yusuke Hayashi" Majkel1337
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
TAPES = ROOT / "submission/hay_router2/actions.json"


def main():
    teams = sys.argv[1:] or ["mtmr_s1"]
    ours = [[json.dumps(t) for t in tape] for tape in json.loads(TAPES.read_text())]
    seen = set()
    runs = collections.defaultdict(list)
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            for seat, team in enumerate(r["teams"]):
                if team in teams and seat < len(r["actions"]) and r["actions"][seat]:
                    runs[team].append((r["episode"], r["world"][seat], r["actions"][seat],
                                       r["rewards"][seat] if seat < len(r["rewards"]) else None))

    for team in teams:
        v = runs.get(team) or []
        print(f"\n=== {team}: {len(v)} seasons against our 13 tapes ===")
        print(f"{'episode':>10} {'world':16} {'tape':>5} {'agrees':>7} {'day':>5} {'bank':>10}")
        depths = []
        for ep, world, acts, bank in sorted(v):
            best, bi = -1, None
            for i, t in enumerate(ours):
                k = 0
                for x, y in zip(acts, t):
                    if x != y:
                        break
                    k += 1
                if k > best:
                    best, bi = k, i
            depths.append(best)
            print(f"{ep:>10} {str(world)[:16]:16} {bi:>5} {best:>7} {best/24:>5.1f} "
                  f"{(bank or 0):>10,.0f}")
        if depths:
            print(f"  agreement: min {min(depths)}  median {sorted(depths)[len(depths)//2]}  "
                  f"max {max(depths)} turns")


if __name__ == "__main__":
    main()
