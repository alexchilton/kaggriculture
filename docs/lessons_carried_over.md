# Lessons carried over from Orbit Wars

Source material lives at
`~/DataspellProjects/orbit_wars/orbit_wars_jax/docs/` — in particular
`rl_postmortem_and_fix_plan.md` and the five competitor write-ups
(`rl_lessons_isaiah_pressman.md`, `rl_lessons_simjeg.md`,
`rl_lessons_billy_bradley_ender.md`, `rl_lessons_felix_neumann.md`,
`rl_lessons_lin_myat_ko.md`).

Read the post-mortem in full before any serious RL work.
This file is the distillation, not a replacement.

Note: the oldest memory file credits Lin Myat Ko as 1st place.
The corrected standings are Isaiah Pressman 1st, simjeg 2nd, Felix Neumann 3rd,
Billy Bradley 8th.

## The short version of what went wrong last time

RL was never impossible — 1st and 2nd place were existence proofs, and 2nd place did it with a
4.3M model barely larger than ours.
The collapses were **structural**: a wrong action parameterization and the wrong *kind* of prior.

Concretely:

- The action was one categorical over ~480 candidates plus NOOP, where NOOP was ~95% of labels.
  The loss was minimised by always predicting NOOP.
- The candidate menu was filtered to the top 192 by heuristic *quality* score, which pinned the
  ceiling to the heuristic's taste and censored the interesting expert moves out of the IL labels.
- Dense per-step shaping rewards optimised a proxy, producing ~50% against random and 0% against
  strong heuristics.
- No-op became a genuine self-play equilibrium that nothing in the setup punished.
- Total experience was **~500 complete games**. The winners ran 2-50 million.
  "Never beat random" was the *expected* outcome, not a failure mode.

## What transfers directly

**Process, mostly. These are the expensive ones.**

1. **Measure before theorising.**
   Log explained variance and return mean/std every update, from the first run.
   `ret=0.00±0.00` means the reward is not reaching the algorithm — stop everything.
   Half the Orbit Wars diagnoses were guesses because nothing was tracked.

2. **Read the logs before building a narrative.**
   The tidy single-cause story in the post-mortem was constructed without reading the logs and was
   mostly wrong. Real RL projects die of a scatter of mundane failures — plumbing bugs, missing
   normalization, KL death, entropy collapse — not one elegant villain.

3. **When every config fails the same way, the problem is what they share: the pipeline.**
   Orbit Wars treated a pipeline-bug signature as a hyperparameter signature and kept restarting
   into the same broken plumbing.

4. **Entropy going down is learning. Entropy crashing to ~0 while win rate is still random is a bug.**
   Kill losers fast, but run winners *long*. Felix killed 3x more runs than he kept and ran the
   survivors 8.4B steps. Both halves are required; Orbit Wars only ever did the first.

5. **One delta at a time, ablation-driven.**
   A stupider architecture that trains beats a smarter one that does not.

6. **Commit to a kill criterion up front**, before the sunk cost accumulates.
   See `CLAUDE.md` for this project's three.

7. **Validate priors with the cheap signal** — supervised ablation and a fast local arena —
   not with full RL runs. Orbit Wars used the most expensive possible signal on the least compute,
   which is why every ablation was inconclusive and every diagnosis a guess.

8. **Near-total ban on "it can't be done."**
   The honest form is "our current setup isn't learning it, and I don't yet know whether that's the
   frame or the game" — then go measure explained variance and find out.

## What does NOT transfer

Do not cargo-cult these. They were correct answers to a different problem.
The reasoning is in `rl_feasibility.md`.

- **"Masking backfires."** That was about masking no-op to force action. Legality masking is
  explicitly safe.
- **"Self-play is essential."** The opponent coupling here is weak — market prices only.
- **"Collapse the action space to all-in."** That fixed a 480-way categorical.
  This action space is already 18 ops.

> **A correction, because this file used to argue the opposite.**
> It said "never shape the reward" does not transfer, on the grounds that a per-step bank delta is
> an exact decomposition of the true objective rather than a proxy. The arithmetic is right and the
> conclusion was overruled: **the ladder is Elo, so bank is itself a proxy for the score.**
> The reward is terminal — win 1, loss 0, gamma 1.0 — for every policy in this project.
> The Orbit Wars ban does transfer, for a reason Orbit Wars did not have.

## The prior taxonomy — the crux, and it still applies

A prior either **shapes the learning problem** or **is the policy**.

- **Shapes the problem (safe):** constrains inputs or action space, learner chooses within it.
  If slightly wrong, the learner routes around it.
- **Is the policy (brittle):** the rule makes the decision. Every imperfection is a permanent ceiling,
  because there is no learner underneath to compensate.

The test: **safe if it only removes moves that are never optimal (a legality fact);
dangerous if it removes moves based on a guess about which move is good (a quality judgment).**

You can stack many safe priors. The problem is never the count, it is the *kind*, or an unvalidated one.
Assertion is not validation — simjeg ablated every prior with cheap IL before touching RL.

**Applied here:** legality masks are safe and encouraged.
A "sensible actions only" filter would be the Orbit Wars mistake repeating itself. Do not build one.

## The right use of a heuristic agent

This is the lesson that cost the most and is easiest to get wrong again.

In Orbit Wars the hand-built v131 heuristic became the policy, then became a candidate filter.
Both capped the ceiling.
The post-mortem's verdict:

> Our whole heuristic effort was the wrong tool for BEING the policy but the perfect tool for
> TEACHING the policy.

**In this project the heuristic agent is, from day one and explicitly:**

- a leaderboard placeholder from week 1,
- the sparring and evaluation opponent,
- the IL bootstrap and offline-search seed.

It is **never** the final policy and **never** a filter on what the learner may consider.

## How to drive the advisor

Verbatim from the post-mortem, because it is about working with Claude and applies to this project too.

> Claude is a better critic than collaborator: fast at finding flaws when given a finished thing
> plus an answer key; prone to helping you walk confidently in a plausible wrong direction
> mid-build unless forced to challenge the frame.

Counters that worked:

- Ask the strategic question explicitly: *"is this collapse telling us the FRAME is wrong? argue that it is."*
- Force the null hypothesis: *"give me three reasons this whole approach is doomed."*
- Demand an existence proof on **day one**: *"has anyone done RL on a game like this, what was their action space?"*
- Commit to a kill criterion up front so the conversation cannot drift into endless tactical tweaks.
- Distrust confident impossibility claims. Make Claude produce the evidence before accepting "can't".

A live example from this project: the first read of Kaggriculture confidently concluded
"RL is the wrong tool, build a planner."
That was overcorrection from the previous competition, and it was overturned by two facts
(`actTimeout`, action-space size) that had not been checked when the claim was made.
Alex pushed back; the claim did not survive contact with the environment source.
**Check the source before forming the opinion.**

## Standing feedback from memory

These are recorded preferences that apply here.

- Never silently change model architecture — ask first.
- Always inspect actual observation data before using field indices. Do not assume the format.
- Test locally before submitting. This competition allows 5 submissions/day.
- `ent_coef`: Orbit Wars used 0.02, which may have been far too high.
  Alex's friend uses 0.0005 for large MultiDiscrete spaces.
- Do not declare things impossible. Check explained variance first.
  Suspect the frame and the parameterization before the model capacity.