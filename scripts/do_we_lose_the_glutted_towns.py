"""Are the games where WOOL and MILK crash to $1 the same games we lose?

Alex, 2026-08-25: *"the milk yarn = 1 is the exact towns we do shit in"*.

`do_the_books_glut_on_the_ladder.py` established that the glut is real on the ladder -- WOOL sits at
the $1 floor for 8.7% of all recorded turns, MILK and MELON the same shape -- against a simulation
that never gluts at all. This asks the next question, which is the one that decides whether it
matters: is the depth of the glut related to whether we WON?

Per recorded game, both are directly readable and neither is inferred:

    our result      `rewards` against `info.TeamNames`, so no replay and no simulation
    the glut        `market.inventory` per turn -> `market_price`, the minimum reached per product

If the losses are the deep-glut games, the sell side is not closed, and the policy question is what
to do when a book is at the floor and the shed is full. If the two are unrelated, the glut is real
but incidental and the search should go elsewhere.

**These games are a SELECTED corpus** -- `project_kaggriculture_losing_narrowly` records that Alex
downloads losses. So the absolute win rate here means nothing. The comparison WITHIN the corpus,
between deep-glut games and shallow ones, is what is being read.

    python -u scripts/do_we_lose_the_glutted_towns.py
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
WATCH = ("WOOL", "MILK", "MELON", "STRAWBERRY")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", default="~/Downloads,data/seed_scripts/ladder_2026-08-16b,"
                                      "data/seed_scripts/top_guys")
    ap.add_argument("--limit", type=int, default=120)
    a = ap.parse_args()

    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    paths = []
    for d in a.dirs.split(","):
        root = pathlib.Path(d.strip()).expanduser()
        if not root.is_absolute():
            root = REPO / root
        paths += sorted(glob.glob(str(root / "*.json")))

    rows = []
    seen = set()
    for p in paths[:a.limit]:
        try:
            raw = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        steps = raw.get("steps") if isinstance(raw, dict) else None
        if not steps or len(steps) < 600:
            continue
        info = raw.get("info") or {}
        names = info.get("TeamNames") or []
        if US not in names:
            continue
        seat = names.index(US)
        ep = str(info.get("EpisodeId") or pathlib.Path(p).stem)
        if ep in seen:
            continue
        seen.add(ep)

        last = steps[-1]
        farms = (last[0].get("observation") or {}).get("farms") or []
        if len(farms) < 2:
            continue
        ours = float(farms[seat].get("money", 0))
        theirs = float(farms[1 - seat].get("money", 0))

        # Deepest price each watched product reached, and how long it spent on the floor.
        low = {p2: 10 ** 9 for p2 in WATCH}
        floor = collections.Counter()
        for st in steps:
            inv = ((st[0].get("observation") or {}).get("market") or {}).get("inventory")
            if not inv:
                continue
            for p2 in WATCH:
                if p2 not in inv:
                    continue
                pr = KG.market_price(p2, int(inv[p2]))
                if pr < low[p2]:
                    low[p2] = pr
                if pr <= 1:
                    floor[p2] += 1
        rows.append((ep, ours, theirs, ours > theirs, low, floor))

    if not rows:
        print("no games with our seat found")
        return

    print(f"{len(rows)} games with our seat\n")
    print(f"{'episode':>10}{'result':>8}{'ours':>11}{'theirs':>11}{'margin':>11}"
          + "".join(f"{p2[:6] + ' low':>12}" for p2 in WATCH)
          + f"{'floor turns':>13}")
    for ep, ours, theirs, won, low, floor in sorted(rows, key=lambda r: r[1] - r[2]):
        ft = sum(floor.values())
        print(f"{ep:>10}{'WIN' if won else 'loss':>8}{ours:>11,.0f}{theirs:>11,.0f}"
              f"{ours - theirs:>+11,.0f}"
              + "".join(f"{low[p2]:>12}" for p2 in WATCH)
              + f"{ft:>13}")

    # ---- the comparison ---------------------------------------------------------------------
    wins = [r for r in rows if r[3]]
    losses = [r for r in rows if not r[3]]

    def mean_floor(rs):
        return sum(sum(r[5].values()) for r in rs) / len(rs) if rs else 0.0

    def mean_low(rs, p2):
        return sum(r[4][p2] for r in rs) / len(rs) if rs else 0.0

    print(f"\n{'':<22}{'wins':>10}{'losses':>10}")
    print(f"{'games':<22}{len(wins):>10}{len(losses):>10}")
    print(f"{'turns at the $1 floor':<22}{mean_floor(wins):>10.0f}{mean_floor(losses):>10.0f}")
    for p2 in WATCH:
        print(f"{'mean lowest ' + p2:<22}{mean_low(wins, p2):>10.0f}{mean_low(losses, p2):>10.0f}")

    deep = [r for r in rows if sum(r[5].values()) >= 200]
    shallow = [r for r in rows if sum(r[5].values()) < 200]
    print(f"\nsplit at 200 turns on the floor:")
    for label, rs in (("deep glut", deep), ("shallow", shallow)):
        if not rs:
            continue
        wr = sum(1 for r in rs if r[3]) / len(rs)
        marg = sum(r[1] - r[2] for r in rs) / len(rs)
        print(f"  {label:<12}{len(rs):>4} games   win {wr:>5.0%}   mean margin {marg:>+11,.0f}")

    print("\nThe corpus is SELECTED -- losses are downloaded preferentially -- so read the")
    print("difference between the two rows, never the absolute win rate.")


if __name__ == "__main__":
    main()
