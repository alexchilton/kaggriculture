# At round 27 the clone's only remaining error is DIG, and what it substitutes decides the season

Measured 2026-08-23, `season_fast-20260822-235031` round 27, pinned to `pinned_round27.pkl`.
`scripts/probe_where_the_replay_goes_wrong.py --horizon 719`, greedy decode -- the one `make_agent` uses.

## The result

Every first divergence on all four tapes, with the teacher driving, is `teacher DIG`.
Nothing else. One to three per season.

    tape          on-tape    off-tape       gap   first pure model error
    92498144      150,316     149,599      -717   d12 h9  DIG -> PLANT
    91906088      128,471     126,541    -1,930   d16 h22 DIG -> SOUTH
    91907974       88,882      46,839   -42,043   d17 h22 DIG -> WEST
    92466371      147,036         372  -146,664   d13 h15 DIG -> PLANT

At round 24, three days earlier, the same probe broke at d8/d10/d8/d14 and the errors were mixed:
`net NORTH` 8/16, `teacher COLLECT_FERTILIZER` 4/16, `teacher DIG` 3/16.
Those were a net still training. They are gone.

## Why the same defect costs $717 and $146,664

The model error is uniform. The consequence is not, and the substitute is why.

- **DIG answered with PLANT** leaves the hand where it is. `92498144` loses $717 -- 15 differing
  cells on d12, 7 on d13, then clean to d29.
- **DIG answered with a move** walks the hand off its tile and every later op in the day lands
  somewhere else. `91907974` loses $42,043.
- **`92466371` answers with PLANT and still collapses to $372.** Displacement is therefore not the
  whole story on that tape, and the d13 cascade breaks something structural that has not been
  identified. This is the open item.

## The digs are unlearnable by construction

`reference/kaggriculture.py:484`: DIG sets the tile to `None`, removing plants, weeds and empty
coops or pastures. On a tile that is already `None` it returns immediately -- a no-op.

Of the teacher's **104 DIG labels, 97 are legal and 7 target an already-empty tile.**
The mask correctly forbids those 7, so `greedy_action` argmaxes over `_masked_logits` carrying
`-1e9` and cannot emit them at any parameter setting, and `bc.py:232` gives an illegal label weight
zero so they never reach the gradient either.

DIG's ceiling is `97/104 = 0.933` and the converged net sits at exactly `0.933`.
**More training cannot fix this.** The op agreement figure hides it: `greedy op 0.9997` at round 27
is a season-wide average over ~7,000 unit labels, and 7 of them are unreachable.

The digs are in the tape because DIG is a real and useful op -- it is how a weed or a spent tile is
cleared before replanting. The 7 are the leader's own wasted actions, which the reference silently
ignores and we cannot copy.

## Two ways out, neither tried

1. **Strip the no-op DIGs from the teacher's action stream**, so the net is never asked the
   question. Cheapest, and it matches what the reference actually executes.
2. **Let the mask allow a no-op DIG**, so the label becomes reproducible. Changes `jax_masks.py`,
   which is RL-side only and compared to nothing by the 300-episode parity gate -- see
   `docs/the_rl_masks_never_followed_the_sims_to_1326_2026-08-23.md` for why that is dangerous.

Option 1 is the smaller blast radius.

## Training state at the time of the probe

    round  greedy op   bundle    traded    fresh
      20   0.8991     0.7646    0.8546
      24   0.9988     0.9955    0.9986    0.0106
      26   0.9997     1.0000    1.0000    0.0005
      27   0.9997     1.0000    1.0000    0.0003

Bundle and traded pinned at 1.0000 for two rounds, `fresh` at 0.0003, `op` flat at the DIG ceiling.
The run is converged; 13 rounds of the 40 remain and are not expected to move it.

## What this does NOT say

The clone is converging **to** the tape agent, not past it. Imitation caps at the teacher.
`149,599` against the tape's `150,316` is 99.5% of the teacher, and the teacher is the thing that
ships. Any gain above the teacher needs the KL-anchored RL step, which is still parked and has not
been started.
