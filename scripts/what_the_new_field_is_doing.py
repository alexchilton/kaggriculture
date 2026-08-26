"""Survey the freshest ladder day: who is winning, and with what?

120 episodes from `kaggle/kaggriculture-episodes-2026-08-25`, pulled 2026-08-26 into
`data/seed_scripts/daily_2026-08-26/` with the winner-banked >= $60k filter.

Looking for tactics we do not have, and specifically for the four things this repo has an open or a
reversed verdict on:

    TOMATO / CARROT / EGG   put on the `hinge` price shape by 1.32.7 (2026-08-15). Our `SELLABLE`
                            list blocked all three from being sold AT ALL for a period, which
                            invalidated four carrot arms and the goose verdict with them
                            (`project_kaggriculture_sellable_blocked_three_products`).
    GOOSE                   measured as losing and deleted from the tree. That verdict was formed
                            while EGG could not be sold, so it is worth re-checking against a field
                            that can sell it.

Per seat, per side of every game: final bank, tiles owned, what was PLANTed, what animals ended on
the board, and which products cleared a SELL. Ranked by bank, so the top of the field is read
separately from the middle -- an average over 240 seats describes nobody.

`BUY_*` and `SELL_*` are market ORDERS and are re-posted every turn, so a raw count of them is
meaningless (`feedback_offers_are_not_fills`). Products SOLD are inferred from the shed falling
while money rises, and are reported as "seats that sold it at all", never as a quantity.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24


def seat_summary(replay, seat):
    steps = replay.get("steps") or []
    planted = collections.Counter()
    placed = collections.Counter()
    for t, step in enumerate(steps):
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if not op:
                continue
            if op[0] == "PLANT" and len(op) >= 2:
                planted[op[1]] += 1
            elif op[0] == "PLACE" and len(op) >= 2:
                placed[op[1]] += 1
    last = (steps[-1][0] or {}).get("observation") or {}
    farms = last.get("farms") or []
    if seat >= len(farms):
        return None
    f = farms[seat]
    animals = collections.Counter()
    tiles = crops_left = 0
    for row in (f.get("tiles") or []):
        for c in row:
            if not isinstance(c, dict):
                continue
            if c.get("owned", True):
                tiles += 1
            if c.get("animal"):
                animals[c["animal"]] += 1
            if c.get("crop"):
                crops_left += 1
    # A product the shed ever held and later gave up while money rose: sold, not just offered.
    sold = set()
    prev_shed, prev_money = None, None
    for t in range(0, len(steps), 4):
        o = (steps[t][0] or {}).get("observation") or {}
        fs = (o.get("farms") or [])
        if seat >= len(fs):
            continue
        shed = dict(fs[seat].get("shed") or {})
        money = float(fs[seat].get("money", 0))
        if prev_shed is not None and money > prev_money:
            for k, v in prev_shed.items():
                if shed.get(k, 0) < v:
                    sold.add(k)
        prev_shed, prev_money = shed, money
    return dict(money=float(f.get("money", 0)), tiles=tiles, planted=planted,
                placed=placed, animals=animals, crops_left=crops_left, sold=sold)


def main(paths):
    rows = []
    for p in paths:
        f = pathlib.Path(p)
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        for seat in range(min(2, len(names))):
            s = seat_summary(r, seat)
            if s:
                s["name"] = names[seat]
                s["ep"] = f.stem
                rows.append(s)
    rows.sort(key=lambda r: -r["money"])
    print(f"{len(rows)} seats from {len(set(r['ep'] for r in rows))} episodes\n")

    print("--- TOP 25 SEATS")
    print(f"{'bank':>10}{'tiles':>7}{'crops@bell':>12}  {'herd':<28}{'top crops':<34}name")
    for r in rows[:25]:
        herd = " ".join(f"{v}{k[:2].lower()}" for k, v in r["animals"].most_common())
        crops = " ".join(f"{k[:4].lower()}{v}" for k, v in r["planted"].most_common(4))
        print(f"{r['money']:>10,.0f}{r['tiles']:>7}{r['crops_left']:>12}  {herd:<28}{crops:<34}"
              f"{r['name'][:22]}")

    def block(label, sel):
        if not sel:
            return
        n = len(sel)
        print(f"\n--- {label}  ({n} seats)")
        pl = collections.Counter()
        an = collections.Counter()
        sold = collections.Counter()
        seats_with = collections.Counter()
        for r in sel:
            pl.update(r["planted"])
            an.update(r["animals"])
            for k in r["sold"]:
                sold[k] += 1
            for k in r["animals"]:
                seats_with[k] += 1
        print("   plants/seat: " + "  ".join(f"{k.lower()} {v/n:.1f}" for k, v in pl.most_common()))
        print("   herd/seat:   " + "  ".join(f"{k.lower()} {v/n:.2f}" for k, v in an.most_common()))
        print("   seats holding: " + "  ".join(f"{k.lower()} {100*v/n:.0f}%"
                                               for k, v in seats_with.most_common()))
        print("   seats that SOLD: " + "  ".join(f"{k.lower()} {100*v/n:.0f}%"
                                                 for k, v in sold.most_common()))

    block("TOP DECILE", rows[:max(1, len(rows)//10)])
    block("SECOND DECILE", rows[len(rows)//10:2*len(rows)//10])
    block("BOTTOM HALF", rows[len(rows)//2:])

    print("\n--- the four open questions")
    for prod, tag in (("GOOSE", "animal"), ("TOMATO", "crop"), ("CARROT", "crop"), ("EGG", "sold")):
        if tag == "animal":
            have = [r for r in rows if r["animals"].get(prod)]
            print(f"   {prod:<8} on the board in {len(have)}/{len(rows)} seats"
                  + (f"; best bank ${max(r['money'] for r in have):,.0f}" if have else ""))
        elif tag == "crop":
            have = [r for r in rows if r["planted"].get(prod)]
            print(f"   {prod:<8} planted by {len(have)}/{len(rows)} seats"
                  + (f"; best bank ${max(r['money'] for r in have):,.0f}"
                     f"; mean plants {sum(r['planted'][prod] for r in have)/len(have):.1f}"
                     if have else ""))
        else:
            have = [r for r in rows if prod in r["sold"]]
            print(f"   {prod:<8} sold by {len(have)}/{len(rows)} seats"
                  + (f"; best bank ${max(r['money'] for r in have):,.0f}" if have else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
