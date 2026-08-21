"""Does any recorded player actually use TOMATO or GOOSE, and does it pay?

Alex, 2026-08-21: *"and what about finding tomatoes or geese?"*

The library approach only reaches a strategy somebody RECORDED. `REPLAY_OPENING_TAPE` holds four
カワシギ seasons and they are melon or strawberry; if no downloaded seat plays tomato or geese well,
there is nothing to add a fifth tape from, and the question is closed by absence rather than by
argument.

Two prior results make this worth re-asking rather than assuming:

  `SELLABLE` blocked CARROT, TOMATO and EGG from being sold **at all** for part of this project's
  life, which invalidated four carrot arms and the goose verdict. Any negative measured in that
  window is void.

  Geese were switched off on the measured ground that they lose to the mirror and to the field --
  but that is a statement about OUR goose play, not about whether a top seat profits from them.

Counts every op and market order naming the token, per seat, and sorts by the seat's final bank.
Reads the whole replay tree, which is ~30 MB a file, so it is slow by design and writes a log.

    python -u scripts/who_plays_tomato_or_geese.py --out data/logs/tomato_geese.log
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TOKENS = ("TOMATO", "GOOSE", "CARROT", "EGG")


def seats(path):
    """`(bank, team, op_counts)` for both seats of one recording, or nothing if it will not parse."""
    try:
        d = json.loads(path.read_text())
        names, steps = d["info"]["TeamNames"], d["steps"]
    except Exception:
        return
    if not steps or len(names) < 2:
        return
    for seat in (0, 1):
        last = steps[-1][seat] if seat < len(steps[-1]) else None
        farms = ((last or {}).get("observation") or {}).get("farms") or []
        if len(farms) <= seat:
            continue
        ops = collections.Counter()
        for s in steps[1:]:
            a = ((s[seat] if seat < len(s) else None) or {}).get("action") or {}
            for x in [a.get("farmer")] + list(a.get("hands") or []):
                if x and len(x) > 1:
                    ops[str(x[1])] += 1
            for m in (a.get("market") or []):
                if len(m) > 1:
                    ops[str(m[1])] += 1
        yield (farms[seat].get("money") or 0, str(names[seat]), ops)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/seed_scripts")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    rows = []
    for p in sorted(pathlib.Path(args.root).rglob("*.json")):
        if p.name == "schedule.json":
            continue
        for bank, team, ops in seats(p) or ():
            rows.append((bank, team, p.parent.name + "/" + p.stem,
                         tuple(ops[t] for t in TOKENS)))
    rows.sort(reverse=True)

    print("%10s  %-20s %-32s %s" % ("bank", "team", "game",
                                    "".join("%8s" % t for t in TOKENS)))
    print("-" * 104)
    hits = [r for r in rows if r[3][0] or r[3][1]]
    for bank, team, game, counts in hits[:args.top]:
        print("%10.0f  %-20s %-32s %s"
              % (bank, team[:20], game, "".join("%8d" % c for c in counts)))

    print("\n%d of %d seats touch TOMATO or GOOSE at all" % (len(hits), len(rows)))
    if hits:
        print("best bank among them          %10.0f" % hits[0][0])
    clean = [r[0] for r in rows if not r[3][0] and not r[3][1]]
    if clean:
        print("best bank touching neither    %10.0f" % max(clean))


if __name__ == "__main__":
    main()
