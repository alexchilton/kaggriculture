# The tape clone's playout collapse: the first VISIBLE divergence is a step, and the probe is blind to the market

> **Read this first.** An earlier version of this file concluded "the failure is entirely movement".
> That was wrong, and the error is the one CLAUDE.md already records: a metric that is correct per row
> and reads as something wider than it is.
>
> `scripts/probe_where_the_replay_goes_wrong.py:117-120` compares `labels["op"][u]` and nothing else.
> **The `wrong` columns below count UNIT OPS only** -- not the market bundle, not the op arguments
> (crop, item, quantity). `OFF-TAPE wrong 0` on days 0-2 says the unit ops matched. The market orders
> could have been wrong on all 72 of those turns and the column would still read 0.
>
> So the first divergence the probe can SEE is a step at turn 78. It cannot rule out that the market
> head diverged from turn 0 and caused it. The duel evidence points that way: the net banks exactly
> $0 or $50, and a policy with sound unit ops still farms and sells something.
>
> What is measured: op agreement is near-perfect, and the playout collapses. What is NOT measured:
> which head is responsible.


Measured 2026-08-27 on `LAPTOP-local` (this Mac), `data/logs/round27_control.log`, via
`scripts/probe_where_the_replay_goes_wrong.py --run data/dagger_tape/season_fast-20260822-235031
--horizon 719 --show 4`.
The probe reads `latest.pkl`, which is **round 28**, not the `pinned_round27.pkl` the earlier write-up
pinned.

## The result

Two columns, same weights. ON-TAPE the teacher drives and the student is only scored, so a
disagreement is pure model error. OFF-TAPE the student drives.

    92498144   day            0    1    2    3    4    5  ...  12   13  ...  29
               ON-TAPE  wrong 0    0    0    0    0    0        1    1        0
               OFF-TAPE wrong 0    0    0   18   23   16       23   19       17
               bank: on-tape 150,255   off-tape 214

    91907974   day            0    1    2    3    4    5  ...  17  ...  25   29
               ON-TAPE  wrong 0    0    0    0    0    0        1        1     0
               OFF-TAPE wrong 0    0    0   18   23   16       23       23    11
               bank: on-tape 88,882    off-tape 291

**The op knowledge is near-perfect: two wrong ops in 719 turns on the first tape, three on the
second.** What destroys the playout is a wrong STEP.

## Both tapes break on the same turn

    92498144  turn 78 day 3 h 6 unit 0 at (4,3): teacher WEST   net NORTH
              turn 79 day 3 h 7 unit 0 at (4,2): teacher FEED   net EAST
              turn 80 day 3 h 8 unit 0 at (5,2): teacher CARE   net WEST
              turn 81 day 3 h 9 unit 0 at (4,2): teacher SOUTH  net EAST

    91907974  turn 78 day 3 h 6 unit 0 at (4,3): teacher WEST   net EAST
              turn 79 day 3 h 7 unit 0 at (5,3): teacher FEED   net WEST
              turn 80 day 3 h 8 unit 0 at (4,3): teacher CARE   net EAST
              turn 81 day 3 h 9 unit 0 at (5,3): teacher SOUTH  net WEST

Turn 78, day 3, hour 6, unit 0, standing on (4,3), on both tapes. That is a specific state, not
drift. After it the unit is on the wrong tile, so every job the teacher does there reads as a move,
and on `91907974` the net ping-pongs (4,3)<->(5,3) for the rest of the season. 23 wrong slots a day
is close to every unit, every hour, for 26 days.

## On a foreign board it never starts

`scripts/duel_net_vs_tape.py --seeds 8`, `pinned_round27.pkl` with its correct 149-bundle vocabulary,
against the Crop Dusta tape clone. `data/logs/net_vs_tape_v2.log`.

    seed  round27_net  dusta_clone_land        delta
    9000            0          148,625     -148,625
    9001           50          163,525     -163,475
    9002            0          125,758     -125,758
    9003           50          151,057     -151,007
    9004            0           74,616      -74,616
    9005           50          141,070     -141,020
    9006            0           96,047      -96,047
    9007           50          157,677     -157,627

    round27_net 0, dusta_clone_land 8, draws 0 of 8.  mean delta -132,272

**Four different seeds at seat 0 all bank exactly $0; four different seeds at seat 1 all bank exactly
$50.** The final bank does not vary with the seed at all, only with the seat. Whatever the net is
conditioning on, it is not the board.

That is consistent with the probe: it is already broken at turn 78 on its OWN board, so a foreign
board never gets a chance to be the explanation.

Worst turn is 138-252 ms after JIT warm-up (2,301 ms on the first turn of the process), against the
1,000 ms limit. Speed is not the problem.

## This corrects `the_clone_only_misses_the_unlearnable_digs_2026-08-23.md`

That document says the clone's only remaining error is DIG. **That is true of the ON-TAPE column
only.** The first DIG error is at turn 297 (`92498144`) and turn 430 (`91907974`). The playout has
already been broken since turn 78 — 219 and 352 turns earlier.

Its per-tape table also attributed the size of each loss to what the net substituted for DIG. The
substitution that matters is the one at turn 78, and it is a step.

## What this says about the fix

Alex's call, 2026-08-27: give movement to the planner.

The measurement supports it directly. The failure lives entirely in the half of the action space
that would be removed. `docs/dusta_clone_results_2026-08-27.md` argued the same split from the other
end -- a wrong step is LEGAL, so masking cannot catch it, and one wrong step puts a unit out of
position for a routed day.

What it does NOT promise:

- `92466371` collapsed to $372 in the 2026-08-23 run while substituting PLANT, which leaves the hand
  where it is. Displacement is not the whole story there and the cause is still unidentified.
- The composition is not "net picks this turn's op, router walks one step". `cover.cover` plans a
  WHOLE DAY at hour 0 and never replans. Feeding it a per-turn head means changing what the net is
  asked for: a day's JOB LIST keyed on tiles, not an op keyed on the unit standing somewhere.

## Round 28 is not round 27

`pinned_round27.pkl` was pinned deliberately. `latest.pkl` is round 28 and is what the probe reads by
default. The numbers above are round 28. Anything quoting the 2026-08-23 figures is quoting round 27
and the two must not be mixed.

## The vocabulary trap, hit again today

`pinned_round27.pkl` embeds no bundle list, so `neural.make_agent` falls back to
`data/il/bundle_vocab.json` -- 197 bundles -- while the checkpoint records `vocab_size = 149`. Its own
`vocab_path` names `bundle_vocab_teacher.json`, which now holds **151**: it was topped up at 12:56 on
2026-08-23, after the round-27 pin was written at 10:02. `Vocabulary.from_bundles` sorts, so two
added bundles move every index above them.

The only 149-bundle file on disk is `data/il/bundle_vocab_teacher_pre_topup.json`.

Run with the wrong one and the net emits six SELL orders into an empty shed on turn 0 and banks $0 --
which reads exactly like a policy that cannot play. `scripts/duel_net_vs_tape.py` now asserts the
bundle count against the checkpoint before it will start.
