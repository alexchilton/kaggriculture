"""How much of a hinge crop to grow, when, and only where it pays -- read off the board.

## Why this replaces two constants

The shipped late-carrot arm fires on two numbers:

    CARROT_DRAIN_MIN = 5     the town's carrot drain must be at least 5
    CARROT_OPP_MAX   = 7     the opponent must hold at most 7 carrot tiles

The first is measured -- 12,096 seasons, monotone in the threshold. **The second never was.**
`docs/carrot_refine_2026-08-22.md` says so in its own conclusions: "the opponent half of the rule is
still untested and needs a field containing a carrot player", and six of its nine arms were
identical by construction because not one pool opponent has ever withheld stock.

It cost a game. Ladder 98495047, seed 1640915609, lost by **$29,384**: town drain 11, so the drain
gate passed, and the opponent held **10** carrot tiles at d25, so `CARROT_OPP_MAX = 7` stood us
down. They took 76 units at $498 on the last day. Our gate read their carrot as "the book is taken"
when in a drain-11 town it meant "the book is rich".

Both constants are proxies for one quantity that is **directly readable**, so this computes that
quantity instead.

## The quantity

Price is a pure function of the town's inventory (`reference/kaggriculture.py:192-207`). Inventory
starts at `I0 = 10_000` for every product and moves three ways only: each unit either side sells
adds one, and the shops drain it on a fixed schedule (`_town_consume`). Define the **deficit**
`D = I0 - inventory`. For a `hinge` product the price is

    u = D / T ;   f = u + HINGE_GAIN * max(0, u - 1)^2 ;   price = base * (1 + target * f)

with `HINGE_GAIN = 8.0`. CARROT is `base 35, T 450, target 1.00`. Verified against a real
observation, d25 of that game: inventory 9261 gives D = 739, u = 1.64, f = 4.92, price $207 --
the tape recorded **$208**.

So the decision is not "is the opponent growing carrot". It is: **after everything both of us will
still sell, will D still be well past the knee when I come to sell?** The opponent's holdings enter
as supply that has not landed yet, which is why the sign of `CARROT_OPP_MAX` was wrong -- their
tiles are a cost to subtract, not a veto, and in a deep book the subtraction leaves plenty.

## What it decides

`plan(obs, ...)` returns `(tiles, why)`. `tiles == 0` means do not fire. Non-zero is how many tiles
to convert, sized so that the book is STILL above the knee after our own dump lands -- selling into
our own collapse is the failure mode `CARROT_OPP_MAX` was groping at.

**Deliberately not swept yet.** `U_MIN` and `SAFETY` are the two free numbers here and they are
first guesses. The test that matters is behavioural, not numeric, and it is in
`tests/test_the_book_is_cornered_only_when_it_is_deep.py`: fire on 98495047, stand down on the four
drain-2/3 towns from the same corpus. A threshold that cannot do both is wrong whatever it measures
on a pool that contains no withholder.
"""

import math

#: `reference/kaggriculture.py:178` -- every product's town inventory starts here.
MARKET_I0 = 10_000

#: `reference/kaggriculture.py:54-70`.
HINGE_GAIN = 8.0

#: The hinge products, with `(base, T, target)` from `MARKET_PARAMS`. Only these reward cornering:
#: on a flat curve, withholding earns nothing and risks the nightly shed overflow.
HINGE = {
    "CARROT": (35.0, 450.0, 1.00),
    "TOMATO": (60.0, 200.0, 0.40),
    "EGG": (50.0, 332.0, 0.40),
}

#: Units a tile yields. CARROT is `max_yield 4`, one-shot, `first_yield_day 2`.
YIELD_PER_TILE = {"CARROT": 4, "TOMATO": 4, "EGG": 1}

#: Fire only if the projected `u` clears this AFTER our own dump is priced in. 1.0 is the knee
#: itself; below it the quadratic term is zero and the crop is worth about what late wheat is.
U_MIN = 1.3

#: Fraction of the headroom above the knee we are willing to consume with our own sale. Selling
#: past this is selling into our own collapse.
SAFETY = 0.6

#: Turns per day, and the last day stock can still be banked.
TPD = 24
RELEASE_DAY = 29


def price_at(product, deficit):
    """What the town would pay for one unit at this deficit. The env's own curve, inverted."""
    base, T, target = HINGE[product]
    u = max(0.0, deficit) / T
    f = u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return base * (1.0 + target * f)


def deficit_now(obs, product):
    """`I0 - inventory`, straight off the shared observation."""
    inv = ((obs.get("market") or {}).get("inventory") or {}).get(product)
    if inv is None:
        return None
    return MARKET_I0 - int(inv)


def drain_per_day(obs, product, shops):
    """Units of `product` the town's unlocked shops pull per day.

    Mirrors `_town_consume`: each shop instance ticks 6 times a day, doubled for a shop that sells
    only this product, plus one a day from the town centre.
    """
    per_tick = 0
    for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
        products = shops.get(name) or []
        if product in products:
            per_tick += 2 if len(products) == 1 else 1
    return per_tick * 6 + 1


def opponent_units(obs, product, me):
    """Units the opponent can still put into the book: what stands on their tiles.

    Their shed is NOT visible -- `private` is per seat -- so this is a floor, not a total. Treating
    it as a floor is the safe direction: it under-states their supply, so it makes us fire less
    often rather than more.
    """
    farms = obs.get("farms") or []
    if len(farms) < 2:
        return 0
    crop = {"EGG": "GOOSE"}.get(product)
    theirs = farms[1 - me] or {}
    units = 0
    for row in (theirs.get("tiles") or []):
        for t in row:
            if not isinstance(t, dict):
                continue
            if crop and t.get("animal") == crop:
                units += t.get("yield_units") or 0
            elif not crop and t.get("crop") == product:
                units += max(t.get("yield_units") or 0, YIELD_PER_TILE.get(product, 4))
    return units


def plan(obs, shops, me=0, product="CARROT", ours_already=0, max_tiles=40):
    """`(tiles_to_convert, why)`. Zero means the book is not deep enough to be worth cornering.

    `ours_already` is what we will supply from stock we already hold or have growing; it is
    subtracted like the opponent's, because our own sale walks the same book down.
    """
    if product not in HINGE:
        return 0, f"{product} is not on the hinge curve"
    D = deficit_now(obs, product)
    if D is None:
        return 0, "no market inventory in the observation"

    day = int(obs.get("day", 0) or 0)
    days_left = max(0, RELEASE_DAY - day)
    base, T, target = HINGE[product]

    # Where the book will be when we come to sell, before we add anything to it.
    projected = D + drain_per_day(obs, product, shops) * days_left
    projected -= opponent_units(obs, product, me) + ours_already

    u = projected / T
    if u < U_MIN:
        return 0, (f"projected deficit {projected:.0f} is u={u:.2f}, under {U_MIN} -- "
                   f"the knee is at {T:.0f} and this book is not deep enough")

    # How much we can sell while staying above the knee, discounted by `SAFETY`. Each unit sold
    # lifts inventory by one and so cuts the deficit by one.
    headroom = max(0.0, projected - T)
    units = int(headroom * SAFETY)
    tiles = min(max_tiles, units // max(1, YIELD_PER_TILE.get(product, 4)))
    if tiles <= 0:
        return 0, f"headroom {headroom:.0f} is under one tile's yield"

    got = price_at(product, projected)
    after = price_at(product, projected - tiles * YIELD_PER_TILE.get(product, 4))
    return tiles, (f"deficit {D} now, {projected:.0f} projected at d{RELEASE_DAY} (u={u:.2f}); "
                   f"{tiles} tiles, price ${got:.0f} -> ${after:.0f} after our own dump")


def when_to_convert(obs, product="CARROT"):
    """The first day a conversion still ripens in time, given the crop's calendar.

    CARROT is `first_yield_day 2`, so a tile sown on d27 is not collectable until d29 and competes
    with the closing walk. Measured 2026-08-24: an arm converting on d27 left 11 tiles standing when
    it sold. The real opponent began on d21 and peaked at d26.
    """
    return RELEASE_DAY - 8 if product == "CARROT" else RELEASE_DAY - 8
