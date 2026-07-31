"""Closed-form model of the Kaggriculture market.

There is one global inventory per product, shared by both players.
Price is a pure function of that inventory.
The town drains inventory on a fixed schedule; player sales add to it.

The drain schedule depends on nothing either player does, so the season's whole price
envelope can be computed offline -- which is what this module is for.
One caveat, and it matters: *which* shop unlocks on a given day is drawn from an RNG that
`_spawn_weeds` has already consumed a per-empty-tile number of draws from, so the unlock
order is a function of board occupancy and cannot be predicted offline.
Callers therefore pass an unlock schedule in, and :func:`observe_unlocks` reads a real one
out of a live episode.

Market parameters and the price function are imported from the installed environment rather
than copied, so this module cannot drift away from ground truth.
"""

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

# Re-exported so callers need not reach into the env module themselves.
PRODUCTS = list(kg.PRODUCTS)
SHOPS = dict(kg.SHOPS)
BASE = {item: kg.MARKET_PARAMS[item]["base"] for item in PRODUCTS}
I0 = {item: kg.MARKET_PARAMS[item]["I0"] for item in PRODUCTS}

TURNS_PER_DAY = 24
EPISODE_STEPS = 720
DAYS = EPISODE_STEPS // TURNS_PER_DAY


def price(item, inventory, params=None):
    """Market price of `item` at `inventory`, exactly as the environment computes it."""
    return kg.market_price(item, inventory, params)


def _center_multiplier(day):
    return next(m for threshold, m in kg.TOWN_CENTER_DEMAND_SCHEDULE if day >= threshold)


def shops_active_at(step, unlocks, turns_per_day=TURNS_PER_DAY):
    """Shops consuming at `step`, given `unlocks` as a {day: shop_name} mapping.

    A shop recorded against day `d` is one that became visible on day `d`, i.e. it was
    chosen by the end-of-day handler for day `d - 1` and consumes from step `d * tpd` on.
    """
    day = step // turns_per_day
    return [shop for unlock_day, shop in sorted(unlocks.items()) if unlock_day <= day]


def town_drain(
    step,
    unlocks,
    turns_per_day=TURNS_PER_DAY,
    shop_interval=4,
    center_interval=12,
):
    """Units of each product the town removes from the market at `step`.

    Mirrors ``kaggriculture._town_consume``: shop ticks land on steps divisible by
    `shop_interval`, the town centre on steps divisible by `center_interval`, and a
    single-product shop pulls double.
    """
    drain = {item: 0 for item in PRODUCTS}

    if step % shop_interval == 0:
        for shop in shops_active_at(step, unlocks, turns_per_day):
            products = SHOPS[shop]
            multiplier = 2 if len(products) == 1 else 1
            for item in products:
                drain[item] += multiplier

    if step % center_interval == 0:
        center_mult = _center_multiplier(step // turns_per_day)
        for item in kg.TOWN_CENTER_PRODUCTS:
            drain[item] += center_mult

    return drain


def drain_per_day(unlocks, days=DAYS, turns_per_day=TURNS_PER_DAY, **kwargs):
    """Total town drain per product for each day, as {item: [day0, day1, ...]}."""
    per_day = {item: [0] * days for item in PRODUCTS}
    for day in range(days):
        for offset in range(turns_per_day):
            drain = town_drain(day * turns_per_day + offset, unlocks, turns_per_day, **kwargs)
            for item, n in drain.items():
                per_day[item][day] += n
    return per_day


def inventory_path(item, unlocks, sales=None, steps=EPISODE_STEPS - 1, turns_per_day=TURNS_PER_DAY, params=None):
    """Inventory of `item` after each of the first `steps` steps, and sale proceeds.

    `sales` is an optional {step: units} mapping of player sales, applied *before* that
    step's town drain, matching the environment's ordering (`_process_market` then
    `_town_consume`).
    Entry `s` of the returned path is the inventory once step `s` is fully processed, which
    is what the environment records at ``env.steps[s + 1]``.

    Returns ``(path, revenue)``.
    """
    sales = sales or {}
    inventory = I0[item]
    revenue = 0
    path = []
    for step in range(steps):
        qty = sales.get(step, 0)
        if qty:
            proceeds, inventory, _ = sell_revenue(item, inventory, qty, params)
            revenue += proceeds
        inventory -= town_drain(step, unlocks, turns_per_day)[item]
        path.append(inventory)
    return path, revenue


def sell_revenue(item, inventory, qty, params=None):
    """Proceeds from selling `qty` units into `inventory`, unit by unit.

    The environment quotes each unit at the inventory left by the previous unit, so a bulk
    sale walks the price down rather than clearing at one price.
    A unit that clears at the $1 floor does **not** raise inventory -- the floor absorbs
    unlimited volume without deepening the glut, which is why a crashed price recovers
    purely on town drain.

    Returns ``(revenue, inventory, unit_prices)``.
    """
    revenue = 0
    unit_prices = []
    for _ in range(qty):
        unit = price(item, inventory, params)
        revenue += unit
        unit_prices.append(unit)
        if unit > kg.PRICE_FLOOR:
            inventory += 1
    return revenue, inventory, unit_prices


def absorption(item, inventory, floor_frac=0.5, params=None, limit=10_000):
    """How many units can be sold at `inventory` before price falls below a fraction of base.

    This is the number that decides whether a product is worth committing tiles to: it is
    the depth of the market at an acceptable price, not the headline price.
    """
    threshold = floor_frac * BASE[item]
    sold = 0
    while sold < limit and price(item, inventory, params) >= threshold:
        inventory += 1
        sold += 1
    return sold


def observe_unlocks(seed, agent_a="pass", agent_b="pass"):
    """Play one episode and report {day: shop_name} for the shops that unlocked.

    Needed because the unlock draw shares an RNG with weed spawning, so the order is a
    function of how many empty tiles each player leaves and cannot be derived from the seed.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([agent_a, agent_b])

    unlocks = {}
    for step in env.steps:
        obs = step[0]["observation"]
        day = obs.get("day", 0)
        for shop in obs.get("town", {}).get("unlocked_shops", []):
            unlocks.setdefault(shop, day)
    return {day: shop for shop, day in unlocks.items()}
