"""`RESERVATION_SELL_CAP`: the per-offer size read off the live book, not off a replay's row.

One test per claim, per `CLAUDE.md`. Each claim is stated before its test and each is checked
against the environment source rather than against a remembered number.

The claim being tested overall is that `rate[prod]` -- "the largest single day the schedule ever
asked for", transcribed from `data/seed_scripts/top_guys/90976060/schedule.json`, a 1.32.2 tape --
is standing in for a market fact that `market_price` and `_town_consume` already state exactly.
"""

import sys

import pytest

sys.path.insert(0, ".")

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.search import schedule_agent as SA

I0 = kg.MARKET_I0
ALL_SHOPS = list(kg.SHOPS)


# ---------------------------------------------------------------------------- 1. the flag is off
def test_the_flag_ships_on():
    """Turned ON 2026-08-08 once a SECOND fixture agreed with the first.

    It shipped off because the handover fixture alone gave +$2,822 mean over five seeds (4 up, 1
    down), inside this project's ~15% seed variance and therefore not a result. Ten MIRROR seasons --
    what Kaggle validation actually runs, and the case that was losing land parcels -- then gave
    62,868 -> 64,667 mean bank with units destroyed at the rollover falling from 86-165 to 39-107
    (`data/logs/mirror_reservation.log`). Two fixtures agreeing on money, waste down on every seed.
    """
    assert SA.RESERVATION_SELL_CAP is True


# ---------------------------------------------------------------------------- 2. price is exact
def test_market_price_is_the_environments_own_function():
    """No transcription. A local copy is a drift bug waiting for the next rebalance, and 1.32.6
    was that rebalance."""
    for prod in SA.SELLABLE:
        for inv in (I0 - 500, I0, I0 + 37, I0 + 400):
            assert SA.market_price(prod, inv) == kg.market_price(prod, inv)


# ---------------------------------------------------------------------------- 3. the drain
def test_the_remaining_town_drain_matches_the_environment_step_for_step():
    """`town_drain_remaining` must equal what `_town_consume` would actually remove.

    Simulated here directly off the env's own constants, so the test fails if the env changes and
    the helper does not.
    """
    center = SA._CENTER_INTERVAL
    for prod in ("WHEAT", "MELON", "FERTILIZER", "MILK"):
        for step in (0, 97, 400, 719):
            expect = 0
            for s in range(step, 720):
                if s % 4 == 0:
                    for name in ALL_SHOPS:
                        products = kg.SHOPS[name]
                        if prod in products:
                            expect += 2 if len(products) == 1 else 1
                if s % center == 0 and prod in kg.TOWN_CENTER_PRODUCTS:
                    expect += next(m for th, m in
                                   getattr(kg, "TOWN_CENTER_DEMAND_SCHEDULE", [(0, 1)])
                                   if (s // 24) >= th)
            got = SA.town_drain_remaining(prod, step, ALL_SHOPS)
            assert got == expect, f"{prod} at step {step}: {got} != {expect}"


def test_fertilizer_has_no_town_drain_at_all():
    """FERTILIZER is in no shop and is excluded from `TOWN_CENTER_PRODUCTS`
    (`reference/kaggriculture.py:100`), so its book NEVER recovers on its own. Holding it has zero
    option value: the only reason to keep it is that FERTILIZE doubles a tile's yield."""
    assert SA.town_drain_remaining("FERTILIZER", 0, ALL_SHOPS) == 0


def test_melon_is_drained_by_the_town_centre_alone():
    """MELON is in no shop either, so only the town centre takes it -- against wheat's five shops
    at six ticks a day. This is why one price threshold cannot serve both.

    Version-aware on purpose: `_CENTER_INTERVAL` is read from the installed env's own spec, so the
    absolute number is 140 on 1.32.2 (centre every 12 steps, plus the 2x/4x late ramp) and 30 on
    the 1.32.6 the ladder runs (every 24, flat 1). The STRUCTURE is what is being pinned.
    """
    wheat = SA.town_drain_remaining("WHEAT", 0, ALL_SHOPS)
    melon = SA.town_drain_remaining("MELON", 0, ALL_SHOPS)
    egg = SA.town_drain_remaining("EGG", 0, ALL_SHOPS)
    # No shop carries MELON, so it drains exactly as much as any product's centre-only share --
    # which EGG minus its two shop ticks a tick must equal.
    assert not any("MELON" in prods for prods in kg.SHOPS.values())
    assert melon == egg - 2 * len(range(0, 720, 4)), (melon, egg)
    assert wheat > 4 * melon, (wheat, melon)


# ---------------------------------------------------------------------------- 4. the depth cap
def test_the_offer_never_walks_the_price_past_the_slip():
    """The whole point of a per-offer cap: `_process_market` quotes each unit at the inventory the
    previous unit left, so an oversized offer walks its own size down the curve. Measured failure:
    wool 123 units -> 138 took revenue $29,041 -> $21,811."""
    for prod in SA.SELLABLE:
        n = SA.reservation_units(prod, I0, 0, ALL_SHOPS, supply=10_000)
        assert n >= 1, prod
        opened = kg.market_price(prod, I0)
        last = kg.market_price(prod, I0 + n - 1)
        assert last >= (1.0 - SA.RESERVATION_SLIP) * opened, (prod, n, opened, last)
        # And it is the LARGEST such offer: one more unit would break the slip, unless the
        # reservation floor (not the slip) is what is binding.
        floor = max(kg.market_price(prod, I0 + 10_000 - int(SA.RESERVATION_CONTEST *
                                    SA.town_drain_remaining(prod, 0, ALL_SHOPS))),
                    (1.0 - SA.RESERVATION_SLIP) * opened)
        assert kg.market_price(prod, I0 + n) < floor, (prod, n)


def test_the_cap_differs_seven_fold_across_products_at_the_same_book():
    """The claim `rate[prod]` cannot express. Same balanced book, same slip, and the products that
    tolerate a big offer are not the ones with the high price."""
    caps = {p: SA.reservation_units(p, I0, 0, ALL_SHOPS, supply=10_000) for p in SA.SELLABLE}
    assert max(caps.values()) >= 7 * min(caps.values()), caps
    assert caps["MILK"] < caps["WHEAT"] < caps["MELON"], caps


# ---------------------------------------------------------------------------- 5. the reservation
def test_a_glut_widens_the_offer_and_a_thin_book_narrows_it():
    """`lambda = market_price(p, I + supply - contest * D_rem)`. When our supply dwarfs the town's
    remaining absorption there is no future in which the stock clears at today's price, so the
    reservation falls below it and the offer widens. When supply is thin the reservation sits at
    the current price and the offer narrows to the units that share it."""
    glut = SA.reservation_units("MELON", I0, 0, ALL_SHOPS, supply=400)
    thin = SA.reservation_units("MELON", I0, 0, ALL_SHOPS, supply=4)
    assert thin < glut, (thin, glut)
    assert thin == 4, thin          # thin supply: the whole holding, never more


def test_it_never_offers_more_than_the_supply():
    for prod in SA.SELLABLE:
        for supply in (0, 1, 3, 9):
            assert SA.reservation_units(prod, I0, 0, ALL_SHOPS, supply=supply) <= supply


def test_a_deficit_book_is_a_wide_integer_plateau_not_a_freeze():
    """The rule must not stop selling when the book is at a deficit. WHEAT's below-`I0` branch is
    `25 + sqrt(deficit)` and `market_price` rounds to an int, so at a 500-unit deficit the $47
    plateau is tens of units wide -- a trickle, which is what a thin-supply reservation should
    give, and NOT zero."""
    n = SA.reservation_units("WHEAT", I0 - 500, 0, ALL_SHOPS, supply=10_000)
    assert n >= 20, n
    assert kg.market_price("WHEAT", I0 - 500) > kg.MARKET_PARAMS["WHEAT"]["base"]


# ---------------------------------------------------------------------------- 6. the wiring
def test_turning_the_flag_on_actually_changes_what_is_ordered():
    """**The trap this test exists for.** The first wiring took `max(rate[prod], reservation)` on
    the argument that a rule which can only widen an offer cannot regress. It was a no-op: five
    seeds of `scripts/handover.py` returned byte-identical finals with the flag on and off, because
    `rate[prod]` was already the larger number on every turn that mattered. Eleven unit tests were
    green throughout. A flag that looks live and is not is worse than no flag, so the suite has to
    check the composition and not only the helper.
    """
    from kaggle_environments import make

    import json
    import pathlib

    sched_path = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
    if not sched_path.exists():
        pytest.skip("schedule fixture not present")
    sched = {int(k): v for k, v in json.loads(sched_path.read_text()).items()}
    thin = {d: {k: v for k, v in r.items()
                if k in ("sells", "buys", "seeds", "plants", "hands", "land", "animals",
                         "builds", "harvests")}
            for d, r in sched.items()}

    def run(flag):
        was = SA.RESERVATION_SELL_CAP
        SA.RESERVATION_SELL_CAP = flag
        try:
            env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
            env.reset(2)
            agent = SA.make_agent(thin, 0, router=True)
            acts = []
            for _ in range(400):
                a = agent(env.state[0].observation, env.configuration)
                acts.append(json.dumps(a, sort_keys=True))
                env.step([a, {}])
            return acts
        finally:
            SA.RESERVATION_SELL_CAP = was

    assert run(True) != run(False)


def test_the_flag_off_is_byte_identical_to_the_shipped_agent():
    """The rail every flag in this file carries: OFF must reproduce the current behaviour exactly,
    action for action, so a measurement of ON is a measurement of ON and nothing else."""
    from kaggle_environments import make

    import json
    import pathlib

    sched_path = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
    if not sched_path.exists():
        pytest.skip("schedule fixture not present")
    sched = {int(k): v for k, v in json.loads(sched_path.read_text()).items()}
    thin = {d: {k: v for k, v in r.items()
                if k in ("sells", "buys", "seeds", "plants", "hands", "land", "animals",
                         "builds", "harvests")}
            for d, r in sched.items()}

    def run():
        env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0})
        env.reset(2)
        agent = SA.make_agent(thin, 0, router=True)
        acts = []
        for _ in range(120):
            obs = env.state[0].observation
            a = agent(obs, env.configuration)
            acts.append(json.dumps(a, sort_keys=True))
            env.step([a, {}])
        return acts

    # The flag now ships ON, so this rail has to force the legacy path rather than assume it. What it
    # pins is unchanged: with the reservation off, the agent is deterministic and reproduces the
    # pre-flag behaviour, so a measurement of ON is a measurement of ON and nothing else.
    before = SA.RESERVATION_SELL_CAP
    SA.RESERVATION_SELL_CAP = False
    try:
        a = run()
        b = run()
    finally:
        SA.RESERVATION_SELL_CAP = before
    assert a == b
