"""Vectorized JAX re-implementation of the Kaggriculture environment.

Exists because the reference env runs at 484 steps/sec on the training box, which makes a
10B-step run take 27 days. See `docs/throughput_measurements.md`.

`kagg/sim/parity.py` is a hard gate: do not train on this sim until parity with the reference
env is exact. A divergent sim makes every downstream result fiction.
"""
