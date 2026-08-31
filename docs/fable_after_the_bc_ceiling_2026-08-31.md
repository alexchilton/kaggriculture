# After the BC ceiling — decision, 2026-08-31

Verdict first: **the tape/planner agent is the product; the net is a dead end for this competition.
Spend the remaining 30 days on direct search over the schedule itself, decoded through the planner,
evaluated in the JAX sim against the recorded field.**
Everything below is the ranking and the reasons, then the four questions in order.

Basis: the measured facts supplied 2026-08-31 (clone agreement 1.0000 teacher-driven, greedy
self-driven $89,665 once, sampled median ~$16, PPO dead at update 0, tape $147,368, planner
$143,966). I have not re-derived them.

## Ranked, by expected value per unit of compute

### 1. Optimise the artifact: search over the schedule, planner as decoder (DO THIS)

The winners submit fixed 720-turn schedules.
The start state is fixed across all 78 recorded games; only opponent, shop timing and weeds vary,
and the shipped agent already handles the variation with two branch bits.
So the object to optimise is exactly what ships: four tapes (or four sets of 30 per-day target
rows), one per branch combination.
We have the only tool that makes this tractable — a JAX sim with 300/300 full-length parity — and
it has sat under a learning stack instead of a search loop.

Concretely, two steps:

**1a. Close the planner's decode gap first.**
The planner arm banks $143,966 against the tape's $147,368.
That $3.4k is a per-day, field-by-field diff between what the planner emits and what the tape does
on the same target rows — the exact diagnostic discipline already built for the d0-d6 work.
Caveat to check before treating $3.4k as real: whether both numbers came from fixed seeds
(`env.reset()` seed drift has inverted a finding before; one tape spanned $48k-$59k).
If the gap survives fixed seeds, close it in `kagg/search/cover.py` / the market block.
Payoff is double: the planner becomes shippable at >= tape, and step 1b gets a lossless decoder.

**1b. Local search over the per-day target rows.**
- **Genotype:** the 30 rows of `data/seed_scripts/kawashigi/schedule.json` per branch — plant
  counts/species per day, build days, land day, market order cadence. Not the raw 720-turn op
  stream: the planner (`cover.py`) repairs routing feasibility after any edit, so every candidate
  is a legal season by construction. Editing raw ops instead means most neighbours are infeasible.
- **Moves:** shift a plant day +-1, move a market order's hour/day, change a qty, retime BUY_LAND,
  add/drop a tile from a day's water/harvest set. Small, named edits — for each accepted move,
  one sentence on what it changes and why it could win (the global rule; it is what the
  `add_land` sweep lacked).
- **Objective:** win rate against the recorded field (`scripts/field_sweep.py`'s opponents — fair
  here precisely because the field is open-loop, as that file's docstring argues), money as
  tiebreak only. Select on win rate, never money: the ladder is Elo, and 11 of 54 recorded losses
  were inside $2,100 — a few $k of schedule improvement plausibly flips real matches.
- **Discipline:** held-out seeds, confirm every winner on a fresh draw, quote the seed range
  (~15% variance), checkpoint + `--resume`, flush rows incrementally, run on the Windows box.
  `sa_hiscadence_probe.py` and `field_sweep.py` are the starting scaffolding.
- **Ship path:** an accepted schedule drops into the existing agent unchanged — same submission
  format, no new machinery. Gate with `gate_pool.py`, then one ladder submission per candidate.

This is the only path on the table with headroom **above** $147k that does not route through a
network, and its evaluation cost is JAX-sim seasons, which we have in bulk.

### 2. Widen the closed loop: more branch bits, each with its own optimised tape

The agent reads two bits of state all season.
Kawashigi himself re-plans on the shop draw; we branch on it once (q4 by d5).
Candidate third/fourth bits: shop-unlock timing beyond yarn, and "opponent is selling my main
product" (we have measured flooding our own book on wool; a contested-market variant tape that
shifts sell cadence or crop mix is cheap to search with the step-1 loop).
Each new bit doubles the tape count but the search machinery from step 1 amortises.
Do this only for bits where the recorded losses show the current tapes actually failing —
read the 54 downloaded losses for which contingency killed us, then build that bit, not a grid
of all bits.

### 3. Nothing else. Explicitly NOT doing:

- **More BC / DAgger on the net for the product** — see (a) and (b).
- **PPO from the clone** — measured dead at update 0; the fix is not a hyperparameter.
- **ES / parameter-space search on the net weights** — it is the one RL-shaped thing that fits an
  argmax-only policy (see (c)), but it is compute spent making a $89.6k artifact approach a $147k
  one we already ship. Only relevant if step 1 somehow exhausts, which it will not by Sep 30.
- **Reopening reward design, per-step rewards, or the RL track generally.** Parked stays parked.

## The four questions

### (a) Is a neural net in the submission worth it?

**No. Plainly: the tape/planner agent is the product and the net is a dead end here.**

The net is a lossy compressor of an agent that already ships uncompressed.
Its ceiling, perfectly realised, is the teacher's $147k; its measured self-driven greedy is
$89,665 (once), because 6,818 op decisions x 719 bundle decisions at p=0.9995 each still compounds
to ~0.2% per season exact, and one dropped BUY_LAND ends a season's economy.
The only argument for a net was generalisation to boards the tapes never saw — but it was trained
exclusively on teacher-visited states, so it has no data there either; off-distribution it is
strictly worse than the planner, which re-plans from the live board by construction.
The state-dependent agent we want **already exists and is called the planner arm**.
It runs inside the submission today, needs no distillation, no vocabulary, no numpy port.

What the net work did buy, and it is not nothing: the numpy port is proven ship infrastructure,
and the BC ceiling is now a measured fact rather than an open question.
Freeze `offline_50epochs.pkl` and the port; stop spending on them.

One correction to bank: the imitation gate was "high agreement", and agreement was measured with
the teacher driving.
That gate was met and is meaningless — the gating quantity for anything downstream is
student-driven season quality, and that gate is failed.
Record it so the next session does not re-argue RL from the 1.0000.

### (b) DAgger against the planner teacher?

It is *coherent* where tape-DAgger was not: the planner reads the board, so it can label the
student's own damaged states, which is the actual DAgger contract.
It would plausibly fix the compounding-error mechanism.

But walk the value through: the product of a successful run is a network that approximates a
$143,966 agent — capped below both the $147,368 tape **and** below its own teacher, which already
ships as code.
You would pay weeks of compute to manufacture a strictly dominated artifact.
The stated tension (planner < tape) is real and the resolution is not to clone the planner —
it is to **fix the planner** (step 1a), which costs a per-day diff instead of a training run and
yields a shippable improvement rather than an approximation of one.

The only honest justification for planner-DAgger is as a substrate for RL fine-tuning that then
beats $147k.
That stacks two speculative stages in front of the deadline, behind a path (step 1) that needs
zero of them.
**Not worth it before Sep 30.**

### (c) The sampled-vs-greedy gap

Correct read: the $16 is irrelevant to the product.
The shipped decode is argmax; the product-relevant number is $89,665 greedy, and its gap to $147k
is (a)'s answer, not an RL question.

The $16 matters only because PPO's rollout policy is the sampling distribution, and a policy whose
entire value sits on a measure-zero argmax path gives sampling nothing to climb.
Low temperature, `--ent-coef` 0.0005, KL-anchoring: all shrink the same knob.
At the temperature where rollouts stop dying, exploration is gone; at the temperature where
exploration exists, the bank is $16.
There is no setting of that dial that produces a gradient, because the failure is one catastrophic
token (a dropped land buy, a wrong bundle) ending the season — smoothing the policy cannot make
the return landscape smooth.

The one method that genuinely fits an argmax-only-good policy is **search in parameter space
evaluated under greedy decode** — ES/CMA-style weight perturbation, fitness = final bank or pool
win rate, no stochastic policy anywhere.
The JAX sim makes it affordable in principle.
It is on the not-doing list anyway, for the (a)/(b) reason: it optimises the wrong artifact.

Flag, labelled **SPECULATION**, for whenever RL reopens: `kl +57.5` with `clip 1.000` at update 0
is also the signature of the rollout decode and the training-time scorer disagreeing about the
same parameters (this codebase has one autoregressive decode and one sum-of-marginals scorer, and
they have diverged before). Same params scoring their own fresh samples should sit near kl 0.
Worth one command before any future RL attempt; changes nothing today because the $16 median
kills PPO regardless.

### (d) The missing framing

Not missing — under-committed to. It is step 1 above: **optimise the artifact.**
The competition's own winners say the answer is a fixed schedule; our memory says every layer of
indirection between the search space and the submission caps the ceiling; the net was two layers
of indirection (learn a policy, that imitates an agent, that replays a schedule).
Remove both layers: search the schedule, decode with the planner, score in the JAX sim against the
recorded field, gate on pool win rate, spend the 5 daily submissions confirming winners on the
ladder.

Search space: per-day target rows per branch (plant/build/land/orders), planner as
feasibility-repairing decoder.
Objective: field win rate on held-out seeds; money as dense within-move signal only.
Compute: JAX-sim seasons on the Windows box — the cheapest evaluation this project owns.

## What was skipped

- No new measurements were run for this doc; all numbers are the supplied 2026-08-31 facts plus
  file docstrings read today (`kagg/search/sa_hiscadence_probe.py`, `scripts/field_sweep.py`).
- The $147,368 vs $143,966 comparison was not re-checked for fixed seeds — that is step 1a's first
  command, not this doc's claim.
