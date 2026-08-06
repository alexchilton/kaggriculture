"""Volume or price? The one question that separates a hostile opponent from an unlucky board.

Our own leaderboard games swing hugely -- ~$130k in some, far less in others -- and "the opponent's
tactics" and "a bad seed" predict the SAME final number while meaning opposite things. They do not
predict the same intermediate quantities, and this prints those:

    units sold      what the FARM produced and got to market. Falls when the board was poor, the
                    parcels came late, or the crew under-executed. Insensitive to the opponent.
    book price      what a unit FETCHED, read straight off the shared order book the replay carries
                    every turn. Both seats sell into ONE inventory and `market_price` falls
                    monotonically in it (`kaggriculture.py:177`), so an opponent can tax us without
                    ever touching our farm. Reported as a whole-season mean and as a days-15-29 mean,
                    because that is the window most of the selling happens in.

So:

    units level, price down           -> the book. The opponent sold into what we were selling.
    units down, price level           -> the farm. Seed, land timing, or execution.
    both down                         -> the farm, and the collapse cost us the book as well.

Also prints the opponent's own volume per product, because "they crushed our milk price" is only a
claim about them if they were actually selling milk.

**Do not price a sale by differencing the bank.** The bank also moves on every purchase, and several
products can leave the shed on one turn. That attribution reported $3,003 of revenue against a
$103,367 season before it was thrown away for the book series above.

Measured on the two games this was written for, both of them our own agent on the ladder:

    game        opponent      our units    milk price d15+    final
    90534961    Sophie             1058              101.1    $103,367   LOST
    90536513    Mohit Babel        1017              225.1    $128,735   WON

We sold MORE and banked $25,368 LESS. Not the seed and not the crew.

Run: python -u scripts/why_did_that_game_go_badly.py data/seed_scripts/our_games/*.json --me <team>
"""

import argparse
import collections
import json
import pathlib
import statistics
import sys

sys.path.insert(0, ".")

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")


def _seat_of(info, me):
    names = info.get("TeamNames") or []
    for i, n in enumerate(names):
        if me and me.lower() in n.lower():
            return i, names
    return 0, names


def _money(step, seat):
    obs = (step[seat] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    if seat < len(farms):
        return float(farms[seat].get("money", 0) or 0)
    farms0 = ((step[0] or {}).get("observation") or {}).get("farms") or []
    return float(farms0[seat].get("money", 0) or 0) if seat < len(farms0) else 0.0


def analyse(path, me):
    d = json.loads(pathlib.Path(path).read_text())
    seat, names = _seat_of(d.get("info") or {}, me)
    steps = d["steps"]

    # Shed contents per seat, sampled each turn, so a SELL can be priced by what actually left it.
    sold_units = [collections.Counter(), collections.Counter()]
    ordered = [collections.Counter(), collections.Counter()]
    bank = [[], []]
    for t, step in enumerate(steps[1:], start=1):
        for s in (0, 1):
            a = (step[s] or {}).get("action") or {}
            for o in a.get("market") or []:
                if not o:
                    continue
                if o[0] == "SELL" and len(o) > 2 and o[1] in PRODUCTS:
                    ordered[s][o[1]] += int(o[2])
            bank[s].append(_money(step, s))

    # Units sold: a fall in a seat's shed IS produce leaving for the market. Reliable.
    #
    # Revenue per unit is NOT derived by differencing the bank -- the bank also moves on purchases and
    # several products can leave the shed on one turn, and an early attempt at that attribution
    # reported $3,003 of revenue against a $103,367 season. The replay carries the shared order book
    # every turn instead (`obs["market"]["prices"]`), which is the honest and exact figure: it is the
    # price BOTH seats face, and it is the whole mechanism by which an opponent can cost us money
    # without touching our farm.
    shed_prev = [None, None]
    for step in steps[1:]:
        for s in (0, 1):
            obs = (step[s] or {}).get("observation") or {}
            shed = collections.Counter((obs.get("private") or {}).get("shed") or {})
            if shed_prev[s] is not None:
                for p in PRODUCTS:
                    gone = shed_prev[s][p] - shed[p]
                    if gone > 0:
                        sold_units[s][p] += gone
            shed_prev[s] = shed

    # The shared book, as seen from seat 0 -- both seats see the same market object.
    price = {p: [] for p in PRODUCTS}
    for step in steps[1:]:
        m = ((step[0] or {}).get("observation") or {}).get("market") or {}
        for p, v in (m.get("prices") or {}).items():
            if p in price:
                price[p].append(float(v))

    final = [bank[s][-1] if bank[s] else 0.0 for s in (0, 1)]
    return dict(path=str(path), names=names, seat=seat, final=final,
                sold_units=sold_units, price=price, ordered=ordered)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("replays", nargs="+")
    ap.add_argument("--me", default="", help="substring of our team name")
    args = ap.parse_args()

    runs = [analyse(p, args.me) for p in args.replays]
    for r in runs:
        us, them = r["seat"], 1 - r["seat"]
        verdict = "WON " if r["final"][us] > r["final"][them] else "LOST"
        print(f"\n{'=' * 96}")
        print(f"{pathlib.Path(r['path']).name}   {verdict}   "
              f"{r['names'][us]} ${r['final'][us]:,.0f}   vs   "
              f"{r['names'][them]} ${r['final'][them]:,.0f}")
        print(f"{'=' * 96}")
        print(f"  {'product':<12}{'our units':>10}{'their units':>13}"
              f"{'book price mean':>17}{'days 15-29':>13}{'min':>8}")
        for p in PRODUCTS:
            ou, tu = r["sold_units"][us][p], r["sold_units"][them][p]
            series = r["price"][p]
            if not (ou or tu) or not series:
                continue
            late = series[15 * 24:] or series
            print(f"  {p:<12}{ou:>10}{tu:>13}"
                  f"{statistics.mean(series):>17,.1f}{statistics.mean(late):>13,.1f}"
                  f"{min(series):>8,.0f}")

    if len(runs) > 1:
        print(f"\n{'=' * 96}\nSIDE BY SIDE -- ours only\n{'=' * 96}")
        hdr = "".join(f"{pathlib.Path(r['path']).stem:>24}" for r in runs)
        print(f"  {'product':<12}{hdr}")
        print(f"  {'':<12}" + "".join(f"{'units':>10}{'price d15+':>14}" for _ in runs))
        for p in PRODUCTS:
            cells, any_row = "", False
            for r in runs:
                u = r["sold_units"][r["seat"]][p]
                series = r["price"][p]
                late = series[15 * 24:] or series or [0]
                any_row = any_row or bool(u)
                cells += f"{u:>10}{statistics.mean(late):>14,.1f}"
            if any_row:
                print(f"  {p:<12}{cells}")
        print()
        for r in runs:
            us = r["seat"]
            print(f"  {pathlib.Path(r['path']).stem}  final ${r['final'][us]:,.0f}   "
                  f"units sold {sum(r['sold_units'][us].values())}   "
                  f"opponent {r['names'][1 - us]}")
        print("\n  MORE units sold for LESS money is the shared order book, not the board and not the "
              "crew.\n  Fewer units at a level price is the farm: seed, land timing or execution.")


if __name__ == "__main__":
    main()
