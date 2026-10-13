"""Two descriptive probes on the adaptive top agents. Neither is proof.

1. Duplicate seeds. The seed fixes the board, so two seasons on one seed differ only
   through the opponent or through stochasticity in the policy itself.
2. Action vocabulary. A rule cascade composes turns from a small set of canned
   moves and reuses them across seasons. A policy conditioned on the full state
   emits a long tail of combinations seen exactly once.

Labelled suggestive, not conclusive: a deterministic network argmax and a rule
cascade are both deterministic functions of the observation.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08",
        "data/replays_2026-09-09", "data/replays_hayashi"]


def main():
    top = json.loads((ROOT/"data/logs/top30.json").read_text())
    rank = {n: i+1 for i, n in enumerate(top)}; rank["Yusuke Hayashi"] = 34

    seasons, seen = defaultdict(list), set()
    for d in DIRS:
        for p in sorted((ROOT/d/"summaries").glob("*.summary.json")):
            rec = json.loads(p.read_text())
            if rec["episode"] in seen: continue
            seen.add(rec["episode"])
            for seat, team in enumerate(rec["teams"]):
                seasons[team].append({"seed": rec["seed"], "episode": rec["episode"],
                                      "opp": rec["teams"][1-seat],
                                      "world": "|".join(rec["world"]),
                                      "actions": rec["actions"][seat]})

    print("=== duplicate seeds (identical board) ===")
    any_dup = False
    for team in sorted(seasons, key=lambda t: rank.get(t, 999)):
        if team not in rank: continue
        byseed = defaultdict(list)
        for s in seasons[team]:
            byseed[s["seed"]].append(s)
        for seed, ss in byseed.items():
            if len(ss) < 2: continue
            any_dup = True
            for i, a in enumerate(ss):
                for b in ss[i+1:]:
                    d = sum(1 for x, y in zip(a["actions"], b["actions"]) if x != y)
                    fd = next((i for i, (x, y) in enumerate(zip(a["actions"], b["actions"]))
                               if x != y), None)
                    print(f"  rk{rank[team]:>3} {team[:22]:22} seed={seed} "
                          f"diff {d:>3}/719 first at {fd}  "
                          f"opp {'SAME' if a['opp']==b['opp'] else 'differs'}")
    if not any_dup:
        print("  none")

    print(f"\n=== action vocabulary ===")
    print(f"{'rk':>3} {'team':24} {'n':>3} {'turns':>6} {'distinct':>9} "
          f"{'seen once':>10} {'reuse':>6}")
    for team in sorted(seasons, key=lambda t: rank.get(t, 999)):
        if team not in rank: continue
        g = seasons[team]
        if len(g) < 3: continue
        c = Counter(a for s in g for a in s["actions"])
        turns = sum(c.values())
        once = sum(1 for v in c.values() if v == 1)
        print(f"{rank[team]:>3} {team[:24]:24} {len(g):>3} {turns:>6} {len(c):>9} "
              f"{once:>10} {1-len(c)/turns:>6.3f}")


if __name__ == "__main__":
    main()
