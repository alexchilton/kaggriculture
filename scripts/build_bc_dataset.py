"""Extract a teacher's turns as BC labels, with the market as ONE bundle token.

    python -u scripts/build_bc_dataset.py --team tetsuya \
        --dirs data/seed_scripts/downloads_2026-08-20 data/seed_scripts/downloads_2026-08-19 \
        --out data/il/tetsuya_bundles.npz

**Why this exists beside `kagg.il.replays.encode_action`.** That function emits the nine independent
market heads, and two things are wrong with them for this purpose:

1. **`hire` is binary** (`replays.py:110`, `hire = np.int32(1)`). The teacher hires SEVEN hands in a
   single turn 271 times; the label records "1". The bundle that funds a crew from the same turn's
   sells is therefore not representable, and a clone that fit these labels perfectly would still
   never hire seven hands. `buy_land` has the same shape.
2. **Nine marginals are not a joint.** 80.7% of the teacher's turns carry no market action, so every
   marginal's base rate is overwhelmingly "no" and their product is "certainly no" -- which is the
   measured zero-orders-under-argmax result in CLAUDE.md.

Both are fixed by treating the whole market list as one symbol. See `kagg/il/bundles.py`.

The unit heads from `encode_action` are kept as they are: a unit's op IS a per-unit decision, the
units are spatially separable, and nothing there is being asked to coordinate.

**Observation features are deliberately NOT built here.** `kagg/il/bc.py` already routes them
through `adapter.state_from_obs` and the same `jax_obs.encode` the policy trains on, for the reason
`adapter.py` gives at length -- a second encoder is a thing that must agree forever and will not.
This script emits labels, the vocabulary, and the clock baseline; training reads features through
the existing path.
"""

import argparse
import collections
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.il import bundles as B                                    # noqa: E402


def seat_of(replay, team):
    names = [str(n) for n in ((replay.get("info") or {}).get("TeamNames") or [])]
    return names.index(team) if team in names else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--coverage", type=float, default=0.985)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths.extend(sorted(pathlib.Path(d).glob("*.json")))
    print("scanning %d replay files for %r" % (len(paths), args.team), flush=True)

    vocab, stats = B.build_vocabulary(paths, args.team, coverage=args.coverage)
    index = {b: i for i, b in enumerate(vocab)}
    print("  turns %d   distinct bundles %d   kept %d for %.1f%% coverage"
          % (stats["turns"], stats["distinct"], stats["kept"], 100 * stats["coverage"]),
          flush=True)

    days, hours, tokens, games = [], [], [], 0
    oov = 0
    banks = []
    for p in paths:
        try:
            d = json.loads(p.read_text())
        except Exception:                                           # noqa: BLE001
            continue
        seat = seat_of(d, args.team)
        if seat is None:
            continue
        games += 1
        rewards = [(q.get("reward") or 0.0) for q in (d.get("steps") or [[]])[-1]]
        banks.append(rewards[seat] if seat < len(rewards) else 0.0)
        steps = d.get("steps") or []
        for i, step in enumerate(steps):
            if i == 0:
                continue
            prev = (steps[i - 1][seat] or {}).get("observation") or {}
            if "day" not in prev:
                continue
            act = (step[seat] or {}).get("action") or {}
            b = B.bundle_of(act)
            tok = index.get(b)
            if tok is None:
                oov += 1
                tok = index[B.EMPTY] if B.EMPTY in index else 0
            days.append(int(prev.get("day", 0) or 0))
            hours.append(int(prev.get("hour", 0) or 0))
            tokens.append(tok)

    days = np.asarray(days, dtype=np.int16)
    hours = np.asarray(hours, dtype=np.int16)
    tokens = np.asarray(tokens, dtype=np.int32)

    base = B.clock_baseline(paths, args.team)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out, day=days, hour=hours, bundle=tokens,
        vocab=np.array([json.dumps(list(b)) for b in vocab], dtype=object),
        team=args.team, games=games,
        baseline=json.dumps(base), stats=json.dumps(stats))

    print("\n%s   %d games, %d turns, %d classes  (OOV %d = %.2f%%)"
          % (out, games, len(tokens), len(vocab), oov, 100 * oov / max(1, len(tokens))))
    print("  teacher final bank: mean $%,.0f   min $%,.0f   max $%,.0f"
          .replace("%,", "%") % (np.mean(banks), np.min(banks), np.max(banks)) if banks else "")
    print("\nGATE -- a clone must beat the clock-only lookup table, not raw accuracy.")
    print("  a model that always predicts EMPTY scores %.1f%% and is the $3,000 do-nothing policy"
          % (100 * stats["empty_rate"]))
    print("  market, NON-EMPTY turns : beat %.1f%%   (H=%.3f bits over %d turns)"
          % (100 * base["market_nonempty"], base["H_nonempty_given_clock"],
             base["market_nonempty_turns"]))
    print("  farmer op               : beat %.1f%%   (H=%.3f bits)"
          % (100 * base["farmer_op"], base["H_farmer_given_clock"]))
    print("  non-empty market rate   : match %.1f%%" % (100 * stats["nonempty_rate"]))

    top = collections.Counter(tokens.tolist()).most_common(6)
    print("\nmost frequent bundles:")
    for t, n in top:
        print("  %6d  %5.1f%%  %s"
              % (n, 100 * n / len(tokens), ", ".join("%s %s" % o for o in vocab[t]) or "(empty)"))


if __name__ == "__main__":
    main()
