"""How many DISTINCT day-blocks does the teacher actually play, and what selects them?

Alex's hypothesis, 2026-08-20: "i was expecting it to learn big block sequences and maybe 6
different ones over the whole 30 days depending on the shops."

That is a measurable claim, and it decides an architecture before anything is built:

  If a day has a HANDFUL of distinct action blocks, the right model is a block CLASSIFIER --
  pick one of N sequences, emit it whole. Small, exact on d0-d3 by construction, and it matches
  both the teacher (which plans a day once at h0) and the winners (which ship fixed 720-turn
  scripts).

  If a day has hundreds or thousands, no classifier can hold them, and the block has to be
  GENERATED -- an autoregressive decode over the day, or a per-turn policy with memory.

The current BC student is neither: it is memoryless and per-turn, which is why it scatters through
a day whose opening is a constant. See `docs/the_bc_pipeline_2026-08-20.md`.

Run it on the box, where the labels are:

    python -u scripts/count_day_blocks.py --shards /home/alex/labels_r0b

Reads the label jsonl written by `label_games.py`: one row per turn, carrying `seed`, `seat`, the
full `obs` and the teacher's `action`. Rows stream; a shard is 1.2 GB and reading one into a list
is what the OOM killer took sixteen of.
"""

import argparse
import collections
import glob
import hashlib
import json
import pathlib


def canonical(action):
    """A day's action, as a stable string. Order matters -- this is a SEQUENCE, not a set."""
    farmer = action.get("farmer") or []
    hands = action.get("hands") or []
    market = action.get("market") or []
    # Market orders are sorted because slot order is imposed at decode; the teacher's own list
    # order is not meaningful. Unit actions are NOT sorted: slot identity is the unit.
    return json.dumps([farmer, hands, sorted(map(list, market))], sort_keys=True, default=str)


#: **The names this file reads, verified against a real row before anything was measured.**
#: The first version of this script read `row["action"]` and `obs["unlocked_shops"]`. Neither
#: exists. `label_games` writes `act`, and the observation carries `shops`. Both lookups returned
#: their default on every row, so every day hashed to the same empty block and the table said
#: "1 distinct block per day, 1 shop configuration" for all 29 days -- a clean, plausible,
#: completely fabricated result.
#:
#: A row is: {"seed", "seat", "obs", "act"}, and obs is
#: {"day", "farms", "hour", "market", "private", "seat", "shops", "step"}.
ACT_KEY = "act"
SHOPS_KEY = "shops"


def find_shops(obs):
    shops = obs.get(SHOPS_KEY)
    if shops is None:
        raise KeyError("observation has no %r; keys are %s"
                       % (SHOPS_KEY, sorted(obs.keys())))
    # Shops are drawn WITH replacement, so the same shop can appear twice and the multiplicity
    # matters -- sorted tuple, not a set.
    return tuple(sorted(str(s) for s in shops))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", required=True)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--limit-shards", type=int, default=0, help="0 = all")
    args = ap.parse_args()

    paths = sorted(glob.glob(args.shards.rstrip("/") + "/*.jsonl"))
    if args.limit_shards:
        paths = paths[:args.limit_shards]
    if not paths:
        raise SystemExit("no jsonl under %s" % args.shards)

    # (game, day) -> list of (hour, canonical action); flushed per game to keep memory flat.
    per_day_blocks = collections.defaultdict(collections.Counter)   # day -> Counter[block hash]
    per_day_shop_block = collections.defaultdict(collections.Counter)  # day -> (shops, block)
    games = set()
    open_day = {}

    def flush(key):
        (game, day), turns = key, open_day.pop(key)
        if len(turns) != 24:
            return
        body = "|".join(a for _h, a in sorted(turns))
        h = hashlib.md5(body.encode()).hexdigest()[:10]
        per_day_blocks[day][h] += 1
        shops = shops_at.get(key)
        per_day_shop_block[day][(shops, h)] += 1

    # **Print what is being read before counting anything.** An empty action and a missing key
    # look identical in the output table, and the first version of this script produced a full,
    # plausible 29-row table entirely out of `{}`.
    with open(paths[0]) as fh:
        first = json.loads(fh.readline())
    print("row keys: %s" % sorted(first.keys()))
    print("sample %r: %s" % (ACT_KEY, canonical(first[ACT_KEY])[:180]))
    print("sample %r: %r\n" % (SHOPS_KEY, (first.get("obs") or {}).get(SHOPS_KEY)))

    shops_at = {}
    for p in paths:
        with open(p) as fh:
            for line in fh:
                row = json.loads(line)
                obs = row.get("obs") or {}
                day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)
                if day >= args.days:
                    continue
                game = (row.get("seed"), row.get("seat"))
                games.add(game)
                key = (game, day)
                if key not in open_day:
                    open_day[key] = []
                    shops_at[key] = find_shops(obs)
                act = row.get(ACT_KEY)
                if act is None:
                    raise KeyError("label row has no %r; keys are %s"
                                   % (ACT_KEY, sorted(row.keys())))
                open_day[key].append((hour, canonical(act)))
                if len(open_day[key]) == 24:
                    flush(key)
        # A game that straddled the end of a shard leaves a partial day; drop it rather than
        # counting a 17-turn "block" as distinct from the same day played in full.
        for key in [k for k in open_day if len(open_day[k]) < 24]:
            open_day.pop(key, None)
            shops_at.pop(key, None)
        print("  read %s" % pathlib.Path(p).name, flush=True)

    print("\ngames (seed, seat): %d" % len(games))
    print("\n%4s %8s %10s %9s %9s   %s"
          % ("day", "games", "distinct", "top", "top3", "shops seen"))
    for day in range(args.days):
        c = per_day_blocks.get(day)
        if not c:
            continue
        n = sum(c.values())
        top = c.most_common(3)
        shops = {s for s, _h in per_day_shop_block[day]}
        print("%4d %8d %10d %8.1f%% %8.1f%%   %d"
              % (day, n, len(c), 100.0 * top[0][1] / n,
                 100.0 * sum(v for _k, v in top) / n, len(shops)))

    # Does the shop draw SELECT the block? If yes, blocks-per-shop-signature is near 1.
    print("\nIf the shops choose the day, each shop signature maps to ~1 block.")
    print("%4s %14s %16s %s" % ("day", "shop configs", "blocks/config", "verdict"))
    for day in range(args.days):
        pairs = per_day_shop_block.get(day)
        if not pairs:
            continue
        by_shop = collections.defaultdict(set)
        for (shops, h), _n in pairs.items():
            by_shop[shops].add(h)
        if not by_shop:
            continue
        mean = sum(len(v) for v in by_shop.values()) / len(by_shop)
        print("%4d %14d %16.2f %s"
              % (day, len(by_shop), mean,
                 "shops decide it" if mean < 1.5 else "shops do NOT decide it"))


if __name__ == "__main__":
    main()
