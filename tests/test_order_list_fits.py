"""The emitted market list must mirror `game._order_book` and fit `maxMarketOrdersPerTurn`.

One theory, one test. `reference/kaggriculture.py:534`:

    queues.append(q[:max_orders])          # max_orders = 10, applied BEFORE _parse_order

The truncation is **positional and pre-parse**, so a padding entry consumes a slot exactly as a real
order does. `to_action` emitted 9 sells + BUY_SEED + HIRE + BUY_LAND = 12, so the last two were
dropped every single turn -- and those two are HIRE and BUY_LAND. Measured by
`tests/test_search_transfer.py`: sim $29,447 against real $18,953, a 55% drift on plans with no
animals at all.

The simulator does something different and correct: `game._order_book` builds candidates in the
canonical order (sells, seeds, products, animals, hire, land), keeps only those with a positive
quantity (`present = c_qty > 0`), and clamps to `MAX_ORDERS`. So it *compacts*. `to_action` *padded*.
With eight slots nothing was ever truncated and the two behaved identically, which is why the
300/300 parity gate never saw it -- `CLAUDE.md`, "a gate only tests what it exercises", again.

The same emit path is also missing BUY_ANIMAL and BUY_PRODUCT entirely, so the submission could not
buy an animal or a unit of feed no matter what the plan said.
"""

import numpy as np
import pytest

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import plan as P

MAX_ORDERS = 10          # reference/kaggriculture.py:526, maxMarketOrdersPerTurn


def _obs(hour=0):
    tiles = [[None] * P.BOARD for _ in range(P.BOARD)]
    return {
        "player": 0, "day": 25, "hour": hour,
        "farms": [{"money": 5000.0, "farmer": [4, 4], "hands": [],
                   "tiles": tiles, "unlocked_quadrants": ["NW"]}],
        "private": {"shed": {}, "seeds": {}},
        "market": {"prices": {}},
    }


def _decision(**over):
    """A Decision with every market channel firing at once -- the worst case for the slot budget."""
    d = X.Decision(
        unit_op=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        unit_crop=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        sell=np.full((1, P.N_PRODUCTS), 5, dtype=np.int64),
        buy_seed=np.full((1, P.N_CROPS), 3, dtype=np.int64),
        hire=np.array([True]),
        buy_land=np.array([True]),
        buy_animal=np.full((1, P.N_ANIMALS), 1, dtype=np.int64),
        buy_product=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
    )
    for k, v in over.items():
        setattr(d, k, v)
    return d


def test_the_market_list_never_exceeds_the_reference_cap():
    """Everything firing at once. The reference silently drops anything past the tenth entry."""
    action = A.to_action(_obs(), _decision(), n_units=1)
    n = len(action["market"])
    assert n <= MAX_ORDERS, (
        f"emitted {n} market orders against a cap of {MAX_ORDERS}; the reference truncates "
        f"positionally before parsing, so entries {MAX_ORDERS + 1}..{n} are discarded")


def test_hire_and_buy_land_survive_a_full_market_turn():
    """The two orders that must never be the ones dropped.

    Both are atomic and both resolve *before* the per-unit lockstep at the same slot index, so they
    get first claim on cash that turn. Losing them costs the whole hiring curve and the land timing
    -- the two genes with the largest measured effect.
    """
    action = A.to_action(_obs(), _decision(), n_units=1)
    ops = [o[0] for o in action["market"]]
    assert "HIRE" in ops, f"HIRE was dropped from {ops}"
    assert "BUY_LAND" in ops, f"BUY_LAND was dropped from {ops}"


def test_no_slot_is_wasted_on_a_zero_quantity_order():
    """A zero-quantity order is rejected by `_parse_order` but still consumes a slot in the queue."""
    d = _decision(sell=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
                  buy_seed=np.zeros((1, P.N_CROPS), dtype=np.int64),
                  buy_animal=np.zeros((1, P.N_ANIMALS), dtype=np.int64))
    action = A.to_action(_obs(), d, n_units=1)
    for order in action["market"]:
        if order[0] in ("SELL", "BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL"):
            assert int(order[2]) > 0, f"{order} is a wasted slot -- `_parse_order` rejects it"


def test_animals_and_feed_can_actually_be_ordered():
    """`to_action` emitted no BUY_ANIMAL and no BUY_PRODUCT, so the animal economy was unreachable."""
    d = _decision(sell=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
                  buy_seed=np.zeros((1, P.N_CROPS), dtype=np.int64),
                  buy_product=np.eye(1, P.N_PRODUCTS, 0, dtype=np.int64) * 12)
    action = A.to_action(_obs(), d, n_units=1)
    ops = [o[0] for o in action["market"]]
    assert "BUY_ANIMAL" in ops, f"the plan ordered an animal and the action says {ops}"
    assert "BUY_PRODUCT" in ops, f"the plan ordered 12 wheat as feed and the action says {ops}"
