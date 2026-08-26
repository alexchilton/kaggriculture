"""Which recording should be the tape for each d3 shop class?

Alex, 2026-08-26: *"if you have a better set that would do better then try the dt and see if there
are improvements"*, after the handover sweep showed the planner beats a MISMATCHED tape and loses to
a matched one -- no yarn all season is +$5,681 for handing over at d12, because the tape we play
there was recorded on a yarn-at-d15 draw and is wrong from early on.

**The tape must be decidable by d3h16**, where the recordings part. That leaves the d3 shop (8
values, 6-22 draws each in `daily_2026-08-26`) and the d3+d6 pair (51 combinations, 11 with four or
more draws). This ranks candidates inside each d3 class so a tape can be chosen per class instead of
seven classes sharing one.

Ranked on the WINNING seat's bank, and both facts are printed:

    won         did that seat beat its opponent -- the ladder is Elo, and a $43k win and a $4k win
                score the same, so a big bank in a LOST game is not a tape worth cloning
    money       the seat's final bank, for separating winners from each other

**These recordings are not a random sample of the ladder.** The older download directories are
selected LOSSES (`project_kaggriculture_losing_narrowly`); how `daily_2026-08-26` was drawn is not
recorded, so treat the win column as descriptive of these files and not as a rate.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24


def final_banks(rep):
    """`[money_seat0, money_seat1]` at the last recorded step."""
    steps = rep.get("steps") or []
    if not steps:
        return []
    obs = (steps[-1][0] or {}).get("observation") or {}
    return [float(f.get("money", 0)) for f in (obs.get("farms") or [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/seed_scripts/daily_2026-08-26")
    ap.add_argument("--top", type=int, default=3, help="candidates to print per class")
    args = ap.parse_args()

    import scripts.breakdown as B

    rows = collections.defaultdict(list)
    for f in sorted(pathlib.Path(args.root).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            rep = json.loads(f.read_text())
            shops = B.recorded_shops(str(f))
        except Exception:                                                      # noqa: BLE001
            continue
        d3 = tuple(sorted(set(shops(3 * TPD) or ())))
        d6 = tuple(sorted(set(shops(6 * TPD) or ())))
        banks = final_banks(rep)
        names = (rep.get("info") or {}).get("TeamNames") or []
        if not d3 or len(banks) < 2 or len(names) < 2:
            continue
        for seat in (0, 1):
            rows[d3[0]].append(dict(file=f.name, seat=seat, team=names[seat],
                                    money=banks[seat], won=banks[seat] > banks[1 - seat],
                                    d6=",".join(x for x in d6 if x not in d3)))

    print(f"{'d3 shop':<16}{'n':>4}  {'wins':>5}   best candidates (won, bank, file, seat)\n")
    for shop in sorted(rows, key=lambda s: -len(rows[s])):
        seats = rows[shop]
        wins = sum(1 for r in seats if r["won"])
        best = sorted(seats, key=lambda r: (not r["won"], -r["money"]))[:args.top]
        print(f"{shop:<16}{len(seats):>4}  {wins:>5}")
        for r in best:
            print(f"{'':<22}{'W' if r['won'] else 'L'}  ${r['money']:>9,.0f}  "
                  f"{r['file']}  seat {r['seat']}  {r['team'][:22]:<22} d6+{r['d6']}")
        print()


if __name__ == "__main__":
    main()
