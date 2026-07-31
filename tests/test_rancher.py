"""Tests for the rancher agent.

It exists to answer a contradiction: our own measurements said animals were net negative, but the
three largest losses on the ladder were all small, wage-free animal farms. The earlier measurement
was taken against a pool of our own agent with our own routing, so it could not distinguish "animals
are bad" from "animals are bad *the way we route them*".
"""

import numpy as np
import pytest
from kaggle_environments import make

from kagg.agents import rancher


def _play(seed, herd=None, opponent="starter"):
    if herd is not None:
        rancher.PARAMS["herd"] = herd
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([rancher.agent, opponent])
    final = env.steps[-1]
    obs = final[0]["observation"]
    animals = sum(
        1 for row in obs["farms"][0]["tiles"] for cell in row
        if isinstance(cell, dict) and cell.get("animal")
    )
    return final[0]["reward"], animals


def test_the_herd_actually_gets_placed():
    """Regression for three separate bugs that each pinned the herd at one animal.

    In order: three of the four shed-access tiles are in locked quadrants, so the plot list was
    mostly unusable; an occupied pasture keeps `kind == "PASTURE"`, so the farmer's own tile always
    looked like it needed work and it never moved; and PLACE draws from carried inventory, so a
    bought animal sat in the shed forever because the empty pasture was not a shed tile.
    """
    rancher.PARAMS["herd"] = 6
    _, animals = _play(4000)

    assert animals >= 4, "herd failed to grow -- check plot selection and animal pickup"


def test_it_hires_nobody():
    """The whole thesis: wages are the tax a small farm avoids paying."""
    env = make("kaggriculture", configuration={"seed": 4000}, debug=False)
    hired = []

    def spy(obs, config=None):
        action = rancher.agent(obs, config)
        hired.extend(o for o in action["market"] if o[0] == "HIRE")
        return action

    env.run([spy, "starter"])

    assert hired == []


def test_it_beats_the_starter_baseline_decisively():
    rancher.PARAMS["herd"] = 6
    money, _ = _play(4001)

    assert money > 20_000


def test_herd_size_has_an_optimum_set_by_the_action_budget():
    """More animals is not better: one farmer has 24 actions a day, and each animal needs several.

    Measured 4 -> $31.6k, 6 -> $45.7k, 10 -> $15.9k. The constraint is the action budget, not money,
    which is exactly the routing cost that made animals look unviable in the heuristic.
    """
    small, _ = _play(4000, herd=6)
    large, _ = _play(4000, herd=16)

    assert small > large
    rancher.PARAMS["herd"] = 6
