"""Vectorized numpy-batched re-implementation of the Kaggriculture environment.

Exists because the reference env runs at 484 steps/sec on the training box, which makes a
10B-step run take 27 days. See `docs/throughput_measurements.md`.

numpy first, JAX later: the hard part is the one-unit-at-a-time market settlement, and that is
far easier to make parity-exact with ordinary control flow than under `lax.scan`. The parity tests
are identical either way, so none of that work is wasted.

**Parity is a hard gate**: do not train on this sim until it matches the reference exactly. A
divergent sim makes every downstream result fiction. See `tests/test_sim_market.py`.
"""

from kagg.sim.market import price, price_of, settle_sales  # noqa: E402

__all__ = ["price", "price_of", "settle_sales"]
