"""Who actually appears in the downloaded replays, and how many DISTINCT episodes there are.

Written because `kawa_herd_counts.py` reported 1291 kawa seats from a set Alex believes holds ~35
games. Counting files is not counting games: the same episode can be downloaded on several days,
and `seat_of` returning a seat is not proof the name matched.
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
    names = collections.Counter()
    per_dir = collections.Counter()
    kawa_ids = set()
    all_ids = set()
    seatless = 0
    errs = collections.Counter()
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
            except Exception as e:  # noqa: BLE001
                errs[type(e).__name__] += 1
                continue
            ep = f.stem
            all_ids.add(ep)
            # Every name the replay carries, however it stores them.
            info = r.get("info") or {}
            tn = info.get("TeamNames") or r.get("TeamNames") or []
            for n in tn:
                names[n] += 1
            seat = RF.seat_of(r, KAWA)
            if seat is None:
                seatless += 1
            else:
                kawa_ids.add(ep)
                per_dir[d] += 1

    print("distinct episode ids across the 5 dirs :", len(all_ids))
    print("episodes where seat_of finds kawa      :", len(kawa_ids))
    print("files with NO kawa seat                :", seatless)
    print("errors                                 :", dict(errs))
    print()
    print("kawa episodes per dir:")
    for d in DIRS:
        print(f"  {d:<28}{per_dir.get(d, 0):>6}")
    print()
    print("top 25 TeamNames seen (name, files):")
    for n, c in names.most_common(25):
        print(f"  {c:>6}  {n}")


if __name__ == "__main__":
    main()
