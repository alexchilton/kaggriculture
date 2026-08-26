"""How many distinct opening scripts does each top player run?

Alex, 2026-08-26: *"so for instance the guy at 2 and 3 - how many different tapes do they have??"*

This is the cost question for re-anchoring. カワシギ needs **four** tapes to cover his whole opening,
because only two bits of the board ever change what he does -- melon-count >= 9 at d3, and the yarn
store at d5 (`project_kaggriculture_only_two_bits_vary`). If the clone lineage is the same shape,
capturing it is four recordings. If every game is a different stream, it is not a tape at all and
there is nothing to copy.

Per player, and then pooled across players:

    distinct openings   how many different d0-d11 op streams that name emitted
    shared              whether two DIFFERENT names emitted the SAME stream -- the direct test that
                        they are running one published script rather than converging
    what splits them    the shop draw of each variant, so a variant can be tied to the bit that
                        selects it

The start state is fixed -- same board, same $3000, same NW quadrant -- so two seats running one
script diverge only when the board does. That is what makes an exact stream comparison meaningful
here and it is why our own agent scores 100% against its tape for the first six days.
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


def stream_hash(replay, seat, last_day=OPEN_TO):
    parts = []
    for t, step in enumerate(replay.get("steps") or []):
        if t // TPD > last_day or seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        parts.append("|".join("-".join(str(x) for x in o) if o else "." for o in ops))
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()[:10]


def yarn_day(replay):
    order, yarn = [], 99
    for t in range(0, len(replay.get("steps") or []), TPD):
        town = ((replay["steps"][t][0] or {}).get("observation") or {}).get("town") or {}
        cur = list(town.get("unlocked_shops") or [])
        while len(order) < len(cur):
            nxt = cur[len(order)]
            order.append(nxt)
            if nxt == "YARN_STORE" and yarn == 99:
                yarn = t // TPD
    return yarn, tuple(order[:3])


def final_money(replay, seat):
    last = (replay["steps"][-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    return float(farms[seat].get("money", 0)) if seat < len(farms) else 0.0


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
        yd, first3 = yarn_day(r)
        for seat in range(min(2, len(names))):
            seats.append(dict(name=names[seat], ep=f.stem,
                              h=stream_hash(r, seat), money=final_money(r, seat),
                              yarn=yd, shops=first3))

    by_name = collections.defaultdict(list)
    for s in seats:
        by_name[s["name"]].append(s)

    print(f"{len(seats)} seats, {len(by_name)} distinct names\n")
    print("--- players with 2+ seats, by best bank")
    ranked = sorted((v for v in by_name.values() if len(v) >= 2),
                    key=lambda v: -max(x["money"] for x in v))
    for v in ranked[:18]:
        variants = collections.Counter(x["h"] for x in v)
        best = max(x["money"] for x in v)
        print(f"   {v[0]['name'][:24]:<25} {len(v):>2} seats  best ${best:>9,.0f}   "
              f"{len(variants)} distinct opening(s)")
        for h, c in variants.most_common():
            ys = sorted({x["yarn"] for x in v if x["h"] == h})
            print(f"      {h}  x{c}   yarn days {ys}")
    print()

    print("--- the same opening under DIFFERENT names (one published script)")
    by_hash = collections.defaultdict(set)
    money_by_hash = collections.defaultdict(list)
    for s in seats:
        by_hash[s["h"]].add(s["name"])
        money_by_hash[s["h"]].append(s["money"])
    shared = [(h, n) for h, n in by_hash.items() if len(n) >= 2]
    shared.sort(key=lambda hn: -max(money_by_hash[hn[0]]))
    for h, names in shared[:12]:
        m = money_by_hash[h]
        print(f"   {h}  {len(names):>2} names, {len(m):>2} seats, "
              f"best ${max(m):>9,.0f} mean ${sum(m)/len(m):>9,.0f}")
        print(f"      {', '.join(sorted(names)[:6])}"
              + (" ..." if len(names) > 6 else ""))
    print()

    print("--- how concentrated is the field?")
    counts = collections.Counter(s["h"] for s in seats)
    top = counts.most_common(8)
    for h, c in top:
        m = money_by_hash[h]
        print(f"   {h}  {c:>3} seats ({100*c/len(seats):>4.1f}%)  "
              f"mean ${sum(m)/len(m):>9,.0f}  best ${max(m):>9,.0f}  "
              f"{len(by_hash[h])} name(s)")
    print(f"   distinct openings overall: {len(counts)} across {len(seats)} seats")


if __name__ == "__main__":
    main()
