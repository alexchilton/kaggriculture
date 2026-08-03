"""P1: the critic must know the game ends.

**The measured problem** (`docs/critic_terminal_blindness_2026-08-03.md`, verified twice). One turn
from the bell, holding $0 against $30,000, the live critic values the position at **0.169**. A 3x
lead on the final turn reads **0.664**. Along real self-play trajectories -- accumulated board,
accumulated money, no synthetic probe -- `V` sits in a 0.12-0.14 band through the whole of the last
five days of a game already lost by day 20.

It is not blind to the clock. `day/30` and `hour/24` have been in `glob` since the first commit of
the per-turn policy and the value head reads them, in the right direction: ahead rises with day,
behind falls, monotone in both. The magnitude is ~0.02 across an entire season. So the critic has
learnt a static money-lead-to-probability map and applies it identically on turn 0 and turn 718.

**Why nothing caught it.** One turn in 719 carries a terminal reward -- 0.14% of rows -- and every
other row trains against the critic's own bootstrapped prediction. A value function that is flat in
day is *perfectly self-consistent* under bootstrapping, so there is no gradient pressure to notice
the end. That is the same fact as `ev` reading 0.79 while `ev_signal` oscillates around 0.4. The two
shipped mitigations (`seat_coef`, `--n-phases`) were both active in the broken run: seat-sum
consistency is necessary but not sufficient, since a critic that always answers 0.5/0.5 satisfies it
exactly while being useless.

**Nothing in the suite pinned any of this, which is why it ran unnoticed for 1,800 updates.** This
module is that pin. The checkpoint-dependent tests are expected to be RED on the current lineage;
that is the failing test the fix is measured against, not a broken test.
"""

import pickle
from pathlib import Path

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")
import jax

from kagg.rl import jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J

# The last turn on which a decision is made. `TURNS_PER_DAY * SEASON_DAYS` is one past the end.
LAST_TURN = J.TURNS_PER_DAY * 30 - 2

RUNS = Path("data/jax_rl_runs")


def _architecture(raw):
    """`(n_layers, d_model, n_heads)` read off a checkpoint's own shapes.

    Needed because most of `data/jax_rl_runs` is smoke runs at `d_model 32 / 1 layer / 2 heads`, and
    the newest file by mtime is usually one of those. Loading a 1-block checkpoint into the 3-block
    production model raises rather than skipping, and a 200-update smoke critic would fail these
    assertions for reasons that have nothing to do with terminal blindness.
    """
    from flax.traverse_util import flatten_dict

    flat = flatten_dict(raw)
    layers = len({k[1] for k in flat if str(k[1]).startswith("Block_")})
    d_model = n_heads = None
    for path, leaf in flat.items():
        joined = "/".join(map(str, path))
        if "MultiHeadDotProductAttention" in joined and path[-1] == "kernel":
            d_model, n_heads = int(leaf.shape[0]), int(leaf.shape[1])
            break
    return layers, d_model, n_heads


# A critic below this many updates says nothing about terminal blindness -- it has barely left its
# initialisation, and asserting anything about its calibration measures the init, not the training.
# Matching on architecture alone was not enough: a local smoke run takes the default `--d-model`, so
# it *is* production-shaped, and a 20-update smoke checkpoint was selected over a real run and duly
# failed the seat-sum assertion. Shape is not maturity.
MIN_TRAINED_UPDATES = 500


def _production_checkpoint():
    """The newest mature checkpoint at the *production* architecture, or None.

    Deliberately not a fixed run name -- these assertions are meant to hold against whatever the
    project's current critic is, and a hard-coded path would quietly stop testing anything the
    moment training moved on. `KAGG_CRITIC_CKPT` overrides and bypasses both filters, which is how
    the run on the training box is pointed at without copying it down.
    """
    import os

    override = os.environ.get("KAGG_CRITIC_CKPT")
    if override:
        return Path(override)
    want = (P.Policy().n_layers, P.Policy().d_model, P.Policy().n_heads)
    for path in sorted(RUNS.glob("*/latest.pkl"), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            with open(path, "rb") as fh:
                ck = pickle.load(fh)
            if _architecture(ck["params"]) != want:
                continue
            if int(ck.get("update", 0)) < MIN_TRAINED_UPDATES:
                continue
            return path
        except (KeyError, EOFError, pickle.UnpicklingError):
            continue
    return None


CKPT = _production_checkpoint()
needs_ckpt = pytest.mark.skipif(
    CKPT is None,
    reason="no checkpoint at the production architecture under data/jax_rl_runs "
           "(set KAGG_CRITIC_CKPT to point at one)")


def _model():
    return P.Policy()


def _load(model):
    """Load the newest checkpoint into the current architecture.

    Pre-P3 checkpoints have a 59-wide `glob` and are migrated. Migration zero-pads the new input row
    and leaves every other weight untouched, so the value head under test is exactly the trained one.
    """
    tmpl = _template_params(model)
    with open(CKPT, "rb") as fh:
        raw = pickle.load(fh)["params"]
    return jax.device_put(P.load_or_migrate(raw, tmpl))


def _template_params(model):
    t, u, g = (A._flat(x) for x in jax_obs.encode(J.reset(1)))
    return model.init(jax.random.PRNGKey(0), t, u, g)


def _value(model, params, state):
    """`V` for both seats of a one-game state, as a plain `[2]` array."""
    t, u, g = (A._flat(x) for x in jax_obs.encode(state))
    _heads, v = model.apply(params, t, u, g)
    return np.asarray(v).reshape(2)


def _position(turn, money):
    """One game, the board held at reset, the clock and the two banks set by hand.

    **The confound, recorded rather than hidden.** An empty board on day 29 is a combination training
    never produces, so a flat response here could in principle be an out-of-distribution artifact.
    The source doc rules that out separately by replaying real trajectories, where the accumulated
    board makes the outcome unambiguous and `V` still does not move. These probes are kept because
    they are fast and isolate the clock as the only variable; the real-trajectory check is the one
    that establishes the finding.
    """
    st = J.reset(1)
    return st._replace(
        step_index=jnp.full_like(st.step_index, int(turn)),
        farm=st.farm._replace(money=jnp.asarray([list(money)], dtype=st.farm.money.dtype)),
    )


# ---- the seat-sum constraint against the discount --------------------------------------------


def _seat_sum_target(gamma_per_day, turn):
    """What `V(seat0) + V(seat1)` must equal, from the reward definition alone.

    The reward is terminal and binary and exactly one seat wins, so
    `V0 + V1 = gamma^(turns remaining) * (P(seat0 wins) + P(seat1 wins)) = gamma^(turns remaining)`
    for every state, decided or not.
    """
    return (gamma_per_day ** (1.0 / J.TURNS_PER_DAY)) ** (LAST_TURN + 1 - turn)


def test_the_seat_sum_regulariser_targets_one_which_only_gamma_one_can_reach():
    """**`seat_loss` is not merely insufficient -- at gamma < 1 it is wrong.**

    `train_jax_rl.py:1044` is `square(pairs.sum(-1) - 1.0)` on every row, at `--seat-coef 1.0`. The
    default `--gamma-per-day` is 0.97, so the achievable sum runs 0.402 at turn 0 up to 1.0 at the
    bell, and the regulariser demands 1.0 throughout -- injecting a 0.598 error where most rows are.
    Sitting near 0.5/0.5 and flat is the least-loss response, which is exactly the observed failure.

    See `docs/seat_sum_fights_the_discount_2026-08-03.md`. This test pins the arithmetic so the
    inconsistency cannot be reintroduced by changing the gamma default alone.
    """
    assert _seat_sum_target(1.0, 0) == pytest.approx(1.0), "gamma 1.0 is the case seat_loss assumes"
    assert _seat_sum_target(1.0, LAST_TURN) == pytest.approx(1.0)

    # The shipped default, which no launch script has ever overridden.
    assert _seat_sum_target(0.97, 0) == pytest.approx(0.402, abs=0.002)
    assert _seat_sum_target(0.97, LAST_TURN) == pytest.approx(0.999, abs=0.002)


def test_a_discounted_run_must_not_also_use_the_seat_sum_regulariser():
    """The guard the launch scripts lacked, stated as a rule rather than a hope.

    Either resolution is fine -- gamma 1.0 with the constraint, or a discount with the target changed
    to `gamma^(turns remaining)` -- but the combination shipped by default is neither.
    """
    for gamma in (0.97, 0.99, 0.995):
        early = _seat_sum_target(gamma, 0)
        assert early < 0.95, (
            f"gamma-per-day {gamma} puts the true seat sum at {early:.3f} on turn 0, so a "
            "seat_loss targeting 1.0 is pushing the critic away from the truth")


# ---- the head is not the limitation ----------------------------------------------------------
#
# These need no checkpoint. They exist so that nobody reaches for an architecture change: the bound
# is reachable, so terminal blindness is a training failure and not a capacity one.


def test_the_value_head_can_reach_both_ends_of_its_range():
    """`nn.sigmoid` is asymptotic, so 0 and 1 are approached, never hit. The question is whether the
    head can get near enough for a certain outcome -- and it can, so a flat 0.12-0.33 response is
    not the bound biting."""
    model = _model()
    params = _template_params(model)
    t, u, g = (A._flat(x) for x in jax_obs.encode(J.reset(1)))

    from flax.traverse_util import flatten_dict, unflatten_dict

    flat = flatten_dict(params)
    # The value head is the only Dense with a single output unit reading the global token.
    heads = [p for p, v in flat.items() if p[-1] == "bias" and jnp.shape(v) == (1,)]
    assert len(heads) == 1, f"expected exactly one scalar-output head, got {heads}"
    bias = heads[0]

    for want, sign in ((0.0, -1.0), (1.0, +1.0)):
        pushed = dict(flat)
        pushed[bias] = jnp.full_like(flat[bias], sign * 40.0)
        _h, v = model.apply(unflatten_dict(pushed), t, u, g)
        assert np.allclose(np.asarray(v), want, atol=1e-3), (
            f"the head cannot express a certain outcome ({want})")


def test_an_untrained_critic_is_already_flat_in_the_clock():
    """**The baseline that makes the finding legible: flat-in-day IS the initialisation.**

    So a trained critic that still separates turn 0 from turn 718 by ~0.02 has not learnt a weak
    version of the right thing -- it has learnt nothing about the clock at all, and the tests below
    are measuring the distance from initialisation rather than a calibration error.

    Note the untrained value is **~0.35, not 0.5**. `nn.Dense`'s bias init is zeros but `gtok` is
    not, so the head's output is not centred. The source doc's candidate 3 speaks of "the sigmoid
    value head's zero-init"; the bias is zero-init and the *output* is not, which matters if anyone
    reasons from a 0.5 starting point.
    """
    model = _model()
    params = _template_params(model)
    opening = _value(model, params, _position(0, (9_000.0, 3_000.0)))
    bell = _value(model, params, _position(LAST_TURN, (9_000.0, 3_000.0)))
    assert abs(float(bell[0]) - float(opening[0])) < 0.05, (
        f"untrained critic already separates the clock: {opening[0]:.3f} -> {bell[0]:.3f}")


# ---- the critic under test ------------------------------------------------------------------
#
# RED on the current lineage, by design. Thresholds are set where a *useful* critic must be, not
# where the broken one is, so they do not have to be revisited when it improves.
#
# **Why `xfail` and not a plain red test.** These cannot pass until P1 lands, and a permanently
# failing test makes the suite's exit code useless for everything else -- which is how a real
# regression would get lost in the noise. `strict=True` is the part that matters: the moment the
# critic learns the game ends, XPASS becomes a *failure* and forces the marker off. So removing
# these three markers is part of P1's definition of done, not an afterthought.
#
# Verified against `league1-20260803-054444` on the training box, which reproduces the source doc
# independently: hopeless 0.139, won 0.687, span 0.030.

terminal_blind = pytest.mark.xfail(
    strict=True, reason="P1: the critic is terminal-blind -- remove this marker when it is fixed")


@needs_ckpt
@terminal_blind
def test_a_hopeless_position_one_turn_from_the_bell_is_valued_near_zero():
    """$0 against $30,000 with one turn left is a loss with probability 1. Measured: 0.169."""
    model = _model()
    v = _value(model, _load(model), _position(LAST_TURN, (0.0, 30_000.0)))
    assert v[0] < 0.05, f"V(hopeless, final turn) = {v[0]:.3f}; the game is over and lost"


@needs_ckpt
@terminal_blind
def test_a_won_position_one_turn_from_the_bell_is_valued_near_one():
    """The mirror. A 3x lead on the final turn is a win with probability ~1. Measured: 0.664."""
    model = _model()
    v = _value(model, _load(model), _position(LAST_TURN, (9_000.0, 3_000.0)))
    assert v[0] > 0.95, f"V(won, final turn) = {v[0]:.3f}; the game is over and won"


@needs_ckpt
@terminal_blind
def test_the_same_lead_is_worth_more_at_the_bell_than_at_the_opening():
    """**The core statement, in the form that does not depend on calibration.**

    A lead on the last turn is decisive; the identical lead on turn 0 is a coin flip with a nudge.
    A critic that has learnt the game ends must therefore separate them by a wide margin. The live
    critic separates them by ~0.02 over an entire season, and by 0.003 in the crushed case -- it is
    reading the clock and treating it as nearly irrelevant.
    """
    model = _model()
    params = _load(model)
    opening = _value(model, params, _position(0, (9_000.0, 3_000.0)))[0]
    bell = _value(model, params, _position(LAST_TURN, (9_000.0, 3_000.0)))[0]
    assert bell - opening > 0.25, (
        f"opening {opening:.3f} -> bell {bell:.3f}: span {bell - opening:.3f}. "
        "The critic is treating the last turn like the first.")


@needs_ckpt
@pytest.mark.xfail(
    strict=False,
    reason="P1: holds on some terminal-blind critics and inverts on others -- see the docstring")
def test_a_certain_outcome_is_valued_further_from_a_toss_up_than_an_uncertain_one():
    """Ordering only -- no thresholds. I wrote this expecting even a badly calibrated critic to get it
    right, so that a failure would mean the day feature was not reaching the decision at all.

    **That expectation was wrong, and the wrongness is the finding.** `league1-20260803-054444` passes
    it; `ppo-20260801-234204` (1,300 updates, same architecture) *inverts* it and values a hopeless
    position higher at the bell than at the opening. So the sign of the clock's effect is not even
    stable across checkpoints of the same lineage -- which is a stronger statement than "the magnitude
    is small", and consistent with the clock contributing noise rather than signal.

    Non-strict `xfail` for exactly that reason: strict would fail on the checkpoints where it happens
    to hold, and "it depends which broken critic you look at" is the honest status. It becomes a real
    assertion again once the critic is fixed.
    """
    model = _model()
    params = _load(model)
    crushed = _value(model, params, _position(LAST_TURN, (0.0, 30_000.0)))[0]
    behind_early = _value(model, params, _position(0, (0.0, 30_000.0)))[0]
    assert crushed < behind_early, (
        f"hopeless at the bell ({crushed:.3f}) is not valued below hopeless at the opening "
        f"({behind_early:.3f})")


@needs_ckpt
def test_the_two_seats_still_sum_to_one():
    """`seat_coef` is active and this must keep passing. It is here to make the point that it passes
    *while* the tests above fail: seat-sum consistency is necessary and not sufficient, and a flat
    0.5/0.5 critic satisfies it perfectly."""
    model = _model()
    v = _value(model, _load(model), _position(LAST_TURN, (0.0, 30_000.0)))
    assert v.sum() == pytest.approx(1.0, abs=0.05), f"seats sum to {v.sum():.3f}"
