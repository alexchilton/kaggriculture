"""Measure arena throughput at different worker counts.

Run: .venv/bin/python scripts/bench_arena.py
"""

import os
import time

from kagg.arena import run_arena


def main():
    print(f"cpu_count={os.cpu_count()}")
    for workers in (1, 4, 8):
        started = time.time()
        report = run_arena("starter", "pass", seeds=range(10), workers=workers)
        elapsed = time.time() - started
        print(
            f"workers={workers:2d}  {elapsed:5.1f}s  "
            f"{report.games / elapsed:5.2f} games/s  |  {report}"
        )


if __name__ == "__main__":
    main()
