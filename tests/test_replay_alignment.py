"""A replay's observation is recorded AFTER that turn's action. Pairing them naively is unsatisfiable.

Every teacher-forced comparison in this project fed `decide` the observation at index `t` and compared
its output against the action at index `t`. Measured on episode 89873723 seat 0:

    step 1: obs hands=2  hires_today=2  seedsWHEAT=6
            action [HIRE], [HIRE], [BUY_ANIMAL COW 1], [BUY_SEED MELON 6], [BUY_SEED WHEAT 6], ...
    step 2: obs hands=3  hires_today=3  seedsWHEAT=11
            action [HIRE], [BUY_SEED WHEAT 5], ...

The observation carries the *post*-action totals. So the naive pairing asks a plan to buy six wheat
seeds on a board already holding six, and to hire two hands already hired -- impossible at any gene
setting. That is what produced "0 of 720 turns identical, first divergence at turn 0", and it was a
property of the harness rather than of the genome. This file pins the alignment so the off-by-one
cannot come back, and so a future reader does not re-derive "replication is impossible" from it.

`replay_plan.teacher_forced_pairs` is the fixed pairing: the pre-action state for turn `t` is the
observation recorded at `t - 1`, with turn 0 using its own (its action is `PASS` with no orders, so
pre- and post-action coincide).
"""

import json
import pathlib

import pytest

from kagg.search import replay_plan as RP

EPISODE = pathlib.Path("data/episodes/89873723.json")
SEAT = 0

pytestmark = pytest.mark.skipif(not EPISODE.exists(), reason="replay not present")


def _steps():
    return json.loads(EPISODE.read_text())["steps"]


def test_the_observation_is_recorded_after_its_own_action():
    """The premise. If this ever fails, the alignment changed and `teacher_forced_pairs` is wrong."""
    steps = _steps()
    obs = steps[1][SEAT]["observation"]
    action = steps[1][SEAT]["action"]

    hires_in_action = sum(1 for o in action["market"] if o and o[0] == "HIRE")
    seeds_in_action = sum(int(o[2]) for o in action["market"]
                          if o and o[0] == "BUY_SEED" and o[1] == "WHEAT")

    assert hires_in_action == 2, f"fixture changed: {action['market']}"
    assert obs["farms"][SEAT]["hires_today"] == hires_in_action, (
        "the observation at step 1 does not reflect step 1's own hires, so it is a pre-action "
        "snapshot after all and `teacher_forced_pairs` must not shift the index")
    assert obs["private"]["seeds"]["WHEAT"] == seeds_in_action


def test_the_shifted_pairing_gives_a_pre_action_board():
    """Turn 1 must be judged against a board with no hands hired and no seeds bought yet."""
    pairs = {t: (before, action) for t, before, action in RP.teacher_forced_pairs(EPISODE, SEAT)}
    before, action = pairs[1]

    assert before["farms"][SEAT]["hires_today"] == 0, (
        f"turn 1's pre-action board already shows {before['farms'][SEAT]['hires_today']} hires")
    assert len(before["farms"][SEAT]["hands"]) == 0
    assert before["private"]["seeds"]["WHEAT"] == 0
    assert float(before["farms"][SEAT]["money"]) == 3000.0
    # And it is still turn 1's action being asked for, not turn 0's.
    assert sum(1 for o in action["market"] if o and o[0] == "HIRE") == 2


def test_turn_zero_uses_the_initial_state():
    """Turn 0's action is a no-op, so its own observation is both pre- and post-action."""
    pairs = {t: (before, action) for t, before, action in RP.teacher_forced_pairs(EPISODE, SEAT)}
    before, action = pairs[0]

    assert float(before["farms"][SEAT]["money"]) == 3000.0
    assert action["market"] == []


def test_every_decided_turn_is_paired():
    """No turns silently dropped -- a shifted iterator is an easy place to lose the first or last."""
    steps = _steps()
    decided = sum(1 for s in steps if isinstance(s[SEAT].get("action"), dict))
    paired = sum(1 for _ in RP.teacher_forced_pairs(EPISODE, SEAT))

    assert paired == decided, f"paired {paired} of {decided} decided turns"
