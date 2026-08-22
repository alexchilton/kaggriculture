# The losses are narrow. (NOT a win rate -- the sample is selected on the outcome.)

> **CORRECTION, same day, from Alex: "our win rate is nothing like what you say -- i only download
> the losses".** The 60 games in `data/seed_scripts/ours_ladder/` were downloaded BECAUSE they were
> losses. Every win-rate number that was in this file -- "5-54", "win rate 0.085", and the whole
> "+$6,000 takes us to 0.475" table -- was computed on a sample conditioned on the thing being
> measured, and is worthless. They have been removed rather than annotated, so nobody re-derives
> them.
>
> This is the `farm:0.445` lesson in CLAUDE.md a second time: a number correct per row and
> meaningless in aggregate, because of what defines the rows.
>
> **What survives the correction** is the only thing the sample can legitimately show: *given that
> we lost, by how much did we lose.* That is unbiased within the set of losses, and it is the useful
> part.

Measured on **60 downloaded ladder games** of our own agent (`data/seed_scripts/ours_ladder/`),
2026-08-13. **These were downloaded because they were losses.** Nothing here is a win rate and
nothing here supports one.

## How big are the losses, given that we lost

    54 losses          median  -$8,900        mean  -$11,600
    inside  $600        6
    inside $2,100      11
    inside $6,000      23
    inside $10,000     31

Two are inside $150 -- `-$70` against TrebolNoir_ and `-$135` against Mirza Yasir Abdullah Baig.
Twenty-three of the 54 are inside $6,000.

**What that does and does not license.** It says that when we lose, we frequently lose by an amount
a single good day would cover. It says nothing about how often we lose, and any claim of the form
"+$X a game buys Y% win rate" needs an unbiased sample -- a full ladder pull, or an arena run over a
fixed seed set. That measurement has not been made.

It remains true, independently of this sample, that the ladder is an Elo rating and a $70 loss
costs what a $39,200 loss costs (`CLAUDE.md`). So a change worth $2,000 is not a rounding error
against a $71k season. The sample cannot tell us how many games that flips.

## The five wins in the set are not evidence either

The set does contain five wins -- by $13.9k, $13.5k, $78.4k, $91.0k and $65.2k -- but they are
whatever happened to be downloaded alongside, not a sample of our wins. The only thing worth noting
is that they are all large, which is consistent with "win big, lose small" but does not establish
it.

## What is NOT the cause

Checked and closed the same day, so they are not re-derived:

- **Stranded stock.** The final shed on seed 11 is completely empty -- 0 units of all nine products,
  $0 of value. `LIQUIDATE_LAST_DAY` does its job. There is no unsold inventory to recover.
- **A single catastrophic matchup.** The losses are spread across 54 distinct opponents with no
  repeat structure; the worst is -$39,200 and the median is about -$8,900.

## The timeout is separate and unquantified

`91304798` is a self-play validation episode on seed 0 that ended `TIMEOUT/TIMEOUT` at step 531 of
720. One game out of 60, and it is our own agent on both seats, so it does not sit in the ladder
sample above. It is recorded here because a timeout is a loss no dollar figure can show, the env
allows 1s/turn, and nothing in this project currently measures our per-turn latency.
