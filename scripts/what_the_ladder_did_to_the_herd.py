"""For a downloaded ladder game: our herd per day, the book we sold into, and who won.

Alex, on a loss: *"i would have thought some of the sheep would die?"* -- which is a question about
what the shipped rule (`router.pays_for_its_ration`) decided on that board, and it is answerable
only from that board's own prices, not from the tape gate.

Prints, for our seat:
    the herd at the last turn of each of the last six days
    WOOL and MILK on the town's book on d27, which is what the rule reads
    what the rule therefore says about a pen holding 0..6 units
    final money, both seats
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import router as RT                                     # noqa: E402

US = "alex chilton"
TPD = 24


def _herd(obs, seat):
    farms = (obs or {}).get("farms") or []
    if seat >= len(farms):
        return collections.Counter()
    c = collections.Counter()
    for row in (farms[seat].get("tiles") or []):
        for t in row:
            if isinstance(t, dict) and t.get("animal"):
                c[t["animal"]] += 1
    return c


def _prices(obs):
    m = (obs or {}).get("market") or {}
    return m.get("prices") or {}


def main(paths):
    for p in paths:
        f = pathlib.Path(p)
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else 0
        opp = 1 - seat
        steps = r.get("steps") or []
        last = (steps[-1][0] or {}).get("observation") or {}
        farms = last.get("farms") or []
        ours = float(farms[seat].get("money", 0)) if seat < len(farms) else 0.0
        theirs = float(farms[opp].get("money", 0)) if opp < len(farms) else 0.0
        print(f"=== {f.stem}   seats {names}   we are seat {seat}")
        print(f"    ours ${ours:,.0f}   theirs ${theirs:,.0f}   "
              f"{'WIN' if ours > theirs else 'LOSS' if ours < theirs else 'DRAW'}")

        print(f"    {'day':>5}{'cows':>6}{'sheep':>7}{'WOOL':>9}{'MILK':>9}{'WHEAT':>8}")
        for day in range(24, 30):
            t = min(day * TPD + TPD - 1, len(steps) - 1)
            obs = (steps[t][0] or {}).get("observation") or {}
            h = _herd(obs, seat)
            pr = _prices(obs)
            print(f"    {day:>5}{h.get('COW',0):>6}{h.get('SHEEP',0):>7}"
                  f"{pr.get('WOOL', float('nan')):>9.0f}{pr.get('MILK', float('nan')):>9.0f}"
                  f"{pr.get('WHEAT', float('nan')):>8.0f}")

        t27 = min(27 * TPD + TPD - 1, len(steps) - 1)
        pr = _prices((steps[t27][0] or {}).get("observation") or {})
        print("    what the rule says at d27 on THIS board:")
        for a, prod in (("SHEEP", "WOOL"), ("COW", "MILK")):
            price = pr.get(prod)
            if price is None:
                print(f"      {a}: no {prod} on the book")
                continue
            verdicts = []
            for held in (0, 2, 4, 6):
                c = {"animal": a, "yield_units": held, "fed_today": False,
                     "consecutive_unfed": 1, "placed_day": 8,
                     "fertilizer_available": False, "cared_today": True}
                verdicts.append(f"{held}:{'fed' if RT.pays_for_its_ration(c, 27, price) else 'DIES'}")
            print(f"      {a:<6} {prod} ${price:>6.0f}   held-> " + "  ".join(verdicts))
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
