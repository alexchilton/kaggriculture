"""Where the money goes, one day at a time, for the opening only.

Alex's instruction, and it is the right correction to what I was doing: stop running whole seasons and
sweeping genes, walk the sequence a step at a time and find where it changes.

The measurement that made this the question (`data/logs/diverge_by_day_147k.log` and the money curve
pulled off the replay):

    day        0     1     2     3     4     5     6     7  |    10     11     12
    theirs   $10  $141  $217  $789  $522  $642 $1595  $915  | $3304  $6885 $14165
    ours    $327  $293  $244  $224  $232  $391  $400  $346  |  $243    $11     $4

Both seats spend almost the whole stake on day 0 -- theirs ends on $10, so day 0 is not the fault.
Our gross by day 6 is $1,585 against their *bank* of $1,595, so revenue is not the fault either. The
first land parcel costs $1,000 (`farm.LAND_PRICES`), they buy it on day 7 and we never clear $1,000 at
all, so the melon and strawberry tiles it unlocks are planted six days late and miss their day-10
first yield (`FIRST_YIELD_DAY` melon 10, strawberry 10).

So the question is narrow: across days 0-7, what does each dollar of revenue get spent on, and which
line item stops the balance ever reaching $1,000? This prints that ledger, per day, and nothing else.

    PYTHONPATH=. python3 -u scripts/cash_ledger.py 2>&1 | tee data/logs/cash_ledger.log
"""

import argparse

import numpy as np

from kagg.search import executor as X
from kagg.search import library, plan as P, replay_plan as RP, rollout
from kagg.sim.farm import HIRE_COST, LAND_PRICES
from kagg.sim.game import Actions, Game
from kagg.sim.market import ANIMAL_COST

SEAT = 0


def ledger(mine, opp, schedule, days, rng):
    """Per-day cash in and cash out, split by what asked for it."""
    game = Game(1, rng=rng, unlock_schedule=schedule)
    actions = Actions(1)
    rows, open_money = [], None
    acc = None

    for step in range(days * 24):
        day, hour = step // 24, step % 24
        if hour == 0:
            open_money = float(game.farms[SEAT].money[0])
            acc = dict(sold=0.0, seeds=0.0, animals=0.0, wheat=0.0, hires=0.0, land=0.0,
                       units_sold=0, seeds_bought=0)

        for player, pl in ((0, mine), (1, opp)):
            view = rollout.build_view(game, player, day, hour)
            dec = X.decide(view, pl)
            if player == SEAT:
                # What the decision *asks* for, priced at the book the turn opened on. The realised
                # amount can be lower -- the market may not fill -- so these are upper bounds, which
                # is what a "what is it trying to spend on" question wants.
                fill = np.minimum(dec.sell[0], view.shed[0])
                acc["sold"] += float((fill * view.prices[0]).sum())
                acc["units_sold"] += int(fill.sum())
                acc["seeds"] += float((dec.buy_seed[0] * P.SEED_COST).sum())
                acc["seeds_bought"] += int(dec.buy_seed[0].sum())
                acc["animals"] += float((dec.buy_animal[0] * ANIMAL_COST).sum())
                acc["wheat"] += float(dec.buy_product[0, X.WHEAT_ITEM]) * 25.0
                if bool(dec.hire[0]):
                    n = int(game.farms[SEAT].hires_today[0])
                    acc["hires"] += float(HIRE_COST[min(n, len(HIRE_COST) - 1)])
                if bool(dec.buy_land[0]):
                    slot = int(game.farms[SEAT].n_land[0])
                    if slot < len(LAND_PRICES):
                        acc["land"] = float(LAND_PRICES[slot])
            rollout._write(actions, player, dec)
        if game.step(actions):
            break

        if hour == 23:
            close = float(game.farms[SEAT].money[0])
            rows.append(dict(day=day, open=open_money, close=close, **acc))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--seat", type=int, default=0)
    ap.add_argument("--days", type=int, default=8)
    a = ap.parse_args()

    layout = RP.layout_from_replay(a.episode, seat=a.seat)
    mine = P.decode(RP.genome_from_layout(layout)[None])
    opp = P.decode(library.opposition()).take([0])
    rows = ledger(mine, opp, rollout.sample_unlock_schedule(np.random.default_rng(0)),
                  a.days, np.random.default_rng(0))

    print(f"first land parcel costs ${LAND_PRICES[0]:,.0f}; "
          f"seed_reserve = ${float(mine.seed_reserve[0]):,.0f}\n")
    print(f"{'day':>3} {'open':>8} {'sold':>9} {'units':>6} | {'seeds':>8} {'n':>4} "
          f"{'animals':>8} {'wheat':>7} {'hires':>7} {'land':>6} | {'close':>8}")
    print("=" * 96)
    for r in rows:
        print(f"{r['day']:>3} {r['open']:>8,.0f} {r['sold']:>9,.0f} {r['units_sold']:>6} | "
              f"{r['seeds']:>8,.0f} {r['seeds_bought']:>4} {r['animals']:>8,.0f} "
              f"{r['wheat']:>7,.0f} {r['hires']:>7,.0f} {r['land']:>6,.0f} | {r['close']:>8,.0f}")
    print("=" * 96)
    tot = {k: sum(r[k] for r in rows) for k in ("sold", "seeds", "animals", "wheat", "hires")}
    print(f"over {len(rows)} days: earned ${tot['sold']:,.0f}   "
          f"seeds ${tot['seeds']:,.0f}  animals ${tot['animals']:,.0f}  "
          f"wheat ${tot['wheat']:,.0f}  hires ${tot['hires']:,.0f}")
    print(f"their bank at day {len(rows) - 1}: "
          f"${_their_money(a.episode, a.seat, len(rows) - 1):,.0f}")


def _their_money(path, seat, day):
    import json
    ep = json.load(open(path))
    last = 0.0
    for t, step in enumerate(ep["steps"]):
        if t // 24 > day:
            break
        obs = step[seat].get("observation") or step[0].get("observation")
        farms = (obs or {}).get("farms")
        if farms and seat < len(farms):
            last = float(farms[seat]["money"])
    return last


if __name__ == "__main__":
    raise SystemExit(main())
