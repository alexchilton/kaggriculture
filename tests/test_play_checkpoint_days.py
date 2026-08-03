"""The replay's day bucketing must cover every turn and end where the game ends.

**The bug this pins.** `play_checkpoint.py` computed `n_days = turns // TURNS_PER_DAY` = `719 // 24`
= **29**, then floored its flow table to `keep = 696` -- so **the last 23 turns of every game never
appeared in the buy/sell/hire/land breakdown at all**. Separately, the bank trace sampled
`money_t[::24]`, whose last index is 696, i.e. the *start* of day 29, while the headline "policy $
median" is `final.farm.money` after turn 718. The two were different timestamps and diverged badly:
against `ranch`, seat 0 read **$388** at turn 696 and **$6** at turn 718.

That mattered because the day-25-28 flows were being used to diagnose an end-of-season bank collapse.
Summing them gave -$1,374 against an actual d25-to-final drop of -$10,648: most of the collapse
happened where the table could not see. Found by Fable, recorded in
`docs/fable_review_animals_2026-08-03_evening.md`.

`CLAUDE.md`: *"A gate only tests what it cannot reach."* A reporting tool that silently omits the
last day of a 30-day game is the same species -- the numbers it prints are all true and the picture
is wrong.
"""

import importlib.util
import pathlib

import numpy as np
import pytest

jnp = pytest.importorskip("jax.numpy")

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "play_checkpoint.py"


def _load():
    spec = importlib.util.spec_from_file_location("_play_checkpoint", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PC = _load()
TPD = 24
TURNS = 719


def test_the_day_count_covers_the_whole_episode():
    """30 game-days, not 29. A 719-turn season is 29 full days plus a 23-turn tail, and the tail is
    where the season is decided."""
    assert PC.n_game_days(TURNS) == 30


def test_every_turn_lands_in_exactly_one_day_bucket():
    """**The core property.** Sum the per-day table and you must get the sum over all turns -- no
    turn dropped, none double counted."""
    flow = np.arange(TURNS, dtype=np.float32)[:, None]          # [turns, 1]
    per_day = np.asarray(PC.per_day_flow(jnp.asarray(flow), TURNS))
    assert per_day.shape == (30, 1)
    assert per_day.sum() == pytest.approx(flow.sum())


def test_the_final_partial_day_is_not_silently_dropped():
    """The regression itself: put all the money in the last 23 turns and it must still be reported.
    Under the old `keep = 696` this bucket summed to exactly zero."""
    flow = np.zeros((TURNS, 1), np.float32)
    flow[696:] = 1.0                                            # the 23 invisible turns
    per_day = np.asarray(PC.per_day_flow(jnp.asarray(flow), TURNS))
    assert per_day[29, 0] == pytest.approx(23.0)
    assert per_day[:29].sum() == pytest.approx(0.0)


def test_a_whole_number_of_days_needs_no_padding():
    """The exactly-divisible case must not gain a spurious empty day."""
    flow = np.ones((TPD * 5, 1), np.float32)
    assert PC.n_game_days(TPD * 5) == 5
    assert np.asarray(PC.per_day_flow(jnp.asarray(flow), TPD * 5)).sum() == pytest.approx(TPD * 5)


# ---- the bank trace ------------------------------------------------------------------------------


def test_the_bank_trace_ends_on_the_final_turn_not_the_start_of_the_last_day():
    """**The divergence that misled the diagnosis.** `d29` must be the bank the game actually ended
    on, so the trace agrees with the headline final-money figure instead of contradicting it."""
    money = np.arange(TURNS, dtype=np.float32)[:, None, None]   # [turns, games, seats]
    trace = np.asarray(PC.bank_by_day(jnp.asarray(money)))
    assert trace.shape[0] == 30
    assert trace[-1, 0, 0] == pytest.approx(TURNS - 1), "the last sample is the last turn"


def test_the_bank_trace_samples_day_ends_evenly():
    """Each sample is the last turn of its day, so consecutive samples are one game-day apart."""
    money = np.arange(TURNS, dtype=np.float32)[:, None, None]
    trace = np.asarray(PC.bank_by_day(jnp.asarray(money)))[:, 0, 0]
    gaps = np.diff(trace[:-1])
    assert np.allclose(gaps, TPD), "full days are evenly spaced"
    assert trace[0] == pytest.approx(TPD - 1), "day 0 reports the bank at its own last turn"
