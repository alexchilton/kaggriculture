# Is RL the right tool for Kaggriculture?

**Conclusion: yes. MaskablePPO with an entity transformer is the right inference-time artifact.**

This document records *why*, because the reasoning is non-obvious and a future session with the
Orbit Wars post-mortem in context will otherwise be tempted to relitigate it and reach the wrong answer.

## A correction, recorded honestly

The first read of this competition concluded "this is a deterministic planning problem, RL is the
wrong primary tool, build a planner."
**That was wrong**, and it was wrong for an instructive reason: it was a reaction to the previous
competition rather than an analysis of this one.

Two facts overturned it:

1. **`actTimeout` is 1 second per turn, with 12 seconds of banked overage for the entire
   720-turn episode.**
   Online search is not merely expensive, it is structurally impossible.
   A planner cannot run at inference *at all*.
   A network forward pass (~1-5 ms) fits with room to spare.
2. **The per-unit action space is ~19 discrete ops.**
   Compare Orbit Wars, where the action was one categorical over ~480 candidate edges
   plus fraction buckets — the parameterization that shattered exploration and caused the collapse.

A planner still has a job here, but it is **offline, as a teacher**, not as the policy.

## Why the Orbit Wars failure modes do not transfer

Each row is a specific, named killer from `rl_postmortem_and_fix_plan.md`.

| Orbit Wars killer | Applies here? | Why |
|---|---|---|
| No-op became a stable self-play equilibrium | **No** | PASS does not buy a safe ~0 EV draw. It buys you $3000 while the opponent banks $50k. The *environment* punishes passivity directly, with no need for an aggressive opponent to supply the gradient. This attractor cannot form. |
| Masking was a quality judgment | **No** | Masking here is pure legality: cannot WATER an empty tile, cannot PLANT without a seed, cannot HARVEST at `yield_units == 0`. Concept 1 of the post-mortem explicitly blesses legality masks. The thing that burned us was masking *no-op* to force action, which is a different animal. |
| Reward shaping optimised a proxy | **No** | See the reward section below. Money is not a proxy for the score, it **is** the score. |
| Exploration shattered across ~480 options | **No** | ~19 ops per unit. An entropy bonus actually lands on the action you want to explore. |
| Self-play instability and mutual passivity | **Largely no** | The opponent only touches you through market prices. Training against a fixed opponent is viable, which removes the entire self-play failure surface. |
| Candidate filter capped the ceiling | **Avoidable** | There is no candidate-generation step to poison. Keep it that way — do not introduce a "sensible actions" filter. |

The single genuinely transferable warning is Concept 6, the death spiral: RL not learning →
"help" it with heuristics → the help starves the learner → conclude RL cannot do this.
The defence is the kill criteria in `CLAUDE.md`, committed before any code was written.

## The reward: per-step bank delta, gamma ~= 1.0

**This is not reward shaping, and it must not be "fixed" back to terminal-only.**

The post-mortem's ban is emphatic and correct *for the problem it was written about*:

> KEEP THE REWARD -1/+1. STOP SHAPING IT.

That ban is about **proxy** rewards.
In Orbit Wars, "captured a planet" and "production advantage" were hand-written guesses at what
winning looks like, so optimising them produced Goodhart's law in the flesh — 50% against random,
0% against strong heuristics.

Here the objective is *literally* the sum of money changes.
Final bank minus starting bank equals the sum of per-step bank deltas, exactly, by construction.
Using per-step delta with gamma = 1.0 is therefore **reward decomposition**, not shaping:
it is the same objective with vastly better credit assignment across a 720-step horizon where
crops pay out 48-240 turns after the decision to plant them.

The correct mental model from the post-mortem itself: *"the critic IS the dense reward done right."*
Here we get the exact dense decomposition for free rather than having to learn it.

Practical notes:

- Use gamma slightly below 1 (0.999) only if variance demands it, and log the difference.
- Selling early at a high price versus holding for a better one is handled correctly by the
  decomposition — a later sale simply produces its reward later.
- Evaluate on **win rate**, train on **own money**. They are near-equivalent because the
  opponent coupling is weak, but the leaderboard scores the former.

## Compute: VRAM is not the constraint

The training box is an RTX 3080 Laptop with **16GB VRAM**, which is ample.

| Item | Estimate |
|---|---|
| Entity transformer, d_model 256, 6 layers, ~120 tokens | ~10M params |
| Weights + grads + Adam moments | ~160 MB |
| Activations, bf16, batch 1024, no checkpointing | ~2-4 GB |
| Vectorized sim state, 8192 parallel games | ~16 MB |

Existence proofs from the Orbit Wars field, all in `orbit_wars_jax/docs/`:

- **Billy Bradley ("Ender"), 8th place** — trained a 4-player agent **entirely on a 3080**,
  total spend under $200, on a *harder* problem than this one.
- **simjeg, 2nd place** — 4.3M parameters.
- **Felix Neumann, 3rd place** — 6.2M parameters.
- Only Isaiah Pressman (1st) needed 200M params and 32x B200. That is not our path.

The post-mortem's own compute section states it plainly:
*"Bottleneck is env steps/sec, not VRAM (model is <1GB)."*

## The actual risks

These are different from last time, and these are what to watch.

1. **Env throughput.** 1163 steps/sec of pure Python is the real constraint.
   This is why the design ports the simulator to a vectorized implementation.
   The post-mortem: *"A fast env is the biggest multiplier and is a code problem, not a hardware problem."*
2. **Long-horizon credit assignment.** 720 steps, with planting decisions paying out 2-10 days later.
   Mitigated by the exact reward decomposition above, but watch explained variance.
3. **The structured joint action.** Farmer plus a *variable-length* list of hands plus an ordered
   10-slot market queue. This is the genuinely hard modelling problem, not the per-unit ops.
   See the design doc for the proposed factorization.
4. **Parity drift** between the fast sim and the reference env. A divergent sim makes every
   downstream result fiction. Hence the hard gate in `CLAUDE.md`.
5. **Unmeasured CPU core count and RAM** on the training box.

## What the friend is doing

Alex's friend is independently running **MaskablePPO with a custom entity transformer policy**,
carried over from his own Orbit Wars work.
They compare notes on Discord but compete separately.

That is the same architectural family this design lands on, arrived at independently, which is
weak but real corroboration.
It is *not* a reason to skip the economics model or the arena — the differentiator will be
the quality of the training signal and the routing, not the choice of algorithm.