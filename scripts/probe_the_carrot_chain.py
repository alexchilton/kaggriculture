"""Did the carrot get planted, harvested into the shed, and sold? All three, separately.

An empty shed at the bell is ambiguous: it means the carrot sold, or it means none was ever grown.
`CARROT_SWAP_DAYS = (25, 26, 27)` sits inside the window the planner owns when
`REPLAY_OPENING_DAYS` is `range(24)`, and the wool/carrot sell rules live in `replayed()` -- the
tape path -- so neither is guaranteed to survive that handover.

    python -u scripts/probe_the_carrot_chain.py --agent submission/main.py
"""
import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="submission/main.py")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 700, 701])
    ap.add_argument("--opponents", nargs="+", default=["mirror", "cow_heavy", "straw_small"])
    args = ap.parse_args()

    from kaggle_environments import make
    from kagg.arena.pool import _build_candidate, _build, OPPONENTS, MIRROR

    print("agent: %s" % args.agent)
    print("%6s %-12s %9s | %7s %8s %7s %7s | %7s"
          % ("seed", "opponent", "money", "planted", "into shed", "sold", "left", "WOOLleft"))

    for seed in args.seeds:
        for name in args.opponents:
            spec = MIRROR if name == "mirror" else OPPONENTS[name]
            env = make("kaggriculture", configuration={"seed": seed}, debug=False)
            env.run([_build_candidate(args.agent), _build(spec, args.agent)])
            steps = env.steps

            planted = 0
            for t in range(len(steps) - 1):
                a = steps[t + 1][0].get("action") or {}
                for u in [a.get("farmer")] + list(a.get("hands") or []):
                    if u and u[0] == "PLANT" and len(u) > 1 and u[1] == "CARROT":
                        planted += 1

            # Shed deltas: a rise is a harvest landing, a fall is a sale.
            gained = sold = 0
            prev = None
            for t in range(len(steps)):
                pr = (steps[t][0].get("observation") or {}).get("private") or {}
                held = int((pr.get("shed") or {}).get("CARROT", 0) or 0)
                if prev is not None:
                    if held > prev:
                        gained += held - prev
                    elif held < prev:
                        sold += prev - held
                prev = held
            left = prev or 0
            wool = int(((steps[-1][0].get("observation") or {}).get("private")
                        or {}).get("shed", {}).get("WOOL", 0) or 0)
            print("%6d %-12s %9.0f | %7d %8d %7d %7d | %7d"
                  % (seed, name, steps[-1][0]["reward"], planted, gained, sold, left, wool))


if __name__ == "__main__":
    main()
