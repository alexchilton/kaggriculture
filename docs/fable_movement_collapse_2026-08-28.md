# Why the student never walks — findings, 2026-08-28

Verdict first: **this is not a collapse and not a plumbing bug. The gradient reaches the movement
labels and is measurably moving them. The exact 0.000 is the greedy argmax sitting on top of a
near-uniform op head that has taken ~56 gradient steps from a cold start, on a target whose
probability mass is split nine ways.**
Also: **the run is dead — it crashed with `SystemExit` at the end of round 1** (5 planner turns not
expressible in `data/il/bundle_vocab_planner.json`; `data/logs/box_launch3.log`, `EXIT=1` at
17:23:25 CEST). Nothing trains until the vocabulary is rebuilt.

## What was read

- `scripts/dagger_tape.py` (whole file; labels 291-292, day0 repeat 944-949, vocab refusal 984-989)
- `scripts/bc_dagger.py:100-272` (`make_step`, `loss_fn` 206-254, `HEAD_WEIGHTS` 123)
- `kagg/il/replays.py` (whole file; `fold_illegal_ops_to_noop` 47-79, `encode_action_legal` 88-97)
- `kagg/rl/jax_masks.py` (whole file; movement bounds-only 109-121, commit tokens appended 138-144)
- `kagg/rl/jax_obs.py` (whole file; `_target` 259-275, clock one-hots 52-63, unit block 318-331)
- `kagg/rl/jax_policy.py` (whole file; unit slot embedding 192, zero-init heads 204-206)
- `kagg/rl/jax_act.py` (whole file; `active_unit_heads` 132-154, `_score` 219-245)
- `kagg/rl/commit.py` (whole file; `resolve` 243-331, `_step_toward` 228-240)
- `kagg/rl/adapter.py:275-312` (unit ordering: farmer first, then hands — matches the label order)
- `scripts/what_does_the_student_say_where_the_teacher_walks.py`
- Checkpoint `data/backup_weights/planner-20260828-014128_latest.pkl` (args unpickled and read)
- `data/dagger_tape/tape-v2/aggregate.pkl` (label census)
- `data/logs/box_launch3.log`, `data/logs/student_vs_teacher_ops.log`

## The state of the run, from the checkpoint itself

`planner-20260828-014128_latest.pkl` args: `round: 1`, `init: None` (**cold start** — the earlier
0.978-op result was a warm-started tape-teacher run), `epochs: 1`, `seen_total: 23008`, aggregate
`n 11504` (16 deterministic episodes dedup to the same 11,504 expert rows every round).
One epoch is 11,504 rows + 7x384 day-0 repeats = ~14,200 rows = **28 batches of 512**.
Two rounds = **~56 Adam steps at lr 1e-4 on a zero-init 966k-param net**.
Then the `bundle_miss` guard at `dagger_tape.py:984` killed the process.
"Flat across two rounds" is rounds 0 -> 1; there was no round 2.

## New measurement: where the mass actually is

Ran this session (`.venv`, script in scratchpad `move_mass.py`), checkpoint above, planner teacher
driving, seed 9000, 240 turns, **509 movement-labelled unit-turns**, full masked softmax per slot:

```
mean p(any of N/S/E/W)   0.4303
mean p(commit tokens)    0.2099
mean p(teacher's dir)    0.1209   (uniform over 23 = 0.0435; masked-uniform = 0.0916)
mean p(argmax winner)    0.1819
mean legal ops           10.9
mean entropy             2.251 nats (uniform over 11 legal = 2.391)
teacher-direction rank   median 4 of ~11 legal (p10 2, p90 6)
```

Caveat: my probe's opponent PASSes, so the board drifts slightly from the training rollouts;
these are class-conditional masses, not agreement numbers, and that drift does not change the shape.

Read it: on a walking turn the student already puts **64% of its mass on "go somewhere"**
(moves + commit tokens), and the teacher's own direction carries **2.8x uniform** after ~56 steps.
The gradient is arriving and working.
But entropy is still within 0.14 nats of uniform, the argmax winner holds only 0.18, and the
walking mass is split across **nine classes** (4 moves + 5 commit tokens) while PASS keeps its
mass in one class.
So no single direction ever beats PASS/WATER under argmax, and greedy movement reads exactly 0.000
— which is what *partial* learning of a split class looks like under argmax, not what "unreachable"
looks like.

## Q1: why stationary ops and never movement

Three mechanisms, all mundane, compounding:

1. **The mask does most of the work for the ops it emits.** WATER is legal only on a dry plant
   underfoot (`jax_masks.py:122`), FEED only on a hungry animal with wheat in hand (:130).
   On those turns the legal set is small and the tile-underfoot features are decisive, so
   "if legal, do it" is learnable in a handful of steps and wins the argmax immediately.
   Movement is bounds-only legal (:109-121), so the mask contributes nothing, ~11 ops are legal
   (measured above), and the correct answer depends on planner-internal route assignment.
   The observed split — emits rare-legality ops, never emits always-legal ops — is exactly the
   order masked cross-entropy learns things in, early.
2. **The walking mass is split 9 ways; PASS is not.** Even a perfectly fitted conditional emits
   zero moves under argmax whenever p(direction | obs) is spread. This is the same
   argmax-of-marginals failure the project already paid for twice ("nine independent 'probably not
   sell' decisions compose into 'never sell'", CLAUDE.md).
3. **~56 gradient steps.** The greedy/sample gap in the round table (greedy op 0.4685 vs sample op
   0.1698) is itself the tell that every head is still near-uniform.

The movement labels are half the data: census over `tape-v2/aggregate.pkl` (60,000 rows, 576,545
live labels): WEST 14.6%, NORTH 13.7%, EAST 12.3%, SOUTH 9.8% = **50.4% movement**;
WATER 13.4%, PASS 8.5%.
Overall greedy 0.4685 with movement at zero means it is close to nailing everything that is not a
walk — consistent with mechanism 1.

## Q2: does the loss reach the movement labels — yes, verified two ways

Code path: `encode_action_legal` (`replays.py:88-97`) folds only mask-illegal labels to NOOP, and
movement is bounds-legal, so walks survive labelling.
In `bc_dagger.loss_fn` the only zeroings are: mask-illegal labels (:226-228, moves are legal),
dead unit slots (:234), the `active` gate which touches only `crop`/`item`/`qty` (:235-236 via
`active_unit_heads`, `jax_act.py:147-154` — `op` is all-ones), and `class_w` which touches only
`bundle` (:237-248). `HEAD_WEIGHTS` gives op 3.0 (:123). Nothing skips movement.
Measured: p(teacher's direction) = 0.121 = 2.8x uniform after 56 steps.
A zeroed gradient cannot produce that.
"Loss falls while agreement is flat" is exactly what mass moving toward the right class without
crossing the argmax threshold looks like.

## Q3: fixes, ranked, each with the mechanism and the cheap check

1. **Rebuild `bundle_vocab_planner.json` over all 16 (tape x seed) combinations.**
   Mechanism: the planner on fresh seeds emits bundles the 4-recorded-game vocabulary lacks, and
   `dagger_tape.py:984` correctly refuses to train on them; the run is dead at round 1.
   Check: the run reaches round 2. Cost: `scripts/build_teacher_bundle_vocab.py` + minutes.
2. **Train it before diagnosing it further.** This is 56 steps from zero-init; the diagnosis
   "collapsed" is premature by construction.
   Decisive 10-minute check, no rollout needed: load `latest.pkl` and the frozen 11,504-row
   aggregate, run the existing `fit` for ~50 epochs on the box GPU, print the per-op movement
   agreement every 10 epochs.
   Confirm: WEST/NORTH leave 0.000 and p(teacher dir) climbs (the clock one-hots
   `jax_obs.py:52-63`, the unit slot embedding `jax_policy.py:192` and episode-identifying prices
   make the 16 fixed trajectories memorizable, and the warm-started tape-teacher run demonstrably
   fitted movement with this same architecture).
   Kill: movement stays at 0.000 while loss falls for 50 epochs — then something structural is
   left, go to 4. In the live run: raise `--epochs` (e.g. 8); one epoch per round is the real
   reason two rounds taught almost nothing.
3. **Stop the five commit tokens acting as unlabelled distractors.** They are legal on essentially
   every walking turn (`jax_masks.py:141`), are never the label (the teacher emits primitives), and
   hold a measured **0.21 mean mass** there — zero-init keeps them near-uniform and the loss only
   pushes them down through the softmax normalisation.
   They raise the bar the correct direction has to clear by ~5 extra classes.
   Either give them labels (fix 4) or, for this BC phase, drop them from the op mask — that is a
   statement about the label space (the teacher cannot emit them), not a quality judgment, but it
   is a mask change and Alex's call.
   Check: re-run the mass probe with commits masked; walking mass re-concentrates over 4 classes.
4. **The structural fix, if 2's kill-branch fires or once off-tape generalization matters:
   relabel the teacher's walks as commitments.** At the first turn of each walk, label
   `COMMIT_<arrival op>`; weight the intermediate walk turns to zero in the op loss (the `decided`
   machinery in `jax_act._score:237-238` is exactly this); execute with `commit.resolve`.
   Mechanism, named: per-step direction is a function of the planner's internal assignment, which
   is not in the observation, so p(direction | obs) is irreducibly multimodal off the memorized
   towns; "walk to a job of kind X" IS in the observation — the four `_target` features
   (`jax_obs.py:259-275`) literally encode it — and it is one class per decision instead of a
   9-way split.
   Caveats to measure, not assume: `resolve` walks to the *nearest* candidate
   (`commit.py:280-296`), not the planner's assigned tile, and two units committing the same kind
   converge on one tile — so judge by playout bank, never by op agreement.
   Cheap pre-check: over one teacher season, count how often the realized walk endpoint is the
   nearest candidate of its arrival-op kind; if it is high (say >80%) the semantics gap is small.

## Q4: is the framing wrong

Half.
For *reproducing the teacher on the 16 fixed towns*, the per-turn primitive classifier is fine:
the trajectories are deterministic and the obs identifies (episode, day, hour, slot), so BC can
memorize the routes — fixes 1-2 should get there and are cheap.
For *anything off those towns* — fresh seeds, or the moment beta anneals and the student deviates —
memorized directions are a lookup table keyed on states that no longer occur, while the stationary
ops still transfer because the mask and tile features carry them.
That is when the movement gap will reopen, and the commit-token relabel (fix 4) is the target that
generalizes, because it asks for a decision the observation can support.
Do not start with 4: the current evidence shows a crashed, barely-trained run, not a failed
architecture.

## One loose thread

`student_vs_teacher_ops.log` shows the student answering CARE on 47% of teacher-PICKUP turns.
PICKUP happens on shed-access tiles; CARE requires an animal underfoot.
That is only consistent if the plan builds a pasture on a shed-access tile (buildable: (4,4) starts
EMPTY) — plausible, unverified.
If a pasture is *not* there, greedy is emitting a masked op and the probe has a mask/state
misalignment; one command settles it (print `t.kind`/`t.animal` at the four shed tiles on a
PICKUP turn).
