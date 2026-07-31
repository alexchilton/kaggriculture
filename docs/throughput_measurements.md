# Env throughput — measured

**Measured 2026-07-31.** Reproduce with `python scripts/bench_arena.py`.
This decides whether the vectorized simulator is optional. It is not.

## Numbers

`starter` vs `pass`, 100 games per row (worker startup amortised), 719 steps per game.

| Machine | CPU | 1 worker | best multiprocess | 1B steps | 10B steps |
|---|---|---|---|---|---|
| Mac (dev) | 14-core Apple Silicon | 1,054 steps/s | 8,009 (12 workers) | 35 h | 347 h |
| **Windows box (training)** | **AMD Ryzen 9 5900HX, 8c/16t** | **484 steps/s** | **4,221 (16 workers)** | **66 h** | **658 h** |

The training box is **2.2x slower per core** than the dev Mac and 1.9x slower in aggregate.
Every throughput figure that matters is therefore the Windows row, not the Mac row.

Scaling is poor: 16 workers gives only 8.7x over one worker on an 8-core/16-thread part.
SMT contributes little and the Python interpreter dominates.

## Correction to a previously recorded fact

`README.md` recorded **1163 steps/sec single-threaded** as a measured fact.
That figure is roughly the *Mac* rate and is 2.4x optimistic for the machine that will actually
train.
The training box does 484.

## What this means for the plan

Competitive runs in the comparable previous competition used **8-15B env steps**
(8th place ~1B on a single 3080; 2nd place 10B; 1st place 15B).

- 1B steps on the training box: **66 hours**. Viable once, far too slow to iterate.
- 10B steps: **658 hours, 27 days**. Not viable.
- To reach 10B in 24 hours the sim must sustain **~116,000 steps/sec**, about **27x** the
  Python env's best multiprocess rate.

These are also *optimistic* numbers, for two reasons:

1. They use `starter`, a trivial random policy. No policy forward pass is included.
2. **`env.run()` cannot feed a GPU.** It plays a whole episode with per-step agent callbacks
   inside a worker process, so policy inference cannot be batched across environments. The
   options with this harness are a CPU policy copy per worker, or shuttling observations to the
   main process over IPC every step. Both are bad, and neither is what the throughput above
   measures.

A vectorized on-device sim removes that entire class of overhead as a side effect, which is a
second, independent argument for it beyond raw speed.

## Consequence

The vectorized simulator is **required, not optional**, and its target is set by the 10B figure:
**~100k+ steps/sec**.
Renting GPU time should be considered rather than assumed away — one 3080 Laptop may not be
enough to be competitive even with a fast sim.

What multiprocessing *does* buy is a **proof-of-life run**: 100M steps in ~6.6 hours on the
training box, enough to test the RL frame against the explained-variance kill criterion in
`CLAUDE.md` before committing to the sim build.
