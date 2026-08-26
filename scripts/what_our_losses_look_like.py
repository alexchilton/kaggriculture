"""Every downloaded ladder game of ours, one row each, losses first.

Alex: *"was there any other findings from the losses were they mostly q4 versions or the 6 6 sheep
cow ? or some close losses or ...?"*

Three named hypotheses, so three columns to test them with:

    opponent        who beat us, and how often the same name appears. If the losses concentrate on
                    one opponent that is a match-up problem, not a play problem.
    cows / sheep    the herd standing at the bell. The "6 cow 6 sheep" question is whether a
                    particular herd shape loses.
    margin          theirs minus ours. A $500 loss and a $40,000 loss are different failures and
                    must not be averaged.

Plus what every other measurement today has pointed at: `standing`, the units left unharvested, and
`tiles`, how much ground we opened.

**This counts only games we downloaded**, which is every episode of the two newest submissions --
not a sample chosen by outcome, unlike `data/seed_scripts/losses*` which Alex downloads by hand
(`project_kaggriculture_losing_narrowly`). A win rate from THIS set is meaningful.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
US = "alex chilton"
TPD = 24


def herd(farm):
    c = collections.Counter()
    standing = tiles = 0
    for row in (farm.get("tiles") or []):
        for t in row:
            if not isinstance(t, dict):
                continue
            if t.get("owned", True):
                tiles += 1
            a = t.get("animal")
            if a:
                c[a] += 1
            if t.get("crop"):
                standing += int(t.get("yield_units", 0) or 0)
    return c, standing, tiles


def main(paths):
    arm_map = {}
    p = REPO / "data/seed_scripts/ours_2026-08-26/_episode_arm.json"
    if p.exists():
        raw = json.loads(p.read_text())
        for k, v in raw.items():
            arm_map[str(k)] = v[0] if isinstance(v, list) else v

    rows = []
    for path in paths:
        f = pathlib.Path(path)
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        seat = names.index(US) if US in names else 0
        opp = 1 - seat
        last = (r["steps"][-1][0] or {}).get("observation") or {}
        farms = last.get("farms") or []
        if len(farms) < 2:
            continue
        ours = float(farms[seat].get("money", 0))
        theirs = float(farms[opp].get("money", 0))
        h, standing, tiles = herd(farms[seat])
        oh, ostanding, otiles = herd(farms[opp])
        prices = ((last.get("market") or {}).get("prices") or {})
        rows.append(dict(
            ep=f.stem, arm=arm_map.get(f.stem, "?"),
            opp=names[opp] if opp < len(names) else "?",
            ours=ours, theirs=theirs, margin=ours - theirs,
            cow=h.get("COW", 0), sheep=h.get("SHEEP", 0), chick=h.get("CHICKEN", 0),
            standing=standing, tiles=tiles,
            ocow=oh.get("COW", 0), osheep=oh.get("SHEEP", 0),
            ostanding=ostanding, otiles=otiles,
            wool=float(prices.get("WOOL", 0) or 0), milk=float(prices.get("MILK", 0) or 0),
        ))

    rows.sort(key=lambda r: r["margin"])
    losses = [r for r in rows if r["margin"] < 0]
    wins = [r for r in rows if r["margin"] > 0]
    print(f"{len(rows)} games   {len(wins)} W   {len(losses)} L   "
          f"{100*len(wins)/max(1,len(rows)):.1f}%")
    print()
    hdr = (f"{'episode':>10}{'arm':>13}{'margin':>10}{'ours':>10}{'theirs':>10}"
           f"{'cow':>5}{'shp':>5}{'stand':>7}{'tiles':>7}"
           f"{'|opp cow':>9}{'shp':>5}{'stand':>7}{'tiles':>7}"
           f"{'wool':>7}{'milk':>7}  opponent")
    print("--- LOSSES (worst first)")
    print(hdr)
    for r in losses:
        print(f"{r['ep']:>10}{r['arm']:>13}{r['margin']:>10,.0f}{r['ours']:>10,.0f}"
              f"{r['theirs']:>10,.0f}{r['cow']:>5}{r['sheep']:>5}{r['standing']:>7}"
              f"{r['tiles']:>7}{r['ocow']:>9}{r['osheep']:>5}{r['ostanding']:>7}"
              f"{r['otiles']:>7}{r['wool']:>7.0f}{r['milk']:>7.0f}  {r['opp']}")
    print()
    print("--- WINS (narrowest first)")
    print(hdr)
    for r in wins:
        print(f"{r['ep']:>10}{r['arm']:>13}{r['margin']:>10,.0f}{r['ours']:>10,.0f}"
              f"{r['theirs']:>10,.0f}{r['cow']:>5}{r['sheep']:>5}{r['standing']:>7}"
              f"{r['tiles']:>7}{r['ocow']:>9}{r['osheep']:>5}{r['ostanding']:>7}"
              f"{r['otiles']:>7}{r['wool']:>7.0f}{r['milk']:>7.0f}  {r['opp']}")
    print()

    print("--- opponents we LOST to, by count")
    c = collections.Counter(r["opp"] for r in losses)
    w = collections.Counter(r["opp"] for r in wins)
    for name, n in c.most_common():
        print(f"   {n:>3} L  {w.get(name,0):>3} W   {name}")
    print()
    print("--- herd shape at the bell")
    for tag, group in (("LOSS", losses), ("WIN", wins)):
        shapes = collections.Counter((r["cow"], r["sheep"]) for r in group)
        print(f"   {tag}: " + "  ".join(f"{c}c/{s}s x{n}" for (c, s), n in shapes.most_common(8)))
    print()
    print("--- margins")
    for tag, group in (("LOSS", losses), ("WIN", wins)):
        if not group:
            continue
        m = sorted(abs(r["margin"]) for r in group)
        print(f"   {tag}  n={len(m)}  median ${m[len(m)//2]:,.0f}   "
              f"under $2,000: {sum(1 for x in m if x < 2000)}   "
              f"under $10,000: {sum(1 for x in m if x < 10000)}   max ${m[-1]:,.0f}")
    print()
    print("--- means, loss vs win")
    for k in ("ours", "theirs", "standing", "tiles", "cow", "sheep", "wool", "milk",
              "ostanding", "otiles"):
        lv = sum(r[k] for r in losses) / max(1, len(losses))
        wv = sum(r[k] for r in wins) / max(1, len(wins))
        print(f"   {k:<10} loss {lv:>10,.1f}   win {wv:>10,.1f}   diff {wv-lv:>+10,.1f}")


if __name__ == "__main__":
    main(sys.argv[1:])
