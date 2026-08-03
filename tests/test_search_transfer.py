"""Does a plan measured on the fast simulator behave the same way in the real environment?

This is the gate for the whole search, and it is a *different* test from `tests/test_sim_parity.py`.
That one proves the simulator reproduces the reference for a random action script. It says nothing
about the composition used here, for three reasons the parity harness makes explicit:

- its scripts drive **one** unit per player, so nothing about multi-unit routing, hand spawning or
  the atomic PLANT rule is exercised;
- it issues no market order list in the shape an agent does, so neither the 10-order cap nor the
  reference's slot-paired settlement is compared;
- hand spawn positions are a **known** divergence -- the simulator puts every hire on the NW shed
  tile, the reference balances them across all four -- and the parity gate excludes them.

So the question that matters for search is empirical: play the *same plans* through both, and see
how far the final banks drift. Anything the search discovers is only worth having if that drift is
small relative to the effects being searched for.

The tolerances below are the measured drift, pinned so that a regression is loud. They are not
tight, and they are not meant to be: the point is to catch a change that breaks transfer, not to
claim the two implementations are identical. They are not, on purpose.
"""

import numpy as np
import pytest

from kagg.search import agent as A
from kagg.search import library, rollout
from kagg.search import plan as P


def _observed_unlocks(env):
    """The shop unlock order the episode actually drew, as `rollout` wants it."""
    seen = {}
    for record in env.steps:
        obs = record[0]["observation"]
        for shop in obs.get("town", {}).get("unlocked_shops", []):
            seen.setdefault(shop, obs.get("day", 0))
    return {day: rollout.shop_index(shop) for shop, day in seen.items()}


def _both(first, second, seed):
    """Final banks from the real environment and from the simulator, same plans, same unlocks."""
    from kaggle_environments import make

    env = make("kaggriculture",
               configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=False)
    env.run([A.make_agent(first), A.make_agent(second)])
    final = env.steps[-1]
    real = (final[0]["reward"], final[1]["reward"])

    plans = P.decode(np.stack([first, second]))
    money = rollout.play(
        (plans.take([0]), plans.take([1])), _observed_unlocks(env), weed_chance=0.0
    )
    return real, (float(money[0, 0]), float(money[0, 1]))


@pytest.mark.slow
@pytest.mark.parametrize("seed", [101, 202])
def test_the_simulator_predicts_the_real_banks_within_ten_percent(seed):
    real, sim = _both(library.melon_wheat(), library.wheat_only(), seed)

    for side in (0, 1):
        drift = abs(sim[side] - real[side]) / max(real[side], 1.0)
        assert drift < 0.10, f"seat {side}: sim {sim[side]:.0f} vs real {real[side]:.0f}"

    # The residual is hand spawning: the simulator stacks every hire on the NW shed tile, so its
    # units start marginally closer to the NW quadrant than the reference's do.
    assert (sim[0] > sim[1]) == (real[0] > real[1])


@pytest.mark.slow
def test_the_two_plans_are_far_apart_so_the_agreement_above_means_something():
    """Two plans that scored the same would satisfy the tolerances while proving nothing."""
    real, sim = _both(library.melon_wheat(), library.wheat_only(), 101)
    assert real[0] > 3 * real[1]
    assert sim[0] > 3 * sim[1]


def test_a_plan_that_does_nothing_banks_its_starting_money_in_both():
    """The floor case: if either implementation leaked money the two would not agree at $3000."""
    idle = library.genome([None] * P.TILES, hands=0, land_days=(999, 999, 999))
    real, sim = _both(idle, idle, 303)
    assert real == (3000.0, 3000.0)
    assert sim == (3000.0, 3000.0)
