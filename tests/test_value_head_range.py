"""The critic must be able to represent the returns it is being trained on.

**The bug this pins, before the shaping lands.** `jax_policy.py:212` is

    value = nn.sigmoid(nn.Dense(1, ...)(gtok)[..., 0])

and the sigmoid is deliberate and load-bearing. Its comment records why: at `--horizon 32` against
719-turn episodes only about one update in eleven contains a terminal reward, the other ten train the
critic purely on its own predictions, that bootstrap has no unique fixed point at gamma ~ 1, and it
**was measured climbing to 1.315** -- an impossible value -- while `explained_variance` still read
+0.98, because a critic that is self-consistently wrong explains its own targets perfectly.

So the sigmoid must not simply be removed. But with terminal reward in `{0, 0.5, 1}` *plus* potential
shaping, a state's return is `terminal + coef * (PHI(end) - PHI(s))`, which can sit **above 1** (win,
and net worth still climbing) or **below 0** (loss, and net worth falling from here). A sigmoid cannot
represent either, so the critic would silently clip at the bounds -- the worst failure mode available,
because clipping looks like confident prediction rather than an error.

The fix keeps the guard and widens it by exactly the amount shaping can contribute:

    value = sigmoid(...) * (1 + 2 * margin) - margin        # spans [-margin, 1 + margin]

`margin = 0.0` must be **byte-identical** to the current head, so a run with shaping off is
unaffected. That is `test_a_zero_margin_head_is_the_current_head`, and it is the reason this is a
rescale rather than a new head.
"""

import pytest

jnp = pytest.importorskip("jax.numpy")
jax = pytest.importorskip("jax")

from kagg.rl import jax_obs as O            # noqa: E402
from kagg.rl import jax_policy as P         # noqa: E402
from kagg.sim import jax_sim as J           # noqa: E402


@pytest.fixture(scope="module")
def obs():
    state = J.reset_with_shops(2, seed=0)
    tiles, units, glob = O.encode(state)
    return (tiles.reshape((-1,) + tiles.shape[-2:]),
            units.reshape((-1,) + units.shape[-2:]),
            glob.reshape((-1, glob.shape[-1])))


def _value(margin, obs, seed=0):
    net = P.Policy(d_model=32, n_layers=1, n_heads=2, value_margin=margin)
    params = net.init(jax.random.PRNGKey(seed), *obs)
    return net, params, net.apply(params, *obs)[1]


def test_a_zero_margin_head_is_the_current_head(obs):
    """Default off. A zero margin must give exactly the sigmoid's own range, so every existing
    checkpoint and every run made before shaping existed is unaffected."""
    _net, _p, v = _value(0.0, obs)
    assert v.shape == (obs[0].shape[0],)
    assert float(v.min()) >= 0.0 and float(v.max()) <= 1.0


def test_the_default_margin_is_zero():
    """The flag ships off, like `money_potential.DEFAULT_COEF`. A default that widened the head would
    change the critic on every run without anyone asking for it."""
    assert P.Policy().value_margin == 0.0


def test_a_margin_lets_the_critic_reach_below_zero_and_above_one(obs):
    """**The regression.** With shaping on, a return can exceed 1 or fall below 0; the head has to be
    able to say so. Checked at the extremes of the pre-activation rather than on a random init, since
    a fresh net predicts ~0.5 and would pass a weaker version of this test by accident."""
    margin = 0.25
    net = P.Policy(d_model=32, n_layers=1, n_heads=2, value_margin=margin)
    params = net.init(jax.random.PRNGKey(0), *obs)

    lo = P.rescale_value(jnp.asarray(0.0), margin)      # sigmoid saturated low
    hi = P.rescale_value(jnp.asarray(1.0), margin)      # saturated high
    assert float(lo) == pytest.approx(-margin)
    assert float(hi) == pytest.approx(1.0 + margin)
    del net, params


def test_the_rescale_is_monotone_and_fixes_the_midpoint():
    """A rescale must not reorder states. The midpoint staying at 0.5 keeps a fresh net's prediction
    where it was, so the change does not move the initialisation."""
    margin = 0.3
    xs = jnp.linspace(0.0, 1.0, 21)
    ys = P.rescale_value(xs, margin)
    assert bool(jnp.all(jnp.diff(ys) > 0))
    assert float(P.rescale_value(jnp.asarray(0.5), margin)) == pytest.approx(0.5)


def test_the_margin_still_bounds_the_critic(obs):
    """The point of the sigmoid was that an impossible value is unreachable. Widening it must not
    make it unbounded -- 1.315 was reached with an unbounded head and read as healthy."""
    margin = 0.25
    _net, _p, v = _value(margin, obs)
    assert float(v.min()) >= -margin - 1e-6
    assert float(v.max()) <= 1.0 + margin + 1e-6
