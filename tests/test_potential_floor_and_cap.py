"""The potential must have signal where the policy actually operates, and a bounded top.

**Why the floor moved from $3,000 to $0.** The floor was there so hoarding earns nothing: recovering
the opening stake is thrift, not production. That reason is sound and the mechanism was wrong, because
the *convexity* already does it far more sharply than a hard floor does. With `EXPONENT = 2` and
`SCALE = 100_000`, a $3,000 bank is worth **1.1%** of a $28,168 season and a $1,856 bank is worth
**0.4%**. Hoarding is already worthless.

What the hard floor added was a **dead zone**. Measured on `day0-long-20260803-200350`,
`bank_final_med` fell from $20,655 to **$1,856** over 300 updates -- so the policy now spends whole
seasons *entirely below the floor*, where `PHI` is identically zero and the shaping term contributes
nothing at all. The one region we most need a gradient in was the one region guaranteed not to have
one. Alex's stated requirement was *"0 for 0, much much more for 100k"*, and `FLOOR = 0` satisfies it
literally: `PHI(0) == 0`.

**Why the top is now capped.** `PHI` was unbounded, so a rich season could contribute arbitrarily much:
at $110,000 it reads 1.21, and at `--shaping-coef 6` that is a return contribution of 7.3 against a
terminal reward of 1.0. Invariance does not protect against that -- Ng's theorem fixes the optimum, not
what PPO does with a term that swamps the objective, and the value head cannot represent it either.
`SCALE` was already chosen so a top-of-leaderboard season lands near 1.0, so clipping there costs
nothing we can currently reach and makes `--value-margin` a computable quantity instead of a guess.

Clipping does not break policy-invariance. `F(s,s') = gamma*PHI(s') - PHI(s)` telescopes for **any**
`PHI`, so a clipped potential is still a potential.
"""

import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import money_potential as MP     # noqa: E402


def test_the_floor_is_zero():
    """The dead zone is gone. A policy ending on $1,856 must still see a gradient."""
    assert MP.FLOOR == 0.0


def test_a_bankrupt_season_still_has_a_gradient():
    """**The regression.** Under `FLOOR = 3_000` this difference was exactly 0.0, so the run whose
    median bank was $1,856 got no shaping signal whatsoever."""
    d = float(MP.shaping(1_856.0, 2_856.0, coef=1.0))
    assert d > 0.0, "a $1,000 gain below the old floor must be worth something"


def test_hoarding_the_stake_is_still_worth_almost_nothing():
    """What the floor was *for*, delivered by the convexity instead. Recovering to the $3,000 opening
    stake must be worth a rounding error against a real season, or thrift becomes a strategy."""
    stake = float(MP.potential(jnp.asarray(3_000.0)))
    season = float(MP.potential(jnp.asarray(28_168.0)))
    assert stake / season < 0.02, f"stake is {stake / season:.1%} of a season; too much"


def test_zero_is_zero():
    """Alex's requirement, literally: 0 for 0."""
    assert float(MP.potential(jnp.asarray(0.0))) == 0.0


def test_the_potential_is_capped_at_one():
    """An unbounded PHI would swamp the terminal reward on a rich season and overflow the value head.
    `SCALE` already puts a top-of-leaderboard bank near 1.0, so the cap binds nowhere we can reach."""
    assert float(MP.potential(jnp.asarray(100_000.0))) == pytest.approx(1.0)
    assert float(MP.potential(jnp.asarray(500_000.0))) == pytest.approx(1.0)
    assert float(MP.potential(jnp.asarray(10_000_000.0))) == pytest.approx(1.0)


def test_the_cap_does_not_break_telescoping():
    """Invariance survives the clip, because any function of state is a valid potential."""
    path = [0.0, 40_000.0, 300_000.0, 5_000.0, 90_000.0]
    total = sum(float(MP.shaping(a, b, coef=1.0)) for a, b in zip(path, path[1:]))
    ends = float(MP.potential(jnp.asarray(path[-1])) - MP.potential(jnp.asarray(path[0])))
    assert total == pytest.approx(ends, abs=1e-6)


def test_the_launch_configuration_fits_the_value_head():
    """The check that keeps `--value-margin` honest. At the configured coefficient, a season's total
    shaping must fit inside the head's widened range, or `ret_clipped` fires and the critic silently
    saturates."""
    coef, margin = 6.0, 0.75
    realistic = float(MP.shaping(0.0, 28_168.0, coef=coef))
    assert realistic < margin, f"a $28k season contributes {realistic:.3f} against margin {margin}"
    # And the worst case is bounded, which is the whole point of the cap.
    assert float(MP.shaping(0.0, 1e9, coef=coef)) == pytest.approx(coef)
