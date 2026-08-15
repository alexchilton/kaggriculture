"""Per day, per product: the shared book's inventory, its price, and what the town drained back.

**The book is shared.** `_process_market` reads one market object off player 0's observation and
drains it per unit in lockstep between both seats (`reference/kaggriculture.py:544-547`). So a
product's price is a race, not a private resource: every unit the opponent sells lowers ours.

That makes the static marginal-revenue table a lower bound rather than an answer. Two things it
cannot see, and both move the number a lot:

- **The town drains inventory back down** all season, refilling headroom. `_town_consume` removes one
  unit of each product a shop sells every `townShopSellInterval` steps, doubled when the shop sells
  only one product, and shops unlock through the season. This is why 144 melon units realised a mean
  of $182 when the static book says melon dies at 150.
- **The opponent's sales arrive on their own schedule**, so the price we get for a unit depends on
  when we sell relative to them, not only on how much we grow.

`T` is the scale over which a product's price decays, and the products differ by 4x:

    WHEAT   T=400, above log  0.2  -- barely moves: $25 -> $20 after 600 units
    CARROT  T=450, above sqrt 0.7
    MELON   T=300, above sq   3.6  -- $250 base, then a cliff
    TOMATO  T=200, above sqrt 0.6
    STRAWBERRY T=100, above linear 1.6  -- the shallowest book in the game

Read the DAY a product's price reaches the floor. A product that floors on d20 paid full price for
20 days; one that floors on d12 did not.

    python -u scripts/when_does_the_book_crash.py --seed 3
"""
import argparse
import importlib
import pathlib
import sys

sys.path.insert(0, ".")

import reference.kaggriculture as KG

REPO = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = ("MELON", "STRAWBERRY", "TOMATO", "CARROT", "WHEAT", "MILK", "WOOL", "EGG")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    a = ap.parse_args()

    from kaggle_environments import make
    import importlib.util

    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")
    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))

    sp = importlib.util.spec_from_file_location("opp", a.opponent)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    opp = mod.agent

    env = make("kaggriculture", configuration={"seed": a.seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)

    I0 = KG.MARKET_I0
    rows, floored = [], {}
    for t in range(719):
        o = env.state[0].observation
        if t % 24 == 0:
            mk = o["market"]
            day = t // 24
            inv = {p: mk["inventory"].get(p, I0) for p in PRODUCTS}
            pr = {p: mk["prices"].get(p, 0) for p in PRODUCTS}
            rows.append((day, inv, pr))
            for p in PRODUCTS:
                if p not in floored and pr[p] <= KG.PRICE_FLOOR:
                    floored[p] = day
        env.step([me(o, t), opp(env.state[1].observation, t)])
        if env.done:
            break

    print(f"seed {a.seed}, opponent {a.opponent}, shared book, both seats selling into it\n")
    print("PRICE at dawn each day")
    print(f"{'day':>4}" + "".join(f"{p[:6]:>9}" for p in PRODUCTS))
    for day, inv, pr in rows:
        print(f"{day:>4}" + "".join(f"{pr[p]:>9,}" for p in PRODUCTS))

    print("\nNET UNITS IN THE BOOK above its starting level (both seats, minus town drain)")
    print(f"{'day':>4}" + "".join(f"{p[:6]:>9}" for p in PRODUCTS))
    for day, inv, pr in rows:
        print(f"{day:>4}" + "".join(f"{inv[p] - I0:>+9,}" for p in PRODUCTS))

    print(f"\n{'product':<12}{'T':>6}{'base':>6}{'floors on':>11}{'net units d29':>15}")
    last = rows[-1][1]
    for p in PRODUCTS:
        par = KG.MARKET_PARAMS[p]
        f = floored.get(p)
        print(f"{p:<12}{par['T']:>6}{par['base']:>6}"
              f"{('d' + str(f)) if f is not None else 'never':>11}{last[p] - I0:>+15,}")
    print("\nA product that never floors had headroom left. One that floors early was overplanted "
          "for this seed, by BOTH seats together -- the book does not care whose units they were.")


if __name__ == "__main__":
    main()
