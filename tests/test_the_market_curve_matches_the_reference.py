"""Our fast market curve is the reference's curve, to the dollar, for every product and inventory.

Written on 2026-08-15, when the balance change (kaggle-environments 1.32.7, PR #1399) added a sixth
shape and our sim did not have it. `kagg/sim/market.py` built `BELOW_FUNC` from a five-name tuple and
died on `KeyError: 'hinge'` at import, so the grid could not run at all -- a loud failure, and the
lucky case. The dangerous one is the same change landing on a shape we already have, where the sim
would keep running and quietly price a different game.

The change:

    CARROT   below log    target 0.20  ->  below hinge  target 1.00
    TOMATO   below linear target 0.40  ->  below hinge  target 0.40
    EGG      below linear target 0.40  ->  below hinge  target 0.40

    hinge(x) = u + HINGE_GAIN * max(0, u - 1)**2      for u = x / T,  HINGE_GAIN = 8.0

`hinge` is the only shape that reads `T`, which is why `_shape` grew a third argument; the reference
passes `T` to every call and ignores it in the other five branches. Below the knee it is exactly
linear, so TOMATO and EGG are unchanged for `x < T` and only run away past it. CARROT changed on both
counts -- five times the premium at the knee AND the runaway.

This asserts against `reference/kaggriculture.py` itself rather than restating the formula, so the
next balance change fails here instead of somewhere expensive.
"""
import importlib

import numpy as np
import pytest

M = importlib.import_module("kagg.sim.market")
KG = importlib.import_module("reference.kaggriculture")


@pytest.mark.parametrize("product", list(M.PRODUCTS))
def test_every_price_matches_the_reference(product):
    """Sweep both sides of I0, and well past the knee where the hinge takes over."""
    i0 = KG.MARKET_PARAMS[product]["I0"]
    t = KG.MARKET_PARAMS[product]["T"]
    invs = sorted({int(i0 + d) for d in
                   list(range(-4 * int(t), 4 * int(t) + 1, max(1, int(t) // 8)))
                   + [0, 1, -1, int(t), -int(t), 10 * int(t), -10 * int(t), -i0]}
                  | {0, 1, i0, 2 * i0})
    invs = [v for v in invs if v >= 0]
    ours = M.price_of(product, np.array(invs, dtype=np.float64))
    for inv, got in zip(invs, np.atleast_1d(ours)):
        want = KG.market_price(product, inv)
        assert int(got) == int(want), (
            f"{product} at inventory {inv}: sim ${int(got)} vs reference ${int(want)}")


def test_the_hinge_is_flat_below_the_knee_and_runs_away_above_it():
    """The shape's defining property, stated where a future change to HINGE_GAIN would break it."""
    t = KG.MARKET_PARAMS["TOMATO"]["T"]
    i0 = KG.MARKET_PARAMS["TOMATO"]["I0"]
    at_knee = int(M.price_of("TOMATO", np.array([i0 - t], dtype=np.float64))[0])
    half = int(M.price_of("TOMATO", np.array([i0 - t / 2], dtype=np.float64))[0])
    double = int(M.price_of("TOMATO", np.array([i0 - 2 * t], dtype=np.float64))[0])
    base = KG.MARKET_PARAMS["TOMATO"]["base"]
    assert half < at_knee < double, f"{half} / {at_knee} / {double}"
    # f(T) == 1 by construction, so the knee price is exactly base * (1 + below_target).
    assert at_knee == round(base * (1 + KG.MARKET_PARAMS["TOMATO"]["below_target"])), at_knee
    # At 2T the hinge is f(2) = 2 + 8 = 10 against linear's 2, so the premium is five times what the
    # pre-1.32.7 curve paid. That ratio IS the balance change; a constant like `4 * at_knee` would
    # only be testing arithmetic.
    was_linear = round(base * (1 + KG.MARKET_PARAMS["TOMATO"]["below_target"] * 2))
    assert double >= 2.5 * was_linear, (
        f"the quadratic term is not firing: linear would pay ${was_linear}, hinge pays ${double}")


def test_the_three_buffed_products_use_the_hinge():
    """A guard on the reference, not on us: if these revert, the analysis built on them is stale."""
    for product in ("CARROT", "TOMATO", "EGG"):
        assert KG.MARKET_PARAMS[product]["below_func"] == "hinge", (
            f"{product} is no longer hinged: {KG.MARKET_PARAMS[product]}")
    assert KG.MARKET_PARAMS["CARROT"]["below_target"] == 1.00, KG.MARKET_PARAMS["CARROT"]
