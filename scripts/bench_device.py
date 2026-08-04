"""Does a GPU actually help this simulator, and at what batch size?

The workload is a `lax.scan` over 719 sequential turns. A GPU cannot parallelise across turns -- only
across the batch -- so at small batch each step is a tiny kernel and the scan is launch-latency bound,
which is exactly the shape where a fast CPU ties or wins. The question is therefore not "is the GPU
faster" but "where do the two curves cross".

That distinction matters because of how the cost scales. CPU throughput is roughly linear in batch:
double the population, double the wall clock. A GPU is flat until it saturates. So if the crossover is
below the batch sizes we care about, the win is not "the same search, faster" -- it is a *larger
population for the same wall clock*, which is a different search. `optimise_script.py` currently runs
batch 96; if batch 1024 costs the same on GPU, that is the finding.

Reports seasons/sec, where one season is a full 719-turn two-seat game. JIT compilation is excluded by
a warm-up call at every batch size, since compile time is paid once per shape and the searches run for
hours.

    PYTHONPATH=. python3 -u scripts/bench_device.py --batches 96,256,512,1024,2048
"""

import argparse
import pathlib
import time

import jax
import jax.numpy as jnp
import numpy as np
from jax import lax

from kagg.search import boards
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

ap = argparse.ArgumentParser()
ap.add_argument("--batches", default="96,256,512,1024,2048",
                help="candidate counts to time, comma separated")
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--sim-seed", type=int, default=0)
ap.add_argument("--repeats", type=int, default=3, help="timed runs per batch size; the best is kept")
args = ap.parse_args()

print(f"backend: {jax.default_backend()}")
print(f"devices: {jax.devices()}\n")

OPPONENTS = []
for name in args.opponents.split(","):
    p = pathlib.Path("data/seed_scripts") / f"{name.strip()}_seed{args.sim_seed}.npz"
    if not p.exists():
        raise SystemExit(f"missing opponent script {p}")
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
    return state.farm.money[:, 0].reshape(N_PAIRS, b)


# The tape contents are irrelevant to timing -- every candidate runs all 719 turns regardless of what
# the ops are, because `lax.scan` has no early exit. Zeros keep the harness honest about what is being
# measured: the simulator, not the decoder.
def fake_batch(b):
    return {f: jnp.zeros((b, T) + OPP_XS[f].shape[2:], dtype=OPP_XS[f].dtype) for f in FIELDS}


print(f"{N_PAIRS} games per candidate, {T} turns per game, "
      f"best of {args.repeats} timed runs\n")
print(f"{'batch':>7} {'seasons':>9} {'compile':>9} {'run':>9} {'seasons/s':>11} {'us/season':>11}")

rows = []
for b in [int(x) for x in args.batches.split(",")]:
    unlocks = boards.unlock_array(N_OPP, args.boards, b, seed=args.sim_seed)
    state = J.reset(len(unlocks), unlock_schedule=unlocks, seed=args.sim_seed)
    cand = fake_batch(b)

    t0 = time.time()
    out = _run(state, cand)
    out.block_until_ready()                     # compile + one execution
    compile_s = time.time() - t0

    best = float("inf")
    for _ in range(args.repeats):
        t0 = time.time()
        out = _run(state, cand)
        out.block_until_ready()                 # JAX is async; without this we would time the dispatch
        best = min(best, time.time() - t0)

    seasons = b * N_PAIRS
    print(f"{b:>7} {seasons:>9,} {compile_s:>8.1f}s {best:>8.2f}s "
          f"{seasons / best:>11,.0f} {best / seasons * 1e6:>11.1f}")
    rows.append((b, seasons / best))

if len(rows) > 1:
    first, last = rows[0], rows[-1]
    print(f"\nbatch {first[0]} -> {last[0]}: {last[1] / first[1]:.2f}x throughput per season. "
          f"A CPU sits near 1.0x here (cost is linear in batch); well above 1.0x means the device "
          f"was idle at the small batch and the search should run a bigger population.")
