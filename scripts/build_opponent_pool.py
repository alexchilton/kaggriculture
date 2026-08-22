"""Who is in the archive, and which of their games is worth putting opposite the replay.

Alex, 2026-08-21: *"i want the tomato and the carrot tested against all seeds we have and get a
larger opponent pool including tets and ryo"*, *"and any others in the top top you downloaded
today"*.

Every sweep so far has held the opponent at ONE fixed replay -- Yusuke Hayashi, seat 1 of
`92498144.json`. That is a problem beyond sample size: `melon_branch` arms off the OPPONENT's melon
tile count at d3, so a fixed opponent can pin the agent to a single tape branch for every run in
the sweep.

This walks the archives, groups by player, and prints a pool: one game per player, chosen as their
MEDIAN game rather than their best. The archive is a selected sample -- Alex downloads losses -- so
a max-bank pick would systematically choose each player's luckiest town, and the pool would be a
row of outliers rather than a field.

    python -u scripts/build_opponent_pool.py
    python -u scripts/build_opponent_pool.py --write kagg/search/opponent_pool.json
"""

import argparse
import collections
import json
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ROOT = REPO / "data/seed_scripts"

#: Archives worth walking. `downloads_2026-08-14to16` is excluded: it predates the 2026-08-15
#: balance change, so those games were played on a different economy (see `CLAUDE.md`).
DIRS = ("downloads_2026-08-20", "downloads_2026-08-19", "leaders_2026-08-19",
        "top_guys", "ryo", "tetsuya", "tetsuya_93866112", "top2", "new_leader",
        "ladder_2026-08-17b", "field_leaders")


def final_banks(game):
    """`[money_seat0, money_seat1]` or `None`. Defensive: the archives are not one shape.

    Some recordings put the observation on `steps[-1][0]`, some carry a seat entry that is a bare
    list, and a truncated download has no farms at all. A scan that assumes one shape drops whole
    directories silently, which is how a pool ends up being three players.
    """
    steps = game.get("steps") or []
    for frame in reversed(steps):
        if not isinstance(frame, list) or not frame:
            continue
        for seat in frame:
            if not isinstance(seat, dict):
                continue
            farms = (seat.get("observation") or {}).get("farms") or []
            if len(farms) >= 2 and all(isinstance(f, dict) for f in farms[:2]):
                return [int(farms[i].get("money", 0) or 0) for i in range(2)]
    return None


def melon_at_d3(game, seat):
    """The player's MELON tile count at the d3 dawn -- the number that picks OUR season.

    `melon_branch` arms when the opponent shows `OPPONENT_MELON` melon tiles at d3, and arming it
    switches the whole replay from his melon season to his strawberry one. So an opponent pool
    picked on bank alone can leave a branch of our own agent untested: measured 2026-08-21, holding
    the opponent at Yusuke Hayashi (5 melon) made the strawberry tape unreachable across 96 runs.
    This is the field that has to be spanned, not the bank.
    """
    steps = game.get("steps") or []
    idx = 3 * 24
    if idx >= len(steps) or not isinstance(steps[idx], list) or not steps[idx]:
        return None
    farms = ((steps[idx][0] or {}).get("observation") or {}).get("farms") or []
    if len(farms) <= seat or not isinstance(farms[seat], dict):
        return None
    return sum(1 for row in (farms[seat].get("tiles") or []) for t in row
               if isinstance(t, dict) and t.get("crop") == "MELON")


def scan(dirs):
    """`{player: [(bank, path, seat)]}` across every readable game in `dirs`."""
    seats, n, bad = collections.defaultdict(list), 0, 0
    for dn in dirs:
        d = ROOT / dn
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            try:
                game = json.loads(p.read_text())
            except Exception:
                bad += 1
                continue
            # `tetsuya/` holds a `schedule.json` and a `tape.json` beside its recordings, and both
            # are lists. A scan that assumes every `.json` under a tape directory is a game dies on
            # the first one.
            if not isinstance(game, dict):
                bad += 1
                continue
            names = (game.get("info") or {}).get("TeamNames") or []
            banks = final_banks(game)
            if len(names) < 2 or banks is None:
                bad += 1
                continue
            n += 1
            for i, nm in enumerate(names[:2]):
                seats[nm].append((banks[i], str(p.relative_to(REPO)), i))
    return seats, n, bad


def pool(seats, min_games, top):
    """One game per player -- the MEDIAN one, not the best. See the module docstring."""
    out = []
    for nm, v in seats.items():
        if len(v) < min_games:
            continue
        v = sorted(v)
        med = v[len(v) // 2]
        out.append((statistics.median([b for b, _, _ in v]), nm, len(v), med))
    out.sort(reverse=True)
    return out[:top]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-games", type=int, default=2)
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--write", default=None, help="write the pool as JSON to this path")
    ap.add_argument("--dirs", nargs="+", default=list(DIRS))
    args = ap.parse_args()

    seats, n, bad = scan(args.dirs)
    print("scanned %d games, %d unreadable, %d distinct players\n" % (n, bad, len(seats)))
    rows = pool(seats, args.min_games, args.top)
    print("%-32s %6s %10s %7s  %-24s %s"
          % ("player", "games", "median", "melon@d3", "median game", "seat"))
    print("-" * 96)
    payload = []
    for med, nm, cnt, (bank, path, seat) in rows:
        try:
            m = melon_at_d3(json.loads((REPO / path).read_text()), seat)
        except Exception:
            m = None
        print("%-32s %6d %10d %7s  %-24s %d"
              % (nm[:32], cnt, med, "-" if m is None else m, pathlib.Path(path).name, seat))
        payload.append({"name": nm, "games": cnt, "median_bank": int(med),
                        "melon_at_d3": m, "replay": path, "seat": seat})

    if args.write:
        pathlib.Path(args.write).write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\nwrote %d opponents to %s" % (len(payload), args.write))


if __name__ == "__main__":
    main()
