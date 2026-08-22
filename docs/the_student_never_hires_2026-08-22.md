# The student never hires, and bundle agreement 0.9983 cannot see it

2026-08-22. Measured against `data/dagger_tape/tape-v2/latest.pkl` at round 25.

## The finding

On **turn 0**, where the student's observation is byte-identical to the tape's -- fixed start state,
same board, $3,000, no drift possible yet -- the student emits an empty market.

```
turn 0 (day 0 hour 0)
  TAPE     [['HIRE'],['HIRE'],['HIRE'],['HIRE'],['HIRE'],
            ['BUY_ANIMAL','COW',2],['BUY_ANIMAL','SHEEP',2],
            ['BUY_SEED','WHEAT',7],['BUY_SEED','MELON',12],['BUY_PRODUCT','WHEAT',6]]
  STUDENT  []
```

Five HIREs. In its own rollout the student therefore plays all 30 days with **one unit instead of
six**, with no animals, no seed and no starting stock.

Every other opening turn matched almost exactly. Turns 1-5 agreed on the farmer op, the hands and
the market, with a single hand mismatch at turn 1 (`PASS` against `WEST`).

## Why every downstream number then makes sense

    opening spend    student $886        tape $2,984
    bank at d1       student $2,114      tape $16
    bank at d5       student $2,041      tape $111
    final bank       student $282        opponent $158,145

The student hoards the float because it never buys anything. The shed stays empty, so the
near-perfect SELL orders it emits are unbacked and the reference declines them. No crew means no
harvests, which means no goods, which means no money for the day-6 land purchase, and every later
tape action assumes a farm that does not exist.

## Why the metric could not see it

    bundle agreement            0.9983
    one turn of 719             0.139%

The single most important decision in the game is 0.14% of the metric. A policy can miss it entirely
and still read as essentially perfect.

This is `CLAUDE.md`'s own lesson landing again: *"A metric can be correct per row and still
meaningless, if its label is unstable over the thing it describes."* Here the metric is correct per
row and the rows are not equally weighted by anything except their count.

## The mechanism: class imbalance on a bundle worth the whole game

    turn-0 bundle       vocabulary index 0, 10 orders including 5x HIRE
    appears             4 of 2876 turns   (0.139%)  -- once per tape
    empty bundle        1425 of 2876      (49.5%)

The loss is a per-turn mean over the bundle head. "Predict empty" is a very strong local optimum:
it is right half the time and the four turns where it is catastrophic contribute almost nothing to
the gradient. Nothing in the objective knows that one of those classes buys the game and the other
is the absence of a decision.

**The representation is not the problem.** Checked and ruled out:

- `MAX_QTY = 64` and the index IS the quantity. Every BUY the tape makes is <= 12; only one SELL per
  tape exceeds 63. The heads can express the whole opening.
- The bundle is a MULTISET and `tables()` keeps `hire` as a count column, so five hires in one turn
  is one class, not five decisions.
- A turn carries up to 10 orders and the tape's turn 0 uses exactly 10, so it fits -- but with no
  margin.
- The class exists in the vocabulary at index 0, so it is reachable.

The net can emit it. It has learned not to.

## Fixes, least to most intrusive

1. **Oversample the opening turns.** The reservoir treats turn 0 like any other turn. Pinning the
   day-0 states, or sampling them at a rate matched to their importance rather than their frequency,
   gives the gradient something to work with.
2. **Weight the bundle loss by rarity, or upweight transacting turns.** ~79% of turns place no order
   at all; the empty class dominates by construction.
3. **Do not learn it at all.** The opening is deterministic and identical across all four tapes. A
   residual policy that emits the tape's action by default gets the five hires for free and never
   has to recover this from four examples.

## What this does NOT explain

`HARVEST` is stuck at 0.810 across rounds 21-26 while every neighbouring op went to 0.95-1.00.
That is measured at beta=1, where the teacher's crew exists, so it is a separate defect and is not
downstream of the hiring failure. It is the next thing to diagnose, and the missing instrument is a
confusion breakdown -- what does it emit *instead* of HARVEST.
