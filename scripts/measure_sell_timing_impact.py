"""Kimi's Test 1: does shifting our sell days change our bank? Thin market or thick?

The framing being tested is that two independent boards sharing one market make this a market game with
a farming backend, so the edge is price discovery -- front-running the opponent's dump, withholding,
counter-buying. That is a real class of game, and it hinges entirely on **market impact**. Three regimes:

    A. thin, high impact    -- selling 9 wheat crashes the price for both. Timing is everything.
    B. thick, low impact    -- a trade barely moves price. The boards are effectively independent.
    C. asymmetric           -- one side's trades move price more, so the leader can starve the other.

The decisive experiment is cheap because we have exact dynamics: take a fixed production plan, shift
*only* its sell days, and measure. Nothing about the farm changes, so any difference in bank is pure
market impact.

Two shifts are measured separately, because they answer different questions:

- **uniform shift** of every sell by k days: tests the season's price *ramp*. The town's eight shops
  unlock across days 3-24, so demand grows all season and a late sale should be worth more.
- **per-product shift** of one product at a time: tests impact against *this opponent's* schedule,
  which is what front-running would exploit.

Prior from `measure_true_drain.py`, which already looked at a real tape: every product CLEARED (the
shops ate everything both players offered) and prices ROSE all season -- wheat 25 -> 54, milk 160 -> 244,
strawberry 120 -> 174. Only MELON glutted, +100 inventory with its price halving 250 -> 150. That is
regime B for seven products and regime A for melon alone, and it predicts the uniform late shift is
worth far more than any front-running.
"""

import argparse

import numpy as np
import jax
import jax.numpy as jnp
from jax import lax

from kagg.search import chains as C
from kagg.search import routines as R
from kagg.sim import jax_sim as J
from kagg.search import boards

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")

ap = argparse.ArgumentParser()
ap.add_argument("--genome", default="data/chain_search_v2/best_beam_genome.npz")
ap.add_argument("--slots", type=int, default=8)
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot")
ap.add_argument("--boards", type=int, default=4)
ap.add_argument("--seed", type=int, default=0)
args = ap.parse_args()

OPPONENTS = []
for name in args.opponents.split(","):
    b = np.load(f"data/seed_scripts/{name.strip()}_seed{args.seed}.npz")
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


unlocks = boards.unlock_array(N_OPP, args.boards, 1, seed=args.seed)
STATE0 = J.reset(len(unlocks), unlock_schedule=unlocks, seed=args.seed)

genome = np.asarray(np.load(args.genome)["genome"], dtype=np.int64)
script, used, skipped = C.decode(genome, args.slots)
BASE = {f: np.asarray(script.arrays()[f])[:T] for f in FIELDS}


def evaluate(sell_array):
    arrs = dict(BASE)
    arrs["sell"] = sell_array[:T]
    cand = {f: jnp.asarray(np.stack([arrs[f]])) for f in FIELDS}
    mine, theirs = _run(STATE0, cand)
    mine, theirs = np.asarray(mine), np.asarray(theirs)
    return int((mine > theirs).sum()), float(mine.mean()), float(theirs.mean())


def shifted(sell, days, products=None):
    """Move sell orders `days` later (positive) or earlier (negative), in whole days."""
    out = np.zeros_like(sell)
    k = days * R.TURNS_PER_DAY
    cols = range(sell.shape[1]) if products is None else products
    for p in range(sell.shape[1]):
        if p in cols:
            if k >= 0:
                out[k:, p] = sell[:sell.shape[0] - k, p] if k else sell[:, p]
            else:
                out[:k, p] = sell[-k:, p]
        else:
            out[:, p] = sell[:, p]
    return out


base_w, base_me, base_them = evaluate(BASE["sell"])
print("=" * 92)
print(f"BASELINE  {base_w}/{N_PAIRS} wins   us ${base_me:,.0f}   them ${base_them:,.0f}")
print(f"          {len(used)} chains, {skipped} skipped, from {args.genome}")
print("=" * 92)

print("\nUNIFORM SHIFT of every sell -- tests the season's price ramp")
print(f"{'shift':>7} {'wins':>7} {'our bank':>12} {'vs base':>10} {'their bank':>12}")
for days in (-3, -2, -1, 0, +1, +2, +3):
    w, me, them = evaluate(shifted(BASE["sell"], days))
    print(f"{days:>+7} {w:>4}/{N_PAIRS} {me:>12,.0f} {me - base_me:>+10,.0f} {them:>12,.0f}")

print("\nPER-PRODUCT SHIFT -- tests front-running this opponent, one product at a time")
print(f"{'product':>12} {'shift':>6} {'wins':>7} {'our bank':>12} {'vs base':>10}")
sold = [p for p in range(BASE["sell"].shape[1]) if BASE["sell"][:, p].sum() > 0]
for p in sold:
    for days in (-2, -1, +1, +2):
        w, me, _t = evaluate(shifted(BASE["sell"], days, products={p}))
        flag = "  <-- material" if abs(me - base_me) > 0.02 * base_me else ""
        print(f"{R.PRODUCTS[p]:>12} {days:>+6} {w:>4}/{N_PAIRS} {me:>12,.0f} "
              f"{me - base_me:>+10,.0f}{flag}")

print()
print("=" * 92)
print("VERDICT: >2% on any single shift means thin market and timing is exploitable.")
print("Near-zero means thick, the boards are effectively independent, and the edge is production.")