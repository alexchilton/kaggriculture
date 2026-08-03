"""Does the credit window explain the stall, and do either of the proposed fixes actually help?

Runs tabular Q-learning on `kagg.rl.toy` in a 2x2: money shaping on/off, reverse curriculum on/off.
Pure numpy, a few seconds per arm on a laptop, no GPU and no JAX.

**What this can and cannot say.** The toy keeps the structure that matters -- terminal binary reward,
a bar equal to what doing nothing achieves, a cost that lands immediately and revenue that lands
`RIPEN + 1` turns later -- and throws away the board, the units, the market and the opponent. So a
fix that fails here will fail on the real game; a fix that works here has cleared a necessary bar and
not a sufficient one. It is a filter, not a proof.

**Why tabular and not PPO.** A tabular learner is the *most* favourable case for long-range credit:
it has no function approximation to interfere and it visits every state exactly. If the credit gap
defeats a tabular learner within a sane episode budget, it certainly defeats PPO with a transformer.
Any arm that fails here fails for a reason that is about the problem, not about the learner.

    python3 scripts/toy_credit_window.py

Writes a table to stdout; tee it to `data/logs/` if you want to keep it.
"""

import argparse
import collections

import numpy as np

from kagg.rl import toy as T

# **A numpy twin of `money_potential.potential`, and why there are two.**
#
# The production one is `jnp`, because it has to run inside the compiled rollout. Calling it from a
# Python step loop would make ~40M jax scalar dispatches for a full sweep -- hours, and it would
# break the point of this script, which is that it runs on a laptop in seconds.
#
# Two implementations of one formula is exactly the thing `adapter.py` warns about ("that creates two
# encoders which must agree forever, and they will not"). The mitigation is the project's standard
# one: `tests/test_toy_potential_parity.py` asserts they agree across the range, so a drift is a red
# test rather than a silently wrong experiment.


def potential_np(money, floor=0.0, scale=100_000.0, k=2.0, cap=1.0):
    # Mirrors `money_potential.potential` exactly, including the 2026-08-03 move of the floor
    # from $3,000 to 0 and the cap at 1.0. `tests/test_toy_potential_parity.py` is what caught
    # the drift when only the jax side was changed -- which is the whole reason it exists.
    return min((max(float(money) - floor, 0.0) / scale) ** k, cap)

MONEY_STEP = 100                       # every price in the toy is a multiple of this
MONEY_LO, MONEY_HI = 0, 8_000
N_MONEY = (MONEY_HI - MONEY_LO) // MONEY_STEP + 1
N_RIPE = T.RIPEN + 2                   # `NO_CROP` (-1) through `RIPEN`, offset by one


def encode(state):
    t, money, ripe = state
    m = int(np.clip((money - MONEY_LO) // MONEY_STEP, 0, N_MONEY - 1))
    return t, m, ripe + 1


def q_table():
    return np.zeros((T.EPISODE + 1, N_MONEY, N_RIPE, T.N_ACTIONS), np.float64)


def run_arm(shaping_coef=0.0, curriculum=False, episodes=60_000, seed=0,
            alpha=0.30, eps0=1.0, eps_final=0.02, mastery=0.90, window=500):
    """One arm. Returns (episodes-to-mastery or None, final win rate, final median bank).

    **The curriculum is a tier that retires on measured mastery**, not on a schedule -- Fable's
    criterion in `docs/fable_review_day0_launch_2026-08-03.md`. A tier starts the episode just before
    a ripening; when the trailing win rate holds above `mastery`, the resume point steps one full
    cycle earlier. Retiring on a fixed schedule instead would advance past rungs the learner had not
    actually cleared, which is how a curriculum silently becomes a harder task with fewer samples.
    """
    rng = np.random.default_rng(seed)
    Q = q_table()
    recent = collections.deque(maxlen=window)
    banks = collections.deque(maxlen=window)
    hit = None
    # How many turns before the end the episode starts. Grows by one cycle per mastered tier until
    # it covers the whole season, at which point the curriculum has retired itself.
    cycle = T.RIPEN + 2
    tier = cycle if curriculum else T.EPISODE

    for ep in range(episodes):
        eps = max(eps_final, eps0 * (1.0 - ep / (0.6 * episodes)))

        if curriculum and tier < T.EPISODE:
            # Resume `tier` turns from the end, with the seed already bought and the crop just about
            # to ripen -- the spend made, the payoff inside reach. `opportunity.resume_turns` picks
            # the equivalent point out of a real rollout.
            start_t = T.EPISODE - tier
            env = T.ToyFarm(start_t=start_t,
                            start_money=T.START_MONEY - T.SEED_COST,
                            start_ripe=0)
        else:
            env = T.ToyFarm()

        s = encode(env.state)
        done = False
        while not done:
            legal = env.legal()
            if rng.random() < eps:
                a = int(rng.choice(np.flatnonzero(legal)))
            else:
                masked = np.where(legal, Q[s][:], -np.inf)
                a = int(np.argmax(masked))

            money_before = env.money
            _, r, done = env.step(a)
            s2 = encode(env.state)

            # Potential-based shaping. At gamma 1.0 this telescopes, so it cannot change the optimal
            # policy -- it only moves credit onto the turn the money actually moved.
            if shaping_coef:
                r = r + shaping_coef * (potential_np(env.money) - potential_np(money_before))

            target = r if done else r + np.max(np.where(env.legal(), Q[s2][:], -np.inf))
            Q[s][a] += alpha * (target - Q[s][a])
            s = s2

        recent.append(float(env.money > T.BAR))
        banks.append(env.money)

        if hit is None and len(recent) == window and np.mean(recent) >= mastery:
            if not curriculum or tier >= T.EPISODE:
                hit = ep
        # Retire a tier once it is mastered, and only then.
        if curriculum and tier < T.EPISODE and len(recent) == window and np.mean(recent) >= mastery:
            tier = min(tier + cycle, T.EPISODE)
            recent.clear()

    return hit, float(np.mean(recent)) if recent else 0.0, float(np.median(banks))


def main():
    ap = argparse.ArgumentParser()
    # ~60 Python-level steps per episode, so a full 4-arm x 3-seed sweep at this budget is a few
    # minutes rather than seconds. Raise it if an arm reads "never" and you want to know whether that
    # is the problem or the budget -- an arm that is merely slow will move, one that is blocked will
    # not.
    ap.add_argument("--episodes", type=int, default=40_000)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--coef", type=float, default=1.0,
                    help="money shaping coefficient for the arms that use it")
    args = ap.parse_args()

    print(f"toy: START ${T.START_MONEY:,}  BAR ${T.BAR:,}  seed ${T.SEED_COST}  "
          f"harvest ${T.HARVEST_GAIN}  ripen {T.RIPEN}  episode {T.EPISODE}")
    print(f"credit gap {T.credit_gap()} turns; optimal bank ${T.optimal_return():,}; "
          f"doing nothing banks ${T.START_MONEY:,} and LOSES")
    print(f"{args.seeds} seeds x {args.episodes:,} episodes per arm\n")

    arms = [("baseline (terminal only)", 0.0, False),
            ("+ money potential", args.coef, False),
            ("+ reverse curriculum", 0.0, True),
            ("+ both", args.coef, True)]

    hdr = f"{'arm':<26} {'solved by':>12} {'win rate':>10} {'median bank':>13}"
    print(hdr); print("-" * len(hdr))
    for name, coef, cur in arms:
        hits, wrs, bks = [], [], []
        for s in range(args.seeds):
            h, wr, bk = run_arm(shaping_coef=coef, curriculum=cur,
                                episodes=args.episodes, seed=s)
            hits.append(h); wrs.append(wr); bks.append(bk)
        solved = [h for h in hits if h is not None]
        when = f"{int(np.median(solved)):,}" if len(solved) > len(hits) // 2 else "never"
        print(f"{name:<26} {when:>12} {np.mean(wrs):>10.3f} {np.median(bks):>12,.0f}")
    print(f"\n'solved by' is the median episode at which the trailing-500 win rate first held "
          f"above 0.90.\n'never' means fewer than half the seeds got there within the budget.")


if __name__ == "__main__":
    main()
