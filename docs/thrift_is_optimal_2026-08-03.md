# The policy is not failing to learn. It has learned that hoarding wins.

> **SUPERSEDED THE SAME HOUR, at update 492. Read `## Correction` at the bottom before anything
> else here.** The conclusion below was drawn from updates 0-209 and describes a *transient*. The
> policy hoarded to build capital and then deployed it: HARV recovered from 0.06% to 3.22%,
> `bank_final_med` reached $7,812, and the incremental win rate against `idle` went from 0.000 to
> **0.800**. The measurements below are accurate; the conclusion drawn from them was not.

**Date:** 2026-08-03, late afternoon.
**Two independent sources agreed on this within ten minutes of each other:** the live run moved for
the first time, and a laptop toy refused to reproduce the stall.

## What the live run did

Alex spotted it in the log first -- `bank med` and `money_max` rising, some maxima above $3,000.

| block | `bank_final_med` | `wr_idle` | `wr_pool` | `ev_signal` | `seed_rate` | HARV % of ops |
|---|---:|---:|---:|---:|---:|---:|
| 0–24 | $0 | 0.0000 | 0.490 | 0.031 | 0.0557 | 1.74 |
| 100–124 | $0 | 0.0000 | 0.493 | 0.278 | 0.0425 | 0.22 |
| 150–174 | $0 | 0.0000 | 0.471 | 0.475 | 0.0369 | 0.37 |
| 175–199 | **$140** | 0.0000 | 0.529 | 0.729 | 0.0287 | 0.32 |
| 200–208 | **$1,139** | 0.0000 | **0.570** | 0.742 | 0.0229 | **0.08** |

`money_max` exceeded $3,000 for the first time in the run's history at block 150–174, peaking at
**$3,335**.

**The step-function prediction from `docs/the_reward_is_a_step_function_2026-08-03.md` held exactly.**
`bank_final_med` climbed from $0 to $1,139 and `wr_idle` stayed at **precisely 0.0000 through the
entire climb**, as did `wr_farm` and `wr_ranch`. Recovering $1,139 of a burnt stake changed not one
terminal reward against any scripted opponent.

**But the mechanism is thrift, not earning**, which is Alex's objection arriving on schedule:

- `seed_rate` more than halved, 0.0557 → 0.0229.
- **HARV fell from 1.74% of ops to 0.08%.** The policy is farming *less*, not more.
- The best single game ever banked $3,335 — $335 of actual profit, against a stake of $3,000.

The bank is rising because the policy stopped spending. It is on its way to the $3,000 do-nothing
ceiling and it is abandoning farming to get there.

**And that is the correct play under this opponent mix.** `wr_pool` rose to 0.570 — its highest ever —
because a hoarder beats a frozen past self that still spends. Pool is 45% of the batch. The other 55%
is lost either way. So hoarding is the reward-maximising policy available, and PPO found it.

`ev_signal` jumping to 0.742 is the same story from the critic's side: now that final bank varies
between games and pool outcomes turn on who has more of it, outcomes have become genuinely
predictable. The critic is not broken. It is accurately predicting a degenerate game.

## What the toy said, including the part that refutes me

`scripts/toy_credit_window.py`, tabular Q-learning on `kagg/rl/toy.py`, 3 seeds x 40,000 episodes:

```
arm                           solved by   win rate   median bank
baseline (terminal only)            499      0.995        3,800
+ money potential                   499      1.000        4,600
+ reverse curriculum              2,499      0.993        3,700
+ both                            2,499      1.000        4,600
```

**The baseline solves it in 499 episodes.** The toy has a credit gap of 13 turns against a 1-turn TD
window — the same order of mismatch as the real game's 240-against-20 — and it does not stall at all.

**So the credit window is not a sufficient explanation for the real stall, and my framing of it was
wrong.** I argued repeatedly today that the payoff being outside GAE's reach is what blocks learning.
The most favourable possible learner still cleared that gap trivially. The gap is real; it is not what
is stopping this.

Caveat on the curriculum rows: "solved by" for those arms only starts counting once the tier has
retired up to full-length episodes, so 2,499 includes the ramp and is not comparable with 499. The
curriculum is not shown to be slower; it is shown not to be *needed* here.

**What the toy does show, and it is the useful part:** terminal-only reward plateaus at
**$3,800 of a possible $4,600**. Once winning is assured the reward is 1 whether you bank $3,400 or
$4,600, so there is no gradient to the optimum. The money potential reaches $4,600 on every seed. That
is a real effect and it maps directly onto the real game — against a broke mirror, $5 is as good as
$50,000.

## Why the toy did not reproduce the stall

Because in the toy **doing nothing loses.** The bar is $3,000 and holding $3,000 is not a win, so the
only route to any reward is a full plant-wait-harvest cycle. The learner farms because there is
nothing else to do.

In the real game, doing nothing **beats 45% of the batch**, because `pool` is frozen copies of a
policy that burns its stake. Hoarding is sufficient. Farming is optional.

That single difference explains both results at once, and it is not about credit assignment, reward
shaping, or the critic.

## What follows

**The diagnosis changes from "the policy cannot learn" to "the policy has learned the wrong game,
correctly."** That reframes every item on the list:

1. **The opponent set is the fault, and it is the only fault that has to be fixed.** Doing nothing
   must lose. `train_jax_rl.py:403-405` says this in as many words, about the `trade` seat: *"it
   removes the 0.5 payoff for inaction instead of trying to regularise around it."*
2. **Graded `idle` above $3,000 is now the leading candidate**, not the fallback
   (`docs/graded_idle_ladder_2026-08-03.md`). It is the only opponent immune to having its income
   destroyed by our own trading, so it is the only one whose bar we can place anywhere and trust.
   Below $3,000 remains dead, for exactly the reason Alex gave.
3. **P2b drops back down the list.** It was promoted on the credit-window argument, and the toy has
   just declined to support that argument. It is built and tested (`kagg/rl/opportunity.py`) and can
   wait for evidence it is needed.
4. **The money potential has a narrower and better-defined job than proposed.** Not "make the policy
   learn" — the policy learns fine — but "stop it settling for the minimum that wins", which is the
   $3,800-versus-$4,600 effect. That matters once the opponent bar is high enough to require real
   farming, and not before.
5. **`ev_signal` should stop being read as a health metric.** It is 0.742 while the policy abandons
   farming. It measures whether outcomes are predictable, not whether they are good.

## What is not yet known

Whether the policy plateaus at exactly $3,000 or pushes past it. The prediction is a plateau: hoarding
saturates at the stake, `wr_idle` needs $3,001 and cannot be reached by thrift, and `draws_idle`
should climb toward 1.0 as the bank approaches $3,000. If instead `money_max` keeps climbing well past
$3,335, the policy is genuinely earning and this whole reading is too pessimistic.

That is a free measurement — both fields are already logged, and the run continues.

## Correction, at update 492 (4.0M turns)

Everything above was read off the first 209 updates. Continuing to 492 shows those were the middle of
a learning curve, not the end of one.

**Incremental win rates** -- the `wr_*` fields are cumulative over the whole run, so the block figures
above understate recent play. Differenced:

| block | `idle` | `ranch` | `farm` | `pool` |
|---|---:|---:|---:|---:|
| 0–79 | 0.000 | 0.000 | 0.000 | 0.502 |
| 160–239 | 0.011 | 0.000 | 0.000 | 0.945 |
| 320–399 | 0.424 | 0.000 | 0.000 | 0.548 |
| 400–479 | **0.800** | 0.000 | 0.000 | 0.922 |

The four phases:

| updates | phase | `bank_final_med` | HARV % of ops |
|---|---|---:|---:|
| 0–199 | burning the stake | $0 | 1.75 → 0.39 |
| 200–279 | hoarding | → $2,434 | **0.06** |
| 280–399 | investing (bank dips to $23) | $1,424 → $23 | 1.08 → 2.11 |
| 400–491 | compounding | **$7,812** | **3.22** |

**Thrift was a stepping stone, not a trap.** The policy accumulated capital and then spent it
productively; `money_max` reached **$20,071**.

### What this retracts

1. **"The policy has learned the wrong game, correctly"** -- no. It learned the right game, in stages.
2. **The step-function prediction is refuted.** `wr_idle` rose smoothly rather than snapping at
   $3,000, because final banks are spread across games, so a rising *mean* bank lifts the win rate
   continuously even though a single game's reward is a step.
3. **The thrift trap did not occur**, though the reasoning that predicted it was sound in isolation.
4. **None of the interventions designed today are needed.** Graded `idle`, the money potential and
   P2b are built, tested and unwired, and should stay that way without new evidence.

### What survives

- The toy's finding stands on its own terms: terminal-only reward plateaus at $3,800 of a possible
  $4,600 because winning by more pays nothing. That effect is real, and it will matter *if* the
  policy stalls just above an opponent's bank rather than pushing past it.
- `ev_signal` is still not a health metric. It read 0.742 while HARV was at 0.08%.
- `wr_farm` and `wr_ranch` remain at **exactly 0.000** across roughly 1,250 and 1,000 games. Nothing
  here has beaten an opponent that earns from its own board.

### The lesson

Two confident conclusions were drawn today from windows of ~50 and ~200 updates, and both inverted
within the hour. `HANDOFF_2026-08-02.md` already records this: *"Four flat points inside the noise
band are not a plateau."* The rule needs widening -- a monotone trend over 200 updates is not a
plateau either, when the whole run is 20,000.
