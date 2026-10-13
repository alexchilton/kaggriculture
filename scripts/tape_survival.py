"""How far does a tape actually survive before the board stops matching?

The tape is only valid while the farm is the one it was recorded against, and it is replayed on a
DIFFERENT seed -- a weed can spawn (0.005 a tile a day), the market opens at different prices, so a
purchase of his can fail where ours succeeds. `schedule_agent._board_is` compares crops, herd and
owned tiles every dawn and latches `tape_stop` on the first mismatch, one way, because the error
compounds: a HARVEST onto the wrong crop is a silent no-op, the produce is never collected, the sell
that assumed it raises nothing, the next purchase fails.

So "how many days of tape" is a fact of each game, not a constant to choose in advance. This reads
it out of the agent's own state rather than re-deriving it, because a second copy of the check in
the harness would be the thing being measured.
"""
import argparse, json, sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run(job):
    seed, plan_path, opp = job
    sys.path.insert(0, str(ROOT))
    import kagg.plan as P
    from kagg.search import schedule_agent as SA
    from kaggle_environments import make

    raw = json.loads((ROOT / plan_path).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in P.TAPE_ONLY}
             for k, r in raw.items()}
    agent = SA.make_agent(sched, 0, router=True)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([agent, str(ROOT / opp)])
    st = getattr(agent, "state", {}) or {}
    return {"seed": seed, "cluster": st.get("tape_cluster"),
            "splice_ok": st.get("splice_ok"), "died": st.get("tape_stopped_day"),
            "bank": env.steps[-1][0]["reward"] or 0,
            "status": "/".join(str(x["status"]) for x in env.steps[-1])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default="data/seed_scripts/spa_family/milk_berry.json")
    ap.add_argument("--opponent", default="submission/shop0909/main.py")
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--procs", type=int, default=5)
    args = ap.parse_args()

    seeds = [11 + 7919 * i for i in range(args.seeds)]
    with Pool(args.procs) as pool:
        rows = pool.map(run, [(s, args.plan, args.opponent) for s in seeds])

    print(f"{'seed':>10} {'cluster':>12} {'splice':>8} {'tape died':>11} {'bank':>10}")
    for r in rows:
        print(f"{r['seed']:>10} {str(r['cluster']):>12} {str(r['splice_ok']):>8} "
              f"{(str(r['died']) if r['died'] else 'ran to 29'):>11} {r['bank']:>10,.0f}")
    died = sorted(r["died"] for r in rows if r["died"])
    print(f"\nran the whole season: {len(rows)-len(died)} of {len(rows)}")
    if died:
        print(f"died on day: {died}")
        print(f"p50 day {died[len(died)//2]}, earliest {died[0]}, latest {died[-1]}")
    print(f"clusters: {dict(Counter(str(r['cluster']) for r in rows))}")
    bad = [r for r in rows if not r["status"].startswith("DONE")]
    if bad:
        print(f"!! {len(bad)} not DONE")


if __name__ == "__main__":
    main()
