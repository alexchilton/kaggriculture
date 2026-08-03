"""The toy's numpy potential must equal the production jax one, everywhere.

**Why two implementations exist.** `kagg/rl/money_potential.py` is `jnp`, because it has to run
inside the compiled rollout. `scripts/toy_credit_window.py` needs the same formula inside a Python
step loop, where a jax scalar dispatch per turn would cost hours over a full sweep and defeat the
purpose of a laptop experiment.

**Why that is dangerous and what this file does about it.** `kagg/rl/adapter.py` states the rule this
breaks -- *"that creates two encoders which must agree forever, and they will not: this project has
already been bitten by a parity gate that tested a subset while reporting coverage, and by a JAX port
that silently fell a commit behind the numpy sim."* The mitigation is the project's standard one: a
differential test over the range that matters, so a drift shows up red rather than as a quietly wrong
experimental result.
"""

import importlib.util
import pathlib

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import money_potential as MP        # noqa: E402

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "toy_credit_window.py"


def _load_script():
    """`scripts/` is not a package, so import the experiment by path."""
    spec = importlib.util.spec_from_file_location("_toy_credit_window", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


S = _load_script()


@pytest.mark.parametrize("money", [0.0, 1.0, 2_999.0, 3_000.0, 3_001.0, 3_400.0, 4_600.0,
                                   12_078.0, 30_292.0, 103_000.0, 250_000.0])
def test_the_two_potentials_agree_at_every_landmark_bank(money):
    """The landmarks are the banks that matter: broke, the stake, one toy cycle, the toy optimum,
    `ranch`, `farm`, the reference $100k, and well past it."""
    a = float(MP.potential(jnp.asarray([money], jnp.float32))[0])
    b = S.potential_np(money)
    assert a == pytest.approx(b, rel=1e-5, abs=1e-9), f"bank ${money:,.0f}"


def test_the_two_potentials_agree_across_a_dense_sweep():
    """Landmarks can miss a piecewise error between them -- the same reason a 200-step parity check
    is a different test from a 719-step one, not a weaker one."""
    xs = np.linspace(0.0, 200_000.0, 401, dtype=np.float64)
    a = np.asarray(MP.potential(jnp.asarray(xs, jnp.float32)), np.float64)
    b = np.array([S.potential_np(x) for x in xs])
    assert np.allclose(a, b, rtol=1e-4, atol=1e-9)


def test_both_share_the_same_constants():
    """A parity test on values is useless if one side is later retuned and the other is not."""
    assert S.potential_np(MP.FLOOR) == 0.0
    assert S.potential_np(MP.FLOOR + MP.SCALE) == pytest.approx(1.0)
    assert S.potential_np.__defaults__ == (MP.FLOOR, MP.SCALE, MP.EXPONENT)
