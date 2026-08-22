# On the fixed two-day opening, the net reproduces the market bundle stream and drifts 22% on routing

> ## SUPERSEDED the same evening. The 22% is an artifact of four defects, not a routing result.
>
> Everything below was measured before `0f27ae8`, `d23fc85` and `5ee1044`. Four defects were live,
> all in `kagg/rl`, all invisible to the 300-episode parity gate:
>
> | | defect | teacher labels made unlearnable |
> |---|---|---|
> | `0f27ae8` | movement onto a LOCKED tile forbidden | 259 |
> | `d23fc85` | shed ops from a LOCKED tile forbidden | 29 |
> | `d23fc85` | `COMMIT_PICKUP` could target only `(4,4)` | -- |
> | `5ee1044` | seat-1 clock frozen at day 0 all season | 300 |
>
> **595 of 27,652 unit labels (2.15%) were unemittable via `_masked_logits` and zero-weighted by
> `bc.py:232`.** A hand spawning at `(5,5)` had no legal move and stood still for the whole season,
> and the tape's next 700 labels assume it walked. The `op ~0.78` rows below are that hand
> compounding, not a measurement of routing capability.
>
> The seat-1 exception singled out below (`91906088` at bundle 0.9792 / traded 0.8000) is the clock
> bug, not a latch effect: `kaggle_environments` gives `step` to seat 0 only, so that tape ran all
> 720 turns as day 0.
>
> After the fixes, on d0-d4, the same probe reaches **`greedy op 1.0000 bundle 1.0000 traded 1.0000`
> at rounds 19 and 20**, against a hard ceiling of `0.9968 / 0.9979` for the run with the clock bug
> still in. `probe_teacher_labels_the_mask_forbids.py` now reports 7 forbidden labels of 27,652, all
> DIG on EMPTY, which the reference genuinely no-ops.
>
> **One further reason not to quote the `bank` column below.** The probe drives with the *sampled*
> decode, and the shipped agent (`neural.py:255`, inside `make_agent`) argmaxes. Those are different
> policies. Every playout bank recorded here and in that evening's logs measured one we do not ship.
>
> Kept as the record of what was believed and why. Do not cite the numbers.

**Read the three limits in "What this does NOT say" before quoting the headline.** An earlier
version of this file said "the market is solved", which overran the evidence in three ways and put
the overclaim above its own corrections.

Measured 2026-08-22 on `data/dagger_tape/d01seq-20260822-200645/latest.pkl`, round 34, d_model 128 /
4 heads / 3 layers, 957,903 parameters, vocabulary `data/il/bundle_vocab_teacher.json`.

Probe: `run_episode(..., beta=0.0, horizon=48)` -- the student drives every turn, alone, and its
action is compared to the teacher's label at the state it is standing in.

    STUDENT DRIVING ALONE (beta = 0.0), 48 turns
    tape                     op   bundle   traded   bank
    92498144.json        0.7853   1.0000   1.0000   16
    91907974.json        0.7607   1.0000   1.0000   19
    92466371.json        0.7791   1.0000   1.0000   24
    91906088.json        0.7784   0.9792   0.8000   20

## What this says

**The market bundle stream is reproduced turn-for-turn on this window.** Three of the four rows are
exact on the bundle -- which op and which item goes out each turn, with the net driving, for 48
turns. `91906088` is the exception at 0.9792 / 0.8000; it is the only seat-1 tape and the only
`(True,True)` latch combination.

## What this does NOT say

Three limits, each of which the headline above used to overrun:

1. **Quantities are not in this measurement.** `market_bundles.py` states it: *"Quantities are
   deliberately not part of the identity"* -- 52 of 116 non-empty bundles carry more than one
   quantity vector. `run_episode` scores the bundle ID, not the `qty_*` heads. So this is exact at
   op/item/multiset granularity, and the SELL quantities are corroborated only by the day-level
   bank -- the outcome-level evidence this same document disqualifies below. Milder than the
   "bank 16/16" error, same family.
2. **The four rows are ONE tape against four opponents, not four tapes.** The teacher's actions are
   byte-identical across all four games over these 48 turns (below). Three exact rows are a
   robustness check across opponent-perturbed states, not three independent successes.
3. **48 turns is the fixed trunk, where the market requires no decision.** The tapes do not fork
   until turn 72 (`tape_tree.log`) and the first shop lands at d3. Every branch-dependent market
   decision -- the melon latch, q4 -- is outside this window. The market head is being measured
   where its correct output is a constant.

So the supportable claim is the title: on the fixed two-day opening the bundle stream is reproduced
turn-for-turn, and routing drifts 22%. Whether the market head can DECIDE, rather than replay, is
untested and needs horizon >= 72.

**The routing is not.** ~22% of unit ops differ, consistently across all four tapes. On the
TEACHER's board (beta 1.0) the same checkpoint scores 1.000 on every op except `WEST 0.960/100`. The
gap between 0.96-on-tape and 0.78-driving is compounding: one wrong step puts a hand on the wrong
tile and every later op is judged against a board that no longer matches.

## Two readings this replaces

**"The playout is exact, it sticks."** Wrong. The playout prints bank and tiles at day granularity,
and `bank o/t 16/16` held for eight consecutive rounds while the action sequence was 22% different.
Two action sequences reached the same bank. An outcome match is not a trajectory match, and quoting
one as the other is the same error as reading an aggregate for a replay.

**"One tape converged, three are thrashing."** Wrong. All four sit at 0.76-0.79. The round-to-round
bank swings were an unconverged unit-op policy, not evidence that three tapes were unlearned.

Also corrected during the same session:

- **d0-d1 is ONE tape, not four.** Teacher actions over the first 48 turns are byte-identical across
  all four games -- 0 of 48 turns differ. The banks differ only because the opponents contest the
  market differently. Alex called this; the probe confirmed it.
- **The tapes fork at turn 72 (day 3)** into exactly two groups by the melon latch. Measured.
  The pairs that differ in the q4 latch first diverge at turn 120 (day 5), but Alex reports the q4
  branch itself only shows at d12 -- so turn 120 is animals and other game-to-game difference, not
  q4. The attribution was mine and it was an inference, not a measurement.
- **The anneal is not the problem.** It degrades the ROLLOUT agreement statistic (0.99 -> 0.71) and
  leaves the PLAYOUT untouched. The playout is hardcoded to `beta=0.0` at `dagger_tape.py:917` and
  never inherits the training beta. Steering by the rollout number was the error.

## The question this raises

`kagg/search/router.py` already solves the day as a Team Orienteering Problem and re-derives each
stop's ops from the live board. The net is being asked to imitate, from examples, the output of an
exact solver the project already owns -- and that is the only part it fails at. The part it adds,
the joint market decision, is at 1.0000.

Open, for Alex: is imitating the router the goal, or is the net's job the market and the branch
decisions with the router kept as a solver?
