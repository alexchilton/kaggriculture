# Fable's review of the DAgger tape-teacher setup

2026-08-22. Read-only review, run against `da2de61`..`17d8ed0`.
Verbatim findings, saved before relaying.
Input given: `docs/dagger_tape_teacher_2026-08-22.md`, `scripts/dagger_tape.py`, `kagg/il/tape_teacher.py`,
`kagg/rl/jax_obs.py`, `kagg/rl/jax_policy.py`, `kagg/rl/jax_act.py`, plus the round 0 / round 5 measurements.

## 1. Loss-down / agreement-down at round 5 is expected, not a defect

Three mechanisms, two verified in source, one arithmetic.

**(a) Sampled agreement conflates correctness with confidence.**
`scripts/dagger_tape.py:150-169` measures agreement on the *sampled* action; the loss is NLL.
The warm start was fit to tetsuya, a different player.
Pulling it toward カワシギ's labels first RAISES entropy -- the confident tetsuya modes get unlearned
before the new modes form -- and a calibrated-but-unconfident policy has falling NLL and falling
sampled agreement at the same time.
The arithmetic is consistent: loss 0.3834 is the mean over 8 heads, ~3.07 nats total; if ~1.8 of
those sit on `op`, then `p(teacher op) ~ e^-1.8 ~ 0.17`, against a measured op agreement of 0.1589.
That is what a policy that has spread its mass looks like, not a broken one.

**(b) The distribution-shift reading is real but secondary.**
The loss is computed over the aggregate (`dagger_tape.py:434-441`), at round 5 mostly
teacher-driven states; agreement is on fresh mixed-driven states.
Mechanism (a) predicts the divergence even on a fixed distribution.

**(c) The loss falls partly mechanically.**
`bc_dagger.py:190-191` zeroes any label the student's mask makes illegal.
On student-damaged boards the time-indexed teacher increasingly names actions that are illegal
*there* -- harvest a crop that does not exist -- and those rows drop out of the per-head mean.
As beta falls, the scoreable population gets easier. Magnitude unverified.

> "The defect is not in the update; it's in the metrics. You have no argmax agreement, no mean
> log p(teacher action) on fresh states, and no per-head loss breakdown. Until you log those,
> 'collapsing' and 'transitioning' print identical numbers."

## 2. It will plateau short unless the time encoding is fixed

The target is by design a ~719-entry lookup keyed on `(step, branch)`.
The clock enters the network as two smooth scalars, `day/30` and `hour/24` (`jax_obs.py:309-310`).
The tape's action changes nearly every step, so the target is maximally high-frequency in a scalar
that moves 1/24 per step. Nets fit low frequencies first; this spends capacity manufacturing a
positional code that could be given for free.

On-tape the board is a strong time proxy, which is why BC-style fitting works at all.
**Off-tape -- precisely the states DAgger collects -- the board/time correlation breaks and the two
scalars are the only reliable key.**

## 3. Minimal fix, and it already exists in this codebase

- Append **one-hot hour [24] + one-hot day [30]** to `glob` in `jax_obs.encode` (~line 309), keep the
  smooth scalars, bump `GLOBAL_FEATURES` (line 49) from 60 to 114.
  One-hot over Fourier because memorisation is the stated intent and 54 floats are trivial.
- Load the warm start through `jax_policy.load_or_migrate`: the `widened_input` branch
  (`jax_policy.py:320-337`) zero-pads the grown rows of the `glob` input projection, so day-one
  behaviour is **bit-identical** and trained weights are untouched.
- **Trap:** `dagger_tape.py:342-351` hard-refuses a `global_features` mismatch on `--init` instead of
  routing through `load_or_migrate`; same for the resume check at `:376-381`. Five-line change.

### Also found: the shop-unlock state is not in the observation at all

Nothing in `jax_obs.encode` reads `unlock_day`/`unlock_shop`, and `adapter.state_from_obs` stubs them
to `NEVER`/0 (`adapter.py:166-167`).
The `q4_armed` predicate -- "yarn store unlocked", read day 5 -- is therefore **invisible to the
student** except through lagged town-drain effects on the inventory vector.
On the 4 fixed games this is confounded with game identity, so training looks fine; against a fresh
opponent at deployment it is an invisible failure mode.
Add the unlocked-shops bits to `glob` in the same migration.

## 4. Improvements ranked by expected value

1. **Time one-hots + unlocked-shops bits.** `jax_obs.encode` / `GLOBAL_FEATURES`; route
   `dagger_tape.py:339-352` through `P.load_or_migrate`.
   Converts the core problem from function approximation to table lookup, which is the stated
   intent. Highest EV by a wide margin.
2. **Instrumentation.** `dagger_tape.py:150-169`: argmax agreement, mean `log p(teacher action)` on
   fresh states, per-head loss (return an aux dict from `bc_dagger.loss_fn`).
   Near-zero cost; decides whether anything else on this list is needed. **Do this before touching
   training.**
3. **Gate beta on measured agreement, not the round index** (`dagger_tape.py:395-396`).
   390 scheduled rounds at beta=0 while op agreement is 0.16 is mostly wasted compute: far-off-tape
   states get tape labels that are frequently illegal or incoherent there.
   Hold beta >= ~0.9 until fresh-state argmax agreement clears a bar, then anneal.
4. **Loss structure** (`bc_dagger.py:171-203`).
   (i) The flat 1/8 average lets easy heads dominate the reported number -- the three `qty_*` heads
   are "predict 0" on the ~79% of turns with no trade, and their collapse is most of the 7x fall.
   Weight `op` and `bundle` up, or at minimum report per-head.
   (ii) Gate `crop`/`item`/`qty` by `active_unit_heads(labels["op"])`; the loss currently trains
   slices like `crop|WATER` that `sample`/`evaluate` (`jax_act.py:131-153`) never read.
   (iii) Gate `qty_*` by the bundle-activated products, matching how they are read at play
   (`jax_act.py:325-341`).
5. **Retire the anti-argmax rule at eval/deployment.**
   The comment at `dagger_tape.py:156-159` cites `neural.py` refusing argmax "because it destroys
   the joint"; that reasoning dates from the mean-field marginal era.
   With one joint `bundle` categorical and op-conditioned argument heads, per-head greedy along the
   autoregressive order is coherent.
   Over 719 compounding steps greedy vs sampling is the difference between `0.99^719 ~ 0.0007` and
   near-certainty of staying on tape.
   **This is our own CLAUDE.md lesson: "a decision to skip a fix can expire when the problem
   changes."**
6. **Reservoir stratification** (`dagger_tape.py:421-428`).
   The comment claims the reservoir protects round 0. **It does not** -- a uniform reservoir keeps
   round 0 at its *proportional* share, which after 400 rounds (1.15M turns seen, 60k cap) is ~150
   rows. Pin a protected block of pure-teacher rows per tape, or keep two reservoirs
   (teacher-driven / student-driven).
7. **lr / epochs.** 3e-4 on a warm start with ~6 minibatches in round 0 disturbs the checkpoint
   before refitting it. Lower to 1e-4 initially, or set a fixed grad-step budget per round.
   Lowest EV -- over 400 rounds the total steps are adequate.

## 5. Structural check on DAgger-then-KL-anchored-RL

Core shape is fine for the stated intent. Three real gaps.

- **The deployment distribution varies in exactly the axis training never does: the opponent.**
  All rollouts use the 4 recorded opponents, replayed (`dagger_tape.py:99-104`).
  The teacher ignores the opponent except for two latches, but the student sees 14 opponent-summary
  features plus `opp_money` (`jax_obs.py:234-244, 305-307`) and nothing stops it keying on them
  spuriously. The net must learn to *ignore* that block, and invariance needs input variation that
  is never supplied.
  Mitigation: opponent-feature dropout/randomisation, or occasional rollouts against pool opponents
  with the teacher still labelling.
- **The q4 branch variable is unobservable** (section 3). The four-way branch is the one closed-loop
  thing the student must replicate, and half of its input is missing from the features.
- **Speculation:** DAgger's value here is smaller than usual, because the teacher cannot teach
  recovery -- off-tape labels are "the tape's action anyway", which reinforces the time lookup but
  never a route back. Most of the algorithm's usual benefit is absent, and the beta~1 region is
  where nearly all the useful data lives. This strengthens item 3.
- **Housekeeping:** `CLAUDE.md:174` and `docs/kill_criteria_and_settled_positions.md` record the RL
  track as **PARKED** ("do not reopen RL without evidence that changes"). Step 2 reopens it.
  Reconcile the docs before a future session "corrects" the work back.

Latch stability under student damage is probably not a live risk -- shop unlocks are env-RNG
scheduled, not action-dependent (`jax_sim.py:36-38`), and the melon read is off a replayed opponent
-- but the melon count *can* drift if the shared market diverges before day 3 and the opponent's
buys fail. The per-episode latches column already printed is the watch; check it stays at the
recorded values as beta falls.

## 6. What we are about to waste days on

- **Reacting to the round-5 reading before instrumenting.** One sampled-agreement number cannot
  distinguish "collapsing" from "unlearning tetsuya en route to カワシギ".
- **The 390 beta=0 rounds as scheduled.** At ~194 s/round that is ~21 hours mostly spent labelling
  wrecked boards with tape actions the student cannot legally take.
- **Trusting the loss number.** It is 1/8-weighted toward heads whose modal answer is "0", and its
  population gets easier as labels go illegal. It is not a progress metric in this loop.
- **The reservoir comment's promise about round 0.** Wrong as written.

## Verdict on the engineering

> "**Opus Prime, and not marginally.** I went looking for the Spaghetti Monster and did not find it."

Cited as evidence: invariants enforced rather than narrated (atomic tmp+rename writes
`:213-229`, hard refusal on width mismatch `:339-352` `:376-381`, the float64 dtype guard `:329-331`,
`bundle_ok` as a required argument in `jax_act.py:56-72`); traps that are paid-for, cited and coded
(seat-1 `step` injection `tape_teacher.py:78-89`, `info.seed` `dagger_tape.py:73-79`, the opponent
private stub matching `neural.py:230`, `unit_live` gating); `tape_teacher.py` minimal with its one
hack fenced as best-effort and never-raises; and the refusal to port the teacher to array code
justified by a measurement rather than taste.

Three dings, none structural:

- the reservoir comment (`dagger_tape.py:418-420`) asserts a protection the maths does not deliver
- the agreement metric embeds the stale anti-argmax decision our own CLAUDE.md warns about
- `make_step` is re-invoked per round, recompiling `fit` for no functional reason (`:397`)
