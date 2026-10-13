"""Fit a wider SHOP_PLANS table for the imported router, on a frozen field.

The published table keys only on worlds holding a YARN_STORE; every other world
falls through to plan 0. `scripts/plan_regret.py` measured what that costs against
the parent. This fits a replacement on a field, selecting on WIN RATE, and holds
seeds back to confirm it.

Phase A  map seed -> world. The world is the first two shops the town unlocks.
         Measured on 2026-09-10: across 26 games per seed with different play on
         our side, the world never moved, so one mirror game per seed reads it.
Phase B  for every world with enough seeds, play all 13 tapes against the frozen
         field on the fit seeds, and take the tape with the best win rate.
Phase C  replay the published table and the fitted table on the HELD-OUT seeds.
         A table that only wins on the seeds it was fitted to is the winner's
         curse, and this repo has paid for that once already.

Resumable: every row is flushed as it lands and re-runs skip finished rows.

    .venv-sub/bin/python -u scripts/fit_shop_table.py --seeds 400 --jobs 6
"""
import argparse
import csv
import importlib.util
import json
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "submission" / "shop0909"
REFS = ROOT / "reference" / "public_agents"
ROUTE_STEP = 144

# The four strongest frozen agents we hold. The public reference agents were
# dropped on 2026-09-10: ledger_lena and rancher_rita sit so far below the tape
# router that nearly every cell won, and the fit stopped discriminating.
FIELD = [("parent0909", str(BUNDLE / "main.py")),
         ("e182", str(ROOT / "submission" / "e182" / "main.py")),
         ("shop0908", str(ROOT / "submission" / "shop0908" / "main.py")),
         ("v31", str(ROOT / "submission" / "v31" / "main.py"))]


class _Forced:
    def __init__(self, plan):
        self.plan = plan

    def get(self, _key, _default=None):
        return self.plan


def load_router(plan, tag):
    spec = importlib.util.spec_from_file_location(f"_router_{tag}", BUNDLE / "main.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    if plan is not None:
        module.SHOP_PLANS = _Forced(plan)
    return module.agent


def published_table():
    spec = importlib.util.spec_from_file_location("_published", BUNDLE / "main.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["_published"] = module
    spec.loader.exec_module(module)
    return dict(module.SHOP_PLANS)


def world_of(seed):
    from kaggle_environments import make
    a = load_router(None, f"wa{seed}")
    b = load_router(None, f"wb{seed}")
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([a, b])
    shops = env.steps[ROUTE_STEP][0]["observation"]["town"]["unlocked_shops"][:2]
    return {"seed": seed, "world": "|".join(shops)}


def duel(job):
    seed, plan, opp_name, opp_path, our_seat = job
    from kaggle_environments import make
    ours = load_router(plan, f"f{plan}_{seed}_{our_seat}")
    theirs = opp_path if opp_name != "parent" else load_router(None, f"p_{seed}_{plan}_{our_seat}")
    pair = [ours, theirs] if our_seat == 0 else [theirs, ours]
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run(pair)
    rewards = [s["reward"] for s in env.steps[-1]]
    ours_r, theirs_r = rewards[our_seat], rewards[1 - our_seat]
    return {"seed": seed, "plan": plan, "opponent": opp_name, "our_seat": our_seat,
            "ours": ours_r, "theirs": theirs_r, "margin": ours_r - theirs_r,
            "win": int(ours_r > theirs_r)}


def stream(path, fields, jobs, fn, pool, label, key_of_job, key_of_row):
    """Run `fn` over `jobs`, appending each result as it lands.

    Rows already in `path` are skipped, so an interrupted run resumes where it
    stopped instead of replaying finished games.
    """
    done = set()
    if path.exists():
        with path.open() as fh:
            for row in csv.DictReader(fh):
                done.add(key_of_row(row))
    todo = [j for j in jobs if key_of_job(j) not in done]
    print(f"  {label}: {len(jobs)} total, {len(done)} already done, {len(todo)} to run", flush=True)

    rows = []
    if path.exists():
        with path.open() as fh:
            rows = [row for row in csv.DictReader(fh)]
        mode = "a"
    else:
        mode = "w"
    with path.open(mode, newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        if mode == "w":
            writer.writeheader()
            fh.flush()
        for i, row in enumerate(pool.imap_unordered(fn, todo), 1):
            writer.writerow(row)
            fh.flush()
            rows.append(row)
            if i % 25 == 0 or i == len(todo):
                print(f"  {label} {i}/{len(todo)}", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=400)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--min-seeds-per-world", type=int, default=6)
    ap.add_argument("--holdout", type=int, default=2)
    ap.add_argument("--max-seeds-per-world", type=int, default=6)
    args = ap.parse_args()

    logs = ROOT / "data" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    wmap_path = logs / "world_map.csv"
    fit_path = logs / "shop_table_fit.csv"

    seeds = [11 + 7919 * i for i in range(args.seeds)]

    with Pool(args.jobs) as pool:
        print(f"phase A: world for {len(seeds)} seeds", flush=True)
        rows = stream(wmap_path, ["seed", "world"], seeds, world_of, pool, "world",
                      key_of_job=lambda seed: str(seed),
                      key_of_row=lambda row: str(row["seed"]))
        wmap = {int(r["seed"]): r["world"] for r in rows}

        worlds = defaultdict(list)
        for seed, world in sorted(wmap.items()):
            worlds[world].append(seed)
        usable = {w: s for w, s in worlds.items() if len(s) >= args.min_seeds_per_world}
        print(f"\n{len(worlds)} distinct worlds, {len(usable)} with >= {args.min_seeds_per_world} seeds", flush=True)
        for w, s in sorted(usable.items(), key=lambda kv: -len(kv[1])):
            print(f"  {w:34} {len(s)} seeds", flush=True)

        fit_seeds, hold_seeds = {}, {}
        for w, s in usable.items():
            s = s[:args.max_seeds_per_world]
            hold_seeds[w] = s[:args.holdout]
            fit_seeds[w] = s[args.holdout:]

        jobs = [(seed, plan, name, path, seat)
                for w in usable for seed in fit_seeds[w]
                for plan in range(13) for name, path in FIELD for seat in (0, 1)]
        print(f"\nphase B: {len(jobs)} games", flush=True)
        fields = ["seed", "plan", "opponent", "our_seat", "ours", "theirs", "margin", "win"]
        rows = stream(fit_path, fields, jobs, duel, pool, "duel",
                      key_of_job=lambda j: (str(j[0]), str(j[1]), j[2], str(j[4])),
                      key_of_row=lambda row: (row["seed"], row["plan"], row["opponent"], row["our_seat"]))
        for r in rows:
            for k in ("seed", "plan", "our_seat", "win"):
                r[k] = int(r[k])
            for k in ("ours", "theirs", "margin"):
                r[k] = float(r[k])

    # Phase B result: per world, the plan with the best win rate.
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[wmap[r["seed"]]][r["plan"]].append(r)
    published = published_table()
    table = {}
    print("\nfitted table (win rate over the frozen field, fit seeds only)", flush=True)
    for w in sorted(by):
        scores = {p: (sum(x["win"] for x in v) / len(v),
                      sum(x["margin"] for x in v) / len(v)) for p, v in by[w].items()}
        best = max(scores, key=lambda p: (scores[p][0], scores[p][1]))
        key = tuple(w.split("|"))
        cur = published.get(key, 0)
        table[w] = best
        flag = "" if best == cur else "  <-- CHANGED"
        print(f"  {w:34} published {cur:2}  fitted {best:2} "
              f"(win {scores[best][0]:.2f}, margin {scores[best][1]:+,.0f}; "
              f"published win {scores.get(cur, (float('nan'), 0))[0]:.2f}){flag}", flush=True)

    # The ceiling: per seed, the best tape by win rate. No selector over this tape
    # set can beat it, because it is chosen with hindsight.
    per_seed = defaultdict(lambda: defaultdict(list))
    for r in rows:
        per_seed[r["seed"]][r["plan"]].append(r)
    ceiling = published_rate = fitted_rate = 0.0
    n = 0
    for seed, plans in per_seed.items():
        rates = {p: sum(x["win"] for x in v) / len(v) for p, v in plans.items()}
        w = wmap[seed]
        key = tuple(w.split("|"))
        ceiling += max(rates.values())
        published_rate += rates.get(published.get(key, 0), 0.0)
        fitted_rate += rates.get(table.get(w, 0), 0.0)
        n += 1
    print(f"\nwin rate over {n} fit seeds x {len(FIELD)} opponents x 2 seats")
    print(f"  published table {published_rate / n:.3f}")
    print(f"  fitted table    {fitted_rate / n:.3f}   (fitted on these seeds -- not a result)")
    print(f"  ORACLE ceiling  {ceiling / n:.3f}   (hindsight best tape per seed)")

    (logs / "fitted_shop_table.json").write_text(json.dumps(
        {"table": table, "fit_seeds": fit_seeds, "holdout_seeds": hold_seeds,
         "field": [n for n, _ in FIELD]}, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {logs / 'fitted_shop_table.json'}", flush=True)
    print("Phase C (held-out confirmation) is a separate run; do not ship this table before it.", flush=True)


if __name__ == "__main__":
    main()
