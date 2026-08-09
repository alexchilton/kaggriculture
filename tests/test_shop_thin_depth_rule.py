"""`SHOP_THIN_DEPTH_RULE`: the per-product, shop-keyed version of the below-base depth rule.

One test per claim, per `CLAUDE.md`. The claim under test is that the below-base sell branch can
be made to apply `reservation_units` -- the same live-book depth rule the above-base branch
already ships with -- WITHOUT reproducing the measured loss of the blanket version, by gating it
on `shop_thin(prod, unlocked_shops)`: whether the town currently has any shop open that sells the
product.

Every claim here was RED before the corresponding code existed: `shop_thin` and
`below_base_sell_units` did not exist on this branch, so importing them raised `AttributeError`
before `kagg/search/schedule_agent.py` was edited.
"""

import json
import pathlib

import pytest

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.search import schedule_agent as SA

I0 = kg.MARKET_I0
ALL_SHOPS = list(kg.SHOPS)


# ---------------------------------------------------------------------------- 1. shop_thin itself
def test_melon_is_thin_on_every_board():
    """No shop in `kg.SHOPS` carries MELON, so it must read thin whatever is unlocked."""
    assert not any("MELON" in prods for prods in kg.SHOPS.values())
    assert SA.shop_thin("MELON", []) is True
    assert SA.shop_thin("MELON", ALL_SHOPS) is True


def test_wool_is_thin_until_yarn_store_unlocks():
    """WOOL's only shop is YARN_STORE. Thin before it unlocks, not thin the moment it does."""
    assert SA.shop_thin("WOOL", []) is True
    assert SA.shop_thin("WOOL", ["BAKERY", "FARMERS_MARKET"]) is True
    assert SA.shop_thin("WOOL", ["YARN_STORE"]) is False
    assert SA.shop_thin("WOOL", ["BAKERY", "YARN_STORE"]) is False


def test_milk_needs_one_of_its_three_shops():
    assert SA.shop_thin("MILK", ["BAKERY", "FARMERS_MARKET", "YARN_STORE"]) is True
    for shop in ("ICE_CREAM_SHOP", "PIZZA_SHOP", "SMOOTHIE_SHOP"):
        assert SA.shop_thin("MILK", [shop]) is False


def test_fertilizer_is_always_thin():
    """No shop sells FERTILIZER and it is not in `TOWN_CENTER_PRODUCTS` either -- the same fact
    `test_fertilizer_has_no_town_drain_at_all` pins from the other direction."""
    assert SA.shop_thin("FERTILIZER", ALL_SHOPS) is True
    assert SA.town_drain_remaining("FERTILIZER", 0, ALL_SHOPS) == 0


# ---------------------------------------------------------------------------- 2. the sizing helper
def test_below_base_sizing_is_unchanged_with_the_flag_off():
    """`SHOP_THIN_DEPTH_RULE` off must reproduce the exact pre-flag arithmetic:
    `min(have, allow, rate_cap)`, then trimmed by what the day already sold."""
    assert SA.SHOP_THIN_DEPTH_RULE is False
    n = SA.below_base_sell_units("MELON", have=50, allow=30, rate_cap=100, sold_today=5,
                                 market_inv=I0 + 200, step=0, unlocked_shops=[], supply=50)
    assert n == min(50, 30, 100) - 5 == 25


def test_the_flag_only_fires_when_the_product_is_shop_thin():
    """A product WITH its shop open must keep the old day-total sizing even with the flag on --
    that is the entire content of the gate, and this is the test that would fail if the gate were
    accidentally dropped and the flag reproduced the measured-losing blanket version."""
    was = SA.SHOP_THIN_DEPTH_RULE
    SA.SHOP_THIN_DEPTH_RULE = True
    try:
        old = SA.below_base_sell_units("WOOL", have=200, allow=30, rate_cap=19,
                                       market_inv=I0 + 50, sold_today=0, step=0,
                                       unlocked_shops=["YARN_STORE"], supply=200)
        assert old == min(200, 30, 19)
    finally:
        SA.SHOP_THIN_DEPTH_RULE = was


def test_the_flag_changes_sizing_when_the_product_is_shop_thin():
    """The case the flag exists for: MELON, deep below base, no shop ever open for it. The
    reservation rule must produce a DIFFERENT number from the day-total cap, or the flag is wired
    to nothing (`RESERVATION_SELL_CAP`'s own history: a first wiring was measured a no-op with
    every component test green)."""
    was = SA.SHOP_THIN_DEPTH_RULE
    SA.SHOP_THIN_DEPTH_RULE = True
    try:
        off_n = SA.below_base_sell_units("MELON", have=140, allow=140, rate_cap=140,
                                         sold_today=0, market_inv=I0 + 100, step=0,
                                         unlocked_shops=[], supply=140)
        SA.SHOP_THIN_DEPTH_RULE = False
        on_n = SA.below_base_sell_units("MELON", have=140, allow=140, rate_cap=140,
                                        sold_today=0, market_inv=I0 + 100, step=0,
                                        unlocked_shops=[], supply=140)
        assert off_n != on_n, (off_n, on_n)
    finally:
        SA.SHOP_THIN_DEPTH_RULE = was


# ---------------------------------------------------------------------------- 3. composition
SCHED_PATH = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")


def _thin_schedule():
    sched = {int(k): v for k, v in json.loads(SCHED_PATH.read_text()).items()}
    return {d: {k: v for k, v in r.items()
                if k in ("sells", "buys", "seeds", "plants", "hands", "land", "animals",
                         "builds", "harvests")}
            for d, r in sched.items()}


def _mirror_run(cand_flag, steps, seed=11):
    """Both seats play the SAME schedule against each other -- the contested-book case this flag
    is meant for. A single agent against an empty `{}` opponent never contests its own book, so
    `have` never exceeds the old day-total cap and the flag is a provable no-op measured against
    the wrong fixture -- confirmed directly: 301 below-base MELON turns on seed 11 single-agent,
    zero of them differing. Mirrored, seed 11 alone produces 13 differing turns.

    Only seat 0 (the candidate) has the flag under test; seat 1 is always the shipped baseline, so
    a difference in seat 0's own action stream is attributable to seat 0's own rule and nothing
    the opponent did.
    """
    from kaggle_environments import make

    was = SA.SHOP_THIN_DEPTH_RULE
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0})
    env.reset(2)
    sched = _thin_schedule()
    SA.SHOP_THIN_DEPTH_RULE = cand_flag
    seat0 = SA.make_agent(sched, 0, router=True)
    SA.SHOP_THIN_DEPTH_RULE = was
    seat1 = SA.make_agent(sched, 1, router=True)
    acts0 = []
    try:
        for _ in range(steps):
            if env.done:
                break
            obs0 = env.state[0].observation
            obs1 = env.state[1].observation
            SA.SHOP_THIN_DEPTH_RULE = cand_flag
            a0 = seat0(obs0, env.configuration)
            SA.SHOP_THIN_DEPTH_RULE = was
            a1 = seat1(obs1, env.configuration)
            acts0.append(json.dumps(a0, sort_keys=True))
            env.step([a0, a1])
        return acts0
    finally:
        SA.SHOP_THIN_DEPTH_RULE = was


@pytest.mark.slow
def test_the_flag_off_is_byte_identical_to_the_shipped_agent():
    """The rail every flag in this file carries: OFF must reproduce current behaviour exactly, so
    a measurement of ON is a measurement of ON and nothing else."""
    if not SCHED_PATH.exists():
        pytest.skip("schedule fixture not present")
    a = _mirror_run(False, 200)
    b = _mirror_run(False, 200)
    assert a == b


@pytest.mark.slow
def test_turning_the_flag_on_actually_changes_what_is_ordered():
    """Composition check, not just the helper -- the exact trap `RESERVATION_SELL_CAP`'s own
    history warns about (a no-op wiring with every component test green). Mirrored so the book is
    actually contested; a lone agent against an empty opponent never floods its own book -- see
    `_mirror_run`'s docstring for the measurement that ruled that fixture out."""
    if not SCHED_PATH.exists():
        pytest.skip("schedule fixture not present")
    steps = 24 * 30
    on = _mirror_run(True, steps)
    off = _mirror_run(False, steps)
    assert on != off
