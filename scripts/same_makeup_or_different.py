"""Same crops and same herd, just played better? Or a different build entirely?

Alex, 2026-08-26: *"well do they have the same make up of plants / animals? and then just improve
the ops and board? or what is the difference ... compare over a few shop systems"*.

`data/logs/clone_divergence.log` settled that the top clones never replay カワシギ -- 11% op match on
day zero against our own 100% control. So they are a separate lineage. The question left is whether
they nonetheless arrive at his BUILD and simply execute it better, or whether they build something
else.

Three-way, stratified by the shop draw, because the draw is one of only three things that vary
between games and YARN_STORE decides whether WOOL has a town bid at all:

    KAWA      his seats from the recorded tapes
    CLONES    top seats from the 2026-08-25 field, >= $125k, on the two winning herd shapes
    OURS      our 54 ladder replays

Per bucket: money, tiles owned at the bell, crew at its peak, plantings by crop, and the herd.
Plantings are counted from PLANT ops, which are emitted once each -- never from BUY_SEED, which is a
market order re-posted every turn (`feedback_offers_are_not_fills`).
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
US = "alex chilton"
NEW = "data/seed_scripts/daily_2026-08-26"
OURS = "data/seed_scripts/ours_2026-08-26"
KAWA_DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
             "kawa_2026-08-24", "leaders_2026-08-24")
CROPS = ("WHEAT", "STRAWBERRY", "CARROT", "MELON", "TOMATO")


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
    return yarn


def profile(replay, seat):
    planted = collections.Counter()
    crew = 0
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            continue
        act = (step[seat] or {}).get("action") or {}
        for op in [act.get("farmer")] + list(act.get("hands") or []):
            if op and op[0] == "PLANT" and len(op) >= 2:
                planted[op[1]] += 1
        if t % TPD == 0:
            farms = ((step[0] or {}).get("observation") or {}).get("farms") or []
            if seat < len(farms):
                crew = max(crew, 1 + len(farms[seat].get("hands") or []))
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
    return dict(money=float(f.get("money", 0)), tiles=tiles, crew=crew,
                planted=planted, herd=herd)


def show(label, rows):
    if not rows:
        print(f"   {label:<10} --"); return
    n = len(rows)
    def m(f):
        return sum(f(r) for r in rows) / n
    crops = "  ".join(f"{c[:4].lower()} {m(lambda r: r['planted'][c]):>5.1f}" for c in CROPS)
    herd = "  ".join(f"{k[:3].lower()} {m(lambda r: r['herd'][k]):>4.1f}"
                     for k in ("COW", "SHEEP", "CHICKEN", "GOOSE"))
    print(f"   {label:<10}{n:>4} seats  ${m(lambda r: r['money']):>9,.0f}  "
          f"tiles {m(lambda r: r['tiles']):>4.1f}  crew {m(lambda r: r['crew']):>4.1f}")
    print(f"   {'':<10}     {crops}")
    print(f"   {'':<10}     {herd}")


def main():
    kawa = collections.defaultdict(list)
    n = 0
    for d in KAWA_DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:60]:
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA not in names:
                continue
            pr = profile(r, names.index(KAWA))
            if pr:
                kawa[yarn_day(r)].append(pr)
                n += 1

    clones = collections.defaultdict(list)
    for f in sorted(pathlib.Path(NEW).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        yd = yarn_day(r)
        for seat in range(min(2, len(names))):
            pr = profile(r, seat)
            if not pr or pr["money"] < 125_000:
                continue
            cow, sheep = pr["herd"].get("COW", 0), pr["herd"].get("SHEEP", 0)
            if (cow >= 10 and sheep == 4) or (sheep >= 9 and cow <= 7):
                clones[yd].append(pr)

    ours = collections.defaultdict(list)
    for f in sorted(pathlib.Path(OURS).glob("[0-9]*.json")):
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        pr = profile(r, names.index(US) if US in names else 0)
        if pr:
            ours[yarn_day(r)].append(pr)

    buckets = sorted(set(kawa) | set(clones) | set(ours))
    for yd in buckets:
        tag = f"YARN d{yd}" if yd != 99 else "YARN never"
        if not (clones[yd] or kawa[yd] or ours[yd]):
            continue
        print(f"=== {tag}")
        show("KAWA", kawa[yd])
        show("CLONES", clones[yd])
        show("OURS", ours[yd])
        print()

    print("=== ALL DRAWS POOLED")
    show("KAWA", [r for v in kawa.values() for r in v])
    show("CLONES", [r for v in clones.values() for r in v])
    show("OURS", [r for v in ours.values() for r in v])


if __name__ == "__main__":
    main()
