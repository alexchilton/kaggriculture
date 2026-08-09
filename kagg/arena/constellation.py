"""Impose a town's shop-unlock draws instead of hoping a seed produces them.

**Why this exists.** The shop draw is not a function of the seed alone. `_end_of_day`
(`reference/kaggriculture.py:847-878`) spawns weeds on the same per-day `rng` *before* it draws the
next shop (`_spawn_weeds` at line 823, called at line 864; the shop draw is at line 878), and weed
spawning depends on which tiles are empty -- so how the agents play shifts the rng stream position
the shop draw lands on. Measured, same seed 29:

    PASS-vs-PASS play: PET_CAFE, FARMERS_MARKET, BRUNCH_SPOT, ICE_CREAM_SHOP, BAKERY, BAKERY,
                        BRUNCH_SPOT, BRUNCH_SPOT
    real agent play:   BRUNCH_SPOT, FARMERS_MARKET, ICE_CREAM_SHOP, YARN_STORE, PET_CAFE,
                        PET_CAFE, BAKERY, BAKERY

So a seed -> constellation catalogue is agent-dependent and goes stale whenever the agent changes.
Searching seeds for a wanted constellation cannot work; the constellation has to be imposed.

**How.** `forced_shops` patches `random.Random.choice` for the lifetime of the `with` block, but
only intercepts the exact call `_end_of_day` makes to draw a shop -- `rng.choice(sorted(SHOPS))`.
Every other draw (weed spawning uses `rng.random()`, not `.choice()`; any other code's `.choice()`
calls use different sequences) passes straight through to the original. The per-day `rng` inside
`_end_of_day` is a *fresh* `random.Random` instance, reseeded from `(seed, day)` and discarded when
the call returns, so whether the shop draw actually consumes it or is intercepted before doing so
has no effect on anything else that day or any later day. Unlock DAYS (every `townShopUnlockInterval`
days) and the `MAX_SHOP_INSTANCES` cap are untouched -- this overrides WHICH shop, never when or
how many.
"""

from __future__ import annotations

import contextlib
import itertools
import random
from typing import Dict, Iterator, List, Sequence, Tuple

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

# Re-exported for convenience -- callers building a full constellation need to know the cap.
MAX_SHOP_INSTANCES = kg.MAX_SHOP_INSTANCES

# The four products that actually matter for animal-product strategy (see
# docs/economics_q5_findings.md). All other SHOPS products (WHEAT, EGG, CARROT, TOMATO) are low
# value, which is exactly why 6,435 possible shop multisets collapse to 285 distinct drain vectors.
_DRAIN_PRODUCTS = ("MILK", "WOOL", "STRAWBERRY", "MELON")


@contextlib.contextmanager
def forced_shops(shops: Sequence[str]) -> Iterator[None]:
    """Force the town's shop-unlock draws to follow `shops`, in order.

    Every time the environment draws a new shop (every `townShopUnlockInterval` days, up to
    `MAX_SHOP_INSTANCES` total), it is handed the next entry of `shops` instead of a random one.
    If `shops` is exhausted before the game stops unlocking, later draws fall back to the
    environment's normal random draw. Everything else -- unlock timing, the instance cap, weed
    spawning, any other randomness -- is untouched.

    Restores `random.Random.choice` exactly on exit, including when the body raises.

        with forced_shops(["YARN_STORE", "YARN_STORE", "PIZZA_SHOP", ...]):
            env = make("kaggriculture", configuration={"seed": 13})
            ...play...
        # town["unlocked_shops"] follows the given list in order.
    """
    target = sorted(kg.SHOPS)
    queue = list(shops)
    original_choice = random.Random.choice

    def patched_choice(self, seq):
        if list(seq) == target and queue:
            return queue.pop(0)
        return original_choice(self, seq)

    random.Random.choice = patched_choice
    try:
        yield
    finally:
        random.Random.choice = original_choice


def drain_vector(shops: Sequence[str]) -> Tuple[int, int, int, int]:
    """Total per-tick drain a constellation of shops pulls from the four high-value products
    (MILK, WOOL, STRAWBERRY, MELON), matching `_town_consume`
    (`reference/kaggriculture.py:715-735`): each shop pulls one of every product it lists per
    tick, except a single-product shop pulls 2x of its one product.
    """
    totals = [0, 0, 0, 0]
    for shop in shops:
        products = kg.SHOPS[shop]
        multiplier = 2 if len(products) == 1 else 1
        for item in products:
            if item in _DRAIN_PRODUCTS:
                totals[_DRAIN_PRODUCTS.index(item)] += multiplier
    return tuple(totals)


def enumerate_constellations() -> List[List[str]]:
    """Enumerate one representative shop list per distinct drain vector.

    There are C(8 + 8 - 1, 8) = 6,435 multisets of `MAX_SHOP_INSTANCES` shops drawn with
    replacement from the 8 shop types, but only 285 distinct drain vectors over the four
    high-value products -- most shop types differ only in low-value products that don't matter
    for animal-product strategy. Returns 285 representative lists, each of exactly
    `MAX_SHOP_INSTANCES` shop names, one per distinct `drain_vector`, suitable for
    `forced_shops`.
    """
    shop_types = sorted(kg.SHOPS)
    seen: Dict[Tuple[int, int, int, int], List[str]] = {}
    for combo in itertools.combinations_with_replacement(shop_types, MAX_SHOP_INSTANCES):
        vec = drain_vector(combo)
        if vec not in seen:
            seen[vec] = list(combo)
    return list(seen.values())
