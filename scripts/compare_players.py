"""Are two players playing the same game? Op profile per day, straight off the action streams.

No simulation. Counts what each player SUBMITTED per day, which is enough to tell a clone from a
different strategy -- routing differs in the ops, the cadence differs in the hours.

    python -u scripts/compare_players.py --dir data/seed_scripts/downloads_2026-08-20
    python -u scripts/compare_players.py --dir <d> --players tetsuya "Ryo Hasegawa"

An op count is an INTENTION, not a landing (`docs/README.md`, and the offers-are-not-fills rule):
a submitted PLANT with no seed does nothing. That is fine here -- the question is what the player
is TRYING to do, and two agents with the same intent profile are running the same strategy.
Market rows are deliberately omitted for that reason: the agent re-posts each order every turn, so
counting them measures re-posting, not trading.
"""
import argparse
import collections
import json
import pathlib

UNIT_OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "FERTILIZE",
            "DIG", "BUILD_PASTURE", "BUILD_COOP", "PLACE_ANIMAL", "PICKUP", "DROP", "PASS")
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")


def profile(path, last_day):
    """{team: {day: Counter(op)}} plus {team: games} for one replay file."""
    d = json.loads(path.read_text())
    names = (d.get("info") or {}).get("TeamNames") or []
    out = {}
    for seat, team in enumerate(names):
        per = collections.defaultdict(collections.Counter)
        for i, step in enumerate(d.get("steps") or []):
            if i == 0:
                continue
            prev = (d["steps"][i - 1][seat] or {}).get("observation") or {}
            day = int(prev.get("day", 0) or 0)
            if day > last_day:
                break
            act = (step[seat] or {}).get("action") or {}
            for u in [act.get("farmer")] + list(act.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                per[day][op if op not in MOVES else "move"] += 1
        out[str(team)] = per
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--last-day", type=int, default=10)
    ap.add_argument("--players", nargs="*", default=None)
    ap.add_argument("--min-games", type=int, default=2)
    args = ap.parse_args()

    agg = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    games = collections.Counter()
    for f in sorted(pathlib.Path(args.dir).glob("*.json")):
        try:
            got = profile(f, args.last_day)
        except Exception:
            continue
        for team, per in got.items():
            games[team] += 1
            for day, c in per.items():
                agg[team][day].update(c)

    who = args.players or [t for t, n in games.most_common() if n >= args.min_games]
    who = [t for t in who if t in agg]
    if not who:
        print("no players with >= %d games in %s" % (args.min_games, args.dir))
        print("teams present: %s" % dict(games.most_common(20)))
        return

    ops = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "PASS", "move")
    print("Mean ops per day, d0-d%d. '%s'\n" % (args.last_day, args.dir))
    for team in who:
        n = games[team]
        print("== %s   (%d games)" % (team, n))
        print("   %-4s %s" % ("day", " ".join("%9s" % o[:9] for o in ops)))
        for day in range(args.last_day + 1):
            c = agg[team][day]
            print("   %-4d %s" % (day, " ".join("%9.1f" % (c[o] / n) for o in ops)))
        print()

    if len(who) >= 2:
        a, b = who[0], who[1]
        na, nb = games[a], games[b]
        print("DIFFERENCE  %s  minus  %s   (mean ops/day)" % (a, b))
        print("   %-4s %s" % ("day", " ".join("%9s" % o[:9] for o in ops)))
        tot = 0.0
        for day in range(args.last_day + 1):
            ca, cb = agg[a][day], agg[b][day]
            row = [ca[o] / na - cb[o] / nb for o in ops]
            tot += sum(abs(v) for v in row)
            print("   %-4d %s" % (day, " ".join("%+9.1f" % v for v in row)))
        print("\n   total absolute difference: %.1f ops/day summed over d0-d%d" % (tot, args.last_day))
        print("   (near 0 = same strategy or a clone; tens = a different game)")


if __name__ == "__main__":
    main()
