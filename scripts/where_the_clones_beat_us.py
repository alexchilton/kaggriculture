"""The top カワシギ-clones against us, day by day, d12-d29.

`data/logs/new_field.log`: the top of the 2026-08-25 field is one script under many names --
`whea134 stra38 carr20 melo11` on an 11co/4sh herd repeats verbatim across nine of the top twelve
seats, and a second cluster runs `whea128 stra39 carr12 melo11` on 10sh/6co over 37 tiles. カワシギ
himself is 12th at $131,597. So the people beating him are running his shape with changes, which is
exactly what we are trying to do -- and they are $20k ahead of him while we are not.

That makes them a better comparison than カワシギ. A difference against him is confounded by
everything the clones also changed; a difference against THEM is the gap that is actually costing
rating.

Clones are identified by outcome and shape, not by name -- the same names appear on both sides of
different games, and one name (`WeAreFarmers`) holds three separate top-25 seats. A seat counts as a
clone if it banked over `--min-bank` and its herd is one of the two shapes above.

Prints, per day, per side: the unit-op mix, crew, tiles, and standing crop -- the same columns as
`scripts/what_differs_from_d12.py`, so the two tables can be read against each other.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
US = "alex chilton"
OPS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "FERTILIZE", "COLLECT_FERTILIZER",
       "PICKUP", "DROP", "PLACE", "DIG", "PASS")
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
FROM_DAY = 12


def shop_signature(replay):
    """The order the town drew its shops, and the day YARN_STORE landed.

    **Shops unlock on a FIXED cadence -- every 3 days from d3 -- but WHICH shop is drawn varies,
    and that is one of only three things that differ between two games** (the others are the
    opponent and the weed rolls; `project_kaggriculture_start_state_is_fixed`). The draw is not
    cosmetic: YARN_STORE is what puts a town bid under WOOL, so a seat that drew yarn at d6 is
    playing a different economy from one that drew it at d24, and comparing their herds is
    apples to oranges. `SHOP_ADAPT_HERD` in our own agent exists precisely because of this.

    Returns `(first_four_shops, yarn_day)`; `yarn_day` is 99 when yarn never lands.
    """
    seen, order, yarn = set(), [], 99
    for t in range(0, len(replay.get("steps") or []), TPD):
        town = ((replay["steps"][t][0] or {}).get("observation") or {}).get("town") or {}
        for sh in (town.get("unlocked_shops") or []):
            pass
        cur = list(town.get("unlocked_shops") or [])
        # the list only grows; take whatever is newly on the end
        while len(order) < len(cur):
            nxt = cur[len(order)]
            order.append(nxt)
            if nxt == "YARN_STORE" and yarn == 99:
                yarn = t // TPD
    return tuple(order[:4]), yarn


def final(replay, seat):
    last = (replay["steps"][-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    if seat >= len(farms):
        return None
    f = farms[seat]
    herd = collections.Counter()
    tiles = 0
    for row in (f.get("tiles") or []):
        for c in row:
            if isinstance(c, dict):
                if c.get("owned", True):
                    tiles += 1
                if c.get("animal"):
                    herd[c["animal"]] += 1
    return float(f.get("money", 0)), herd, tiles


def day_rows(replay, seat):
    out = collections.defaultdict(collections.Counter)
    for t, step in enumerate(replay.get("steps") or []):
        day = t // TPD
        if day < FROM_DAY or seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        row = out[day]
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if not op:
                continue
            name = op[0]
            row["_MOVE" if name in MOVES else name] += 1
            row["_turns"] += 1
        if t % TPD == TPD - 1:
            farms = ((step[0] or {}).get("observation") or {}).get("farms") or []
            if seat < len(farms):
                f = farms[seat]
                row["crew"] = 1 + len(f.get("hands") or [])
                st = 0
                for r in (f.get("tiles") or []):
                    for c in r:
                        if isinstance(c, dict) and c.get("crop"):
                            st += int(c.get("yield_units", 0) or 0)
                row["standing"] = st
    return out


def collect(pairs):
    acc = collections.defaultdict(lambda: collections.defaultdict(list))
    for replay, seat in pairs:
        for day, row in day_rows(replay, seat).items():
            for k, v in row.items():
                acc[day][k].append(v)
    return acc, len(pairs)


def table(label, acc, n):
    cols = list(OPS) + ["_MOVE", "crew", "standing"]
    print(f"=== {label}   ({n} seats)")
    print("   day" + "".join(f"{c.replace('_',''):>7}" for c in cols))
    tot = collections.Counter()
    for day in sorted(acc):
        row = acc[day]
        def m(k):
            v = row.get(k) or [0]
            return sum(v) / len(v)
        print(f"   {day:>3}" + "".join(f"{m(c):>7.1f}" for c in cols))
        for c in cols:
            tot[c] += m(c)
    print("   SUM" + "".join(f"{tot[c]:>7.0f}" if c not in ("crew", "standing") else f"{'':>7}"
                             for c in cols))
    print()
    return tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", default="data/seed_scripts/daily_2026-08-26")
    ap.add_argument("--ours", default="data/seed_scripts/ours_2026-08-26")
    ap.add_argument("--min-bank", type=float, default=125_000.0)
    args = ap.parse_args()

    clones = []
    for f in sorted(pathlib.Path(args.new).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = ((r.get("info") or {}).get("TeamNames") or [])
        for seat in range(min(2, len(names))):
            fin = final(r, seat)
            if not fin:
                continue
            money, herd, _tiles = fin
            cow, sheep = herd.get("COW", 0), herd.get("SHEEP", 0)
            shape = (cow >= 10 and sheep == 4) or (sheep >= 9 and cow <= 7)
            if money >= args.min_bank and shape:
                sig = shop_signature(r)
                clones.append((r, seat, money, names[seat], sig))
    print(f"clone seats over ${args.min_bank:,.0f}: {len(clones)}")
    for _r, _s, m, nm, sig in sorted(clones, key=lambda z: -z[2])[:14]:
        print(f"   ${m:>9,.0f}  yarn d{sig[1]:<3} {'>'.join(x[:5] for x in sig[0]):<28} {nm}")
    print()
    dist = collections.Counter(sig[1] for *_x, sig in clones)
    print("   clone YARN_STORE day: " + "  ".join(f"d{k}:{v}" for k, v in sorted(dist.items())))

    ours = []
    for f in sorted(pathlib.Path(args.ours).glob("[0-9]*.json")):
        r = json.loads(f.read_text())
        names = ((r.get("info") or {}).get("TeamNames") or [])
        ours.append((r, names.index(US) if US in names else 0, shop_signature(r)))
    dist = collections.Counter(sig[1] for *_x, sig in ours)
    print("   ours  YARN_STORE day: " + "  ".join(f"d{k}:{v}" for k, v in sorted(dist.items())))
    print()

    # **Matched on the shop draw.** Only yarn-days present on BOTH sides are compared, so the
    # herd difference cannot be an artefact of one group having been offered a wool market and the
    # other not.
    cl_days = collections.Counter(sig[1] for *_x, sig in clones)
    ou_days = collections.Counter(sig[1] for *_x, sig in ours)
    shared = sorted(set(cl_days) & set(ou_days))
    print(f"=== matched on YARN_STORE day; shared draws: {shared}")
    cl_sel = [(r, s) for r, s, _m, _n, sig in clones if sig[1] in shared]
    ou_sel = [(r, s) for r, s, sig in ours if sig[1] in shared]
    print(f"    clones {len(cl_sel)} seats   ours {len(ou_sel)} seats\n")

    ca, cn = collect(cl_sel)
    ct = table("TOP CLONES (matched)", ca, cn)
    oa, on = collect(ou_sel)
    ot = table("OURS (matched)", oa, on)

    print("=== d12-d29 totals per seat, ours minus theirs")
    for c in list(OPS) + ["_MOVE", "_turns"]:
        print(f"   {c.replace('_',''):<20}{ot[c]:>9.1f}{ct[c]:>9.1f}{ot[c]-ct[c]:>+9.1f}")


if __name__ == "__main__":
    main()
