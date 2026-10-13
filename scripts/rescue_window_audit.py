"""Where does the E182 overlay actually differ from its parent? Audit, not opinion.

policy.py declares START, FINAL = 712, 718. If that holds in play, then no
collapse anywhere in a season can be blamed on the rescue: the two agents emit
identical actions everywhere else, so any difference in outcome before turn 712
came from the opponent or the draw.

Both agents play the same seed against the same opponent and their submitted
action streams are compared turn by turn.

    .venv-sub/bin/python -u scripts/rescue_window_audit.py --seeds 12
"""
import argparse
import json
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E182 = str(ROOT / "submission" / "e182" / "main.py")
PARENT = str(ROOT / "submission" / "shop0909" / "main.py")
OPPONENTS = {"shop0908": str(ROOT / "submission" / "shop0908" / "main.py"),
             "v31": str(ROOT / "submission" / "v31" / "main.py"),
             "parent0909": PARENT}


def stream(seed, agent_path, opp_path, our_seat):
    from kaggle_environments import make
    pair = [agent_path, opp_path] if our_seat == 0 else [opp_path, agent_path]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    acts = [json.dumps(step[our_seat].get("action"), sort_keys=True) for step in env.steps[1:]]
    return acts, env.steps[-1][our_seat]["reward"]


def audit(job):
    seed, opp_name, our_seat = job
    opp = OPPONENTS[opp_name]
    a, ra = stream(seed, E182, opp, our_seat)
    b, rb = stream(seed, PARENT, opp, our_seat)
    diff = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return {"seed": seed, "opponent": opp_name, "seat": our_seat,
            "diff_turns": diff, "e182_reward": ra, "parent_reward": rb}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--jobs", type=int, default=5)
    args = ap.parse_args()
    seeds = [11 + 7919 * i for i in range(args.seeds)]
    jobs = [(s, o, seat) for s in seeds for o in OPPONENTS for seat in (0, 1)]
    print(f"{len(jobs)} paired seasons", flush=True)

    outside = 0
    hist = Counter()
    with Pool(args.jobs) as pool:
        for i, r in enumerate(pool.imap_unordered(audit, jobs), 1):
            bad = [t for t in r["diff_turns"] if not 712 <= t <= 718]
            outside += len(bad)
            for t in r["diff_turns"]:
                hist[t] += 1
            flag = f"  *** {len(bad)} OUTSIDE THE WINDOW: {bad[:10]}" if bad else ""
            print(f"  [{i}/{len(jobs)}] seed={r['seed']} vs {r['opponent']} seat={r['seat']} "
                  f"diff turns={len(r['diff_turns'])} "
                  f"reward {r['e182_reward']:,.0f} vs {r['parent_reward']:,.0f}{flag}", flush=True)

    print(f"\nturns where the two ever differed: {sorted(hist)}")
    print(f"differences outside [712,718] across all seasons: {outside}")
    print("VERDICT: the overlay is confined to its declared window."
          if outside == 0 else "VERDICT: the overlay escapes its window. Investigate.")


if __name__ == "__main__":
    main()
