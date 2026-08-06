"""Every trade the farm actually made, at the price it actually got, ours beside the tape's.

The board is now level. Across thirty days of seed 11 the pens match exactly (30/30 days), planted
matches 130 to 131, harvested 322 to 338, animal-days run at 97% and we lose 9 tiles to weeds against
the tape's 34 -- our field is in fact BIGGER, 1155 crop-tile-days against 1097. And the bank is at 64%.

Producing 95% as much and banking 64% is not a farming difference, it is a trading difference, and it
cannot be read off the order list: an order is a request. `SELL WHEAT 20` walks the shed one unit at a
time and stops when the shed empties or the price collapses; `BUY_PRODUCT WHEAT 40` stops when the
money runs out. The tape orders 1,131 wheat sales a season and cannot possibly have made them.

So this measures the only thing that is not a request. `_commit_unit` is the env's own single-unit
commit -- one item, one price, returns False when it cannot fill -- and wrapping it records exactly
what changed hands and for how much, for both seats, with no inference at all.

Prints per day: units sold, revenue, mean realised price, units bought and what they cost, by item;
then the season totals per item, which is where the difference should show as either volume or price.
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import schedule_agent
import agent_ladder as L

KG = importlib.import_module("kaggle_environments.envs.kaggriculture.kaggriculture")

#: Filled by the wrapper below: `(seat, day, op, item, price)` for every unit that actually changed
#: hands. Cleared per run.
TRADES = []
_CTX = {"farms": None, "day": 0}


def _install():
    """Wrap the env's own per-unit commit so realised trades are recorded rather than inferred."""
    if getattr(KG, "_ledger_installed", False):
        return
    orig_commit, orig_market = KG._commit_unit, KG._process_market

    def commit(op, item, price, farm, private, market):
        ok = orig_commit(op, item, price, farm, private, market)
        if ok and _CTX["farms"] is not None:
            seat = 0 if farm is _CTX["farms"][0] else 1
            TRADES.append((seat, _CTX["day"], op, item, float(price)))
        return ok

    def process(state, env):
        # `farms` is the live list the commits mutate, so identity is a reliable seat test.
        _CTX["farms"] = state[0].observation.farms
        _CTX["day"] = int(state[0].observation.get("day", 0))
        return orig_market(state, env)

    KG._commit_unit, KG._process_market = commit, process
    KG._ledger_installed = True


def run(seed, make_us=None, tape=None, theirs=None):
    _install()
    del TRADES[:]
    env = L._env(seed, 0.0)
    us = make_us() if make_us else None
    for t in range(719):
        obs = env.state[0].observation
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        n0 = len(obs["farms"][0].get("hands") or [])
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:n0], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    return list(TRADES), float(env.state[0].observation["farms"][0]["money"])


def summarise(trades, seat):
    """`(per_day, per_item)` of realised units and dollars for one seat."""
    day = collections.defaultdict(collections.Counter)
    item = collections.defaultdict(collections.Counter)
    for s, d, op, it, price in trades:
        if s != seat:
            continue
        kind = "sold" if op == "SELL" else "bought"
        day[d][kind + "_n"] += 1
        day[d][kind + "_$"] += price
        item[(kind, it)]["n"] += 1
        item[(kind, it)]["$"] += price
    return day, item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", nargs="?", type=int, default=11)
    args = ap.parse_args()
    mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_tr, tape_money = run(args.seed, tape=mine, theirs=theirs)
    our_tr, our_money = run(args.seed,
                            make_us=lambda: schedule_agent.make_agent(sched, 0, router=True),
                            theirs=theirs)
    od, oi = summarise(our_tr, 0)
    td, ti = summarise(tape_tr, 0)

    print(f"seed {args.seed}   tape ${tape_money:,.0f}   ours ${our_money:,.0f} "
          f"({100 * our_money / tape_money:.0f}%)\n")
    print(f"{'':>4} {'UNITS SOLD':>13} {'SALE REVENUE':>19} {'MEAN PRICE':>15} "
          f"{'UNITS BOUGHT':>15} {'PURCHASE SPEND':>19}")
    print(f"{'day':>4} {'ours':>6}{'tape':>7} {'ours':>9}{'tape':>10} {'ours':>7}{'tape':>8} "
          f"{'ours':>7}{'tape':>8} {'ours':>9}{'tape':>10}")
    for d in sorted(set(od) | set(td)):
        o, t = od[d], td[d]
        op_ = o["sold_$"] / max(1, o["sold_n"])
        tp = t["sold_$"] / max(1, t["sold_n"])
        print(f"{d:>4} {o['sold_n']:>6}{t['sold_n']:>7} {o['sold_$']:>9,.0f}{t['sold_$']:>10,.0f} "
              f"{op_:>7.0f}{tp:>8.0f} {o['bought_n']:>7}{t['bought_n']:>8} "
              f"{o['bought_$']:>9,.0f}{t['bought_$']:>10,.0f}")

    print(f"\n  {'':<12}{'UNITS SOLD':>18}{'REVENUE':>22}{'MEAN PRICE':>18}")
    print(f"  {'item':<12}{'ours':>8}{'tape':>10}{'ours':>11}{'tape':>11}{'ours':>9}{'tape':>9}")
    items = sorted({it for _k, it in list(oi) + list(ti)})
    for it in items:
        o, t = oi[("sold", it)], ti[("sold", it)]
        print(f"  {it:<12}{o['n']:>8}{t['n']:>10}{o['$']:>11,.0f}{t['$']:>11,.0f}"
              f"{o['$'] / max(1, o['n']):>9.0f}{t['$'] / max(1, t['n']):>9.0f}")
    so, st = sum(v["$"] for k, v in oi.items() if k[0] == "sold"), \
        sum(v["$"] for k, v in ti.items() if k[0] == "sold")
    bo, bt = sum(v["$"] for k, v in oi.items() if k[0] == "bought"), \
        sum(v["$"] for k, v in ti.items() if k[0] == "bought")
    print(f"\n  gross sale revenue    ours ${so:>10,.0f}   tape ${st:>10,.0f}   "
          f"{100 * so / max(1, st):>5.0f}%")
    print(f"  gross purchase spend  ours ${bo:>10,.0f}   tape ${bt:>10,.0f}")
    print(f"  trading margin        ours ${so - bo:>10,.0f}   tape ${st - bt:>10,.0f}")
    print(f"\n  {'':<12}{'UNITS BOUGHT':>18}{'SPEND':>22}")
    for it in items:
        o, t = oi[("bought", it)], ti[("bought", it)]
        if not (o["n"] or t["n"]):
            continue
        print(f"  {it:<12}{o['n']:>8}{t['n']:>10}{o['$']:>11,.0f}{t['$']:>11,.0f}")


if __name__ == "__main__":
    main()
