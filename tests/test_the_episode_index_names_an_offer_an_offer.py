"""A field called `sell` on a row about a re-posting agent is a trap, whatever the docstring says.

`scripts/episode_index.py` extracts one compact row per seat from a day's ~686 ladder replays, and
the row is the only thing every later analysis reads -- the 20 GB of JSON is not opened twice. Its
`sell`, `buy`, `seed` and `animals` fields were sums of order quantities off the action stream.

The docstring said so, at length, and pointed at `order_turns` as the tell. That is not enough. The
field name travels with the number into every table built from the index, and the docstring does
not. So the offer fields carry `_offered` in their names, and the exact quantities sit beside them
under names that mean what they say.

This project has now made the offers-for-fills mistake four times. Three of those had a warning
written down somewhere.
"""

import json
import sys

import pytest

sys.path.insert(0, ".")

import scripts.episode_index as ei


def synthetic(tmp_path):
    """A recording where seat 0 re-posts a standing SELL and plants two tiles.

    Hand-built rather than simulated: it needs an agent that re-offers, and no sparring agent in
    this repo does -- which is exactly why a game between the stock agents cannot catch this.
    """
    board = [[None] * 3 for _ in range(3)]
    steps = []
    for t in range(30):
        if t == 5:
            board[0][0] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0, "yield_units": 0}
        if t == 9:
            board[1][0] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0, "yield_units": 0}
        farms = [{"tiles": [[dict(c) if isinstance(c, dict) else c for c in row] for row in board],
                  "money": 3000, "hands": [], "hires_today": 0, "unlocked_quadrants": ["NW"]},
                 {"tiles": [[None] * 3 for _ in range(3)], "money": 3000, "hands": [],
                  "hires_today": 0, "unlocked_quadrants": ["NW"]}]
        obs = {"step": t, "day": 0, "hour": t, "farms": farms,
               "market": {"inventory": {"WHEAT": 100}, "prices": {"WHEAT": 10}},
               "town": {"unlocked_shops": []},
               "private": {"seeds": {}, "shed": {}, "inventories": [{}]}}
        act = {"farmer": ["PASS"], "hands": [],
               "market": [["SELL", "WHEAT", 9], ["BUY_SEED", "WHEAT", 4]]}
        steps.append([{"observation": obs, "action": act},
                      {"observation": {"private": {"seeds": {}, "shed": {},
                                                   "inventories": [{}]}},
                       "action": {"farmer": ["PASS"], "hands": [], "market": []}}])
    path = tmp_path / "77777777.json"
    path.write_text(json.dumps({
        "info": {"TeamNames": ["us", "them"]}, "rewards": [1.0, 0.0],
        "configuration": {"turnsPerDay": 24, "townShopSellInterval": 4,
                          "townCenterSellInterval": 24, "weedSpawnChance": 0.0},
        "steps": steps}))
    return str(path)


def test_no_field_holding_an_order_total_is_named_after_the_thing_it_is_not(tmp_path):
    rows = ei.one(synthetic(tmp_path))
    assert rows, "the index rejected a well-formed recording"
    row = rows[0]

    for name in ("sell", "buy", "seed", "animals", "plants"):
        assert name not in row, (
            f"`{name}` is back on the index row. Whatever it holds, the name is the one a later "
            f"table will print, and these four held order quantities.")
    assert row["sell_offered"]["WHEAT"] == 9 * 30
    assert row["seed_offered"]["WHEAT"] == 4 * 30


def test_the_row_carries_the_real_plant_count_beside_the_offer(tmp_path):
    """Two tiles changed. The seed order asked for 120."""
    row = ei.one(synthetic(tmp_path))[0]
    assert row["plants_real"] == {"WHEAT": 2}
    assert row["seed_offered"]["WHEAT"] == 120


def test_a_re_poster_is_visible_from_the_row_alone(tmp_path):
    """`orders` far above `order_turns` is the signature of a standing quota. It is kept because it
    is the one number that says an offer column cannot be read as a quantity -- but it is now a
    corroboration, not the reader's only defence."""
    row = ei.one(synthetic(tmp_path))[0]
    assert row["orders"] == 60 and row["order_turns"] == 30


def test_the_index_still_returns_nothing_for_a_malformed_file(tmp_path):
    bad = tmp_path / "broken.json"
    bad.write_text("{not json")
    assert ei.one(str(bad)) == []
    empty = tmp_path / "empty.json"
    empty.write_text(json.dumps({"info": {"TeamNames": ["a"]}, "rewards": [], "steps": []}))
    assert ei.one(str(empty)) == []
