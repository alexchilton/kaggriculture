"""A wrapper-only arm must change the season. Before 2026-08-31 none of them did.

`Arm.wrappers` was declared, populated by `arm()`, stored on the object -- and never read.
`edited_openings` skips every wrapper op with `continue`, and `season.mine()` applied only
`surplus_sells`. The `Arm` docstring names a `build_agent` that "decided which runtime wrappers it
got"; no such function exists in the file. So `herd_*`, `cow_*`, `sheep_*`, `cowshift_*`, `topup_*`,
`cond_carrot_*` and `x_cow` were byte-identical copies of the control, and a sweep over them would
have reported a grid of measured nulls.

This test fails with `_apply_wrappers` removed from `season.mine()`, which is the point: a green
suite after a fix says the fix broke nothing, not that anything checks it.

It is deliberately a BEHAVIOURAL check on a short season rather than an assertion about the wrapper
object. `herd_species` decides at `decide_day` and expresses itself through BUY_ANIMAL orders, so
an identity test on the returned callable would pass even if the wrapper never fired.
"""
import importlib.util
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def _sweep():
    spec = importlib.util.spec_from_file_location(
        "tape_edit_sweep", REPO / "scripts/tape_edit_sweep.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tape_edit_sweep"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_the_cow_arm_changes_the_herd_the_control_buys():
    """`cow_d0` forces the split to COW at day 0. The control must buy a different herd."""
    S = _sweep()
    arms = S.build_arms()
    pool = S.load_pool()
    opp = S.opponent_spec("kawashigi", pool)

    # Eight days is past the whole herd purchase -- `_herd_split` has committed and the animals are
    # bought -- and short enough to run in a test.
    control = S.season(arms["control"], 11, opp, 0.0, "kawashigi", 8)
    cow = S.season(arms["cow_d0"], 11, opp, 0.0, "kawashigi", 8)

    assert control[0] != cow[0] or control[2] != cow[2], (
        "cow_d0 produced an identical season to the control: money %r vs %r, crops %r vs %r. "
        "The wrapper is not being applied." % (control[0], cow[0], control[2], cow[2]))


def test_every_arm_builds_without_raising():
    """`edited_openings` used to raise IndexError on the CONTROL arm, so on every arm.

    It iterated the `Arm` NamedTuple itself -- yielding `("control", (), (), ())` -- and evaluated
    `e[0]` on the empty `opening` field.
    """
    S = _sweep()
    arms = S.build_arms()
    assert "control" in arms
    for name, a in arms.items():
        try:
            S.edited_openings(a)
        except Exception as exc:                                   # noqa: BLE001
            pytest.fail("arm %s failed to build its openings: %r" % (name, exc))
