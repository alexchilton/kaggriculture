"""Measure arena throughput at different worker counts.

The point of this measurement is to decide whether the vectorized simulator is worth
building. Env steps/sec is the training bottleneck, so if plain multiprocessing gets close
to the budget a 1B-step run needs, the vectorized sim plus its parity harness -- the most
expensive item on the roadmap -- can be deferred.

Run: .venv/bin/python scripts/bench_arena.py
"""

import os
import time

from kagg.arena import run_arena

STEPS_PER_GAME = 719  # interpreter processes steps 0..718
TARGET_STEPS = 1_000_000_000  # Ender's budget, the existence proof we are pacing against


def main():
    cores = os.cpu_count()
    print(f"cpu_count={cores}")
    print(f"{'workers':>7s} {'elapsed':>8s} {'games/s':>8s} {'steps/s':>9s} "
          f"{'x1':>5s} {'1B steps':>10s}")

    baseline = None
    counts = sorted({1, 2, 4, 8, max(1, cores - 2), cores})
    for workers in counts:
        started = time.time()
        report = run_arena("starter", "pass", seeds=range(10), workers=workers)
        elapsed = time.time() - started
        steps_per_sec = report.games * STEPS_PER_GAME / elapsed
        baseline = baseline or steps_per_sec
        hours = TARGET_STEPS / steps_per_sec / 3600
        print(f"{workers:7d} {elapsed:7.1f}s {report.games / elapsed:8.2f} "
              f"{steps_per_sec:9.0f} {steps_per_sec / baseline:4.1f}x {hours:9.1f}h")


if __name__ == "__main__":
    main()
