"""Per replay, per seat: what each side REALISED per unit, and how much it sold before the crash.

Strawberry peaks around d18-d20 at $210-$233 and then falls to $60-$70 as both farms' harvests land.
In replay `93372504` we sold 213 units at a mean of $140 while the opponent sold 230 at $174 -- a
$7,242 gap in a game we lost by $5,560, on nearly identical volume. This asks whether that repeats
or whether that game was a one-off.

**Units are counted as FILLS, never offers.** The agent re-posts an unfilled order every turn, so
summing sell actions inflates volume roughly 6x. A fall in a seat's `private["shed"]` is a sale;
that is the only thing counted here.

**These replays are a SELECTED sample -- they are downloaded losses.** So no win rate, no "we lose
X% of the time", and no cross-game average of our bank. The only sound statistic is the PAIRED
comparison inside one game: both seats sold into the same book on the same days, so a difference in
realised price per unit is a difference in timing, not in luck.

`SHARE_BY` is the last day of the high window. The share of a season's units sold on or before it is
the actionable number, because it is what planting dates control: strawberry first yields at d+10
then every 2 days, so a d5 planting sells into the peak and a d11 planting sells into the floor.

    python -u scripts/when_do_we_sell.py --product STRAWBERRY --glob '~/Downloads/*.json'
"""
import argparse
import collections
import glob
import json
import os
import pathlib
import statistics
import sys

sys.path.insert(0, ".")

SHARE_BY = {"STRAWBERRY": 21, "MELON": 13, "TOMATO": 24, "CARROT": 26, "WHEAT": 26,
            "MILK": 20, "WOOL": 14, "EGG": 26}


def analyse(path, product):
    d = json.load(open(path))
    steps = d["steps"]
    names = d["info"].get("TeamNames") or ["?", "?"]
    sold = [collections.Counter(), collections.Counter()]
    rev = [0.0, 0.0]
    prev = [0, 0]
    for t in range(len(steps)):
        o = steps[t][0].get("observation") or {}
        mk = o.get("market") or {}
        price = (mk.get("prices") or {}).get(product)
        if price is None:
            continue
        for s in (0, 1):
            pr = (steps[t][s].get("observation") or {}).get("private") or {}
            cur = (pr.get("shed") or {}).get(product, 0)
            if cur < prev[s]:
                n = prev[s] - cur
                sold[s][t // 24] += n
                rev[s] += n * price
            prev[s] = cur
    cut = SHARE_BY.get(product, 21)
    out = []
    for s in (0, 1):
        tot = sum(sold[s].values())
        early = sum(v for day, v in sold[s].items() if day <= cut)
        out.append(dict(name=names[s], units=tot, revenue=rev[s],
                        per_unit=(rev[s] / tot if tot else 0.0),
                        early_share=(early / tot if tot else 0.0),
                        final=steps[-1][s].get("reward")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product", default="STRAWBERRY")
    ap.add_argument("--globs", nargs="+",
                    default=[os.path.expanduser("~/Downloads/*.json")])
    ap.add_argument("--me", default="alex chilton")
    a = ap.parse_args()

    paths = sorted({p for g in a.globs for p in glob.glob(os.path.expanduser(g))})
    cut = SHARE_BY.get(a.product, 21)
    print(f"{a.product}: realised price per unit, PAIRED inside each game. "
          f"'early' = share of units sold on or before d{cut}.")
    print("These are downloaded LOSSES -- a selected sample. Only the within-game pair is sound.\n")
    print(f"{'replay':<14}{'ours $/u':>10}{'theirs':>9}{'gap':>9}"
          f"{'our units':>11}{'theirs':>8}{'our early':>11}{'their early':>12}   opponent")
    gaps, mine, theirs, e_us, e_them = [], [], [], [], []
    for p in paths:
        try:
            rows = analyse(p, a.product)
        except Exception:
            continue
        us = next((r for r in rows if a.me.lower() in (r["name"] or "").lower()), None)
        if us is None:
            continue
        op = rows[1] if rows[0] is us else rows[0]
        if not us["units"] or not op["units"]:
            continue
        gap = us["per_unit"] - op["per_unit"]
        gaps.append(gap); mine.append(us["per_unit"]); theirs.append(op["per_unit"])
        e_us.append(us["early_share"]); e_them.append(op["early_share"])
        print(f"{pathlib.Path(p).stem:<14}{us['per_unit']:>10,.0f}{op['per_unit']:>9,.0f}"
              f"{gap:>+9,.0f}{us['units']:>11}{op['units']:>8}"
              f"{us['early_share']:>10.0%}{op['early_share']:>11.0%}   {op['name'][:18]}")
    if not gaps:
        print("no comparable games found")
        return
    worse = sum(1 for g in gaps if g < 0)
    print(f"\n{len(gaps)} games.  our mean ${statistics.mean(mine):,.0f}/unit   "
          f"theirs ${statistics.mean(theirs):,.0f}/unit   "
          f"mean gap {statistics.mean(gaps):+,.0f}   median {statistics.median(gaps):+,.0f}")
    print(f"we realised LESS per unit in {worse}/{len(gaps)} games")
    print(f"share sold by d{cut}:  ours {statistics.mean(e_us):.0%}   "
          f"theirs {statistics.mean(e_them):.0%}")
    print("\nIf the gap is consistent and our early share is lower, the crop is being planted late "
          "rather than sold badly -- first yield is d+10, so the planting date sets the sell window.")


if __name__ == "__main__":
    main()
