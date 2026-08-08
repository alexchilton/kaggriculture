# Prompt for Kimi: is direct trajectory optimisation the right frame?

2026-08-04.
Written to be pasted verbatim into an external model, so it is self-contained and assumes no knowledge of this repo.
The point is to get the *frame* challenged, not the implementation tuned — the last time an external read redirected this project it was because it questioned the frame.

---

I'm competing in a Kaggle simulation competition: a 2-player farming game, 30 in-game days × 24 turns = 720 turns, fully deterministic given a seed, scored by an Elo-style ladder so margin doesn't count — only win/loss.

**Evidence that reframed my approach.**
I downloaded replay JSONs from the current #1 and several other top players and diffed their action sequences across 5 fresh episodes, in both seats, against 5 different opponents.
Their per-turn actions are **byte-identical** across episodes: market orders identical in 6/10 pairs and 99.9% in the other 4, unit actions 96–99.6% identical.
The few divergent days cluster on the same days across all pairs, which points at an environment random event (weeds) rather than at reacting to the opponent.
Conclusion: the top agents are not policies. They submit a **fixed open-loop 720-turn script**.
I also replayed one leader's exact recorded script through my own simulator and got $144,743 against their recorded $145,018 — 0.2% — so my offline simulator is trustworthy.

**So I abandoned RL** (PPO over 720 steps, which had stalled) and switched to **direct search over the action sequence itself**.
The current implementation:

- Genome = the full action array for 719 turns: per-unit op (18 ops) × 24 unit slots, plus 9 sell quantities, 5 seed buys, 9 product buys, 3 animal buys, a hire count and a buy-land count. Order 10^5 discrete variables.
- Seed = my own heuristic agent's recorded trajectory ($23.8k final bank).
- Search = (1+λ) hill-climb: 192 candidates per iteration, 8 random single-slot edits each, evaluated exactly (weeds off, so one perturbation is an exact finite difference, not a noisy gradient estimate).
- Selection = wins across a fixed set of 4 recorded opponent scripts, money only as a tie-break.
- **Neutral drift allowed**: accept equal-scoring candidates so the search can cross plateaus, while tracking best-ever separately. Reason: `BUILD_PASTURE` earns nothing by itself — it pays back only after an animal is bought, carried to a pen, placed and fed — so every prefix of that chain scores neutral, and a strict hill-climber rejects step one forever. About 35% of leader revenue is livestock and my seed has zero of it.
- Throughput: ~10s per iteration of 192 candidates on a laptop (JAX, `lax.scan` over turns). So ~3,700 iterations overnight.

**My questions:**

1. Is a (1+λ) hill-climber with neutral drift the right search for this, or am I choosing badly?
   The obvious alternatives are CEM over a lower-dimensional parameterisation (tried; it caps the ceiling by construction), simulated annealing, a genetic algorithm with crossover, or something that exploits the sequential structure — optimising day-by-day forward with lookahead, or beam search over days.
   Note the objective is exactly deterministic and cheap, and one candidate costs one full 719-turn rollout.

2. Random single-slot edits seem far too weak for chains.
   Building the animal economy requires a *coordinated* set of edits across many turns: buy on day 5, build a pasture, walk a unit to the shed, pick up, place, then feed daily for 25 days.
   Random per-slot mutation has to find that by chance.
   What's the right move — hand-written macro-mutations that insert a whole chain at once, learning a mutation distribution, a hierarchical/coarse-to-fine parameterisation, or something else?

3. Is there a credit-assignment trick I'm leaving on the table?
   Because the sim is deterministic and I can replay any prefix, I can compute the exact value of any single edit rather than sampling it.
   Is there a known method that exploits exact, cheap, replayable finite differences over a long action sequence?
   This feels adjacent to what a compiler superoptimiser or a stochastic program-synthesis search does.

4. Selection is on wins against only 4 fixed opponents, which is a very coarse signal (a 0–4 integer) and risks overfitting to those 4.
   Money as a tie-break may be actively misleading, since the ladder is Elo and a $43k win scores the same as a $4k win.
   How should I define the objective?

5. **The one I most want challenged: is the whole open-loop premise a trap?**
   The top agents' scripts are fixed, but they were presumably *tuned* against the live ladder over weeks with a human in the loop.
   If I optimise a fixed script against my own recorded opponents offline, am I building something that wins my private tournament and loses the real one?
   What would you check to find out?
