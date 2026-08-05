"""Exhaustive local search over the genome. The right tool for a deterministic objective.

The season is a deterministic function of the tape, and the tape is a deterministic function of 64
integers. Nothing about that calls for sampling. So instead of a distribution over genomes, sweep every
gene through every one of its values, keep the best single change, and repeat until nothing improves.

What that buys over what we had been running:

| method                  | neighbourhood                       | guarantee                     |
|-------------------------|-------------------------------------|-------------------------------|
| `beam_chains --refine`  | one slot, **timing genes only**     | none beyond timing            |
| `search_chains` (CEM)   | random draws from a distribution    | none                          |
| this                    | **every gene, every value**         | a 1-change local optimum      |

The beam's refine pass is already a coordinate descent; it is just restricted to `start_day` and
`land_day`. Widening it to all eight genes is the step that was missing, and it is the one that can ask
"slot 6 is off -- is *any* chain better there?", which is where the beam left two slots idle at
$76,728.

Cost: 64 genes x up to 84 values is ~5,400 candidates a sweep, 1,024 per GPU call, so roughly six calls
and a couple of minutes.

**Steepest descent, not first-improvement.** Every neighbour is scored before anything is accepted, so
the path is reproducible and the report can say exactly which change was worth what. On a deterministic
objective there is no reason to accept the first improvement found.

    PYTHONPATH=. python -u scripts/local_search.py --genome data/chain_search_groups/best_beam_genome.npz
"""

import argparse
import pathlib
import time

import numpy as np
import jax
import jax.numpy as jnp
from jax import lax

from kagg.search import boards, chains as C
from kagg.search import routines as R
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

ap = argparse.ArgumentParser()
ap.add_argument("--genome", default="data/chain_search_groups/best_beam_genome.npz")
ap.add_argument("--slots", type=int, default=8)
ap.add_argument("--sweeps", type=int, default=12)
ap.add_argument("--chunk", type=int, default=1024)
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--sim-seed", type=int, default=0)
ap.add_argument("--holdout", type=int, default=8,
                help="unseen board draws to score the final genome on")
ap.add_argument("--out", default="data/chain_search_local")
# Coarse grids for the macro moves. The full cross-product of block x land_day x start_day is far too
# large; these are the days that matter -- the leader buys on 7 and 10, and a chain starting before its
# ground arrives is the defect this is meant to avoid. Single-gene sweeps still cover every day, so the
# fine timing is found there once the structure is right.
ap.add_argument("--land-day-moves", default="0,4,7,10,14")
ap.add_argument("--start-day-moves", default="0,2,5,8,11,14,18")
args = ap.parse_args()

N_SLOTS = args.slots
CHUNK = args.chunk
LAND_DAY_MOVES = [int(x) for x in args.land_day_moves.split(",")]
START_DAY_MOVES = [int(x) for x in args.start_day_moves.split(",")]

OPPONENTS = []
for name in args.opponents.split(","):
    b = np.load(pathlib.Path("data/seed_scripts") / f"{name.strip()}_seed{args.sim_seed}.npz")
    OPPONENTS.append({f: jnp.asarray(np.asarray(b[f])[:, 1]) for f in FIELDS})
N_OPP = len(OPPONENTS)
N_PAIRS = boards.pair_count(N_OPP, args.boards)
OPP_XS = {f: jnp.stack([OPPONENTS[o][f]
                        for o in boards.opponent_of_pair(args.boards, N_PAIRS)], axis=1)
          for f in FIELDS}
T = int(OPP_XS["unit_op"].shape[0])


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
_N_EVALS = 0


def _state(seed):
    """One board assignment per seed, at a fixed `CHUNK` so `_run` compiles exactly once."""
    if seed not in _STATES:
        unlocks = boards.unlock_array(N_OPP, args.boards, CHUNK, seed=seed)
        _STATES[seed] = J.reset(len(unlocks), unlock_schedule=unlocks, seed=seed)
    return _STATES[seed]


def values(genomes, seed=None):
    """`(wins, mean money)` per genome. Chunked and padded so the batch shape never varies."""
    global _N_EVALS
    seed = args.sim_seed if seed is None else seed
    _N_EVALS += len(genomes)
    wins = np.zeros(len(genomes))
    money = np.zeros(len(genomes))
    for lo in range(0, len(genomes), CHUNK):
        block = genomes[lo:lo + CHUNK]
        pad = CHUNK - len(block)
        scripts = [C.decode(g, N_SLOTS)[0].arrays() for g in block]
        scripts += [C.decode(block[-1], N_SLOTS)[0].arrays()] * pad
        cand = {f: jnp.asarray(np.stack([s[f][:T] for s in scripts])) for f in FIELDS}
        mine, theirs = _run(_state(seed), cand)
        mine, theirs = np.asarray(mine), np.asarray(theirs)
        wins[lo:lo + len(block)] = (mine > theirs).sum(axis=0)[:len(block)]
        money[lo:lo + len(block)] = mine.mean(axis=0)[:len(block)]
    return wins, money


# --------------------------------------------------------------------------
# The neighbourhood: every gene of every slot, through every legal value
# --------------------------------------------------------------------------
def gene_values(slot, gene_i, genome):
    """Every value gene `gene_i` can take, with the pointless ones dropped.

    `decode()` takes each gene modulo the vocabulary it indexes, so a value beyond the arity is a
    duplicate of one below it. Dropping those is not an approximation -- it removes candidates that
    decode to a tape already in the sweep.
    """
    g = np.asarray(genome, dtype=np.int64).reshape(N_SLOTS, len(C.GENES))
    name = C.GENES[gene_i]
    kind = C.KINDS[int(g[slot, 0]) % len(C.KINDS)]
    if name == "kind":
        return range(len(C.KINDS))
    if name == "what":
        return range(len(R.ANIMAL_NAMES) if kind == "ranch" else len(R.CROPS))
    if name == "block":
        return range(len(C.RANCH_GROUPS) if kind == "ranch" else len(C.BLOCKS))
    if name == "start_day":
        return range(len(C.START_DAY_CHOICES))
    if name == "land_day":
        return range(len(C.LAND_DAY_CHOICES))
    return range(2)                          # fertilize / fert_trade / feed_loop


def neighbours(genome):
    """Every single-gene change, plus the coordinated moves single changes cannot reach.

    **Why macro moves are necessary and not a luxury.** Some genes are only worth anything together, and
    steepest descent one gene at a time cannot cross the valley between:

    * `block` and `land_day`. Moving a chain to NE without funding the parcel buys land on whatever day
      `land_day` already says -- day 0 for most slots, the cash trap. Setting `land_day` alone does
      nothing at all, because a chain on NW needs no parcel: every one of the six land_day genes in the
      best genome of 2026-08-05 was **inert**, and sweeping all 31 values changed not one turn. That is
      the reason a farm on 25 tiles never bought its way onto 75.
    * filling an OFF slot. It needs a `kind`, a `block` and a `start_day` at once; any one alone is a
      no-op or a loss. Two slots sat idle at $81,102 for exactly this reason.

    This is the same argument `routines.py` makes about partial chains -- a prefix is money-negative, so
    the fix is to make the whole thing one move -- applied a level up.
    """
    g = np.asarray(genome, dtype=np.int64).reshape(N_SLOTS, len(C.GENES))
    out = []
    for slot in range(N_SLOTS):
        for gi, name in enumerate(C.GENES):
            for v in gene_values(slot, gi, genome):
                if v == int(g[slot, gi]):
                    continue
                h = g.copy()
                h[slot, gi] = v
                out.append((h.reshape(-1), slot, name, v))

    b_i, l_i, k_i, s_i = (C.GENES.index(n) for n in ("block", "land_day", "kind", "start_day"))
    land_days = [C.LAND_DAY_CHOICES.index(d) for d in LAND_DAY_MOVES
                 if d in C.LAND_DAY_CHOICES]

    # (block, land_day) jointly: move a chain onto ground that needs buying AND fund the parcel.
    for slot in range(N_SLOTS):
        kind = C.KINDS[int(g[slot, 0]) % len(C.KINDS)]
        if kind == "off":
            continue
        pool = C.RANCH_GROUPS if kind == "ranch" else C.BLOCKS
        for bi, ground in enumerate(pool):
            if R.land_purchases_for(ground[0]) == 0:
                continue                      # no parcel needed, so the pairing adds nothing
            for li in land_days:
                h = g.copy()
                h[slot, b_i] = bi
                h[slot, l_i] = li
                out.append((h.reshape(-1), slot, "block+land_day",
                            f"{ground[0]}@{C.LAND_DAY_CHOICES[li]}"))

    # Fill an OFF slot: kind, block, start_day and land_day together.
    for slot in range(N_SLOTS):
        if C.KINDS[int(g[slot, 0]) % len(C.KINDS)] != "off":
            continue
        for kind in ("grow", "ranch"):
            pool = C.RANCH_GROUPS if kind == "ranch" else C.BLOCKS
            for bi, ground in enumerate(pool):
                need = R.land_purchases_for(ground[0])
                for sd in START_DAY_MOVES:
                    if sd not in C.START_DAY_CHOICES:
                        continue
                    for li in (land_days if need else [C.LAND_DAY_CHOICES.index(0)]):
                        if need and C.LAND_DAY_CHOICES[li] > sd:
                            continue          # ground must arrive before the chain starts
                        h = g.copy()
                        h[slot, k_i] = C.KINDS.index(kind)
                        h[slot, b_i] = bi
                        h[slot, s_i] = C.START_DAY_CHOICES.index(sd)
                        h[slot, l_i] = li
                        out.append((h.reshape(-1), slot, f"fill:{kind}",
                                    f"{ground[0]}@d{sd}/land{C.LAND_DAY_CHOICES[li]}"))
    return out


# --------------------------------------------------------------------------
loaded = np.load(args.genome)
genome = np.asarray(loaded["genome"], dtype=np.int64)
if genome.size != N_SLOTS * len(C.GENES):
    raise SystemExit(f"{args.genome} has {genome.size} genes; {N_SLOTS} slots needs "
                     f"{N_SLOTS * len(C.GENES)} (a stride change makes old genomes unreadable)")

w, m = values([genome])
best = (float(w[0]), float(m[0]), genome.copy())
print(f"backend {jax.default_backend()}, {N_PAIRS} games per candidate, chunk {CHUNK}")
print(f"start: {best[0]:.0f}/{N_PAIRS} wins, ${best[1]:,.0f} from {args.genome}\n")

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
t0 = time.time()

for sweep in range(args.sweeps):
    cands = neighbours(best[2])
    wins, money = values([c[0] for c in cands])
    order = np.lexsort((money, wins))[::-1]
    k = int(order[0])
    # Steepest descent: everything is scored, then the single best change is taken.
    if (float(wins[k]), float(money[k])) <= (best[0], best[1]):
        print(f"sweep {sweep}: no single-gene change improves on "
              f"{best[0]:.0f}/{N_PAIRS} ${best[1]:,.0f} -- this is a 1-change LOCAL OPTIMUM "
              f"({len(cands):,} neighbours checked, {_N_EVALS:,} evaluations, "
              f"{time.time()-t0:.0f}s)")
        break
    _g, slot, name, v = cands[k]
    print(f"sweep {sweep}: slot {slot} {name} -> {v} | {wins[k]:.0f}/{N_PAIRS} "
          f"${money[k]:>10,.0f} | {money[k] - best[1]:>+9,.0f} | {len(cands):,} neighbours | "
          f"{time.time()-t0:.0f}s", flush=True)
    best = (float(wins[k]), float(money[k]), cands[k][0].copy())
    np.savez_compressed(out / "best_beam_genome.npz", genome=best[2], wins=best[0],
                        money=best[1], slots=N_SLOTS)
else:
    print(f"\nstopped at the sweep limit ({args.sweeps}); this is NOT a proven local optimum")

script, used, skipped = C.decode(best[2], N_SLOTS)
print(f"\nbest: {best[0]:.0f}/{N_PAIRS} wins, ${best[1]:,.0f}, {skipped} chains skipped")
for u in used:
    print("   ", u)

# Held out. The search saw only `--sim-seed`; these draws it has never seen, and the spread is the
# honest answer -- CLAUDE.md: "seed variance is ~15%. Always quote the seed range."
if args.holdout:
    hw, hm = [], []
    for sd in [args.sim_seed + 500_000 + i for i in range(args.holdout)]:
        w1, m1 = values([best[2]], seed=sd)
        hw.append(float(w1[0])); hm.append(float(m1[0]))
    print(f"\nheld out on {len(hm)} unseen draws: wins {np.mean(hw):.1f}/{N_PAIRS} "
          f"(min {min(hw):.0f}, max {max(hw):.0f}), money ${np.mean(hm):,.0f} "
          f"(${min(hm):,.0f} - ${max(hm):,.0f})")
    print(f"in-search ${best[1]:,.0f} vs held-out ${np.mean(hm):,.0f} "
          f"({np.mean(hm) / max(best[1], 1) - 1:+.1%}) -- the winner's curse, measured")

print(f"\nwrote {out / 'best_beam_genome.npz'} ({_N_EVALS:,} evaluations in {time.time()-t0:.0f}s)")
