"""How much does the day-6 shop rule leave on the table?

Shop Router 0909 branches exactly twice: at step 144 it picks one of 13 tapes from
the first two unlocked shops, and at step 648 it forces the shared ending. This
script forces every tape in turn on the same seed and reads off which one actually
wins, so the gap between the rule's pick and the best pick is a dollar regret --
an upper bound on what ANY better routing over this tape set could buy, v58's
included.

The parent file is never edited. The plan is forced by replacing the module's
SHOP_PLANS lookup in a freshly imported copy, so router_parent.py keeps its
published hash.

    .venv-sub/bin/python -u scripts/plan_regret.py --seeds 16 --jobs 5

Rows are flushed as they finish, so a kill costs one game.
"""
import argparse
import csv
import importlib.util
import json
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "submission" / "shop0909"
ROUTE_STEP = 144


class _Forced:
    """Stands in for SHOP_PLANS so every shop pair maps to one tape."""

    def __init__(self, plan):
        self.plan = plan

    def get(self, _key, _default=None):
        return self.plan


def load_agent(plan=None, tag=""):
    spec = importlib.util.spec_from_file_location(f"_router_{tag}", BUNDLE / "main.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if plan is not None:
        module.SHOP_PLANS = _Forced(plan)
    return module.agent, module


def play(job):
    seed, plan, our_seat = job
    from kaggle_environments import make
    ours, module = load_agent(plan, f"forced{plan}_{seed}_{our_seat}")
    theirs, _ = load_agent(None, f"parent_{plan}_{seed}_{our_seat}")
    pair = [ours, theirs] if our_seat == 0 else [theirs, ours]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    rewards = [s["reward"] for s in env.steps[-1]]

    shops = env.steps[ROUTE_STEP][0]["observation"]["town"]["unlocked_shops"][:2]
    # What the unmodified rule would have chosen for this world.
    import json as _json
    parent_src = (BUNDLE / "main.py").read_text()
    rule_pick = None
    spec = importlib.util.spec_from_file_location("_plans_only", BUNDLE / "main.py")
    clean = importlib.util.module_from_spec(spec)
    sys.modules["_plans_only"] = clean
    spec.loader.exec_module(clean)
    rule_pick = clean.SHOP_PLANS.get(tuple(shops), 0)

    return {"seed": seed, "plan": plan, "our_seat": our_seat,
            "ours": rewards[our_seat], "theirs": rewards[1 - our_seat],
            "margin": rewards[our_seat] - rewards[1 - our_seat],
            "world": "|".join(shops), "rule_pick": rule_pick,
            "win": int(rewards[our_seat] > rewards[1 - our_seat])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--plans", type=int, default=13)
    ap.add_argument("--out", default="data/logs/plan_regret.csv")
    args = ap.parse_args()

    seeds = [11, 4242, 70683142, 244615642, 1240813987, 99114898, 7, 123456,
             2026, 31337, 555, 98898511, 186814513, 1914872111, 424242, 8675309][:args.seeds]
    jobs = [(s, p, seat) for s in seeds for p in range(args.plans) for seat in (0, 1)]
    print(f"{len(jobs)} games: {len(seeds)} seeds x {args.plans} plans x 2 seats", flush=True)

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["seed", "plan", "our_seat", "ours", "theirs", "margin", "world", "rule_pick", "win"]
    with out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        fh.flush()
        with Pool(args.jobs) as pool:
            for i, row in enumerate(pool.imap_unordered(play, jobs), 1):
                writer.writerow(row)
                fh.flush()
                print(f"[{i}/{len(jobs)}] seed={row['seed']} plan={row['plan']} "
                      f"seat={row['our_seat']} margin={row['margin']:+} "
                      f"world={row['world']} rule={row['rule_pick']}", flush=True)
    print(f"wrote {out}", flush=True)


if __name__ == "__main__":
    main()
