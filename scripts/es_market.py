"""Evolution strategy over the market policy, scored against real leaderboard tapes.

**Fitness is SELECTABLE, and running more than one mode is the point -- see `FITNESS` below.**
Win rate is the true objective: the ladder is an Elo rating, so a $43k win and a $4k win are the same
result. But the 172-game tape gate scores 97.7% for the shipped agent, and an objective pinned at its
ceiling gives the optimiser nothing to follow -- the same saturation that made `kagg/arena/pool.py`
useless and left `LATE_SELL_BIAS` looking inert. `blend` (the default) keeps win rate in charge and
uses margin only to order candidates that win the same number of games. `margin` and `winrate` run
the pure versions. If two modes disagree about the champion, that disagreement is the finding.

**Paired seeds, always.** Opponent *i* is played on seed `SEED0 + i` in every candidate and every
generation. Seed variance on money is ~$24,500, which would otherwise swamp a real effect; pairing
removes it from the comparison entirely. This is why the same seeds are reused rather than resampled
-- and it is also the winner's-curse risk, so `--holdout` re-scores the final champion on seeds it
never saw. A search winner that does not survive a fresh draw is noise (CLAUDE.md).

**Baselines are evaluated every generation, not once.** The shipped configuration is scored on the
same seeds as the population, so a generation's improvement is read against a number measured in the
same conditions rather than against a remembered one.

Run on the box, in the 1.32.6 venv -- NOT `.venv` or `.venv-cuda`, which carry 1.32.3/1.32.4 and a
`townCenterSellInterval` of 12, the dead economy:

    ~/kagg/.venv-kagg/bin/python -u ~/kagg/scripts/es_market.py --gens 30 --pop 12 \
        --workers 14 2>&1 | tee ~/kagg/logs/es_market.log
"""

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLAN = ROOT / "data/seed_scripts/top_guys/90976060/schedule.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
SEED0 = 4001

#: name -> (low, high, kind). `kind` is "i" for integer, "f" for float, "b" for a 0/1 gate.
#:
#: Every one of these already exists as a module constant with a measured comment beside it; the ES
#: is searching the space those comments each explored one axis of. Bounds are deliberately wider
#: than the values anyone has tried, because a search confined to the neighbourhood of the current
#: setting can only confirm it.
SPACE = {
    "FEED_TURN_CAP":            (1, 12, "i"),
    "FEED_DAYS":                (1, 4, "i"),
    "FEED_DAYS_LATE":           (2, 6, "i"),
    "FEED_DAYS_FROM_DAY":       (8, 22, "i"),
    "FEED_DAYS_FLOOR":          (0, 3, "i"),
    "SELL_CARRY_DAYS":          (1, 5, "i"),
    "RESERVATION_CONTEST":      (0.0, 1.0, "f"),
    "RESERVATION_SLIP":         (0.0, 0.35, "f"),
    "SELL_OFFER_CAP":           (8, 60, "i"),
    "CAP_SELL_OFFER_SIZE":      (0, 1, "b"),
    "LATE_SELL_FROM_HOUR":      (0, 20, "i"),
    "LATE_SELL_BIAS":           (0, 1, "b"),
    "SELL_EVERY_N_HOURS":       (1, 12, "i"),
    "SELL_ON_DRAIN_CADENCE":    (0, 1, "b"),
}


def opponents(limit):
    """Distinct 1.32.6 opponents, one seat each -- breadth over depth."""
    import glob
    seen, out = set(), []
    for p in sorted(glob.glob(str(ROOT / "data/seed_scripts/top_guys/*.json"))):
        try:
            d = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        if (d.get("configuration") or {}).get("townCenterSellInterval") != 24:
            continue
        names = (d.get("info") or {}).get("TeamNames") or ["?", "?"]
        for s in (0, 1):
            if s < len(names) and names[s] != "alex chilton" and names[s] not in seen:
                seen.add(names[s])
                out.append((p, s, names[s]))
    return out[:limit]


def _thin():
    sched = {int(k): v for k, v in json.loads(PLAN.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def play(job):
    """One game. Returns the MARGIN in our favour."""
    path, rec_seat, our_seat, seed, genome = job
    from kaggle_environments import make

    import kagg.search.schedule_agent as SA
    for k, v in genome.items():
        setattr(SA, k, v)
    from kagg.arena.tape import build_tape_agent

    ours = SA.make_agent(_thin(), our_seat, router=True)
    theirs = build_tape_agent(path, rec_seat, jitter_seed=seed, drop=0.10, scale=0.20)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    agents = {our_seat: ours, 1 - our_seat: theirs}
    for _t in range(24 * 30):
        if env.done:
            break
        acts = []
        for p in (0, 1):
            o = env.state[p].observation
            a = agents[p](o)
            n = len(o["farms"][p].get("hands") or [])
            acts.append({"farmer": a["farmer"], "hands": list(a["hands"])[:n],
                         "market": a["market"]})
        env.step(acts)
    farms = env.state[0].observation["farms"]
    return float(farms[our_seat]["money"]) - float(farms[1 - our_seat]["money"])


def decode(vec):
    g = {}
    for (name, (lo, hi, kind)), x in zip(SPACE.items(), vec):
        x = min(1.0, max(0.0, x))
        if kind == "f":
            g[name] = lo + x * (hi - lo)
        elif kind == "b":
            g[name] = bool(x >= 0.5)
        else:
            g[name] = int(round(lo + x * (hi - lo)))
    return g


def shipped_genome():
    """Read the current module defaults, so the baseline is the code and not a remembered number."""
    sys.path.insert(0, str(ROOT))
    import kagg.search.schedule_agent as SA
    return {k: getattr(SA, k) for k in SPACE}


#: How a candidate is scored. **This is a real fork in the road, not a detail.**
#:
#: `winrate` is the TRUE objective -- the ladder is an Elo rating, so a $43k win and a $4k win are
#: the same result, and CLAUDE.md's hardest-won rule is "select on win rate, not money". Its problem
#: here is measured: the shipped agent scores 97.7% against this field, and an objective pinned near
#: its ceiling gives the optimiser almost no gradient to follow.
#:
#: `margin` has gradient everywhere but optimises the wrong thing, and can happily trade a win for a
#: bigger loss elsewhere.
#:
#: `blend` is win rate with margin as a TIEBREAK: the margin term is scaled to be worth less than a
#: single game, so it can never overturn a win-rate difference, and only decides between candidates
#: that win the same number of games. That keeps the true objective in charge while restoring a
#: gradient in the saturated region.
#:
#: Run at least two of these. If they disagree about the champion, that disagreement is the finding.
FITNESS = ("winrate", "margin", "blend")


def evaluate(genome, opps, ex, seed0=SEED0, how="blend"):
    jobs = [(p, s, our, seed0 + i, genome)
            for i, (p, s, _n) in enumerate(opps) for our in (0, 1)]
    margins = list(ex.map(play, jobs))
    wins = statistics.mean(1.0 if m > 0 else (0.5 if m == 0 else 0.0) for m in margins)
    mean_margin = statistics.mean(margins)
    if how == "margin":
        return mean_margin, margins
    if how == "winrate":
        return wins, margins
    # One game is worth 1/len(margins) of the win-rate term; scale the margin tiebreak an order of
    # magnitude below that so it orders ties and nothing else.
    return wins + 0.1 * (mean_margin / 1e6) / max(1, len(margins)), margins


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gens", type=int, default=20)
    ap.add_argument("--pop", type=int, default=10)
    ap.add_argument("--opponents", type=int, default=16)
    ap.add_argument("--workers", type=int, default=14)
    ap.add_argument("--sigma", type=float, default=0.25)
    ap.add_argument("--holdout", type=int, default=24, help="fresh seed offset for the champion")
    ap.add_argument("--fitness", choices=FITNESS, default="blend")
    ap.add_argument("--out", default=str(ROOT / "logs/es_best.json"))
    args = ap.parse_args()

    sys.path.insert(0, str(ROOT))
    opps = opponents(args.opponents)
    rng = random.Random(7)
    n = len(SPACE)
    print(f"ES over {n} market parameters | {len(opps)} opponents x 2 seatings "
          f"= {2 * len(opps)} games per candidate | pop {args.pop} | gens {args.gens}", flush=True)
    print("opponents: " + ", ".join(nm for _p, _s, nm in opps), flush=True)

    base = shipped_genome()
    print("shipped genome: " + json.dumps({k: (v if not isinstance(v, float) else round(v, 3))
                                           for k, v in base.items()}), flush=True)

    # Start the mean AT the shipped configuration rather than at random: it is a working policy and
    # the search should have to beat it, not rediscover it.
    mean = []
    for name, (lo, hi, kind) in SPACE.items():
        v = base[name]
        v = float(v) if not isinstance(v, bool) else (1.0 if v else 0.0)
        mean.append(0.5 if hi == lo else min(1.0, max(0.0, (v - lo) / (hi - lo))))

    best_fit, best_g = None, None
    with cf.ProcessPoolExecutor(max_workers=args.workers) as ex:
        base_fit, _ = evaluate(base, opps, ex, how=args.fitness)
        print(f"gen  -  SHIPPED baseline fitness {base_fit:.4f}", flush=True)
        best_fit, best_g = base_fit, dict(base)

        # **CMA-ES, not the plain (mu, lambda) this started as.** The isotropic version takes one
        # step size in every direction, so it cannot learn that `FEED_DAYS_LATE` and
        # `FEED_DAYS_FROM_DAY` must move together, or that `RESERVATION_SLIP` wants small steps while
        # `SELL_OFFER_CAP` wants large ones. CMA learns the full covariance and rescales per
        # direction, which is worth a great deal when one evaluation is 32-48 full seasons.
        #
        # Full covariance is fine at n=14. It would NOT be at a few hundred genes: the matrix is
        # O(n^2) free parameters needing ~O(n^2) evaluations plus a periodic O(n^3) eigendecomposition,
        # and `CMA_diagonal` (sep-CMA) or a low-rank variant is the standard remedy there.
        try:
            import cma
        except ImportError:
            cma = None
            print("cma not installed; falling back to isotropic (mu, lambda)", flush=True)

        if cma is not None:
            es = cma.CMAEvolutionStrategy(
                mean, args.sigma,
                {"popsize": args.pop, "bounds": [0, 1], "seed": 7, "verbose": -9})
            for gen in range(args.gens):
                pop = es.ask()
                genomes = [decode(v) for v in pop]
                fits = [evaluate(g, opps, ex, how=args.fitness)[0] for g in genomes]
                es.tell(pop, [-f for f in fits])      # cma minimises; margin is to be maximised
                i = max(range(len(fits)), key=lambda k: fits[k])
                if fits[i] > best_fit:
                    best_fit, best_g = fits[i], genomes[i]
                    pathlib.Path(args.out).write_text(json.dumps(
                        {"fitness": best_fit, "genome": {k: (bool(v) if isinstance(v, bool) else v)
                                                         for k, v in best_g.items()}}, indent=1))
                print(f"gen {gen:2d}  best {fits[i]:>12.4f}  "
                      f"median {statistics.median(fits):>12.4f}  "
                      f"champion {best_fit:>12.4f}  (shipped {base_fit:.4f})  "
                      f"sigma {es.sigma:.3f}", flush=True)
        else:
            for gen in range(args.gens):
                pop = [[min(1.0, max(0.0, m + rng.gauss(0, args.sigma))) for m in mean]
                       for _ in range(args.pop)]
                scored = []
                for vec in pop:
                    g = decode(vec)
                    fit, _ = evaluate(g, opps, ex, how=args.fitness)
                    scored.append((fit, vec, g))
                scored.sort(key=lambda t: -t[0])
                elite = scored[: max(2, args.pop // 2)]
                mean = [statistics.mean(v[i] for _f, v, _g in elite) for i in range(n)]
                if scored[0][0] > best_fit:
                    best_fit, best_g = scored[0][0], scored[0][2]
                print(f"gen {gen:2d}  best ${scored[0][0]:>10,.0f}  "
                      f"champion {best_fit:>12.4f}  (shipped {base_fit:.4f})", flush=True)

        # **The winner's curse check.** A search winner is confirmed on seeds it never saw, or it is
        # noise -- this project has watched a fixed-seed objective report +40% where held-out seeds
        # said +12.8%.
        print("\nheld-out confirmation on fresh seeds:", flush=True)
        h = SEED0 + 10_000 + args.holdout
        b_out, _ = evaluate(base, opps, ex, seed0=h, how=args.fitness)
        c_out, _ = evaluate(best_g, opps, ex, seed0=h, how=args.fitness)
        print(f"  shipped  {b_out:.4f}\n  champion {c_out:.4f}\n  delta    {c_out - b_out:+.4f}",
              flush=True)
        print("\nchampion genome: " + json.dumps(
            {k: (bool(v) if isinstance(v, bool) else v) for k, v in best_g.items()}), flush=True)


if __name__ == "__main__":
    sys.exit(main())
