"""`PRICE_AWARE_SELL_CAP`: does the sell loop read the market instead of the row's own volume?

**The theory.** `allow` -- bounded by `today + carry` or `have - still_owed`, itself keyed to the
DAY TOTAL a schedule row ever asked for -- is a fact about ONE REPLAY's production
(`data/seed_scripts/top_guys/90976060/schedule.json`, a 1.32.2 tape), not a fact about what the
market can absorb across a season. `docs/brief_market_selling_2026-08-08.md` measures the symptom
directly: top 1.32.6 plans sell 305-649 WHEAT across a season, ours sells 71, because the row we
imitate never asked for more. `market_price` is public and exact (`kaggriculture.py:179`), so
whether a product is glutted does not have to be guessed from the row.

**`rate[prod]`, the PER-OFFER bound, is a separate thing and must not move.** A first version of
this flag dropped both at once (`n = have`) and the arena caught it: win rate unchanged (94.4%,
the pool was already saturated) but mean money fell ~30% against every single opponent, seeds
500-505 (`data/logs/price_aware_arena_2026-08-08.log`) -- a big `have` right after a harvest went
out as one order and walked the whole size down the price curve in a single turn, the same dump
shape already measured on wool in `LIQUIDATE_FROM_HOUR`'s docstring ($29,041 -> $21,811). The tests
below pin BOTH halves for exactly this reason.

**One theory, one test, per CLAUDE.md.** Each test below pins one side of the claim:

1. Flag OFF must be byte-identical to today -- this is the safety rail, since the flag ships OFF.
2. Flag ON, price >= base (WHEAT, not glutted): the DAY TOTAL is no longer the ceiling.
3. Flag ON, price < base (a real glut, modelled on MELON): the existing caps are untouched --
   this is the case the flag is deliberately NOT supposed to touch, per its own docstring.
4. The wheat-feed reserve and the fertilizer hold-back are reserves netted into `have` BEFORE this
   code ever runs (see `_router_acts`'s sell block), so the flag can only ever raise an offer that
   was already stock-and-reserve-bounded, never invent stock. Pinned on WHEAT with a live herd.
5. `rate[prod]` still bounds a SINGLE offer even with the flag on -- the arena-measured half.

Uses the same harness as `tests/test_stock_the_schedule_never_names.py`: a static shed, no market
draw, so the question is only "what is the agent willing to OFFER against a given holding."
"""

import sys

import pytest

sys.path.insert(0, ".")

from kagg.search import router as RT
from kagg.search import schedule_agent as SA


def blank_board(unlocked=("NW",)):
    return [["LOCKED" if RT.R.quadrant_of(x, y) not in unlocked else None
             for x in range(10)] for y in range(10)]


def empty_sched(days=30, **row):
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={}, hands=0)
    return {d: dict(base, **(row if d == 0 else {})) for d in range(days)}


def steady_sched(prod, per_day, days=30):
    """Every day asks for the same `per_day`, so `still_owed` stays large all season.

    `empty_sched(sells={...})` only sets day 0's row; every later day is empty, so
    `CUMULATIVE_SELLS`'s dead-stock release (`tests/test_stock_the_schedule_never_names.py`) fires
    on its own and releases the whole shed regardless of price -- that mechanism is real and
    correct, but it is not what these tests are isolating. Asking for `per_day` on every day keeps
    `still_owed` high enough that `allow` stays pinned near `rate[prod] == per_day`, so the ONLY
    thing that can widen an offer is the flag under test.
    """
    base = dict(plants=[], animals_bought={}, builds=0, places=[], hires=0, land=0,
                seeds={}, buys={}, sells={prod: per_day}, hands=0)
    return {d: dict(base) for d in range(days)}


def _offer_a_day(sched, shed, prices=None, day=0, money=3000, alive=0):
    """Total units of each product OFFERED across one full day, driving the agent turn by turn.

    `prices` is the market quote handed to the agent every turn -- a static number, since the
    question under test is the agent's own cap logic, not `market_price`'s shape (that function is
    the reference environment's, trusted and untouched here).
    """
    board = blank_board()
    agent = SA.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": money, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    if alive:
        # A minimally complete pen -- `router.animal_ops` reads `fed_today` unconditionally, so a
        # bare `{"animal": ...}` dict crashes it. Fields per `tests/test_adapter.py`'s `TILE_FIELDS`.
        farm["tiles"][4][3] = {
            "kind": "PASTURE", "animal": "COW", "placed_day": 0,
            "consecutive_unfed": 0, "fed_today": False, "cared_today": False,
            "pending_care_bonus": False,
        }
    total = {}
    for hour in range(RT.TPD):
        obs = {"day": day, "hour": hour, "farms": [farm], "step": day * RT.TPD + hour,
               "private": {"shed": dict(shed), "seeds": {}, "inventories": [{}]}}
        if prices is not None:
            obs["market"] = {"prices": dict(prices), "inventory": {}}
        act = agent(obs)
        for o in act["market"]:
            if o[0] == "SELL":
                total[o[1]] = total.get(o[1], 0) + int(o[2])
    return total


@pytest.fixture(autouse=True)
def _restore_flag():
    """Every test sets the flag explicitly; restore the shipped default after."""
    before = SA.PRICE_AWARE_SELL_CAP
    yield
    SA.PRICE_AWARE_SELL_CAP = before


def test_flag_off_is_byte_identical_to_the_row(monkeypatch):
    """The safety rail: the flag ships OFF, so this must hold with no other change."""
    sched = steady_sched("WHEAT", 4)
    SA.PRICE_AWARE_SELL_CAP = False
    # Price says WHEAT is wildly scarce -- if the flag were somehow live this would matter a lot.
    without_price = _offer_a_day(sched, {"WHEAT": 80})
    with_price = _offer_a_day(sched, {"WHEAT": 80}, prices={"WHEAT": 999})
    assert without_price == with_price == {"WHEAT": 4}, (
        f"flag OFF must ignore the market entirely: {without_price} vs {with_price}")


def test_flag_on_lets_a_scarce_product_exceed_the_row():
    """WHEAT at or above `RT.BASE_PRICE['WHEAT']` (25): the DAY TOTAL stops being the ceiling.

    This is the exact shape of the brief's finding -- a row asking for a handful of wheat against a
    shed that could offer far more, with the market saying that is safe. Kept inside
    `SHED_CAPACITY` (100) so `SELL_TO_MAKE_ROOM`'s own release cannot also explain a big offer --
    the point under test is the price branch alone. The season total climbs well past the row's
    `rate=4` because the day-total cap (`allow`) is what the flag relaxes -- see
    `test_flag_on_never_exceeds_the_per_offer_rate` for the half of this that must NOT move.
    """
    sched = steady_sched("WHEAT", 4)
    SA.PRICE_AWARE_SELL_CAP = True
    offered = _offer_a_day(sched, {"WHEAT": 80}, prices={"WHEAT": RT.BASE_PRICE["WHEAT"]})
    assert offered.get("WHEAT", 0) > 4, (
        f"offered only {offered.get('WHEAT', 0)} against a shed of 80 at a non-glut price -- "
        f"the row's day-total is still binding")


def test_flag_on_never_exceeds_the_per_offer_rate():
    """`rate[prod]` still bounds a SINGLE offer even with the flag on -- this is the whole fix.

    A first version of `PRICE_AWARE_SELL_CAP` set `n = have` outright, which let one turn's `have`
    -- e.g. right after a harvest lands -- go out as ONE order and walk the whole size down the
    price curve in a single turn's lockstep. Measured on the arena pool (seeds 500-505): win rate
    unchanged (94.4%, the pool was already saturated) but mean money fell ~30% against every single
    opponent (`data/logs/price_aware_arena_2026-08-08.log`) -- the same dump signature already
    measured on wool in `LIQUIDATE_FROM_HOUR`'s docstring (123 units -> 138, revenue $29,041 ->
    $21,811). This pins the fix: the day total may widen, but no single turn may offer more than
    `rate[prod]`.
    """
    sched = steady_sched("WHEAT", 4)
    SA.PRICE_AWARE_SELL_CAP = True
    # **`rate[prod]` is only the per-offer bound while `RESERVATION_SELL_CAP` is off.** That flag
    # deliberately replaces it with a bound derived from the live book (`reservation_units`), and with
    # both on this offered 20 against `rate=4`. That is NOT the uncapped dump the arena caught at -30%
    # mean money: the replacement is pinned by `test_the_offer_never_walks_the_price_past_the_slip` in
    # `tests/test_reservation_sell_cap.py`, which bounds an offer by how far it may walk the PRICE
    # instead of by a number copied off one replay's schedule. This test owns the legacy regime, so it
    # states which regime it is in rather than inheriting whatever the module default happens to be.
    _reservation = SA.RESERVATION_SELL_CAP
    SA.RESERVATION_SELL_CAP = False
    board = blank_board()
    agent = SA.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": 3000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    biggest = 0
    for hour in range(RT.TPD):
        obs = {"day": 0, "hour": hour, "farms": [farm], "step": hour,
               "market": {"prices": {"WHEAT": RT.BASE_PRICE["WHEAT"]}, "inventory": {}},
               "private": {"shed": {"WHEAT": 80}, "seeds": {}, "inventories": [{}]}}
        act = agent(obs)
        for o in act["market"]:
            if o[:2] == ["SELL", "WHEAT"]:
                biggest = max(biggest, int(o[2]))
    SA.RESERVATION_SELL_CAP = _reservation
    assert biggest <= 4, (
        f"a single turn offered {biggest} against a shed of 80 -- rate[prod]=4 must still bound "
        f"one offer even with the flag on, or this is the dump the arena measurement caught")


def test_flag_on_still_throttles_a_glutted_product():
    """MELON below `RT.BASE_PRICE['MELON']` (250): the existing, tuned caps are untouched.

    This is the case `PRICE_AWARE_SELL_CAP`'s own docstring says it must NOT touch -- the one
    product measured to respond visibly to volume (`docs/fable_market_selling_2026-08-08.md`). Kept
    inside `SHED_CAPACITY` for the same reason as the scarce test above.
    """
    sched = steady_sched("MELON", 4)
    SA.PRICE_AWARE_SELL_CAP = True
    glutted = _offer_a_day(sched, {"MELON": 80}, prices={"MELON": RT.BASE_PRICE["MELON"] - 1})
    SA.PRICE_AWARE_SELL_CAP = False
    off = _offer_a_day(sched, {"MELON": 80})
    assert glutted == off, (
        f"a glutted price must reproduce the flag-off row exactly: on={glutted} off={off}")
    assert glutted.get("MELON", 0) <= 4, (
        f"offered {glutted.get('MELON', 0)} of 80 against a glutted price -- the row's rate=4 "
        f"should still be the ceiling")


def test_flag_on_never_sells_the_herds_feed():
    """The wheat-feed reserve is netted into `have` upstream of this code; the flag cannot see past it.

    One live animal needs `feed_days(day) * 1` wheat reserved. Checked per TURN, not summed over a
    day: `_offer_a_day` hands back the same static shed every hour (deliberately, to isolate
    willingness-to-offer from market absorption -- see its docstring), so with the flag on and no
    day-total cap, the same `have` is a legitimately re-offered STANDING order 24 times, which is
    the documented, correct behaviour for a rate-bounded row too (`n = min(have, ...)` every turn)
    and is not what is under test here. What must never happen, on any single turn, is `have` itself
    including wheat the herd needs -- that reserve is subtracted upstream of this code
    (`_router_acts`'s `if prod == "WHEAT":` block) and the flag has no path around it.
    """
    sched = steady_sched("WHEAT", 2)
    SA.PRICE_AWARE_SELL_CAP = True
    reserve = SA.feed_days(0) * 1
    shed_wheat = reserve + 10
    board = blank_board()
    agent = SA.make_agent(sched, 0, router=True)
    farm = {"tiles": board, "money": 3000, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW"]}
    farm["tiles"][4][3] = {
        "kind": "PASTURE", "animal": "COW", "placed_day": 0,
        "consecutive_unfed": 0, "fed_today": False, "cared_today": False,
        "pending_care_bonus": False,
    }
    biggest = 0
    for hour in range(RT.TPD):
        obs = {"day": 0, "hour": hour, "farms": [farm], "step": hour,
               "market": {"prices": {"WHEAT": RT.BASE_PRICE["WHEAT"]}, "inventory": {}},
               "private": {"shed": {"WHEAT": shed_wheat}, "seeds": {}, "inventories": [{}]}}
        act = agent(obs)
        for o in act["market"]:
            if o[:2] == ["SELL", "WHEAT"]:
                biggest = max(biggest, int(o[2]))
    assert biggest <= shed_wheat - reserve, (
        f"a single turn offered {biggest} of a shed of {shed_wheat} with a live animal needing a "
        f"reserve of {reserve} -- the feed floor did not survive a non-glut price")
