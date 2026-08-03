# Is the model too small? — measured 2026-08-03

Short answer: **no, and scaling it now would be the wrong lever.**
We are not capacity-bound, we are step-bound by roughly two orders of magnitude.

## What we actually have

`kagg/rl/jax_policy.py`, defaults `d_model=128, n_layers=3, n_heads=4`, entity transformer over
`1 global + 100 tile + 24 unit = 125` tokens.

**727,055 parameters.** Counted, not estimated —
`scripts/`-adjacent probe in the scratchpad, `Policy.init` on a real `jax_obs.encode` batch.

Where they sit:

| module | params | share |
|---|---:|---:|
| `Block_0..2` (the trunk) | 594,816 | 81.8% |
| all 15 action/value heads | 116,367 | 16.0% |
| `tile_pos` + `unit_pos` | 15,872 | 2.2% |

The heads are cheap.
Essentially all the capacity is the three transformer blocks, so `--d-model` and `--layers` are the
only knobs that move the number.

Scaling table, same obs, real init:

| d_model | layers | heads | params | vs now |
|---:|---:|---:|---:|---:|
| **128** | **3** | **4** | **727,055** | **1.00×** |
| 128 | 4 | 4 | 925,327 | 1.27× |
| 192 | 4 | 4 | 1,977,423 | 2.72× |
| 256 | 4 | 8 | 3,422,735 | 4.71× |
| 256 | 6 | 8 | 5,002,255 | 6.88× |
| 384 | 6 | 8 | 11,041,935 | 15.2× |
| 512 | 8 | 8 | 25,745,679 | 35.4× |

## Where the winners sat

From the Orbit Wars post-mortems in `orbit_wars_jax/docs/`:

| finisher | params | env steps |
|---|---:|---:|
| IsaiahP (1st) | 200M | 15B |
| Felix Neumann (3rd) | 6.2M | 8.4B (2p) |
| simjeg (2nd) | 4.3M | 10B |
| **Ender (8th, our blueprint)** | small | **~1B** |
| **us** | **0.73M** | **6.8M turn-steps** |

0.73M against simjeg's 4.3M is a factor of 6 — real, but not the interesting number.

## The interesting number: steps per parameter

A model only earns its parameters if it sees enough data to fit them.

| | steps / param |
|---|---:|
| simjeg | ~2,300 |
| Felix | ~1,350 |
| IsaiahP | ~75 |
| **us** | **~19** |

We are 70–120× below the small-model winners on data-per-parameter.
By that measure the network we already have is **over**sized for the experience we have fed it, not
undersized.
Adding parameters makes this ratio worse in exactly the direction that hurts.

## The actual constraint is throughput

Measured on the live run (`day0-long-20260803-200350`, batch 256, horizon 32):

- steady-state **~340 turn-steps/s**, consistent across three runs (344 / 332 / 314)
- GPU pinned at **100% util, 6.4 GB of 16 GB**
- ~24 s per update; one 719-turn episode completes every ~22 updates

Ender hit **~4,000 env-steps/s** on a 4090 and ran ~1B steps.
At our 340/s, 1B steps is **38 days** of wall clock.
That, not width, is what separates us from the cheapest finisher.

## Why the GPU being at 100% does *not* mean the model is the bottleneck

FLOP accounting per update, `d_model=128`, `L=3`, 125 tokens, 512 rows (256 games × 2 seats):

- one forward ≈ `12·d²·L` per token → ~77 GFLOP
- rollout: 32 forwards → ~2.5 TFLOP
- PPO: 2 epochs × 32 minibatches × 3× (fwd+bwd) → ~15 TFLOP
- **total ≈ 17 TFLOP per update**

A 3080 laptop does that in ~1 s even on pessimistic effective throughput.
The update takes 24 s.
So **the network is somewhere around 5–15% of wall clock; the other 85–95% is the simulator, the
scripted opponents inside the rollout scan, and scan/dispatch overhead.**

The useful consequence: going to `d_model=256, layers=4` (4.7× the params) would **not** cost 4.7×
wall clock — closer to +15–50%.
Capacity is cheap here. Steps are not.

This is a FLOP estimate, not a profile.
The decisive experiment is a short `--d-model 256 --layers 4` probe measuring `sps` against the
same-length 128/3 baseline, and it needs the GPU free.

## Recommendation

1. **Do not change `--d-model` or `--layers` yet.** At 19 steps/param the model is not what is
   holding us back, and a change now would confound the pool/resume fix that just landed.
2. **Attack throughput.** 340 turn-steps/s against Ender's ~4,000 is the gap that matters. Profile
   where the 24 s goes — prime suspects are the scripted opponents (`farm`/`ranch`/`homestead` all
   run inside the rollout scan for the full batch) and `commit.py`.
3. **Scale the model only after steps get cheap.** When we are running 10–100× more steps,
   `d_model=256, layers=4` (3.4M, simjeg territory) is the natural target — and by then it will
   still be nearly free in wall clock.

Related: [[rl_lessons_billy_bradley_ender]], [[rl_lessons_simjeg]], [[rl_postmortem_and_fix_plan]].
