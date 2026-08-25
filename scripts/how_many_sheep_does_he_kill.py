"""How many sheep does カワシギ let go, and does he keep the pen or the animal?

Alex: "he doesnt kill everyone just a few - find the number".

Two counts, per seat:

    placed      PLACE ops for each species -- what he owned. A unit op, emitted once.
    alive       what stands at the bell.
    lost        placed - alive, per species.

`BUY_ANIMAL` is a market order and is re-posted every turn, so it overcounts and is not used
(`feedback_offers_are_not_fills`).

The distribution matters more than the mean here: "he kills 2.8 sheep" is a number nothing does if
the real behaviour is "2 sheep in the common case and 6 in a big-herd case".
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

KAWA = "カワシギ"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")
SPECIES = ("COW", "SHEEP")


def main():
    lost_sheep = collections.Counter()
    lost_cow = collections.Counter()
    by_placed = collections.defaultdict(list)
    kept_share = []
    n = 0
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json")):
            try:
                r = json.loads(f.read_text())
            except Exception:  # noqa: BLE001
                continue
            if not isinstance(r, dict):
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            seat = names.index(KAWA)
            n += 1
            pl = collections.Counter()
            for step in r.get("steps") or []:
                if seat >= len(step):
                    continue
                act = (step[seat] or {}).get("action") or {}
                for op in [act.get("farmer")] + list(act.get("hands") or []):
                    if op and len(op) >= 2 and op[0] == "PLACE" and op[1] in SPECIES:
                        pl[op[1]] += 1
            farms = ((r["steps"][-1][0] or {}).get("observation") or {}).get("farms") or []
            al = collections.Counter()
            if seat < len(farms):
                for row in (farms[seat].get("tiles") or []):
                    for t in row:
                        if isinstance(t, dict) and t.get("animal"):
                            al[t["animal"]] += 1
            ls = pl["SHEEP"] - al["SHEEP"]
            lc = pl["COW"] - al["COW"]
            lost_sheep[ls] += 1
            lost_cow[lc] += 1
            by_placed[pl["SHEEP"]].append(ls)
            if pl["SHEEP"]:
                kept_share.append(al["SHEEP"] / pl["SHEEP"])

    print(f"kawa post-change seats: {n}", flush=True)
    print()
    print("SHEEP LET GO PER SEAT")
    print(f"  {'lost':>5}{'seats':>7}   share")
    for k in sorted(lost_sheep):
        print(f"  {k:>5}{lost_sheep[k]:>7}   {100.0 * lost_sheep[k] / n:>5.1f}%")
    tot = sum(k * v for k, v in lost_sheep.items())
    print(f"  mean {tot / n:.2f} sheep per seat")
    print()
    print("COWS LET GO PER SEAT")
    for k in sorted(lost_cow):
        print(f"  {k:>5}{lost_cow[k]:>7}   {100.0 * lost_cow[k] / n:>5.1f}%")
    print()
    print("HOW MANY HE LETS GO, BY HOW MANY HE PLACED")
    print(f"  {'placed':>7}{'seats':>7}{'mean lost':>11}{'mean kept':>11}")
    for placed in sorted(by_placed):
        v = by_placed[placed]
        print(f"  {placed:>7}{len(v):>7}{sum(v) / len(v):>11.2f}{placed - sum(v) / len(v):>11.2f}")
    if kept_share:
        print()
        print(f"  he keeps {100.0 * sum(kept_share) / len(kept_share):.1f}% of the sheep he places")


if __name__ == "__main__":
    main()
