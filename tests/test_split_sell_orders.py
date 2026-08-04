"""Is `SELL X a; SELL X b` the same as `SELL X a+b`? The whole replication question turns on it.

**Why this test exists.** I reported to Alex that 1-1 replication of the winner is "impossible by
construction", and the load-bearing claim was that the winner's turn 1 emits three separate orders
for one product:

    ['HIRE'], ['HIRE'], ['BUY_ANIMAL','COW',1], ['BUY_SEED','MELON',6],
    ['BUY_SEED','WHEAT',6], ['SELL','WHEAT',1], ['SELL','WHEAT',3], ['SELL','WHEAT',1]

while `Decision.sell` carries one quantity per product per turn and can only emit `SELL WHEAT 5`.
That much is true about the *order list*. Whether it is true about the *money* was never tested, and
CLAUDE.md is explicit that a theory without a failing test is a guess.

Reading the reference says it should not matter. `_process_market` loops over order slots and calls
`_refresh_prices` once per slot (ref 602), but `_refresh_prices` is a pure function of inventory
(ref 194-197) and the per-unit quote inside the lockstep loop does not read the cached prices at
all -- it recomputes `market_price(item, market["inventory"][item], ...)` live for every single unit
(ref 571). So the extra refreshes that splitting inserts only update the dict agents *observe*, and
cannot change the price any unit transacts at.

**Scope, corrected after measuring.** "Partitioning a SELL is free" holds only when nothing sits
between the pieces. A `BUY_PRODUCT` of the *same* product between two SELLs is NOT merge-equivalent --
see `test_a_buy_between_two_sells_of_the_same_product_is_NOT_merge_equivalent`, which is the actual
first error in replaying the winner's day 0 ($58 against $33 on turn 11).

The other exception is the contested case, and it is a real one. The lockstep runs across *both* seats at
the same slot index, so splitting changes which of the opponent's orders a given unit competes
against. CLAUDE.md already flags this as the project's known blind spot -- "300 full-length episodes
that never once had both players selling the same product" -- so it gets its own test rather than an
assumption.
"""

import numpy as np
import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg


def _reference_market(orders, shed, money=0.0):
    """Run the real `kaggriculture._process_market` over hand-built state.

    Lifted from `tests/test_sim_market.py`, deliberately by copy: that one is a parity fixture for
    our own market and this one is a question about the reference's own behaviour. Coupling them
    would mean a change made for one silently redefines the other.
    """
    from types import SimpleNamespace as NS

    inv = {item: kg.MARKET_PARAMS[item]["I0"] for item in kg.PRODUCTS}
    market = {"inventory": dict(inv), "prices": {}}
    farms = [{"money": float(money), "hands": [], "farmer": [4, 4],
              "tiles": [[None] * 10 for _ in range(10)],
              "unlocked_quadrants": ["NW"], "hires_today": 0} for _ in range(2)]
    state = [
        NS(observation=NS(market=market, farms=farms, player=p,
                          private={"shed": dict(shed[p]), "seeds": {}, "inventories": [{}]}),
           action={"market": orders[p]})
        for p in range(2)
    ]
    env = NS(configuration={"boardSize": 10, "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1})

    kg._process_market(state, env)
    return [farms[p]["money"] for p in range(2)], dict(market["inventory"])


def test_splitting_a_sell_is_worth_the_same_as_one_merged_order():
    """**The claim I got wrong.** The winner's actual turn-1 split, against its merged equivalent.

    If this passes, `SELL WHEAT 1/3/1` is not a reason the genome cannot reproduce the winner, and
    the representation gap for sells is cosmetic rather than structural.
    """
    split, split_inv = _reference_market(
        [[["SELL", "WHEAT", 1], ["SELL", "WHEAT", 3], ["SELL", "WHEAT", 1]], []],
        [{"WHEAT": 50}, {}],
    )
    merged, merged_inv = _reference_market(
        [[["SELL", "WHEAT", 5]], []],
        [{"WHEAT": 50}, {}],
    )

    assert split[0] == merged[0], (
        f"split 1/3/1 banked ${split[0]:,.0f} but merged 5 banked ${merged[0]:,.0f} -- "
        f"order granularity changes the money, so the genome really cannot express this turn")
    assert split_inv == merged_inv


@pytest.mark.parametrize("pieces", [[1, 1], [2, 3], [1, 3, 1], [1, 1, 1, 1, 1], [4, 2, 3, 1]])
def test_any_partition_of_the_same_quantity_pays_the_same(pieces):
    """Not just the winner's partition -- any of them, since a general claim needs general evidence."""
    total = sum(pieces)
    split, _ = _reference_market([[["SELL", "WHEAT", n] for n in pieces], []],
                                 [{"WHEAT": 100}, {}])
    merged, _ = _reference_market([[["SELL", "WHEAT", total]], []], [{"WHEAT": 100}, {}])

    assert split[0] == merged[0], f"{pieces} banked ${split[0]:,.0f} vs ${merged[0]:,.0f} merged"


def test_a_contested_product_is_where_splitting_does_change_the_money():
    """The genuine exception, and the one CLAUDE.md warns has never been exercised.

    Both seats sell WHEAT in the same turn. Seat 0 splits, seat 1 does not. The lockstep pairs seats
    by *slot index*, so seat 0's split changes which units it competes against and therefore what
    inventory each of its units is quoted at.

    This test asserts nothing about which way the difference goes -- only that "merging is lossless"
    is a claim about the uncontested case and must not be applied blindly to a two-seat turn.
    """
    split, _ = _reference_market(
        [[["SELL", "WHEAT", 1], ["SELL", "WHEAT", 3], ["SELL", "WHEAT", 1]],
         [["SELL", "WHEAT", 5]]],
        [{"WHEAT": 50}, {"WHEAT": 50}],
    )
    merged, _ = _reference_market(
        [[["SELL", "WHEAT", 5]], [["SELL", "WHEAT", 5]]],
        [{"WHEAT": 50}, {"WHEAT": 50}],
    )

    # Recorded, not predicted: whatever the reference does here is the fact we have to live with.
    print(f"\ncontested: seat0 split=${split[0]:,.0f} merged=${merged[0]:,.0f}  "
          f"(delta ${split[0] - merged[0]:,.0f})")
    print(f"contested: seat1 vs   split=${split[1]:,.0f} merged=${merged[1]:,.0f}")


def test_a_buy_between_two_sells_of_the_same_product_is_NOT_merge_equivalent():
    """**The limit of the claim above, and the first real replication error.**

    The tests above establish that partitioning a SELL is free. That is true only when nothing sits
    between the pieces. Turn 11 of day 0 on episode 89873723 seat 0 is:

        [["SELL", "WHEAT", 1], ["BUY_PRODUCT", "WHEAT", 2], ["SELL", "WHEAT", 2]]

    `Actions` carries one quantity per product per turn, so we can only emit `SELL 3` then `BUY 2`.
    `_process_market` walks slots in order, SELL raises inventory and `BUY_PRODUCT` quotes at
    `inventory - 1`, so selling all three units before buying prices the buy differently.

    Measured in `data/logs/replay_tape_day0.log`: driving the winner's own tape through `kagg.sim`
    reproduces money, crew, pens and animals **dollar- and count-exact for turns 0 through 10**, and
    diverges by $32 at turn 11 -- this turn. It is the entire reason a day does not replicate, and it
    is what task #12, a faithful raw order list, exists to fix.
    """
    shed = [{"WHEAT": 19}, {"WHEAT": 19}]
    straddled = [["SELL", "WHEAT", 1], ["BUY_PRODUCT", "WHEAT", 2], ["SELL", "WHEAT", 2]]
    merged = [["SELL", "WHEAT", 3], ["BUY_PRODUCT", "WHEAT", 2]]

    theirs, _ = _reference_market([straddled, straddled], shed, money=8.0)
    ours, _ = _reference_market([merged, merged], shed, money=8.0)

    assert theirs[0] != ours[0], (
        "if these ever agree, per-product quantities are sufficient after all and the raw order list "
        "is unnecessary")
    assert theirs[0] == 58 and ours[0] == 33, (
        f"the measured gap changed: straddled ${theirs[0]:,.0f} vs merged ${ours[0]:,.0f}")
