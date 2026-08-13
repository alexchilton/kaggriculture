"""A BUY_SEED order is a request for seed; a PLANT is a tile that changed kind. They are not
the same number and nothing may print them as though they were.

The mechanism: the agent re-posts a standing market order on every turn until it fills, so the
same intended purchase appears in the action stream up to 24 times a day. Summing `order[2]`
over turns therefore counts an intention, repeatedly, and calls the result a quantity.

Measured on four real ladder games (`data/seed_scripts/ours_ladder_new/`), the two disagree by
up to 20x:

    92564858   real MELON plants 18    BUY_SEED MELON offered 251
    92566708   real STRAWBERRY 36      BUY_SEED STRAWBERRY offered 460

A plant is not an inference. `_apply_unit_action`'s PLANT branch writes `_new_plant` onto a tile
that was `None`, so every plant that happened is standing on the board in the very next recorded
observation, with the day it was planted on it. Counting tile transitions is exact and needs no
simulation.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, ".")

from kagg.analysis.replay_fills import offered, real_plants

LADDER = pathlib.Path("data/seed_scripts/ours_ladder_new")

#: Counted off tile transitions in the recordings, and re-derived independently before this test
#: was written. These are the numbers the tools must print.
REAL_PLANTS = {
    "92564858": {"WHEAT": 138, "STRAWBERRY": 34, "MELON": 18, "CARROT": 5},
    "92566708": {"WHEAT": 139, "STRAWBERRY": 36, "MELON": 19, "CARROT": 6},
    "92562037": {"WHEAT": 138, "STRAWBERRY": 36, "MELON": 19, "CARROT": 6},
    "92550780": {"WHEAT": 138, "STRAWBERRY": 36, "MELON": 19, "CARROT": 6},
}
#: What summing `BUY_SEED` order quantities off the same recordings produces instead. Kept here so
#: the test asserts on the SIZE of the error, not merely that two numbers differ.
SEED_OFFERS = {
    "92564858": {"MELON": 251, "WHEAT": 148, "STRAWBERRY": 92, "CARROT": 42},
    "92566708": {"STRAWBERRY": 460, "MELON": 386, "WHEAT": 378, "CARROT": 54},
    "92562037": {"WHEAT": 148, "MELON": 136, "STRAWBERRY": 97, "CARROT": 42},
    "92550780": {"WHEAT": 149, "CARROT": 98, "MELON": 69, "STRAWBERRY": 57},
}


def synthetic_replay(n_turns, seed_order_per_turn, plants):
    """A two-seat recording where seat 0 asks for seed on every turn and plants `len(plants)` tiles.

    Deliberately hand-built rather than simulated: the whole point is a recording where the offer
    total and the plant total are known independently and are wildly different, which is what the
    real games look like and what no fixture generated from an agent would guarantee.

    `plants` is a list of `(turn, x, y, crop)`. A tile stays planted once planted.
    """
    board = [[None] * 4 for _ in range(4)]
    steps = []
    for t in range(n_turns):
        for (turn, x, y, crop) in plants:
            if turn == t:
                board[y][x] = {"kind": "PLANT", "crop": crop, "planted_day": t // 24,
                               "yield_units": 0}
        farms = [{"tiles": [[dict(c) if isinstance(c, dict) else c for c in row] for row in board],
                  "money": 3000, "hands": []},
                 {"tiles": [[None] * 4 for _ in range(4)], "money": 3000, "hands": []}]
        obs = {"step": t, "day": t // 24, "hour": t % 24, "farms": farms,
               "market": {"inventory": {"WHEAT": 100}, "prices": {"WHEAT": 10}},
               "town": {"unlocked_shops": []},
               "private": {"seeds": {}, "shed": {}, "inventories": [{}]}}
        act = {"farmer": ["PASS"], "hands": [],
               "market": [["BUY_SEED", "WHEAT", seed_order_per_turn]]}
        steps.append([{"observation": obs, "action": act},
                      {"observation": {"private": {"seeds": {}, "shed": {}, "inventories": [{}]}},
                       "action": {"farmer": ["PASS"], "hands": [], "market": []}}])
    return {"info": {"TeamNames": ["us", "them"]}, "rewards": [1.0, 0.0],
            "configuration": {"turnsPerDay": 24, "townShopSellInterval": 4,
                              "townCenterSellInterval": 24},
            "steps": steps}


def test_a_reoffered_seed_order_is_not_counted_once_per_turn():
    """50 turns of "buy me 5 wheat seed" is not 250 plants. It is however many tiles changed."""
    replay = synthetic_replay(50, 5, [(3, 0, 0, "WHEAT"), (7, 1, 0, "WHEAT")])

    assert real_plants(replay, 0) == collections.Counter({"WHEAT": 2})
    # The offer total is still available -- it is a real thing an agent did -- but under a name
    # that cannot be mistaken for a plant.
    assert offered(replay, 0)["BUY_SEED"] == collections.Counter({"WHEAT": 250})


def test_a_tile_replanted_after_harvest_counts_twice():
    """`HARVEST` on a non-ongoing crop sets the tile back to `None`, so the same square carries
    more than one plant in a season and the board at the close is not the season's total.

    This is the discriminator against the other tempting shortcut -- counting the plants standing
    in the final observation. On the four real games that reads about a fifth of the truth.
    """
    replay = synthetic_replay(30, 1, [(2, 0, 0, "WHEAT")])
    # clear the tile mid-season, then plant it again on a later day
    for t in range(10, 26):
        replay["steps"][t][0]["observation"]["farms"][0]["tiles"][0][0] = None
    for t in range(26, 30):
        replay["steps"][t][0]["observation"]["farms"][0]["tiles"][0][0] = {
            "kind": "PLANT", "crop": "WHEAT", "planted_day": 1, "yield_units": 0}

    assert real_plants(replay, 0) == collections.Counter({"WHEAT": 2})


@pytest.mark.parametrize("game", sorted(REAL_PLANTS))
def test_the_four_ladder_games_report_plants_not_seed_orders(game):
    """The four games this defect was demonstrated on. Requires the downloaded recordings."""
    path = LADDER / f"{game}.json"
    if not path.exists():
        pytest.skip(f"{path} not downloaded")
    replay = json.loads(path.read_text())
    seat = replay["info"]["TeamNames"].index("alex chilton")

    assert dict(real_plants(replay, seat)) == REAL_PLANTS[game]
    # And the number the old column printed is genuinely a different number, so a tool that
    # regressed to it could not pass by coincidence.
    assert dict(offered(replay, seat)["BUY_SEED"]) == SEED_OFFERS[game]
