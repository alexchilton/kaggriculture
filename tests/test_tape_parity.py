"""Replay a real leader's 720-turn action tape and land on the env's exact bank, turn for turn.

This is the gate that says a trajectory search is worth running: given a sequence of actions, our
simulator produces the season those actions actually produce, so a candidate's score is the score it
would really get. Without it, every candidate would be ranked by a simulator settling a different
game.

**The reference is the installed environment, not the recording. Changed 2026-08-09.** It used to be
the money written into `data/episodes/89873723.json`, pinned as `EXPECTED_BANK = 147_178`. That
number is no longer reachable and its unreachability is not a bug:

    episode 89873723 `configuration`:  townCenterSellInterval 12,  module_version 1.32.3

`kaggle-environments` 1.32.6 ("Kaggriculture town rebalance") took `townCenterSellInterval` to 24 and
deleted `TOWN_CENTER_DEMAND_SCHEDULE`, an 8x cut in late-season town demand, and changed four rules
besides (see `tests/test_parity_1326_rules.py`). Measured: driving that identical action tape into
the **installed** environment banks **$92,313**, against the $147,178 it banked on the ladder that
recorded it. A simulator that reproduced $147,178 today would be wrong.

So the recorded bank is a fact about a game that no longer exists, and pinning it turned a rule
change into a test failure that read like our bug -- the exact failure mode `tests/test_sim_town.py`
already warns about for the centre schedule. What is worth gating is the *claim*, which never
mentioned a particular number: **given these actions, our sim equals the environment.** Replaying the
tape into the installed env costs about four seconds and is version-proof, so that is what this does.

**Two traps not to re-derive.**

`steps[0].action` is the placeholder recorded when the environment resets, before any agent has seen
a board. Applying it shifts every later turn by one, which puts each day boundary a turn out of
place, and costs roughly two thirds of the bank. Four separate "first divergences" were chased and
explained -- turns 23, 47, 48, 97 -- before this was found, and every one of them was the shift.
`test_applying_the_reset_placeholder_breaks_it` pins it.

The shop unlock schedule has to be **read out of the env run that is being compared against**, never
hard-coded. `_spawn_weeds` consumes one RNG draw per empty tile before `rng.choice` picks the shop,
so the draw depends on both players' board occupancy; the same seed with weeds on and off produces
different shops. And from 1.32.6 the draw is *with replacement*, so the schedule is a list that may
name one shop twice -- this tape's own run opens FARMERS_MARKET three times.
"""

import importlib.util
import json
import pathlib
import sys

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.sim.game import Actions, Game
from kagg.sim.town import SHOP_INDEX

EPISODE = pathlib.Path("data/episodes/89873723.json")
SEAT = 0
TURNS_PER_DAY = 24
# `steps[0].action` is the reset placeholder and is never applied. See the module docstring.
FIRST_ACTION_TURN = 1
# `env.info["seed"]` from the recording. Fixing it keeps the replay deterministic run to run;
# CLAUDE.md records that leaving the env to draw its own seed makes every number noise.
SEED = 687_155_480

pytestmark = pytest.mark.skipif(not EPISODE.exists(), reason="replay not present")

_REFERENCE = None


def _rtd():
    """`scripts/replay_tape_day.py` holds the tape -> Actions writers; import it by path."""
    spec = importlib.util.spec_from_file_location("rtd", "scripts/replay_tape_day.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["rtd"] = module
    spec.loader.exec_module(module)
    return module


def _reference():
    """Drive the recorded tape through the installed env. `(per-turn money, unlock schedule)`.

    Cached: three tests want it and it costs about four seconds. Weeds are off on both sides, the
    one deliberate divergence in the simulator -- their spawn RNG is a per-day Python generator
    consuming a draw per empty tile, which cannot be ported without losing the speedup the
    simulator exists for.
    """
    global _REFERENCE
    if _REFERENCE is not None:
        return _REFERENCE

    from kaggle_environments import make

    steps = json.loads(EPISODE.read_text())["steps"]
    env = make("kaggriculture",
               configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=False)
    env.reset(num_agents=2)

    money, unlocks, seen = [], {}, 0
    for t in range(FIRST_ACTION_TURN, len(steps)):
        actions = []
        for seat in range(2):
            act = steps[t][seat].get("action")
            actions.append(act if isinstance(act, dict)
                           else {"farmer": ["PASS"], "hands": [], "market": []})
        env.step(actions)
        obs = env.state[0].observation
        money.append(float(obs["farms"][SEAT]["money"]))
        # The list, not the set: 1.32.6 draws with replacement and each instance consumes.
        shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
        if len(shops) > seen:
            unlocks.setdefault(obs.get("day", 0), []).extend(shops[seen:])
            seen = len(shops)
        if env.done:
            break

    schedule = {d: [SHOP_INDEX[s] for s in names] for d, names in unlocks.items()}
    _REFERENCE = (steps, money, schedule)
    return _REFERENCE


def _frames(steps, rtd, start=FIRST_ACTION_TURN):
    """One `Actions` per recorded turn, both seats, market orders in their recorded slot order."""
    for t in range(start, len(steps)):
        actions = Actions(1)
        for seat in range(2):
            act = steps[t][seat].get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                rtd.write_unit(actions, seat, slot, entry)
            rtd.write_market(actions, seat, act.get("market"))
        yield t, actions


def test_the_numpy_sim_tracks_the_environments_bank_every_turn():
    """**The claim.** Not just the final number -- every turn of it."""
    steps, reference, schedule = _reference()
    rtd = _rtd()
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)

    checked = 0
    for (t, actions), expected in zip(_frames(steps, rtd), reference):
        game.step(actions)
        ours = float(game.farms[0].money[0])
        checked += 1
        assert ours == pytest.approx(expected, abs=0.5), (
            f"turn {t} (day {t // TURNS_PER_DAY} hour {t % TURNS_PER_DAY}): "
            f"ours ${ours:,.0f} vs the env's ${expected:,.0f}")

    assert checked > 700, f"only {checked} turns were compared -- the gate proved little"


def test_the_jax_sim_reaches_the_same_bank():
    """The batched evaluator a trajectory search scores against has to agree, or it ranks fiction."""
    jax_sim = pytest.importorskip("kagg.sim.jax_sim")
    steps, reference, schedule = _reference()
    rtd = _rtd()
    state = jax_sim.reset(1, unlock_schedule=schedule)

    for _t, actions in _frames(steps, rtd):
        state = jax_sim.step(state, jax_sim.from_numpy_actions(actions), weed_chance=0.0)

    ours = float(np.asarray(jax_sim.money(state))[0, 0])
    assert ours == pytest.approx(reference[-1], abs=0.5), (
        f"jax banked ${ours:,.0f} against the env's ${reference[-1]:,.0f}")


def test_the_recorded_bank_is_a_1_32_3_number_and_is_not_the_target():
    """Pins *why* the fixture was re-baselined, so nobody restores `EXPECTED_BANK = 147_178`.

    If a future release makes the recorded bank reachable again this goes red, which is the correct
    signal: it would mean the town rebalance had been reverted and every economic figure in the docs
    needed rechecking. It is not a test that our simulator is right -- the two above are that.
    """
    config = json.loads(EPISODE.read_text())["configuration"]
    assert config["townCenterSellInterval"] == 12, (
        "the recording no longer carries the pre-rebalance centre interval")

    _steps, reference, _schedule = _reference()
    recorded = 147_178.0
    assert reference[-1] < recorded * 0.8, (
        f"the same actions bank ${reference[-1]:,.0f} on the installed env against the recorded "
        f"${recorded:,.0f}; if those have converged, the rules moved back and this test is obsolete "
        f"rather than passing")


def test_applying_the_reset_placeholder_breaks_it():
    """Pins the off-by-one, so nobody re-introduces it and spends a session chasing turn 48.

    Deliberately asserts the *wrong* alignment is wrong. A regression here would otherwise be silent:
    the season still runs, still looks plausible, and simply banks a fraction of what it should.
    """
    steps, reference, schedule = _reference()
    rtd = _rtd()
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)

    for _t, actions in _frames(steps, rtd, start=0):   # from 0, i.e. including the placeholder
        game.step(actions)

    shifted = float(game.farms[0].money[0])
    assert shifted < reference[-1] * 0.5, (
        f"replaying from index 0 banked ${shifted:,.0f}, close to the correct "
        f"${reference[-1]:,.0f} -- if the placeholder no longer costs anything, this test is "
        f"obsolete rather than passing")
