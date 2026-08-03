"""Annealing the KL prior must not leave the policy with no regulariser at all.

**Why this exists.** `HANDOFF_2026-08-03.md` item 2. `--kl-anneal` decays `reg_coef`, and `reg_coef`
is shared: when a prior is set, `regulariser = reg_coef * kl_prior` and there is no entropy term at
all. So annealing the prior away anneals *every* regulariser away, and the run finishes completely
unregularised. That is known-dangerous here and not theoretical -- on `ppo-20260802-085329` entropy
climbed 13.35 -> 26.70 while the win rate fell 0.525 -> 0.291 over 66 updates, with the critic still
improving (`ev_signal` rising to +0.293). The anchor came off and the policy diffused.

**Why it is a handover and not a sum.** `train_jax_rl.py` argues at length, correctly, that under
Ender's structure the KL *replaces* entropy rather than adding to it, and that a separate
`--kl-coef 0.01` alongside `--ent-coef 0` cost two runs by leaving effectively no regulariser.
Summing the two would also double-count: `hand_prior_heads` returns a uniform prior for every head
it does not shape, and `KL(p || uniform) = -H(p) + const`, so on those heads the KL already *is* an
entropy bonus. So the anneal hands over from one to the other on a convex blend rather than adding
a second term.

The property pinned here: **at every point on the anneal, including the end, the regulariser is
non-zero and the entropy term's weight is the one that grows.**
"""

import importlib.util
import pathlib

import jax.numpy as jnp
import numpy as np
import pytest


def _mod():
    spec = importlib.util.spec_from_file_location(
        "t", pathlib.Path(__file__).resolve().parent.parent / "scripts" / "train_jax_rl.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Stand-in values. `entropy_loss` is negative entropy (a loss), matching the sign the trainer uses.
KL = 2.5
ENT_LOSS = -13.0
COEF = 0.01


def test_no_anneal_is_byte_identical_to_pure_kl():
    """`--kl-anneal 0` must not change a single number. This is the regression guard.

    The live run is training under the old behaviour right now, so a change that silently altered
    the un-annealed objective would invalidate every comparison against it.
    """
    m = _mod()
    got = m.blend_regulariser(COEF, 1.0, jnp.asarray(KL), jnp.asarray(ENT_LOSS), kl_active=True)
    assert float(got) == pytest.approx(COEF * KL, abs=0.0)


def test_fully_annealed_is_pure_entropy_at_full_strength_not_zero():
    """The whole point. At the end of the anneal the prior is gone and entropy is holding.

    This is the assertion the handoff asked for: entropy survives when KL is annealed.
    """
    m = _mod()
    got = m.blend_regulariser(COEF, 0.0, jnp.asarray(KL), jnp.asarray(ENT_LOSS), kl_active=True)
    assert float(got) == pytest.approx(COEF * ENT_LOSS, abs=0.0)
    assert float(got) != 0.0, "annealed to zero regularisation -- this is the bug being fixed"


def test_midway_is_the_convex_blend():
    m = _mod()
    got = m.blend_regulariser(COEF, 0.25, jnp.asarray(KL), jnp.asarray(ENT_LOSS), kl_active=True)
    expect = COEF * (0.25 * KL + 0.75 * ENT_LOSS)
    assert float(got) == pytest.approx(expect, rel=1e-12)


def test_without_a_prior_the_fraction_is_ignored_and_entropy_governs():
    """`kl_active=False` is the no-prior run. It was pure entropy before and stays pure entropy."""
    m = _mod()
    for frac in (0.0, 0.5, 1.0):
        got = m.blend_regulariser(COEF, frac, jnp.asarray(KL), jnp.asarray(ENT_LOSS),
                                  kl_active=False)
        assert float(got) == pytest.approx(COEF * ENT_LOSS, abs=0.0)


@pytest.mark.parametrize("anneal,it,expect", [
    (0, 0, 1.0), (0, 500, 1.0),          # disabled: never decays
    (100, 0, 1.0), (100, 25, 0.75), (100, 50, 0.5), (100, 100, 0.0), (100, 400, 0.0),
])
def test_the_anneal_schedule_clamps_at_zero_and_never_goes_negative(anneal, it, expect):
    """A negative fraction would flip the KL's sign and *push away* from the prior."""
    m = _mod()
    assert m.kl_fraction(anneal, it) == pytest.approx(expect)


def test_the_regulariser_strength_never_collapses_across_a_whole_anneal():
    """Sweep the entire schedule and assert the objective always has a regulariser in it.

    The failure being prevented is not "the value is slightly off at one iteration", it is
    "somewhere in the back half of the run there is nothing holding the policy at all". So this
    walks every update rather than checking endpoints, which is what `CLAUDE.md` means by refusing
    to quote an endpoint off a tail.
    """
    m = _mod()
    anneal = 200
    for it in range(0, 400):
        frac = m.kl_fraction(anneal, it)
        got = float(m.blend_regulariser(COEF, frac, jnp.asarray(KL), jnp.asarray(ENT_LOSS),
                                        kl_active=True))
        assert abs(got) > 1e-9, f"regulariser vanished at update {it} (frac {frac})"
        # And the entropy share only ever grows.
        assert 0.0 <= frac <= 1.0


def test_traced_fraction_works_under_jit():
    """`reg_coef` was once baked in as a Python float and was constant for a whole run.

    That bug is recorded in `train_jax_rl.py`'s own anneal comment -- the flag was parsed and then
    could not have worked, because the closure captured a concrete value. The fraction must be a
    traced argument for the same reason, so this pins that it survives `jit`.
    """
    import jax
    m = _mod()
    f = jax.jit(lambda c, fr, kl, e: m.blend_regulariser(c, fr, kl, e, kl_active=True))
    a = float(f(COEF, jnp.asarray(1.0), jnp.asarray(KL), jnp.asarray(ENT_LOSS)))
    b = float(f(COEF, jnp.asarray(0.0), jnp.asarray(KL), jnp.asarray(ENT_LOSS)))
    assert a == pytest.approx(COEF * KL)
    assert b == pytest.approx(COEF * ENT_LOSS)
    assert a != b, "the fraction was constant-folded; it is not actually traced"
