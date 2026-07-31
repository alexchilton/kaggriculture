"""Tests for the local arena.

The arena is the measurement tool the whole project depends on, so its own
guarantees -- determinism, seat-swapping, correct attribution -- are tested
before anything is built on top of it.
"""

from kagg.arena import run_arena, run_match


def test_run_match_is_deterministic_for_a_fixed_seed():
    first = run_match("starter", "starter", seed=7)
    second = run_match("starter", "starter", seed=7)

    assert first.money == second.money


def test_different_seeds_produce_different_games():
    """Characterisation test: proves the seed is actually plumbed into the env.

    If this ever fails, the arena is measuring a single fixed episode and every
    comparison built on it is worthless.
    """
    results = {run_match("starter", "starter", seed=s).money for s in range(4)}

    assert len(results) > 1


def test_run_arena_plays_each_seed_in_both_seatings():
    report = run_arena("starter", "pass", seeds=[0, 1, 2], workers=2)

    assert report.games == 6


def test_run_arena_attributes_money_to_the_agent_not_the_seat():
    """`pass` never spends, so its bank must be exactly the starting money.

    If seat attribution is broken, agent B's mean will be contaminated by
    `starter`'s winnings from the swapped seating.
    """
    report = run_arena("starter", "pass", seeds=[0, 1, 2], workers=2)

    assert report.mean_money[1] == 3000.0
    assert report.mean_money[0] > 3400.0


def test_run_arena_reports_win_rate_for_the_first_agent():
    report = run_arena("starter", "pass", seeds=[0, 1, 2], workers=2)

    assert report.win_rate == 1.0
