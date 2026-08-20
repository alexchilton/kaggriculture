# The RL track: what it measured, and why it is parked

> **This file used to argue for RL as the primary tool and for a per-step bank-delta reward.
> Both were overruled, and the arguments have been replaced with the measurements that overruled
> them.**
>
> `CLAUDE.md` still carries a bullet saying this file "still argues for [per-step bank delta] at
> length" and is kept so a future session does not reinstate it from here. That is no longer true
> of this file: the reward rule below is the corrected one. The bullet's *ruling* stands.
>
> The path is unchanged because `CLAUDE.md` and several modules point at it.

## The ruling on reward, and it applies to every policy in the project

**The reward is terminal: win 1, loss 0 (or -1/+1), gamma 1.0. Never per step.**
Alex's call, made explicitly, 2026-08-01.

The original argument for per-step bank delta was that final bank minus starting bank is *exactly*
the sum of per-step deltas, so it is reward **decomposition**, not shaping. That is arithmetically
true and strategically wrong: **the ladder is an Elo rating, so margin does not count.** A $43k win
and a $4k win are the same result, and a per-step money reward trains a margin maximiser.

It is also what the evidence says. Of the top finishers in the comparable competition whose
write-ups we have, four used a terminal signal — Felix Neumann -1/+1, simjeg terminal with
gamma 0.995, Isaiah Pressman terminal, Billy Bradley's `ender` positive-only 0/1/2 with gamma
0.998 — and **none** used a per-step bank delta.

If credit assignment over 720 steps stalls, the agreed next move is a **per-game-day** signal, not
a per-step one, and only after `explained_variance` has been checked.

Potential-based shaping is a separate question and is not banned by the above: Ng, Harada & Russell
1999 leaves the optimal policy provably unchanged, and at gamma 1.0 the per-turn terms telescope so
an episode's total shaping is exactly `PHI(end) - PHI(start)` whatever route was taken.
`kagg/rl/money_potential.py` implements one (floored at the $3,000 stake, scaled to $100k, squared)
with 16 tests. `coef` defaults to 0.0 and it was **never wired into `train_jax_rl.py`**.
`kagg/rl/net_worth.py` sketches a balance-sheet potential that would stop FEED and FERTILIZE reading
as pure loss. Neither was built out; both are recorded here rather than in a separate ideas file.

## Why the track is parked

The problem does not have the property RL is for. See "2026-08-05 — What kind of problem
kaggriculture is" below for the full argument; the short version:

- **There is nothing to react to.** The top of the leaderboard submits byte-identical 720-turn
  tapes across seats and opponents (`the_field.md`).
- **The environment is deterministic given the tape**, so `Q(s, a) = V(s')` can be *computed* by
  simulation rather than estimated. One perturbation's effect is an **exact finite difference** —
  the quantity a critic, GAE and 719 steps of credit assignment exist to approximate.
- **The reward is terminal and the objective is a ranking against a fixed field**, which is a
  best-response computation.

RL becomes right again if the field turns adaptive, or if the state space outgrows exhaustive
evaluation. Neither is true today.

## What the track measured, and it is worth keeping

Every item below is a measurement that cost real time to obtain. Several are about *measurement*
rather than about RL and generalise to anything this project does next.

### The failures were temporal, not architectural

`jax_sim._end_of_day` returns every unit to spawn, **dismisses every hired hand** and **empties
every unit's inventory**. So every *maintenance* op — which needs a walk back to a tile on a later
turn — is re-motivated from scratch each dawn: four independent draws that must all land, for a
payoff days away, under a critic at `ev_signal < 0.3`.

Over 412,992 owned-unit actions the policy placed 4,591 animals and **fed 12**; planted 13,439
crops and **harvested 98**. Setup ops (PLANT, PLACE — one action, on the tile you already occupy)
it did *more* than the teacher. **It did not fail to learn farming; it learned exactly the subset of
farming that survives a one-step credit horizon.**

That killed the "it can't do them" theory outright: on day-25 seeded boards, COLLECT_FERTILIZER is
legal on 15.1% of unit-slots and CARE on 11.2%, and the policy had chosen COLLECT_FERTILIZER **zero
times in 23,684 episodes**. Legal often, never taken.

`kagg/rl/commit.py` fixes it: a `COMMIT_*` token in the same categorical as every primitive op
freezes a target, the unit walks it and fires the arrival op on contact, and intermediate turns are
**excluded from the PPO density** (not scored as probability 1). After **11 updates**:

| op | before | with commitments |
|---|---|---|
| COLLFERT / FERTIL | **0.00%** | 2.01% |
| CARE | 0.07% | 1.98% |
| PICKUP | 0.63% | 3.58% |
| HARVEST | 0.44% | 1.14% |
| harv/plant | 0.18 | 0.63 (teacher 2.28) |

### The decode destroys the behaviour, not the network

`play_checkpoint.py` defaulted to per-head argmax. Same checkpoint, same 32 games:

| | greedy | **sampled** |
|---|---|---|
| WATER | 0% | **5.62%** |
| PLANT | 0% | **2.50%** |
| raw FEED | **0** | **18** |
| bank | $2,998, zero variance | $1,305 (min 54, max 3,534) |
| W/D/L | 0/0/16 | 0/0/16 |

**The marginals contain the behaviour; argmax over independent per-head marginals destroys it.**
Nine independent "probably not sell" decisions compose into "never sell". `condition_on_trade` —
drawing the op first and scoring the argument heads on the slice it selects — is the fix, and it
shipped for the **market** heads where the marginals discriminate 12:1.

`condition_on_op`, the same technique on the **unit** heads, was built and measured as **no
detectable difference** (effect changes sign between seeds; within-architecture seed spread is as
large as the effect). It is inert by construction there: `crop` is read by PLANT alone and was
already `p(crop | PLANT)`, and only PICKUP and PLACE share `item`/`qty`, at 7.8:1.
**Do not read that null on the unit heads as a verdict on the market ones.**

The durable value from that work is the scaffolding: the `ratio == 1.0` gate catches a silently
corrupted PPO update, and `migrate_params` means an architecture change no longer costs every
checkpoint and the KL anchor.

### Metrics that measured the setup, not the policy

This is the most expensive recurring lesson in the whole track.

- **`vs farm 0.659` was entirely an artifact of the seeded start.** From turn 0 the same checkpoint
  went 0/0/32, banking $2,998 against the scripted farmer's $30,292, with 100% movement and zero
  productive actions over a whole season. **Prefer a replay to an aggregate.** The reward pays 0.5
  for a draw, so two policies that both bank $0 draw with certainty — `money == money` is exact.
- **The per-opponent win rate measured nothing** even though it was computed on exactly the right
  rows: the opponent was re-drawn every update while a game spans ~22.5 of them, so a game faced a
  mean of 4.9 distinct opponents and the label recorded whoever held the seat at the end.
  **Ask what unit an aggregate is aggregating over, and whether the label is constant across it.**
- **The curriculum mix was specified in slots and spent in episodes.** `0:0.1` asked for 10% of
  slots and delivered ~3% of finished episodes, because day-0 episodes are ~6x longer. Day 25
  supplied ~83% of terminal episodes, so the aggregate `wr` was a day-25 number wearing a mix's
  name — and it was carrying four rungs sitting at chance (day20 0.523, day15 0.491, day10 0.484,
  day0 0.528).
- **`ev_signal` and the animal gap are structurally uninformative under symmetric starts.** With
  identical seats the true value is 0.5 on every board at t=0, so there is nothing to explain from
  the state. **The >0.5 explained-variance kill criterion does not apply to a symmetric run.**
- **`best.pkl` is selected on cumulative win rate and therefore favours early updates** — update 38
  on one run whose settled rate came much later. Prefer `latest.pkl` unless you have checked.
- **After any configuration change, check whether a metric still measures what it was calibrated
  on.** Four numbers in one session were read as findings when the setup had changed what they
  measured.

### The scale gap was the real story

| | bank |
|---|---:|
| top public agents, head to head | **$90,000 – $123,000** |
| our policy at update 690 | $18,332 median, $34,127 best |
| our best training opponent (`farm`) | $27,340 |

**We trained against a pool whose ceiling was a quarter of the field's floor**, and no opponent in
it used the animal economy, crops beyond melon, fertiliser or a twelve-hand crew.
Meanwhile total experience across the whole track never approached the 1B-15B env steps the
competitors in the comparable competition used — Billy Bradley ~1B on a single 3080, simjeg 10B,
Isaiah Pressman 15B.

**We were step-bound by roughly two orders of magnitude, not capacity-bound.** `kagg/rl/jax_policy.py`
defaults to `d_model=128, n_layers=3, n_heads=4`; simjeg took 2nd in the comparable competition with
4.3M parameters and Felix Neumann 3rd with 6.2M. Scaling the model was measured as the wrong lever.

Throughput is in "2026-07-31 — Env throughput, measured" below. VRAM was never the constraint.

### Hardware

The 3080 had been running at **210 MHz of 2100** under `SwThermalSlowdown` at 90 C, drawing 41-64 W.
Every throughput figure in the RL era was measured on a throttled card and the "1B steps is about a
month" estimate was 3x pessimistic. Cold it does ~1,100 turns/s and decays to ~370 within two
minutes.
**This is closed and ruled on. Do not re-rank cooling into any review.**

## The Orbit Wars killers, and which transferred

Kept from the original file because the table is still the right analysis of *this* environment.

| Orbit Wars killer | Applies here? | Why |
|---|---|---|
| No-op became a stable self-play equilibrium | **No** | PASS buys you $3,000 while the opponent banks $50k. The environment punishes passivity directly. |
| Masking was a quality judgment | **No** | Masking here is pure legality. The thing that burned us was masking *no-op* to force action. |
| Reward shaping optimised a proxy | **Partly** | Money is not a proxy for bank, but bank is a proxy for the Elo score. Hence the terminal ruling above. |
| Exploration shattered across ~480 options | **No** | 18 ops per unit. |
| Self-play instability | **Largely no** | The opponent couples only through market prices. |
| Candidate filter capped the ceiling | **Avoidable** | There is no candidate-generation step to poison. Keep it that way. |

The genuinely transferable warning is the death spiral: RL not learning → "help" it with heuristics
→ the help starves the learner → conclude RL cannot do this. The defence is the kill criteria in
`CLAUDE.md`, committed before any code was written.

**Scope note on the explained-variance gate.** It was written for the per-turn, 720-step,
full-action-space policy. `kagg/rl/env.py`'s strategy env clears 0.89 easily, but that is a 30-step
problem with 9 discrete heads and hand-built features. Clearing it there is *not* evidence the hard
frame works.

## Two corrections this track made to its own record

- **A decision to skip a fix can expire when the problem changes.** `hand_prior_heads` declined to
  shape the market heads for a stated and correct reason: their failure was *under*-firing from a
  broken joint decode, and a flat prior would not fix a missing correlation. The autoregressive
  decode landed and the failure inverted to over-firing — `buy_seed` on 29.1% of turns, bank at $0
  by day five. Same code, same argument, opposite problem.
- **Evaluate a technique against the problem its author built it for.** Ender's autoregressive
  micro-steps were assessed here against the spawn deadlock — correctly answered *no*, twice, and
  struck off. He built them for **action-space explosion**, which we independently had and had
  measured three times. A correct *no* to the wrong question is indistinguishable from a dead end.

## 2026-07-31 — Env throughput, measured

Folded in from `docs/throughput_measurements.md`.

Reproduce with `python scripts/bench_arena.py`.
This decided whether the vectorized simulator was optional. It is not.

### Numbers

`starter` vs `pass`, 100 games per row (worker startup amortised), 719 steps per game.

| Machine | CPU | 1 worker | best multiprocess | 1B steps | 10B steps |
|---|---|---|---|---|---|
| Mac (dev) | 14-core Apple Silicon | 1,054 steps/s | 8,009 (12 workers) | 35 h | 347 h |
| **Windows box (training)** | **AMD Ryzen 9 5900HX, 8c/16t** | **484 steps/s** | **4,221 (16 workers)** | **66 h** | **658 h** |

The training box is **2.2x slower per core** than the dev Mac and 1.9x slower in aggregate.
Every throughput figure that matters is therefore the Windows row, not the Mac row.

Scaling is poor: 16 workers gives only 8.7x over one worker on an 8-core/16-thread part.
SMT contributes little and the Python interpreter dominates.

### Correction to a previously recorded fact

`README.md` recorded **1163 steps/sec single-threaded** as a measured fact.
That figure is roughly the *Mac* rate and is 2.4x optimistic for the machine that will actually
train.
The training box does 484.

### What this means for the plan

Competitive runs in the comparable previous competition used **8-15B env steps**
(8th place ~1B on a single 3080; 2nd place 10B; 1st place 15B).

- 1B steps on the training box: **66 hours**. Viable once, far too slow to iterate.
- 10B steps: **658 hours, 27 days**. Not viable.
- To reach 10B in 24 hours the sim must sustain **~116,000 steps/sec**, about **27x** the
  Python env's best multiprocess rate.

These are also *optimistic* numbers, for two reasons:

1. They use `starter`, a trivial random policy. No policy forward pass is included.
2. **`env.run()` cannot feed a GPU.** It plays a whole episode with per-step agent callbacks
   inside a worker process, so policy inference cannot be batched across environments. The
   options with this harness are a CPU policy copy per worker, or shuttling observations to the
   main process over IPC every step. Both are bad, and neither is what the throughput above
   measures.

A vectorized on-device sim removes that entire class of overhead as a side effect, which is a
second, independent argument for it beyond raw speed.

### Consequence

The vectorized simulator is **required, not optional**, and its target is set by the 10B figure:
**~100k+ steps/sec**.
Renting GPU time should be considered rather than assumed away — one 3080 Laptop may not be
enough to be competitive even with a fast sim.

What multiprocessing *does* buy is a **proof-of-life run**: 100M steps in ~6.6 hours on the
training box, enough to test the RL frame against the explained-variance kill criterion in
`CLAUDE.md` before committing to the sim build.

### Correction: the "1,032x" sim figure was an idle-profile measurement

Recorded 2026-07-31, after a JAX port measured the same code and could not reproduce it.

The 499,543 steps/sec (and a later 752k) quoted for the numpy sim were measured with **one live
unit per player on an empty board**, issuing WATER against nothing. Almost every masked update hit
its `if not active.any(): continue` shortcut. That is the sim's best case, not its working case.

Measured again on the same machine, at B=512, with units actually planting:

| live units per player | steps/sec |
|---|---|
| 1 (the original figure's shape) | 818,000 |
| 8 | 571,000 |
| 24 | 356,000 |

And even that 24-unit figure is optimistic, because the units all start stacked on the spawn tile,
so after the first one plants the rest hit the occupied-tile early exit. An independent measurement
with units genuinely spread out and hiring each turn put the numpy sim at **~15,000 steps/sec** at
B=512 -- though that run was taken while the machine was at load 200, which the same benchmark
showed can move absolute numbers by up to 2x.

**What to trust:** ratios, not absolutes. Absolute throughput on this Mac varies with machine load
by up to 2x, so any single figure is only meaningful next to a control measured at the same time.
The speedup over the reference environment is somewhere between **30x and 200x on realistic
workloads**, not the 1,032x first recorded. That is still transformative -- a 1B-step run goes from
66 hours to somewhere between 20 minutes and 2 hours -- but the headline number was wrong and was
repeated in several places before being caught.

**The lesson:** a benchmark whose workload does nothing measures the shortcut, not the code. State
the workload alongside the number, always.

## 2026-08-05 — What kind of problem kaggriculture is

Folded in from `docs/what_kind_of_problem_this_is.md`.

Written after a day in which every result that looked like a fact about the game turned out to be
a limitation of our own code. The purpose is to name the problem class precisely, so the next
session reaches for the right tool instead of rediscovering the wrong one.

### The short version

**It is a deterministic, open-loop, multi-dimensional knapsack with a time-phased budget, played as
a best response against a fixed field.**

Every clause is load-bearing and each rules out a family of approaches. Measured rather than argued:

- **the allocation is computable** — closed form from the town's drains reproduces the leader's farm;
- **the schedule genuinely needs search** — greedy-by-payback under a cash simulation recovers only
  23% of what a beam finds, so this half is not reducible to a rule;
- **the simulator is the verifier**, never the search engine.

We spent weeks treating all three as one undifferentiated search problem.

### Why it is not a reinforcement learning problem

Not because RL is weak, but because the problem has no property RL is for.

**There is nothing to react to.** The top of the leaderboard submits a fixed 720-turn tape, and four
fresh replays of the leader are byte-identical in every derived quantity across four opponents and
both seats. A policy mapping observations to actions is solving a harder problem than the one being
scored.

**The environment is deterministic given the tape.** `Q(s, a) = V(s')` can be *computed* by
simulation rather than estimated. Fitted-Q, TD learning and replay buffers all exist to approximate
a value function we can evaluate exactly.

**The horizon is 30 decisions, not 720.** A season is a bag of chains, one per unit. Credit
assignment over 720 steps was the motivating difficulty for the RL framing and is an artifact of the
wrong decision granularity.

**And the reward is terminal.** The ladder is Elo, so a $43k win and a $4k win score identically.
That is a *ranking* objective over a fixed field — a best-response computation, not a control
problem.

RL becomes right again if the field turns adaptive, or if the state space grows past what exhaustive
evaluation can reach. Neither is true today. See "Why the track is parked" above.

### The structure, formally

Choose a set of **chains** (a crop block or a pen group, with a start day and options) to maximise
the final bank, subject to:

| constraint | value | notes |
|---|---|---|
| tiles | 100, non-overlapping | 25 owned at spawn; 75 after two parcels |
| units (slots) | one chain per unit | a unit's position is a cumulative sum, so two chains on one unit interleave and both fail |
| turns | 23 work turns per unit-day | the binding constraint on tiles per chain |
| market drain | 8 products, 2,086 crop + 1,122 animal units | how much the town removes before the price floors |
| cash | $3,000 at dawn on day 0 | **a flow, not a stock** |
| land | $1,000 / $2,000 / $4,000 in fixed order | `_do_buy_land` ignores which quadrant you ask for |
| hires | Fibonacci in the day's hire count, resets daily | 12 hands is $376/day; 17 is $4,180/day |

The objective is **nearly additive**: chains interact through exactly three channels — the shared
price curve per product, cash timing, and tile/slot exclusivity. Nothing else couples them.

That near-additivity plus the *concavity* of the price curve is what makes the **allocation**
tractable: with a concave objective and linear constraints, ranking by marginal-value-per-resource is
near-optimal rather than a heuristic. See `economics_q5_findings.md` §4 for the arithmetic that
recovers the leader's farm.

**But cash timing is not a mild coupling, and this is where the naive reading goes wrong.** Cash is a
flow, so "chain B is unaffordable until chain A has sold" is a precedence constraint that compounds
over thirty days: which chain to fund first, and whether a given dollar buys land or seeds, changes
what is affordable for the rest of the season. Measured, that coupling is worth roughly **four times
the allocation itself**. Additivity buys you the mix. It does not buy you the schedule.

### What genuinely needs search

**1. The schedule.** The leader's own timeline is a dependency chain:

```
melon + wheat in NW, day 0-2   ->  revenue by day 3
revenue                        ->  NE parcel day 7, SW parcel day 10
parcels                        ->  strawberry on 41 tiles, days 7-14
```

A hand-built farm cannot test it, because every configuration either has the land or does not —
which is choosing the answer. Measured: asking for 6 wide strawberry blocks with no revenue first
ends with 75 tiles still locked and a starved pen.

**2. Inputs versus outputs.** Wheat's own market is seventh of eight and the leader plants 40 tiles
of it, because it is an **input**: 14 pens eat ~420 units a season and wheat is the only crop
returning cash by day 3. A revenue ranking scores it last. This is the one coupling a purely additive
model cannot represent — the calculator computes 0 wheat tiles against his 40.

**3. The opponent shares the drain.** Both players sell into the same town inventory. Against a fixed
field this is still tractable — it is a best response, and the leaderboard *is* fixed since everyone
submits static tapes — but it is a game, not a solitaire optimisation.

### The tool ordering

1. **Compute the allocation** (`scripts/allocation_calculator.py`). A target, not a starting point.
2. **Beam over chains for the basin** (`scripts/beam_chains.py`) — one exact joint max per slot, the
   simulator as the model, beam width for the interactions. Cheap and deterministic.
   Its weakness is structural: greedy forward selection commits slot by slot and `--refine` sweeps
   *timing only*, so it can re-time a genome but not restructure one.
3. **CEM/ES to restructure out of the basin** (`scripts/search_chains.py --seed-genome`). An ES
   mutates whole genomes, so it can move a slot from melon to strawberry *and* fix that slot's land
   day in one proposal. The beam structurally cannot.
4. **Verify on held-out seeds, in the real environment** (`scripts/arena_gate.py`) — fresh seeds,
   weeds on, live pool. Not optional, and not the same as the in-search score.

> **Status note, 2026-08-08.** The chain-search stack above is the *offline* half and is currently
> parked; what ships is the closed-loop schedule agent in `architecture.md`. The problem
> classification is unchanged and the agreed direction ("offline basis, checked per day, repaired on
> deviation") comes straight from it. Dollar figures produced by that stack are from a codebase that
> has since moved; treat them as evidence about *method*, not as current scores.

### The trap that has cost the most: overfitting the objective

Recorded twice in `CLAUDE.md` — *"a fixed 3-seed objective reported +40% where held-out seeds said
+12.8%"* and *"11 accepted moves in 14 generations for +1.6%"* — and `search_chains.py` had the
defect built in until 2026-08-05: the board draw was cached on one seed, so thirty generations of
five hundred candidates all fit the same sixteen games, and the incumbent kept whatever score its
lucky draw gave it and could never be displaced.

Both fixed: a new draw every generation, the incumbent re-scored alongside its challengers on that
same draw, and a `--holdout` pass that prints the in-search versus held-out gap so the curse is
measured rather than assumed.

**Seed variance is ~15%. Always quote the range.**

### The failure mode to watch for, because it recurred six times in one day

Every one of these was reported by the search as a fact about the game and was actually a limitation
of the chain builder:

| looked like | actually was |
|---|---|
| "animals do not pay" | `ranch()` never collected fertilizer; then capped the herd at 4 |
| "fertilizer does not help" | `grow()` emitted `FERTILIZE` and never *ordered* any, so every op was refused |
| "day 0 is the right time to buy land" | the catalog hardcoded `LAND_DAY_CHOICES.index(0)` |
| "strawberry loses to melon" | `BLOCK_SIZE = 4`, because `grow()` watered every tile every day |
| "four pens is the right herd" | 1 pen = 1 chain = 1 slot, so five pens ate five of eight slots |
| "weeds cost nothing" | true on our farms, false on a farm that replants — carrot +$2,055 with DIG |

**Before believing a measurement about a mechanic, ask what the code could not express.** List what
the action space, the routine and the catalog can each emit.
`tests/test_catalog_covers_every_gene.py` enforces the catalog half automatically — it asserts every
gene `decode()` reads takes more than one value somewhere in the catalog — and it caught a live
instance on its first run.

### The shape of the target

The top of the board is a knife-edge: everyone banks $120k-160k and the leader edges it by ~3%. On
an Elo ladder a $2,634 win scores what a $50,000 win scores, so the target is a **small consistent
edge over several near-equal fixed scripts** — and because they are fixed, they cannot punish
anything. They are a stationary target to compute a best response against.
