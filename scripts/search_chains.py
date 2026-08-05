"""CEM over chain instances: choose which routines to run, where, and when.

This is the orchestration layer `kagg/search/routines.py` was written for and never had. The routines
guarantee that a chain is coherent; this decides which chains make a season. What the search owns is
strategy -- which routine, where, when, how many -- while correctness lives in the decoder, which is
the split `routines.py`'s own docstring argues for.

**Why CEM rather than the tape hill-climber.** Measured today on the same hardware: mutating the
winner's 720-turn tape moved it +0.5% in 40 iterations, and mutating our own tape +1.5%, from $28,333
against a $147,000 target (`data/logs/opt_fixed_slot_*.log`). Local edits polish; they do not build.
The gene-space CEM went from `pop mean 0.03` to `win 1.00, delta +53,358` in 30 generations on CPU
(`data/logs/cem_run_2026-08-04b.log`). Same game, same evaluator, two orders of magnitude difference in
what the representation permits.

**Every candidate is scored on the same set of boards.** `kagg/search/boards.py` exists because
`reset_with_shops` draws a fresh shop-unlock order per batch element, which made one identical tape
score $107,661 to $152,867 depending on where it sat in the batch. An argmax over that ranks boards,
not strategies. This script inherits the fix rather than repeating the bug.

**Selection is on wins, money only as a tie-break** -- `CLAUDE.md` is explicit that the ladder is Elo
and a $43k win scores the same as a $4k one.

    PYTHONPATH=. python3 -u scripts/search_chains.py --generations 30 --pop 64
"""

import argparse
import pathlib
import time

import jax
import jax.numpy as jnp
import numpy as np
from jax import lax

from kagg.search import boards, chains as C
from kagg.search import routines as R
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

ap = argparse.ArgumentParser()
ap.add_argument("--slots", type=int, default=8, help="chain instances per genome; slot i owns unit i")
ap.add_argument("--generations", type=int, default=30)
ap.add_argument("--pop", type=int, default=64)
ap.add_argument("--elite", type=float, default=0.2)
ap.add_argument("--resample", action="store_true", default=True,
                help="new board draw every generation; the default, and see evaluate()")
ap.add_argument("--no-resample", dest="resample", action="store_false",
                help="score every generation on one fixed draw (overfits; for comparison only)")
ap.add_argument("--seed-genome", default="data/chain_search_groups/best_beam_genome.npz",
                help="start from the beam's answer; the ES restructures what the beam cannot")
ap.add_argument("--holdout", type=int, default=8,
                help="unseen board draws to score the final genome on")
ap.add_argument("--smooth", type=float, default=0.3, help="how much of the old distribution to keep")
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--sim-seed", type=int, default=0)
ap.add_argument("--rng", type=int, default=0)
ap.add_argument("--out", default="data/chain_search")
args = ap.parse_args()

N_SLOTS = args.slots
N_GENES = C.n_genes(N_SLOTS)
GENE_SIZES = np.tile(np.asarray(C.GENE_SIZES), N_SLOTS)

print(f"slots {N_SLOTS} -> {N_GENES} genes; blocks {len(C.BLOCKS)} reachable "
      f"of {len(C.ALL_BLOCKS)} cut")
if C.UNREACHABLE_BLOCKS:
    # Never silently: a dropped block is board the search cannot reach at all.
    print(f"  {len(C.UNREACHABLE_BLOCKS)} blocks unreachable inside a 24-turn day: "
          f"{C.UNREACHABLE_BLOCKS}")

OPPONENTS = []
for name in args.opponents.split(","):
    p = pathlib.Path("data/seed_scripts") / f"{name.strip()}_seed{args.sim_seed}.npz"
    if not p.exists():
        raise SystemExit(f"missing opponent script {p}")
    b = np.load(p)
    OPPONENTS.append((name.strip(), {f: jnp.asarray(np.asarray(b[f])[:, 1]) for f in FIELDS}))

N_OPP = len(OPPONENTS)
N_PAIRS = boards.pair_count(N_OPP, args.boards)
OPP_XS = {f: jnp.stack([OPPONENTS[o][1][f]
                        for o in boards.opponent_of_pair(args.boards, N_PAIRS)], axis=1)
          for f in FIELDS}
T = int(OPP_XS["unit_op"].shape[0])
print(f"opponents ({N_OPP}): {', '.join(n for n, _ in OPPONENTS)}")
print(f"boards {args.boards} x opponents {N_OPP} = {N_PAIRS} games per candidate, {T} turns\n")


def _expand(mine_t, theirs_t, b):
    tail = mine_t.shape[1:]
    m = jnp.broadcast_to(mine_t[None], (N_PAIRS, b) + tail).reshape((N_PAIRS * b,) + tail)
    th = jnp.broadcast_to(theirs_t[:, None], (N_PAIRS, b) + tail).reshape((N_PAIRS * b,) + tail)
    return jnp.stack([m, th], axis=1)


@jax.jit
def _run(state0, cand):
    b = cand["unit_op"].shape[0]
    xs = {f: jnp.swapaxes(cand[f], 0, 1) for f in FIELDS}

    def body(st, pair):
        mine, theirs = pair
        acts = J.Actions(**{f: _expand(mine[f], theirs[f], b) for f in FIELDS})
        return J.step(st, acts, weed_chance=0.0), None

    state, _ = lax.scan(body, state0, (xs, OPP_XS), length=T)
    return (state.farm.money[:, 0].reshape(N_PAIRS, b),
            state.farm.money[:, 1].reshape(N_PAIRS, b))


_STATES = {}


def evaluate(genomes, seed=None):
    """`(wins[N], mean_money[N], skipped[N])` for a population, on the board draw `seed`.

    **`seed` is resampled every generation, and that is not optional.** With it fixed, thirty
    generations of five hundred candidates all fit the same sixteen games, and CLAUDE.md records what
    that costs: "a fixed 3-seed objective reported +40% where held-out seeds said +12.8%", and "11
    accepted moves in 14 generations for +1.6%". The whole point of an ES here is that it can
    restructure a genome where the beam cannot; overfitting one board draw would spend that freedom on
    noise.

    The states are cached per `(batch, seed)` because `_run` is jitted on the batch shape, so a new
    seed costs a `J.reset` but no recompile.
    """
    seed = args.sim_seed if seed is None else seed
    scripts, skips = [], []
    for g in genomes:
        script, _used, skipped = C.decode(g, N_SLOTS)
        scripts.append(script.arrays())
        skips.append(skipped)
    b = len(scripts)
    cand = {f: jnp.asarray(np.stack([s[f][:T] for s in scripts])) for f in FIELDS}
    key = (b, seed)
    if key not in _STATES:
        unlocks = boards.unlock_array(N_OPP, args.boards, b, seed=seed)
        _STATES[key] = J.reset(len(unlocks), unlock_schedule=unlocks, seed=seed)
    mine, theirs = _run(_STATES[key], cand)
    mine, theirs = np.asarray(mine), np.asarray(theirs)
    return (mine > theirs).sum(axis=0).astype(float), mine.mean(axis=0), np.asarray(skips)


rng = np.random.default_rng(args.rng)
# Uniform over each gene's own arity, so a gene with 24 values is not squeezed into the same shape as
# one with 3. Ragged, hence a list rather than an array.
probs = [np.full(int(k), 1.0 / int(k)) for k in GENE_SIZES]

# Start from the beam's answer when there is one. The beam finds a good basin cheaply and cannot
# restructure out of it -- greedy forward selection commits a slot and `--refine` only sweeps timing --
# which is exactly the division of labour: beam for the basin, ES to rearrange inside and out of it.
seed_g = C.seeded_genome(N_SLOTS)
if args.seed_genome:
    sp = pathlib.Path(args.seed_genome)
    if sp.exists():
        loaded = np.asarray(np.load(sp)["genome"], dtype=np.int64)
        if loaded.size == N_GENES:
            seed_g = loaded
            print(f"seeded from {sp}")
        else:
            # A stride change makes an old genome unreadable rather than merely stale; say so.
            print(f"ignoring {sp}: {loaded.size} genes against {N_GENES} for {N_SLOTS} slots")
    else:
        print(f"ignoring {sp}: not found")
w, m, sk = evaluate(seed_g[None])
print(f"seed genome: {w[0]:.0f}/{N_PAIRS} wins, ${m[0]:,.0f}, {sk[0]} chains skipped\n")

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
best = (float(w[0]), float(m[0]), seed_g.copy())
t0 = time.time()

for gen in range(args.generations):
    sampled = np.stack([np.asarray([rng.choice(len(p), p=p) for p in probs])
                        for _ in range(args.pop - 1)])
    # The incumbent is always in the population, so it is **re-scored on this generation's board draw**
    # alongside its challengers. Without that it would keep whatever score its lucky draw gave it and
    # could never be displaced -- the winner's curse made permanent.
    pop = np.concatenate([best[2][None], sampled])

    gen_seed = args.sim_seed + gen * 1_000_003 if args.resample else args.sim_seed
    wins, money, skipped = evaluate(pop, seed=gen_seed)
    order = np.lexsort((money, wins))[::-1]
    n_elite = max(2, int(args.elite * args.pop))
    elite = pop[order[:n_elite]]

    for j, p in enumerate(probs):
        counts = np.bincount(elite[:, j], minlength=len(p)).astype(float)
        fresh = counts / counts.sum()
        probs[j] = args.smooth * p + (1.0 - args.smooth) * fresh

    # Compare on the SAME draw: index 0 is the incumbent, freshly scored this generation. Comparing a
    # challenger's new score against the incumbent's remembered one is how a search wanders.
    k = int(order[0])
    if (float(wins[k]), float(money[k])) > (float(wins[0]), float(money[0])):
        best = (float(wins[k]), float(money[k]), pop[k].copy())
        np.savez_compressed(out / "best_chain_genome.npz", genome=best[2], wins=best[0],
                            money=best[1], slots=N_SLOTS, gen=gen)
    else:
        best = (float(wins[0]), float(money[0]), best[2])

    print(f"gen {gen:>3} | seed {gen_seed:>10} | incumbent {wins[0]:.0f}/{N_PAIRS} "
          f"${money[0]:>10,.0f} | best this gen {wins[k]:.0f}/{N_PAIRS} ${money[k]:>10,.0f} | "
          f"elite wins {wins[order[:n_elite]].mean()/N_PAIRS:.2f} | "
          f"skipped {skipped.mean():.1f}/{N_SLOTS} | {time.time()-t0:.0f}s", flush=True)

script, used, skipped = C.decode(best[2], N_SLOTS)
print(f"\nbest on its own draw: {best[0]:.0f}/{N_PAIRS} wins, ${best[1]:,.0f}, "
      f"{skipped} chains skipped")
for u in used:
    print("   ", u)

# **Held out.** The search saw every board draw it was scored on, so its own number is optimistic by
# construction. These draws it has never seen, and the spread across them is the honest answer --
# CLAUDE.md: "seed variance is ~15%. Always quote the seed range."
holdout = [args.sim_seed + 500_000 + i for i in range(args.holdout)]
if holdout:
    hw, hm = [], []
    for sd in holdout:
        w1, m1, _ = evaluate(best[2][None], seed=sd)
        hw.append(float(w1[0])); hm.append(float(m1[0]))
    print(f"\nheld out on {len(holdout)} unseen draws: "
          f"wins {np.mean(hw):.1f}/{N_PAIRS} (min {min(hw):.0f}, max {max(hw):.0f}), "
          f"money ${np.mean(hm):,.0f} (${min(hm):,.0f} - ${max(hm):,.0f})")
    print(f"in-search money ${best[1]:,.0f} vs held-out ${np.mean(hm):,.0f} "
          f"({np.mean(hm) / max(best[1], 1) - 1:+.1%}) -- the winner's curse, measured")

print(f"\nwrote {out / 'best_chain_genome.npz'}")
print("NOT a competitive number yet: recorded opponents, weeds off, one sim seed. Score it on "
      "kagg.arena across fresh seeds before believing it.")
