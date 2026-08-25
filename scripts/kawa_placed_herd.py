"""What kawa PLACED, not what survived to the bell.

Alex: "sometimes he deliberately doesn't feed them so don't look at the end."

`PLACE` is the right count. You cannot place an animal you do not own, and it is a unit op, so it is
emitted once -- unlike `BUY_ANIMAL`, which is a market order the agent re-posts every turn and which
therefore overcounts (`feedback_offers_are_not_fills`).

This exists because the final-board count sent an earlier reading of this question wrong: the herd
distribution off the last step said his modes were 10/2 and 6/6 at a total of 12, and the placed
counts on the same games are 10/4 and 6/12 -- total 14 and 18. The survivors are not the policy.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

KAWA = "カワシギ"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")
SPECIES = ("COW", "SHEEP")


def main():
    placed_dist, alive_dist, pairs = collections.Counter(), collections.Counter(), collections.Counter()
    n = 0
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(r, dict):
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            seat = names.index(KAWA)
            n += 1
            pl = collections.Counter()
            for step in r.get("steps") or []:
                if seat >= len(step):
                    continue
                act = (step[seat] or {}).get("action") or {}
                for op in [act.get("farmer")] + list(act.get("hands") or []):
                    if op and len(op) >= 2 and op[0] == "PLACE" and op[1] in SPECIES:
                        pl[op[1]] += 1
            farms = ((r["steps"][-1][0] or {}).get("observation") or {}).get("farms") or []
            al = collections.Counter()
            if seat < len(farms):
                for row in (farms[seat].get("tiles") or []):
                    for t in row:
                        if isinstance(t, dict) and t.get("animal"):
                            al[t["animal"]] += 1
            P = (pl["COW"], pl["SHEEP"])
            A = (al["COW"], al["SHEEP"])
            placed_dist[P] += 1
            alive_dist[A] += 1
            pairs[(P, A)] += 1

    print(f"kawa post-change tapes: {n}", flush=True)
    if not n:
        return
    print()
    print("PLACED -- what he actually owned")
    print(f"  {'C/S':<10}{'seats':>6}{'total':>7}   share")
    for (c, s), k in placed_dist.most_common(10):
        print(f"  {str(c) + '/' + str(s):<10}{k:>6}{c + s:>7}   {100.0 * k / n:>5.1f}%")
    print()
    print("ALIVE at the bell -- survivors only, NOT the policy")
    print(f"  {'C/S':<10}{'seats':>6}{'total':>7}   share")
    for (c, s), k in alive_dist.most_common(8):
        print(f"  {str(c) + '/' + str(s):<10}{k:>6}{c + s:>7}   {100.0 * k / n:>5.1f}%")
    print()
    print("placed -> alive, top 10:")
    for (P, A), k in pairs.most_common(10):
        print(f"  {P[0]}/{P[1]}={P[0] + P[1]:<3} -> {A[0]}/{A[1]}={A[0] + A[1]:<3}  {k:>3} seats"
              f"   sheep lost {P[1] - A[1]}, cows lost {P[0] - A[0]}")
    tot_p = sum((c + s) * k for (c, s), k in placed_dist.items())
    tot_a = sum((c + s) * k for (c, s), k in alive_dist.items())
    print()
    print(f"mean PLACED total {tot_p / n:.2f}   mean ALIVE total {tot_a / n:.2f}")


if __name__ == "__main__":
    main()
