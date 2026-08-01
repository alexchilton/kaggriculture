"""The training log's win rate, and why the obvious definitions of it cannot move.

`wr` read 0.500 to three decimals on every update of a 63-update run. That is not a policy sitting
at parity -- it is arithmetic leaking into the metric, and it has now happened twice with two
different definitions. These tests pin the property that makes a win rate informative: it must be
able to read something other than 0.5 when the live policy is winning.

The rollout is a compiled JAX scan over the simulator and far too heavy to stand up here, so these
work on the row masks it emits, which is where both bugs actually lived.
"""

import numpy as np
import pytest


def _rows(n_games, opponent_frac):
    """The per-row flags one rollout step emits, laid out as the scan lays them out.

    Rows are `[game, seat]` flattened with the seat axis innermost, so rows 2k and 2k+1 are the two
    seats of one game. Seat 0 is always the live policy; seat 1 is the frozen opponent in exactly
    the games flagged for cross-play.
    """
    use_opp = np.zeros(n_games, dtype=bool)
    use_opp[:int(round(opponent_frac * n_games))] = True

    seat = np.tile([0, 1], n_games)
    crossplay = np.repeat(use_opp, 2)
    take_opp = crossplay & (seat == 1)
    return dict(seat=seat, crossplay=crossplay, trainable=~take_opp)


def _win_rate(rows, reward, live):
    """Mean terminal reward over whichever rows `live` selects."""
    sel = live
    return reward[sel].mean() if sel.any() else float("nan")


def _terminal_reward(rows, live_wins):
    """One game, one winner: seat 0 takes `live_wins`, seat 1 takes the complement."""
    seat0 = np.where(live_wins, 1.0, 0.0)
    reward = np.empty(len(rows["seat"]))
    reward[0::2] = seat0
    reward[1::2] = 1.0 - seat0
    return reward


@pytest.mark.parametrize("opponent_frac", [0.0, 0.25, 0.5])
def test_trainable_rows_alone_pin_the_win_rate_near_one_half(opponent_frac):
    """The previous definition, and why it could not move.

    In a self-play group *both* seats are trainable, so both are counted and the pair averages
    exactly 0.5 whatever either side did. Only a cross-play game contributes a single free row. At
    `--opponent-frac 0.25` that is two pinned rows per self-play game against one free row per
    cross-play game, so 86% of the measurement is fixed by arithmetic -- which is why a policy
    winning *every* cross-play game still cannot push the number far from a half.
    """
    n_games = 64
    rows = _rows(n_games, opponent_frac)
    reward = _terminal_reward(rows, live_wins=np.ones(n_games, dtype=bool))

    wr = _win_rate(rows, reward, rows["trainable"])

    # Two pinned rows per self-play game, one free row per cross-play game.
    ceiling = 0.5 + 0.5 * opponent_frac / (2 - opponent_frac)
    assert wr == pytest.approx(ceiling, abs=1e-9)
    assert wr < 1.0, "a perfect policy cannot read 1.0 under this definition, at any fraction"


def test_the_pinning_is_worst_at_the_fraction_the_runs_actually_use():
    """`--opponent-frac 0.25`: a policy winning every cross-play game reads 0.571, not 1.0.

    So the whole observable range is 0.43-0.57 and the run's 0.500 was consistent with anything.
    """
    rows = _rows(64, 0.25)
    perfect = _terminal_reward(rows, np.ones(64, dtype=bool))

    assert _win_rate(rows, perfect, rows["trainable"]) == pytest.approx(0.5714, abs=1e-4)


def test_crossplay_rows_move_with_the_policy():
    """The definition now in use: the live policy's seat in a cross-play game.

    That row's outcome is the only one not determined by its partner, so it is the whole signal.
    """
    n_games = 64
    rows = _rows(n_games, 0.25)
    live = rows["trainable"] & rows["crossplay"]

    always = _terminal_reward(rows, np.ones(n_games, dtype=bool))
    never = _terminal_reward(rows, np.zeros(n_games, dtype=bool))

    assert _win_rate(rows, always, live) == pytest.approx(1.0)
    assert _win_rate(rows, never, live) == pytest.approx(0.0)


def _use_opp(batch, opponent_frac, it, contiguous):
    """Which games face the frozen opponent on update `it`, old scheme and new."""
    n = int(round(opponent_frac * batch))
    flags = np.zeros(batch, dtype=bool)
    if not n:
        return flags
    if contiguous:
        flags[[(it * n + j) % batch for j in range(n)]] = True
    else:
        stride = max(1, batch // n)
        flags[[(j * stride + it) % batch for j in range(n)]] = True
    return flags


@pytest.mark.parametrize("contiguous,expect_covered", [(True, False), (False, True)])
def test_crossplay_games_must_reach_the_end_of_the_season(contiguous, expect_covered):
    """A game's index is its phase group, and a phase group is a fixed season position.

    So index order is season order, and the games that *finish* are the contiguous band sitting at
    the season boundary. Choosing cross-play games as a contiguous block means two blocks rotating
    at different rates, which mostly miss: the cross-play win rate saw zero qualifying rows update
    after update, and the frozen opponent never played the endgame. Striding covers every band on
    every update.
    """
    batch = 256
    ending = np.zeros(batch, dtype=bool)
    ending[-24:] = True                      # the phase groups about to cross turn 719

    covered = [bool((_use_opp(batch, 0.25, it, contiguous) & ending).any()) for it in range(8)]

    assert all(covered) is expect_covered, f"per-update coverage of the endgame: {covered}"


def test_crossplay_rows_are_the_live_policys_own_seat():
    """Never the opponent's: its reward is our loss, and averaging it back in cancels the signal."""
    rows = _rows(16, 0.25)
    live = rows["trainable"] & rows["crossplay"]

    assert live.sum() == 4, "one row per cross-play game, not two"
    assert set(rows["seat"][live]) == {0}
