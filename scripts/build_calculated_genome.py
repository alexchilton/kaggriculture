"""Build a genome straight from the calculated allocation and score it. No beam.

`scripts/allocation_calculator.py` derives the target mix in closed form from the town's drains and the
measured per-tile yields, and it lands on the leader's farm: 7.6 cows against his 8, 5.9 sheep against
his 6, 47.7 strawberry tiles against his 41.
If the mix is computable, the obvious question is why go through a search at all -- so this writes the
computed allocation into a genome and evaluates it directly.

Two things the calculator does **not** give, and this script has to supply:

* **The schedule.** Cash is a flow, not a stock: strawberry's ground is unaffordable until the wheat has
  paid. The dependency chain is melon and wheat in NW on day 0-2, revenue by day 3, parcels on days 7
  and 10, strawberry on the new ground days 7-14. That is the leader's timeline and it is used here as a
  *given*, not as something discovered.
* **The slot budget.** The allocation needs more chains than eight slots hold, which is measured below
  rather than assumed. Extra slots cost hires on a Fibonacci ladder that resets daily, so the sweep runs
  several slot counts and prints what each one actually banks.

The comparison that matters is against the beam's best on the same 16 games. If the calculated genome
wins, the search was only ever finding what arithmetic could have told us. If it loses, the schedule --
or something else the calculator cannot see -- is doing more work than the mix.
"""

import argparse
import pathlib

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
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--sim-seed", type=int, default=0)
ap.add_argument("--slots", default="8,10,12,14", help="slot counts to sweep")
ap.add_argument("--out", default="data/chain_search_calculated")
args = ap.parse_args()

OPPONENTS = []
for name in args.opponents.split(","):
    p = pathlib.Path("data/seed_scripts") / f"{name.strip()}_seed{args.sim_seed}.npz"
    b = np.load(p)
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


def score(genome, n_slots):
    script, used, skipped = C.decode(genome, n_slots)
    arrs = script.arrays()
    cand = {f: jnp.asarray(np.stack([arrs[f][:T]])) for f in FIELDS}
    if 1 not in _STATES:
        unlocks = boards.unlock_array(N_OPP, args.boards, 1, seed=args.sim_seed)
        _STATES[1] = J.reset(len(unlocks), unlock_schedule=unlocks, seed=args.sim_seed)
    mine, theirs = _run(_STATES[1], cand)
    mine, theirs = np.asarray(mine), np.asarray(theirs)
    return int((mine > theirs).sum()), float(mine.mean()), used, skipped


# --------------------------------------------------------------------------
# The calculated allocation, and the leader's schedule to hang it on
# --------------------------------------------------------------------------
# Herd from drain / yield-per-season, exactly as allocation_calculator.py derives it.
DRAIN = C.DRAIN_UNITS


def herd_target(animal):
    a = R.ANIMALS[animal]
    events = max(0, (R.SEASON_DAYS - a["first_yield_day"]) // max(a["interval"], 1))
    units = events * a["max_held"]
    return int(np.ceil(DRAIN[a["product"]] / max(units, 1)))


def tiles_target(crop):
    from kagg.economics import production as P
    y = max(P.TILE_YIELD_FERTILIZED[crop], P.TILE_YIELD_PER_SEASON[crop])
    return int(np.ceil(DRAIN[crop] / max(y, 1e-9)))


COWS, SHEEP = herd_target("COW"), herd_target("SHEEP")
STRAW, MELON = tiles_target("STRAWBERRY"), tiles_target("MELON")
print(f"calculated target: {COWS} cows, {SHEEP} sheep, {STRAW} strawberry tiles, {MELON} melon tiles")
print(f"leader runs:       8 cows, 6 sheep, 41 strawberry tiles, 20 melon tiles\n")

# The leader's schedule, used as given. Wheat and melon open in NW for day-3 cash; parcels follow on
# days 7 and 10; strawberry goes onto the new ground as it arrives.
PLAN = []
PLAN.append(("grow", "MELON", "narrow", 0, 0))            # day-0 cash, NW, no land
PLAN.append(("grow", "WHEAT", "narrow", 0, 0))            # the only crop paying by day 3
n_cow_chains = int(np.ceil(COWS / 4))
for i in range(n_cow_chains):
    PLAN.append(("ranch", "COW", "group4", 4 + i, 0))     # herd from day 4, NW ground
n_sheep_chains = int(np.ceil(SHEEP / 4))
for i in range(n_sheep_chains):
    PLAN.append(("ranch", "SHEEP", "group4", 5 + i, 0))
n_straw = int(np.ceil(STRAW / 8))
for i in range(n_straw):
    PLAN.append(("grow", "STRAWBERRY", "wide", 8 + i, 7))  # after the day-7 parcel
print(f"the plan needs {len(PLAN)} chains: "
      f"{sum(1 for p in PLAN if p[0]=='ranch')} ranch + {sum(1 for p in PLAN if p[0]=='grow')} grow\n")


def build(n_slots):
    """Write as much of the plan as `n_slots` holds, nearest-and-cheapest ground first."""
    g = np.zeros((n_slots, len(C.GENES)), dtype=np.int64)
    used_tiles, notes = set(), []

    def pick(pool, want_land_free):
        for b in pool:
            tiles = set(b if isinstance(b[0], tuple) else [b])
            if tiles & used_tiles:
                continue
            if want_land_free and C.land_cost(list(tiles)[0]) > 0:
                continue
            return b
        return None

    narrow = [b for b in C.NARROW_BLOCKS]
    wide = [b for b in C.WIDE_BLOCKS]
    groups4 = [gr for gr in C.RANCH_GROUPS if len(gr) >= 3]

    for slot, (kind, what, shape, start, land_day) in enumerate(PLAN[:n_slots]):
        pool = {"narrow": narrow, "wide": wide, "group4": groups4}[shape]
        # Land-free ground for anything starting before day 7; bought ground after.
        b = pick(pool, want_land_free=(land_day == 0)) or pick(pool, want_land_free=False)
        if b is None:
            notes.append(f"slot {slot}: no free {shape} block left")
            continue
        tiles = list(b) if isinstance(b[0], tuple) else [b]
        used_tiles.update(tiles)
        if kind == "ranch":
            block_i = next(i for i, gr in enumerate(C.RANCH_GROUPS) if gr == b)
            what_i = R.ANIMAL_NAMES.index(what)
        else:
            block_i = C.BLOCKS.index(b)
            what_i = R.CROPS.index(what)
        row = [C.KINDS.index(kind), what_i, block_i,
               C.START_DAY_CHOICES.index(min(start, R.SEASON_DAYS - 2)),
               C.LAND_DAY_CHOICES.index(land_day)]
        g[slot] = row + [0] * (len(C.GENES) - len(row))
    return g.reshape(-1), notes


print("=" * 96)
print("THE CALCULATED GENOME, SCORED DIRECTLY -- no beam")
print("=" * 96)
out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
print(f"{'slots':>6} {'wins':>8} {'money':>11} {'skipped':>8} {'hands':>6} {'hire $/season':>14}")
from kagg.sim.farm import HIRE_COST
hc = np.asarray(HIRE_COST)
best = None
for n_slots in [int(x) for x in args.slots.split(",")]:
    genome, notes = build(n_slots)
    try:
        w, m, used, skipped = score(genome, n_slots)
    except Exception as exc:                     # noqa: BLE001 - report and keep sweeping
        print(f"{n_slots:>6}  FAILED: {type(exc).__name__}: {exc}")
        continue
    script, _u, _s = C.decode(genome, n_slots)
    hands = int(np.asarray(script.hire).max())
    hire = int(hc[:hands].sum()) * R.SEASON_DAYS if hands else 0
    print(f"{n_slots:>6} {w:>3}/{N_PAIRS:<4} {m:>11,.0f} {skipped:>8} {hands:>6} {hire:>14,}")
    for note in notes:
        print(f"         {note}")
    if best is None or (w, m) > (best[0], best[1]):
        best = (w, m, genome, n_slots)

if best:
    w, m, genome, n_slots = best
    np.savez_compressed(out / "best_beam_genome.npz", genome=genome, wins=w, money=m, slots=n_slots)
    print(f"\nbest calculated genome: {n_slots} slots, {w}/{N_PAIRS} wins, ${m:,.0f}")
    _script, used, skipped = C.decode(genome, n_slots)
    for u in used:
        print("   ", u)
    print(f"\nwrote {out / 'best_beam_genome.npz'} ({skipped} chains skipped)")
    print("\nCompare against the beam on the same 16 games. If this wins, the search was finding what")
    print("arithmetic already knew. If it loses, the schedule is doing more work than the mix.")
