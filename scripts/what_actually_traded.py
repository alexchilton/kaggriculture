"""What SOUTA, カワシギ and we actually SOLD -- fills, never offers.

The order counts said SELL 495 / 471 / 158 and that is noise. Alex's argument, 2026-08-24, is the
decisive one and it needs no code: the three of us hold the SAME land -- WHEAT ~26, STRAWBERRY
~22-26, COW ~8-9, SHEEP ~5-7 at d25 -- so we cannot be producing a third of what they produce.
The extra orders are re-posts of a standing quota, and kawa will emit `BUY 8` and `SELL 3` of the
same product on one turn.

`kagg/analysis/replay_fills.trade_fills` is the only correct reader for a downloaded game: a ladder
replay carries `seed: None`, so it cannot be re-simulated and `fills.py` has no commit to wrap.
It reconciles the seat's own shed against the town's market inventory.

**Read the caveats it returns.** `sold` is a LOWER BOUND. `shared` is volume that certainly moved
but which two ledgers could not attribute to a seat; `unresolved` is volume the market ledger could
not see because the product sat at the $1 floor while the shed was unreadable. Both are printed
beside the totals, and `cov` is the fraction of turns where this seat's shed was readable at all.
A comparison drawn from a low-coverage game is not a comparison.
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.analysis import replay_fills as RF                                # noqa: E402


def profile(files, who, label):
    sold = collections.Counter()
    bought = collections.Counter()
    shared = collections.Counter()
    unres = collections.Counter()
    money = collections.Counter()
    revenue_days = collections.defaultdict(collections.Counter)
    cov = 0.0
    n = 0
    for f in files:
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if who not in names:
            continue
        seat = names.index(who)
        try:
            tf = RF.trade_fills(rec)
        except Exception as e:                                               # noqa: BLE001
            print(f"  {pathlib.Path(f).stem}: {e!r}", flush=True)
            continue
        sold += tf.sold[seat]
        bought += tf.bought[seat]
        shared += tf.shared_sold
        unres += tf.unresolved_sold
        cov += tf.coverage(seat)
        for d, c in tf.sold_by_day[seat].items():
            revenue_days[d] += c
        # Revenue: each unit is worth what the town quoted on the turn it committed, so the price
        # has to be read per TURN. A per-day or per-season average price would hide exactly the
        # thing being looked for -- selling the same units into a worse book.
        for t, c in tf.sold_by_turn[seat].items():
            px = ((RF._obs(rec, t).get("market") or {}).get("prices") or {})
            for prod, units in c.items():
                money[prod] += units * float(px.get(prod, 0) or 0)
        n += 1
        print(f"  {label} {pathlib.Path(f).stem} cov {tf.coverage(seat):.2f}", flush=True)
    if not n:
        return None
    return {"n": n, "sold": sold, "bought": bought, "shared": shared, "unres": unres,
            "cov": cov / n, "by_day": revenue_days, "money": money}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=8, help="games per agent; these are 30 MB each")
    a = ap.parse_args()

    dl = sorted(glob.glob("/Users/alexchilton/Downloads/*.json"))[: a.limit]
    ours = sorted(glob.glob(str(REPO / "data/seed_scripts/losses/*.json")))[: a.limit]
    kawa = []
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c"):
        kawa += sorted(glob.glob(str(REPO / f"data/seed_scripts/{name}/*.json")))
    kawa = kawa[: a.limit]

    who = [("SOUTA", dl, "SOUTA Sakurai"),
           ("kawashigi", kawa, "カワシギ"),
           ("us", ours, "alex chilton")]

    profs = {}
    for label, files, name in who:
        profs[label] = profile(files, name, label)

    print("\nUNITS SOLD per game -- fills, lower bound. `shared`/`unres` are the unattributable"
          " volume and belong beside the numbers, not folded into them.\n")
    prods = ["WHEAT", "STRAWBERRY", "MELON", "CARROT", "TOMATO", "MILK", "WOOL", "EGG"]
    print(f"{'who':>12} {'n':>3} {'cov':>5}  " + " ".join(f"{p[:5]:>6}" for p in prods)
          + f" {'TOTAL':>7}")
    for label, _f, _n in who:
        p = profs[label]
        if p is None:
            print(f"{label:>12}  no games")
            continue
        cells = " ".join(f"{p['sold'][x] / p['n']:>6.1f}" for x in prods)
        print(f"{label:>12} {p['n']:>3} {p['cov']:>5.2f}  {cells} "
              f"{sum(p['sold'].values()) / p['n']:>7.1f}")

    print("\n$ PER UNIT actually realised -- revenue / units, priced at the turn each unit"
          " committed.\nSame volume at a worse price is the failure this is looking for.\n")
    print(f"{'who':>12} {'n':>3}  " + " ".join(f"{p[:5]:>6}" for p in prods) + f" {'TOTAL$':>10}")
    for label, _f, _n in who:
        p = profs[label]
        if p is None:
            continue
        cells = []
        for x in prods:
            u = p["sold"][x]
            cells.append(f"{p['money'][x] / u:>6.0f}" if u else f"{'-':>6}")
        print(f"{label:>12} {p['n']:>3}  " + " ".join(cells)
              + f" {sum(p['money'].values()) / p['n']:>10,.0f}")

    print("\nunattributable volume per game (both seats combined)")
    for label, _f, _n in who:
        p = profs[label]
        if p is None:
            continue
        print(f"{label:>12}  shared {sum(p['shared'].values()) / p['n']:>7.1f}   "
              f"unresolved {sum(p['unres'].values()) / p['n']:>7.1f}")

    print("\nunits sold per DAY (all products)")
    print(f"{'day':>4} " + " ".join(f"{lbl:>10}" for lbl, _f, _n in who))
    for d in range(30):
        cells = []
        for lbl, _f, _n in who:
            p = profs[lbl]
            cells.append(f"{sum(p['by_day'].get(d, {}).values()) / p['n']:>10.1f}"
                         if p else f"{'-':>10}")
        print(f"{d:>4} " + " ".join(cells))


if __name__ == "__main__":
    main()
