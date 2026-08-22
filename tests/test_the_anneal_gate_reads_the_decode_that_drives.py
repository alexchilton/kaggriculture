"""Beta hands the wheel to the SAMPLED action, so the gate that releases it must read the sampled
agreement -- and it must cover every head the student decides with, not just the unit ops.

**The defect this pins.** Measured 2026-08-22, `data/logs/dagger_d01_fixed.log`, round 1:

    sample op 0.9939  bundle 0.0104  |  greedy op 0.9939  bundle 1.0000

The gate read `greedy op` = 0.9939, cleared the 0.99 bar, and started annealing. One round earlier
the bundle head had been reset to init, so the market decode the student would actually play was at
0.0104. Control passed to a policy whose market head was near-random, and `op` agreement fell
0.9939 -> 0.5539 on the next round.

Two separate mistakes, and the test covers both:

  * the gate measured `greedy` while the rollout plays `sample`, so it read the head's best guess
    rather than what the game would receive;
  * the gate measured `op` only, so a head that had never been trained did not count against it.
"""

import importlib.util
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def DT():
    spec = importlib.util.spec_from_file_location("dagger_tape", REPO / "scripts/dagger_tape.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def counts(op_hit, op_n, bundle_hit, bundle_n, g_op_hit=None, g_bundle_hit=None):
    """The counter shape `run_episode` fills, so the test speaks the real vocabulary."""
    return {
        "op_hit": op_hit, "op_n": op_n,
        "bundle_hit": bundle_hit, "bundle_n": bundle_n,
        "g_op_hit": op_n if g_op_hit is None else g_op_hit,
        "g_bundle_hit": bundle_n if g_bundle_hit is None else g_bundle_hit,
    }


def test_the_round_one_case_does_not_clear_the_bar(DT):
    """The exact numbers that released beta while the market head was random."""
    agree = counts(op_hit=9939, op_n=10000, bundle_hit=104, bundle_n=10000,
                   g_op_hit=9939, g_bundle_hit=10000)
    assert DT.anneal_agreement(agree) == pytest.approx(0.0104, abs=1e-6), (
        "the gate must see the sampled BUNDLE at 0.0104, not the greedy op at 0.9939")
    assert DT.anneal_agreement(agree) < 0.99


def test_a_policy_good_on_both_heads_clears_it(DT):
    agree = counts(op_hit=9950, op_n=10000, bundle_hit=9990, bundle_n=10000)
    assert DT.anneal_agreement(agree) >= 0.99


def test_a_good_bundle_cannot_carry_a_bad_op(DT):
    """Symmetric -- the weakest head decides, whichever it is."""
    agree = counts(op_hit=5000, op_n=10000, bundle_hit=10000, bundle_n=10000)
    assert DT.anneal_agreement(agree) == pytest.approx(0.5)


def test_the_greedy_columns_do_not_move_it(DT):
    """Greedy is reported and is a real open question. It is not what the rollout plays."""
    bad = counts(op_hit=5000, op_n=10000, bundle_hit=5000, bundle_n=10000,
                 g_op_hit=10000, g_bundle_hit=10000)
    assert DT.anneal_agreement(bad) == pytest.approx(0.5)


def test_an_empty_round_does_not_release_the_teacher(DT):
    """No turns measured is not evidence of agreement. Zero denominators must score 0, not 1."""
    assert DT.anneal_agreement(counts(0, 0, 0, 0)) == 0.0
