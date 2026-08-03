"""The toy MDP must behave as specified before any conclusion is drawn from it.

**Why this file is not optional.** The toy exists to answer "is the credit window the blocker", and a
buggy toy answers it confidently and wrongly -- which is this project's most expensive recurring
failure (`CLAUDE.md`: a parity gate that tested a subset while reporting coverage, twice). If PLANT
silently failed, a learner would never plant and the toy would "prove" the credit window is fatal.
"""

import numpy as np
import pytest

from kagg.rl import toy as T


def test_doing_nothing_holds_the_stake_and_loses():
    """**The premise the whole exercise rests on.** The bar is what an idle opponent banks, so
    standing still must not win -- exactly the real `idle` seat at $3,000 (`train_jax_rl.py:392`)."""
    env = T.ToyFarm()
    r = 0.0
    for _ in range(T.EPISODE):
        _, r, done = env.step(T.NOOP)
    assert done
    assert env.money == T.START_MONEY
    assert r == 0.0, "holding the stake ties the bar and a tie is not a win"


def test_one_full_cycle_beats_the_bar():
    """And it must beat it, or the task is unsolvable and every arm would read zero."""
    env = T.ToyFarm()
    env.step(T.PLANT)
    for _ in range(T.RIPEN):
        env.step(T.NOOP)
    env.step(T.HARVEST)
    assert env.money == T.START_MONEY - T.SEED_COST + T.HARVEST_GAIN
    assert env.money > T.BAR
    r = 0.0
    while env.t < T.EPISODE:
        _, r, _ = env.step(T.NOOP)
    assert r == 1.0


def test_the_reward_is_terminal_only():
    """Every intermediate turn pays exactly 0, including the harvest turn. That is the property the
    money-shaping proposal exists to change, so it must be true here first."""
    env = T.ToyFarm()
    env.step(T.PLANT)
    for _ in range(T.RIPEN):
        _, r, done = env.step(T.NOOP)
        assert r == 0.0 and not done
    _, r, done = env.step(T.HARVEST)
    assert r == 0.0, "the harvest itself pays nothing -- the money moved, the reward did not"
    assert not done


def test_planting_costs_immediately():
    """The cost lands on the turn it is incurred. Combined with the test above, this *is* the
    problem: the debit is immediate and the credit is terminal."""
    env = T.ToyFarm()
    env.step(T.PLANT)
    assert env.money == T.START_MONEY - T.SEED_COST


def test_a_crop_cannot_be_harvested_before_it_ripens():
    env = T.ToyFarm()
    env.step(T.PLANT)
    for _ in range(T.RIPEN - 1):
        assert not env.legal()[T.HARVEST]
        env.step(T.NOOP)
    env.step(T.NOOP)
    assert env.legal()[T.HARVEST], "ready after exactly RIPEN waits"


def test_harvesting_early_is_a_no_op_and_does_not_pay():
    """An illegal action is ignored, as the real simulator ignores an op a unit cannot perform. If it
    silently paid, a random policy would look competent."""
    env = T.ToyFarm()
    env.step(T.PLANT)
    before = env.money
    env.step(T.HARVEST)
    assert env.money == before


def test_a_second_plant_is_illegal_while_a_crop_is_growing():
    env = T.ToyFarm()
    env.step(T.PLANT)
    assert not env.legal()[T.PLANT]


def test_planting_is_illegal_when_the_seed_cannot_be_afforded():
    env = T.ToyFarm(start_money=T.SEED_COST - 1)
    assert not env.legal()[T.PLANT]


def test_a_ripe_crop_waits_rather_than_spoiling():
    """Ripe stays ripe until harvested, which is why `opportunity.newly_ready` takes a rising edge
    rather than a level."""
    env = T.ToyFarm()
    env.step(T.PLANT)
    for _ in range(T.RIPEN + 10):
        env.step(T.NOOP)
    assert env.ripe_in == 0 and env.legal()[T.HARVEST]


def test_noop_is_always_legal():
    for money in (0, T.SEED_COST - 1, T.START_MONEY):
        assert T.ToyFarm(start_money=money).legal()[T.NOOP]


# ---- the reverse-curriculum knobs ----------------------------------------------------------------


def test_starting_ripe_and_late_makes_the_payoff_one_action_away():
    """**P2b in miniature.** The spend has happened, the crop is ready, and the terminal is close --
    so the harvest and the reward land inside any sane credit window."""
    env = T.ToyFarm(start_t=T.EPISODE - 2, start_money=T.START_MONEY - T.SEED_COST, start_ripe=0)
    assert env.legal()[T.HARVEST]
    env.step(T.HARVEST)
    _, r, done = env.step(T.NOOP)
    assert done and r == 1.0


def test_the_same_late_start_without_harvesting_loses():
    """The other half of the pair: the resume state must not be a free win, or the curriculum
    teaches nothing. This is the 'resume *before* the opportunity' rule from `opportunity.py`."""
    env = T.ToyFarm(start_t=T.EPISODE - 2, start_money=T.START_MONEY - T.SEED_COST, start_ripe=0)
    env.step(T.NOOP)
    _, r, done = env.step(T.NOOP)
    assert done and r == 0.0


# ---- calibration helpers --------------------------------------------------------------------------


def test_the_credit_gap_is_far_longer_than_a_short_window():
    """The ratio that makes this toy faithful: the real game is ~240 turns of ripening against a
    ~20-turn GAE reach, so the toy must also be an order of magnitude out."""
    assert T.credit_gap() == T.RIPEN + 1
    assert T.credit_gap() >= 12


def test_the_optimal_return_is_several_cycles_and_is_reachable():
    best = T.optimal_return()
    assert best > T.BAR
    cycles = (best - T.START_MONEY) // (T.HARVEST_GAIN - T.SEED_COST)
    assert cycles >= 3, "several cycles fit, so there is a gradient above merely winning"


def test_playing_the_optimal_policy_by_hand_reaches_the_optimal_return():
    """A closed-form claim is worth nothing unless a policy can actually achieve it.

    **The last-plant rule is part of optimal play, not a detail.** A purely greedy "plant whenever
    you can" policy sows one more crop at `t=56` that cannot ripen before the season ends and burns
    the seed money, finishing $100 short. `jax_heuristic.py` carries the same rule for the same
    reason -- *"Melon needs twelve days from planting to the end of its yield window, so seed bought
    later than this cannot mature before the season ends and is money set on fire."* This test
    originally omitted it and read as an off-by-one in the environment.
    """
    env = T.ToyFarm()
    done = False
    while not done:
        legal = env.legal()
        in_time = env.t + T.RIPEN + 1 < T.EPISODE
        a = T.HARVEST if legal[T.HARVEST] else (T.PLANT if legal[T.PLANT] and in_time else T.NOOP)
        _, _, done = env.step(a)
    assert env.money == T.optimal_return()


def test_planting_too_late_to_ripen_burns_the_seed_money():
    """The other side of the same rule, pinned so the toy keeps the trap that makes the real game
    hard: spending is always available and is not always worth it."""
    env = T.ToyFarm(start_t=T.EPISODE - 2)
    env.step(T.PLANT)
    while env.t < T.EPISODE:
        env.step(T.NOOP)
    assert env.money == T.START_MONEY - T.SEED_COST
    assert env.money < T.BAR, "a doomed plant turns a tie into a loss"
