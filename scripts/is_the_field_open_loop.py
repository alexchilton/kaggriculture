"""Do the top players react to their opponent at all, or do they replay one fixed season?

Alex, 2026-08-21: *"i think kawa is optimised to the board and the rules - i dont think there are
many optimised to the opponent and i think those are way more dynamic reactions"*.

This is the load-bearing premise for every adversarial arm, so it gets measured rather than
assumed. If the field is open-loop, a rule of ours that reads THEIR board cannot be countered --
they will not adapt back -- and the market is the one channel through which we can still hurt them.
If the field is reactive, the same rule starts an arms race we have not modelled.

The test: take one player with many recorded games, group their games by OPPONENT, and compare
their own action streams turn by turn. A player optimised to the board plays nearly the same 720
turns whatever is in the other chair; a player optimised to the opponent does not.

Two confounds are handled, and both matter:

  **The town differs between games.** A player who reacts only to the SHOP DRAW will still diverge
  across games, and that is not opponent-reaction. So divergence is reported against the day the
  first shop lands (d3) -- anything before d3 is a response to neither, since no shop has unlocked
  and the boards start identical (`project_kaggriculture_start_state_is_fixed`).

  **Comparing the wrong quantity.** Two seasons can agree on every op and differ on market
  quantities, or vice versa. Unit ops and market orders are counted separately.

    python -u scripts/is_the_field_open_loop.py --player "Ryo Hasegawa"
    python -u scripts/is_the_field_open_loop.py --player tetsuya --max-games 12
"""

import argparse
import collections
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ROOT = REPO / "data/seed_scripts"
CACHE = REPO / "data/action_cache.jsonl"

#: The first shop unlocks at d3 h0. Before that no draw has landed and both boards are identical,
#: so any disagreement there is the player's own randomness, not a reaction to anything.
FIRST_SHOP_TURN = 3 * 24


def drain_key(draw):
    """The town's DRAIN VECTOR -- what it takes off the book, not which shops it drew.

    Grouping on the ordered draw tuple was far too strict: 40 Ryo Hasegawa games gave 40 distinct
    draws and zero collisions, because eight shops drawn with replacement from eight types is 8**8.
    Order does not matter to the economy and neither, mostly, do the names -- two different mixes
    that consume the same products at the same rate are the same town as far as any player can tell.
    `PIZZA_SHOP + BAKERY` and `FARMERS_MARKET + BRUNCH_SPOT` are not identical, but they collide far
    more often than the raw tuple and they collide on the thing that acts.
    """
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG    # noqa: PLC0415
    out = collections.Counter()
    for sname in draw:
        products = KG.SHOPS[sname]
        mult = 2 if len(products) == 1 else 1
        for prod in products:
            out[prod] += mult
    return tuple(sorted(out.items()))


def load_cache(path=CACHE):
    """`[(id, names, draw, actions)]` from `scripts/build_action_cache.py`.

    One pass over the archive instead of one pass PER PLAYER. The uncached version was re-parsing
    858 games x 30 MB for every player asked about -- about 280 GB for an eleven-player sweep, which
    had to be killed.
    """
    if not pathlib.Path(path).exists():
        raise SystemExit("no %s -- run: python -u scripts/build_action_cache.py" % path)
    out = []
    with open(path) as fh:
        for line in fh:
            d = json.loads(line)
            out.append((d["id"], d["names"], tuple(d["draw"]), d["actions"]))
    return out


def as_stream(actions):
    """Hashable per-turn tuples, so comparisons are cheap."""
    return [(tuple(f), tuple(tuple(h) for h in hs), tuple(tuple(o) for o in m))
            for f, hs, m in actions]


def first_divergence(a, b):
    """`(unit_turn, market_turn)` -- the first turn each stream disagrees, or 720 if never."""
    n = min(len(a), len(b))
    u = next((i for i in range(n) if a[i][0] != b[i][0] or a[i][1] != b[i][1]), 720)
    m = next((i for i in range(n) if a[i][2] != b[i][2]), 720)
    return u, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--players", nargs="+", default=None, help="default: every player with >=6 games")
    ap.add_argument("--min-games", type=int, default=6)
    ap.add_argument("--pairs", type=int, default=300)
    args = ap.parse_args()

    games = load_cache()
    by_player = collections.defaultdict(list)
    for _id, names, draw, acts in games:
        for seat, nm in enumerate(names):
            by_player[nm].append((acts[seat], names[1 - seat]))
    players = args.players or [n for n, v in sorted(by_player.items(), key=lambda kv: -len(kv[1]))
                               if len(v) >= args.min_games]

    # **Where does a player's season stop being fixed?** The first shop unlocks at d3 h0 and
    # nothing else changes on that turn, so the `at d3` column is the one that answers "does this
    # player react to the town". Before d3 the town is empty and both boards started identical
    # (`project_kaggriculture_start_state_is_fixed`), so divergence there is the opponent's own d0
    # play -- visible on their board and in the price their sells moved -- or a weed roll at 0.005
    # per empty tile per day. Those two cannot be separated from recordings.
    print("%d games cached, %d players with >=%d games\n" % (len(games), len(players), args.min_games))
    print("%-26s %6s %6s %7s %7s %7s %7s %7s"
          % ("player", "games", "pairs", "<d3", "at d3", "at d4", "at d6", "median"))
    print("-" * 80)
    for name in players:
        rows = by_player[name]
        st = [as_stream(a) for a, _ in rows]
        prs = list(itertools.combinations(range(len(st)), 2))[:args.pairs]
        if not prs:
            continue
        days = [first_divergence(st[i], st[j])[0] // 24 for i, j in prs]
        c, n = collections.Counter(days), len(days)
        print("%-26s %6d %6d %6.0f%% %6.0f%% %6.0f%% %6.0f%% %7d"
              % (name[:26], len(rows), n,
                 100.0 * sum(v for k, v in c.items() if k < 3) / n,
                 100.0 * c.get(3, 0) / n, 100.0 * c.get(4, 0) / n, 100.0 * c.get(6, 0) / n,
                 sorted(days)[n // 2]), flush=True)

    print("\n  at d3 is the town-reaction column: the first shop unlocks on that turn.")
    print("  <d3 is opponent-or-weed and the two cannot be told apart from recordings.")


if __name__ == "__main__":
    main()
