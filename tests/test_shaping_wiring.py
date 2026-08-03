"""The shaping term must be wired where GAE can see it, off by default, and cut at the episode seam.

**Why a wiring test and not only a maths test.** `tests/test_net_worth.py` proves the potential is
correct; it says nothing about whether the trainer ever calls it. This project has twice built a
mechanism and left it disconnected -- `money_potential.py` shipped with 16 passing tests and no call
site anywhere in `train_jax_rl.py`, and `opportunity.py` shipped with 21 and the same. A green maths
suite next to dead code reads exactly like a working feature.

The three properties, each of which failed at least once in some form during this session's work:

1. **Off is byte-exactly off.** `--shaping-coef 0` must produce the same rewards as a build made
   before the term existed, or the A/B against the plateauing run is not an A/B.
2. **The terminal turn is excluded.** `nxt` on a terminating turn is the *reset* board, so
   `PHI(after)` there is the $3,000 opening stake and the naive difference books the whole season's net
   worth as a loss on its final turn -- a large negative reward landing exactly where the win/loss
   signal lives. This is the same class of bug as the virgin-slot reward that paid 0.5 for two starved
   farms standing still.
3. **The value head is widened with it.** Shaping pushes returns outside [0, 1] and the head is a
   sigmoid on purpose. Turning on shaping without `--value-margin` silently clips the critic, and
   clipping looks like confidence rather than error.
"""

import ast
import pathlib

import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import net_worth as NW        # noqa: E402
from kagg.sim import jax_sim as J          # noqa: E402

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "train_jax_rl.py"


@pytest.fixture(scope="module")
def tree():
    return ast.parse(SCRIPT.read_text())


def _defaults(tree):
    """Every `--flag: default` the parser declares."""
    out = {}
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "add_argument"):
            continue
        names = [a.value for a in n.args if isinstance(a, ast.Constant)]
        flag = next((x for x in names if isinstance(x, str) and x.startswith("--")), None)
        if flag is None:
            continue
        for kw in n.keywords:
            if kw.arg == "default" and isinstance(kw.value, ast.Constant):
                out[flag] = kw.value.value
    return out


def test_both_flags_exist_and_ship_off(tree):
    """A default that turned shaping on would change every run without anyone asking."""
    d = _defaults(tree)
    assert d.get("--shaping-coef") == 0.0
    assert d.get("--value-margin") == 0.0


def test_the_rollout_is_actually_given_the_coefficient(tree):
    """The dead-code guard. `make_rollout` must receive `shaping_coef` at its call site -- a flag that
    is parsed and never threaded is the exact shape of `money_potential`'s first six weeks."""
    src = SCRIPT.read_text()
    assert "shaping_coef=args.shaping_coef" in src, "make_rollout never receives the flag"
    assert "net_worth.net_worth_shaping" in src, "the shaping function is never called"


def test_the_policy_is_given_the_value_margin(tree):
    """Same guard for the head. Parsing `--value-margin` and not passing it would leave the critic
    clipped while the log claimed a margin was set."""
    assert "value_margin=args.value_margin" in SCRIPT.read_text()


def test_a_zero_coefficient_contributes_exactly_nothing():
    """Not 'approximately nothing'. The A/B depends on this being an identity."""
    a = J.reset_with_shops(2, seed=0)
    b = J.reset_with_shops(2, seed=1)
    assert float(jnp.abs(NW.net_worth_shaping(a, b, coef=0.0)).max()) == 0.0


def test_shaping_across_a_reset_would_book_a_false_loss():
    """**The reason the terminal turn is excluded, demonstrated rather than asserted.**

    A season ending rich, differenced against the reset board, produces a large negative reward. If
    that landed on the terminating turn it would sit on top of the win/loss signal and swamp it.
    """
    rich = J.reset_with_shops(2, seed=0)
    rich = rich._replace(farm=rich.farm._replace(money=rich.farm.money + 25_000.0))
    fresh = J.reset_with_shops(2, seed=0)
    across = NW.net_worth_shaping(rich, fresh, coef=1.0)
    assert float(across.min()) < -0.01, "a reset seam should look like a big loss; if not, this test "\
                                        "no longer demonstrates the hazard it exists to justify"


def test_the_terminal_turn_is_masked_in_the_trainer():
    """The fix for the above, pinned in the source: the shaped term is `where(just_done, 0, shaped)`."""
    src = SCRIPT.read_text()
    assert "jnp.where(just_done[:, None], 0.0, shaped)" in src, (
        "the shaping term must be zeroed on the terminating turn, where `nxt` is the reset board"
    )


def test_a_seasons_shaping_is_small_against_the_terminal_reward():
    """**The scale check.** Invariance protects the optimum, not the learning dynamics: a term whose
    range swamps the terminal 1.0 becomes the objective in practice whatever Ng's theorem says.

    A season going $3,000 -> $28,168 (the scripted farmer's bank) must contribute well under 1.0 at
    coef 1.0, so the coefficient has headroom rather than needing to be tiny to be safe.
    """
    start = jnp.asarray(3_000.0)
    end = jnp.asarray(28_168.0)
    total = float(NW.shaping(start, end, coef=1.0))
    assert 0.0 < total < 0.25, total
