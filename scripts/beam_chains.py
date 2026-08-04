"""The Bellman over chain actions: one exact joint max per slot, with the simulator as the model.

`docs/fable_bellman_route_and_crop_spec_2026-08-04.md` proposed fitted-Q over 30 day-decisions and named
the thing that would kill it: **the action-space explosion recurs one level up.** If a day's action is
several independent discrete heads under an argmax, the failure this project has already measured three
times rebuilds itself with chains as the vocabulary -- nine independent "probably not sell" marginals
composing into "never sell".

This is the same Bellman with that trap closed, and it closes it by not needing a network:

- **The decision sequence is slots, not turns.** Slot `k` owns unit `k`, so there are 8 decisions in a
  season rather than 720. `V(s)` is the final bank of the partial farm, which is the terminal reward the
  project has ruled on -- no shaping, no discounting.
- **The model is exact.** The simulator is deterministic given a board, so `Q(s, a) = V(s')` needs no
  approximation, no replay buffer and no TD error. Fitted-Q exists to *estimate* what we can compute.
- **One joint max per slot, over the whole catalog.** Every `(kind, what, block)` is enumerated and
  scored, so there are no per-head marginals to compose badly. This is the "small enumerable catalog"
  the spec asked for, made large enough to be interesting by evaluating it in a batch.

A beam rather than pure greedy, because chains interact: melon's value depends on how much melon is
already planted, and greedy would commit to the first slot's argmax before knowing that. Width `--beam`
carries the top few partial farms forward. Then `--refine` passes sweep each slot's timing with the rest
held fixed -- coordinate descent on the schedule, which is where the money is once the mix is right.

**What this is not.** It is not a learned value function, and it cannot generalise to a board it has not
been run on. If the state space grows past what exhaustive evaluation can reach -- more slots, or a
per-day decision -- the learned Q comes back and this becomes the thing that generates its training
targets. Until then, an exact model beats an estimate of one.

    PYTHONPATH=. python3 -u scripts/beam_chains.py --beam 4 --refine 2
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
ap.add_argument("--slots", type=int, default=8)
ap.add_argument("--beam", type=int, default=16, help="partial farms carried between slot decisions")
ap.add_argument("--per-kind", type=int, default=2,
                help="most beam entries allowed to add the same (kind, what) at one slot")
ap.add_argument("--refine", type=int, default=2, help="coordinate-descent passes over timing")
ap.add_argument("--chunk", type=int, default=64, help="candidates per simulator batch")
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--sim-seed", type=int, default=0)
ap.add_argument("--out", default="data/chain_search")
# The leader tape buys its two parcels on days 7 and 10 and never buys the third. Our catalog offered
# day 0 only, and day 0 is the one day nothing has been earned -- `data/logs/land_day7.log` measures
# waiting at up to +$22,911 on a 4-pen farm. Pin it here to test the leader's shape directly; the
# `--refine` passes still sweep the whole grid afterwards unless `--pin-land` holds it.
ap.add_argument("--force-land-day", type=int, default=0,
                help="day every land-needing chain orders its first parcel (leader uses 7)")
ap.add_argument("--pin-land", action="store_true",
                help="keep --force-land-day through refinement instead of re-sweeping it")
args = ap.parse_args()

N_SLOTS = args.slots
CHUNK = args.chunk

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


_STATE = None
_N_EVALS = 0


def _state():
    """One board assignment, built once. Fixed `CHUNK` so `_run` compiles exactly once."""
    global _STATE
    if _STATE is None:
        unlocks = boards.unlock_array(N_OPP, args.boards, CHUNK, seed=args.sim_seed)
        _STATE = J.reset(len(unlocks), unlock_schedule=unlocks, seed=args.sim_seed)
    return _STATE


def values(genomes):
    """`(wins, money)` per genome. Chunked and padded so the batch shape never varies."""
    global _N_EVALS
    _N_EVALS += len(genomes)
    wins = np.zeros(len(genomes))
    money = np.zeros(len(genomes))
    for lo in range(0, len(genomes), CHUNK):
        block = genomes[lo:lo + CHUNK]
        pad = CHUNK - len(block)
        scripts = [C.decode(g, N_SLOTS)[0].arrays() for g in block]
        scripts += [C.decode(block[-1], N_SLOTS)[0].arrays()] * pad
        cand = {f: jnp.asarray(np.stack([s[f][:T] for s in scripts])) for f in FIELDS}
        mine, theirs = _run(_state(), cand)
        mine, theirs = np.asarray(mine), np.asarray(theirs)
        wins[lo:lo + len(block)] = (mine > theirs).sum(axis=0)[:len(block)]
        money[lo:lo + len(block)] = mine.mean(axis=0)[:len(block)]
    return wins, money


# --------------------------------------------------------------------------
# The action catalog
# --------------------------------------------------------------------------
# A slot's gene row is (kind, what, block, start_day, land_day, fertilize). Land is only a decision
# where the tile is not already owned, so NW collapses to one land choice instead of six -- that is a
# 6x saving on three quarters of the catalog and changes nothing, because `buy_land` on owned land is
# a no-op.
DEFAULT_START = 2
DEFAULT_START_I = C.START_DAY_CHOICES.index(DEFAULT_START)


FORCED_LAND_I = C.LAND_DAY_CHOICES.index(args.force_land_day)


def _land_choices(tile):
    if C.land_cost(tile) == 0:
        return (0,)
    if args.pin_land:
        return (FORCED_LAND_I,)
    return tuple(range(len(C.LAND_DAY_CHOICES)))


def catalog(slot):
    """Every chain instance slot `slot` may hold, at the default timing. One joint max runs over this.

    Timing is deliberately *not* in here. Crossing mix with schedule multiplies the catalog by 42 and
    the mix is what decides whether a slot is worth owning at all; the `--refine` passes then sweep
    timing with the mix fixed. Two cheap exhaustive sweeps beat one that cannot be afforded.
    """
    out = [("off", 0, 0, 0, 0, 0, 0)]
    for c_i, crop in enumerate(R.CROPS):
        # The fertilized variant only where it can differ. Melon yields 12 per tile either way, so a
        # `fertilize=1` melon decodes to an identical script and would just be scored twice. When it
        # does fertilize, both funding routes are offered: buy the units (`fert_trade=1`) or take
        # whatever the herd left in the shed (`fert_trade=0`).
        ferts = ((0, 0), (1, 0), (1, 1)) if crop in R.FERTILIZER_HELPS else ((0, 0),)
        for b_i, block in enumerate(C.BLOCKS):
            land_i = 0 if C.land_cost(block[0]) == 0 else FORCED_LAND_I
            for f, trade in ferts:
                out.append(("grow", c_i, b_i, DEFAULT_START_I, land_i, f, trade))
    # Any slot may now propose a pen on any tile. The old rule -- slot `k` offered cell `k` only --
    # existed because a shed pen's unit is fixed by its cell, and it meant the beam could never put an
    # animal on a cell a crop had already taken. Off the shed the slot owns its own unit, so the
    # binding is gone and the herd is no longer capped at four.
    for a_i in range(len(R.ANIMAL_NAMES)):
        for t_i, tile in enumerate(C.RANCH_TILES):
            parcels = R.land_purchases_for(tile)
            land_i = 0 if not parcels else FORCED_LAND_I
            # **The pen must start after its ground arrives.** `routines.py` spaces a chain's parcels
            # one per day from `land_day`, so the last one lands on `land_day + parcels - 1` and the
            # animal can only be placed the day after. Offering a day-0 pen on a day-7 parcel makes
            # PLACE fail silently on locked ground -- which is how the first seeded genome bought four
            # animals and placed one.
            start = 0 if not parcels else min(R.SEASON_DAYS - 2,
                                              C.LAND_DAY_CHOICES[land_i] + parcels)
            start_i = C.START_DAY_CHOICES.index(start)
            # Both fertilizer dispositions: sell the herd's output, or leave it in the shed for the
            # crop chains. Rival uses of one good, and the farm used to do both blindly.
            for trade in (0, 1):
                out.append(("ranch", a_i, t_i, start_i, land_i, 0, trade))
    return out


def with_slot(genome, slot, action):
    g = np.asarray(genome, dtype=np.int64).reshape(N_SLOTS, len(C.GENES)).copy()
    kind, what, block, start_i, land_i, fert_i, trade_i = action
    g[slot] = (C.KINDS.index(kind), what, block, start_i, land_i, fert_i, trade_i)
    return g.reshape(-1)


def describe(genome):
    _script, used, skipped = C.decode(genome, N_SLOTS)
    return used, skipped


# --------------------------------------------------------------------------
# Forward pass: one exact max per slot, beam width B
# --------------------------------------------------------------------------
t0 = time.time()
empty = np.zeros(N_SLOTS * len(C.GENES), dtype=np.int64)
w0, m0 = values([empty])
beam = [(float(w0[0]), float(m0[0]), empty)]
print(f"{N_PAIRS} games per candidate, {T} turns, chunk {CHUNK}")
print(f"empty farm: {w0[0]:.0f}/{N_PAIRS} wins, ${m0[0]:,.0f}\n")

for slot in range(N_SLOTS):
    cat = catalog(slot)
    cands, provenance = [], []
    for bi, (_w, _m, g) in enumerate(beam):
        for a in cat:
            cands.append(with_slot(g, slot, a))
            provenance.append((bi, a))
    wins, money = values(cands)
    order = np.lexsort((money, wins))[::-1]
    # **Diversity cap, and it is load-bearing.** Without it the six melon blocks on land we already
    # own tie at exactly $15,241, four identical ideas fill a width-4 beam, and every structurally
    # different option is dropped at slot 0 and never reconsidered. Measured in
    # `data/logs/animal_diagnostic_fixed.log`: the best pen ranks 12 of 124 while being worth
    # **+$2,167** over the melon block it would displace. The search was not rejecting animals, it
    # could not see them. Capping how many entries may add the same `(kind, what)` costs nothing and
    # makes the beam carry distinct strategies rather than near-duplicates of one.
    beam, per_key = [], {}
    for i in order:
        action = provenance[i][1]
        key = (action[0], action[1])
        if per_key.get(key, 0) >= args.per_kind:
            continue
        per_key[key] = per_key.get(key, 0) + 1
        beam.append((float(wins[i]), float(money[i]), cands[i]))
        if len(beam) >= args.beam:
            break
    bw, bm, bg = beam[0]
    used, _ = describe(bg)
    print(f"slot {slot} | {len(cands):>5} evaluated | best {bw:.0f}/{N_PAIRS} ${bm:>10,.0f} | "
          f"beam holds {len(per_key)} distinct kinds | {used[-1] if used else 'off'} | "
          f"{time.time()-t0:.0f}s", flush=True)

best = beam[0]
print(f"\nforward pass: {best[0]:.0f}/{N_PAIRS} wins, ${best[1]:,.0f} "
      f"({_N_EVALS:,} evaluations, {time.time()-t0:.0f}s)")

# --------------------------------------------------------------------------
# Refinement: sweep each slot's timing with every other slot held fixed
# --------------------------------------------------------------------------
for sweep in range(args.refine):
    moved = 0
    for slot in range(N_SLOTS):
        g = best[2].reshape(N_SLOTS, len(C.GENES))
        if C.KINDS[int(g[slot, 0]) % len(C.KINDS)] == "off":
            continue
        kind = C.KINDS[int(g[slot, 0])]
        tile = (C.RANCH_TILES[int(g[slot, 2]) % len(C.RANCH_TILES)] if kind == "ranch"
                else C.BLOCKS[int(g[slot, 2]) % len(C.BLOCKS)][0])
        cands = []
        for s_i in range(len(C.START_DAY_CHOICES)):
            for l_i in _land_choices(tile):
                # Land after the chain starts is money spent on a pen that cannot be built yet.
                if C.LAND_DAY_CHOICES[l_i] > C.START_DAY_CHOICES[s_i] and C.land_cost(tile) > 0:
                    continue
                cands.append(with_slot(best[2], slot,
                                       (kind, int(g[slot, 1]), int(g[slot, 2]), s_i, l_i,
                                        int(g[slot, 5]), int(g[slot, 6]))))
        if not cands:
            continue
        wins, money = values(cands)
        k = int(np.lexsort((money, wins))[-1])
        if (float(wins[k]), float(money[k])) > (best[0], best[1]):
            best = (float(wins[k]), float(money[k]), cands[k])
            moved += 1
    print(f"refine {sweep} | {moved} slots retimed | {best[0]:.0f}/{N_PAIRS} ${best[1]:,.0f} | "
          f"{time.time()-t0:.0f}s", flush=True)
    if moved == 0:
        break

used, skipped = describe(best[2])
print(f"\nbest: {best[0]:.0f}/{N_PAIRS} wins, ${best[1]:,.0f}, {skipped} chains skipped")
for u in used:
    print("   ", u)

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
dest = out / "best_beam_genome.npz"
np.savez_compressed(dest, genome=best[2], wins=best[0], money=best[1], slots=N_SLOTS)
print(f"\n{_N_EVALS:,} simulator evaluations in {time.time()-t0:.0f}s")
print(f"wrote {dest}")
print("NOT a competitive number yet: recorded opponents, weeds off, one sim seed. Score it on "
      "kagg.arena across fresh seeds before believing it.")
