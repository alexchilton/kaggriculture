# Fable's review of the whole picture, and what verified

**Date:** 2026-08-03, afternoon.
Requested after the learning-rate probe, to get a third read on a disagreement between two earlier
reviews.
Every load-bearing claim below was re-checked here against the live source; citations are to lines
opened, not to Fable's summary.

## The headline: nothing in this pipeline ever plays the competition

**Verified, and it is the largest gap on the board.**

- `grep -n arena scripts/train_jax_rl.py scripts/play_checkpoint.py` → **no matches.**
- `grep -n contrarian` in the same two files and all of `kagg/rl/` → only prose in comments and
  docstrings. `contrarian` is never played.
- `play_checkpoint.py:48-53` — `OPPONENTS` is `farm` / `carrot` / `ranch` / `idle`, the same
  JAX-native scripted family the trainer uses.
- `kagg.arena.evaluate` is used by `bench_arena.py`, `tune_converter.py`, `tune_shepherd.py`,
  `build_submission.py`, `search_plans.py`, `heuristic.py`, `rancher.py`, `contrarian.py`,
  `search/agent.py` — **every heuristic in the project, and no RL script.**

So the entire day-0-versus-curriculum argument is about whether the policy can learn anything against
four training-only opponents, and nobody has checked whether beating those correlates with beating
the field we are actually scored against.
`CLAUDE.md` already carries the rule this violates: *"Never tune or evaluate against `starter`
alone... Use `kagg.arena.evaluate` and the opponent pool."*

**It is cheap to close, which is the part that makes it urgent rather than merely true.**
The bridge is already built and already tested:

- `kagg/rl/adapter.py` rebuilds a `jax_sim.State` from the reference environment's nested dicts, and
  its own docstring names this exact gap — *"Without a bridge a trained checkpoint cannot be scored
  against `contrarian` and cannot be submitted, so it is the last structural gap between 'the loss
  went down' and 'it plays'."*
- `kagg/agents/neural.py:188-189` is a working arena-compatible agent built on that bridge.
- `tests/test_adapter.py` is the parity harness for it.

Every piece exists. Nothing connects them. A periodic off-the-hot-path eval of the current checkpoint
against `contrarian` / `heuristic` / `rancher` would say whether any of this compute is converging on
something that scores, independent of how every other question here resolves.

**In fairness to the trainer**, `train_jax_rl.py:345-346` explains why `contrarian` cannot be an
in-loop opponent: *"a Python heuristic cannot run inside a compiled scan, and the adapter bridges
dicts into a State, not out."*
That reasoning is sound and is about the **training loop**.
It does not apply to a periodic out-of-loop evaluation, which is what is missing.

## The binomial calculation nobody had run

Fable flagged that "0 wins in 278 games" was being read as a verdict without anyone computing what it
can actually rule out. Run here:

```
P(0 wins in n) = (1-p)^n <= 0.05   =>   n >= ln(0.05)/ln(1-p)

 true p   n needed    verdict at n=278
  0.20         14     ruled out
  0.10         29     ruled out
  0.05         59     ruled out
  0.02        149     ruled out
  0.01        299     NOT ruled out
  0.005       598     NOT ruled out
  0.001      2995     NOT ruled out
```

**0 wins in 278 games is still consistent with a true win rate as high as 1.07%.**
To push that ceiling to 0.30% takes 1,000 games; to 0.10% takes 3,000.

So the observation rules out "the policy is anywhere near competitive with the scripted farmer" —
which nobody claimed — and does **not** rule out the small-but-nonzero win rate that a
just-starting-to-learn policy would have.
Position A's central evidence does not carry the weight that was put on it.

## Corrections to my brief

1. **`money_med` is not an outcome, and I used it as one.**
   `HANDOFF_2026-08-03-evening.md` says so explicitly, and `train_jax_rl.py:551-559` carries the
   comment: it samples cash-on-hand wherever an unfinished episode happens to be when the update
   ends. **`bank_final_med` is the field**, it is already logged, and it was not quoted.

2. **I overstated the A/B tension.**
   Opus's actual text (`opus_review_2026-08-03.md:184-187`) is conditional and deferential — *"If
   step 1 says no gradient, the funded arm needs outcome variance... Note this reopens a decision the
   human made deliberately; it is theirs to take."*
   I relayed that as a forced binary. It is not one.

3. **`--horizon` defaults to 128** (`:1276`), not 32. Every launch on record passes `--horizon 32`
   explicitly, so the arithmetic is right, but "code default" language should not be conflated with
   "value actually run" — that distinction is doing real work elsewhere in the same brief
   (`--gamma-per-day`).

4. **The point-5 live-run numbers are unverifiable from the repo.** The probe and day-0 run logs are
   not synced locally; I read them off the box directly and never wrote them down. That is the
   project's own standing rule broken — write findings to a doc before relaying.

**What re-verified clean:** `seat_loss` at `:1094` unconditional at `--seat-coef` default 1.0
(`:1302`); `--gamma-per-day` default 0.97 at `:1286` with `gamma = gpd ** (1/TURNS_PER_DAY)` at
`:1544`; GAE trace zeroed on `done | trunc` (`:663`) and bootstrap cut only on `done` (`:659`), scan
length `horizon` (`:649`) — so the ~20-turn effective reach and the "critic carries credit for ~96%
of the episode" claim are arithmetically sound; `terminal_loss_shares` fed the squared GAE advantage
(`:2099-2100` against `:673`), retraction correct; `kl_fraction` returning 1.0 for the whole run at
`--kl-anneal 0` (`:942-950`, `:998-1019`); `--n-phases` genuinely live for a from-scratch run
(`warn_if_phases_inert` at `:117-132` only fires `if seeded`); the delta-V probe and P2b's harvester
both genuinely unbuilt.

## The gradient question, sharpened

Fable's reframing is better than the one I put to it.
"If reward does not vary there is no gradient" is too coarse, because the PPO policy gradient is
`advantage * grad log pi` and the advantage is a TD residual, not raw reward variance.

- The **critic** gets a live gradient the first time its estimate disagrees with a fixed outcome —
  which is exactly what a flat-band critic sharpening as `ev_signal` rises looks like.
- The **policy** gradient specifically needs some reachable action to change the outcome.

So Position A is defensible about **specific opponents** (farm/ranch/idle, if currently outside
reachable policy space) and not about **the training mix**, because `pool` is ~45% of the batch
(`fable_review_day0_launch_2026-08-03.md:43`) and is self-play against frozen past checkpoints, whose
outcome distribution is not structurally pinned the way a scripted opponent's is.

Fable does **not** find `draws_pool` falling and `ev_signal` rising sufficient on their own: per-update
`ev_signal` has sampling error of ~0.2–0.3 over ~22 terminal rows (`opus_review_2026-08-03.md:88-92`,
which recommended a cumulative version that was never built), and neither number is broken out by
opponent, so both could be entirely a pool-self-play effect.

A cheap discriminator it names, needing **no code change**: the three loss scalars are already logged
separately (`:1182`), so the share of `grad_norm` explained by `policy_loss` versus
`seat_loss` + `kl_prior` can be computed today from existing `log.jsonl`.
If essentially all of it is the regularisers, that is close to "no policy gradient".

## Recommendation: A versus B is not a binary

Fable's resolution, which I accept:

- Position B is right on measurement, and it is not a hypothesis — the deleted elite rungs taught a
  spurious day→wealth correlation, measured as `P(buy_land)` ramping to 0.48 by day 28 on a
  held-fixed poor board. Nobody, including Opus, argues for restoring them.
- Opus's actual proposal is a **seeded short-horizon** curriculum, which is nearer to P2b's spirit
  (short horizon-to-terminal without wealth-gifting) than to the deleted rungs.
- **Keep day-0 from-scratch as the funded primary arm** — it satisfies B and preserves the clean
  control. Treat P2b as the escalation if the gradient measurement says farm/ranch/idle are genuinely
  unreachable.
- `p2b_state_source_2026-08-03.md` shows P2b blocked against `league1` — but that is a fact about a
  stale off-policy checkpoint that loses 128/128, not about the current run, which may supply its own
  resume states within a modest number of further updates.

On its own earlier day-0-only argument Fable does not retract, and distinguishes: it was a claim about
*measurement* (you cannot diagnose behaviour at the true 0.14% terminal density in a regime 5–6× denser),
not a claim that day-0 should be the only thing ever funded. Running a labelled short-horizon arm
*alongside* the control is consistent with it; dropping the control is not.

## Ranked next actions, under the 10× thermal tax

1. **Fix the thermal throttling.** Not on the original list, and it dominates everything on it. 210–270
   MHz of a 2100 MHz boost at 88 °C is a ~10× tax on every item below. Repaste, clean intake,
   undervolt, or cap the power/boost target — a sustained lower clock can beat a
   boost-then-throttle-at-90-°C cycle on average throughput. Both prior reviews independently reached
   the same conclusion: a cooling fix is worth more than any hyperparameter here.
2. **The periodic arena eval against the real pool.** (My ranking, above Fable's #2 — Fable ranked the
   delta-V probe here and raised the arena gap only in "what's being missed". Every piece already
   exists and it is the only item that measures whether the compute is converging on something that
   scores.)
3. **The non-circular delta-V critic probe.** Cheapest of the ML options — one extra forward pass
   after `run_epochs`, read-only, resumes from the current checkpoint without perturbing training,
   following the pattern `terminal_loss_shares` already established ("trains bit-identically",
   `:966-967`). Settles whether P1 is a live drowned gradient or an artifact, and settles the
   value-clip question as a byproduct.
4. **Keep day-0 running at 3e-5** — but this needs no decision. The LR probe already earned its
   conclusion. Let it run; do not treat "more of the same" as today's action item, and do not kill it.
5. **P2b own-rollout resume states — last.** Blocked on two unresolved design questions, and its
   precondition (payoffs to harvest) is unconfirmed. Building it now risks exactly the "add a third
   mechanism before measuring why the first two are insufficient" mistake the critic-blindness doc
   exists to prevent.

## Also missing

Per-opponent breakdown exists for `win_rate` and `draws` (`wr_farm`, `draws_pool`, …) but **not** for
`bank_final_med`, and not for the loss-scalar decomposition. Both are cheap and both would sharpen the
gradient question past what the current field set can answer.
