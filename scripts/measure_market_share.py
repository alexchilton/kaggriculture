"""What share of each town drain did the leader actually capture?

`scheduler.OPPONENT_SHARE` was set to 0.5 on an argument rather than a measurement -- "the opponent
sells into the same town inventory, so halve every drain" -- and that halving is what produced 4 cows
and 3 sheep against the leader's 8 and 6. Unhalving it reproduced his herd exactly, so 0.5 is wrong for
*sizing*. But 1.0 cannot be right for *revenue*: if both players banked nearly the whole drain the total
would exceed what the town pays out, and their final banks differ by only 1.7-4.2%.

Both can be true at once, and that is the point of this script. Sizing and pricing are different
questions:

- **Capacity** is sized against the whole drain, because a contested market is won by whoever can
  deliver when the shop opens. Being able to supply only half guarantees you take only half.
- **Revenue** is what you actually banked, which is your realised share of the drain.

So rather than sweep a single number, measure the realised share directly. Every SELL order the leader
submitted is on the tape, for both seats, so `units_sold / DRAIN_UNITS` is a measurement and not a
model. Reported per product and per seat across all four replays.

Caveat, stated because it bounds the conclusion: a SELL *order* is a request, and `_process_market`
fills it only while shed stock and town demand last. So these counts are an upper bound on units
actually moved -- they are what he asked to sell. Where an order exceeds the drain, that is the
over-request the routines deliberately make (`grow()` over-requests on purpose), not a capture above
100%.
"""

import collections
import json
import pathlib

import numpy as np

from kagg.search import chains as C
from kagg.search import routines as R

LEADER = "somewhere after"
REPLAYS = sorted(pathlib.Path("data/seed_scripts/new_leader").glob("*.json"))


def sells_by_product(path):
    """`{seat_label: {product: units_ordered}}` plus each seat's final bank, off one tape."""
    d = json.load(open(path))
    names = d["info"]["TeamNames"]
    out = {n: collections.Counter() for n in names}
    banks = {n: 0.0 for n in names}
    for step in d["steps"]:
        for seat, name in enumerate(names):
            st = step[seat] or {}
            obs = st.get("observation") or {}
            farms = obs.get("farms")
            if farms and seat < len(farms):
                banks[name] = float(farms[seat]["money"])
            for o in ((st.get("action") or {}).get("market") or []):
                if o and o[0] == "SELL":
                    out[name][o[1]] += int(o[2]) if len(o) > 2 else 1
    return out, banks


print("=" * 96)
print("REALISED SHARE OF EACH TOWN DRAIN -- units ordered on the tape / DRAIN_UNITS")
print("=" * 96)

totals = collections.defaultdict(list)
opp_totals = collections.defaultdict(list)
for path in REPLAYS:
    sells, banks = sells_by_product(path)
    leader = next((n for n in sells if n == LEADER), None)
    if leader is None:
        print(f"\n{path.name}: leader not in {list(sells)} -- skipped")
        continue
    others = [n for n in sells if n != leader]
    print(f"\n{path.name}   {leader} ${banks[leader]:,.0f} "
          f"vs {others[0]} ${banks[others[0]]:,.0f} "
          f"({(banks[leader]/max(banks[others[0]],1)-1)*100:+.1f}%)")
    print(f"      {'product':>12} {'drain':>7} {'HIS':>7} {'share':>7} "
          f"{'THEIRS':>7} {'share':>7} {'both':>7}")
    for prod, drain in sorted(C.DRAIN_UNITS.items(), key=lambda kv: -kv[1]):
        his = sells[leader].get(prod, 0)
        thr = sells[others[0]].get(prod, 0)
        if not his and not thr:
            continue
        totals[prod].append(his / drain)
        opp_totals[prod].append(thr / drain)
        print(f"      {prod:>12} {drain:>7} {his:>7} {his/drain:>6.0%} "
              f"{thr:>7} {thr/drain:>6.0%} {(his+thr)/drain:>6.0%}")

print()
print("=" * 96)
print("MEAN ACROSS REPLAYS -- this is what `OPPONENT_SHARE` should be, per product")
print("=" * 96)
print(f"{'product':>12} {'drain':>7} {'his share':>11} {'their share':>13} {'combined':>10}")
w_his, w_both, w_drain = 0.0, 0.0, 0.0
for prod, drain in sorted(C.DRAIN_UNITS.items(), key=lambda kv: -kv[1]):
    if prod not in totals:
        print(f"{prod:>12} {drain:>7} {'never sold':>11}")
        continue
    h, t = float(np.mean(totals[prod])), float(np.mean(opp_totals[prod]))
    print(f"{prod:>12} {drain:>7} {h:>10.0%} {t:>12.0%} {h+t:>9.0%}")
    w_his += h * drain
    w_both += (h + t) * drain
    w_drain += drain

print()
print(f"drain-weighted: he orders {w_his/w_drain:.2f} of the drain he competes for, "
      f"both seats together {w_both/w_drain:.2f}")
print()
print("Read this as two numbers, not one:")
print(f"  capacity_share -> size the mix so you *can* serve the whole drain")
print(f"  revenue_share  -> what a contested drain actually pays you")