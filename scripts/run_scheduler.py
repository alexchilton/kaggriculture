"""Feed the calculated mix to the scheduler, score the result, compare against the beam.

The three-stage pipeline this project arrived at on 2026-08-05, run end to end:

    1. allocation_calculator.py   what to own      -- closed form from the drains
    2. scheduler.schedule()       when to own it   -- greedy by payback under a cash simulation
    3. jax_sim                    what it banks    -- the verifier, never the search engine

Stage 1 alone was measured at $13,479 (`data/logs/calculated_genome.log`): the right mix on a naive
schedule dies, because four cows and three sheep on day 5 is $3,100 against a $3,000 bank. The beam,
searching mix and schedule together, reached $72,543. This asks whether stage 2 recovers that.
"""

import argparse
import pathlib

import numpy as np
import jax
import jax.numpy as jnp
from jax import lax

from kagg.search import boards, chains as C, scheduler as S
from kagg.search import routines as R
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

ap = argparse.ArgumentParser()
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--sim-seed", type=int, default=0)
ap.add_argument("--slots", type=int, default=12)
ap.add_argument("--reserve", default="0,300,800,1500", help="cash reserves to sweep")
ap.add_argument("--out", default="data/chain_search_scheduled")
# **1.0, not 0.5.** Halving every drain for the opponent's share was added without measuring it and it
# halves the farm: 4 cows and 3 sheep instead of 8 and 6. The unhalved mix is the one that reproduces
# the leader exactly, and he wins against opponents who also sell -- so the drain a player can actually
# take is closer to the whole thing than to half.
ap.add_argument("--share", type=float, default=1.0)
args = ap.parse_args()

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


_ST = {}


def score(genome, n_slots):
    script, used, skipped = C.decode(genome, n_slots)
    arrs = script.arrays()
    cand = {f: jnp.asarray(np.stack([arrs[f][:T]])) for f in FIELDS}
    if 1 not in _ST:
        unlocks = boards.unlock_array(N_OPP, args.boards, 1, seed=args.sim_seed)
        _ST[1] = J.reset(len(unlocks), unlock_schedule=unlocks, seed=args.sim_seed)
    mine, theirs = _run(_ST[1], cand)
    mine, theirs = np.asarray(mine), np.asarray(theirs)
    return int((mine > theirs).sum()), float(mine.mean()), used, skipped


# ------------------------------------------------------------------ stage 1: the mix
from kagg.economics import production as P


def herd_target(a):
    an = R.ANIMALS[a]
    events = max(0, (R.SEASON_DAYS - an["first_yield_day"]) // max(an["interval"], 1))
    return int(np.ceil(C.DRAIN_UNITS[an["product"]] * args.share / max(events * an["max_held"], 1)))


def tiles_target(c):
    y = max(P.TILE_YIELD_FERTILIZED[c], P.TILE_YIELD_PER_SEASON[c])
    return int(np.ceil(C.DRAIN_UNITS[c] * args.share / max(y, 1e-9)))


print("stage 1 -- the mix, halved for the opponent's share of every drain")
targets = {"COW": herd_target("COW"), "SHEEP": herd_target("SHEEP")}
for c in ("STRAWBERRY", "MELON", "WHEAT"):
    targets[c] = tiles_target(c)
print(f"  {targets}   (leader: 8 cow, 6 sheep, 41 straw, 20 melon, 40 wheat)\n")

# Build the mix as concrete chains on concrete ground, nearest and rent-free first.
used_tiles, mix = set(), []


# **Never SE.** Reaching it costs all three parcels -- $7,000 -- and the leader never buys it: he owns
# NW, NE and SW, 75 tiles, for $3,000. Letting the allocator fall back to "any block" sprawled 18 chains
# over 92 tiles including four blocks behind the $7,000 gate, and the farm banked $2,147 with nine chains
# refused. A mix that cannot be reached is not a mix.
MAX_PARCELS = 2


def take(pool, want_free):
    for b in pool:
        tiles = tuple(b) if isinstance(b[0], tuple) else (b,)
        if set(tiles) & used_tiles:
            continue
        if R.land_purchases_for(tiles[0]) > MAX_PARCELS:
            continue
        if want_free and C.land_cost(tiles[0]) > 0:
            continue
        used_tiles.update(tiles)
        return tiles
    return None


groups = [g for g in C.RANCH_GROUPS if len(g) >= 3]
for animal, n in (("COW", targets["COW"]), ("SHEEP", targets["SHEEP"])):
    placed = 0
    while placed < n:
        g = take(groups, True) or take(groups, False)
        if g is None:
            break
        mix.append(("ranch", animal, g))
        placed += len(g)
for crop, n in (("WHEAT", targets["WHEAT"]), ("STRAWBERRY", targets["STRAWBERRY"]),
                ("MELON", targets["MELON"])):
    pool = C.WIDE_BLOCKS if crop == "STRAWBERRY" else C.NARROW_BLOCKS
    placed = 0
    while placed < n:
        b = take(pool, True) or take(pool, False)
        if b is None:
            break
        mix.append(("grow", crop, b))
        placed += len(b)
print(f"stage 1 produced {len(mix)} chains over {len(used_tiles)} tiles")
for k, w, t in mix:
    print(f"    {k:>5} {w:>11} {len(t)} tiles at {t[0]} (land ${C.land_cost(t[0]):,})")

# ------------------------------------------------------------------ stage 2 + 3
print()
print("=" * 96)
print("stage 2 -- greedy by payback under a cash simulation, then scored")
print("=" * 96)
print(f"{'reserve':>8} {'chains placed':>14} {'wins':>8} {'money':>11} {'skipped':>8}   land days")
out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
best = None
for reserve in [float(x) for x in args.reserve.split(",")]:
    sched, curve, parcels = S.schedule(mix, reserve=reserve)
    genome = S.to_genome(sched, args.slots)
    try:
        w, m, used, skipped = score(genome, args.slots)
    except Exception as exc:                          # noqa: BLE001
        print(f"{reserve:>8.0f}  FAILED: {type(exc).__name__}: {exc}")
        continue
    print(f"{reserve:>8.0f} {len(sched):>14} {w:>3}/{N_PAIRS:<4} {m:>11,.0f} {skipped:>8}   "
          f"{sorted(parcels.values())}")
    if best is None or (w, m) > (best[0], best[1]):
        best = (w, m, genome, sched, reserve)

if best:
    w, m, genome, sched, reserve = best
    np.savez_compressed(out / "best_beam_genome.npz", genome=genome, wins=w, money=m,
                        slots=args.slots)
    print(f"\nbest: reserve ${reserve:,.0f}, {w}/{N_PAIRS} wins, ${m:,.0f}")
    for k, wt, t, start, ld in sched[:args.slots]:
        print(f"    day {start:>2} (land {ld:>2})  {k:>5} {wt:>11} {len(t)} tiles at {t[0]}")
    print(f"\nwrote {out / 'best_beam_genome.npz'}")
    print("\nagainst the beam's $72,543 on the same 16 games.")
