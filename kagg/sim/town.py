"""Batched town consumption: what the town removes from the market each step.

The drain schedule depends on nothing either player does, so for a fixed unlock order the whole
season's drain can be precomputed once and then applied by table lookup -- no per-step branching
at all. That is the cheapest win in the simulator.

The one thing that cannot be precomputed offline is *which* shop unlocks on a given day.
`_spawn_weeds` consumes one RNG draw per empty unlocked tile before `rng.choice` picks the shop,
so the order is a function of both players' board occupancy. The simulator has to generate it as
it goes, exactly as the reference does, or replays will not match. `unlock_schedule` therefore
takes the sequence as input rather than pretending to derive it.

Verified against `kagg.economics.market`, whose drain model is itself exact against live episodes
across every product and every step.
"""

import json
import pathlib

import numpy as np

import kaggle_environments
from kaggle_environments.envs.kaggriculture import kaggriculture as kg

from kagg.sim.market import N_PRODUCTS, PRODUCT_INDEX

_ENV_SPEC = json.loads(
    (pathlib.Path(kaggle_environments.__file__).parent
     / "envs/kaggriculture/kaggriculture.json").read_text())

#: The centre's per-day demand ramp, or a flat 1 where the installed env has no ramp at all.
#: 1.32.6 DELETED `TOWN_CENTER_DEMAND_SCHEDULE` -- it was `[(20, 4), (10, 2), (0, 1)]`, so late-season
#: drawdown fell from 4x-twice-daily to 1x-once-daily, an 8x cut. `getattr` rather than a version
#: check so the same source runs against both, and so this reads as flat instead of crashing.
CENTER_SCHEDULE = sorted(getattr(kg, "TOWN_CENTER_DEMAND_SCHEDULE", [(0, 1)]))

SHOPS = list(kg.SHOPS)
SHOP_INDEX = {name: i for i, name in enumerate(SHOPS)}
N_SHOPS = len(SHOPS)

TURNS_PER_DAY = 24
SHOP_INTERVAL = 4
#: **Read from the env's own spec, not hard-coded.** `kaggle-environments` 1.32.6 ("Kaggriculture town
#: rebalance", merged 2026-08-07) took `townCenterSellInterval` from 12 to 24, so the centre now buys
#: once a day rather than twice. A literal 12 here was silently a different game from the one the
#: leaderboard runs.
CENTER_INTERVAL = int(_ENV_SPEC["configuration"]["townCenterSellInterval"]["default"])

# [N_SHOPS, N_PRODUCTS] units pulled per shop tick. A single-product shop pulls double.
SHOP_PULL = np.zeros((N_SHOPS, N_PRODUCTS), dtype=np.int64)
for _name, _products in kg.SHOPS.items():
    _mult = 2 if len(_products) == 1 else 1
    for _p in _products:
        SHOP_PULL[SHOP_INDEX[_name], PRODUCT_INDEX[_p]] = _mult

# The town centre pulls every non-fertilizer product.
CENTER_PULL = np.zeros(N_PRODUCTS, dtype=np.int64)
for _p in kg.TOWN_CENTER_PRODUCTS:
    CENTER_PULL[PRODUCT_INDEX[_p]] = 1


def center_multiplier(day):
    """Town-centre demand ramp, as the INSTALLED env defines it.

    Was 1x, then 2x from day 10, then 4x from day 20. From 1.32.6 there is no ramp: a flat 1 all
    season. See `CENTER_SCHEDULE`.
    """
    day = np.asarray(day)
    out = np.ones(day.shape, dtype=np.int64) if day.ndim else 1
    for threshold, mult in CENTER_SCHEDULE:
        out = np.where(day >= threshold, mult, out)
    return out


def drain_at(step, unlocked_mask, turns_per_day=TURNS_PER_DAY):
    """Units removed from the market at `step`. `unlocked_mask` is [B, N_SHOPS] of bools.

    Mirrors `_town_consume`: shop ticks land on steps divisible by 4, the centre on steps
    divisible by 12, and the centre multiplier steps up with the day.
    """
    unlocked_mask = np.asarray(unlocked_mask, dtype=bool)
    batch = unlocked_mask.shape[0]
    drain = np.zeros((batch, N_PRODUCTS), dtype=np.int64)

    if step % SHOP_INTERVAL == 0:
        drain += unlocked_mask.astype(np.int64) @ SHOP_PULL

    if step % CENTER_INTERVAL == 0:
        drain += int(center_multiplier(step // turns_per_day)) * CENTER_PULL

    return drain


def season_drain_table(unlock_days, steps=719, turns_per_day=TURNS_PER_DAY):
    """Precompute drain for every step of a season, for one unlock schedule.

    `unlock_days` maps day -> shop name, as `kagg.economics.market.observe_unlocks` returns.
    Returns [steps, N_PRODUCTS], so the game loop reads a row instead of recomputing.
    """
    table = np.zeros((steps, N_PRODUCTS), dtype=np.int64)
    mask = np.zeros((1, N_SHOPS), dtype=bool)

    for step in range(steps):
        day = step // turns_per_day
        for unlock_day, shop in unlock_days.items():
            if unlock_day <= day:
                mask[0, SHOP_INDEX[shop]] = True
        table[step] = drain_at(step, mask, turns_per_day)[0]
    return table
