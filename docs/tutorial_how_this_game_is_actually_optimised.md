# How this game is actually optimised, and why our two tracks could not do it

2026-08-04. Findings note. Everything marked **measured** comes from replay data in
`data/episodes/`; everything marked **inference** is reasoning from that data and is flagged as such.

---

## 1. The winners submit fixed scripts. That is not the same as being unoptimised.

**Measured.** Six leaderboard replays, five distinct players. For each player appearing in more than
one replay, every turn's action was split into `units` (`farmer` + `hands` ops) and `market` (trading
orders) and compared turn-by-turn between episodes.

```
senkin13        4 episodes, 6 pairwise comparisons, different opponents AND swapped seats
                units  identical 720/720  (100.0%)  in all six comparisons
                market identical 720/720  (100.0%)  in all six comparisons
                banks $121,538 - $145,034

syouya tobita   units  identical 720/720       (100.0%)  in all six
                market identical 716-720/720   ( 99.4-100.0%)

Dmitry Larko    units  701/720 (97.4%)   market 689/720 (95.7%)
```

`senkin13` plays a byte-identical 720-turn sequence regardless of opponent, and regardless of which
seat it holds -- episode 89544610 has the seats swapped and the script does not change.

> **CAVEAT ADDED AFTER REVIEW, AND IT IS SERIOUS. Read this before relying on the table above.**
>
> `senkin13` and `syouya tobita` are **not confirmed top-ranked**.
> `docs/episode_teardown_2026-08-03.md:100-104` already said so -- *"These are not the top five... a
> strong mid-field agent at ~$145k"* -- and this document originally dropped that.
> They are also a **mirror match**: 536/720 identical action dicts *between the two of them*, which is
> exactly the sample `CLAUDE.md` warns against generalising from (*"a mirror match is not a best
> response"*).
>
> The only confirmed top-tier games are the `Dmitry Larko` pair, and those are the **weakest**
> open-loop evidence in the table (97.4% / 95.7%). Our own docs do not even agree on that figure --
> `docs/market_finetune_design_2026-08-04.md:21` reports 673/720 = 93.5% for the same pair.
>
> So the airtight statistics belong to a player of unconfirmed rank, and the confirmed leader is the
> noisy data point. **Pull episodes for the actual top-five names and re-run this diff before treating
> "the winners are open-loop" as settled.** That has been an open item since 2026-08-03.
>
> The claim that survives independently of rank is section 4's: **"manual player" ranks #3**, and a
> human cannot compute reactive per-turn decisions across 720 turns under a clock. Lean on that.
>
> **Also untested, not negligible:** there are **zero** `WEED` tiles across all 720 turns of all six
> replays, despite `weedSpawnChance: 0.005`. "The winners ignore weeds" is therefore untested rather
> than proven harmless, and any open-loop script must be validated across many fresh random seeds
> before submission.

The distinction that matters, and the one this project kept collapsing:

- **Reactivity** is conditioning actions on observed state *at play time*. They have essentially none.
- **Optimisation** is searching for a good action sequence *before* play time. They clearly did a great
  deal of it.

Open-loop does not mean unoptimised. It means the optimisation happened offline and the result was
frozen. So the question "how can anything be optimised if they don't react" dissolves: the object of
optimisation is the **sequence**, offline -- not a **policy**, online.

A secondary measured fact rules out the obvious compression: **every player shows 30/30 distinct daily
unit-routines.** No two days are byte-identical, so "one daily routine, repeated" cannot express what
the winners play. There is seasonal phase structure, but the artifact is a genuine 720-step program.

---

## 2. Why optimising a 720-step sequence is tractable, when our two tracks were not

The enabling property is **determinism**. `f(action_sequence) -> final_money` is a deterministic
function of the sequence. Two consequences, and both are large:

**Evaluation is exact.** `CLAUDE.md` records seed variance at ~15%, and that noise is the reason the
project needed held-out seeds, resampling, and confirm-the-winner-on-a-fresh-draw. It is also why the
CEM search needs population 256 over 20 generations to see anything at all: it is averaging away noise.
With no noise, one evaluation is the answer.

**A single perturbation's effect is exactly measurable.** Change turn 312's action, re-run, read the
delta. That is not an estimate requiring N samples -- it is the exact finite difference in a discrete
space. This is precisely the quantity that PPO spends an entire critic, GAE, and 719 steps of credit
assignment trying to approximate.

That makes standard combinatorial methods work:

1. **Coordinate ascent.** For each of 720 turns, try every legal alternative action and keep the best.
   One sweep is `720 x alternatives` evaluations, embarrassingly parallel on the batched JAX sim.
   Iterate until no single turn yields an improvement.
2. **Rollout-based lookahead -- and this is NOT a new option.** An earlier draft of this document
   claimed `CLAUDE.md` rejected beam search for lacking a partial-return score, and that a
   deterministic evaluator made the rejection "expire". Both halves were wrong. `CLAUDE.md` never
   mentions beam search; the relevant text is `kagg/search/cem.py:6-12`, and it *already* considered
   rollout-based pruning and rejected it for a different reason: *"Pruning on the true objective would
   need a rollout per node, at which point it is a population method with worse sample efficiency."*

   So this is a return to an option already weighed and priced as **inferior to CEM**, not a newly
   unlocked one. The reframe consequently owes an argument it has not yet made: why *trajectory-space*
   CEM beats *gene-space* CEM. They are the same paradigm; the claim can only be that the
   parameterisation is richer and less lossy, and that the executor's hand-coded interpretation is the
   binding ceiling. That is a real argument but it is not novelty.
3. **Waste elimination.** Measured: `senkin13`'s farmer-unit no-op rate is **7.2%** (52 of 720) against
   our plan executor's ~**88%** (`docs/executor_livestock_broken_2026-08-04.md`). This is the one part
   of the cost argument that strengthened under review, and it needs no strategic insight to collect.

**Cost, stated honestly.** An earlier draft put a coordinate-ascent sweep at "720 x alternatives".
That undercounts by more than an order of magnitude: a turn's action is a joint over up to 24 unit
slots plus a 10-slot market queue, so the real granularity is roughly **(turn x slot) ~ 17,000+**
single-choice points per sweep. Still tractable -- checkpoint the state at turn `t` and `lax.scan` the
remainder across a batch dimension, which `kagg/sim/jax_sim.py:1214,1300-1308` supports -- but the
figure is ~17,000, not 720.

---

## 3. Why our two tracks failed

Both tracks optimised **proxies**. The winners optimise **the artifact that gets submitted**. Every
layer of indirection between the search space and the artifact costs you, and we had two.

**The CEM/plan track.** It searches 283 genes which `kagg/search/executor.py` then *interprets*. The
ceiling is therefore the executor's expressiveness, not the search's power. This is not abstract: when
livestock failed, it failed because the 9-step animal chain was hand-coded and wrong, and CEM had no
way to route around the bug. Measured consequence -- the leaders' own allocation, run through our
executor, banks **$0** and loses 3/3, buying 29 animals against a specified 14 and 15 units of feed
against their 967.

`CLAUDE.md` had already written the warning: *"A heuristic agent is a teacher and a sparring partner,
never the final policy. This is the correction to the Orbit Wars failure where heuristics became the
policy and capped the ceiling."* The failure was reproduced anyway.

**The RL track.** It trains a reactive per-turn policy, paying the full price of credit assignment over
719 steps with one bit of terminal reward, in order to learn a behaviour the evidence says requires no
reactivity at all. The costs it paid for nothing:

| Fought | Why it existed | Under trajectory optimisation |
|---|---|---|
| Credit assignment over 719 steps | RL must infer which action mattered | Exact: perturb a turn, read the delta |
| Reward on ~11 of 8,192 rows | Terminal-only PPO | Objective evaluated exactly per rollout |
| Entropy vs. objective | Exploration proxy | No entropy term exists |
| 9 uncorrelated heads cannot form a chain | Factored policy marginals | The chain is written into the sequence |
| `ev_signal`, GAE, value margin, shaping | Critic machinery | No critic |

And the strategic ceiling was already known: the leaders bank $100k-$144k with ~35% of revenue from
milk and wool, against our best crop-only result of **$28,168**. A perfected crop policy does not lose
narrowly; it loses by 3-5x, because the missing revenue is not in the crop space at all. No entropy
setting or shaping coefficient changes that.

---

## 4. How they probably got there

**Inference, not measured.** We know *what* they submit (a fixed script); we do not know their
construction process. But one leaderboard fact is very informative: **"manual player" ranks #3 at
2,911.8.** A human, playing by hand, is third.

That says the game yields to patient reasoning about a fixed plan far more readily than to clever
algorithms. It is consistent with the top scripts being human-built and then iteratively refined --
play, read the replay, notice a specific waste ("I spent six turns walking to the shed"), fix that one
thing, re-run, measure, repeat.

That process *is* coordinate ascent, with a human as the search operator. And a human is a strong
operator here, because they can reason about *why* a turn is wasted instead of sampling blindly. The
automatable version of the same loop is section 2.1.

---

## 5. Current status of the validating experiment

We hold `senkin13`'s exact winning script in the replay JSON, so the sharpest available test is to
replay those actions through our own simulator and check we reproduce $145k.

**PASSED, to within 0.2%.**

```
turn  day |  recorded p0      ours p0     err | recorded p1      ours p1     err
  48    2 |          109          109      +0 |         211          211      +0
 240   10 |        1,082        1,082      +0 |         876          875      -1
 480   20 |       50,796       50,887     +91 |      50,509       50,343    -166
 718   29 |      145,018      144,743    -275 |     143,571      143,884    +313

final: recorded $145,018 / $143,571    ours $144,743 / $143,884
ratio ours/recorded: 0.998 / 1.002
```

This is a stronger gate than the action-level parity harness, because it runs a real $145k season
*including the livestock economy* -- ~35% of that revenue is milk and wool, the half both of our tracks
failed to use. The simulator reproduces it.

**What was wrong, and it was not the adapter.** The first attempt returned $0/$0 with a $2 divergence at
turn 2. `Actions.hire` was a **boolean**, so at most one hire per turn was expressible, while
`senkin13` batches hires within a single turn on **106 of 720 turns** (304 hires total, up to 4 in one
turn) starting at turn 1. Once our crew size differed from the recorded one, every subsequent unit
action -- addressed by slot index -- landed on the wrong farmer. Positions tracked exactly for 209
turns and then the season collapsed.

`Actions.hire` and `Actions.buy_land` are integer counts as of 2026-08-04, emitting one order slot per
hire (the reference spends a slot per atomic order). Pinned by `tests/test_multiple_hires_per_turn.py`,
mutation-verified, and the full suite shows no parity regression.

**The residual ~0.2% is understood, and it is the next fidelity item.** Tracking is exact to +/-$1 for
ten days and then drifts ~$150. Our `_order_book` lays orders out in a canonical order -- sells, seeds,
products, animals, HIRE, BUY_LAND (`kagg/sim/game.py:240`) -- whereas `senkin13` emits HIRE *first*.
`_process_market` pairs the two players' i-th orders and quotes from the same pre-commit inventory, so
the pairing changes prices. Per-product arrays cannot carry an arbitrary order; exact replay would need
a raw-order-list entry point.

This is a **deterministic** bias, not noise, so candidate-vs-candidate comparisons during optimisation
remain self-consistent even before it is fixed.

Scripts: `scratchpad/replay_leader.py`, `scratchpad/replay_diag.py`.
Logs: `data/logs/replay_after_hire_fix.log`, `data/logs/replay_diag.log`.

---

## 6. What to carry forward

- Optimise the artifact that gets submitted, not a parameterisation of it. Two layers of indirection
  cost this project a day each.
- Determinism is the most valuable property this environment has, and both tracks were built as though
  it were stochastic.
- Before ruling out a method, check whether the reason it was ruled out still holds. Beam search was
  rejected for a reason that a deterministic evaluator invalidates.
- A measured ceiling beats a tuning intuition. $28,168 against $100k-$144k was knowable before any of
  the entropy work.
