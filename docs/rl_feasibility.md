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

The problem does not have the property RL is for. See `what_kind_of_problem_this_is.md` for the
full argument; the short version:

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

Throughput is in `throughput_measurements.md`. VRAM was never the constraint.

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
