"""Units that changed hands, recovered from a recording, checked against the env's own commit.

There is no simulation in `kagg/analysis/replay_fills.py` and there cannot be -- a downloaded
ladder game has no seed, so it cannot be re-played. What it has instead is two independent
ledgers that both record the same trades:

1. **The shed.** `_commit_unit` is the only market path that touches `private["shed"]`, and both
   seats' `private` is present in a downloaded replay. On a turn where the seat emitted no
   `DROP`/`PICKUP`/`PLACE` -- the only unit ops that touch the same field -- and which is not the
   end-of-day rollover, a shed delta IS a fill.
2. **The market inventory.** `inv(t) - inv(t-1) + town_drain(t) = sold - bought`, summed over both
   seats, with `town_drain` exact from the shop list and `step % 4` / `step % 24`. This one covers
   the turns the shed cannot, and fails in exactly one place the shed does not: `_commit_unit`
   does not add to supply when a unit sells at $1, so a product sitting on `PRICE_FLOOR` moves
   invisibly here.

Neither ledger is complete, and the union of the two is still not complete. So the contract this
test pins is not "always exact" -- it is:

- **never overstates.** A recovered figure is a lower bound on the truth, per seat, per product.
  This is the direction that matters: the failure being fixed inflated a melon count 14x.
- **conserves.** Nothing is invented and nothing silently vanishes: attributed + shared +
  unresolved accounts for every unit both sides really traded.
- **exact when only one side trades that product**, which is the common case and the one every
  per-product question in this project has actually needed.

The ground truth is `kagg.analysis.fills.record_fills`, which wraps `_commit_unit` itself.
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.analysis.fills import record_fills
from kagg.analysis.replay_fills import trade_fills

pytest.importorskip("kaggle_environments")

#: 15 days. Long enough that both sides have built a herd and are selling into a moved market,
#: short enough to stay a unit test -- the pair below runs in under a second.
STEPS = 361


def play(a, b, seed=11, steps=STEPS):
    """Run a game and return `(replay JSON, ground-truth fills)`."""
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": steps}, debug=True)
    with record_fills(env) as truth:
        env.run([a, b])
    return env.toJSON(), truth


def disjoint_pair():
    from kagg.agents import heuristic, rancher
    return heuristic.make_agent(), rancher.agent


def mirror_pair():
    from kagg.agents import heuristic
    return heuristic.make_agent(), heuristic.make_agent()


def test_recovered_sales_never_exceed_what_actually_committed():
    """The direction that matters. An overstatement is the bug; an understatement is a caveat."""
    replay, truth = play(*mirror_pair())
    got = trade_fills(replay)

    for seat in (0, 1):
        for product, units in got.sold[seat].items():
            real = truth.sold(seat, product)[0]
            assert units <= real, (
                f"seat {seat} {product}: recovered {units} sales but only {real} committed")
        for product, units in got.bought[seat].items():
            real = truth.bought(seat, product)[0]
            assert units <= real, (
                f"seat {seat} {product}: recovered {units} buys but only {real} committed")


def test_nothing_is_invented_and_nothing_silently_vanishes():
    """Per product that never sat on the floor: attributed + shared equals the real two-sided
    volume. The floor is excluded because it is a stated blind spot, not an oversight --
    `_commit_unit` does not add to supply for a unit sold at $1, so those units are invisible in
    the market ledger by construction and are reported in `unresolved` instead."""
    replay, truth = play(*mirror_pair())
    got = trade_fills(replay)

    products = set(got.sold[0]) | set(got.sold[1]) | set(got.shared_sold)
    products |= {p for p in truth.products()
                 if any(truth.sold(seat, p)[0] for seat in (0, 1))}
    checked = 0
    for product in products - got.floored:
        real = sum(truth.sold(seat, product)[0] for seat in (0, 1))
        net = real - sum(truth.bought(seat, product)[0] for seat in (0, 1))
        seen = (got.sold[0][product] + got.sold[1][product] + got.shared_sold[product]
                - got.bought[0][product] - got.bought[1][product])
        assert seen == net, f"{product}: accounted net {seen} against {net} committed"
        checked += 1
    assert checked, "the game traded nothing off the floor; this test proved nothing"


def test_attribution_is_exact_when_only_one_side_trades_that_product():
    """`heuristic` sells melon and nothing else; `rancher` sells milk and fertilizer and nothing
    else. Every unit is unambiguous, so the recovery must be exact and `shared` must be empty."""
    replay, truth = play(*disjoint_pair())
    got = trade_fills(replay)

    for seat, product in ((0, "MELON"), (1, "MILK"), (1, "FERTILIZER")):
        assert got.sold[seat][product] == truth.sold(seat, product)[0], (
            f"seat {seat} {product}: {got.sold[seat][product]} != {truth.sold(seat, product)[0]}")
    assert not +got.shared_sold, f"nothing should be ambiguous here: {got.shared_sold}"


def re_offering(inner, *orders):
    """`inner`, plus a standing order re-posted on every single turn.

    The point is a recording where the offer total and the fill total are wildly apart, which is
    what our own agent's re-posting produces on the ladder and what NO well-behaved sparring agent
    in this repo produces -- `heuristic` asks for seed once and `rancher` asks for each cow once,
    so a game between the stock agents cannot tell a correct count from one that sums the orders.
    """
    def agent(obs, config=None):
        out = dict(inner(obs, config) if config is not None else inner(obs))
        out["market"] = list(out.get("market") or []) + [list(o) for o in orders]
        return out
    return agent


def test_a_seed_purchase_is_exact_because_seeds_have_a_closed_ledger():
    """`private["seeds"]` is touched by exactly two things -- `BUY_SEED` adds one, `PLANT` removes
    one -- and plants are countable off the board. So the fill is `delta + plants`, with no
    ambiguity and no lower bound about it."""
    from kagg.agents import heuristic
    from kagg.analysis.replay_fills import offered, seed_fills

    replay, truth = play(re_offering(heuristic.make_agent(), ["BUY_SEED", "MELON", 50]),
                         re_offering(heuristic.make_agent(), ["BUY_SEED", "MELON", 50]))
    for seat in (0, 1):
        got = seed_fills(replay, seat)
        for crop in ("WHEAT", "MELON", "STRAWBERRY", "CARROT", "TOMATO"):
            assert got[crop] == truth.units(seat, "BUY_SEED", crop), crop
        # and the discrimination is real: the offer total is an order of magnitude out
        assert offered(replay, seat)["BUY_SEED"]["MELON"] > 10 * max(1, got["MELON"])


def test_an_animal_bought_is_read_off_the_shed_because_the_market_never_sees_it():
    """`BUY_ANIMAL` lands the beast in `private["shed"]`, but COW and SHEEP are not in `PRODUCTS`
    so `market["inventory"]` never moves for one. The shed is the only witness there is."""
    from kagg.agents import heuristic, rancher
    from kagg.analysis.replay_fills import offered

    replay, truth = play(re_offering(heuristic.make_agent(), ["BUY_ANIMAL", "COW", 4]),
                         re_offering(rancher.agent, ["BUY_ANIMAL", "SHEEP", 4]))
    got = trade_fills(replay)
    for seat in (0, 1):
        for animal in ("COW", "SHEEP", "GOOSE", "CHICKEN", "PIG"):
            assert got.animals_bought[seat][animal] == truth.units(seat, "BUY_ANIMAL", animal), (
                f"seat {seat} {animal}")
    assert sum(got.animals_bought[0].values()), "seat 0 bought no animals; this proved nothing"
    assert (offered(replay, 0)["BUY_ANIMAL"]["COW"]
            > 10 * max(1, got.animals_bought[0]["COW"])), "the order stream is not discriminated"


def test_hire_and_buy_land_are_fills_too_because_the_env_can_refuse_them():
    """`_do_hire` and `_do_buy_land` return silently when the bank is short, so an emitted HIRE is
    an offer like any other. They do not pass through `_commit_unit`, which is why they were the
    two ops `kagg/analysis/fills.py` did not cover."""
    replay, truth = play(*mirror_pair())
    got = trade_fills(replay)
    for seat in (0, 1):
        hands_hired = sum(
            1 for t in range(1, len(replay["steps"]))
            if len(replay["steps"][t][0]["observation"]["farms"][seat].get("hands") or [])
            > len(replay["steps"][t - 1][0]["observation"]["farms"][seat].get("hands") or []))
        assert got.hired[seat] >= hands_hired
        assert got.hired[seat] == truth.units(seat, "HIRE")
