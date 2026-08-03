"""Alex's money shaping: zero at the starting stake, convex above it, potential-based.

**The design, and why this form.** A terminal bonus proportional to final bank changes the optimum
to margin maximisation, which an Elo ladder does not score. A *potential-based* term --
`F(s, s') = gamma * PHI(s') - PHI(s)` -- provably leaves the optimal policy unchanged (Ng, Harada &
Russell 1999), so it cannot move the objective at all; its entire effect is to relocate credit in
time, which is the actual complaint. At `gamma = 1.0` the per-step terms telescope, so the whole
episode's shaping equals `PHI(end) - PHI(start)` regardless of the path taken.

Three properties this file pins, because each corresponds to a failure this project has already had
or reasoned about:

- **Do-nothing earns nothing.** `train_jax_rl.py:392` records that an idle farm is a stable fixed
  point banking $3,000, and `docs/the_reward_is_a_step_function_2026-08-03.md` shows the reward is
  flat over $0-$3,000. Putting `PHI`'s zero at the starting stake means hoarding sums to exactly zero
  rather than being paid for.
- **Spending and earning are credited where they happen.** The policy currently experiences the cost
  of planting (immediate) and never the benefit (~240 turns later, outside GAE's ~20-turn reach).
  Per-step differences put both inside the window.
- **The path does not matter, only the endpoints.** That is the telescoping property, and it is what
  makes the shaping unable to reward a detour.
"""

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

from kagg.rl import money_potential as MP        # noqa: E402

START = 3000.0                                    # every farm's opening bank


def _m(*vals):
    return jnp.asarray(np.asarray(vals, np.float32))


# ---- the potential itself ------------------------------------------------------------------------


def test_the_potential_is_zero_at_the_starting_stake():
    """**Alex's condition.** $3,000 is what doing nothing achieves, so it must be worth nothing."""
    # **The floor moved to $0 on 2026-08-03** because a hard floor at the stake created a dead zone
    # exactly where the policy was operating (`bank_final_med` had fallen to $1,856). The convexity
    # already makes hoarding worthless -- see `tests/test_potential_floor_and_cap.py`. What must still
    # hold is Alex's requirement, "0 for 0", and that the stake is worth a rounding error.
    assert float(MP.potential(_m(0.0))[0]) == pytest.approx(0.0)
    assert float(MP.potential(_m(START))[0]) / float(MP.potential(_m(28_168.0))[0]) < 0.02


def test_the_potential_is_negligible_below_the_starting_stake_and_never_negative():
    """Clipped at zero, not signed, so a broke farm is never *paid* -- and below the opening stake the
    convexity makes the value a rounding error rather than a hard zero.

    **This test asserted an exact 0.0 until 2026-08-03**, which was the hard floor. It became a dead
    zone: `bank_final_med` fell to $1,856 and the whole season sat where the gradient was identically
    zero. What must hold is that thrift is not a strategy, which is a statement about *magnitude*.
    """
    season = float(MP.potential(_m(28_168.0))[0])
    assert float(MP.potential(_m(0.0))[0]) == pytest.approx(0.0)
    for m in (1.0, 1500.0, 2999.0):
        v = float(MP.potential(_m(m))[0])
        assert v >= 0.0, f"bank ${m:,.0f} must never be negative"
        assert v / season < 0.02, f"bank ${m:,.0f} is {v / season:.1%} of a season"


def test_the_potential_rises_above_the_starting_stake():
    a = float(MP.potential(_m(START + 1_000))[0])
    b = float(MP.potential(_m(START + 50_000))[0])
    assert 0.0 < a < b


def test_the_potential_is_convex_so_a_dollar_is_worth_more_when_rich():
    """**"much much more for 100k".** With `k > 1` the same $1,000 earned is worth more at $90k than
    at $4k, which is what distinguishes a real farm from a $5 win against a broke mirror."""
    d = 1_000.0
    low = float(MP.potential(_m(START + d))[0]) - float(MP.potential(_m(START))[0])
    high = float(MP.potential(_m(START + 50_000 + d))[0]) - float(MP.potential(_m(START + 50_000))[0])
    assert high > low * 10, "k=2 over this range should be far more than an order of magnitude"


def test_the_potential_reaches_one_at_the_reference_bank():
    """`SCALE` is $100,000 above the stake -- roughly the $106k-$113k the top two agents banked
    (`CLAUDE.md`, episode 89197802). Normalising there keeps the shaping the same order as the 0/1
    terminal reward instead of dwarfing it."""
    assert float(MP.potential(_m(START + MP.SCALE))[0]) == pytest.approx(1.0, abs=1e-5)


# ---- the per-step shaping ------------------------------------------------------------------------


def test_standing_still_is_worth_exactly_zero():
    """The whole point of putting the zero at the stake: an idle farm holds $3,000 for 719 turns and
    collects nothing for it."""
    money = jnp.full((10,), START)
    assert float(jnp.abs(MP.shaping(money[:-1], money[1:], coef=1.0)).sum()) == pytest.approx(0.0)


def test_burning_the_stake_costs_almost_nothing():
    """Going broke is barely punished, which is the point -- punishing it would make hoarding the goal.

    Was an exact zero under the hard floor. Now it telescopes to `-PHI(START)`, which is 1.1% of a
    real season, so the incentive to sit on the stake is still negligible.
    """
    money = jnp.asarray(np.linspace(START, 0.0, 12, dtype=np.float32))
    total = float(MP.shaping(money[:-1], money[1:], coef=1.0).sum())
    season = float(MP.potential(_m(28_168.0))[0])
    assert total <= 0.0
    assert abs(total) / season < 0.02


def test_spending_then_earning_back_the_same_bank_nets_to_zero():
    """The valley, traversed. Buying seed dips the bank and harvesting restores it; the shaping is
    negative then positive and cancels -- but each half lands on the turn it happened, which is the
    entire reason for using a per-step form."""
    money = _m(START + 5_000, START + 4_000, START + 3_000, START + 5_000)
    steps = MP.shaping(money[:-1], money[1:], coef=1.0)
    assert float(steps[0]) < 0 and float(steps[1]) < 0 and float(steps[2]) > 0
    assert float(steps.sum()) == pytest.approx(0.0, abs=1e-6)


def test_the_shaping_telescopes_so_only_the_endpoints_matter():
    """**The policy-invariance property, checked directly.** Two paths from the same start to the
    same finish must sum to the same shaping, or the term could pay for a detour."""
    direct = _m(START, START + 20_000)
    scenic = _m(START, START - 2_000, START + 1_000, START + 40_000, START + 20_000)
    a = float(MP.shaping(direct[:-1], direct[1:], coef=1.0).sum())
    b = float(MP.shaping(scenic[:-1], scenic[1:], coef=1.0).sum())
    assert a == pytest.approx(b, abs=1e-6)
    # The telescoped total is `PHI(end) - PHI(start)`. This used to be written as `PHI(end)` alone,
    # which was only true while the floor sat at the opening stake and made `PHI(START)` exactly zero.
    endpoints = float((MP.potential(_m(START + 20_000)) - MP.potential(_m(START)))[0])
    assert a == pytest.approx(endpoints, abs=1e-6)


def test_a_harvest_pays_on_the_turn_it_happens():
    """The failure this exists to fix: today the cost of planting lands inside GAE's ~20-turn reach
    and the revenue lands ~240 turns later, outside it. Here the revenue lands on its own turn."""
    money = _m(START + 10_000, START + 10_000, START + 14_000, START + 14_000)
    steps = MP.shaping(money[:-1], money[1:], coef=1.0)
    assert float(steps[0]) == pytest.approx(0.0)
    assert float(steps[1]) > 0.0
    assert float(steps[2]) == pytest.approx(0.0)


def test_the_shaping_is_small_against_a_win():
    """A terminal win pays 1.0. At a realistic bank the per-step term must not swamp it, or the
    policy optimises money and `CLAUDE.md`'s "select on win rate, not money" is violated in
    practice even though it is preserved in theory."""
    money = _m(START, START + 12_000)          # roughly beating `ranch`
    assert 0.0 < float(MP.shaping(money[:-1], money[1:], coef=1.0).sum()) < 0.05


def test_the_coefficient_scales_the_whole_term():
    a = MP.shaping(_m(START), _m(START + 50_000), coef=1.0)
    b = MP.shaping(_m(START), _m(START + 50_000), coef=0.25)
    assert float(b[0]) == pytest.approx(float(a[0]) * 0.25, rel=1e-5)


def test_the_default_coefficient_is_off():
    """It ships disabled. Every other test in this file passes `coef=1.0` explicitly, because a test
    that exercises a feature which is off is asserting about zeros -- `CLAUDE.md`: *"a gate only
    tests what it exercises."* Four of these were written that way and passed vacuously."""
    assert MP.DEFAULT_COEF == 0.0
    assert float(MP.shaping(_m(START), _m(START + 50_000))[0]) == 0.0


def test_a_zero_coefficient_disables_it_byte_for_byte():
    """The off switch has to be exactly off, so a run with the flag at 0 is comparable with every
    run made before the flag existed."""
    money = _m(START, START + 9_000, START - 1_000, START + 80_000)
    assert float(jnp.abs(MP.shaping(money[:-1], money[1:], coef=0.0)).sum()) == 0.0


# ---- shape and batching ---------------------------------------------------------------------------


def test_shaping_preserves_the_batch_shape():
    """Rollout money is `[B, P]`; the term is applied per row and must not reduce."""
    before = jnp.full((4, 2), START)
    after = jnp.full((4, 2), START + 1_000.0)
    assert MP.shaping(before, after, coef=1.0).shape == (4, 2)


def test_the_two_seats_are_treated_independently():
    """Seat 1 is the opponent on most rows and is not trained (`train_jax_rl.py:599`), but the term
    must still be computed per seat rather than mixing them -- the same species of error as the
    per-opponent win rate that averaged over a re-drawn label."""
    before = jnp.asarray(np.array([[START, START]], np.float32))
    after = jnp.asarray(np.array([[START + 10_000, START - 3_000]], np.float32))
    got = MP.shaping(before, after, coef=1.0)
    assert float(got[0, 0]) > 0.0
    # Seat 1 lost its stake. Under the old hard floor that was exactly 0.0; now it is a small
    # negative, and what the test is really about is that the two seats did not mix.
    assert float(got[0, 1]) < 0.0
    assert abs(float(got[0, 1])) < abs(float(got[0, 0]))
