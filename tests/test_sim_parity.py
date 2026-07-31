"""End-to-end parity: the gate CLAUDE.md sets before training on the fast sim.

Kept small enough to run in the normal suite. The full gate is a longer run recorded in
`docs/experiment_log.md`: 60 full-length episodes, all exact.

This file exists because unit tests did not catch the bug that mattered. Every component had
passing tests and the *composition* was still wrong -- `plant` spent a seed even when the tile was
occupied and the plant did not land, so the sim quietly starved over a few hundred steps. A
200-step check passed; the 719-step gate failed 40 out of 40. Test the composition, at length.
"""

import numpy as np
import pytest

from kagg.sim.parity import compare, random_script, run_reference, run_sim


def test_the_harness_never_acts_for_a_hand_the_farm_has_not_hired():
    """The gate must drive the reference the way an agent does: one action per unit it owns.

    Every agent builds its action from `[farmer, *farm["hands"]]`, so it submits exactly as many
    unit actions as it has units. The reference, given a longer list, ignores the surplus actions
    for movement and work -- but still counts them in the atomic PLANT rule, which is computed over
    the *submitted* actions rather than over the units that exist. A harness that always fills six
    unit slots therefore has the reference block plants that no real game would block, and the
    simulator, which masks dead unit slots, correctly plants them.

    Two units driven, no hand hired and one wheat seed held: the reference sees two PLANT requests
    against one seed and drops both.
    """
    from kagg.sim import ops as O
    from kagg.sim.tiles import CROP_INDEX

    wheat = CROP_INDEX["WHEAT"]

    def entry(ops, buy=None):
        return {
            "units": [(list(ops), [wheat] * len(ops)), ([O.NOOP] * len(ops), [wheat] * len(ops))],
            "sell": [{}, {}],
            "buy_seed": [dict(buy or {}), {}],
            "hire": [False, False],
            "buy_land": [False, False],
        }

    script = [
        entry([O.NOOP, O.NOOP], buy={"WHEAT": 1}),
        entry([O.PLANT_OP, O.PLANT_OP]),
    ]

    reference, unlocks = run_reference(script, seed=900)
    sim = run_sim([script], unlocks=unlocks)[0]

    assert compare(sim[: len(reference)], reference) == []


@pytest.mark.parametrize("seed", [0, 1])
def test_full_length_episode_is_exact(seed):
    """719 steps, comparing bank, market inventory and both farms' tile composition every step."""
    rng = np.random.default_rng(seed)
    script = random_script(rng, steps=719)

    reference, unlocks = run_reference(script, seed=700 + seed)
    sim = run_sim([script], unlocks=unlocks)[0]

    assert compare(sim[: len(reference)], reference) == []


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_full_length_episode_with_a_hired_crew_is_exact(seed):
    """The case CLAUDE.md recorded as broken: a full season with several units working at once.

    `hire_rate` is deliberately high. Hands are dismissed nightly and the hire fee is Fibonacci
    within the day, so at the 0.05 default a farm almost never fields a crew and this becomes a
    single-unit test wearing a multi-unit name -- which is how the last two divergences survived a
    gate that was passing. At 0.5 a second unit is live on 16% of player-turns and a sixth on 4.6%.
    """
    rng = np.random.default_rng(4242 + seed)
    script = random_script(rng, steps=719, max_units=6, allow_hire=True, hire_rate=0.5)

    reference, unlocks = run_reference(script, seed=1500 + seed)
    sim = run_sim([script], unlocks=unlocks)[0]

    assert compare(sim[: len(reference)], reference) == []


def test_a_batch_of_different_scripts_stays_exact():
    """Games in a batch must not contaminate each other -- the whole point of batching."""
    rng = np.random.default_rng(5)
    scripts = [random_script(rng, steps=240) for _ in range(3)]

    sims = run_sim(scripts, unlocks={})
    for i, script in enumerate(scripts):
        reference, unlocks = run_reference(script, seed=800 + i)
        # Unlocks differ per seed, so compare only what does not depend on the shop schedule.
        assert compare(
            sims[i][: len(reference)], reference, label=f"game {i}: ", fields=("tiles",)
        ) == []


def test_seeds_are_only_spent_when_a_plant_actually_lands():
    """Regression for the bug that failed the gate 40/40 while every unit test passed."""
    from kagg.sim import ops as O
    from kagg.sim.game import Actions, Game
    from kagg.sim.tiles import CROP_INDEX, PLANT

    game = Game(1, weed_chance=0.0)
    game.farms[0].seeds[0, CROP_INDEX["WHEAT"]] = 5

    actions = Actions(1)
    actions.unit_op[0, 0, 0] = O.PLANT_OP
    actions.unit_crop[0, 0, 0] = CROP_INDEX["WHEAT"]

    game.step(actions)
    assert game.farms[0].seeds[0, CROP_INDEX["WHEAT"]] == 4      # planted, so one seed spent
    assert game.tiles[0].kind[0, game.farms[0].unit_pos[0, 0, 1] * 10
                              + game.farms[0].unit_pos[0, 0, 0]] == PLANT

    # The tile is now occupied, so the next PLANT is a no-op and must cost nothing.
    game.step(actions)
    assert game.farms[0].seeds[0, CROP_INDEX["WHEAT"]] == 4
