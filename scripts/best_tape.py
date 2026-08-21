"""Rank one player's own seasons by his own bank, and dump the best as a 30-row schedule.

Alex, 2026-08-21: "the original leaders not so long back really only had 1 optimised tape the whole
way through".

That is what our own shipped agent is -- `_PLAN_JSON` is 30 target rows and it scores 2600 -- and it
is what the winners submit. So before building adaptive selection, take the simplest thing that
could work: ONE of Kawashigi's actual seasons, as rows, through our executor.

**One real game, not the modal row per day.** The modal row for each day comes from a different
game, so stitching them makes a season nobody played: the seed bought on d7 belongs to one line and
the planting on d8 to another. That is the six-marginal decode error at the level of a season. A
single game's rows are coherent by construction.

**Ranked by HIS bank, not by win rate.** These downloads are selected, so a win rate computed on
them is meaningless -- that mistake has been made in this project before. His final money is his
own quantity and is a fair basis for choosing which of his seasons to copy, with the caveat that a
big bank may reflect a weak opponent as much as a strong plan.

    python -u scripts/best_tape.py --player カワシギ --dirs data/seed_scripts/kawashigi ... \\
        --out data/tape_kawa_best.json
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts.extract_target_rows import target_row, TURNS_PER_DAY      # noqa: E402


def season(path, player, days):
    rep = json.loads(pathlib.Path(path).read_text())
    if not isinstance(rep, dict) or not rep.get("steps"):
        return []
    info = rep.get("info")
    names = info.get("TeamNames") if isinstance(info, dict) else None
    if not names or player not in names:
        return []
    rewards = rep.get("rewards") or []

    out = []
    for seat, nm in enumerate(names):
        if nm != player:
            continue
        turns = collections.defaultdict(dict)
        dawn = {}
        for step in rep["steps"]:
            if seat >= len(step):
                continue
            cell = step[seat]
            obs = cell.get("observation") or {}
            day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)
            if day >= days or cell.get("action") is None:
                continue
            turns[day][hour] = cell["action"]
            if hour == 0:
                dawn[day] = obs
        rows = {}
        for day, hh in turns.items():
            if len(hh) != TURNS_PER_DAY or day not in dawn:
                continue
            rows[day] = target_row([hh[h] for h in range(TURNS_PER_DAY)], dawn[day], seat)
        mine = float(rewards[seat]) if seat < len(rewards) and rewards[seat] is not None else None
        theirs = float(rewards[1 - seat]) if len(rewards) > 1 and rewards[1 - seat] is not None \
            else None
        out.append({"game": pathlib.Path(path).stem, "seat": seat,
                    "bank": mine, "opponent_bank": theirs, "rows": rows})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--player", required=True)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    paths = []
    for d in args.dirs:
        paths += sorted(glob.glob(d.rstrip("/") + "/*.json"))

    seasons = []
    for p in paths:
        seasons += season(p, args.player, args.days)
    full = [s for s in seasons if len(s["rows"]) == args.days and s["bank"] is not None]
    print("%s: %d seasons, %d complete with a bank\n" % (args.player, len(seasons), len(full)))
    if not full:
        raise SystemExit("no complete season with a recorded bank")

    # **Money is NOT the key.** The ladder is Elo: a $43k win and a $4k win score identically, and
    # `CLAUDE.md` records that selecting on money is what sent this project wrong before. Ranking
    # by bank picked game 94439800 third -- a season he LOST by $12,024, in a rich economy.
    #
    # So: won games first, and among those the largest margin, which is the closest thing to "this
    # plan beat what it was up against". Bank is printed but never sorted on.
    full.sort(key=lambda s: (s["opponent_bank"] is not None
                             and s["bank"] > s["opponent_bank"],
                             (s["bank"] - (s["opponent_bank"] or 0))), reverse=True)
    won = sum(1 for s in full if s["opponent_bank"] is not None
              and s["bank"] > s["opponent_bank"])
    print("won %d of %d complete seasons in this (SELECTED) sample -- not a win rate\n"
          % (won, len(full)))
    print("%-16s %5s %12s %14s %9s %s"
          % ("game", "seat", "his bank", "opponent bank", "margin", "result"))
    for s in full[:args.top]:
        margin = s["bank"] - (s["opponent_bank"] or 0)
        print("%-16s %5d %12.0f %14.0f %9.0f %s"
              % (s["game"], s["seat"], s["bank"], s["opponent_bank"] or 0, margin,
                 "WON" if margin > 0 else "lost"))

    banks = [s["bank"] for s in full]
    banks.sort()
    mid = banks[len(banks) // 2]
    print("\nhis bank across %d complete seasons: min %.0f  median %.0f  max %.0f"
          % (len(banks), banks[0], mid, banks[-1]))

    best = full[0]
    payload = {"player": args.player, "game": best["game"], "seat": best["seat"],
               "bank": best["bank"], "opponent_bank": best["opponent_bank"],
               "schedule": {str(d): r for d, r in sorted(best["rows"].items())}}
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1))
    print("\nwrote %s  (game %s seat %d, bank %.0f)"
          % (out, best["game"], best["seat"], best["bank"]))
    print("d0 row: %s" % json.dumps(best["rows"][0])[:300])


if __name__ == "__main__":
    main()
