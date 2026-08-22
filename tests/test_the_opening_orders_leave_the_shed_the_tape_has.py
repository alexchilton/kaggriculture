"""The same ten orders in a different sequence buy a different farm. Pin the sequence by OUTCOME.

**The defect this pins.** `orders_from_heads` sorts the decoded orders by `SLOT_ORDER`, which was
`(SELL, BUY_SEED, BUY_PRODUCT, BUY_ANIMAL, HIRE, BUY_LAND)`. The teacher writes turn 0 as
`HIRE x5, BUY_ANIMAL COW 2, BUY_ANIMAL SHEEP 2, BUY_SEED WHEAT 7, BUY_SEED MELON 12,
BUY_PRODUCT WHEAT 6`. Same ten orders, and measured 2026-08-22 on the real environment:

    HIRE first (the tape)   bank 3000 -> 13    hands 5   shed {WHEAT: 5, COW: 2, SHEEP: 2}
    the old SLOT_ORDER      bank 3000 -> 484   hands 5   shed {WHEAT: 6, COW: 2, SHEEP: 1}

Both sheds hold exactly nine items -- **the shed capacity binds, and the sequence decides what
fills it**. Buying the wheat product before the animals costs a whole sheep and strands $471.

So the net emitted the correct ten orders and the DECODER turned them into a worse farm. That is
invisible to any agreement metric, because the bundle is a sorted multiset and scores as a hit.

A sweep of all distinct orderings found eight that reproduce the tape exactly and two that lose two
of the five hires outright (`hands 3`). `SELL HIRE ANIM SEED PROD LAND` is chosen because it is both
in the winning set and matches the teacher's own turn-0 sequence.

`SELL` stays first for the reason already in `orders_from_heads`: slots settle in sequence and a
sell in the same turn funds the purchases after it.
"""

import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from kagg.il import market_bundles as MB

OPENING = [["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
           ["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 2],
           ["BUY_SEED", "WHEAT", 7], ["BUY_SEED", "MELON", 12],
           ["BUY_PRODUCT", "WHEAT", 6]]

#: What the tape's own sequence produces, measured on the reference environment.
TAPE_BANK = 13.0
TAPE_SHED = {"WHEAT": 5, "COW": 2, "SHEEP": 2}
TAPE_HANDS = 5


def _decoded_opening():
    """The opening as `orders_from_heads` would emit it, from the bundle alone."""
    vocab = MB.Vocabulary.from_bundles([MB.bundle_of([]), MB.bundle_of(OPENING)])
    products, crops = list(MB.M.PRODUCTS), list(MB.F.CROPS)
    qty_sell = [0] * len(products)
    qty_buy_product = [0] * len(products)
    qty_buy_seed = [0] * len(crops)
    qty_buy_product[products.index("WHEAT")] = 6
    qty_buy_seed[crops.index("WHEAT")] = 7
    qty_buy_seed[crops.index("MELON")] = 12
    return MB.orders_from_heads(vocab, vocab.index(MB.bundle_of(OPENING)),
                                qty_sell=qty_sell, qty_buy_product=qty_buy_product,
                                qty_buy_seed=qty_buy_seed,
                                products=products, crops=crops, animals=list(MB.M.ANIMALS))


def _play_one_turn(market):
    """Step the REAL environment once. The outcome is the only thing that settles this."""
    import importlib.util

    import numpy as np
    from kaggle_environments import make

    spec = importlib.util.spec_from_file_location("dagger_tape", REPO / "scripts/dagger_tape.py")
    DT = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(DT)

    game = DT.episode_specs(DT.tape_games(), DT.opponent_pool(0), 0, np.random.default_rng(0))[0]
    env = make("kaggriculture", configuration=game["cfg"], debug=False)
    env.reset(2)
    seat = game["seat"]
    pair = [None, None]
    pair[seat] = {"farmer": ["BUILD_PASTURE"], "hands": [], "market": market}
    pair[1 - seat] = DT.opponent_action(game, 0, 0)
    env.step(pair)
    farm = env.state[seat].observation["farms"][seat]
    shed = {k: v for k, v in (env.state[seat].observation["private"]["shed"] or {}).items() if v}
    return farm.get("money"), len(farm.get("hands") or []), shed


def test_sell_is_still_first():
    """Unchanged and load-bearing: a sell in the same turn funds the purchases after it."""
    assert MB.SLOT_ORDER[0] == MB.SELL


def test_the_decoded_opening_buys_the_same_farm_as_the_tape():
    bank, hands, shed = _play_one_turn(_decoded_opening())
    assert hands == TAPE_HANDS, "all five hires must land"
    assert shed == TAPE_SHED, (
        "the shed capacity binds at nine items and the ORDER decides what fills it; "
        "buying the wheat product before the animals costs a sheep")
    assert bank == TAPE_BANK


def test_the_orders_are_the_same_ten():
    """The sequence changed; the set must not have."""
    got = sorted((o[0], o[1] if len(o) > 1 else "", o[2] if len(o) > 2 else 1)
                 for o in _decoded_opening())
    want = sorted((o[0], o[1] if len(o) > 1 else "", o[2] if len(o) > 2 else 1) for o in OPENING)
    assert got == want


def test_buying_the_product_early_is_what_breaks_it():
    """The mechanism, not just the symptom -- so a future reorder cannot silently reintroduce it."""
    early = sorted(OPENING, key=lambda o: ["SELL", "BUY_PRODUCT", "BUY_SEED",
                                           "BUY_ANIMAL", "HIRE"].index(o[0]))
    _bank, hands, shed = _play_one_turn(early)
    assert (shed, hands) != (TAPE_SHED, TAPE_HANDS), (
        "if this now matches, the shed capacity rule changed and SLOT_ORDER should be re-swept")
