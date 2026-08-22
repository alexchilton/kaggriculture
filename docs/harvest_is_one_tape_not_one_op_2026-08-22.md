# HARVEST 0.811 was never a harvest problem — it is one tape out of four

2026-08-22.
Measured on `data/dagger_tape/tape-v2/latest.pkl` at round 27, `.venv` on this Mac, greedy decode,
teacher-driven states (beta = 1.00).

## The number that prompted it

The per-op agreement table had `HARVEST` pinned at 0.810-0.811 over rounds 21-30 while every
neighbouring op climbed:

```
per-op (greedy)  HARVEST 0.811/1585  DIG 0.933/104  PICKUP 0.950/579  WEST 0.970/4041
                 SOUTH 0.983/2723  EAST 0.984/3398  NORTH 0.990/3788  BUILD_PASTURE 1.000/64
```

That reads as "the net cannot learn HARVEST". It is not what is happening.

## Split by tape

```
tape       latches       seat   HARVEST slots   missed   accuracy
92498144   (False, False)  0        389            0       1.000
91907974   (False, True)   0        388            0       1.000
92466371   (True,  False)  0        391            0       1.000
91906088   (True,  True)   1        417          300       0.281
```

`(389 + 388 + 391 + 117) / 1585 = 0.811`, so the aggregate is fully explained by the split.

Three tapes are **exact**. One is at 0.281.

## What it emits instead, on the failing tape

```
WATER 82   WEST 69   NORTH 49   EAST 48   SOUTH 39   FERTILIZE 6   PASS 5   DIG 2
```

Movement and watering — that is, the *other tapes'* behaviour at those turns. It is not emitting
noise and it is not emitting a near-miss of HARVEST. It is emitting a different program.

## The reading

A step function is structural, not a difficulty gradient. Two things make `91906088` the odd one
out, and only one of them is likely to matter:

1. **It is the `(True, True)` arm** — both latches armed, so it is the strawberry + four-quadrant
   program. Its schedule genuinely differs from the other three.
2. It is the only **seat-1** recording.

The 3-to-1 vote is the mechanism that fits the evidence: the net has learned the majority program
and cannot tell it is on the minority tape, so it plays the majority one. The substituted ops being
exactly the other tapes' ops at those turns is what a majority vote looks like from the inside.

**This is a hypothesis, not a measurement.** Seat is not ruled out and would want a separate probe:
re-record or re-seat one of the three passing tapes and see whether the accuracy follows the seat or
follows the branch.

## Why it may be identifiable in principle and not in practice

The two latches are the tape identity, and both are now visible to the student:

- `melon_armed` reads the opponent's MELON tile count, which is in the opponent block.
- `q4_armed` reads whether the yarn store is unlocked, which is in the shop bits added this session
  (`jax_obs.GLOBAL_FEATURES` 60 -> 122). Before that change it was **invisible on this path** —
  `adapter.state_from_obs` stubbed every unlock day to NEVER.

So the information is present. It has not been used. Whether more training closes it is open; the
shop bits are only ~25 rounds old and the checkpoint has not been trained long with them.

## What this does NOT say

It says nothing about the opening. `docs/the_student_never_hires_2026-08-22.md` is a separate and
larger defect: on turn 0 the student emits `[]` against a tape bundle of ten orders including five
HIREs, and then plays thirty days with one unit. HARVEST agreement here is measured at beta = 1,
where the teacher's crew exists, so the two are independent.
