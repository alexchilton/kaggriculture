"""Find the strongest cornering configuration, by playing it against our own shipped agent.

## Step 1 of 3

    1. THIS: search `swap_from` x `release_day` x town for the cell that beats us hardest.
    2. Flip that cell onto our seat.
    3. Grade it by paired tape replay over the whole loss corpus, on flipped games.

## Calibration, and why it is the first thing in this file

The target is ladder game 98495047, seed 1640915609, which we lost by **$29,384**. Until a cell
reaches that, the grid is in the wrong region and any aggregate over it describes nothing.

Progress so far, same seed, opponent built from `kagg.agents.morph`:

    swap_from  tiles@d26  held@d28  close$  town deficit   margin
        14        30        135      211        743       +12,194   over-committed, loses
        18        29        130      286        818        -5,828   best so far
        21        32         93      224        757        -4,555
        24        29         27      272        805        -2,259
    Mr Carrot     32         76      498        975       -29,384   the real game

Holding is no longer the limiter -- at `swap_from=18` we hold **130** units against his 76 and still
get $286 against his $498. The **deficit** is the limiter, and price is a pure function of it
(`reference/kaggriculture.py:192-207`). In the real game the loser sold only 11 carrots all season;
here our own seat keeps replenishing the book. So `our_floor` is an axis too: it withholds on OUR
side, which is the only way the deficit reaches 975.

## What each axis changes

    swap_from    first day the opponent's own PLANT WHEAT is rewritten to CARROT. Early enough to
                 ripen (CARROT is first_yield_day 2), late enough not to sacrifice mid-season wheat
                 income -- d14 banks $48,417 and loses, so this is a real trade-off, not a ramp.
    release_day  when the withheld stock is finally sold. d29 is the last day that banks; d28 sells
                 into a shallower deficit but leaves a second market turn.
    our_floor    price below which OUR seat stops selling. 0 is the shipped agent. Non-zero is the
                 counterfactual where we stop feeding the book we are trying to corner.
    seed         the town. Drain differs with the shop draw, and drain sets how big the deficit can
                 grow, so a cell that wins on one town may not exist on another.

**A cell can only win by abstaining early, converting late, and withholding.** A configuration that
supplies its hinge crop all season keeps its own book under the knee and is a null by construction --
measured, and the reason the first heuristic attempt returned +$166k for us.

    python -u scripts/find_the_carrot_algo.py --seeds 1640915609,700,701
"""

import argparse
import collections
import itertools
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
US = ".claude/worktrees/e2500/submission/e2500_close.py"
BUNDLE = "submission/e2500_carrot.py"
MARKET_I0 = 10_000


def snap(steps, day, seat):
    """`(carrot tiles, carrot held, price, town deficit)` for `seat` at dusk on `day`."""
    i = min(day * TPD + TPD - 1, len(steps) - 1)
    obs = steps[i][seat]["observation"]
    priv = obs["private"]
    held = collections.Counter(priv.get("shed") or {})
    for inv in (priv.get("inventories") or []):
        held.update(inv)
    tiles = sum(1 for row in obs["farms"][seat]["tiles"] for t in row
                if isinstance(t, dict) and t.get("crop") == "CARROT")
    mkt = steps[i][0]["observation"].get("market") or {}
    price = (mkt.get("prices") or {}).get("CARROT", 0)
    inv = (mkt.get("inventory") or {}).get("CARROT", MARKET_I0)
    return tiles, held.get("CARROT", 0), price, MARKET_I0 - inv


def one(seed, swap_from, release_day, our_floor):
    """One game: our agent (optionally withholding) against a cornering morph. Returns a row."""
    from kaggle_environments import make                                     # noqa: PLC0415

    from kagg.agents.morph import make_agent                                 # noqa: PLC0415

    opp = make_agent(bundle=BUNDLE, hinge_crop="CARROT",
                     swap_from=swap_from, swap_to=27, release_day=release_day)
    if our_floor:
        # Our seat also stops feeding the book. `hinge_crop=None` keeps our planting untouched --
        # the ONLY difference from the shipped agent is that carrot sales below the floor are held.
        us = make_agent(bundle=BUNDLE, hinge_crop=None, withhold=("CARROT",),
                        release_day=29, floor_price=our_floor)
    else:
        us = str(REPO / US)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([us, opp])
    st = env.steps

    t26, _, _, _ = snap(st, 26, 1)
    _, h28, _, _ = snap(st, 28, 1)
    _, _, px, deficit = snap(st, 29, 1)
    banks = [st[-1][s]["observation"]["farms"][s]["money"] for s in (0, 1)]
    return {"seed": seed, "swap_from": swap_from, "release_day": release_day,
            "our_floor": our_floor, "opp_tiles_d26": t26, "opp_held_d28": h28,
            "close_price": round(float(px or 0)), "deficit": deficit,
            "ours": round(banks[0]), "theirs": round(banks[1]),
            "margin": round(banks[0] - banks[1])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="1640915609,700,701")
    ap.add_argument("--swap-from", default="16,18,20")
    ap.add_argument("--release", default="29")
    ap.add_argument("--our-floor", default="0,60")
    ap.add_argument("--out", default="data/logs/carrot_algo_search.csv")
    a = ap.parse_args()

    seeds = [int(s) for s in a.seeds.split(",")]
    sweeps = [int(s) for s in a.swap_from.split(",")]
    rels = [int(s) for s in a.release.split(",")]
    floors = [int(s) for s in a.our_floor.split(",")]
    grid = list(itertools.product(seeds, sweeps, rels, floors))
    print(f"{len(grid)} games: {len(seeds)} towns x {len(sweeps)} swap_from x "
          f"{len(rels)} release x {len(floors)} our_floor", flush=True)
    print("target: margin -29,384 on seed 1640915609 (deficit 975, close $498)\n", flush=True)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["seed", "swap_from", "release_day", "our_floor", "opp_tiles_d26", "opp_held_d28",
            "close_price", "deficit", "ours", "theirs", "margin"]
    # Header first, one flushed row per game: a sweep that writes at the end loses everything when
    # it is killed, and this project has produced 0 rows from 29,568 planned seasons that way.
    fh = out.open("w")
    fh.write(",".join(cols) + "\n")
    fh.flush()

    t0 = time.time()
    for n, (seed, sf, rel, floor) in enumerate(grid, 1):
        try:
            r = one(seed, sf, rel, floor)
        except Exception as e:                                               # noqa: BLE001
            print(f"  {n}/{len(grid)} seed {seed} sf {sf} floor {floor}: {e!r}", flush=True)
            continue
        fh.write(",".join(str(r[c]) for c in cols) + "\n")
        fh.flush()
        print(f"  {n:>3}/{len(grid)} seed {seed:>10} sf {sf:>2} rel {rel} floor {floor:>3} | "
              f"held {r['opp_held_d28']:>3} close ${r['close_price']:>4} "
              f"deficit {r['deficit']:>4} | margin {r['margin']:>+9,}", flush=True)
    fh.close()
    print(f"\n{time.time() - t0:.0f}s -> {out}", flush=True)


if __name__ == "__main__":
    main()
