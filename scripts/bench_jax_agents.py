"""Round-robin the JAX scripted agents against each other, both seatings, on the real simulator.

**Why this and not `bench_agents.py`.** That one benchmarks the numpy agents through
`kaggle_environments`, which is what the leaderboard runs but is far too slow for a sweep. These are
the agents that actually populate the PPO rollout, they run inside `jax.lax.scan`, and until now the
only way to see one play was against a trained checkpoint. Their banks were each measured once, at
different times, against different opponents, and quoted from their own docstrings ever since --
`jax_heuristic` $23,783, `jax_rancher` $12,078, `jax_carrot` $3,410. Nobody has played them against
each other.

**Both seatings.** `_process_market` quotes both players against the same inventory but commits in
seat order, so seat 0 has an edge on contested trades (`eval_policy.py`'s docstring). Every pair is
played twice with the seats exchanged.

**Weeds ON, and this is not optional.** `J.step`'s `weed_chance` defaults to 0, and with it off
every game in a batch produces the *identical* final bank -- 8 games, 8 identical values, unchanged
across seeds, because the only per-game variation left is the shop schedule and it does not move a
melon farmer's revenue. A benchmark run that way reports "median over 48 games" while holding one
sample. At `weed_chance=0.02` the same 8 games span $16,056 to $33,690, a 2x spread, which is the
distribution any agent comparison has to resolve against. `CLAUDE.md`: *"Seed variance is ~15%.
Always quote the seed range."*

**`reset_with_shops`, never plain `reset`.** `jax_sim.py:371-377` records that a frozen town buys 140
wheat a season against the reference's 698, holding end-of-season wheat at $37 instead of $51 and
milk at $263 instead of $340. A benchmark on a frozen town measures a different game.

    python3 scripts/bench_jax_agents.py --games 32
"""

import argparse
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jax                                    # noqa: E402
import jax.numpy as jnp                       # noqa: E402
import numpy as np                            # noqa: E402

from kagg.rl import jax_carrot as CARROT      # noqa: E402
from kagg.rl import jax_frontier as FRONT     # noqa: E402
from kagg.rl import jax_heuristic as HEUR     # noqa: E402
from kagg.rl import jax_homestead as HOME     # noqa: E402
from kagg.rl import jax_rancher as RANCH      # noqa: E402
from kagg.sim import jax_sim as J             # noqa: E402

EPISODE_TURNS = 719          # matches `train_jax_rl.py:81` and `play_checkpoint.py:60`

AGENTS = {
    "frontier": FRONT.actions,
    "homestead": HOME.actions,
    "farm": HEUR.actions,
    "ranch": RANCH.actions,
    "carrot": CARROT.actions,
    "idle": None,            # all-zeros IS the do-nothing agent (`train_jax_rl.py:352`)
}


def _zeros_like_actions(a):
    return jax.tree_util.tree_map(lambda x: jnp.zeros_like(x), a)


def play(fn_a, fn_b, games, seed, weeds=0.02):
    """Seat 0 plays `fn_a`, seat 1 plays `fn_b`. Returns final `[games, 2]` money."""
    state = J.reset_with_shops(games, seed=seed)

    def turn(st, _):
        # Each agent returns actions for BOTH seats; take each one's own seat from its own plan.
        a = fn_a(st) if fn_a is not None else None
        b = fn_b(st) if fn_b is not None else None
        ref = a if a is not None else b
        a = _zeros_like_actions(ref) if a is None else a
        b = _zeros_like_actions(ref) if b is None else b
        seat = jnp.arange(2)[None, :]
        take_a = (seat == 0)

        def pick(x, y):
            m = take_a.reshape((1, 2) + (1,) * (x.ndim - 2))
            return jnp.where(m, x, y)

        merged = jax.tree_util.tree_map(pick, a, b)
        return J.step(st, merged, weed_chance=weeds), None

    state, _ = jax.lax.scan(turn, state, None, length=EPISODE_TURNS)
    return np.asarray(jax.device_get(state.farm.money))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=32)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--agents", default=",".join(AGENTS))
    ap.add_argument("--seeds", type=int, default=3, help="independent boards per pair")
    ap.add_argument("--weeds", type=float, default=0.02,
                    help="weed spawn chance. 0 makes every game in a batch identical -- see the "
                         "module docstring. Only set it to 0 to reproduce a deterministic trace.")
    args = ap.parse_args()

    names = [n.strip() for n in args.agents.split(",") if n.strip() in AGENTS]
    print(f"{len(names)} agents, {args.games} games x 2 seatings per pair, "
          f"{EPISODE_TURNS}-turn episodes, real shop schedule\n")

    score = {n: 0.0 for n in names}
    played = {n: 0 for n in names}
    banks = {n: [] for n in names}

    hdr = f"{'pair':<24} {'A wins':>7} {'draws':>6} {'A $ med':>10} {'B $ med':>10}"
    print(hdr)
    print("-" * len(hdr))
    for a, b in itertools.combinations(names, 2):
        am, bm = [], []
        for sd in range(args.seeds):
            m0 = play(AGENTS[a], AGENTS[b], args.games, sd, args.weeds)     # a in seat 0
            m1 = play(AGENTS[b], AGENTS[a], args.games, sd, args.weeds)     # seats swapped
            am += [m0[:, 0], m1[:, 1]]
            bm += [m0[:, 1], m1[:, 0]]
        a_money = np.concatenate(am)
        b_money = np.concatenate(bm)
        wins = float((a_money > b_money).mean())
        draws = float((a_money == b_money).mean())
        n = len(a_money)
        score[a] += (wins + 0.5 * draws) * n
        score[b] += (1.0 - wins - 0.5 * draws) * n
        played[a] += n
        played[b] += n
        banks[a].append(np.median(a_money))
        banks[b].append(np.median(b_money))
        print(f"{a + ' vs ' + b:<24} {wins:>7.3f} {draws:>6.3f} "
              f"{np.median(a_money):>10,.0f} {np.median(b_money):>10,.0f}")

    print(f"\n{'agent':<12} {'score':>7} {'median $ across pairs':>24}")
    print("-" * 46)
    for n in sorted(names, key=lambda x: -(score[x] / max(played[x], 1))):
        print(f"{n:<12} {score[n] / max(played[n], 1):>7.3f} "
              f"{np.median(banks[n]) if banks[n] else float('nan'):>24,.0f}")


if __name__ == "__main__":
    main()