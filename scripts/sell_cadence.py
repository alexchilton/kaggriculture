"""Do we DUMP or DRIP, and does the tape? Per-unit fills tagged with the turn they committed on.

The arithmetic says spacing a season's sales out is worth +77% on MILK and +42% on STRAWBERRY,
because both have `linear` above-curves with a 1.60 target and a T of 122 and 100 -- they reach the
$1 floor about fifty units above I0, so a big sell puts most of its units on the floor.

**That arithmetic is not evidence about this agent.** It says what the curve pays for a given
cadence; it says nothing about the cadence we actually have. If goods trickle into the shed and the
standing offer clears them a few at a time, we already drip and there is nothing to win. This repo
has been wrong in exactly this direction before -- "eggs are always good" was $17,199 against $6,281
straight off the curve and inverted once demand was in it -- and there is a recorded null pointing
the same way: setting `RESERVATION_SLIP` to 0 to stop the offer walking the price came back
byte-identical, with the note that the bunching was never the sell cap, it was the goods reaching
the shed at h13 instead of h4.

So this measures the thing itself. `_commit_unit` is the only place a unit changes hands, and it is
called once per unit, so wrapping it with the current turn gives the exact size of every burst.
`kagg/analysis/fills.py` explains why any proxy for this is wrong; this is that module plus a turn.

Reported per product and per seat:

  - **bursts**: how many turns sold anything, and the size distribution of those bursts.
  - **realised**: what we actually banked for those units.
  - **ceiling**: what the same units would have fetched one-per-turn from the same opening book,
    with the town draining in between. The gap is the money cadence is worth, and it is an upper
    bound -- one unit a turn needs the goods to be in the shed that early, which is the real
    constraint and is not modelled here.

    python -u scripts/sell_cadence.py --seeds 4
"""

import argparse
import collections
import importlib
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

import breakdown as B
from kaggle_environments import make

from reference.kaggriculture import (MARKET_I0, SHOPS, TOWN_CENTER_PRODUCTS, market_price)

TPD = 24
OURS = "data/seed_scripts/top_guys/90976060/schedule.json"
RIVAL = "data/seed_scripts/top_guys/90976060.json"


def season_drain(product, unlocked):
    """Units the town removes over a whole season, for this shop draw. Mirrors `_town_consume`."""
    total = 0
    for name in unlocked:
        products = SHOPS.get(name, [])
        if product in products:
            total += (2 if len(products) == 1 else 1) * (719 // 4)
    if product in TOWN_CENTER_PRODUCTS:
        total += 719 // 24
    return total


def dripped(units, drain, chunks):
    """What `units` fetch spread over `chunks` turns, with `drain` spread across the same span."""
    inv = MARKET_I0
    total = 0.0
    per, carry, per_drain = units / chunks, 0.0, drain / chunks
    for _ in range(chunks):
        n = int(per + carry)
        carry = per + carry - n
        for _ in range(n):
            p = market_price(PRODUCT, inv)
            total += p
            if p > 1:
                inv += 1
        inv = max(MARKET_I0 - 2000, inv - per_drain)
    return total


def play(seed, module, schedule, replay, days=30):
    """One game, returning `(rows, unlocked)` where a row is `(turn, seat, op, item, price)`."""
    import kaggle_environments.envs.kaggriculture.kaggriculture as kg

    raw = json.loads(pathlib.Path(schedule).read_text())
    sched = {int(k): {a: b for a, b in v.items() if a not in B.TAPE_ONLY}
             for k, v in raw.items()}
    B.schedule_agent = SA = importlib.import_module(module)
    CREW = importlib.import_module("kagg.search.crew")
    was, CREW.STRICT_FEASIBILITY = CREW.STRICT_FEASIBILITY, False

    rows = []
    turn = {"t": 0}
    seats = {}
    orig_commit, orig_market = kg._commit_unit, kg._process_market

    def commit(op, item, price, farm, private, market, *a, **kw):
        ok = orig_commit(op, item, price, farm, private, market, *a, **kw)
        if ok:
            seat = seats.get(id(farm))
            if seat is not None:
                rows.append((turn["t"], seat, op, item, price))
        return ok

    def process_market(state, env_):
        seats.clear()
        seats.update({id(f): i for i, f in enumerate(state[0].observation.farms)})
        return orig_market(state, env_)

    kg._commit_unit, kg._process_market = commit, process_market
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay), seed=seed, weedSpawnChance=0.0),
                   debug=False)
        env.reset(2)
        agent = SA.make_agent(sched, 0, router=True)
        team = ((json.loads(pathlib.Path(replay).read_text()).get("info") or {})
                .get("TeamNames") or ["", ""])[1]
        opp = B.tape_policy(replay, team, 1)
        for t in range(min(719, TPD * days)):
            turn["t"] = t
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if env.state[0].status == "DONE":
                break
        unlocked = list((env.state[0].observation.get("town") or {}).get("unlocked_shops") or [])
        return rows, unlocked
    finally:
        kg._commit_unit, kg._process_market = orig_commit, orig_market
        CREW.STRICT_FEASIBILITY = was


def main():
    global PRODUCT
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--first-seed", type=int, default=11)
    ap.add_argument("--module", default="kagg.search.schedule_agent")
    ap.add_argument("--schedule", default=OURS)
    ap.add_argument("--replay", default=RIVAL)
    args = ap.parse_args()

    agg = collections.defaultdict(lambda: collections.defaultdict(list))
    drains = collections.defaultdict(list)
    for seed in range(args.first_seed, args.first_seed + args.seeds):
        rows, unlocked = play(seed, args.module, args.schedule, args.replay)
        per_turn = collections.Counter()
        revenue = collections.defaultdict(float)
        for t, seat, op, item, price in rows:
            if op != "SELL":
                continue
            per_turn[(seat, item, t)] += 1
            revenue[(seat, item)] += price
        for (seat, item, _t), n in per_turn.items():
            agg[(seat, item)]["bursts"].append(n)
        for k, v in revenue.items():
            agg[k]["revenue"].append(v)
        for p in set(i for (_s, i, _t) in per_turn):
            drains[p].append(season_drain(p, unlocked))

    print(f"seeds {args.first_seed}..{args.first_seed + args.seeds - 1}   "
          f"seat 0 = ours, seat 1 = the tape\n")
    print(f"  {'seat':>4} {'product':<11} {'units':>6} {'turns':>6} {'per turn':>9} {'biggest':>8} "
          f"{'realised':>10} {'$/unit':>7} {'1-per-turn':>11} {'left on table':>14}")
    for (seat, item) in sorted(agg, key=lambda k: (k[0], k[1])):
        bursts = agg[(seat, item)]["bursts"]
        rev = sum(agg[(seat, item)]["revenue"])
        units = sum(bursts)
        if units < 10:
            continue
        PRODUCT = item
        n_seeds = max(1, args.seeds)
        drain = statistics.mean(drains.get(item, [0])) if drains.get(item) else 0
        ceiling = dripped(units / n_seeds, drain, 719) * n_seeds
        print(f"  {seat:>4} {item:<11} {units:>6} {len(bursts):>6} "
              f"{units/len(bursts):>9.1f} {max(bursts):>8} {rev:>10,.0f} {rev/units:>7.0f} "
              f"{ceiling:>11,.0f} {ceiling - rev:>+14,.0f}")


if __name__ == "__main__":
    main()
