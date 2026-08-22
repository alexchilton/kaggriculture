# DAgger from the shipped agent — the teacher is a call, not a dataset

Written 2026-08-22.
Measured on this Mac, `.venv`, tape `(True, False)` = `92466371.json`, seed 70683142, `weedSpawnChance = 0.0`.

## The instruction

> "why dataset — because it needs to not be bc but teacher per step per turn.
> dataset would just be like passing in the tapes of kawa"

Correct, and it is the whole design.
A recorded trajectory is behaviour cloning on カワシギ's tapes, which was already tried and was not
good enough.
DAgger requires the teacher to answer **at whatever state the student wandered into**, so the
labels land on the student's own state distribution rather than the teacher's.

The teacher is therefore `agent(obs) -> action`, callable per turn, not a file.

## What the teacher is

`SA.make_agent(plan, seat, router=True)` — the agent running the carrot sweep, unmodified.

It is **not** open-loop, and that matters for DAgger.
The tape lookup is time-indexed, but the branch that *chooses* the tape is read off the board:

| latch | read on | predicate | source |
| --- | --- | --- | --- |
| `melon_armed` | day 3 | opponent holds >= 9 MELON tiles | `melon_branch.py:215` |
| `q4_armed` | day 5 | the yarn store is already unlocked | `q4_branch.py:242` |

`Branch.arm` (`branch.py:78`) decides once and latches.
The species relabel (`_herd_split`, `schedule_agent.py:2929`) reads `unlocked_shops` and so also
moves with the board.

So the closed-loop part of the teacher responds to the student's rollout, and the time-indexed part
supplies the recovery action for the turn the student is on.
That is the honest statement of what this teacher can and cannot teach: **it cannot re-plan a
route around a board the student has damaged.** It answers "at turn t, on this branch, do X".
With a fixed start state and weeds off, the student's states stay near the tape, which is the
condition that makes this workable — and it is the user's own reason for `weed = 0` first.

## Two designs, and why the second one loses

**(a) Call the real agent per step.** Teacher stays byte-identical to what ships.

**(b) Port the teacher to array code** so it runs inside `bc_dagger.py`'s `lax.scan`.
Tempting, because the tape *is* a table: `TAPE[key][step]` is a static gather, and both latches are
one array comparison each.
**Rejected on a measurement, not a preference** — see below. It would be a second implementation of
the agent that has to agree with the first one forever.
`kagg/rl/adapter.py`'s own docstring rejects the identical shortcut for the identical reason:
"That creates two encoders which must agree forever, and they will not."

## The measurement that decided it

`scratchpad/time_loop.py`, 240 turns of the real season:

```
  teacher     2.08 ms/turn      the shipped agent, on the dict obs
  step        1.14 ms/turn      reference env
  adapt       0.86 ms/turn      adapter.state_from_obs -- ran clean, no error
  encode     12.89 ms/turn      jax_obs.encode        <-- the bottleneck
  TOTAL      16.97 ms/turn
```

The teacher is **not** the cost. The unjitted encoder is, by 6x.

`scratchpad/time_teacher.py` over the full 719 turns gives a teacher mean of **17.90 ms**, higher
than the 2.08 ms above because the planner gets dearer as the board fills.
Taking the full-season figure, the loop is ~33 ms/turn, so 8 rounds x 64 episodes x 719 turns is
**~3.3 h single-core** — and 12.9 ms of that is `jax.jit` away.

Porting the agent to array code would buy back a couple of hours and cost a second codebase.
Not worth it.

## The loop, and why it needs no new bridge

Roll out in the **reference environment**, because that is the only place the dict obs the teacher
reads and the state the student encodes both exist:

| step | what runs | already exists |
| --- | --- | --- |
| obs | reference env dict observation | yes |
| teacher label | shipped agent called on that dict obs | yes — no port |
| student features | `jax_obs.encode(adapter.state_from_obs(obs, privates))` | yes — the same encoder training uses |
| action taken | beta-mix: teacher with prob beta, else student | new |
| label encoding | `replays.encode_action` + `market_bundles.bundle_of` | yes |

Note the direction. `adapter.state_from_obs` goes dict -> `State`, which is the way we need.
The opposite bridge (`State` -> dict, to keep `bc_dagger.py`'s batched scan) **does not exist** and
would be new code on the critical path. Rolling out in the reference env avoids writing it.

## Two traps already paid for, both live here

- **Seat 1 has no `step`.** `kaggle-environments` populates it only for seat 0. An agent seated
  second reads `step=0` every turn and replays turn 0 all season. Inject it:
  `obs["step"] = day * 24 + hour`. Tape `(True, True)` is a seat-1 recording.
- **`configuration.seed` is None; the real seed is `info.seed`.** Reading it from configuration
  leaves `env.reset()` drawing a fresh town. Two runs of the verifier disagreed by 499 turns on one
  tape before this was fixed.

## The vocabulary gap does not exist — measured, and it corrects an earlier note

An earlier note in this session recorded "584 market bundles on the tapes against a 128-class head",
and made a vocab rebuild a prerequisite. **Both numbers were wrong.**
Measured with `market_bundles.bundle_of` over all four recordings:

```
tape                     turns   distinct bundles
(False, False)  92498144   719         74
(False, True)   91907974   719         88
(True, False)   92466371   719         73
(True, True)    91906088   719         75
UNION over the four tapes:             148

head width       N_BUNDLES = 256       jax_policy.py:92, not 128
existing vocab   197 entries           data/il/bundle_vocab.json
coverage         2876/2876 tape turns  100.000%, 0 missing bundles
```

The head is 256 wide, the shipped 197-entry vocabulary already contains every bundle the four tapes
emit, and nothing needs rebuilding. `Vocabulary.coverage` is the command that settles this; re-run
it rather than trusting the number here if the teacher changes.

## Everything the loop needs already exists

| need | supplied by | status |
| --- | --- | --- |
| teacher, queryable per turn | `kagg/il/tape_teacher.py` | written, tested |
| dict action -> head labels | `replays.encode_action` | returns exactly `jax_act.ALL_HEADS` |
| dict obs -> student features | `adapter.state_from_obs` + `jax_obs.encode` | exists |
| market vocabulary | `data/il/bundle_vocab.json` | covers the tapes 100% |
| loss / optimiser step | `bc_dagger.make_step` returns `rollout, fit` separately | reuse `fit` |

Only the rollout is new: a Python loop over the reference env that fills the same `batch_data`
dict the jitted `fit` already consumes -- `obs`, `masks`, `labels`, `unit_live`.

Two things to get right in it, both visible in `bc_dagger.py`'s own rollout:

- The jitted rollout plays **both seats** (`batch * 2`) in self-play. The tape teacher labels our
  seat only, so either the opponent seat gets its own teacher instance or its rows are excluded.
- `unit_live` exists because `MAX_UNITS` is 24 against a crew of a few, so scoring dead slots makes
  ~85% of the loss a constant. That padding mistake has been made three times here, once in this
  very loss.

## Second pass, after Fable's review

Full review: `docs/fable_dagger_review_2026-08-22.md`. What changed, and why.

**The observation now carries the clock and the open shops.** `glob` went 60 -> 122: one-hot hour
[24], one-hot day [30], one bit per unlocked shop [8].
The teacher is a ~719-entry lookup keyed on the turn, and the clock used to arrive as two smooth
scalars; a net fits low frequencies first, so that spent capacity manufacturing a positional code.
On-tape the board proxies for the turn, which is why plain BC fit at all; off-tape -- where DAgger
collects -- it does not.
The shop bits close a hole nobody had noticed: `q4_branch` picks the tape on "is the yarn store
unlocked", `adapter.state_from_obs` stubbed the unlock schedule to NEVER, and so that input was
**invisible to the student on the only path this loop uses**.
Old checkpoints load through `jax_policy.load_or_migrate`, which zero-pads the new columns, so
day-one behaviour is bit-identical. Pinned by
`tests/test_the_observation_carries_the_clock_and_the_open_shops.py`.

**Agreement is measured on both decodes.** Sampled and greedy, for `op`, `bundle`, and `bundle`
restricted to turns the teacher trades. First measurement, 80 turns from the warm start:
greedy 0.5932 / 0.7000 against sampled 0.5559 / 0.5875 -- greedy is ahead on every column, which is
the evidence needed to revisit the anti-argmax rule at deployment.

**Fresh-state loss is reported separately from the aggregate loss.** The aggregate is dominated by
earlier rounds, so a loss falling on data already fitted says nothing. Measured together for the
first time: fresh 1.9711 against aggregate 1.5974.

**Per-head loss is reported.** It immediately showed `qty_sell` at 7.85 against every other head
under 2.4, which a 1/8-weighted average had been hiding.

**The loss now gates conditional heads and weights the decisions.** `crop`/`item`/`qty` are scored
only for the op that reads them (`jax_act.active_unit_heads`), `qty_*` only for the products the
chosen bundle names, and `op`/`bundle` carry weight 3.0 in one `HEAD_WEIGHTS` block.
~79% of turns place no order, so the three `qty_*` heads were mostly "predict zero" and dominated
any fall in the reported number.

**Beta anneals when it is earned, not on a schedule.** The teacher keeps driving until greedy `op`
agreement on fresh states clears `--anneal-after-agree` (0.80). The previous run spent rounds 10+
at agreement 0.17, labelling wrecked boards with a time-indexed teacher whose answer there is
frequently illegal and never a route back.

**The reservoir is two pools.** The old comment claimed a uniform reservoir protected round 0's
tape states. **It did not**: a uniform reservoir keeps every round at its proportional share, so
after 400 rounds round 0 survives as ~150 rows of 60,000. Teacher-driven turns now have their own
protected pool (`--expert-cap`).

**`make_step` is built once**, not per round; it was recompiling `fit` every round for nothing.

### Not done, and why

Fable suggested opponent-feature dropout so the student learns to ignore the opponent block.
**Declined: it would break the melon latch.** `melon_armed` reads the opponent's MELON tile count,
and the opponent block is `N_KINDS + N_CROPS + N_ANIMAL_KINDS` -- the opponent's crop counts are
exactly the signal being dropped. The concern behind the suggestion is real, but the fix is
opponent *variation* (rollouts against pool opponents, teacher still labelling), which is a change
to the training setup rather than a feature toggle.

### Observed, not yet addressed

**The latches drift off-tape.** In the killed run, at beta=0, `92466371` (the `(True, False)`
recording) armed `(True, True)` and `91906088` (the `(True, True)` recording) armed `(True, False)`.
The student damages the shared market before day 3, the opponent's melon buys fail, and the day-3
melon read flips. So a far-off-tape rollout is not merely hard, it is replaying a different tape
than the board was recorded under. This is another argument for keeping beta high until agreement
is earned.

## Still open

No KL anchor exists — both `kagg/il/bc.py:151` and `scripts/bc_dagger.py:30` say so. That is what
"kl stays low, no change" needs, and it is a later step than this one.
