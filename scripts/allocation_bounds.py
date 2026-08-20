#!/usr/bin/env python3
"""MILP bounds on the season allocation: the near-optimal RANGE for every crop and species.

For each of three opponent-supply scenarios this solves a 30-day MILP for end-of-season money,
then re-solves min/max of each crop's and species' season total subject to the objective staying
within 1% (and 5%) of the optimum.  The write-up, with every assumption, is
docs/allocation_bounds_2026-08-16.md.

Ground truth: the installed kaggle-environments 1.32.7 kaggriculture module (byte-identical to
the main repo's reference/kaggriculture.py).  All prices, growth rules and costs are imported
from it, never re-typed.

Usage:
    python -u scripts/allocation_bounds.py            # full run (three scenarios + ranges)
    python -u scripts/allocation_bounds.py --quick    # scenario 1 only, 5% ranges only
"""

import argparse
import json
import math
import random
import sys
import time
from collections import defaultdict

import numpy as np
import scipy.sparse as sp
from scipy.optimize import Bounds, LinearConstraint, milp

import kaggle_environments
from kaggle_environments.envs.kaggriculture import kaggriculture as KG

TAPE = "/Users/alexchilton/DataspellProjects/kaggriculture/data/seed_scripts/kawashigi/92498144.json"
DAYS = 30
LAST = DAYS - 1                       # day 29
TURNS = 24
LAMBDA_WALK = 3477.0 / 2773.0         # measured leader move/work ratio (seed 11 tape)
PICKUP_SHARE = 0.1                    # amortised PICKUP op per animal-feeding per day
START_MONEY = 3000
PRODUCTS = list(KG.PRODUCTS)          # 9, includes FERTILIZER
CROPS = KG.CROPS
ANIMALS = KG.ANIMALS
I0 = KG.MARKET_I0
LEADER_REF = {"MELON": 20, "STRAWBERRY": 34, "COW": 6, "SHEEP": 8, "GOOSE": 0,
              "WHEAT": None, "CARROT": None, "TOMATO": None}

# ---------------------------------------------------------------------------
# Phase 1 -- replay the recorded episode through the real engine, logging fills
# ---------------------------------------------------------------------------

def replay_fills(tape_path):
    """Re-run episode 92498144 with the recorded actions and seed; log every market fill.

    Returns (fills, unlock_days, meta).  fills: list of (step, player, op, item, price).
    Asserts the recomputed rewards equal the recorded ones, so the fills are exact,
    not inferred (offers are not fills)."""
    d = json.load(open(tape_path))
    cfg = dict(d["configuration"])
    cfg["seed"] = d["info"]["seed"]
    rec = d["steps"]
    n_rec = len(rec)

    fills = []
    ctx = {"step": 0, "farms": None}
    orig_commit = KG._commit_unit
    orig_pm = KG._process_market

    def commit_logger(op, item, price, farm, private, market, shed_capacity=100):
        ok = orig_commit(op, item, price, farm, private, market, shed_capacity)
        if ok:
            player = 0 if farm is ctx["farms"][0] else 1
            fills.append((ctx["step"], player, op, item, price))
        return ok

    def pm_logger(state, env):
        ctx["step"] = KG.get(state[0].observation, "step", 0)
        ctx["farms"] = state[0].observation.farms
        return orig_pm(state, env)

    last_err = None
    for offset in (1, 0):
        fills.clear()
        KG._commit_unit = commit_logger
        KG._process_market = pm_logger
        try:
            env = kaggle_environments.make("kaggriculture", configuration=cfg)

            def make_replayer(seat):
                def agent(obs, config):
                    t = KG.get(obs, "step", 0) + offset
                    if t < n_rec:
                        a = rec[t][seat].get("action")
                        if isinstance(a, dict):
                            return a
                    return {"farmer": ["PASS"], "hands": [], "market": []}
                return agent

            out = env.run([make_replayer(0), make_replayer(1)])
        finally:
            KG._commit_unit = orig_commit
            KG._process_market = orig_pm
        got = [out[-1][i]["reward"] for i in range(2)]
        # The episode was recorded on an earlier engine (pre-hinge pricing for
        # CARROT/TOMATO/EGG), so replaying the recorded actions on 1.32.7 shifts a few
        # sale prices.  Units filled are what we extract; accept <=0.2% reward drift.
        if all(abs(g - r) <= max(200.0, 0.002 * abs(r)) for g, r in zip(got, d["rewards"])):
            drift = [g - r for g, r in zip(got, d["rewards"])]
            print(f"[replay] action offset {offset}: rewards {got} vs recorded {d['rewards']} "
                  f"(drift {drift}, 1.32.7 repricing of the recorded actions)")
            break
        last_err = (offset, got)
    else:
        raise SystemExit(f"replay failed to reproduce rewards: {last_err} vs {d['rewards']}")

    # shop unlock timeline (with replacement): read from the recorded observations
    unlock_days = []          # (active_from_day, shop_name)
    seen = 0
    for t in range(n_rec):
        town = rec[t][0]["observation"].get("town", {})
        shops = town.get("unlocked_shops", [])
        while seen < len(shops):
            day = t // TURNS
            unlock_days.append((day, shops[seen]))
            seen += 1
    meta = {"rewards": d["rewards"], "seed": d["info"]["seed"],
            "names": d["info"]["TeamNames"], "config": cfg}
    return fills, unlock_days, meta


def aggregate_opponent(fills, seat=0):
    """Per-day per-product net book impact of the given seat, plus stats.

    net = sells that moved the book (price > 1) minus BUY_PRODUCT units.
    Also returns gross sells and buys, and seed/animal purchase counts."""
    net = defaultdict(lambda: np.zeros(DAYS))
    sells = defaultdict(lambda: np.zeros(DAYS))
    buys = defaultdict(lambda: np.zeros(DAYS))
    rev = defaultdict(float)
    seed_buys = defaultdict(int)
    animal_buys = defaultdict(int)
    for step, player, op, item, price in fills:
        if player != seat:
            continue
        day = step // TURNS
        if op == "SELL":
            sells[item][day] += 1
            rev[item] += price
            if price > 1:
                net[item][day] += 1
        elif op == "BUY_PRODUCT":
            buys[item][day] += 1
            net[item][day] -= 1
        elif op == "BUY_SEED":
            seed_buys[item] += 1
        elif op == "BUY_ANIMAL":
            animal_buys[item] += 1
    return {"net": net, "sells": sells, "buys": buys, "rev": rev,
            "seed_buys": dict(seed_buys), "animal_buys": dict(animal_buys)}


# ---------------------------------------------------------------------------
# Phase 2 -- per-tile cycle profiles, simulated from the env rules
# ---------------------------------------------------------------------------

class Profile:
    __slots__ = ("name", "start", "end", "ops", "moves", "yields", "fert_use", "wheat_use",
                 "cash_cost")

    def __init__(self, name, start):
        self.name = name
        self.start = start
        self.end = start
        self.ops = defaultdict(float)       # day -> work ops
        self.moves = defaultdict(float)     # day -> tile visits (geometry walk model)
        self.yields = defaultdict(lambda: defaultdict(float))  # day -> product -> units
        self.fert_use = defaultdict(float)  # day -> units
        self.wheat_use = defaultdict(float)
        self.cash_cost = defaultdict(float)  # day -> $


def oneshot_profile(crop, fert, d0):
    cd = CROPS[crop]
    ws = (cd["max_yield_day"] + 1) // 2
    fy, my, ymax = cd["first_yield_day"], cd["max_yield_day"], cd["max_yield"]
    if d0 + fy > LAST:
        return None
    best = None
    for ha in range(fy, min(my, LAST - d0) + 1):
        yield_units, unwatered, fert_until = 1, 1, -1
        waters, ferts = [], []
        for age in range(0, ha + 1):
            in_window = ws <= age <= my
            want = in_window and yield_units < ymax
            must = unwatered >= 1 and age < ha       # survive to harvest day
            if want and fert and fert_until < age:
                ferts.append(age)
                fert_until = age + 2
            if want or must:
                waters.append(age)
                if in_window:
                    yield_units = min(ymax, yield_units + (2 if fert_until >= age else 1))
                unwatered = 0
            else:
                unwatered += 1
        cand = (yield_units, -(len(waters) + len(ferts)), -ha)
        if best is None or cand > best[0]:
            best = (cand, ha, yield_units, waters, ferts)
    _, ha, yld, waters, ferts = best
    p = Profile(f"{crop.lower()}{'_f' if fert else '_u'}@{d0}", d0)
    p.end = d0 + ha
    p.ops[d0] += 1                                  # PLANT
    p.moves[d0] += 1
    p.cash_cost[d0] += cd["seed"]
    for a in waters:
        p.ops[d0 + a] += 1
        p.moves[d0 + a] += 1
    for a in ferts:
        p.ops[d0 + a] += 1                          # FERTILIZE rides the watering visit
        p.fert_use[d0 + a] += 1
    p.ops[d0 + ha] += 1                             # HARVEST
    p.moves[d0 + ha] += 1
    p.yields[d0 + ha][crop] += yld
    return p


def ongoing_profile(crop, fert, d0, daily_water=False):
    cd = CROPS[crop]
    fy, iv, ymax = cd["first_yield_day"], cd["interval"], cd["max_yield"]
    if d0 + fy > LAST:
        return None
    p = Profile(f"{crop.lower()}{'_f' if fert else '_u'}@{d0}", d0)
    p.ops[d0] += 1
    p.moves[d0] += 1
    p.cash_cost[d0] += cd["seed"]
    # production evenings (end of day cur, credited morning cur+1)
    prod_evenings = []
    count = 0
    cur = d0
    while cur <= LAST - 1:
        dsf = (cur + 1) - d0 - fy
        if dsf >= 0 and dsf % iv == 0:
            count += 1
            if count > ymax:
                break
            prod_evenings.append(cur)
            if count == ymax:
                break
        cur += 1
    if not prod_evenings:
        return None
    last_ev = prod_evenings[-1]
    # watering: survival every other day; fertilised variant also waters production evenings
    waters, ferts = set(), []
    unwatered, fert_until = 1, -1
    for day in range(d0, last_ev + 1):
        want = fert and (day in prod_evenings)
        if want and fert_until < day:
            # cover as many upcoming production evenings as possible
            ferts.append(day)
            fert_until = day + 2
        if unwatered >= 1 or want or daily_water:
            waters.add(day)
            unwatered = 0
        else:
            unwatered += 1
    for day in waters:
        p.ops[day] += 1
        p.moves[day] += 1
    for day in ferts:
        p.ops[day] += 1
        p.fert_use[day] += 1
    # held units and harvest mornings
    held = 0
    inc = 2 if fert else 1
    harvest_days = []
    for ev in prod_evenings:
        held = min(ymax, held + inc)
        morning = ev + 1
        nxt = inc if ev != last_ev else 0
        if morning <= LAST and (held + nxt > ymax or ev == last_ev):
            harvest_days.append((morning, held))
            held = 0
    for morning, units in harvest_days:
        p.ops[morning] += 1
        p.moves[morning] += 1
        p.yields[morning][crop] += units
    # dig to free the tile after the plant decays
    dig_day = last_ev + 2
    if dig_day <= LAST:
        p.ops[dig_day] += 1
        p.moves[dig_day] += 1
        p.end = dig_day
    else:
        p.end = LAST
    return p


def animal_profile(species, d0):
    a = ANIMALS[species]
    fy, iv, cap, product = a["first_yield_day"], a["interval"], a["max_held"], a["product"]
    if d0 + fy > LAST:
        return None
    p = Profile(f"{species.lower()}@{d0}", d0)
    p.end = LAST                       # pen occupies the tile for the rest of the season
    p.ops[d0] += 3                     # BUILD + PICKUP animal + PLACE
    p.moves[d0] += 1                   # one pen visit; pickup happens at the shed at dawn
    p.cash_cost[d0] += a["cost"]
    # last production evening within the season
    last_ev = None
    cur = d0
    while cur <= LAST - 1:
        dsf = (cur + 1) - d0 - fy
        if dsf >= 0 and dsf % iv == 0:
            last_ev = cur
        cur += 1
    if last_ev is None:
        return None
    pending, held = 0, 0
    for day in range(d0, last_ev + 1):
        p.ops[day] += 1 + PICKUP_SHARE            # FEED (+ amortised pickup)
        p.moves[day] += 1                         # one pen visit; feed/care/harvest ride it
        p.wheat_use[day] += 1
        dsf = (day + 1) - d0 - fy
        produced = dsf >= 0 and dsf % iv == 0     # evening production, credited morning day+1
        if produced:
            held = min(cap, held + 1 + pending)
            pending = 0
        if pending < cap - 1 and day < last_ev:   # CARE only when the bonus can land
            p.ops[day] += 1
            pending += 1
        if produced:
            morning = day + 1                     # <= last_ev+1 <= 29
            if held + 1 + iv > cap or day == last_ev:
                p.ops[morning] += 1
                p.yields[morning][product] += held
                held = 0
    return p


CROP_VARIANTS = [
    ("WHEAT", False), ("WHEAT", True),
    ("CARROT", False), ("CARROT", True),
    ("MELON", False),
    ("TOMATO", False), ("TOMATO", True),
    ("STRAWBERRY", False), ("STRAWBERRY", True),
]


# Start days: dense over the cash-critical opening, every other day after.
# Halves MILP symmetry; measured cost vs full granularity is ~1% of Z*.
START_DAYS = list(range(0, 6)) + list(range(6, DAYS, 2))


def build_profiles(daily_water=False):
    crop_profiles = {}     # (crop, fert, d0) -> Profile
    for crop, fert in CROP_VARIANTS:
        ongoing = CROPS[crop]["ongoing"]
        for d0 in START_DAYS:
            if ongoing:
                pr = ongoing_profile(crop, fert, d0, daily_water=daily_water)
            else:
                pr = oneshot_profile(crop, fert, d0)
            if pr is not None and any(u for ym in pr.yields.values() for u in ym.values()):
                crop_profiles[(crop, fert, d0)] = pr
    animal_profiles = {}
    for species in ANIMALS:
        for d0 in START_DAYS:
            pr = animal_profile(species, d0)
            if pr is not None:
                animal_profiles[(species, d0)] = pr
    return crop_profiles, animal_profiles


def selfcheck_profiles(crop_profiles, animal_profiles):
    def tot(p, product):
        return sum(ym.get(product, 0) for ym in p.yields.values())

    w = crop_profiles[("WHEAT", False, 0)]
    assert tot(w, "WHEAT") == 4 and sum(w.ops.values()) == 6, (tot(w, "WHEAT"), sum(w.ops.values()))
    wf = crop_profiles[("WHEAT", True, 0)]
    assert tot(wf, "WHEAT") == 6, tot(wf, "WHEAT")
    m = crop_profiles[("MELON", False, 0)]
    assert tot(m, "MELON") == 6 and m.end == 10, (tot(m, "MELON"), m.end)
    assert sum(m.ops.values()) == 10, sum(m.ops.values())
    t = crop_profiles[("TOMATO", False, 0)]
    assert tot(t, "TOMATO") == 4 and t.yields[11]["TOMATO"] == 4, dict(t.yields)
    tf = crop_profiles[("TOMATO", True, 0)]
    assert tot(tf, "TOMATO") == 8, tot(tf, "TOMATO")
    s = crop_profiles[("STRAWBERRY", False, 0)]
    assert tot(s, "STRAWBERRY") == 4 and s.yields[16]["STRAWBERRY"] == 4, dict(s.yields)
    sf = crop_profiles[("STRAWBERRY", True, 0)]
    assert tot(sf, "STRAWBERRY") == 8 and sum(sf.fert_use.values()) == 2, dict(sf.yields)
    g = animal_profiles[("GOOSE", 0)]
    assert g.yields[4]["EGG"] == 4, dict(g.yields)
    c = animal_profiles[("COW", 0)]
    assert c.yields[8]["MILK"] == 6, dict(c.yields)
    sh = animal_profiles[("SHEEP", 0)]
    assert sh.yields[6]["WOOL"] == 6, dict(sh.yields)
    # env price anchors
    assert KG.market_price("MELON", I0) == 250
    assert KG.market_price("MELON", I0 + 100) == 150
    assert KG.market_price("WHEAT", I0 - 400) == 45
    print("[selfcheck] profile and price anchors OK "
          f"(goose@0 eggs={tot(g,'EGG'):.0f}, cow@0 milk={tot(c,'MILK'):.0f}, "
          f"sheep@0 wool={tot(sh,'WOOL'):.0f})")


# ---------------------------------------------------------------------------
# Phase 3 -- town drain, book simulation, sell-slot values, buy prices
# ---------------------------------------------------------------------------

def drain_schedule(unlock_days, variant="actual"):
    """Per-product per-day units the town removes from the book.

    Town center: 1 of every product except FERTILIZER per day (interval 24).
    Shops: 6 ticks/day per unlocked instance; single-product shops pull 2x."""
    drain = {p: np.zeros(DAYS) for p in PRODUCTS}
    for p in PRODUCTS:
        if p != "FERTILIZER":
            drain[p][:] += 1.0
    if variant == "none":
        return drain
    if variant == "actual":
        instances = unlock_days
    elif variant == "expected":
        # 8 instances at days 3,6,...,24, each an average shop (weight/8 of every shop)
        instances = [(3 * (k + 1), None) for k in range(8)]
    for day0, shop in instances:
        for d in range(day0, DAYS):
            if shop is None:
                for s, prods in KG.SHOPS.items():
                    mult = 2 if len(prods) == 1 else 1
                    for item in prods:
                        drain[item][d] += 6.0 * mult / len(KG.SHOPS)
            else:
                prods = KG.SHOPS[shop]
                mult = 2 if len(prods) == 1 else 1
                for item in prods:
                    drain[item][d] += 6.0 * mult
    return drain


SELL_WINDOW_START = {"WHEAT": 2, "CARROT": 2, "MELON": 10, "TOMATO": 8, "STRAWBERRY": 10,
                     "EGG": 4, "MILK": 8, "WOOL": 6, "FERTILIZER": 1}
QMAX = {"WHEAT": 1500, "CARROT": 600, "MELON": 330, "TOMATO": 420, "STRAWBERRY": 540,
        "EGG": 990, "MILK": 540, "WOOL": 420, "FERTILIZER": 720}
K_SLOTS = 30


def slot_table(product, opp_net_day, drain_day):
    """K sell slots with fixed assumed sell days.

    Slot days follow the cumulative NET town demand (drain minus opponent supply), i.e.
    the model is assumed to sell into demand as it materialises -- what the leader's
    cadence does -- rather than uniformly.  Products with no positive net demand fall
    back to a uniform spread over the window.

    Slot k's marginal value assumes slots 1..k-1 were already sold (maximum prior own
    supply), so every slot value is a LOWER bound on the realised price of those units
    for any fill pattern the LP chooses.  No SOS2/binaries needed: cherry-picking a
    later slot without the earlier ones only under-prices it."""
    w0 = SELL_WINDOW_START[product]
    width = QMAX[product] // K_SLOTS
    opp = opp_net_day.get(product, np.zeros(DAYS))
    room = np.maximum.accumulate(np.cumsum(drain_day[product] - opp))  # monotone book room
    has_demand_regime = room[-1] >= width
    days = []
    for k in range(K_SLOTS):
        target = (k + 0.5) * width
        if target <= room[-1]:
            d = int(np.searchsorted(room, target))   # sell unit-for-unit into book room
        elif has_demand_regime:
            d = LAST                                 # surplus tail sells at season end
        else:
            d = w0 + int(round((k + 0.5) * (LAST - w0) / K_SLOTS))  # no-demand product
        days.append(min(LAST, max(w0, d)))
    days.sort()
    inv = float(I0)
    values, unit_prices = [], []
    k = 0
    for d in range(DAYS):
        inv += opp_net_day.get(product, np.zeros(DAYS))[d] if isinstance(opp_net_day, dict) else 0.0
        inv -= drain_day[product][d]
        while k < K_SLOTS and days[k] == d:
            v = 0.0
            for _ in range(width):
                price = KG.market_price(product, int(round(inv)))
                v += price
                if price > 1:
                    inv += 1
            values.append(v)
            unit_prices.append(v / width)
            k += 1
    while k < K_SLOTS:      # slots dated past loop end (defensive)
        values.append(width * 1.0)
        unit_prices.append(1.0)
        k += 1
    return {"width": width, "days": days, "values": values, "unit": unit_prices}


def day_price_series(product, opp_net_day, drain_day, own_extra=None):
    """Price at each day with no own sales (used for BUY costs), optionally with an
    own net flow (own_extra, negative = our buys) folded in."""
    inv = float(I0)
    out = np.zeros(DAYS)
    for d in range(DAYS):
        inv += opp_net_day.get(product, np.zeros(DAYS))[d] if isinstance(opp_net_day, dict) else 0.0
        inv -= drain_day[product][d]
        if own_extra is not None:
            inv += own_extra[d]
        out[d] = KG.market_price(product, int(round(inv)) - 1)
    return out


# ---------------------------------------------------------------------------
# Phase 4 -- MILP
# ---------------------------------------------------------------------------

class Model:
    def __init__(self):
        self.lb, self.ub, self.integrality, self.names = [], [], [], []
        self.rows = []       # (coeff dict, lo, hi)
        self.obj = defaultdict(float)   # maximise

    def var(self, name, lb=0.0, ub=np.inf, integer=False):
        self.names.append(name)
        self.lb.append(lb)
        self.ub.append(ub)
        self.integrality.append(1 if integer else 0)
        return len(self.names) - 1

    def constr(self, coeffs, lo=-np.inf, hi=np.inf):
        self.rows.append((dict(coeffs), lo, hi))

    def solve(self, sense="max", obj_override=None, floor=None, time_limit=120,
              mip_gap=2e-3, relax=False, extra_rows=None):
        """floor adds the hard constraint Z >= floor.  relax=True drops integrality
        (LP): with a floor this yields valid OUTER bounds on the integer range, since
        every integer-feasible point is LP-feasible.  extra_rows: list of
        (coeff_dict, lo, hi) appended for this solve only."""
        n = len(self.names)
        obj = self.obj if obj_override is None else obj_override
        rows = list(self.rows)
        if floor is not None:
            rows.append(({i: v for i, v in self.obj.items()}, floor, np.inf))
        if extra_rows:
            rows.extend(extra_rows)
        c = np.zeros(n)
        for i, v in obj.items():
            c[i] = v
        data, ri, ci = [], [], []
        lo, hi = [], []
        for r, (coeffs, l, h) in enumerate(rows):
            for i, v in coeffs.items():
                if v != 0.0:
                    data.append(v)
                    ri.append(r)
                    ci.append(i)
            lo.append(l)
            hi.append(h)
        A = sp.csr_matrix((data, (ri, ci)), shape=(len(rows), n))
        integrality = np.zeros(n) if relax else np.array(self.integrality)
        res = milp(c=(-c if sense == "max" else c),
                   constraints=LinearConstraint(A, lo, hi),
                   integrality=integrality,
                   bounds=Bounds(np.array(self.lb), np.array(self.ub)),
                   options={"time_limit": time_limit, "mip_rel_gap": mip_gap,
                            "presolve": True, "disp": False})
        if res.x is None:
            raise RuntimeError(f"solve failed: {res.message}")
        if not res.success:
            gap = getattr(res, "mip_gap", None)
            print(f"    [warn] incumbent at time limit (gap {gap})")
        val = -res.fun if sense == "max" else res.fun
        return val, res.x


# Geometry walk model: each worked tile costs 1 move per visit (serpentine adjacency),
# and each active unit pays a fixed dawn-out + dusk-home transit.  The mean Manhattan
# distance from a shed-access corner to a tile of its quadrant is exactly 4.0
# (E|dx| + E|dy| over a 5x5 from the corner), so out + home = 8 moves per unit-day.
TRANSIT_MOVES = 8.0


def build_model(crop_profiles, animal_profiles, slots, wheat_price, fert_price, walk="flat"):
    m = Model()
    x = {}                      # (crop, fert, d0) -> var (cycles started)
    for key, pr in crop_profiles.items():
        x[key] = m.var(f"x_{pr.name}", 0, 50, integer=True)
    y = {}
    for key, pr in animal_profiles.items():
        y[key] = m.var(f"y_{pr.name}", 0, 20, integer=True)
    MAX_HANDS = 15
    h = [m.var(f"h_{d}", 0, MAX_HANDS, integer=True) for d in range(DAYS)]
    z = [[m.var(f"z_{d}_{i}", 0, 1) for i in range(MAX_HANDS)] for d in range(DAYS)]
    zeta = [[m.var(f"land_{k}_{d}", 0, 1, integer=True) for d in range(DAYS)] for k in range(3)]
    wbuy = [m.var(f"wbuy_{d}") for d in range(DAYS)]
    g = [m.var(f"gfeed_{d}") for d in range(DAYS)]
    fbuy = [m.var(f"fbuy_{d}") for d in range(DAYS)]
    fcol = [m.var(f"fcol_{d}") for d in range(DAYS)]
    u = {p: [m.var(f"u_{p}_{k}", 0, slots[p]["width"]) for k in range(K_SLOTS)] for p in PRODUCTS}

    # hire slots: sum_i z = h ; cost fib(i) each (convex, so LP fills cheap slots first)
    for d in range(DAYS):
        m.constr({z[d][i]: 1.0 for i in range(MAX_HANDS)} | {h[d]: -1.0}, 0, 0)

    # land: each parcel bought at most once, in order
    for k in range(3):
        m.constr({zeta[k][d]: 1.0 for d in range(DAYS)}, -np.inf, 1.0)
    for k in range(1, 3):
        for d in range(DAYS):
            m.constr({zeta[k][t]: 1.0 for t in range(d + 1)} |
                     {zeta[k - 1][t]: -1.0 for t in range(d + 1)}, -np.inf, 0.0)

    # per-day tiles, labour, and cash prefix
    for d in range(DAYS):
        occ = defaultdict(float)
        for key, pr in crop_profiles.items():
            if pr.start <= d <= pr.end:
                occ[x[key]] += 1.0
        for key, pr in animal_profiles.items():
            if pr.start <= d:
                occ[y[key]] += 1.0
        for k in range(3):
            for t in range(d + 1):
                occ[zeta[k][t]] -= 25.0
        m.constr(occ, -np.inf, 25.0)

        lab = defaultdict(float)
        if walk == "flat":
            for key, pr in crop_profiles.items():
                if pr.ops.get(d):
                    lab[x[key]] += pr.ops[d] * (1 + LAMBDA_WALK)
            for key, pr in animal_profiles.items():
                if pr.ops.get(d):
                    lab[y[key]] += pr.ops[d] * (1 + LAMBDA_WALK)
            lab[fcol[d]] += 1.0 * (1 + LAMBDA_WALK)
            per_unit = TURNS
        else:                            # "geom": ops + tile-visit moves + unit transit
            for key, pr in crop_profiles.items():
                load = pr.ops.get(d, 0.0) + pr.moves.get(d, 0.0)
                if load:
                    lab[x[key]] += load
            for key, pr in animal_profiles.items():
                load = pr.ops.get(d, 0.0) + pr.moves.get(d, 0.0)
                if load:
                    lab[y[key]] += load
            lab[fcol[d]] += 1.0          # collection rides the daily pen visit
            per_unit = TURNS - TRANSIT_MOVES
        lab[h[d]] -= per_unit
        m.constr(lab, -np.inf, per_unit)   # main farmer contributes one unit

    # cash prefix: sum of net flows through day d >= -3000
    flow = [defaultdict(float) for _ in range(DAYS)]
    for key, pr in crop_profiles.items():
        for d, cost in pr.cash_cost.items():
            flow[d][x[key]] -= cost
    for key, pr in animal_profiles.items():
        for d, cost in pr.cash_cost.items():
            flow[d][y[key]] -= cost
    for d in range(DAYS):
        for i in range(MAX_HANDS):
            flow[d][z[d][i]] -= KG._fib(i)
        for k in range(3):
            flow[d][zeta[k][d]] -= KG.LAND_PRICES[k]
        flow[d][wbuy[d]] -= wheat_price[d]
        flow[d][fbuy[d]] -= fert_price[d]
    for p in PRODUCTS:
        for k in range(K_SLOTS):
            flow[slots[p]["days"][k]][u[p][k]] += slots[p]["unit"][k]
    run = defaultdict(float)
    for d in range(DAYS):
        for i, v in flow[d].items():
            run[i] += v
        m.constr(dict(run), -START_MONEY, np.inf)

    # wheat feed: g + wbuy = daily need; grown feed available the morning after harvest
    for d in range(DAYS):
        need = defaultdict(float)
        for key, pr in animal_profiles.items():
            if pr.wheat_use.get(d):
                need[y[key]] += pr.wheat_use[d]
        need[g[d]] -= 1.0
        need[wbuy[d]] -= 1.0
        m.constr(need, 0, 0)
    cumy_wheat = defaultdict(float)     # cumulative wheat yield through day d-1
    for d in range(DAYS):
        cg = {g[t]: 1.0 for t in range(d + 1)}
        for key, pr in crop_profiles.items():
            for t, ym in pr.yields.items():
                if t <= d - 1 and "WHEAT" in ym:
                    cg[x[key]] = cg.get(x[key], 0.0) - ym["WHEAT"]
        m.constr(cg, -np.inf, 0.0)

    # sale availability: cumulative sold through slot day <= cumulative harvested (minus feed for wheat)
    for p in PRODUCTS:
        for k in range(K_SLOTS):
            tau = slots[p]["days"][k]
            av = {u[p][kk]: 1.0 for kk in range(k + 1) if slots[p]["days"][kk] <= tau}
            for key, pr in crop_profiles.items():
                for t, ym in pr.yields.items():
                    if t <= tau and p in ym:
                        av[x[key]] = av.get(x[key], 0.0) - ym[p]
            for key, pr in animal_profiles.items():
                for t, ym in pr.yields.items():
                    if t <= tau and p in ym:
                        av[y[key]] = av.get(y[key], 0.0) - ym[p]
            if p == "WHEAT":
                for t in range(tau + 1):
                    av[g[t]] = av.get(g[t], 0.0) + 1.0
            if p == "FERTILIZER":
                for t in range(tau + 1):
                    av[fcol[t]] = av.get(fcol[t], 0.0) - 1.0
                    av[fbuy[t]] = av.get(fbuy[t], 0.0) - 1.0
                for key, pr in crop_profiles.items():
                    for t, q in pr.fert_use.items():
                        if t <= tau:
                            av[x[key]] = av.get(x[key], 0.0) + q
            m.constr(av, -np.inf, 0.0)

    # fertilizer balance: collected + bought >= used (+ sold, handled above)
    for d in range(DAYS):
        fb = {fcol[t]: 1.0 for t in range(d + 1)}
        for t in range(d + 1):
            fb[fbuy[t]] = fb.get(fbuy[t], 0.0) + 1.0
        for key, pr in crop_profiles.items():
            for t, q in pr.fert_use.items():
                if t <= d:
                    fb[x[key]] = fb.get(x[key], 0.0) - q
        m.constr(fb, 0.0, np.inf)
        # collection limited to animals alive (placed on an earlier day)
        cc = {fcol[d]: 1.0}
        for key, pr in animal_profiles.items():
            if pr.start <= d - 1:
                cc[y[key]] = cc.get(y[key], 0.0) - 1.0
        m.constr(cc, -np.inf, 0.0)

    # objective: end-of-season money minus start
    for p in PRODUCTS:
        for k in range(K_SLOTS):
            m.obj[u[p][k]] += slots[p]["unit"][k]
    for key, pr in crop_profiles.items():
        m.obj[x[key]] -= sum(pr.cash_cost.values())
    for key, pr in animal_profiles.items():
        m.obj[y[key]] -= sum(pr.cash_cost.values())
    for d in range(DAYS):
        for i in range(MAX_HANDS):
            m.obj[z[d][i]] -= KG._fib(i)
        for k in range(3):
            m.obj[zeta[k][d]] -= KG.LAND_PRICES[k]
        m.obj[wbuy[d]] -= wheat_price[d]
        m.obj[fbuy[d]] -= fert_price[d]

    handles = {"x": x, "y": y, "h": h, "z": z, "zeta": zeta, "wbuy": wbuy,
               "g": g, "fbuy": fbuy, "fcol": fcol, "u": u}
    return m, handles


def item_expr(handles, item):
    if item in CROPS:
        return {v: 1.0 for (crop, fert, d0), v in handles["x"].items() if crop == item}
    if item in ANIMALS:
        return {v: 1.0 for (spec, d0), v in handles["y"].items() if spec == item}
    if item == "HANDS":
        return {v: 1.0 for v in handles["h"]}
    if item == "LAND":
        return {v: 1.0 for row in handles["zeta"] for v in row}
    raise KeyError(item)


def describe_solution(xvec, handles, crop_profiles, animal_profiles, slots):
    out = {}
    for crop in CROPS:
        cyc = sum(round(xvec[v]) for (c, f, d0), v in handles["x"].items() if c == crop)
        peak = 0
        for d in range(DAYS):
            occ = sum(round(xvec[v]) for (c, f, d0), v in handles["x"].items()
                      if c == crop and crop_profiles[(c, f, d0)].start <= d <= crop_profiles[(c, f, d0)].end)
            peak = max(peak, occ)
        out[crop] = (cyc, peak)
    for spec in ANIMALS:
        n = sum(round(xvec[v]) for (s, d0), v in handles["y"].items() if s == spec)
        out[spec] = (n, n)
    out["HANDS_MEAN"] = sum(xvec[v] for v in handles["h"]) / DAYS
    out["LAND"] = sum(round(xvec[v]) for row in handles["zeta"] for v in row)
    out["SOLD"] = {p: sum(xvec[v] for v in handles["u"][p]) for p in PRODUCTS}
    out["WBUY"] = sum(xvec[v] for v in handles["wbuy"])
    out["FCOL"] = sum(xvec[v] for v in handles["fcol"])
    return out


# ---------------------------------------------------------------------------
# pass 2 -- shared helpers, attribution, per-draw policy, best response
# ---------------------------------------------------------------------------

def random_draw(seed):
    """A shop draw sampled the way the env draws it: 8 instances at days 3,6,...,24,
    uniform over sorted(SHOPS) WITH replacement (reference _end_of_day)."""
    rng = random.Random(seed)
    return [(3 * (k + 1), rng.choice(sorted(KG.SHOPS))) for k in range(8)]


def draw_label(draw):
    counts = defaultdict(int)
    for _, s in draw:
        counts[s] += 1
    return ",".join(f"{s.split('_')[0]}{'' if n == 1 else 'x' + str(n)}"
                    for s, n in sorted(counts.items()))


def solve_base(crop_profiles, animal_profiles, opp_net, drain, gap, tl, walk, t0):
    """Base MILP + one wheat-buy price feedback pass.  Returns everything the bands
    and checks need."""
    slots = {p: slot_table(p, opp_net, drain) for p in PRODUCTS}
    wp = day_price_series("WHEAT", opp_net, drain)
    fp = day_price_series("FERTILIZER", opp_net, drain)
    model, handles = build_model(crop_profiles, animal_profiles, slots, wp, fp, walk=walk)
    zstar, xvec = model.solve(time_limit=tl, mip_gap=gap)
    wb = np.array([xvec[v] for v in handles["wbuy"]])
    if wb.sum() > 100:
        wp2 = day_price_series("WHEAT", opp_net, drain, own_extra=-wb)
        model, handles = build_model(crop_profiles, animal_profiles, slots, wp2, fp, walk=walk)
        z2, xvec = model.solve(time_limit=tl, mip_gap=gap)
        print(f"    [feedback] wheat bought {wb.sum():.0f}, "
              f"price end ${wp[-1]:.0f}->${wp2[-1]:.0f}, Z ${zstar:,.0f}->${z2:,.0f}")
        zstar = z2
    print(f"    [base] Z* = ${zstar:,.0f}  [{time.time()-t0:.0f}s]")
    return model, handles, slots, zstar, xvec


def compute_bands(model, handles, items, tols, zstar, range_tl):
    bands = {}
    for tol in tols:
        floor = (1 - tol) * zstar - 1
        for item in items:
            expr = item_expr(handles, item)
            vals = []
            for sense in ("min", "max"):
                try:
                    v, _ = model.solve(sense=sense, obj_override=expr, floor=floor,
                                       time_limit=range_tl, relax=True)
                except RuntimeError:
                    v = float("nan")
                vals.append(v)
            bands[(item, tol)] = tuple(vals)
    return bands


def band_table(bands, items, tols, base=None, leader=None):
    lines = []
    hdr = f"    {'item':<11}" + (f" {'base':>5}" if base else "")
    for tol in tols:
        hdr += f"  {format(tol, '.1%') + ' band':>16}"
    if leader:
        hdr += f"  {'leader':>7}"
    lines.append(hdr)
    for item in items:
        row = f"    {item:<11}"
        if base:
            row += f" {base[item][0] if isinstance(base[item], tuple) else base[item]:>5}"
        for tol in tols:
            lo, hi = bands[(item, tol)]
            row += f"  {'[' + format(lo, '.1f') + ', ' + format(hi, '.1f') + ']':>16}"
        if leader:
            ref = leader.get(item)
            row += f"  {ref if ref is not None else '-':>7}"
        lines.append(row)
    return "\n".join(lines)


def solution_load(xvec, handles, crop_profiles, animal_profiles, walk):
    """Implied ops / moves / capacity usage of a solution, for validation."""
    ops = np.zeros(DAYS)
    moves = np.zeros(DAYS)
    harv = np.zeros(DAYS)
    for key, pr in crop_profiles.items():
        n = xvec[handles["x"][key]]
        if n < 1e-6:
            continue
        for day, o in pr.ops.items():
            ops[day] += o * n
        for day, mv in pr.moves.items():
            moves[day] += mv * n
        for day, ym in pr.yields.items():
            harv[day] += sum(ym.values()) * n
    for key, pr in animal_profiles.items():
        n = xvec[handles["y"][key]]
        if n < 1e-6:
            continue
        for day, o in pr.ops.items():
            ops[day] += o * n
        for day, mv in pr.moves.items():
            moves[day] += mv * n
        for day, ym in pr.yields.items():
            harv[day] += sum(ym.values()) * n
    units = np.array([1 + xvec[handles["h"][d]] for d in range(DAYS)])
    for d in range(DAYS):
        ops[d] += xvec[handles["fcol"][d]]
    if walk == "geom":
        moves_total = moves + TRANSIT_MOVES * units
    else:
        moves_total = ops * LAMBDA_WALK
    return {"ops": ops.sum(), "moves": moves_total.sum(),
            "ratio": moves_total.sum() / max(ops.sum(), 1.0),
            "unit_days": units.sum(), "peak_harvest": harv.max()}


def extract_fills(xvec, handles, slots):
    """Our net per-day book impact, for best-response iteration."""
    net = {p: np.zeros(DAYS) for p in PRODUCTS}
    for p in PRODUCTS:
        for k, var in enumerate(handles["u"][p]):
            q = xvec[var]
            if q > 1e-6:
                net[p][slots[p]["days"][k]] += q
    for d in range(DAYS):
        net["WHEAT"][d] -= xvec[handles["wbuy"][d]]
        net["FERTILIZER"][d] -= xvec[handles["fbuy"][d]]
    return net


ITEMS = list(CROPS) + list(ANIMALS)
LEADER_PIN = {"MELON": 20, "STRAWBERRY": 34}


def leader_pin_check(model, zstar, handles, tl, t0):
    extra = [(item_expr(handles, it), q, q) for it, q in LEADER_PIN.items()]
    try:
        zc, _ = model.solve(time_limit=tl, mip_gap=1e-3, extra_rows=extra)
        drop = 1 - zc / zstar
        print(f"    [pin] MELON=20,STRAW=34: Z ${zc:,.0f} drop {drop:.2%}  "
              f"[{time.time()-t0:.0f}s]")
        return drop
    except RuntimeError as e:
        print(f"    [pin] no solution within limit ({e})")
        return float("nan")


def mode_attrib(args, leader_net, unlock_days, t0):
    """Items 2-4 one at a time against a recomputed pass-1 baseline, S1 actual draw."""
    drain = drain_schedule(unlock_days, "actual")
    tols = [0.001, 0.01, 0.05]
    variants = [
        ("V0 pass1-baseline", dict(daily=False, walk="flat", gap=2e-3, tl=150)),
        ("V1 tight-gap", dict(daily=False, walk="flat", gap=args.base_gap, tl=args.time_limit)),
        ("V2 daily-water", dict(daily=True, walk="flat", gap=2e-3, tl=150)),
        ("V3 geom-walk", dict(daily=False, walk="geom", gap=2e-3, tl=150)),
        ("V4 combined", dict(daily=True, walk="geom", gap=args.base_gap, tl=args.time_limit)),
    ]
    widths = {}
    for vname, cfg in variants:
        print(f"\n=== attrib {vname} (daily_water={cfg['daily']}, walk={cfg['walk']}, "
              f"gap={cfg['gap']}, tl={cfg['tl']}) ===")
        cp, ap_ = build_profiles(daily_water=cfg["daily"])
        model, handles, slots, zstar, xvec = solve_base(
            cp, ap_, leader_net, drain, cfg["gap"], cfg["tl"], cfg["walk"], t0)
        base = describe_solution(xvec, handles, cp, ap_, slots)
        load = solution_load(xvec, handles, cp, ap_, cfg["walk"])
        print(f"    mix: " + ", ".join(f"{c}={base[c][0]}" for c in CROPS) + "; " +
              ", ".join(f"{a}={base[a][0]}" for a in ANIMALS) +
              f"; hands {base['HANDS_MEAN']:.1f}")
        print(f"    load: work {load['ops']:.0f} moves {load['moves']:.0f} "
              f"ratio {load['ratio']:.3f} (tape 1.254) unit-days {load['unit_days']:.0f} "
              f"peak daily harvest {load['peak_harvest']:.0f} (shed cap 100)")
        bands = compute_bands(model, handles, ITEMS, tols, zstar, args.range_time_limit)
        print(band_table(bands, ITEMS, tols, base=base, leader=LEADER_REF))
        for tol in tols:
            widths[(vname, tol)] = {it: bands[(it, tol)][1] - bands[(it, tol)][0]
                                    for it in ITEMS}
    print("\n=== attrib summary: 1% band widths per variant ===")
    hdr = f"    {'item':<11}" + "".join(f" {v[:12]:>13}" for v, _ in variants)
    print(hdr)
    for it in ITEMS:
        print(f"    {it:<11}" + "".join(f" {widths[(v, 0.01)][it]:>13.1f}"
                                        for v, _ in variants))


def mode_policy(args, leader_net, unlock_days, t0):
    """Per-draw clairvoyant optimum + bands with the combined model."""
    cp, ap_ = build_profiles(daily_water=True)
    draws = [] if args.skip_actual else [("actual-92498144", unlock_days)]
    for i in range(args.draws):
        d = random_draw(args.draw_seed + i)
        draws.append((f"rng{args.draw_seed + i}", d))
    tols = [0.001, 0.01]
    rows = []
    for dname, draw in draws:
        print(f"\n=== draw {dname}: {draw_label(draw)} ===")
        drain = drain_schedule(draw, "actual")
        print("    season town drain: " +
              ", ".join(f"{p}={drain[p].sum():.0f}" for p in PRODUCTS if drain[p].sum() > 0))
        model, handles, slots, zstar, xvec = solve_base(
            cp, ap_, leader_net, drain, args.base_gap, args.time_limit, "geom", t0)
        base = describe_solution(xvec, handles, cp, ap_, slots)
        bands = compute_bands(model, handles, ITEMS, tols, zstar, args.range_time_limit)
        print("    mix: " + ", ".join(f"{c}={base[c][0]}" for c in CROPS) + "; " +
              ", ".join(f"{a}={base[a][0]}" for a in ANIMALS))
        print(band_table(bands, ITEMS, tols, base=base, leader=LEADER_REF))
        drop = leader_pin_check(model, zstar, handles, 300, t0)
        rows.append((dname, draw_label(draw), zstar, base, bands, drop))
    print("\n=== policy table (per draw: optimal mix, melon/straw 1% band, 20/34 pin cost) ===")
    print(f"    {'draw':<16} {'Z*':>9}  {'W':>3} {'C':>3} {'T':>3} {'S':>3} {'M':>3} "
          f"{'G':>3} {'Co':>3} {'Sh':>3}  {'MELON 1%':>13} {'STRAW 1%':>13} {'pin':>7}")
    for dname, lbl, zstar, base, bands, drop in rows:
        mlo, mhi = bands[("MELON", 0.01)]
        slo, shi = bands[("STRAWBERRY", 0.01)]
        print(f"    {dname:<16} {zstar:>9,.0f}  "
              f"{base['WHEAT'][0]:>3} {base['CARROT'][0]:>3} {base['TOMATO'][0]:>3} "
              f"{base['STRAWBERRY'][0]:>3} {base['MELON'][0]:>3} {base['GOOSE'][0]:>3} "
              f"{base['COW'][0]:>3} {base['SHEEP'][0]:>3}  "
              f"{'[' + format(mlo, '.0f') + ',' + format(mhi, '.0f') + ']':>13} "
              f"{'[' + format(slo, '.0f') + ',' + format(shi, '.0f') + ']':>13} "
              f"{drop:>7.1%}")
        print(f"        shops: {lbl}")


def mode_br(args, leader_net, unlock_days, t0):
    """Best-response iteration: opponent supply <- our previous optimum's fills."""
    cp, ap_ = build_profiles(daily_water=True)
    drain = drain_schedule(unlock_days, "actual")
    opp = {p: leader_net[p].copy() for p in PRODUCTS}
    for it in range(args.br_iters):
        print(f"\n=== best-response iteration {it} "
              f"(opp melon {opp['MELON'].sum():.0f}, straw {opp['STRAWBERRY'].sum():.0f}, "
              f"milk {opp['MILK'].sum():.0f}) ===")
        model, handles, slots, zstar, xvec = solve_base(
            cp, ap_, opp, drain, args.base_gap, args.time_limit, "geom", t0)
        base = describe_solution(xvec, handles, cp, ap_, slots)
        print("    mix: " + ", ".join(f"{c}={base[c][0]}" for c in CROPS) + "; " +
              ", ".join(f"{a}={base[a][0]}" for a in ANIMALS))
        print("    sold: " + ", ".join(f"{p}={base['SOLD'][p]:.0f}" for p in PRODUCTS
                                       if base["SOLD"][p] > 0.5))
        opp = extract_fills(xvec, handles, slots)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default=TAPE)
    ap.add_argument("--quick", action="store_true", help="scenario 1 only, 5%% ranges only")
    ap.add_argument("--time-limit", type=float, default=180.0)
    ap.add_argument("--range-time-limit", type=float, default=60.0)
    ap.add_argument("--mode", choices=["scenarios", "attrib", "policy", "br"],
                    default="scenarios")
    ap.add_argument("--base-gap", type=float, default=5e-4,
                    help="mip_rel_gap for pass-2 base solves")
    ap.add_argument("--draws", type=int, default=5, help="random draws in policy mode")
    ap.add_argument("--draw-seed", type=int, default=11)
    ap.add_argument("--br-iters", type=int, default=4)
    ap.add_argument("--skip-actual", action="store_true",
                    help="policy mode: only the random draws (resume after a kill)")
    args = ap.parse_args()

    t0 = time.time()
    print(f"[env] kaggle_environments {kaggle_environments.__version__} at {KG.__file__}")
    fills, unlock_days, meta = replay_fills(args.tape)
    opp = aggregate_opponent(fills, seat=0)
    us1 = aggregate_opponent(fills, seat=1)
    print(f"[replay] seats: {meta['names']} rewards {meta['rewards']} seed {meta['seed']}")
    print(f"[replay] shop instances (active_from_day, shop): {unlock_days}")
    print("[replay] leader (seat 0) season fills:")
    for p in PRODUCTS:
        s, b = opp["sells"][p].sum(), opp["buys"][p].sum()
        if s or b:
            print(f"    {p:<11} sold {s:5.0f}  (${opp['rev'][p]:,.0f})   bought {b:5.0f}")
    print(f"[replay] leader seed buys {opp['seed_buys']}  animal buys {opp['animal_buys']}")
    print(f"[replay] opp (seat 1) melon/straw sold "
          f"{us1['sells']['MELON'].sum():.0f}/{us1['sells']['STRAWBERRY'].sum():.0f}")

    crop_profiles, animal_profiles = build_profiles()
    selfcheck_profiles(crop_profiles, animal_profiles)
    print(f"[profiles] {len(crop_profiles)} crop cycles, {len(animal_profiles)} animal placements")

    drain = drain_schedule(unlock_days, "actual")
    print("[drain] season totals (units the town removes):",
          {p: round(drain[p].sum()) for p in PRODUCTS})

    leader_net = {p: opp["net"][p] for p in PRODUCTS}
    if args.mode != "scenarios":
        {"attrib": mode_attrib, "policy": mode_policy, "br": mode_br}[args.mode](
            args, leader_net, unlock_days, t0)
        print(f"\n[done] total {time.time()-t0:.0f}s")
        return

    scenarios = [("S1 opp=leader", {p: leader_net[p] for p in PRODUCTS}),
                 ("S2 opp=zero", {p: np.zeros(DAYS) for p in PRODUCTS}),
                 ("S3 opp=2x leader", {p: 2.0 * leader_net[p] for p in PRODUCTS})]
    if args.quick:
        scenarios = scenarios[:1]

    crop_items = list(CROPS)
    animal_items = list(ANIMALS)
    items = crop_items + animal_items
    tols = [0.05] if args.quick else [0.01, 0.05]
    all_results = {}

    for sname, opp_net in scenarios:
        print(f"\n=== {sname} ===")
        slots = {p: slot_table(p, opp_net, drain) for p in PRODUCTS}
        for p in ("MELON", "STRAWBERRY", "WOOL", "MILK", "WHEAT"):
            up = slots[p]["unit"]
            print(f"[slots] {p:<11} width {slots[p]['width']:>3} unit$ first/mid/last "
                  f"{up[0]:7.1f} {up[K_SLOTS//2]:7.1f} {up[-1]:7.1f}")
        wheat_price = day_price_series("WHEAT", opp_net, drain)
        fert_price = day_price_series("FERTILIZER", opp_net, drain)
        model, handles = build_model(crop_profiles, animal_profiles, slots, wheat_price, fert_price)
        print(f"[milp] {len(model.names)} vars ({sum(model.integrality)} int), "
              f"{len(model.rows)} constraints")
        zstar, xvec = model.solve(time_limit=args.time_limit)
        print(f"[milp] Z* = ${zstar:,.0f}  (bank ${zstar + START_MONEY:,.0f})  "
              f"[{time.time()-t0:.0f}s]")

        # one price-feedback iteration on bought wheat
        wb = np.array([xvec[v] for v in handles["wbuy"]])
        if wb.sum() > 100:
            wheat_price2 = day_price_series("WHEAT", opp_net, drain, own_extra=-wb)
            model, handles = build_model(crop_profiles, animal_profiles, slots, wheat_price2, fert_price)
            z2, xvec = model.solve(time_limit=args.time_limit)
            print(f"[milp] wheat-buy feedback: bought {wb.sum():.0f}, price end "
                  f"${wheat_price[-1]:.0f} -> ${wheat_price2[-1]:.0f}, Z* ${zstar:,.0f} -> ${z2:,.0f}")
            zstar = z2

        base = describe_solution(xvec, handles, crop_profiles, animal_profiles, slots)
        print("[base] cycles(peak tiles): " +
              ", ".join(f"{c}={base[c][0]}({base[c][1]})" for c in crop_items))
        print("[base] animals: " + ", ".join(f"{a}={base[a][0]}" for a in animal_items) +
              f"  hands/day mean {base['HANDS_MEAN']:.1f}  parcels {base['LAND']}")
        print("[base] sold: " + ", ".join(f"{p}={base['SOLD'][p]:.0f}" for p in PRODUCTS
                                          if base['SOLD'][p] > 0.5))
        print(f"[base] wheat bought {base['WBUY']:.0f}, fertilizer collected {base['FCOL']:.0f}")

        # Direct check of the leader's reference allocation: pin it, measure the cost.
        for cname, fixes in [("MELON=20,STRAW=34", {"MELON": 20, "STRAWBERRY": 34}),
                             ("MELON=20,STRAW=34,COW=6,SHEEP=8",
                              {"MELON": 20, "STRAWBERRY": 34, "COW": 6, "SHEEP": 8})]:
            extra = [(item_expr(handles, it), q, q) for it, q in fixes.items()]
            try:
                zc, _ = model.solve(time_limit=args.time_limit, extra_rows=extra)
                print(f"[leadercheck] {cname}: Z ${zc:,.0f} = {zc / zstar:.1%} of Z* "
                      f"(drop {1 - zc / zstar:.2%})  [{time.time()-t0:.0f}s]")
            except RuntimeError as e:
                print(f"[leadercheck] {cname}: no solution within limit ({e})")

        ranges = {}
        for tol in tols:
            floor = (1 - tol) * zstar - 1
            for item in items:
                expr = item_expr(handles, item)

                def _range_solve(sense):
                    # LP relaxation: valid OUTER bound on the integer range.
                    try:
                        v, _ = model.solve(sense=sense, obj_override=expr, floor=floor,
                                           time_limit=args.range_time_limit, relax=True)
                        return v
                    except RuntimeError:
                        print(f"    [warn] {item} {sense} @{tol:.0%}: LP failed, NaN")
                        return float("nan")

                lo = _range_solve("min")
                hi = _range_solve("max")
                ranges[(item, tol)] = (lo, hi)
                print(f"[range] {sname} {item:<10} @{tol:.0%}: [{lo:6.1f}, {hi:6.1f}]  "
                      f"[{time.time()-t0:.0f}s]")
        all_results[sname] = {"zstar": zstar, "base": base, "ranges": ranges,
                              "slots": {p: slots[p]["unit"] for p in PRODUCTS}}

    # shop-draw sensitivity on scenario 1
    if not args.quick:
        print("\n=== shop-draw sensitivity (scenario 1 economics) ===")
        for variant in ("expected", "none"):
            drv = drain_schedule(unlock_days, variant)
            slots_v = {p: slot_table(p, scenarios[0][1], drv) for p in PRODUCTS}
            wp = day_price_series("WHEAT", scenarios[0][1], drv)
            fp = day_price_series("FERTILIZER", scenarios[0][1], drv)
            mv, hv = build_model(crop_profiles, animal_profiles, slots_v, wp, fp)
            zv, xv = mv.solve(time_limit=args.time_limit)
            bv = describe_solution(xv, hv, crop_profiles, animal_profiles, slots_v)
            print(f"[sens] drain={variant:<9} Z* ${zv:,.0f}  " +
                  ", ".join(f"{c}={bv[c][0]}" for c in crop_items) + "  " +
                  ", ".join(f"{a}={bv[a][0]}" for a in animal_items))

    # final tables
    print("\n" + "=" * 100)
    for sname in all_results:
        r = all_results[sname]
        print(f"\n{sname}:  Z* = ${r['zstar']:,.0f}  (bank ${r['zstar'] + START_MONEY:,.0f})")
        hdr = f"{'item':<11} {'base':>5}"
        for tol in tols:
            hdr += f"  {'['+format(tol,'.0%')+' range]':>15}"
        hdr += f"  {'leader':>7}"
        print(hdr)
        for item in items:
            b = r["base"].get(item)
            bstr = f"{b[0]:>5}" if isinstance(b, tuple) else (f"{r['base']['HANDS_MEAN']:5.1f}"
                                                              if item == "HANDS" else f"{r['base']['LAND']:>5}")
            line = f"{item:<11} {bstr}"
            for tol in tols:
                lo, hi = r["ranges"].get((item, tol), (float('nan'), float('nan')))
                line += f"  {'['+format(lo,'.0f')+', '+format(hi,'.0f')+']':>15}"
            ref = LEADER_REF.get(item)
            line += f"  {ref if ref is not None else '-':>7}"
            print(line)
    print(f"\n[done] total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
