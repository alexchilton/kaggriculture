"""Cross-entropy method over farm plans.

Why CEM rather than beam search or a GA
---------------------------------------

**Beam search was rejected on the shape of the problem.** A beam over per-day decisions needs a
per-day score to prune on, and this game has none worth having: the whole point of the measured
economics is that money banked early is money *not* invested, so a day-12 leader is routinely a
day-30 loser. Anything that prunes on partial return prunes exactly the strategies -- late-maturing
crops, deferred selling, a slow capital ramp -- that the economics say are the prize. Pruning on the
true objective would need a rollout per node, at which point it is a population method with worse
sample efficiency.

**CEM rather than a GA** because the genome is a set of independent categorical choices with no
meaningful locality between genes, so crossover has no structure to exploit, while a factored
categorical distribution has one very useful property: the fitted distribution is itself the
answer. After the search, ``p(tile 37 = MELON)`` is a direct statement about that tile, with the
strength of the evidence attached. That is what makes the result readable rather than merely a
winning genome, and readable is what the brief actually asks for.

The elite update is the standard one, smoothed and floored:

    p <- (1 - alpha) * p + alpha * (elite frequency),  then clip to `floor` and renormalise

The floor matters more here than usual. With 277 genes and ~40 elites, a category can vanish from
the elite set by chance in one generation and never come back; a 1% floor keeps every option alive
for the whole run.

Two methodological guards, both taken from `docs/experiment_log.md` section 3, where the heuristic
tuner learned them expensively:

- **Unlock schedules are resampled every generation.** A fixed set of schedules is a fixed set of
  seeds, and a fixed set of seeds reported +40% where held-out seeds said +12.8%.
- **The reported winner is re-scored on a fresh draw** before it is believed, because taking the
  best of N noisy estimates biases every comparison upward.
"""

import numpy as np

from kagg.search import plan as P
from kagg.search import rollout


def _rank(win_rate, delta):
    """Indices worst-to-best. Win rate first, money delta only to break its many ties.

    Selecting on money is the documented way to pick the wrong agent in this project: `hold_days`
    14 banked the most and won the least. Delta appears here purely because a handful of games
    gives a very coarse win rate, and something has to order the plans that all lose 0-6.
    """
    return np.lexsort((delta, win_rate))


class Result:
    def __init__(self):
        self.history = []
        self.best_genome = None
        self.best_score = (-1.0, -np.inf)
        self.probs = None


def search(opposition, generations=25, pop=192, elite_frac=0.2, alpha=0.55, floor=0.01,
           schedules=2, weed_chance=0.005, seed=0, log=print):
    """Run CEM against a fixed set of opponent plans. `opposition` is ``[M, N_GENES]``."""
    rng = np.random.default_rng(seed)
    probs = P.uniform_probs()
    opponents = P.decode(opposition)
    n_elite = max(4, int(pop * elite_frac))
    result = Result()

    for gen in range(generations):
        genomes = P.sample(probs, pop, rng)
        if result.best_genome is not None:
            genomes[0] = result.best_genome          # elitism, so a good plan is never lost

        draw = [rollout.sample_unlock_schedule(rng) for _ in range(schedules)]
        win, delta = rollout.evaluate(
            P.decode(genomes), opponents, draw,
            weed_chance=weed_chance, seed=int(rng.integers(1 << 30)),
        )

        order = _rank(win, delta)
        elite = genomes[order[-n_elite:]]
        top = order[-1]

        counts = np.zeros_like(probs)
        for gene in range(P.N_GENES):
            counts[gene, : P.N_CATS[gene]] = np.bincount(
                elite[:, gene], minlength=int(P.N_CATS[gene])
            )[: P.N_CATS[gene]]
        empirical = counts / counts.sum(axis=1, keepdims=True)
        probs = (1 - alpha) * probs + alpha * empirical
        probs = np.where(probs > 0, np.maximum(probs, floor), 0.0)
        probs /= probs.sum(axis=1, keepdims=True)

        score = (float(win[top]), float(delta[top]))
        if score > result.best_score:
            result.best_score = score
            result.best_genome = genomes[top].copy()
        result.history.append({
            "generation": gen,
            "best_win": float(win[top]),
            "best_delta": float(delta[top]),
            "mean_win": float(win.mean()),
            "elite_win": float(win[order[-n_elite:]].mean()),
        })
        log(f"gen {gen:3d} | best win {win[top]:.2f} delta {delta[top]:+9.0f} "
            f"| elite win {win[order[-n_elite:]].mean():.2f} | pop mean {win.mean():.2f}")

    result.probs = probs
    return result


def confirm(genomes, opposition, schedules=6, weed_chance=0.005, seed=99):
    """Re-score candidates on a fresh draw of unlock schedules -- the winner's-curse check."""
    rng = np.random.default_rng(seed)
    draw = [rollout.sample_unlock_schedule(rng) for _ in range(schedules)]
    return rollout.evaluate(
        P.decode(genomes), P.decode(opposition), draw, weed_chance=weed_chance, seed=seed
    )


def modal_genome(probs):
    """The most likely plan under the fitted distribution."""
    return probs.argmax(axis=1)
