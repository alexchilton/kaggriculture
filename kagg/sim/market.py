"""Batched market: prices and order settlement across B games at once.

This is the piece the design doc predicted parity would break on, so it is built first and tested
against the reference environment before anything else in the simulator exists.

The awkwardness is real. `_process_market` settles orders **one unit at a time, alternating
between both players**, re-quoting the price after every single unit. Two players each selling 200
melons is 400 sequential price lookups with a data dependency between each. There is no way to
vectorize *within* one order queue.

What does vectorize is **across games**. Every game in the batch settles its i-th unit
simultaneously, so a batch of 4096 games costs the same number of Python-level iterations as one
game. That is the whole trick, and it is why a numpy-batched simulator is worth building before
reaching for JAX: the control flow stays ordinary Python and only the arithmetic goes wide.

Price is a pure function of inventory, so it is exact under vectorization -- but only if the
rounding matches. The reference does `max(PRICE_FLOOR, int(round(price)))`; Python's `round` and
`numpy.rint` both round half to even, so they agree. `tests/test_sim_market.py` asserts that
across the full inventory range rather than trusting it.
"""

import numpy as np

from kaggle_environments.envs.kaggriculture import kaggriculture as kg

PRODUCTS = list(kg.PRODUCTS)
PRODUCT_INDEX = {name: i for i, name in enumerate(PRODUCTS)}
N_PRODUCTS = len(PRODUCTS)
PRICE_FLOOR = kg.PRICE_FLOOR

# Per-product curve parameters as arrays, so price() is one vector expression.
_P = [kg.MARKET_PARAMS[name] for name in PRODUCTS]
BASE = np.array([p["base"] for p in _P], dtype=np.float64)
I0 = np.array([p["I0"] for p in _P], dtype=np.float64)
T = np.array([p["T"] for p in _P], dtype=np.float64)

_SHAPES = ("linear", "sq", "sqrt", "log", "log10")
_SHAPE_ID = {name: i for i, name in enumerate(_SHAPES)}
BELOW_FUNC = np.array([_SHAPE_ID[p["below_func"]] for p in _P], dtype=np.int64)
ABOVE_FUNC = np.array([_SHAPE_ID[p["above_func"]] for p in _P], dtype=np.int64)
BELOW_TARGET = np.array([p["below_target"] for p in _P], dtype=np.float64)
ABOVE_TARGET = np.array([p["above_target"] for p in _P], dtype=np.float64)


def _shape(func_id, x):
    """Vectorized `kaggriculture._shape`, selecting per element by function id.

    `func_id` broadcasts against `x`, so this works for a full [B, N_PRODUCTS] grid and for a
    single product's [B] column alike.
    """
    x = np.maximum(np.asarray(x, dtype=np.float64), 0.0)
    func_id = np.asarray(func_id)
    out = np.zeros(np.broadcast(func_id, x).shape, dtype=np.float64)
    branches = (x, x * x, np.sqrt(x), np.log1p(x), np.log10(1.0 + x))
    for fid, values in enumerate(branches):
        np.copyto(out, np.broadcast_to(values, out.shape), where=(func_id == fid))
    return out


# `amp` depends only on constants, so precompute it once.
_BELOW_AMP = BELOW_TARGET * BASE / _shape(BELOW_FUNC, T)
_ABOVE_AMP = ABOVE_TARGET * BASE / _shape(ABOVE_FUNC, T)


def _price_from(inventory, base, i0, below_func, below_amp, above_func, above_amp):
    inventory = np.asarray(inventory, dtype=np.float64)
    scarce = base + below_amp * _shape(below_func, i0 - inventory)
    glut = base - above_amp * _shape(above_func, inventory - i0)
    raw = np.where(inventory < i0, scarce, glut)
    return np.maximum(PRICE_FLOOR, np.rint(raw)).astype(np.int64)


def price(inventory):
    """Price of every product in every game. `inventory` is [..., N_PRODUCTS]."""
    return _price_from(inventory, BASE, I0, BELOW_FUNC, _BELOW_AMP, ABOVE_FUNC, _ABOVE_AMP)


def price_of(product, inventory):
    """Price of one product across a batch. `inventory` is any shape, typically [B]."""
    i = PRODUCT_INDEX[product] if isinstance(product, str) else int(product)
    return _price_from(
        inventory, BASE[i], I0[i], BELOW_FUNC[i], _BELOW_AMP[i], ABOVE_FUNC[i], _ABOVE_AMP[i]
    )


def settle_sales(product, inventory, orders, money, held):
    """Settle simultaneous sell orders across a batch of games, one unit at a time.

    Shapes: `inventory`, and `[B]` or `[B, P]` for the rest, where P is the number of players
    whose orders settle concurrently. Player columns are processed in seat order within each unit
    step, matching `_process_market`, which quotes both players against the same pre-commit
    inventory and then commits them in order.

    Follows `_commit_unit`: a unit clearing at the floor still pays out but does **not** raise
    inventory. That is why a crashed price recovers on town drain alone, and it bounds how much
    damage a price attack can do.

    Returns `(inventory, money, held)` with the same shapes as the inputs.
    """
    inventory = np.array(inventory, dtype=np.int64, copy=True)
    orders = np.atleast_2d(np.array(orders, dtype=np.int64, copy=True).T).T
    money = np.atleast_2d(np.array(money, dtype=np.float64, copy=True).T).T
    held = np.atleast_2d(np.array(held, dtype=np.int64, copy=True).T).T
    if orders.ndim == 1:
        orders, money, held = orders[:, None], money[:, None], held[:, None]

    remaining = orders.copy()
    n_players = remaining.shape[1]

    for _ in range(int(remaining.max()) if remaining.size else 0):
        if not (remaining > 0).any():
            break
        for seat in range(n_players):
            active = (remaining[:, seat] > 0) & (held[:, seat] > 0)
            if not active.any():
                continue
            unit_price = price_of(product, inventory)
            money[:, seat] = np.where(active, money[:, seat] + unit_price, money[:, seat])
            held[:, seat] = np.where(active, held[:, seat] - 1, held[:, seat])
            remaining[:, seat] = np.where(active, remaining[:, seat] - 1, remaining[:, seat])
            inventory = np.where(active & (unit_price > PRICE_FLOOR), inventory + 1, inventory)

    squeeze = np.asarray(orders).shape[1] == 1
    if squeeze:
        return inventory, money[:, 0], held[:, 0]
    return inventory, money, held
