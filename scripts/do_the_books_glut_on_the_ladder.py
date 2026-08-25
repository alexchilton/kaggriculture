"""Do the books actually glut? Measured on REAL ladder games, not on a simulation.

Fable concluded 2026-08-25 that we are "never glutted" -- six of seven products trading below
`MARKET_I0`, deepest glut +6 units -- and recommended closing the sell side on that basis. That was
measured against `contrarian`, which banks about $15,900 against our $169,000 and barely competes
for the book.

Alex: *"r u sure??? there are lots of games where at the end milk and wool is 1"*. And the project's
own memory records ladder game 99114898 taking **WOOL from $239 to $11 on 57 units over I0**.

Those cannot both be true, so this reads the recorded games. `market.inventory` is in every step of
a replay, so the book -- and therefore the price -- is directly observable for every product on
every turn of every real game. No inference, no simulation, no opponent model.

Reports per product: the worst price reached, on which day, and how many game-turns sat at or below
a fraction of base. A single glutted game matters more than an average here: the sell rule only has
to be wrong when the book is deep, and an average over 700 healthy turns will hide it.

    python -u scripts/do_the_books_glut_on_the_ladder.py
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
US = "alex chilton"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", default="~/Downloads,data/seed_scripts/ladder_2026-08-16b,"
                                      "data/seed_scripts/top_guys")
    ap.add_argument("--limit", type=int, default=60)
    a = ap.parse_args()

    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    paths = []
    for d in a.dirs.split(","):
        root = pathlib.Path(d.strip()).expanduser()
        if not root.is_absolute():
            root = REPO / root
        paths += sorted(glob.glob(str(root / "*.json")))
    print(f"scanning {len(paths)} files\n", flush=True)

    worst = {}                                  # product -> (price, episode, day)
    deep_turns = collections.Counter()          # product -> turns at <= 25% of base
    floor_turns = collections.Counter()         # product -> turns at the $1 floor
    total_turns = collections.Counter()
    games = 0

    for p in paths[:a.limit]:
        try:
            raw = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        steps = raw.get("steps") if isinstance(raw, dict) else None
        if not steps or len(steps) < 600:
            continue
        ep = str((raw.get("info") or {}).get("EpisodeId") or pathlib.Path(p).stem)
        games += 1
        for t, st in enumerate(steps):
            obs = st[0].get("observation") or {}
            inv = (obs.get("market") or {}).get("inventory")
            if not inv:
                continue
            for prod, book in inv.items():
                if prod not in KG.MARKET_PARAMS:
                    continue
                price = KG.market_price(prod, int(book))
                base = KG.MARKET_PARAMS[prod]["base"]
                total_turns[prod] += 1
                if price <= 0.25 * base:
                    deep_turns[prod] += 1
                if price <= 1:
                    floor_turns[prod] += 1
                cur = worst.get(prod)
                if cur is None or price < cur[0]:
                    worst[prod] = (price, ep, t // TPD)

    print(f"{games} full games read\n")
    print(f"{'product':<13}{'base':>7}{'worst $':>9}{'in game':>12}{'day':>5}"
          f"{'turns <=25%':>13}{'turns at $1':>13}{'of turns':>10}")
    for prod in sorted(worst, key=lambda q: worst[q][0]):
        price, ep, day = worst[prod]
        base = KG.MARKET_PARAMS[prod]["base"]
        n = total_turns[prod]
        print(f"{prod:<13}{base:>7}{price:>9}{ep:>12}{day:>5}"
              f"{deep_turns[prod]:>13}{floor_turns[prod]:>13}{n:>10}")

    print("\nIf a product reaches $1 in a real game, the book DOES glut there and the sell rule")
    print("matters exactly at those turns -- an average over healthy turns cannot see it.")


if __name__ == "__main__":
    main()
