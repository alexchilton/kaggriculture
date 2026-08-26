"""What herd カワシギ actually finishes with, counted off the board in every downloaded seat.

Answers one question: does the leader ever play COW 6 / SHEEP 6?
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.analysis import replay_fills as RF  # noqa: E402

KAWA = "カワシギ"
DIRS = ("downloads_2026-08-13", "downloads_2026-08-14to16", "downloads_2026-08-19",
        "downloads_2026-08-20", "downloads_2026-08-21")


def main():
    tot = collections.Counter()
    n_read = 0
    errs = collections.Counter()
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
                seat = RF.seat_of(r, KAWA)
                if seat is None:
                    continue
                a = RF.animals_alive(r, seat, when=-1)
                c, sh = int(a.get("COW", 0)), int(a.get("SHEEP", 0))
                tot[(c, sh)] += 1
                n_read += 1
            except Exception as e:  # noqa: BLE001
                errs[type(e).__name__] += 1
    print(f"kawa seats read: {n_read}   errors: {dict(errs)}")
    print(f"{'COW/SHEEP':<12}{'games':>7}{'total':>7}")
    for (c, sh), n in sorted(tot.items(), key=lambda kv: -kv[1]):
        print(f"{str(c) + '/' + str(sh):<12}{n:>7}{c + sh:>7}")
    print()
    print("games at COW 6 / SHEEP 6:", tot.get((6, 6), 0))
    print("games at total 12      :", sum(n for (c, s), n in tot.items() if c + s == 12))


if __name__ == "__main__":
    main()
