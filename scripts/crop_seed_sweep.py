"""Sweep crop reallocation across seeds and a field of opponents, and record each seed's town drain.

**Rewritten 2026-08-15 after a 5,376-game run returned nothing.** Both halves had been written
against assumed shapes rather than checked ones, and both failed silently while exiting 0:

- the drain table read `observation["shops"]`, which does not exist -- shops live at
  `observation["town"]["unlocked_shops"]`, a list of names appended as they unlock. Every seed
  reported a drain of 0 for every product.
- `pool.evaluate` looks its opponents up as `OPPONENTS[name]`, so a spec must be a KEY in that
  dict. Passing the frozen build's file path raised `KeyError` on all 16 configs.

Both are now read from the environment rather than assumed, and `main()` smoke-tests a single
config end to end before the grid is allowed to start.

## What it measures, and what it cannot

The ladder is Elo, so the primary figure is WIN RATE against a field. Money is reported second and
is the noisier number: seed variance here is ~15%, far larger than any effect being swept.
`PoolResult.win_rate` counts wins only, so draws are reported separately rather than folded in.

The cross-seed part is why the tape cannot be used: `breakdown.py` replays recorded ACTIONS, which
are valid only on the board they were recorded against.

## Why the drain column is the point

The 2026-08-15 balance change makes TOMATO viable in ~50% of games, CARROT ~26%, EGG ~22% --
deliberately not universally. So a single best allocation may not exist, and the question is whether
the optimum tracks the shop draw. Recording drain per seed is what makes that answerable instead of
assumed.
"""
import collections
import itertools
import json
import pathlib
import shutil
import sys
import time

sys.path.insert(0, ".")

import reference.kaggriculture as KG

REPO = pathlib.Path(__file__).resolve().parent.parent
WORK = REPO / "data" / "sweep"
FROZEN = WORK / "frozen_shipped.py"

SEEDS = list(range(1, 17))
WORKERS = 14

#: `(src, dst, tiles)` triples for `schedule_agent.CROP_TILE_SHIFTS`, one per config.
#: Coarse and exploratory -- the point is to see whether anything jumps, not to tune.
CONFIGS = {
    "baseline":          (),
    "melon->wheat 6":    (("MELON", "WHEAT", 6),),
    "melon->wheat 12":   (("MELON", "WHEAT", 12),),
    "melon->straw 6":    (("MELON", "STRAWBERRY", 6),),
    "straw->carrot 8":   (("STRAWBERRY", "CARROT", 8),),
    "straw->tomato 8":   (("STRAWBERRY", "TOMATO", 8),),
    "straw->wheat 12":   (("STRAWBERRY", "WHEAT", 12),),
    "wheat->tomato 8":   (("WHEAT", "TOMATO", 8),),
    "wheat->carrot 8":   (("WHEAT", "CARROT", 8),),
    "melon+straw->wheat": (("MELON", "WHEAT", 6), ("STRAWBERRY", "WHEAT", 8)),
}

#: Pool members, plus the frozen shipped build injected under this name. Everything here competes
#: for market prices; `starter` and `pass` are excluded because they never contest the book.
FIELD = ("mirror", "contrarian", "wheat_only", "melon_heavy", "cow_heavy", "carrot_25", "shipped")


def seed_drain(seed, sell_interval=None):
    """Units of each product the town absorbs over the season, from the shop draw alone.

    `_town_consume` removes one unit of each product a shop sells every `townShopSellInterval`
    steps, doubled when the shop sells only one product. A shop unlocked on day D drains for the
    30 - D days that remain. `KG.SHOPS[name]` is the product list.
    """
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    ticks_per_day = 24 // int(sell_interval or env.configuration.get("townShopSellInterval", 4))

    seen = collections.Counter()          # shop name -> instances already counted
    first_day = {}                        # (name, instance) -> day it appeared
    for t in range(719):
        shops = collections.Counter(env.state[0].observation["town"]["unlocked_shops"])
        for name, n in shops.items():
            while seen[name] < n:
                first_day[(name, seen[name])] = t // 24
                seen[name] += 1
        env.step([[], []])
        if env.done:
            break

    total = collections.Counter()
    for (name, _), day in first_day.items():
        products = KG.SHOPS.get(name) or []
        mult = 2 if len(products) == 1 else 1
        for p in products:
            total[p] += mult * ticks_per_day * max(0, 30 - day)
    return total


def write_candidate(label, shifts, live_routes=True, from_day=0):
    """One config as an importable agent.

    **Two things have to be switched off for a crop sweep to mean anything**, and leaving either on
    is what made the first run return four byte-identical rows:

    - `LATE_CROP_FROM_DAY` defaults to 12, but the schedule plants MELON on d0/d6/d7 and STRAWBERRY
      on d5-d12. Gated at d12 there is nothing of either left to re-crew, so every melon shift was a
      no-op by construction.
    - `SOLVED_DAYS` covers 12-29 -- every day that would water or harvest a shifted crop. A stop is
      matched on `(tile, ops)`, so changing the crop drops the stop from the route rather than
      adapting it. The config is then judged on routes built for crops it no longer grows.

    With `live_routes` the solver is off for the whole solved range and `cover.cost` runs live, so
    every config is served by routes derived from its OWN board. That is a weaker executor than the
    shipped one, and deliberately so: both arms are weakened identically, which is what makes the
    comparison about the crops.
    """
    WORK.mkdir(parents=True, exist_ok=True)
    tag = "live" if live_routes else "solved"
    path = WORK / ("cand_" + "".join(c if c.isalnum() else "_" for c in label) + f"_{tag}.py")
    unsolve = "tuple(range(12, 30))" if live_routes else "()"
    path.write_text(
        f"import sys\n"
        f"sys.path.insert(0, {str(REPO)!r})\n"
        f"import kagg.search.schedule_agent as A\n"
        f"import kagg.search.cover as C\n"
        f"import kagg.plan as PLAN\n"
        f"A.CROP_TILE_SHIFTS = {shifts!r}\n"
        f"A.LATE_CROP_FROM_DAY = {from_day}\n"
        f"C.UNSOLVE_DAYS = {unsolve}\n"
        # filter the BUILT dict: it is assembled at import with a tuple conversion that rebuilding
        # from SOLVED_DAYS would lose
        f"C.PRECOMPUTED_ROUTES = {{d: v for d, v in C.PRECOMPUTED_ROUTES.items() "
        f"if d not in C.UNSOLVE_DAYS}}\n"
        f"_S = PLAN.load({str(REPO / 'data/seed_scripts/kawashigi/schedule.json')!r})\n"
        f"_A = {{}}\n"
        f"def agent(obs, config):\n"
        f"    seat = obs['player']\n"
        f"    if seat not in _A:\n"
        f"        _A[seat] = A.make_agent(_S, me=seat)\n"
        f"    return _A[seat](obs, obs['step'])\n"
    )
    return str(path)


def main():
    from kagg.arena import pool

    WORK.mkdir(parents=True, exist_ok=True)
    (REPO / "data" / "logs").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO / "submission" / "main.py", FROZEN)
    pool.OPPONENTS["shipped"] = str(FROZEN)          # `evaluate` looks opponents up by NAME

    # ---------------------------------------------------------------- smoke test, one config only
    print("SMOKE TEST: one config, two seeds, before the grid is allowed to run", flush=True)
    probe = write_candidate("baseline", ())
    res = pool.evaluate(probe, SEEDS[:2], opponents=FIELD, workers=WORKERS)
    if not res.per_opponent or any(v is None for v in res.per_opponent.values()):
        print("  smoke test produced no per-opponent rows -- STOPPING")
        return
    print(f"  win {res.win_rate:.1%}  draw {res.draw_rate:.1%}  mean ${res.mean_money:,.0f}")
    print(f"  per-opponent {  {k: round(v[0], 3) for k, v in sorted(res.per_opponent.items())} }")
    d = seed_drain(SEEDS[0])
    if not sum(d.values()):
        print("  drain came back empty -- STOPPING")
        return
    print(f"  seed {SEEDS[0]} drain {dict(d)}\n", flush=True)

    # ---------------------------------------------------------------------------- the drain table
    print("per-seed town drain, units absorbed over the season:")
    print(f"{'seed':>5} {'TOMATO':>8} {'CARROT':>8} {'EGG':>8} {'WHEAT':>8} {'WOOL':>8} "
          f"{'MILK':>8} {'STRAW':>8} {'MELON':>8}")
    drain = {}
    for s in SEEDS:
        d = seed_drain(s)
        drain[s] = dict(d)
        print(f"{s:>5} {d['TOMATO']:>8} {d['CARROT']:>8} {d['EGG']:>8} {d['WHEAT']:>8} "
              f"{d['WOOL']:>8} {d['MILK']:>8} {d['STRAWBERRY']:>8} {d['MELON']:>8}", flush=True)
    json.dump(drain, open(REPO / "data/logs/seed_drains.json", "w"), indent=1)

    # ---------------------------------------------------------------------------------- the grid
    # The confound, measured rather than argued: the same two configs with the solver ON and OFF.
    # If the gap is large, no solved-route number in this file means anything about crops.
    print("\nCONFOUND CHECK -- baseline with the late routes solved vs live:")
    for tag, live in (("solved", False), ("live", True)):
        c = write_candidate("baseline", (), live_routes=live)
        r = pool.evaluate(c, SEEDS[:6], opponents=FIELD, workers=WORKERS)
        print(f"  routes {tag:<7} win {r.win_rate:>6.1%}  draw {r.draw_rate:>5.1%}  "
              f"mean ${r.mean_money:>9,.0f}", flush=True)

    print(f"\nLIVE ROUTES (solver off d12-d29), shifts from d0 -- so every config is routed for its "
          f"own board\n")
    print(f"{'config':<22}{'WIN':>7}{'DRAW':>7}{'mean $':>11}{'vs shipped':>11}   per-opponent")
    rows = []
    for label, shifts in CONFIGS.items():
        t0 = time.time()
        cand = write_candidate(label, shifts, live_routes=True, from_day=0)
        try:
            res = pool.evaluate(cand, SEEDS, opponents=FIELD, workers=WORKERS)
        except Exception as e:
            print(f"{label:<22}  FAILED {type(e).__name__}: {e}", flush=True)
            continue
        shipped = res.per_opponent.get("shipped", (float("nan"), float("nan")))
        per = "  ".join(f"{k[:9]}:{v[0]:.0%}" for k, v in sorted(res.per_opponent.items()))
        print(f"{label:<22}{res.win_rate:>6.1%}{res.draw_rate:>7.1%}{res.mean_money:>11,.0f}"
              f"{shipped[0]:>10.0%}   {per}   [{time.time()-t0:.0f}s]", flush=True)
        rows.append(dict(config=label, shifts=shifts, win_rate=res.win_rate,
                         draw_rate=res.draw_rate, mean_money=res.mean_money,
                         vs_shipped=shipped[0],
                         per_opponent={k: list(v) for k, v in res.per_opponent.items()}))
        json.dump(rows, open(REPO / "data/logs/crop_sweep_rows.json", "w"), indent=1)

    if rows:
        best = max(rows, key=lambda r: r["win_rate"])
        base = next((r for r in rows if r["config"] == "baseline"), None)
        print(f"\nbest by win rate: {best['config']}  {best['win_rate']:.1%}  "
              f"mean ${best['mean_money']:,.0f}")
        if base:
            print(f"baseline:         {base['config']}  {base['win_rate']:.1%}  "
                  f"mean ${base['mean_money']:,.0f}")


if __name__ == "__main__":
    main()
