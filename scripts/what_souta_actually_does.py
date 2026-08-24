"""What does SOUTA Sakurai do, across every game of his we hold?

He beat us by $29,384 on 98495047 by holding ~76 carrots and dumping them at $498. One game is not
a mechanism. Alex downloaded 25 of his games on 2026-08-24; he is 15-5 in the first 20 read and
wins at every money level, so this is a strong agent and worth reading properly.

The question this answers: **is the carrot corner his standard play, or is it conditional on the
board?** If he does it every game, it is a strategy we can copy wholesale. If he only does it where
the town's carrot drain is deep, the conditional is the thing to copy and the crop is incidental.

Per game it reports:

    drain     CARROT units the town's unlocked shops pull per tick at d25 (`_town_consume` shape)
    peak      the most carrot tiles he held on any day, and the day he hit it
    d29       carrot units in his shed at d29 dawn -- the POSITION
    price     what CARROT closed at
    margin    his money minus his opponent's

Read in place from ~/Downloads; 25 files at ~30 MB each is not worth copying into the repo.
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
HIM = "SOUTA Sakurai"


def _shops():
    sys.path.insert(0, str(REPO / "reference"))
    import kaggriculture as KG
    return KG.SHOPS


def drain_of(obs, shops, product="CARROT"):
    per_tick = 0
    for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
        ps = shops.get(name) or []
        if product in ps:
            per_tick += 2 if len(ps) == 1 else 1
    return per_tick


def tiles_of(farm, crop="CARROT"):
    return sum(1 for row in (farm.get("tiles") or []) for t in row
               if isinstance(t, dict) and t.get("crop") == crop)


def shed_of(obs, product="CARROT"):
    p = obs.get("private") or {}
    c = collections.Counter(p.get("shed") or {})
    for i in (p.get("inventories") or []):
        c.update(i)
    return int(c.get(product, 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="/Users/alexchilton/Downloads/*.json")
    ap.add_argument("--who", default=HIM)
    ap.add_argument("--product", default="CARROT")
    ap.add_argument("--out", default="data/logs/souta_carrot.csv")
    a = ap.parse_args()

    shops = _shops()
    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seat,drain,peak_tiles,peak_day,d29_units,close_price,his_money,"
             "opp_money,margin,won\n")
    fh.flush()

    print(f"{a.who}, {a.product}. `drain` is units/tick the town pulls at d25.\n")
    print(f"{'episode':>10} {'drain':>6} {'peak':>5} {'@day':>5} {'d29':>5} {'price':>7} "
          f"{'his $':>10} {'opp $':>10} {'margin':>10}  W/L", flush=True)

    rows = []
    for f in sorted(glob.glob(a.glob)):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        info = rec.get("info") or {}
        names = info.get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        steps = rec["steps"]
        ep = pathlib.Path(f).stem

        peak = peak_day = 0
        for d in range(30):
            t = d * TPD
            if t >= len(steps):
                break
            o = steps[t][seat]["observation"]
            n = tiles_of(o["farms"][seat], a.product)
            if n > peak:
                peak, peak_day = n, d

        t29 = min(29 * TPD, len(steps) - 1)
        o29 = steps[t29][seat]["observation"]
        d29 = shed_of(o29, a.product)
        drain = drain_of(steps[min(25 * TPD, len(steps) - 1)][seat]["observation"], shops,
                         a.product)
        last = steps[-1][seat]["observation"]
        price = float(((last.get("market") or {}).get("prices") or {}).get(a.product, 0) or 0)
        rw = rec.get("rewards") or [0, 0]
        his, opp = rw[seat], rw[1 - seat]
        won = "W" if his > opp else ("D" if his == opp else "L")

        print(f"{ep:>10} {drain:>6} {peak:>5} {peak_day:>5} {d29:>5} {price:>7.0f} "
              f"{his:>10,.0f} {opp:>10,.0f} {his - opp:>+10,.0f}  {won}", flush=True)
        fh.write(",".join(str(x) for x in [ep, seat, drain, peak, peak_day, d29, round(price),
                                           round(his), round(opp), round(his - opp), won]) + "\n")
        fh.flush()
        rows.append((drain, peak, d29, price, his - opp, won))
    fh.close()

    if rows:
        deep = [r for r in rows if r[0] >= 5]
        shallow = [r for r in rows if r[0] < 5]
        print(f"\n{len(rows)} games. record "
              f"{sum(1 for r in rows if r[5] == 'W')}-{sum(1 for r in rows if r[5] == 'L')}")
        for label, g in (("drain >= 5", deep), ("drain <  5", shallow)):
            if not g:
                continue
            print(f"  {label:>10}  n={len(g):>2}  mean peak tiles {sum(r[1] for r in g)/len(g):>5.1f}"
                  f"  mean d29 units {sum(r[2] for r in g)/len(g):>5.1f}"
                  f"  mean close ${sum(r[3] for r in g)/len(g):>6.0f}"
                  f"  W-L {sum(1 for r in g if r[5]=='W')}-{sum(1 for r in g if r[5]=='L')}")
    print(f"\nrows -> {out}")


if __name__ == "__main__":
    main()
