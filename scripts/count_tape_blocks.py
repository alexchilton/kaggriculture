"""How much do the DOWNLOADED players agree, day by day? The other clones, in the mix.

Alex, 2026-08-20: "and if you include the other clones? into the mix".

`count_day_blocks.py` answers the same question for OUR teacher and finds the opening is nearly a
constant (1 block on d0-d1, 2 on d2-d3) that fragments from d8. This asks it of the 87 downloaded
replays instead, because the tape -- not our planner -- is the better source for an opening block:
the replay reproduces the strong player's board and every op exactly through d11.

`submission/main.py:4887` already records that four tapes agree op-for-op and part at d4 h01. This
measures that claim across everything we have, and reports it two ways:

  ALL SEASONS   every (replay, seat). A player who appears in twenty replays counts twenty times,
                which inflates the top block's share.
  UNIQUE PLAYERS  one season per team name. This is the honest number for "do different people
                play the same opening".

**These downloads are SELECTED LOSSES** (`project_kaggriculture_losing_narrowly`). Never rank the
blocks by outcome here -- the sample cannot support it. What it CAN support is "what does the field
do", which is exactly what an opening library needs.

    python -u scripts/count_tape_blocks.py --dirs data/seed_scripts/top_guys --days 14
"""

import argparse
import collections
import glob
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.count_day_blocks import canonical                    # noqa: E402

TURNS_PER_DAY = 24


def seasons(paths, days, skipped):
    """Yield (player_name, day, block_hash) for every seat of every replay."""
    for p in paths:
        try:
            rep = json.loads(pathlib.Path(p).read_text())
        except Exception as exc:                                  # noqa: BLE001
            print("  skipped %s: %s" % (pathlib.Path(p).name, exc))
            continue
        # **Not every .json in these directories is a replay.** The `<id>-N.json` files are agent
        # LOGS -- a bare list of {"duration", "stdout", "stderr"} per step -- and calling `.get` on
        # one raised AttributeError and took the whole run with it. Identify a replay by the field
        # this script actually needs rather than by filename.
        if not isinstance(rep, dict) or not rep.get("steps"):
            skipped.append(pathlib.Path(p).name)
            continue
        # `info` is a dict on the downloads that came through the Kaggle API, absent on others.
        info = rep.get("info")
        names = info.get("TeamNames") if isinstance(info, dict) else None
        if not names:
            names = ["%s#0" % pathlib.Path(p).stem, "%s#1" % pathlib.Path(p).stem]
        steps = rep.get("steps") or []
        per_seat_day = collections.defaultdict(list)
        for step in steps:
            for seat, cell in enumerate(step):
                obs = cell.get("observation") or {}
                day = int(obs.get("day", 0) or 0)
                if day >= days:
                    continue
                act = cell.get("action")
                if act is None:
                    continue
                per_seat_day[(seat, day)].append(
                    (int(obs.get("hour", 0) or 0), canonical(act)))
        for (seat, day), turns in per_seat_day.items():
            if len(turns) != TURNS_PER_DAY:
                continue
            body = "|".join(a for _h, a in sorted(turns))
            name = names[seat] if seat < len(names) else "seat%d" % seat
            yield ("%s" % name, day, hashlib.md5(body.encode()).hexdigest()[:10])


def table(title, rows, days):
    """rows: day -> Counter[block]"""
    print("\n%s" % title)
    print("%4s %10s %10s %8s %8s" % ("day", "seasons", "distinct", "top", "top3"))
    for day in range(days):
        c = rows.get(day)
        if not c:
            continue
        n = sum(c.values())
        top = c.most_common(3)
        print("%4d %10d %10d %7.1f%% %7.1f%%"
              % (day, n, len(c), 100.0 * top[0][1] / n,
                 100.0 * sum(v for _k, v in top) / n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--days", type=int, default=14)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths += sorted(glob.glob(d.rstrip("/") + "/*.json"))
    if not paths:
        raise SystemExit("no replays under %s" % args.dirs)
    print("replays: %d" % len(paths))

    all_rows = collections.defaultdict(collections.Counter)
    by_player = collections.defaultdict(dict)      # player -> day -> block (first season only)
    players = set()
    skipped = []
    for name, day, block in seasons(paths, args.days, skipped):
        all_rows[day][block] += 1
        players.add(name)
        by_player[name].setdefault(day, block)

    print("not replays, skipped: %d %s"
          % (len(skipped), skipped[:4] + (["..."] if len(skipped) > 4 else [])))
    print("distinct team names: %d" % len(players))

    table("ALL SEASONS (a frequent player counts many times)", all_rows, args.days)

    uniq = collections.defaultdict(collections.Counter)
    for name, per_day in by_player.items():
        for day, block in per_day.items():
            uniq[day][block] += 1
    table("UNIQUE PLAYERS (one season each -- the honest number)", uniq, args.days)

    # How far does the FIELD's most common line run before it breaks up? This is the number that
    # decides how many days an opening block can cover.
    print("\nThe most common block, day by day, over unique players:")
    print("%4s %10s %s" % ("day", "share", "verdict"))
    for day in range(args.days):
        c = uniq.get(day)
        if not c:
            continue
        n = sum(c.values())
        share = c.most_common(1)[0][1] / n
        print("%4d %9.1f%% %s"
              % (day, 100.0 * share,
                 "one block covers the field" if share > 0.8 else
                 "a few blocks would" if share > 0.4 else "no small library fits"))


if __name__ == "__main__":
    main()
