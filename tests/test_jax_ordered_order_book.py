"""The JAX sim must express an explicit market-order list, exactly as the numpy sim now does.

`kagg/sim/game.py` gained `order_op` / `order_item` / `order_qty` on 2026-08-04, and with it the numpy
simulator reproduces a winner's full 720-turn tape against the reference interpreter -- money, shed and
market inventory, every turn (`tests/test_tape_parity.py`). `jax_sim.Actions` did not gain them, so it
still collapses a turn to per-product totals.

That gap is not cosmetic. A turn that interleaves orders on one product --

    SELL WHEAT 1 , BUY_PRODUCT WHEAT 2 , SELL WHEAT 2

-- collapses to `SELL 3 , BUY 2`, and since SELL raises inventory while `BUY_PRODUCT` quotes at
`inventory - 1`, moving both sells ahead of the buy reprices it: $58 against $33 measured directly
against the reference (`tests/test_split_sell_orders.py`).

**Why it blocks the search rather than merely being untidy.** The JAX sim is the batched evaluator any
trajectory search has to score against. If it settles a different game from the one Kaggle runs, every
candidate is ranked by the wrong number -- the exact "optimise the artifact, not a proxy" failure this
project has already paid for once.

The assertions are lockstep against `kagg.sim.game`, not against hand-computed values: that simulator
is the one now verified turn-for-turn against the reference, so agreeing with it is the strongest claim
available without running the reference in-process.
"""

import numpy as np
import pytest

jax = pytest.importorskip("jax")
jnp = pytest.importorskip("jax.numpy")

from kagg.sim import jax_sim as J
from kagg.sim.game import (
    ORDER_BUY_PRODUCT,
    ORDER_HIRE,
    ORDER_SELL,
    Actions,
    Game,
)
from kagg.sim.market import PRODUCT_INDEX

WHEAT = PRODUCT_INDEX["WHEAT"]
MONEY = 8.0
SHED_WHEAT = 19


def _numpy_money(build):
    game = Game(1, starting_money=MONEY, weed_chance=0.0, rng=np.random.default_rng(0))
    for seat in range(2):
        game.farms[seat].shed[:, WHEAT] = SHED_WHEAT
    actions = Actions(1)
    build(actions)
    game._process_market(actions)
    return float(game.farms[0].money[0])


def _jax_money(build):
    """Same market phase in JAX, seeded to the same shed and money."""
    state = _seeded_state()
    actions = Actions(1)
    build(actions)
    out = J._process_market(state.farm, state.tiles, state.inventory,
                            J.from_numpy_actions(actions))
    return float(np.asarray(out[0].money)[0, 0])


def _seeded_state():
    """A fresh state with both seats holding `SHED_WHEAT`, matching the numpy fixture."""
    state = J.reset(1, starting_money=MONEY)
    farm = state.farm._replace(shed=state.farm.shed.at[:, :, WHEAT].set(SHED_WHEAT))
    return state._replace(farm=farm)


def _straddled(actions):
    for seat in range(2):
        actions.order_op[0, seat, :3] = [ORDER_SELL, ORDER_BUY_PRODUCT, ORDER_SELL]
        actions.order_item[0, seat, :3] = [WHEAT, WHEAT, WHEAT]
        actions.order_qty[0, seat, :3] = [1, 2, 2]


def _merged(actions):
    for seat in range(2):
        actions.sell[0, seat, WHEAT] = 3
        actions.buy_product[0, seat, WHEAT] = 2


def test_jax_actions_carries_the_explicit_order_list():
    """The interface. Without these fields the JAX sim cannot represent the turn at all."""
    zero = J.zero_actions(4)
    for field in ("order_op", "order_item", "order_qty"):
        assert hasattr(zero, field), f"jax_sim.Actions has no {field}"
        assert getattr(zero, field).shape == (4, 2, J.MAX_ORDERS)
        assert not np.asarray(getattr(zero, field)).any(), f"{field} must default to empty"


def test_from_numpy_actions_carries_the_order_list_across():
    """`from_numpy_actions` is the bridge the parity gate and every converter use."""
    actions = Actions(1)
    _straddled(actions)
    j = J.from_numpy_actions(actions)

    np.testing.assert_array_equal(np.asarray(j.order_op), actions.order_op)
    np.testing.assert_array_equal(np.asarray(j.order_item), actions.order_item)
    np.testing.assert_array_equal(np.asarray(j.order_qty), actions.order_qty)


def test_the_interleaved_turn_settles_as_the_numpy_sim_settles_it():
    """**The bug.** SELL 1 / BUY 2 / SELL 2 must not be flattened into SELL 3 / BUY 2."""
    expected = _numpy_money(_straddled)
    got = _jax_money(_straddled)

    assert got == pytest.approx(expected, abs=0.5), (
        f"JAX banked ${got:,.2f} on the interleaved order list against the numpy sim's "
        f"${expected:,.2f} -- the explicit slot order is being ignored")


def test_the_interleaved_and_merged_forms_really_do_differ():
    """Anti-vacuity: if these agreed, the test above would pass for the wrong reason."""
    assert _numpy_money(_straddled) != _numpy_money(_merged)


def test_the_canonical_layout_is_unchanged_when_no_list_is_supplied():
    """Every existing caller -- the RL rollouts, the arena, the parity gate -- passes totals only."""
    assert _jax_money(_merged) == pytest.approx(_numpy_money(_merged), abs=0.5)


def test_a_zero_quantity_slot_is_dropped_rather_than_spending_one():
    """`_parse_order` rejects qty <= 0 while the reference has already spent the slot positionally.

    So a zero entry must compact away, not pad -- the same `present`/`cumsum` rule the canonical path
    uses, and the reason a caller cannot smuggle in more than `MAX_ORDERS` orders.
    """
    def padded(actions):
        for seat in range(2):
            actions.order_op[0, seat, :4] = [ORDER_SELL, ORDER_SELL, ORDER_BUY_PRODUCT, ORDER_SELL]
            actions.order_item[0, seat, :4] = [WHEAT, WHEAT, WHEAT, WHEAT]
            actions.order_qty[0, seat, :4] = [1, 0, 2, 2]

    assert _jax_money(padded) == pytest.approx(_jax_money(_straddled), abs=0.5)


def test_hire_in_an_explicit_slot_still_fires():
    """HIRE carries no quantity, so it must not be read as absent when its qty column is zero."""
    def hires(actions):
        for seat in range(2):
            actions.order_op[0, seat, :2] = [ORDER_HIRE, ORDER_SELL]
            actions.order_item[0, seat, :2] = [0, WHEAT]
            actions.order_qty[0, seat, :2] = [0, 2]

    state = _seeded_state()
    actions = Actions(1)
    hires(actions)
    out = J._process_market(state.farm, state.tiles, state.inventory,
                            J.from_numpy_actions(actions))
    assert int(np.asarray(out[0].hires_today)[0, 0]) == 1, "the explicit HIRE slot did not fire"


@pytest.mark.slow
def test_the_jax_sim_reproduces_a_real_tape_exactly_like_the_numpy_sim():
    """**The claim #14 exists to establish.** Same tape, same money, every turn.

    `tests/test_tape_parity.py` proves the numpy sim reproduces episode 89873723 against the *reference
    interpreter*. This chains onto that: the JAX sim agreeing with the numpy sim turn for turn means it
    agrees with the reference too, which is what makes it usable as the evaluator for a trajectory
    search. Without it, every candidate would be ranked by a simulator settling a different game from
    the one Kaggle runs.
    """
    import importlib.util
    import json
    import pathlib
    import sys

    episode = pathlib.Path("data/episodes/89873723.json")
    if not episode.exists():
        pytest.skip("replay not present")

    spec = importlib.util.spec_from_file_location("rtd", "scripts/replay_tape_day.py")
    rtd = importlib.util.module_from_spec(spec)
    sys.modules["rtd"] = rtd
    spec.loader.exec_module(rtd)

    from kagg.search import executor as X

    steps = json.loads(episode.read_text())["steps"]
    schedule = rtd.unlock_schedule(steps)
    turns = 240

    def frame(t):
        actions = Actions(1)
        for seat in range(2):
            act = steps[t][seat].get("action")
            if not isinstance(act, dict):
                continue
            units = [act.get("farmer")] + list(act.get("hands") or [])
            for slot, entry in enumerate(units[: X.MAX_EXEC_UNITS]):
                rtd.write_unit(actions, seat, slot, entry)
            rtd.write_market(actions, seat, act.get("market"))
        return actions

    game = Game(1, weed_chance=0.0, rng=np.random.default_rng(0), unlock_schedule=schedule)
    state = J.reset(1, unlock_schedule=schedule)
    for t in range(turns):
        actions = frame(t)
        game.step(actions)
        state = J.step(state, J.from_numpy_actions(actions), weed_chance=0.0)
        theirs = float(game.farms[0].money[0])
        ours = float(np.asarray(J.money(state))[0, 0])
        assert ours == pytest.approx(theirs, abs=0.5), (
            f"turn {t} (day {t // 24} hour {t % 24}): jax ${ours:,.0f} vs numpy ${theirs:,.0f}")
