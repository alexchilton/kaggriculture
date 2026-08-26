"""Scan seeds for their shop-unlock fingerprint, then use it two ways.

Written because two questions got answered "not possible" when both are a scan away:

1. **"The yarn-store branch is untested."** `gain_from_waiting` treats WOOL as worthless to hold
   when no `YARN_STORE` was drawn and valuable when one was, and neither tape seed drew one -- so
   half the branch has never executed. Seeds that draw a yarn store are not rare and not hidden;
   they are findable by scanning, exactly like the CARROT drain buckets.

2. **"The losing ladder games carry `configuration.seed = None`, so they cannot be replayed."**
   True that the field is empty. Not true that the seed is unrecoverable: the unlock SEQUENCE plus
   its timing is a fingerprint, and `_maybe_unlock_shop` draws from the same seeded RNG every game.
   Scan seeds, fingerprint each, and match against the recorded games.

The board start state is identical on every game (`docs`: all 78 replays start on the same board,
NW only, $3,000, no shops), so the only things a seed decides are the shop draw, the unlock timing
and the weeds. That is what makes the fingerprint discriminating and cheap.

Both players PASS for the whole scan. Shop unlocks are driven by the town, not by our play, so a
PASS game gives the same draw far faster than driving the real agent. `--verify` re-runs a handful
of matched seeds against the recorded sequence to confirm that assumption rather than trusting it.

**WRONG, AND THIS WHOLE SCRIPT'S OUTPUT IS VOID. Measured 2026-08-25.**

The PASS assumption in the paragraph above is false, `--verify` was described but never written, and
`scripts/find_the_yarn_seeds.py` had already recorded the reason in its own docstring before this
was written.

`_end_of_day` builds ONE `random.Random((seed * 1_000_003) ^ day)` per day
(`reference/kaggriculture.py:871`). It calls `_spawn_weeds` for **both** farms and only then draws
the shop. `_spawn_weeds` calls `rng.random()` only where `farm["tiles"][y][x] is None`
(`:836-840`), so the number of draws consumed before the shop choice depends on how much land each
player owns and how much of it is planted. Play moves the stream; the shop draw moves with it.

Measured, PASS game vs our live agent against `contrarian`, first three unlocks:

```
  seed   PASS                                       REAL
   700   SMOOTHIE, SMOOTHIE, SMOOTHIE               BRUNCH_SPOT, FARMERS_MARKET, ICE_CREAM
   701   FARMERS_MARKET, PET_CAFE, FARMERS_MARKET   PIZZA_SHOP, YARN_STORE, FARMERS_MARKET
   702   BAKERY, SMOOTHIE, ICE_CREAM                PET_CAFE, YARN_STORE, ICE_CREAM
   258   YARN_STORE, SMOOTHIE, BRUNCH_SPOT          PIZZA_SHOP, ICE_CREAM, ICE_CREAM
   127   SMOOTHIE, FARMERS_MARKET, FARMERS_MARKET   PIZZA_SHOP, YARN_STORE, YARN_STORE
```

0 of 5 match. So the "24 of 35 recorded games matched to a seed" table and the "127 of 400 seeds
draw a yarn store" count are both meaningless. Nothing downstream of them stands.

**The method that would actually work.** A recorded game contains BOTH players' action streams, so
replay both of them under a candidate seed and compare the unlock sequence. That reproduces the
exact tile occupancy the real game had, which is what the RNG consumption depends on. It costs one
full season per (seed, game) instead of one PASS game per seed, which is why this shortcut looked
attractive. It is not implemented.

For yarn-store seeds specifically, use `scripts/find_the_yarn_seeds.py`, which plays real agents
and stops at d7.
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
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}


def fingerprint_of_seed(seed, days=12):
    """(shop, day) pairs in unlock order, for a PASS game on this seed."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    seen, seq = set(), []
    for t in range(days * TPD):
        o = env.state[0].observation
        for s in ((o.get("town") or {}).get("unlocked_shops") or []):
            key = (s, len([x for x in seq if x[0] == s]))
            if key not in seen:
                seen.add(key)
                seq.append((s, t // TPD))
        env.step([PASS_ACTION, PASS_ACTION])
        if env.done:
            break
    return tuple(seq)


def fingerprint_of_game(path, days=12):
    rec = json.loads(pathlib.Path(path).read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    if US not in names:
        return None, None
    me = names.index(US)
    seen, seq = set(), []
    for t, st in enumerate(rec["steps"]):
        if t // TPD >= days:
            break
        o = st[0].get("observation") or {}
        for s in ((o.get("town") or {}).get("unlocked_shops") or []):
            key = (s, len([x for x in seq if x[0] == s]))
            if key not in seen:
                seen.add(key)
                seq.append((s, t // TPD))
    last = rec["steps"][-1]
    farms = (last[0].get("observation") or {}).get("farms") or []
    margin = (float(farms[me]["money"]) - float(farms[1 - me]["money"])) if len(farms) > 1 else 0.0
    return tuple(seq), margin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first", type=int, default=0)
    ap.add_argument("--count", type=int, default=400)
    ap.add_argument("--days", type=int, default=12)
    ap.add_argument("--out", default="data/logs/seed_fingerprints.json")
    args = ap.parse_args()

    # ---- the recorded games we want to find --------------------------------------------
    games = {}
    for f in sorted(glob.glob(str(pathlib.Path.home() / "Downloads" / "*.json"))):
        fp, margin = fingerprint_of_game(f, args.days)
        if fp:
            games[pathlib.Path(f).stem] = (fp, margin)
    print(f"recorded games with our seat: {len(games)}", flush=True)

    # ---- scan ---------------------------------------------------------------------------
    table = {}
    yarn = []
    matches = collections.defaultdict(list)
    for i in range(args.first, args.first + args.count):
        fp = fingerprint_of_seed(i, args.days)
        table[i] = [[s, d] for s, d in fp]
        if any(s == "YARN_STORE" for s, _d in fp):
            yarn.append(i)
        for name, (gfp, _m) in games.items():
            if gfp and fp[:len(gfp)] == gfp:
                matches[name].append(i)
        if (i - args.first + 1) % 50 == 0:
            print(f"  scanned {i - args.first + 1}/{args.count}  "
                  f"yarn-store seeds so far {len(yarn)}  matched games {len(matches)}", flush=True)

    pathlib.Path(args.out).write_text(json.dumps(table))
    print(f"\nwrote {args.out}")
    print(f"seeds scanned            {args.count}")
    print(f"seeds drawing YARN_STORE {len(yarn)}  ({100.0 * len(yarn) / max(1, args.count):.0f}%)")
    print(f"  first twenty: {yarn[:20]}")
    print(f"\nrecorded games matched to a seed: {len(matches)}")
    for name, seeds in sorted(matches.items()):
        print(f"  {name:<14} -> {seeds[:5]}{' ...' if len(seeds) > 5 else ''}  "
              f"margin {games[name][1]:+,.0f}")
    if not matches:
        print("  none in this range -- the fingerprint is unique enough to need a wider scan,")
        print("  or unlock timing depends on play and the PASS assumption is wrong. Widen with")
        print("  --first/--count before concluding either.")


if __name__ == "__main__":
    main()
