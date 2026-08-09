"""Does the feed-hold work move our SELL shape toward Seb's? Measured on fills, not offers.

`docs/fable_market_shape_2026-08-09.md` characterised the gap as: Seb sells few, small, late and
precise; we post a standing re-offer. #46 was raised as "the knapsack is the instrument that closes
that". It is not -- what shipped is shed *eviction* order (which product is discarded when the shed
overflows at dusk) and a bound on the wheat *buy*. Neither is a sell decision. This script is the
check on that claim rather than an argument about it.

**Fills, never offers.** The agent re-posts each quota on all 24 turns of a day, so summing `o[2]`
from the action stream counts one intended sale up to 24 times -- the mistake recorded in
`feedback_offers_are_not_fills`. What is read here is the BANK: a sale is the only event in the
game that raises money, so a positive delta is a fill and its size is the revenue. An order that
posts and fills nothing moves no money and is correctly invisible.

Reported per player: fills, fills per active day, mean and max revenue per fill, and the share
landing at hour 16 or later -- which is the whole of "late and precise".
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

TAPE = "data/seed_scripts/top_guys/90976060.json"
SCHED = "data/seed_scripts/top_guys/90976060/schedule.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _thin():
    sched = {int(k): v for k, v in json.loads(pathlib.Path(SCHED).read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _money(farm):
    return farm.get("money", 0.0)


def run(seed, use_feed_hold, jitter_seed=None):
    """Play our agent against the seb tape, recording every turn where the bank ROSE.

    A sale is the only event in the game that raises money: harvesting, feeding and building do not
    touch it, and every other market order (buy seed, buy product, buy animal, hire, buy land) only
    spends. So a positive money delta is a fill, and its size is the revenue.

    Reading the bank rather than the order list is the point. The agent re-posts each quota on all
    24 turns of a day, so counting orders counts one intended sale up to 24 times -- the mistake in
    `feedback_offers_are_not_fills`. A posted order that fills nothing moves no money and is
    correctly invisible here.

    Inventory is deliberately not read: `farm["farmer"]` is a POSITION (`[4, 4]`), not a holder, and
    `shed` is null until one is built. Assuming that shape rather than inspecting it is what broke
    the first version of this script.
    """
    import importlib

    from kaggle_environments import make

    import kagg.search.schedule_agent as SA
    importlib.reload(SA)
    if use_feed_hold:
        for flag, val in (("FEED_HOLD_BOUNDS_THE_BUY", True),):
            if hasattr(SA, flag):
                setattr(SA, flag, val)

    from kagg.arena.tape import build_tape_agent

    ours = SA.make_agent(_thin(), 0, router=True)
    theirs = build_tape_agent(TAPE, 1, jitter_seed=jitter_seed,
                              drop=0.0 if jitter_seed is None else 0.15,
                              scale=0.0 if jitter_seed is None else 0.25)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    fills = {0: [], 1: []}
    prev = [None, None]

    for t in range(24 * 30):
        if env.done:
            break
        o0 = env.state[0].observation
        farms = o0["farms"]
        for p in (0, 1):
            if prev[p] is not None:
                dm = _money(farms[p]) - prev[p]
                if dm > 0:
                    fills[p].append((t // 24, t % 24, dm))
            prev[p] = _money(farms[p])

        n0 = len(farms[0].get("hands") or [])
        n1 = len(farms[1].get("hands") or [])
        a0 = ours(o0)
        a1 = theirs(env.state[1].observation)
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    final = env.state[0].observation["farms"]
    return fills, (_money(final[0]), _money(final[1]))


def describe(label, rows):
    if not rows:
        return f"{label:<22}{'no fills':>10}"
    days = collections.Counter(r[0] for r in rows)
    hours = collections.Counter(r[1] for r in rows)
    sizes = [r[2] for r in rows]
    late = sum(v for h, v in hours.items() if h >= 16) / len(rows)
    active = len(days)
    return (f"{label:<22}{len(rows):>7}{len(rows) / max(active, 1):>9.1f}"
            f"{sum(sizes) / len(sizes):>10,.0f}{max(sizes):>9,.0f}{late:>9.0%}{active:>8}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="11,12,13")
    ap.add_argument("--jitter", type=int, default=None, help="market jitter seed for the tape")
    a = ap.parse_args()

    print(f"{'arm':<22}{'fills':>7}{'per day':>9}{"mean $":>10}{"max $":>9}{'late%':>9}{'days':>8}"
          f"   (late = hour >= 16)", flush=True)
    for seed in [int(s) for s in a.seeds.split(",")]:
        print(f"--- seed {seed}", flush=True)
        for use_hold in (False, True):
            fills, money = run(seed, use_hold, a.jitter)
            arm = "feed_hold" if use_hold else "shipped"
            print(describe(f"  ours ({arm})", fills[0]) + f"   ${money[0]:,.0f}", flush=True)
            if not use_hold:
                print(describe("  SEB (tape)", fills[1]) + f"   ${money[1]:,.0f}", flush=True)


if __name__ == "__main__":
    main()
