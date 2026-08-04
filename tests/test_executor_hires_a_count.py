"""The multi-hire fix landed in the simulator and stopped there. The decoder still collapses it.

`kagg/sim/game.py:113` and `kagg/sim/jax_sim.py:291` both carry integer hire counts as of 2026-08-04,
the latter saying so explicitly -- "Integer counts, not flags: casting to bool here would collapse
'hire twice' to 'hire once'". `tests/test_multiple_hires_per_turn.py` pins that, and pins the
reference behaviour, and pins a real leader issuing two HIREs on turn 1.

What no test reaches is the two layers **above** the simulator:

    executor.py:210   hire: np.ndarray            # [B] bool
    executor.py:493   hire = (view.n_units - 1) < target_hands
    agent.py:244      ([["HIRE"]] if bool(decision.hire[0]) else [])

So a capability the simulator has is narrowed back to one-per-turn by our own plan decoder, and the
submission can never emit the two-HIRE turn the leaders open with. This is the same shape of defect as
the livestock blindness in `tests/test_observation_view_sees_livestock.py`: the fix went into one layer
and the layer above kept flattening it. CLAUDE.md's rule for exactly this -- "a gate only tests what it
exercises" -- is why these assertions target `decide` and `to_action` rather than `Game`.

**Behavioural consequence, stated because it is not merely a type change.** `HIRE_COST` is Fibonacci in
`hires_today` and resets every dawn, so N hands cost the same whether taken in one turn or spread over
N turns -- but taken in one turn they start working up to N-1 hours earlier, so the ramp changes and not
just the dtype.

**And "as many as possible" is the wrong answer, measured.** The first attempt asked for the whole
shortfall, and a fourteen-hand request filled all ten of the turn's order slots -- both `_process_market`
and `game._order_book` compact a turn into ten -- crowding out every SELL. The farm banked $98 on a
$3,000 stake. `executor.HIRES_PER_TURN = 3` is the cap, taken from the leader tape rather than picked:
across 15,840 archived turns the per-turn HIRE counts are 1 x154, 2 x506, **3 x1642**, 4 x16, 10 x56.
"""

import numpy as np
import pytest

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import plan as P
from kagg.sim.tiles import EMPTY

TARGET_HANDS = 6


def _view(n_units, money=3000.0):
    tiles = 100
    return X.View(
        day=0, hour=0,
        kind=np.full((1, tiles), EMPTY, dtype=np.int64),
        crop=np.full((1, tiles), -1, dtype=np.int64),
        planted_day=np.zeros((1, tiles), dtype=np.int64),
        watered=np.zeros((1, tiles), dtype=bool),
        yield_units=np.zeros((1, tiles), dtype=np.int64),
        unit_ord=np.zeros((1, X.MAX_EXEC_UNITS), dtype=np.int64),
        n_units=np.array([n_units]),
        money=np.array([money]),
        seeds=np.zeros((1, P.N_CROPS), dtype=np.int64),
        shed=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
        prices=np.zeros((1, P.N_PRODUCTS), dtype=np.int64),
        n_land=np.array([0]),
    )


def _plan(hands=TARGET_HANDS, selling=False):
    """A plan whose day-0 hire target is `hands`, so `decide` is asked for several at once.

    `selling` also asks for the largest sell quantity and the lowest price floor, which the
    all-zeroes genome does not -- a fixture that wants no sells cannot detect sells being crowded out.
    """
    g = np.zeros(P.N_GENES, dtype=np.int64)
    lo, hi = P.gene_slice("hires")
    level = int(np.abs(np.asarray(P.HIRE_LEVELS) - hands).argmin())
    g[lo:hi] = level
    if selling:
        lo, hi = P.gene_slice("sell_qty")
        g[lo:hi] = int(np.asarray(P.SELL_QTYS).argmax())
        lo, hi = P.gene_slice("sell_qty_animal")
        g[lo:hi] = int(np.asarray(P.SELL_QTYS).argmax())
        lo, hi = P.gene_slice("floor_frac")
        g[lo:hi] = int(np.asarray(P.FLOOR_FRACS).argmin())
        lo, hi = P.gene_slice("floor_frac_animal")
        g[lo:hi] = int(np.asarray(P.FLOOR_FRACS).argmin())
    return P.decode(g[None]), int(np.asarray(P.HIRE_LEVELS)[level])


def test_decide_asks_for_every_hand_it_is_short_not_just_one():
    """**The bug.** A plan wanting six hands on a one-unit farm must ask for six, not one."""
    plan, target = _plan()
    decision = X.decide(_view(n_units=1), plan)

    asked = int(decision.hire[0])
    expected = min(target, X.HIRES_PER_TURN)
    assert asked == expected, (
        f"plan targets {target} hands and the farm has 0, but `decide` asked for {asked}. A boolean "
        f"hire caps the ramp at one hand per turn while `game.py` and `jax_sim.py` both accept counts; "
        f"the per-turn cap is `HIRES_PER_TURN = {X.HIRES_PER_TURN}`, measured off the leader tape.")


def test_decide_stops_asking_once_the_crew_is_full():
    """The count must be a shortfall, not a constant -- otherwise it rehires every turn forever."""
    plan, target = _plan()
    decision = X.decide(_view(n_units=target + 1), plan)

    assert int(decision.hire[0]) == 0, (
        f"crew already at {target} hands plus the farmer, still asked for {int(decision.hire[0])}")


def test_to_action_emits_one_hire_order_per_hand():
    """The submission has to *write* the orders. `_process_market` resolves one HIRE per slot."""
    plan, target = _plan()
    obs = {"player": 0, "day": 0, "hour": 0,
           "farms": [{"money": 3000.0, "farmer": [4, 4], "hands": [],
                      "hires_today": 0, "unlocked_quadrants": ["NW"],
                      "tiles": [[None] * 10 for _ in range(10)]}],
           "market": {"prices": {}}, "private": {"shed": {}, "seeds": {}, "inventories": [{}]}}

    view = A.observation_view(obs)
    action = A.to_action(obs, X.decide(view, plan), int(view.n_units[0]))
    hires = [o for o in action["market"] if o and o[0] == "HIRE"]

    assert len(hires) == min(target, X.HIRES_PER_TURN), (
        f"asked for {target} hands, emitted {len(hires)} HIRE orders: {action['market']}")


def test_the_order_list_still_fits_when_the_whole_crew_is_hired_at_once():
    """A twelve-hand opening must not push the list past `MAX_ORDERS` and silently drop the tail.

    This is the failure mode already recorded in `agent.py`: truncation in the reference is positional
    and applied before parsing, so an over-long list drops its *last* entries -- which is how widening
    sells to nine products once cost 55% money drift.
    """
    plan, _ = _plan(hands=12)
    obs = {"player": 0, "day": 0, "hour": 0,
           "farms": [{"money": 3000.0, "farmer": [4, 4], "hands": [],
                      "hires_today": 0, "unlocked_quadrants": ["NW"],
                      "tiles": [[None] * 10 for _ in range(10)]}],
           "market": {"prices": {}}, "private": {"shed": {}, "seeds": {}, "inventories": [{}]}}

    view = A.observation_view(obs)
    action = A.to_action(obs, X.decide(view, plan), int(view.n_units[0]))

    assert len(action["market"]) <= A.MAX_ORDERS, (
        f"emitted {len(action['market'])} orders against a cap of {A.MAX_ORDERS}: {action['market']}")


def test_hiring_never_starves_the_market_orders():
    """**Measured regression, not a hypothetical.** Hiring must not consume the whole order budget.

    The first version of the count change let a fourteen-hand request fill all ten slots, so
    `market[: MAX_ORDERS - len(atomic)]` became `market[:0]` and every SELL and BUY vanished. Two
    `test_search_executor.py` gates caught it: the farm banked **$98** against a $3,000 stake and plant
    requests fell from >100 to 26. Selling is where the money comes from; hands only multiply what the
    farm can already afford to do.
    """
    plan, _ = _plan(hands=14, selling=True)
    shed = {n: 20 for n in A.PRODUCT_NAMES}
    obs = {"player": 0, "day": 3, "hour": 5,
           "farms": [{"money": 3000.0, "farmer": [4, 4], "hands": [],
                      "hires_today": 0, "unlocked_quadrants": ["NW"],
                      "tiles": [[None] * 10 for _ in range(10)]}],
           "market": {"prices": {n: 100 for n in A.PRODUCT_NAMES}},
           "private": {"shed": shed, "seeds": {}, "inventories": [{}]}}

    view = A.observation_view(obs)
    decision = X.decide(view, plan)
    action = A.to_action(obs, decision, int(view.n_units[0]))

    wanted_sells = int((decision.sell[0] > 0).sum())
    got_sells = len([o for o in action["market"] if o and o[0] == "SELL"])

    assert wanted_sells > 0, "fixture is wrong: the plan does not want to sell anything here"
    assert got_sells > 0, (
        f"the plan wanted {wanted_sells} sell orders and hiring crowded out every one of them: "
        f"{action['market']}")
    assert len(action["market"]) <= A.MAX_ORDERS
