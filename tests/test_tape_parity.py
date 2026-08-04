"""Parity against a real leader's recorded tape, not a random script.

`tests/test_sim_parity.py` drives both engines with `random_script`, which is the right gate for
coverage but never produces a leader's opening -- CLAUDE.md's recurring lesson is that a gate only
tests what it exercises, and it lists three separate occasions where a green random-script gate hid a
real divergence. This file plays episode 89873723's actual 720-turn action tape, both seats, through
`kaggle_environments` and through `kagg.sim`, and compares their **live** state.

Two things had to be neutralised for the comparison to mean anything, and both are recorded here so
nobody re-derives them:

1. **Weeds off on both sides.** Our sim deliberately does not reproduce the reference's weed RNG stream.
2. **The shop-unlock schedule imposed on both.** `_end_of_day` builds one `random.Random` and hands it
   to `_spawn_weeds` *before* `rng.choice(sorted(remaining))`, and `_spawn_weeds` draws once per empty
   tile -- so which shop unlocks depends on both players' board occupancy, not the seed alone. It is
   not recoverable offline: brute-forcing a seed against the observed order gives 13981, and the live
   env with that seed unlocks a different shop. Episodes record `configuration.seed: null` regardless.

Do NOT compare against the replay JSON's observations instead. Measured directly, the recorded
observation at step `t` reflects `action[t]` but is captured **before that step's `_end_of_day`**, so
shed, carried inventories and the daily animal/plant refresh all read one step stale. Comparing those
fields against the JSON reports a divergence on every day boundary that is purely an artifact of when
the recorder looked -- which is what made an earlier pass report first-divergences at turns 23, 47, 48
and 97, none of them real.
"""

import json
import pathlib

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.sim.game import Actions, Game
from kagg.sim.market import ITEMS, PRODUCTS
from kagg.sim.town import SHOPS

EPISODE = pathlib.Path("data/episodes/89873723.json")
TURNS_PER_DAY = 24

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


def _reference(steps, n_turns, schedule):
    from kaggle_environments import make

    plan = [[steps[t][seat].get("action") for seat in range(2)] for t in range(len(steps))]
    env = make("kaggriculture", configuration={"seed": 0, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    trace = []
    for t in range(n_turns):
        acts = [a if isinstance(a, dict) else {"farmer": ["PASS"], "hands": [], "market": []}
                for a in plan[t]]
        env.step(acts)
        obs0 = env.state[0].observation
        day = (t + 1) // TURNS_PER_DAY
        obs0.town["unlocked_shops"] = [SHOPS[i] for d, i in sorted(schedule.items()) if d <= day]
        privates = [s.observation.private for s in env.state]
        trace.append((
            [float(obs0.farms[i]["money"]) for i in range(2)],
            [{k: int(v) for k, v in (privates[i].get("shed") or {}).items() if v} for i in range(2)],
            dict(obs0.market["inventory"]),
        ))
        if env.done:
            break
    return trace


def _ours(steps, n_turns, schedule):
    rtd = _rtd()
    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)
    trace = []
    for t in range(n_turns):
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
        trace.append((
            [float(game.farms[i].money[0]) for i in range(2)],
            [{ITEMS[i]: int(v) for i, v in enumerate(game.farms[s].shed[0]) if v}
             for s in range(2)],
            {p: int(game.inventory[0, i]) for i, p in enumerate(PRODUCTS)},
        ))
    return trace


def _compare(n_turns):
    steps = json.loads(EPISODE.read_text())["steps"]
    n = min(n_turns, len(steps))
    schedule = _rtd().unlock_schedule(steps)
    ref, ours = _reference(steps, n, schedule), _ours(steps, n, schedule)

    for t, ((rm, rs, ri), (om, os_, oi)) in enumerate(zip(ref, ours)):
        where = f"turn {t} (day {t // TURNS_PER_DAY} hour {t % TURNS_PER_DAY})"
        assert om[0] == pytest.approx(rm[0], abs=0.5), (
            f"{where}: money ours ${om[0]:,.0f} vs reference ${rm[0]:,.0f}")
        assert os_[0] == rs[0], f"{where}: shed ours {os_[0]} vs reference {rs[0]}"
        bad = {k: (oi[k], ri[k]) for k in ri if oi.get(k) != ri[k]}
        assert not bad, f"{where}: market inventory (ours, reference) {bad}"
    return n


def test_the_first_three_days_of_a_real_tape_are_exact():
    """Fast gate. Three days covers the opening, the first day boundaries and the first shop unlock."""
    assert _compare(3 * TURNS_PER_DAY) == 3 * TURNS_PER_DAY


@pytest.mark.slow
def test_the_whole_season_of_a_real_tape_is_exact():
    """**The claim.** All 720 turns of the $147,178 seat, money, shed and market inventory.

    This is what makes "can we replicate a winner turn by turn" answerable: given their actions, our
    simulator produces their season exactly, so anything that remains is choosing the actions.
    """
    assert _compare(720) == 720
