"""Replay a real leader's tape and land on their exact bank, turn for turn.

Episode 89873723 seat 0 banked **$147,178**. Driving its recorded 720-turn action tape -- both seats --
through `kagg.sim` reproduces that number exactly, and matches the recorded money at every single turn
along the way. The JAX simulator does the same.

This is the gate that says a trajectory search is worth running: given a sequence of actions, our
simulator produces the season those actions actually produced on Kaggle, so a candidate's score is the
score it would really get. Without it, every candidate would be ranked by a simulator settling a
different game.

**The one-line trap that hid this for a whole session.** `steps[0].action` is the placeholder recorded
when the environment resets, before any agent has seen a board. Applying it shifts every later turn by
one, which puts each day boundary a turn out of place. Measured, replaying into the *official*
environment:

    from index 0:  first divergence turn  48,  final $43,443
    from index 1:  first divergence turn 577,  final $147,031   (recorded $147,178)

A 3.4x shortfall that looks exactly like a broken simulator and is an off-by-one in the harness. Four
separate "first divergences" were chased and explained -- turns 23, 47, 48, 97 -- before this was
found; every one of them was the shift, or the recorder's own snapshot timing, and none was real.

The other thing not to re-derive: the recorded observation at step `t` reflects `action[t]` but is
captured **before that step's `_end_of_day`**, so shed, carried inventories and the daily animal/plant
refresh all read one step stale. Money does not, which is why money is what this compares.
"""

import json
import pathlib

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.sim.game import Actions, Game

EPISODE = pathlib.Path("data/episodes/89873723.json")
SEAT = 0
EXPECTED_BANK = 147_178.0
TURNS_PER_DAY = 24
# `steps[0].action` is the reset placeholder and is never applied. See the module docstring.
FIRST_ACTION_TURN = 1

pytestmark = pytest.mark.skipif(not EPISODE.exists(), reason="replay not present")


def _rtd():
    """`scripts/replay_tape_day.py` holds the tape -> Actions writers; import it by path."""
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location("rtd", "scripts/replay_tape_day.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["rtd"] = module
    spec.loader.exec_module(module)
    return module


def _frames(steps, rtd):
    """One `Actions` per recorded turn, both seats, market orders in their recorded slot order."""
    for t in range(FIRST_ACTION_TURN, len(steps)):
        actions = Actions(1)
        for seat in range(2):
            act = steps[t][seat].get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                rtd.write_unit(actions, seat, slot, entry)
            rtd.write_market(actions, seat, act.get("market"))
        recorded = (steps[t][SEAT].get("observation") or {}).get("farms")
        yield t, actions, (float(recorded[SEAT]["money"]) if recorded else None)


def _load():
    rtd = _rtd()
    steps = json.loads(EPISODE.read_text())["steps"]
    return rtd, steps, rtd.unlock_schedule(steps)


def test_the_numpy_sim_tracks_the_recorded_bank_every_turn():
    """**The claim.** Not just the final number -- every turn of it."""
    rtd, steps, schedule = _load()
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)

    checked = 0
    for t, actions, recorded in _frames(steps, rtd):
        game.step(actions)
        if recorded is None:
            continue
        ours = float(game.farms[0].money[0])
        checked += 1
        assert ours == pytest.approx(recorded, abs=0.5), (
            f"turn {t} (day {t // TURNS_PER_DAY} hour {t % TURNS_PER_DAY}): "
            f"ours ${ours:,.0f} vs recorded ${recorded:,.0f}")

    assert checked > 700, f"only {checked} turns carried a recorded bank -- the gate proved little"
    assert float(game.farms[0].money[0]) == pytest.approx(EXPECTED_BANK, abs=0.5)


def test_the_jax_sim_reaches_the_same_bank():
    """The batched evaluator a trajectory search scores against has to agree, or it ranks fiction."""
    jax_sim = pytest.importorskip("kagg.sim.jax_sim")
    rtd, steps, schedule = _load()
    state = jax_sim.reset(1, unlock_schedule=schedule)

    for _t, actions, _recorded in _frames(steps, rtd):
        state = jax_sim.step(state, jax_sim.from_numpy_actions(actions), weed_chance=0.0)

    ours = float(np.asarray(jax_sim.money(state))[0, 0])
    assert ours == pytest.approx(EXPECTED_BANK, abs=0.5), (
        f"jax banked ${ours:,.0f} against the recorded ${EXPECTED_BANK:,.0f}")


def test_applying_the_reset_placeholder_breaks_it():
    """Pins the off-by-one, so nobody re-introduces it and spends a session chasing turn 48.

    Deliberately asserts the *wrong* alignment is wrong. A regression here would otherwise be silent:
    the season still runs, still looks plausible, and simply banks a third of what it should.
    """
    rtd, steps, schedule = _load()
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)

    for t in range(0, len(steps)):          # from 0, i.e. including the placeholder
        actions = Actions(1)
        for seat in range(2):
            act = steps[t][seat].get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                rtd.write_unit(actions, seat, slot, entry)
            rtd.write_market(actions, seat, act.get("market"))
        game.step(actions)

    shifted = float(game.farms[0].money[0])
    assert shifted < EXPECTED_BANK * 0.5, (
        f"replaying from index 0 banked ${shifted:,.0f}, close to the correct ${EXPECTED_BANK:,.0f} -- "
        f"if the placeholder no longer costs anything, this test is obsolete rather than passing")
