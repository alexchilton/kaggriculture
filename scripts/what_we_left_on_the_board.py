"""What a finished game threw away: produce in hands, ripe tiles never harvested, seed never planted.

Three leaks, all of them invisible in the bank and all of them priced here at what they would
ACTUALLY have fetched -- the book is walked one unit at a time, because selling n units does not
realise n x the marginal price.

- **In hands at the final turn.** `_end_of_day` calls `_drop_inventories_to_shed`, but on day 29
  that runs after the last step, and `_commit_unit` refuses a SELL unless the goods are already in
  `private["shed"]`. So anything in a hand at the close is discarded.
- **Ripe and never harvested.** A tile holding `yield_units` that no stop reached.
- **Seed bought and never planted.** Cash converted into nothing.

Why it matters: on `93346440`, a game WON by $70,525, this totalled $3,260 -- of which $1,525 was
seven units of WOOL and MILK, because both closed ABOVE base on that board. Recent losses have
margins of $645, $962, $1,963 and $3,414. The leak is the size of the losses.

    python -u scripts/what_we_left_on_the_board.py ~/Downloads/93351093.json
    python -u scripts/what_we_left_on_the_board.py ~/Downloads/*.json --me "alex chilton"
"""
import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

import reference.kaggriculture as KG


def realised(inventory, product, units):
    """What `units` of `product` would fetch, selling one at a time and walking the book down."""
    stock, total = inventory[product], 0.0
    for _ in range(int(units)):
        total += KG.market_price(product, stock)
        stock += 1
    return total


def report(path, me_name):
    d = json.loads(pathlib.Path(path).read_text())
    steps = d["steps"]
    names = d.get("info", {}).get("TeamNames") or ["seat0", "seat1"]
    me = next((i for i, n in enumerate(names) if me_name.lower() in str(n).lower()), 0)
    them = 1 - me

    obs = steps[-1][me]["observation"]
    priv = steps[-1][me]["observation"]["private"]
    inv = obs["market"]["inventory"]
    money = [f.get("money", 0) for f in obs["farms"]]
    margin = money[me] - money[them]

    print("=" * 78)
    print(f"{pathlib.Path(path).stem}   {'WIN' if margin > 0 else 'LOSS'}   "
          f"{names[me]} ${money[me]:,.0f}  vs  {names[them]} ${money[them]:,.0f}   "
          f"margin ${margin:,.0f}")

    hands = collections.Counter()
    for h in (priv.get("inventories") or []):
        for k, v in (h or {}).items():
            hands[k] += v
    standing = collections.Counter()
    for row in obs["farms"][me]["tiles"]:
        for c in row:
            if isinstance(c, dict) and c.get("crop") and c.get("yield_units"):
                standing[c["crop"]] += c["yield_units"]

    print(f"\n  {'source':<26}{'product':<12}{'units':>6}{'unit $':>9}{'realised $':>12}")
    total = 0.0
    for label, bag in (("in hands, discarded", hands), ("ripe, never harvested", standing)):
        for p, n in sorted(bag.items()):
            if p not in inv or not n:
                continue
            value = realised(inv, p, n)
            total += value
            print(f"  {label:<26}{p:<12}{n:>6}{KG.market_price(p, inv[p]):>9.0f}{value:>12,.0f}")

    seeds = {k: v for k, v in (priv.get("seeds") or {}).items() if v}
    seed_value = sum(KG.CROPS[k]["seed"] * v for k, v in seeds.items())
    if seeds:
        print(f"  {'seed bought, never planted':<26}{str(seeds):<12}"
              f"{sum(seeds.values()):>6}{'-':>9}{seed_value:>12,.0f}")

    leak = total + seed_value
    print(f"\n  {'TOTAL LEFT ON THE BOARD':<54}{leak:>12,.0f}")
    if margin < 0:
        print(f"  losing margin ${-margin:,.0f} -- the leak "
              f"{'COVERS it' if leak > -margin else 'does NOT cover it'}")
    return leak, margin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("replays", nargs="+")
    ap.add_argument("--me", default="alex chilton")
    args = ap.parse_args()
    rows = [report(p, args.me) for p in args.replays]
    if len(rows) > 1:
        covered = sum(1 for leak, m in rows if m < 0 and leak > -m)
        losses = sum(1 for _, m in rows if m < 0)
        print(f"\n{losses} losses, {covered} of them smaller than their own closing leak")


if __name__ == "__main__":
    main()
