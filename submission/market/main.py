"""Shop Router 0909 with its SELL layer gated on the quote it would walk down to.

The field plan is the parent's, action for action. Only the market channel is
rewritten, and only by REMOVING or SHRINKING sells whose marginal unit would
clear below a per-product floor. Nothing is added, reordered, or moved between
turns, so the parent's funding order is preserved.

Three guards, each from a measured failure:

  funding   Sells pay for the buys that follow them in the same queue. A unit is
            only withheld while the turn's remaining purchases stay affordable.
            (Reference dataset, Closer Cleo: hoisting sells starved a later
            BUY_PRODUCT, the animals went unfed and the farm lost far more than
            the reordering gained.)
  shed      Withheld goods stay in the shed, capacity 100. Near the cap the gate
            opens, because an overflow loses the unit outright.
  endgame   A unit may only be held if the season has time to recover the price.
            Measured on seed 4242: with the gate open to day 29 the two banks ran
            within $900 to day 22 and then split -2,182, -4,965, -8,530, -12,891
            over the last week, because the tape's heavy sell phase is days 23-29
            and a unit withheld there is never sold. The gate now closes at day 22.

Price model copied from the engine: a quote is a pure function of the shared
market inventory, so selling n units walks the price down n times. Steep
above-curves are the only place this can matter -- MELON above_target 3.60 and
WOOL 3.20 on a squared curve, against WHEAT and EGG at 0.20 on a log.
"""
import importlib.util
import math
import sys
from pathlib import Path

PRICE_FLOOR = 1
MARKET_I0 = 10000
HINGE_GAIN = 4.0
MARKET_PARAMS = {
    "WHEAT":      {"base":  25, "T": 400, "below_func": "sqrt",   "below_target": 0.80, "above_func": "log",    "above_target": 0.20},
    "CARROT":     {"base":  35, "T": 450, "below_func": "hinge",  "below_target": 1.00, "above_func": "sqrt",   "above_target": 0.70},
    "TOMATO":     {"base":  60, "T": 200, "below_func": "hinge",  "below_target": 0.40, "above_func": "sqrt",   "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "T": 100, "below_func": "sqrt",   "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON":      {"base": 250, "T": 300, "below_func": "log",    "below_target": 0.20, "above_func": "sq",     "above_target": 3.60},
    "EGG":        {"base":  50, "T": 332, "below_func": "hinge",  "below_target": 0.40, "above_func": "log",    "above_target": 0.20},
    "MILK":       {"base": 160, "T": 122, "below_func": "sqrt",   "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL":       {"base": 200, "T": 105, "below_func": "log",    "below_target": 0.20, "above_func": "sq",     "above_target": 3.20},
    "FERTILIZER": {"base": 100, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}
# Withhold a unit whose quote sits below this fraction of the product's base.
# One number per product, and only the steep curves are gated at all.
FLOOR_FRACTION = {"MELON": 0.45, "WOOL": 0.45, "STRAWBERRY": 0.40, "MILK": 0.40}
SHED_CAPACITY = 100
SHED_HEADROOM = 12
NO_HOLD_AFTER_STEP = 22 * 24   # day 22; see the endgame note above


def _shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def market_price(item, inventory):
    p = MARKET_PARAMS[item]
    base, T = p["base"], p["T"]
    if inventory < MARKET_I0:
        amp = p["below_target"] * base / _shape(p["below_func"], T, T)
        price = base + amp * _shape(p["below_func"], MARKET_I0 - inventory, T)
    else:
        amp = p["above_target"] * base / _shape(p["above_func"], T, T)
        price = base - amp * _shape(p["above_func"], inventory - MARKET_I0, T)
    return max(PRICE_FLOOR, int(round(price)))


def _load_parent():
    folder = Path(_load_parent.__code__.co_filename).resolve().parent
    path = folder / "router_parent.py"
    spec = importlib.util.spec_from_file_location("_market_parent", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["_market_parent"] = module
    spec.loader.exec_module(module)
    return module, folder


_PARENT_MODULE, _FOLDER = _load_parent()
_POLICY = _PARENT_MODULE.Policy(_FOLDER)


def _shed_total(observation):
    shed = observation["private"]["shed"]
    return sum(max(0, int(v)) for v in shed.values())


def gate_sells(action, observation, step):
    """Shrink SELL quantities whose marginal unit clears under the floor."""
    orders = action.get("market") or []
    if not orders or step >= NO_HOLD_AFTER_STEP:
        return action
    if _shed_total(observation) >= SHED_CAPACITY - SHED_HEADROOM:
        return action

    inventory = observation["market"]["inventory"]
    money = int(observation["farms"][observation["player"]]["money"])
    # An order is an OFFER, not a fill. This agent re-offers the same quota every
    # turn and the engine fills only what the shed actually holds, so the price
    # walk must run over deliverable units -- never over the offered quantity.
    # Walking the offer instead withheld 1,993 MILK in one season and cost $25k.
    shed = {k: max(0, int(v)) for k, v in observation["private"]["shed"].items()}

    # What the untouched queue would raise, and what it must pay for.
    planned_revenue = 0
    required = 0
    for order in orders:
        if not order:
            continue
        op = order[0]
        if op == "SELL" and order[1] in MARKET_PARAMS:
            inv = int(inventory.get(order[1], MARKET_I0))
            for i in range(min(int(order[2]), shed.get(order[1], 0))):
                planned_revenue += market_price(order[1], inv + i)
        elif op == "BUY_PRODUCT" and len(order) > 2 and order[1] in MARKET_PARAMS:
            inv = int(inventory.get(order[1], MARKET_I0))
            required += market_price(order[1], inv) * int(order[2])

    budget_slack = money + planned_revenue - required

    gated = []
    for order in orders:
        if not order or order[0] != "SELL" or order[1] not in FLOOR_FRACTION:
            gated.append(order)
            continue
        item = order[1]
        want = min(int(order[2]), shed.get(item, 0))
        if want <= 0:                      # nothing deliverable, leave the offer alone
            gated.append(order)
            continue
        floor = FLOOR_FRACTION[item] * MARKET_PARAMS[item]["base"]
        inv = int(inventory.get(item, MARKET_I0))
        keep = 0
        for i in range(want):
            price = market_price(item, inv + i)
            if price < floor and budget_slack >= price:
                budget_slack -= price      # withholding costs us that revenue
                continue
            keep = i + 1
        if keep >= want:
            gated.append(order)            # offer unchanged, including its headroom
        elif keep > 0:
            gated.append([order[0], item, keep])
        # keep == 0 drops the order; the slot stays empty, order is not reshuffled
    action["market"] = gated
    return action


def agent(observation, configuration=None):
    action = _POLICY.act(observation)
    return gate_sells(action, observation, int(observation["step"]))
