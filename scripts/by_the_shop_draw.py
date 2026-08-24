"""Group games by the TOWN'S SHOP DRAW before comparing anything.

Alex, 2026-08-24: *"we have different tapes for different shops like kawa so the average is not good
to show."*

He is right and it invalidates the season means printed earlier today. カワシギ is four tapes and the
arm is chosen off the board (`project_kaggriculture_only_two_bits_vary`); a mean over his games
averages four different plans. The same applies to SOUTA, and to us. Worse, the shop draw sets the
town's DRAIN per product, so it moves the price curve as well as the plan -- two games with
different shops are not two samples of one quantity.

So: bucket by the set of shops the town unlocked, then compare inside a bucket only.

Reported per bucket, per agent:

    n        games
    W-L      record
    $        mean final bank
    carrot   peak carrot tiles seen at any day's dawn -- the corner, if it happened
    sold     units actually sold, from `replay_fills.trade_fills`, never offers

The shop signature is the sorted set of shops unlocked by the end of the game. Unlock ORDER also
varies and is not folded in here; a bucket is therefore still a mix of orderings.
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

TPD = 24


def shop_signature(rec, seat):
    steps = rec["steps"]
    o = steps[min(29 * TPD, len(steps) - 1)][seat]["observation"]
    shops = sorted((o.get("town") or {}).get("unlocked_shops") or [])
    return tuple(shops)


def peak_carrot(rec, seat):
    steps = rec["steps"]
    peak = 0
    for d in range(30):
        t = d * TPD
        if t >= len(steps):
            break
        farm = steps[t][seat]["observation"]["farms"][seat]
        n = sum(1 for row in (farm.get("tiles") or []) for x in row
                if isinstance(x, dict) and x.get("crop") == "CARROT")
        peak = max(peak, n)
    return peak


def scan(files, names_wanted, limit_per=None):
    rows = []
    seen = collections.Counter()
    for f in sorted(files):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        for label, who in names_wanted:
            if who not in names:
                continue
            if limit_per and seen[label] >= limit_per:
                continue
            seat = names.index(who)
            rw = rec.get("rewards") or [0, 0]
            try:
                tf = RF.trade_fills(rec)
                sold = dict(tf.sold[seat])
                cov = tf.coverage(seat)
            except Exception:                                                # noqa: BLE001
                sold, cov = {}, 0.0
            rows.append({"ep": pathlib.Path(f).stem, "who": label, "seat": seat,
                         "sig": shop_signature(rec, seat), "carrot": peak_carrot(rec, seat),
                         "money": rw[seat], "opp": rw[1 - seat], "sold": sold, "cov": cov})
            seen[label] += 1
            print(f"  {label:>10} {pathlib.Path(f).stem}  cov {cov:.2f}", flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=12)
    a = ap.parse_args()

    dl = glob.glob("/Users/alexchilton/Downloads/*.json")
    ours = glob.glob(str(REPO / "data/seed_scripts/losses/*.json"))
    kawa = []
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c"):
        kawa += glob.glob(str(REPO / f"data/seed_scripts/{name}/*.json"))
    lead = glob.glob(str(REPO / "data/seed_scripts/leaders_2026-08-24/*.json"))

    rows = []
    rows += scan(dl, [("SOUTA", "SOUTA Sakurai")], a.limit)
    rows += scan(kawa, [("kawashigi", "カワシギ")], a.limit)
    rows += scan(ours + lead, [("us", "alex chilton")], a.limit)

    by_sig = collections.defaultdict(list)
    for r in rows:
        by_sig[r["sig"]].append(r)

    print(f"\n{len(rows)} games, {len(by_sig)} distinct shop draws.\n")
    prods = ["WHEAT", "STRAWBERRY", "MELON", "CARROT", "MILK", "WOOL"]

    for sig in sorted(by_sig, key=lambda s: -len(by_sig[s])):
        group = by_sig[sig]
        if len(group) < 2:
            continue
        print("=" * 100)
        print("shops: " + (", ".join(sig) if sig else "(none)"))
        print(f"{'who':>10} {'episode':>10} {'carrot':>7} {'$':>10} {'opp $':>10} {'W/L':>4}  "
              + " ".join(f"{p[:5]:>6}" for p in prods))
        for r in sorted(group, key=lambda x: (x["who"], -x["money"])):
            wl = "W" if r["money"] > r["opp"] else ("D" if r["money"] == r["opp"] else "L")
            cells = " ".join(f"{r['sold'].get(p, 0):>6}" for p in prods)
            print(f"{r['who']:>10} {r['ep']:>10} {r['carrot']:>7} {r['money']:>10,.0f} "
                  f"{r['opp']:>10,.0f} {wl:>4}  {cells}")
        print()

    singles = sum(1 for s in by_sig if len(by_sig[s]) == 1)
    print(f"{singles} shop draws appear in only one game and are not shown above.")

    # A pooled mean over games is a mean over different towns. A STRATIFIED mean is not: take the
    # within-draw mean for each agent, then average those across the draws where both agents played.
    # Each draw then contributes equally regardless of how many games it holds, and the shop mix
    # cannot differ between the two columns by construction.
    agents = sorted({r["who"] for r in rows})
    print("\nSTRATIFIED over shop draws: within-draw means, averaged over draws where BOTH played.")
    for i, a1 in enumerate(agents):
        for a2 in agents[i + 1:]:
            strata = []
            for sig, group in by_sig.items():
                g1 = [r for r in group if r["who"] == a1]
                g2 = [r for r in group if r["who"] == a2]
                if g1 and g2:
                    strata.append((sum(r["money"] for r in g1) / len(g1),
                                   sum(r["money"] for r in g2) / len(g2),
                                   sum(r["carrot"] for r in g1) / len(g1),
                                   sum(r["carrot"] for r in g2) / len(g2)))
            if not strata:
                print(f"  {a1:>10} vs {a2:<10}  no shop draw contains both -- not comparable")
                continue
            d = sum(s[0] - s[1] for s in strata) / len(strata)
            c = sum(s[2] - s[3] for s in strata) / len(strata)
            print(f"  {a1:>10} vs {a2:<10}  {len(strata):>2} shared draws   "
                  f"bank {d:>+10,.0f}   peak carrot tiles {c:>+5.1f}")


if __name__ == "__main__":
    main()
