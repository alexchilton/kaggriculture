"""Per-product: units SOLD, revenue, and the hour of day each sale landed on.

The grid's `crop_STRAWBERRY` row counts TILES ALIVE, and its `SELL` row counts every product
together. Neither says whether a crop we kept alive turned into money, and a strawberry is an
ongoing crop -- a tile alive on d8 pays out over the following weeks, if the routing reaches it and
the produce gets to the shed.

Two things this answers that no grid row can:

  units and revenue PER PRODUCT   did the extra living tiles convert
  the HOUR the sale landed        the market is a ladder and the first seller takes the top rung

The hour matters as much as the count. Measured on d6, seed 11: the same 12 wool sold in two lots
of six either way, but the tape's first lot fetched `[218,217,215,214,212,209]` at h04 and ours
fetched exactly his SECOND rung, `[199..194]`, at h11. Same units, $143 less, and that $143 is what
left d7 unable to fund its seed order.

Never counts offers. `kagg/analysis/fills.py` wraps `_commit_unit`, which is the only function that
moves shed and money together, so every row here is a fill that happened.

    python -u scripts/what_reached_the_market.py --arm straw --days 30
    python -u scripts/what_reached_the_market.py --arm straw --days 30 --baseline HEAD~1
"""
import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
MELON_SEASON = "data/seed_scripts/kawashigi/92498144.json"
STRAWBERRY_SEASON = "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"


def season(arm="straw", seed=11, weeds=0.0, days=30, pin_shops=True):
    """`(sold, harvested, money)` for seat 0 -- sold is `{product: (units, revenue, [hours])}`."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.analysis.fills import record_fills
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if arm == "straw" else MELON_SEASON))
    economy = B.env_config(replay)
    shops = B.recorded_shops(replay) if pin_shops else None

    env = make("kaggriculture", configuration=dict(economy, seed=seed, weedSpawnChance=weeds),
               debug=True)
    env.reset(2)
    agent, opp = SA.make_agent(sched, 0), B.tape_policy(replay, TEAM, 1)
    harvested = collections.Counter()
    with record_fills(env) as f:
        for t in range(days * TPD):
            o0, o1 = env.state[0].observation, env.state[1].observation
            if shops is not None:
                env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o1["farms"][1].get("hands") or [])
            for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                if a and a[0] == "HARVEST":
                    harvested["HARVEST"] += 1
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if env.done:
                break
        rows = collections.defaultdict(lambda: [0, 0.0, []])
        for d, h, op, item, price in f.at_turn(0):
            if op == "SELL":
                r = rows[item]
                r[0] += 1
                r[1] += price
                r[2].append(h)
    money = env.state[0].observation["farms"][0]["money"]
    return {k: tuple(v) for k, v in rows.items()}, harvested, money


def show(label, sold, money):
    print(f"\n=== {label}   final bank ${round(money):,}")
    print(f"{'product':>14} {'units':>7} {'revenue':>11} {'$/unit':>8} {'median hour':>12} "
          f"{'sold before h8':>15}")
    tot_u = tot_r = 0
    for p, (u, rev, hours) in sorted(sold.items(), key=lambda kv: -kv[1][1]):
        hs = sorted(hours)
        med = hs[len(hs) // 2] if hs else 0
        early = sum(1 for h in hs if h < 8)
        tot_u += u
        tot_r += rev
        print(f"{p:>14} {u:>7} {round(rev):>11,} {rev / max(1, u):>8.1f} {med:>12} "
              f"{f'{early} ({100 * early / max(1, u):.0f}%)':>15}")
    print(f"{'TOTAL':>14} {tot_u:>7} {round(tot_r):>11,}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="straw")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    a = ap.parse_args()
    sold, harv, money = season(a.arm, a.seed, a.weeds, a.days)
    show(f"arm {a.arm!r} seed {a.seed} weeds {a.weeds} days {a.days}", sold, money)
    print(f"\nHARVEST ops: {harv['HARVEST']}")


if __name__ == "__main__":
    main()
