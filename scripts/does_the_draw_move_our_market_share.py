"""Does the shop DRAW move our market share on the lines that have no adaptive handling?

The question, from the 2026-08-24 session: the dawn planner reads `unlocked_shops` and re-plans
only for the product lines someone hand-built drain-awareness for -- WOOL (`_herd_split`'s
undrawn-deck logic), MILK (`MILK_DRAINING_SHOPS` headroom), STRAWBERRY (`STRAWBERRY_SHOPS`),
TOMATO/CARROT (their own drain gates). EGG has nothing, and WHEAT/FERTILIZER sell paths never
read `unlocked_shops` at all. `cover.py` itself is shop-blind end to end.

**Prediction if the static-line theory is right:** our realised outcome on an ADAPTIVE line should
be insensitive to how kindly the town drew -- the planner re-plans around a bad draw. On a
NON-adaptive line our outcome should move with the draw, because nothing between the plan and the
market reacts to it.

Measured per game, both seats on the same book:

    share   our revenue / (our + their revenue) for the product
    r       Pearson r between that share and how many shops buying the product the town
            actually drew (instances, since draws are with replacement)
    r_time  same, against the STEP of the first unlock of any shop buying the product
            (negative r means later unlock, worse share)

A strong r on one line and ~0 on another is the signature. No strong r anywhere means the draw
does not reach the market outcomes through this channel and the static-line theory dies here.

Fills are inventory deltas, not offers (see `what_we_actually_get_paid.py` for why).

    python -u scripts/does_the_draw_move_our_market_share.py --dirs ladder_2026-08-16b,top_guys --limit 100
"""

import argparse
import collections
import glob
import json
import math
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
US = "alex chilton"

SOLD_ONLY = ("MILK", "WOOL", "EGG", "MELON", "STRAWBERRY", "CARROT", "TOMATO")

#: Which shops buy what -- `reference/kaggriculture.py` SHOPS, verbatim. Kept local so this
#: script cannot import the agent (and its 151 constants) just to read a constant dict.
SHOPS = {
    "BAKERY": ["EGG", "WHEAT"],
    "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
SHOPS_FOR = {p: [s for s, prods in SHOPS.items() if p in prods] for p in SOLD_ONLY}


def _held(step, seat):
    priv = step[seat]["observation"]["private"]
    out = collections.Counter(priv.get("shed") or {})
    for inv in priv.get("inventories") or []:
        out.update(inv)
    return out


def _pearson(xs, ys):
    n = len(xs)
    if n < 4:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def audit(path):
    """`(per-product fills, draw features)` or None."""
    try:
        rep = json.loads(pathlib.Path(path).read_text())
    except Exception:
        return None
    if not isinstance(rep, dict):
        return None
    info = rep.get("info") or {}
    names = info.get("TeamNames") or []
    steps = rep.get("steps") or []
    if US not in names or len(steps) < 700:
        return None
    seat = names.index(US)

    # Draw features off seat 0's observation, tracking first-unlock step per shop NAME.
    counts = collections.Counter()
    first_at = {}
    prev_shops = []
    fills = {p: [0, 0.0, 0, 0.0] for p in SOLD_ONLY}
    prev_held = {0: _held(steps[0], 0), 1: _held(steps[1], 1)} if len(steps) > 1 else None
    if prev_held is None:
        return None

    for i in range(len(steps)):
        step = steps[i]
        shops = list(((step[0]["observation"]).get("town") or {}).get("unlocked_shops") or [])
        if len(shops) > len(prev_shops):
            for s in shops:
                counts[s] += 1
                first_at.setdefault(s, i)
            prev_shops = shops
        if i == 0:
            continue
        px = ((step[0]["observation"].get("market") or {}).get("prices") or {})
        for s in (0, 1):
            now = _held(step, s)
            for p in SOLD_ONLY:
                gone = prev_held[s].get(p, 0) - now.get(p, 0)
                if gone > 0:
                    slot = 0 if s == seat else 2
                    fills[p][slot] += gone
                    fills[p][slot + 1] += gone * float(px.get(p, 0) or 0)
            prev_held[s] = now
    return fills, counts, first_at


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", default="ladder_2026-08-16b,top_guys")
    ap.add_argument("--limit", type=int, default=100)
    a = ap.parse_args()

    files = []
    for d in a.dirs.split(","):
        files += sorted(glob.glob(str(REPO / "data/seed_scripts" / d.strip() / "*.json")))
    print(f"scanning {len(files)} files from {a.dirs}", flush=True)

    games = []
    totals = {p: [0, 0.0, 0, 0.0] for p in SOLD_ONLY}
    for f in files:
        if len(games) >= a.limit:
            break
        r = audit(f)
        if r is None:
            continue
        fills, counts, first_at = r
        games.append(r)
        for p in SOLD_ONLY:
            for k in range(4):
                totals[p][k] += fills[p][k]

    print(f"\n{len(games)} games\n")
    print(f"{'product':<12} {'handles draw?':>14} {'our share':>18} "
          f"{'r vs shop count':>17} {'r vs first unlock':>19}")
    verdict = {"WOOL": "yes (_herd_split)", "MILK": "yes (drain headroom)",
               "STRAWBERRY": "yes (shop count)", "TOMATO": "yes (drain gate)",
               "CARROT": "yes (drain gate)", "EGG": "NO", "MELON": "no shops -> control"}
    for p in SOLD_ONLY:
        ou, orev, tu, trev = totals[p]
        shares, xs_count, xs_time = [], [], []
        for fills, counts, first_at in games:
            _, orv, _, trv = fills[p]
            if orv + trv <= 0:
                continue
            shares.append(orv / (orv + trv))
            xs_count.append(sum(counts[s] for s in SHOPS_FOR[p]))
            t = min((first_at[s] for s in SHOPS_FOR[p] if s in first_at), default=None)
            xs_time.append(t if t is not None else 720)
        if not shares:
            continue
        m = sum(shares) / len(shares)
        sd = (sum((x - m) ** 2 for x in shares) / len(shares)) ** 0.5
        print(f"{p:<12} {verdict[p]:>14} {m:>7.0%} ±{sd:>5.0%} ({len(shares):>3}g) "
              f"{_pearson(xs_count, shares):>17.2f} {_pearson(xs_time, shares):>19.2f}")

    print("\nReading it:")
    print("  r near 0 on an ADAPTIVE line and |r| clearly > 0 on a NON-adaptive line")
    print("  is the static-line defect. |r| < ~0.2 everywhere means the draw does not reach")
    print("  realised outcomes through this channel and the theory is dead.")


if __name__ == "__main__":
    main()
