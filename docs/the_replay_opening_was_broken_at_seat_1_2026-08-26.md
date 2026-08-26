# `--replay-days` replayed turn 0 all season at seat 1

Found 2026-08-26 while gating the split-tape arms. One line, two places, and it made the whole
`--replay-days` feature unusable in half of every ladder match from the day it was written.

## The bug

`scripts/build_planner_submission.py`, the epilogue the bundle ships:

```python
step = int(obs.get("step", 0) or 0)
if step < len(_OPENING):
    farmer, hands, market = _OPENING[step]
```

**`kaggle-environments` gives `step` to seat 0 only.** Measured, live env, both seats:

```
turn 0 seat 0: step=0    day=0 hour=0 player=0
turn 0 seat 1: step=None day=0 hour=0 player=1
turn 1 seat 0: step=1    day=0 hour=1 player=0
turn 1 seat 1: step=None day=0 hour=1 player=1
```

So at seat 1 `obs.get("step", 0) or 0` is **0 on every turn**, `_OPENING[0]` is returned 720 times,
and the artifact plays day 0's actions for the entire season.

## What it cost

Gate against the clone tapes, `data/logs/gate_replay_arms.log`, seat 1:

```
main_base        ours $155,150   theirs $157,770
main_replay12    ours $      0   theirs $197,294
main_replay20    ours $      0   theirs $197,294
main_replay28    ours $      0   theirs $197,294
```

**$0 -- not even the $3,000 start.** Identical across all three replay depths and identical opponent
totals, which is the signature of a failure that does not depend on the arm at all.

`main_base` is unaffected because it embeds no opening: `_OPENING` is empty and the branch never
fires.

## Why the build said "submission verified"

`reproduce()` carries the same indexing, and it always plays **seat 0**:

```python
owned = len((obs.get("farms") or [{}, {}])[0].get("hands") or [])
```

At seat 0 `step` is present and correct, so the verifier exercised the one seat where the code
works. Three artifacts were built, all three printed `submission verified`, and all three banked $0
in half their games.

**This is the "a gate only tests what it exercises" lesson for the fourth time in this project** --
after single-unit parity scripts, the JAX suite with no atomic-PLANT rule, and 300 episodes where
both players never sold the same product. `CLAUDE.md` already says to ask what a gate *cannot*
reach. Seat 1 is what this one could not reach.

The repo also already knew the underlying fact: `project_kaggriculture_seat1_has_no_step` records
that a harness seating us second replays turn 0 all season and banks $0, and concludes *"Ladder
artifact is FINE; fix the harness, not the agent."* That conclusion was true of the harness it was
written about and false of this code path, which had the identical defect.

## The fix

`day * 24 + hour`, which both seats have and which is correct at both:

```python
step = int(obs.get("day", 0) or 0) * 24 + int(obs.get("hour", 0) or 0)
```

Applied in the shipped epilogue and in `reproduce()`'s `repo_play`, so the verifier and the artifact
index the opening the same way.

## What this does to the day's other measurements

- **The handover sweep stands.** `+$11,256` for handing over at d20 instead of d12 was measured with
  `scripts/breakdown.py --handover`, which drives the agent directly and never touches this
  epilogue.
- **The bare-tape portability numbers stand.** `scripts/how_far_does_a_bare_tape_hold.py` replays
  through `tape_policy`, not the bundle.
- **The clone-gate rows for `main_replay12/20/28` are VOID.** Both seatings ran the broken path, so
  `0/6` measured the bug and says nothing about replay depth.
- **`main_base` at 0/6 stands.**

The arms have to be rebuilt and re-gated before anything is claimed about how far the tape should
play in a shipped artifact.
