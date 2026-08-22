"""Does any player time their selling, or does everyone sell on a fixed clock?

Alex, 2026-08-21: *"so you are saying there are no reactive agents - so no one is trying to either
time the market or sell negatively adversarially?"*.

Nothing measured so far answers that. `who_is_a_clone_of_whom.py` shows 38 of 58 players share an
OPENING, which says they share code, not that the shared code is unreactive. `is_the_field_open_loop.py`
shows a third of the field re-plans at d3, which is a reaction to the TOWN.

This is a falsification test, and only in one direction. If a player emits their SELL orders at the
same HOURS in every game they play, they cannot be timing the market -- the price path differs
between games and their clock does not. The converse is not proof: sell hours also move because the
goods reached the shed at a different hour, which is a board effect, not a price reaction.

So a high score here means "scripted, definitely not timing". A low score means "not established".

Two quantities per player:

  `hour set match`  the fraction of game PAIRS whose set of selling hours-of-day is identical
  `per-day match`   the same, but requiring the same hours on the same DAY -- much stricter,
                    and the one that distinguishes a fixed daily cadence from a fixed schedule

    python -u scripts/does_anyone_time_the_market.py
"""

import argparse
import collections
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

CACHE = REPO / "data/action_cache.jsonl"
LB = REPO / "data/leaderboard_2026-08-21.json"


def sell_shape(actions):
    """`(hours_of_day_with_a_sell, {day: hours})` for one recorded season."""
    hours, per_day = set(), collections.defaultdict(set)
    for t, (_, _, market) in enumerate(actions):
        for o in market:
            if o and o[0] == "SELL":
                hours.add(t % 24)
                per_day[t // 24].add(t % 24)
                break
    return frozenset(hours), {d: frozenset(v) for d, v in per_day.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-games", type=int, default=6)
    ap.add_argument("--pairs", type=int, default=120)
    args = ap.parse_args()

    if not CACHE.exists():
        raise SystemExit("no %s -- run: python -u scripts/build_action_cache.py" % CACHE)
    lb = json.loads(LB.read_text()) if LB.exists() else {}

    per_player = collections.defaultdict(list)
    with open(CACHE) as fh:
        for line in fh:
            d = json.loads(line)
            for seat, nm in enumerate(d["names"]):
                per_player[nm].append(sell_shape(d["actions"][seat]))

    rows = []
    for nm, shapes in per_player.items():
        if len(shapes) < args.min_games:
            continue
        prs = list(itertools.combinations(range(len(shapes)), 2))[:args.pairs]
        if not prs:
            continue
        same_hours = sum(1 for i, j in prs if shapes[i][0] == shapes[j][0])
        same_daily = 0
        for i, j in prs:
            a, b = shapes[i][1], shapes[j][1]
            days = set(a) | set(b)
            if days and all(a.get(d) == b.get(d) for d in days):
                same_daily += 1
        n = len(prs)
        e = lb.get(nm)
        rows.append((e[0] if e else 99999, nm, len(shapes), 100.0 * same_hours / n,
                     100.0 * same_daily / n, sorted(shapes[0][0])))

    rows.sort()
    print("%d players with >=%d games\n" % (len(rows), args.min_games))
    print("%-26s %5s %6s %11s %11s   %s"
          % ("player", "rank", "games", "hour set", "per-day", "selling hours (one game)"))
    print("-" * 104)
    for rank, nm, n, h, d, hrs in rows[:34]:
        print("%-26s %5s %6d %10.0f%% %10.0f%%   %s"
              % (nm[:26], rank if rank < 99999 else "-", n, h, d,
                 " ".join(map(str, hrs))[:40]))

    print("\n  hour set 100%% = the player sells at the same hours-of-day in every game.")
    print("  per-day 100%% = the same hours on the same days too: a fixed schedule, not a clock.")
    print("  Either at 100%% falsifies market timing for that player. Below 100%% proves nothing")
    print("  on its own -- goods reach the shed at different hours on different boards.")


if __name__ == "__main__":
    main()
