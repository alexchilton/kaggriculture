"""SpaTaro's seasons indexed by UNLOCK HISTORY, not by world.

A recorded tape is a legal plan for exactly as long as the town it saw matches the town we
are in. Keying on the world -- the first two shops -- throws away every unlock after the
second, and is circular besides, because our own selling moves the unlocks (§4a of
docs/spataro_architecture_2026-09-11.md).

So the key is the ordered list of (day, shop) unlocks so far. It starts empty and grows, so
the library narrows as the season reveals itself, and a tape that still matches at day 9 is
still a legal plan at day 9.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09"]
OUT = ROOT / "data" / "spataro_unlock_library.json"


def main():
    lib = []
    for d in DIRS:
        for f in sorted((ROOT/d).glob("*.json")):
            if f.name.endswith("summary.json"):
                continue
            r = json.loads(f.read_text())
            if "SpaTaro" not in r["info"]["TeamNames"]:
                continue
            seat = r["info"]["TeamNames"].index("SpaTaro")
            st = r["steps"]
            seen, seq = [], []
            for i, s in enumerate(st):
                for x in ((s[seat]["observation"].get("town") or {}).get("unlocked_shops") or []):
                    if x not in seen:
                        seen.append(x)
                        seq.append([i // 24, x])
            lib.append({"ep": r["info"]["EpisodeId"], "bank": r["rewards"][seat],
                        "unlocks": seq,
                        "stream": [s[seat].get("action") for s in st[1:]]})
    lib.sort(key=lambda x: -x["bank"])
    OUT.write_text(json.dumps(lib, separators=(",", ":")))
    print(f"{len(lib)} seasons indexed by unlock history -> {OUT}")
    print(f"\n{'bank':>10}  unlock history")
    for x in lib[:8]:
        print(f"{x['bank']:>10,.0f}  " + ", ".join(f"d{d}:{s}" for d, s in x["unlocks"]))
    # how many distinct histories, and how much the prefix narrows the field
    from collections import Counter
    for k in (1, 2, 3, 4, 5):
        pref = Counter(tuple(map(tuple, x["unlocks"][:k])) for x in lib)
        print(f"\nafter {k} unlock(s): {len(pref)} distinct prefixes, "
              f"largest group {max(pref.values())}/{len(lib)}")


if __name__ == "__main__":
    main()
