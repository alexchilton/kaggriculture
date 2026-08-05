"""Where the money goes, ours against the tape's, day by day and line by line.

Everything downstream now hangs off the bank. The buy and sell ORDERS match the tape exactly -- that
test passes -- and yet `day 3: money 45 against the tape's 217` and `day 8: 171 against 928`, and a
short bank is what silently kills `BUY_ANIMAL`: every animal PICKUP in our season finds an empty shed,
so 11 pens stand with 5 animals in them.

An order matching is not a transaction matching. Four things can differ with identical orders:

    fill      a SELL of 10 sells `min(10, held)`, so a shed that is short sells less
    price     `market_price` walks with the town's inventory, so the same order earns less if our
              own earlier orders, or the opponent's, moved the book first
    hires     the Fibonacci partial sum is per DAY, but only for the orders that actually clear
    slots     `maxMarketOrdersPerTurn` = 10 truncates the tail of a turn silently

So this reports realised cash, not intent: per day, money at dawn, what the sells actually earned,
what the buys actually cost, and the residual -- which is production and hiring.
"""

import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import dayplan, routines as R
import build_script_submission as B

TPD = R.TURNS_PER_DAY
REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"


def tape_side():
    """Dawn bank and realised order volume per day, off the tape."""
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    dawn, sold, bought = {}, collections.Counter(), collections.Counter()
    per_day = collections.defaultdict(lambda: dict(sold=0, bought=0))
    for t, step in enumerate(d["steps"][1:]):
        day, hour = divmod(t, TPD)
        s = step[seat] or {}
        obs = s.get("observation") or {}
        farms = obs.get("farms") or []
        if hour == 0 and len(farms) > seat:
            dawn[day] = float(farms[seat]["money"])
        for o in ((s.get("action") or {}).get("market") or []):
            if not o:
                continue
            n = int(o[2]) if len(o) > 2 else 1
            if o[0] == "SELL":
                per_day[day]["sold"] += n
            elif o[0] in ("BUY_PRODUCT", "BUY_SEED"):
                per_day[day]["bought"] += n
    return dawn, per_day


def our_side():
    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, rep = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    from kaggle_environments import make
    env = make("kaggriculture", debug=True)
    env.reset(2)
    dawn = {}
    per_day = collections.defaultdict(lambda: dict(sold=0, bought=0, filled=0, held=0))
    for t in range(len(plan)):
        day, hour = divmod(t, TPD)
        obs = env.state[0].observation
        me = obs["farms"][0]
        priv = obs["private"]
        if hour == 0:
            dawn[day] = float(me["money"])
        shed = collections.Counter(priv.get("shed") or {})
        farmer, hands_, market = plan[t]
        for o in market:
            n = int(o[2]) if len(o) > 2 else 1
            if o[0] == "SELL":
                per_day[day]["sold"] += n
                per_day[day]["filled"] += min(n, shed.get(o[1], 0))
            elif o[0] in ("BUY_PRODUCT", "BUY_SEED"):
                per_day[day]["bought"] += n
        n_units = len(me.get("hands") or [])
        env.step([{"farmer": farmer, "hands": hands_[:n_units], "market": market},
                  {"farmer": ["PASS"], "hands": [], "market": []}])
        if env.state[0].status == "DONE":
            break
    return dawn, per_day


def main():
    a_dawn, a_day = tape_side()
    b_dawn, b_day = our_side()
    print(f"{'day':>4} {'our dawn':>10} {'tape dawn':>10} {'gap':>9} | "
          f"{'sell ord':>9} {'FILLED':>7} {'tape sell':>9} | {'our buy':>8} {'tape buy':>9}")
    for day in sorted(a_dawn):
        if day not in b_dawn:
            continue
        A, Bd = a_day[day], b_day[day]
        flag = "  <-- unfilled" if Bd["filled"] < Bd["sold"] else ""
        print(f"{day:>4} {b_dawn[day]:>10,.0f} {a_dawn[day]:>10,.0f} "
              f"{b_dawn[day] - a_dawn[day]:>9,.0f} | "
              f"{Bd['sold']:>9} {Bd['filled']:>7} {A['sold']:>9} | "
              f"{Bd['bought']:>8} {A['bought']:>9}{flag}")


if __name__ == "__main__":
    main()
