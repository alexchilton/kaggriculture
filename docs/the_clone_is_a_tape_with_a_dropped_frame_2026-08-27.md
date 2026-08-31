# The clone makes 1-10 real errors a season. Everything else is a phase shift.

Measured 2026-08-27, `pinned_round27.pkl` with its correct 149-bundle vocabulary.
`data/logs/corrections_all.log`, `corrections_market.log`, `op_agreement.log`.

Alex's call, before the measurement: *"it is almost certainly a single or 2 errors and cascade,
similar to the 72"*. That is what it is.

## Off-tape, the student driving alone

    tape            op agree     bank    teacher   ratio
    91906088.json     99.97%  126,541   128,471   98.5%
    92498144.json     99.68%  149,599   150,255   99.6%
    91907974.json     87.20%   46,839    88,882   52.7%
    92466371.json     51.25%      372   147,117    0.3%

Money follows the ops, steeply and non-linearly: 99.7% keeps the season, 87% halves it, 51% ends it.

## With every divergence corrected, the errors are countable on two hands

`scripts/probe_how_many_corrections_a_season_needs.py --correct all` pins the trajectory to the tape,
so each correction is an independent error rather than an earlier one's shadow.

    tape            corrections  unit-only  mkt-only   real*
    92498144.json             7          5         2      4
    91907974.json             4          4         0      3
    92466371.json            11          3         8     10
    91906088.json             4          4         0      1

\* minus the bare-DROP noise below.

**Four to eleven errors in 719 turns**, against 87% and 51% agreement when free-running. The gap
between those two numbers IS the cascade.

## Three error classes, and one of them is not an error

1. **`teacher DROP` -> `net DROP WHEAT 1`.** Cosmetic. `reference/kaggriculture.py:343-356` takes no
   arguments and dumps the unit's whole inventory; the extra fields are ignored. Identical
   behaviour. The probe over-counted these -- 3 of 7 on `92498144`, 3 of 4 on `91906088`.
2. **`SELL WOOL 6` -> `SELL WOOL 1`.** Wool sell quantities, the bulk of `92466371`'s market errors.
3. **`teacher DIG` -> `net PLANT ...` or a move.** The first divergence on THREE of the four tapes,
   and the one that costs the season.

## The cascade is a dropped frame, not a wrong policy

From the market-corrected run on `92498144`:

    turn 297 teacher DIG               net PLANT STRAWBERRY
    turn 298 teacher PLANT STRAWBERRY  net WATER
    turn 299 teacher WATER             net SOUTH
    turn 300 teacher SOUTH             net PLANT STRAWBERRY

The net is emitting the teacher's **next** action, one turn late. It skipped a turn and the whole
memorised sequence shifted. That is a tape with a dropped frame.

Whether it re-syncs decides the season:

    92498144   d12:15 errors, then 5, 1, 1 -- recovers        99.6% of teacher
    92466371   d13:9, then 23-24 EVERY day to d29 -- never    0.3% of teacher

24 corrections a day is every unit, every hour.

## The mask forbids what the game allows

`kagg/rl/jax_masks.py:125`:

    masks[O.DIG] = (kind == J.WEED) | is_plant | empty_structure

An empty tile is none of those, so DIG is masked off. The reference ACCEPTS it --
`reference/kaggriculture.py:484`, `if tile is None: return` -- as a legal no-op that costs the unit
its turn.

So the net's first choice is deleted and its second choice is the next action in the sequence. The
frame drops.

## This corrects the 2026-08-23 write-up

`docs/the_clone_only_misses_the_unlearnable_digs_2026-08-23.md` found the same DIG and read the
consequence as displacement -- "DIG answered with PLANT leaves the hand where it is" (cheap) versus
"answered with a move walks the hand off its tile" (expensive). It then recorded `92466371`
collapsing to $372 while substituting PLANT as unexplained and structural.

The mechanism is not displacement. It is the phase shift, and it applies whatever the substitute is.
`92466371` substitutes PLANT, stays on its tile, and still dies -- because the SEQUENCE moved.

## THE PROPOSED FIX IS A NULL -- the mask is not what displaces the DIG

`data/logs/dig_premise.log`, measured after the section below was written:

    turn 297 d12 u7 at (4,7) tile=None  mask=BLOCKED
        unmasked top3 ['WATER', 'PLANT', 'COLLECT_FERTILIZER']  -> plays PLANT
    turn 331 d13 u8 at (3,8) tile=None  mask=BLOCKED
        unmasked top3 ['WATER', 'PLANT', 'FEED']              -> plays PLANT

DIG is not in the net's top THREE at the turns that break the season. Removing the mask, or
substituting PASS when the mask blocks a DIG argmax, would never fire. The net does not know DIG is
the answer there.

The control makes it starker. Where the tile IS a weed and DIG is legal:

    turn 376 d15 u11 at (3,9) tile=WEED  mask=ok
        unmasked top3 ['COLLECT_FERTILIZER', 'CARE', 'PLANT']  -> plays DIG

DIG is not top-3 there either, yet it plays DIG -- the MASK selects it by eliminating everything
else. The net has no learned signal for DIG anywhere; the mask has been standing in for one.

**And this weakens the "dropped frame" reading above.** At turn 297 the net does not merely skip a
turn: it PLANTS A STRAWBERRY on an empty tile, spending a seed and creating a crop the teacher never
made. Watering it at 298 is then the correct response to the board IT created. That is not
distinguishable, from what has been measured here, from a phase shift. Both stories fit the trace.

What is measured: DIG is the first divergence on three of four tapes, the net has no signal for it,
and the mask cannot be the fix.

## The proposed fix (SUPERSEDED -- see above)

Emit `PASS` when DIG is the unmasked argmax but the mask forbids it. Behaviourally identical to the
teacher's no-op, burns the same turn, keeps the sequence aligned. No retrain, and no change to
`jax_masks.py`, which is RL-side and uncovered by the 300-episode parity gate.

**Gated on one premise, measured by `scripts/probe_is_the_net_asking_for_the_dig.py`:** that the
net's UNMASKED first choice at those turns really is DIG. If something else displaces it, this fix is
a null. Result in `data/logs/dig_premise.log`.

## What this says about the 10-hour resume

The run stopped at round 27 of 40 and resuming was the obvious lever while the failures looked like
undertraining. They are not: the net makes 1-10 errors a season. More rounds would not fix a masked
label or a bare-DROP mismatch, and the two weak arms are not weak because they are underfitted.

Hold the resume until the DIG fix is measured.
