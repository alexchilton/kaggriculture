"""The town's demand is a number of units, and it is exactly recoverable.

`_town_consume` is arithmetic: every `townShopSellInterval` steps each unlocked shop INSTANCE takes
one of each product it sells (two if it sells only one), and every `townCenterSellInterval` steps
the town centre takes one of everything but fertilizer. Nothing is random and nothing depends on
either player.

This matters because the drain is the load-bearing term in `trade_fills` -- the market ledger only
balances if the drain subtracted is the drain that happened -- and because two errors in it were
live in `scripts/why_we_lost.py`:

1. **The town centre was left out entirely.** Its 30 units a season per product ARE the whole drain
   on anything no shop sells, so the table printed `MELON drained 0` for a game where the town ate
   30 melons and the price ended at $19 against a $250 base.
2. **The closing shop list was applied to the whole season.** A shop unlocks every third day, so
   that credits week one with demand that did not exist yet.
"""

import collections
import sys

import pytest

sys.path.insert(0, ".")

from kagg.analysis.replay_fills import season_drain, town_drain

pytest.importorskip("kaggle_environments")


def test_a_shop_that_sells_one_thing_drains_it_twice():
    """`YARN_STORE` sells only WOOL, so `_town_consume` doubles it. Two instances is four units."""
    assert town_drain(0, ["YARN_STORE"], 4, 0) == collections.Counter({"WOOL": 2})
    assert town_drain(0, ["YARN_STORE", "YARN_STORE"], 4, 0) == collections.Counter({"WOOL": 4})
    assert town_drain(1, ["YARN_STORE"], 4, 0) == collections.Counter()


def test_the_town_centre_drains_everything_but_fertilizer():
    """The part the old table omitted. It is the entire demand for a product no shop carries."""
    drained = town_drain(0, [], 0, 24)
    assert drained["MELON"] == 1
    assert drained["FERTILIZER"] == 0


def test_the_reconstructed_drain_equals_the_inventory_a_real_game_lost():
    """End to end, against the env itself: for a product neither side ever traded, every unit that
    left `market["inventory"]` left through the town. If the reconstruction is off by a step or a
    shop, this diverges."""
    from kaggle_environments import make

    from kagg.agents import heuristic
    from kagg.analysis.fills import record_fills

    env = make("kaggriculture", configuration={"seed": 11, "episodeSteps": 361}, debug=True)
    with record_fills(env) as truth:
        env.run([heuristic.make_agent(), heuristic.make_agent()])
    replay = env.toJSON()

    untraded = [p for p in ("TOMATO", "CARROT", "EGG", "WOOL", "MILK")
                if not any(truth.sold(s, p)[0] or truth.bought(s, p)[0] for s in (0, 1))]
    assert untraded, "both sides traded everything; this test proved nothing"

    drained = season_drain(replay)
    first = replay["steps"][0][0]["observation"]["market"]["inventory"]
    last = replay["steps"][-1][0]["observation"]["market"]["inventory"]
    for product in untraded:
        assert first[product] - last[product] == drained[product], product


def test_the_season_drain_does_not_backdate_a_shop_that_had_not_unlocked():
    """A shop unlocks every third day. Charging the closing list to the whole season overstates."""
    from kaggle_environments import make

    from kagg.agents import heuristic
    from kagg.analysis.replay_fills import shop_demand, shop_instances

    env = make("kaggriculture", configuration={"seed": 11, "episodeSteps": 721}, debug=True)
    env.run([heuristic.make_agent(), heuristic.make_agent()])
    replay = env.toJSON()

    closing = list(shop_instances(replay).elements())
    assert closing, "no shop unlocked; this test proved nothing"
    naive = shop_demand(closing, len(replay["steps"]) - 1)
    real = season_drain(replay)
    assert any(real[p] < naive[p] for p in naive), (
        f"the closing list should overstate the season: {dict(real)} vs {dict(naive)}")
