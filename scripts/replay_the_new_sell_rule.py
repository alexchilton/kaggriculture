"""Run the ACTUAL shipped sell rule over real ladder replays and see what it would have banked.

`what_we_should_have_sold.py` searched a uniform scale and reported that the money is in selling
less. That is an abstraction: it says an optimum exists, not that our rule finds it. This runs
`reservation_units` itself -- the function in the bundle, with whatever flags are set right now --
against the live book at every turn of a real game, and prices the schedule it would have produced.

Method. Our own contribution to the book is known, so the path the market would have had without us
is `base[t] = inv_obs[t] - (our cumulative sales before t)`. Walking forward, the rule sees the book
we would actually have created (`base[t] + our counterfactual cumulative`), the shops open on that
turn, and the stock we still expect to sell, and returns an offer. We take the smaller of that and
what we really offered, because the rule is a cap alongside the schedule row rather than a
replacement for it, and widening an offer needs goods this replay cannot prove we held.

Read the result as a LOWER bound for two reasons: the opponent is held fixed, and withheld stock is
priced at zero rather than being carried and sold later.

    PYTHONPATH=. python3 -u scripts/replay_the_new_sell_rule.py data/ladder/losses/*.json
"""

import collections
import json
import sys

import kaggle_environments.envs.kaggriculture.kaggriculture as kg

from kagg.search import schedule_agent as SA

ME = "alex chilton"
ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON", "WHEAT", "FERTILIZER")


def load(path):
    d = json.loads(open(path).read())
    teams = (d.get("info") or {}).get("TeamNames") or []
    seat = teams.index(ME)
    rewards = d.get("rewards") or [s.get("reward") for s in d["steps"][-1]]
    inv, mine, shops = [], [], []
    for step in d["steps"]:
        obs = (step[0] or {}).get("observation") or {}
        book = (obs.get("market") or {}).get("inventory")
        if book is None:
            continue
        inv.append(dict(book))
        shops.append(list((obs.get("town") or {}).get("unlocked_shops") or []))
        c = collections.Counter()
        for o in ((step[seat] or {}).get("action") or {}).get("market", []) or []:
            if o and o[0] == "SELL":
                c[o[1]] += int(o[2])
        mine.append(c)
    return teams, seat, rewards, inv, mine, shops


def run(item, inv, mine, shops, use_rule):
    """Revenue on `item`, either as played or as the live rule would have capped it."""
    total = sum(m[item] for m in mine)
    revenue, cum, sold, withheld = 0.0, 0, 0, 0
    for t in range(len(inv)):
        want = mine[t][item]
        book = inv[t][item] - withheld
        if use_rule and want:
            allowed = SA.reservation_units(item, book, t, shops[t], max(1, total - sold))
            want = min(want, allowed)
        for _ in range(want):
            revenue += kg.market_price(item, book)
            book += 1
        sold += want
        withheld += mine[t][item] - want
    return revenue, sold


def main(paths):
    flips = kept = 0
    grand = collections.Counter()
    print(f"  HOLD_A_FLOORED_BOOK = {SA.HOLD_A_FLOORED_BOOK}\n")
    print(f"  {'game':<11}{'opponent':<20}{'ours':>9}{'theirs':>9}{'as played':>11}"
          f"{'with rule':>11}{'gain':>10}{'verdict':>16}")
    for path in paths:
        teams, seat, rewards, inv, mine, shops = load(path)
        gap = (rewards[1 - seat] or 0) - (rewards[seat] or 0)
        was = now = 0.0
        for item in ITEMS:
            if item not in inv[0]:
                continue
            a, _ = run(item, inv, mine, shops, False)
            b, _ = run(item, inv, mine, shops, True)
            was, now = was + a, now + b
            grand[item] += b - a
        gain = now - was
        flip = gain > gap
        flips += flip
        kept += gain > 0
        print(f"  {path.split('/')[-1].split('.')[0]:<11}{teams[1-seat][:19]:<20}"
              f"{rewards[seat] or 0:>9,.0f}{rewards[1-seat] or 0:>9,.0f}"
              f"{was:>11,.0f}{now:>11,.0f}{gain:>+10,.0f}"
              f"{('WOULD WIN' if flip else 'still short'):>16}")
    print(f"\n  {flips}/{len(paths)} losses flip to wins;  {kept}/{len(paths)} gain money at all")
    print("  by product:")
    for item, g in grand.most_common():
        print(f"    {item:<12}{g:>+14,.0f}")


if __name__ == "__main__":
    main(sys.argv[1:])
