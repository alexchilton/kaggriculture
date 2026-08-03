# P2b's premise does not survive contact with `league1`

**Date:** 2026-08-03 (late).
**Status:** blocking finding. P2b as written cannot be built from the checkpoint we have.

## What P2b assumed

The agreed shape of P2b is *reverse curriculum from the policy's own trajectories*: roll the current
policy forward, keep the states **just before a payoff**, and resume training from those instead of
from the elite replay rungs (`10:0.1,15:0.1,20:0.1,25:0.1`), which P2 showed teach "late day = rich
farm" rather than "here is how a farm gets rich".

That design has one hard prerequisite: the policy must produce payoffs to sit in front of.

## What `league1` actually does

Measured on the stopped `league1` checkpoint, 32 games per cell, against the scripted `farm`
baseline, in both seats and under both market conditions (`data/logs/ab_frozen_town.log`):

| | A: frozen town | B: real shop schedule |
|---|---|---|
| W/D/L seat 0 | 0 / 0 / 32 | 0 / 0 / 32 |
| W/D/L seat 1 | 0 / 0 / 32 | 0 / 0 / 32 |
| policy bank at day 29 | $20 / $6 | $6 / $2 |
| farmer bank at day 29 | ~$30,292 | ~$30,292 |
| gross sales, season | $1,525 / $1,518 | $2,300 / $2,648 |
| hire, season | -$2,365 / -$2,600 | -$2,122 / -$2,280 |
| HARV share of actions | 0.72% / 0.76% | 0.92% / 0.89% |
| FEED share of actions | 0.49% / 0.76% | 0.41% / 1.50% |

The policy loses **128 out of 128 games** and arrives at the bell with single-digit dollars. Its bank
declines monotonically from $3,000 on day 0 to nothing: `d0:3,000 d5:2,872 d10:2,875 d15:2,310
d20:992 d25:7 d29:6`. Three quarters of its actions are the four movement ops.

Fixing the frozen-market bug **raised** gross sales by about 50% and left the result unchanged,
which is worth recording separately: B1 was a real train/deploy mismatch but it was not what is
holding this policy at zero.

## Why that kills the design, not just the checkpoint

There is no state in `league1`'s trajectory distribution that is "just before a payoff", because
there are no payoffs. Harvesting resume points from it would sample uniformly from a 30-day slide
into bankruptcy, and the reverse curriculum would resume the policy just before the moments it
already reaches unaided. The terminal-density argument for P2b survives; the *credit* argument does
not.

Note also that `league1` is exactly the policy the elite rungs produced. Warm-starting from it and
then deleting those rungs asks the new run to un-learn a prior instead of never acquiring it — and
its critic is fitted to "this episode ends at $0", which is the same terminal blindness P1 is about.

## What the state source could be instead

Not decided; this is input to the P2b design, which has not been approved.

1. **The scripted `farm` baseline.** It demonstrably reaches ~$30,292, so states just before its
   harvests exist and are cheap to generate. Off-policy, but so are the replay rungs it would
   replace, and unlike them it is a *trajectory* we can walk backwards rather than a snapshot.
2. **Replay trajectories, resumed just before a harvest** rather than sampled as whole-board
   snapshots at a fixed day. Same source as the poisoned rungs, different object: the point is the
   turn before the payoff, not the day-25 balance sheet.
3. **Bootstrap.** Train from day 0 until the policy harvests at all, then switch to self-harvested
   resume points. Honest to the original design, but it defers P2b behind an unknown amount of
   training and needs a trigger criterion of its own.

Whichever is chosen, the mastery criterion Fable never supplied is still open, and options 1 and 2
change what it can be measured against.

## Consequence for sequencing

P2b is not the next thing to build. Either the state source is redesigned first, or a run that can
produce payoffs at all comes first — which is the case for taking P3 (`rehire_afford`, now merged)
and P4 (the chain runs at a loss: hire alone exceeds gross sales) before P2b.
