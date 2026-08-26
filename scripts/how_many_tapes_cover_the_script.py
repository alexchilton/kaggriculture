"""How many tapes cover ONE script across every shop draw?

Alex, 2026-08-26: *"not just 1 tape tho for all i mean 1 guy how many unique tapes across all
shops"*.

`data/logs/tape_count.log` found the top of the field is a single published script: five openings
cover 58% of 240 seats, and one of them (`62d81623f9`) is emitted byte-identically by 25 different
names. So the unit to count is not "tapes per player" -- players share them -- it is **how many
distinct openings that script emits over the space of shop draws**, because that is exactly how many
recordings we would have to capture to reproduce it.

カワシギ needs FOUR: only two bits of the board change what he does, melon-count >= 9 at d3 and the
yarn store at d5, and four tapes cover all four arms (`project_kaggriculture_only_two_bits_vary`).

This asks the same question of the clone script:

    signature -> opening   for each shop draw, which opening(s) the script emits. A draw that maps
                           to exactly one opening is a branch we could capture with one recording.
                           A draw that maps to several means something OTHER than the shops selects
                           it, and that bit has to be found before a tape set is complete.
    coverage               how many recordings it would take to cover N% of observed seats.

The shop signature is the full unlock ORDER, not just the yarn day -- the yarn day was enough to
show the herd flip but it cannot distinguish two draws that differ in what came before it.
"""

import collections
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
NEW = "data/seed_scripts/daily_2026-08-26"
OPEN_TO = 11
#: The five openings that carry 58% of the field, from `data/logs/tape_count.log`.
SCRIPT = {"d1f515b59d", "62d81623f9", "356835aca0", "123c42fb5d", "d198b9f673"}


def stream_hash(replay, seat, last_day=OPEN_TO):
    parts = []
    for t, step in enumerate(replay.get("steps") or []):
        if t // TPD > last_day or seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        parts.append("|".join("-".join(str(x) for x in o) if o else "." for o in ops))
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()[:10]


def shops(replay, upto_day=12):
    order = []
    for t in range(0, len(replay.get("steps") or []), TPD):
        if t // TPD > upto_day:
            break
        cur = list((((replay["steps"][t][0] or {}).get("observation") or {}).get("town")
                    or {}).get("unlocked_shops") or [])
        while len(order) < len(cur):
            order.append(cur[len(order)])
    return tuple(order)


def short(sig):
    return ">".join(s[:4] for s in sig) or "(none)"


def main():
    seats = []
    for f in sorted(pathlib.Path(NEW).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        sig = shops(r)
        last = (r["steps"][-1][0] or {}).get("observation") or {}
        farms = last.get("farms") or []
        for seat in range(min(2, len(names))):
            if seat >= len(farms):
                continue
            seats.append(dict(name=names[seat], ep=f.stem, h=stream_hash(r, seat),
                              sig=sig, money=float(farms[seat].get("money", 0))))

    script = [s for s in seats if s["h"] in SCRIPT]
    print(f"{len(seats)} seats total; {len(script)} run the shared script "
          f"({100*len(script)/len(seats):.0f}%)\n")

    by_sig = collections.defaultdict(collections.Counter)
    for s in script:
        by_sig[s["sig"]][s["h"]] += 1
    print("--- shop draw -> opening, for the shared script")
    print(f"   {'draw (unlock order to d12)':<44}{'seats':>6}  openings")
    clean = ambiguous = 0
    for sig, hs in sorted(by_sig.items(), key=lambda kv: -sum(kv[1].values())):
        n = sum(hs.values())
        tag = "  ".join(f"{h}x{c}" for h, c in hs.most_common())
        if len(hs) == 1:
            clean += n
        else:
            ambiguous += n
        print(f"   {short(sig):<44}{n:>6}  {tag}")
    print()
    print(f"   draws mapping to exactly ONE opening: {clean} seats")
    print(f"   draws mapping to SEVERAL:             {ambiguous} seats")
    print()

    print("--- and the reverse: which draws each opening covers")
    by_h = collections.defaultdict(list)
    for s in script:
        by_h[s["h"]].append(s)
    for h, rows in sorted(by_h.items(), key=lambda kv: -len(kv[1])):
        sigs = collections.Counter(short(r["sig"]) for r in rows)
        m = [r["money"] for r in rows]
        print(f"   {h}  {len(rows):>3} seats  mean ${sum(m)/len(m):>9,.0f}  "
              f"{len(sigs)} distinct draw(s)")
        for sg, c in sigs.most_common(4):
            print(f"        x{c:<3} {sg}")
    print()

    print("--- how many recordings to cover the observed field")
    counts = collections.Counter(s["h"] for s in seats)
    total, run = len(seats), 0
    for i, (h, c) in enumerate(counts.most_common(12), 1):
        run += c
        print(f"   {i:>2} tape(s): {100*run/total:>5.1f}% of seats   (+{h} {c})")


if __name__ == "__main__":
    main()
