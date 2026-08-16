"""The melon->strawberry fork reads the opponent's melon on the day the two cases are still apart.

Written RED before the constants moved, per the project rule.

## The measurement behind it

51 recorded カワシギ games (`data/seed_scripts/downloads_2026-08-13`), split by his own allocation:

    MELON 20 / STRAWBERRY 34   42 games
    MELON 12 / STRAWBERRY 42    9 games

Opponent melon tiles visible to him, by the day he could read them:

    day   his STRAWBERRY games      his MELON games        separable?
    d3    min  9  max 13            min 4  max  8          YES, hard gap 8|9
    d4    min  9  max 13            min 4  max  8          YES, hard gap 8|9
    d5    min  9  max 13            min 4  max 10          NO, overlaps at 9 and 10

The classes are separable at d3 and d4 and **merge by d5**, because three of the melon-heavy games'
opponents keep planting melon after d3 and grow into the strawberry group's range. Reading late does
not read a noisier version of the signal -- it reads a signal that is no longer there.

The shipped rule read **d5 at a threshold of 7**. Both halves were wrong: the day is past the point
where the cases separate, and 7 sits *below* the melon-heavy group's own maximum of 8, so it fires on
his commonest case.

## What these tests do and do not claim

They pin the rule to the measurement. They do NOT claim the rule is optimal -- it is カワシギ's rule,
read off his games, and he wins all nine of the strawberry-heavy ones. Whether the conditional beats
a hard-wired mix is a separate question that needs the pool and win rate.

Nine positive cases is a thin basis for a perfect separator. The gap is wide rather than marginal,
which is why it is worth pinning, but a later sample could narrow it -- so the test asserts the
measured boundary explicitly rather than hiding it behind the constant.
"""
import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import schedule_agent as A

#: The measured extremes, from the 51 games. `d3` is the earliest day both were sampled.
HIS_STRAWBERRY_GAMES_MIN_AT_D3 = 9
HIS_MELON_GAMES_MAX_AT_D3 = 8
HIS_MELON_GAMES_MAX_AT_D5 = 10


def test_the_fork_reads_before_the_two_cases_merge():
    """d5 cannot separate them: his melon-heavy games reach 10 there, inside the other group."""
    assert A.MELON_YIELD_FROM_DAY <= 4, (
        "the classes overlap from d5 on -- reading there sees a signal that no longer exists")
    assert A.MELON_YIELD_FROM_DAY >= 3, (
        "d3 is the earliest day the measurement covers; earlier is unmeasured, not better")


def test_the_threshold_sits_in_the_measured_gap():
    """Between his melon games' max (8) and his strawberry games' min (9), at d3."""
    assert HIS_MELON_GAMES_MAX_AT_D3 < A.MELON_YIELD_OPPONENT_MELON <= HIS_STRAWBERRY_GAMES_MIN_AT_D3


def test_the_old_threshold_would_have_fired_on_his_commonest_case():
    """7 is below the melon-heavy group's own maximum, so it misfires by construction."""
    assert 7 <= HIS_MELON_GAMES_MAX_AT_D3, "the premise of this test has changed; re-measure"
    assert A.MELON_YIELD_OPPONENT_MELON > HIS_MELON_GAMES_MAX_AT_D3


def test_the_fork_is_still_switched_on():
    """The dial the CEM kept in every generation. Off is a different agent, not a safer one."""
    assert A.MELON_YIELDS_TO_A_MELON_HEAVY_OPPONENT is True


@pytest.mark.parametrize("opp_melon,should_fire", [
    (4, False), (5, False), (7, False), (8, False),   # his melon-heavy games, at d3
    (9, True), (10, True), (12, True), (13, True),    # his strawberry-heavy games, at d3
])
def test_every_recorded_game_lands_on_the_side_he_played(opp_melon, should_fire):
    assert (opp_melon >= A.MELON_YIELD_OPPONENT_MELON) is should_fire


def test_the_swap_moves_melon_into_strawberry_and_keeps_the_count():
    """`_melon_to_strawberry` rewrites in place and preserves the planting ORDER."""
    row = {"seeds": {"STRAWBERRY": 3, "MELON": 5, "CARROT": 7},
           "plants": ["MELON", "WHEAT", "MELON"]}
    out = A._melon_to_strawberry(row)
    assert out["plants"] == ["STRAWBERRY", "WHEAT", "STRAWBERRY"]
    assert out["seeds"].get("MELON", 0) == 0
    assert out["seeds"]["STRAWBERRY"] == 8
    assert out["seeds"]["CARROT"] == 7
    assert row["plants"] == ["MELON", "WHEAT", "MELON"], "the caller's row must not be mutated"
