"""The adapter must record WHEN a shop opened, not just that it is open.

    python -u -m pytest tests/test_the_adapter_remembers_when_each_shop_opened.py -q

THE DEFECT
----------
`adapter._unlock_days` stamps day **0** on every shop it finds in `town.unlocked_shops`::

    days = np.full((1, J.MAX_INSTANCES), J.NEVER, dtype=np.int32)
    days[0, : len(slots)] = 0                         # <- adapter.py:111

In `jax_sim` the same field holds the TRUE day: the town opens one shop at the end of every third
day (`kaggriculture.py:886`), so the first instance carries 3, the next 6, and so on.

The day-0 stamp was the right fix for the drain and is still right for it -- `_drain` only ever asks
`unlock_day <= day`, and both 0 and 3 answer the same way once the shop is open. So this has never
shown up, and the existing shop test only checks the OPEN/CLOSED bits.

It stops being harmless the moment anything reads the day as a date:

  - the q4 latch is "was the yarn store open by day 5" (`q4_branch.py:90,249`). Through the adapter
    every open shop reads day 0, so a shop that opened on day 12 is indistinguishable from one that
    opened on day 3, and the latch is not recoverable at all.
  - any "how long has this shop been trading" feature trains on the true day through `jax_sim` and
    plays on 0 through the adapter -- the same train/deploy split that
    `test_a_dead_unit_slot_looks_the_same_from_both_encoders` was written for.

WHY A MEMO IS ENOUGH
--------------------
`town.unlocked_shops` is append-only: the env appends and never removes (1.32.6 draws WITH
replacement, so the same shop can hold two slots -- which is why the memo is keyed on the slot
POSITION, not on the shop name). An agent sees every turn of its own game, so the first turn a slot
exists is exactly the day that slot opened. The observation does not state the unlock day; the
sequence of observations does.
"""
import pathlib
import sys

import numpy as np
import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

DAYS = 5                      # far enough that the first shop (day 3) is open and dated


def _walk_a_real_game(days=DAYS):
    """Step a real env with idle players, feeding every turn to a `ShopClock`.

    Returns `(clock, first_open_day, turns)`. `first_open_day` is read off the observation itself,
    so the assertion never depends on our own model of the unlock cadence.
    """
    from kaggle_environments import make

    from kagg.rl import adapter as AD
    from kagg.sim import jax_sim as J

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    clock = AD.GameMemo()
    first_open_day = None
    turns = days * J.TURNS_PER_DAY
    for turn in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        clock.observe(obs, step=turn)
        open_now = [n for n in ((obs.get("town") or {}).get("unlocked_shops") or [])]
        if open_now and first_open_day is None:
            first_open_day = turn // J.TURNS_PER_DAY
        env.step([{}, {}])
    return clock, first_open_day, turns


def _state(obs, step, clock=None):
    from kagg.rl import adapter as AD

    privates = [obs["private"] if p == 0 else AD.agent_private_stub() for p in range(2)]
    return AD.state_from_obs(obs, privates, step=step, memo=clock)


def test_the_adapter_dates_a_shop_from_the_turn_it_first_appeared():
    """The headline: an open shop must carry the day it opened, not 0."""
    from kagg.sim import jax_sim as J

    clock, first_open_day, turns = _walk_a_real_game()
    if first_open_day is None:
        pytest.skip("no shop opened inside %d turns" % turns)

    days = np.asarray(clock.unlock_days())[0]
    dated = days[days < J.NEVER]
    assert dated.size, "the clock saw a shop open but dated no instance"
    assert int(dated.min()) == first_open_day, (
        "the first instance is dated day %d; the observation shows the first shop open on day %d.\n"
        "A day-0 stamp makes every open shop look like it has been trading since the season began, "
        "so 'open by day 5' is not a question the play path can answer."
        % (int(dated.min()), first_open_day))


def test_a_shop_that_opens_later_is_dated_later():
    """Two instances that opened on different days must not collapse to the same number.

    This is the one the q4 latch needs. `days.min()` being right is not enough -- what the latch
    asks is whether a PARTICULAR shop was open by a particular day, and that needs the instances
    to be distinguishable from each other.
    """
    from kagg.sim import jax_sim as J

    clock, first_open_day, turns = _walk_a_real_game(days=10)
    if first_open_day is None:
        pytest.skip("no shop opened inside %d turns" % turns)

    days = np.asarray(clock.unlock_days())[0]
    dated = sorted(int(d) for d in days if d < J.NEVER)
    if len(dated) < 2:
        pytest.skip("only %d instance(s) opened inside 10 days" % len(dated))
    assert len(set(dated)) > 1, (
        "every one of the %d open instances is dated day %s. They opened on different days."
        % (len(dated), dated[0]))


def test_the_dated_schedule_reaches_the_state_the_encoder_reads():
    """The memo is useless if `state_from_obs` ignores it."""
    from kagg.sim import jax_sim as J

    clock, first_open_day, turns = _walk_a_real_game()
    if first_open_day is None:
        pytest.skip("no shop opened inside %d turns" % turns)

    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    step = DAYS * J.TURNS_PER_DAY - 1
    for _ in range(step):
        if env.done:
            break
        env.step([{}, {}])
    obs = env.state[0].observation

    st = _state(obs, step, clock)
    days = np.asarray(st.unlock_day)[0]
    dated = days[days < J.NEVER]
    assert dated.size and int(dated.min()) == first_open_day, (
        "state_from_obs produced unlock_day %s; the clock says the first shop opened on day %d."
        % (dated.tolist(), first_open_day))


def test_the_memo_is_keyed_on_the_slot_not_the_shop_name():
    """1.32.6 draws WITH replacement, so one shop can hold two slots that opened days apart.

    Keying the memo on the shop name would date the second instance from the first one's day, and
    `_drain` treats the two slots as independent consumers -- so the error is a wrong drain, not a
    cosmetic one.
    """
    from kagg.rl import adapter as AD
    from kagg.sim import jax_sim as J
    from kagg.sim.town import SHOPS

    name = sorted(SHOPS)[0]
    clock = AD.GameMemo()
    clock.observe({"town": {"unlocked_shops": [name]}}, step=3 * J.TURNS_PER_DAY)
    clock.observe({"town": {"unlocked_shops": [name, name]}}, step=6 * J.TURNS_PER_DAY)

    days = [int(d) for d in np.asarray(clock.unlock_days())[0] if d < J.NEVER]
    assert days[:2] == [3, 6], (
        "two slots of the same shop dated %s; they were first seen on days 3 and 6. "
        "The memo is keyed on the shop name, not the slot." % (days[:2],))
