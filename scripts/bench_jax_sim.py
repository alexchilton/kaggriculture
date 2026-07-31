"""Measure the JAX simulator against the numpy one, honestly.

Both simulators are driven with the *same* pre-generated action stream, from the same starting
state, on the same machine, in the same process. Timing rules:

- The JAX step is warmed up first, because the first call pays XLA compilation. Compile time is
  reported separately rather than hidden inside the throughput number.
- Every timed JAX call ends with `block_until_ready()`. JAX dispatches asynchronously, so without
  it the loop "finishes" before the work does and the number is fiction.
- Actions are generated once, outside the timing loop, for both sides.

Three profiles, because they give very different answers and quoting only one would be misleading.
The numpy sim is built out of `if not x.any(): continue` short-circuits, so its throughput is a
function of how little is happening; the JAX sim's is not. A single-profile benchmark can
therefore be made to say almost anything.

- **idle** -- all-NOOP, empty board, no market orders. Every numpy short-circuit fires and almost
  no work is done. This is the numpy sim's ceiling and the profile its recorded headline figure
  appears to have been measured on. It is also the only profile where numpy wins.
- **farmer only** -- one live unit per player, which is what `parity.random_script` produces. The
  numpy sim skips the other 23 unit slots (`if not active.any(): continue`) and the JAX sim runs
  its slot loop to `max(n_units)`, so both do one pass.
- **full crew** -- hiring every turn on a large bank, so the crew ramps to 24 within a day. This
  is what a competent policy's turns look like and it is 24x more unit work per step.

One env step is one turn for one game, so B games advancing one turn counts as B env steps. Same
convention as `docs/throughput_measurements.md`, where the reference environment does 484/sec on
the training box.

**Absolute numbers on this Mac drift by up to 2x between a cold machine and one that has been at
100% CPU for five minutes.** Ratios held to within a few percent across runs, so quote the ratio
and treat the absolute figure as valid only alongside the run that produced it.

Run: `.venv/bin/python scripts/bench_jax_sim.py`
"""

import argparse
import time

import numpy as np


def make_frames(rng, batch, n, hire=False, idle=False):
    """`n` turns of actions with a realistic op mix, reused cyclically by the timing loops."""
    from kagg.sim.farm import MAX_UNITS, N_CROPS
    from kagg.sim.game import Actions
    from kagg.sim.market import N_PRODUCTS

    if idle:
        return [Actions(batch)]

    frames = []
    for _ in range(n):
        a = Actions(batch)
        a.unit_op[:] = rng.integers(0, 9, size=(batch, 2, MAX_UNITS))
        a.unit_crop[:] = rng.integers(0, N_CROPS, size=(batch, 2, MAX_UNITS))
        a.sell[:] = np.where(
            rng.random((batch, 2, N_PRODUCTS)) < 0.15,
            rng.integers(0, 4, (batch, 2, N_PRODUCTS)), 0,
        )
        a.buy_seed[:] = np.where(
            rng.random((batch, 2, N_CROPS)) < 0.2, rng.integers(1, 3, (batch, 2, N_CROPS)), 0
        )
        a.hire[:] = hire
        frames.append(a)
    return frames


def bench_numpy(batch, steps, frames, money, repeats=3):
    from kagg.sim.game import Game

    best = 0.0
    for _ in range(repeats):
        game = Game(batch, starting_money=money, weed_chance=0.0)
        game.step(frames[0])                   # warm the allocator, as the JAX side is warmed
        t0 = time.perf_counter()
        for t in range(steps):
            game.step(frames[t % len(frames)])
        best = max(best, batch * steps / (time.perf_counter() - t0))
    return best


def bench_jax_step(batch, steps, frames, money):
    """A Python loop over the jitted step -- the shape a policy in the loop forces."""
    from kagg.sim import jax_sim as J

    jax_frames = [J.from_numpy_actions(f) for f in frames]

    t0 = time.perf_counter()
    warm = J.step(J.reset(batch, starting_money=money), jax_frames[0])
    warm.farm.money.block_until_ready()
    compile_s = time.perf_counter() - t0

    best = 0.0
    for _ in range(3):
        state = J.reset(batch, starting_money=money)
        t0 = time.perf_counter()
        for t in range(steps):
            state = J.step(state, jax_frames[t % len(jax_frames)])
        state.farm.money.block_until_ready()
        best = max(best, batch * steps / (time.perf_counter() - t0))
    return best, compile_s


def bench_jax_rollout(batch, steps, frames, money):
    """The same step function under a jitted `lax.scan` -- no Python in the loop at all."""
    from kagg.sim import jax_sim as J

    stacked = J.stack_actions([frames[t % len(frames)] for t in range(steps)])

    t0 = time.perf_counter()
    final, _ = J.rollout(J.reset(batch, starting_money=money), stacked)
    final.farm.money.block_until_ready()
    compile_s = time.perf_counter() - t0

    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        final, _ = J.rollout(J.reset(batch, starting_money=money), stacked)
        final.farm.money.block_until_ready()
        best = max(best, batch * steps / (time.perf_counter() - t0))
    return best, compile_s


def run_profile(name, batches, steps, hire, money, numpy_max_batch, idle=False):
    rng = np.random.default_rng(0)
    print(f"\n### {name}\n")
    print(f"{'B':>7} {'numpy/s':>12} {'jax step/s':>12} {'jax scan/s':>12} "
          f"{'step x':>8} {'scan x':>8} {'compile s':>10}")
    print("-" * 78)

    for batch in batches:
        n_steps = max(24, steps if batch <= 4096 else steps // 4)
        frames = make_frames(rng, batch, 8, hire=hire, idle=idle)

        np_rate = bench_numpy(batch, n_steps, frames, money) if batch <= numpy_max_batch else None
        jx_rate, compile_s = bench_jax_step(batch, n_steps, frames, money)
        sc_rate, _ = bench_jax_rollout(batch, n_steps, frames, money)

        np_s = f"{np_rate:,.0f}" if np_rate else "-"
        step_x = f"{jx_rate / np_rate:.2f}x" if np_rate else "-"
        scan_x = f"{sc_rate / np_rate:.2f}x" if np_rate else "-"
        print(f"{batch:>7} {np_s:>12} {jx_rate:>12,.0f} {sc_rate:>12,.0f} "
              f"{step_x:>8} {scan_x:>8} {compile_s:>10.1f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", type=int, nargs="+", default=[256, 512, 1024, 4096, 16384])
    parser.add_argument("--steps", type=int, default=96)
    parser.add_argument("--numpy-max-batch", type=int, default=16384)
    parser.add_argument("--profile", choices=["idle", "farmer", "crew", "both"], default="both")
    args = parser.parse_args()

    import jax
    print(f"jax devices: {jax.devices()}")

    if args.profile in ("idle", "both"):
        run_profile("idle (all-NOOP, nothing planted, no market orders)", args.batches, args.steps,
                    hire=False, money=3000.0, numpy_max_batch=args.numpy_max_batch, idle=True)
    if args.profile in ("farmer", "both"):
        run_profile("farmer only (1 live unit per player)", args.batches, args.steps,
                    hire=False, money=3000.0, numpy_max_batch=args.numpy_max_batch)
    if args.profile in ("crew", "both"):
        run_profile("full crew (hiring every turn, ramps to 24 units)", args.batches, args.steps,
                    hire=True, money=5_000_000.0, numpy_max_batch=args.numpy_max_batch)


if __name__ == "__main__":
    main()
