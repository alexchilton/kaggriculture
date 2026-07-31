# Kaggriculture Agent — Design

Date: 2026-07-31
Status: agreed in brainstorming, not yet implemented

## The governing constraint

`actTimeout` is **1 second per turn**, with **12 seconds of banked overage for the entire
720-turn episode**.
Online search is structurally impossible. A network forward pass (~1-5 ms) fits easily.

Everything expensive happens **offline** and is compiled into either a static schedule or
network weights. This single fact determines the whole architecture.

## Pipeline

```
vectorized sim  ->  economics model  ->  heuristic agent  ->  offline search  ->  IL  ->  MaskablePPO
                                              |                                            |
                                       LB placeholder                              final submission
                                       + sparring partner
```

## Components

Each is independently testable and has one job.

### `kagg/arena/` — built first

Runs N games on fixed seeds, multiprocess, reports **absolute money delta** and win rate.

Built before any agent, because the Orbit Wars post-mortem's harshest finding was that
half the diagnoses were guesses for want of measurement.
This environment is deterministic given a seed, and the score is a continuous low-variance
scalar, so an A/B across 20 seeds takes seconds.
That is an enormous advantage over the previous competition and it should be exploited from hour one.

### `kagg/sim/` — vectorized simulator

Batched re-implementation of `reference/kaggriculture.py`, B games in parallel.

**`kagg/sim/parity.py` is a hard gate.**
It runs identical action sequences through our sim and the reference env and asserts full state
equality at every step, across many seeds and random action sequences.
A divergent sim makes every downstream result fiction.
**Do not train on the fast sim until parity is exact over 1000 random action sequences.**

Design notes:

- **Struct-of-arrays.** Tile state becomes parallel fixed-size arrays over `[B, 100]`:
  `kind, crop, planted_day, watered_today, consecutive_unwatered, yield_units,
  max_lifespan_step, fertilized_until_day, animal, fed_today, cared_today,
  pending_care_bonus, fertilizer_available`.
  No dicts, no `None` — encode as integer enums with a sentinel.
- **Fixed max hands.** Pick a cap, mask the unused slots.
- **Market is a 9-vector** of inventory plus a pure price function.

**Known risk — market settlement.**
The rules process buy and sell orders **one unit at a time, concurrently across both players**,
with the price re-evaluated after each unit.
That is inherently sequential and is the awkward part of any vectorized port.
Two options: a `lax.scan` over a bounded order queue, or a closed-form integral of the price curve
over the quantity.
The scan is safer and should be tried first; the closed form is an optimisation to attempt only
once parity is green.
**Expect this to be where parity breaks.** Write its tests first.

**JAX versus numpy-batched.**
JAX on the 3080 is the intended end state.
If the market scan proves painful, a numpy-batched implementation (vectorized across games,
ordinary Python control flow per step) is a legitimate fallback — it should still be 50-200x the
reference env, which may well be enough.
Decide with a measurement, not a preference.
The parity harness is identical either way, so it is not wasted work.

### `kagg/econ/` — economics model

Pure functions, no simulator: price curves, ROI per crop per tile-day, town drain schedule,
market absorption ceiling.

This is what tells us whether an agent is anywhere near optimal, independently of any agent.
Without it, "the agent made $18k" is uninterpretable.
See `docs/economics_analysis.md` for the day-1 hypotheses this needs to confirm or kill.

### `kagg/agents/heuristic.py` — teacher, not policy

A strong hand-built agent. Explicitly **not** the intended final submission.

Its three jobs: leaderboard placeholder from week 1, sparring and evaluation opponent,
and IL bootstrap.
This is the Orbit Wars lesson applied from the start rather than discovered at autopsy —
see `docs/lessons_carried_over.md`.

**It must never become a filter on what the learner may consider.**

### `kagg/search/` — offline planner

Beam search or CEM over action schedules, running on the vectorized sim.
Orders of magnitude too slow for inference; exists purely to generate near-optimal
trajectories as IL targets.

The deterministic environment is what makes this viable, and it is a far better source of
training data than the scraped replays used in Orbit Wars.

### `kagg/policy/` — entity transformer

Entities: 100 tile tokens + unit tokens (farmer + hands) + market/global tokens ≈ **120 tokens**.

Heads:

- **Per-unit op head** — categorical over ~19 ops, **legality-masked**.
- **Argument heads** — crop selection for PLANT, item selection for PICKUP/PLACE.
- **Market head** — see below.

At d_model 256 and 6 layers this is roughly 10M parameters, comfortably inside 16GB.
simjeg took 2nd in Orbit Wars with 4.3M.

### `kagg/train/` — IL then MaskablePPO

IL from search and heuristic trajectories, then PPO finetune.

## The hard problem: the market action

The market action is an **ordered list of up to 10** `[op, item, n]` orders.
This, not the farm ops, is the genuinely difficult modelling problem.

**Chosen approach — factorize per product.**
A fixed 9-wide head emitting a sell fraction per product, plus small discrete heads for
hire count, `BUY_LAND`, `BUY_SEED` per crop, and `BUY_ANIMAL`.

Rationale: order within a turn barely matters because orders settle one unit at a time
concurrently, so a fixed-size vector loses almost nothing and gains a great deal.
This is precisely the "per-planet Bernoulli instead of one-of-N-including-noop" fix from the
Orbit Wars post-mortem, transplanted — it keeps the probability mass for "sell something"
from being shattered across a sequence.

**Fallback ablations, in order of preference:**

1. Rule-based market layer (sell above a price threshold) with the network controlling only
   farm ops. Cheap, and isolates whether the market head is even where the value is.
2. Autoregressive over the 10 slots, as in Ender's micro-step approach.

## Reward

**Per-step bank delta, gamma ≈ 1.0.**

This is reward *decomposition*, not shaping — final bank minus starting bank is exactly the sum
of per-step deltas, by construction.
The full argument, and why the Orbit Wars ban on shaping does not apply, is in
`docs/rl_feasibility.md`. Read it before changing this.

Train on own money; evaluate on win rate.

## Deliberately out of scope for v1

- **Market denial.** Both farms are fully visible and premium goods floor at $1 on small volume,
  so dumping a good immediately before the opponent harvests it is a real attack.
  Worthless until the base economy is strong. Revisit in September.
- **Self-play.** The opponent couples only through market prices.
  Train against a fixed opponent until measurement says otherwise.
  Verification question 4 in `docs/economics_analysis.md` settles this.

## Kill criteria

Committed before implementation, so they cannot be rationalised away later.

| Gate | Criterion | If it fails |
|---|---|---|
| Economics | Heuristic agent clears **$20k** final bank | The economics model is wrong, not the agent |
| Sim | Parity exact over **1000** random action sequences | Do not train on the fast sim |
| RL | Explained variance passes **0.5** early | The frame is wrong, not the hyperparameters |

## Rough sequencing

61 days to the deadline, 54 to the new-entrant cutoff.

| Phase | Work |
|---|---|
| Week 1 | Arena, economics model, heuristic agent, first leaderboard submission |
| Week 2 | Vectorized sim plus parity harness |
| Weeks 3-4 | Offline search, IL |
| Weeks 4-8 | MaskablePPO finetune, ablations |
| September | Market denial, endgame tuning |

Getting a heuristic agent onto the leaderboard in week 1 matters:
it establishes a real baseline, and the `starter` agent everyone forks makes only $512.

## Testing

Every theory gets a failing pytest before any code change — carried over from
`orbit_wars/CLAUDE.md` and repeated in this project's `CLAUDE.md`.
The environment is deterministic given a seed, so there is no excuse for an untested theory.

The parity harness is the highest-value test in the project. Write it early, run it constantly.