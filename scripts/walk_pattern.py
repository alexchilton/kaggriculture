"""Which generator produces his walk? Lawnmower, serpentine, nearest-neighbour, or none.

Alex: "he should match the fucking movement - lawnmower or weird serpentine", and "do a fucking
pattern match".

For every unit on every day, this takes the tiles that unit WORKED (not merely stood on), in the
order it worked them, and asks which candidate ordering over that same SET reproduces the observed
order. The set is held fixed, so this measures the ORDER only -- which tiles a unit gets is a separate
question and is reported alongside as the unit's bounding box.

Candidates, each tried from the unit's dawn square:

    lawnmower_row   rows nearest the shed first, every row swept the same direction
    serp_row        rows nearest the shed first, direction alternating (boustrophedon)
    serp_row_x      same, but the first row opens at the end nearest the shed's x
    lawnmower_col   columns nearest the shed first, same direction each column
    serp_col        columns, alternating
    nearest         greedy nearest-neighbour from the dawn square
    dist_from_shed  strictly increasing distance from the shed

Scored three ways, because exact equality is a brittle test on a tour that may be interrupted by a
shed trip:

    exact      the candidate order equals the observed order
    adjacent   fraction of consecutive observed pairs that are also consecutive in the candidate
    kendall    rank agreement between the two orderings

`nearest` is the honest null here: almost any sensible tour looks somewhat nearest-neighbour, so a
candidate only means something if it beats that.
"""
import argparse, collections, itertools, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24
WORK = {"PLANT", "WATER", "HARVEST", "FERTILIZE", "FEED", "CARE", "COLLECT_FERTILIZER",
        "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE", "PICKUP", "DROP"}
SHED = (4, 4)


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def lawnmower(tiles, shed, axis=1, alternate=False, open_at_shed=False):
    other = 1 - axis
    lanes = collections.defaultdict(list)
    for t in tiles:
        lanes[t[axis]].append(t)
    order = sorted(lanes, key=lambda v: (abs(v - shed[axis]), v))
    out, flip = [], False
    if open_at_shed and order:
        first = sorted(lanes[order[0]], key=lambda t: t[other])
        flip = abs(first[-1][other] - shed[other]) < abs(first[0][other] - shed[other])
    for i, v in enumerate(order):
        rev = (flip != bool(i % 2)) if alternate else flip
        out.extend(sorted(lanes[v], key=lambda t: t[other], reverse=rev))
    return out


def nearest_chain(tiles, start):
    left, out, pos = list(tiles), [], start
    while left:
        nxt = min(left, key=lambda t: (dist(pos, t), t))
        left.remove(nxt)
        out.append(nxt)
        pos = nxt
    return out


CANDIDATES = {
    "lawnmower_row": lambda ts, shed, start: lawnmower(ts, shed, 1, False, False),
    "serp_row":      lambda ts, shed, start: lawnmower(ts, shed, 1, True, False),
    "serp_row_x":    lambda ts, shed, start: lawnmower(ts, shed, 1, True, True),
    "lawnmower_col": lambda ts, shed, start: lawnmower(ts, shed, 0, False, False),
    "serp_col":      lambda ts, shed, start: lawnmower(ts, shed, 0, True, False),
    "nearest":       lambda ts, shed, start: nearest_chain(ts, start),
    "dist_from_shed": lambda ts, shed, start: sorted(ts, key=lambda t: (dist(shed, t), t)),
}


def kendall(a, b):
    ia = {t: i for i, t in enumerate(a)}
    ib = {t: i for i, t in enumerate(b)}
    common = [t for t in a if t in ib]
    if len(common) < 2:
        return None
    agree = tot = 0
    for x, y in itertools.combinations(common, 2):
        tot += 1
        if (ia[x] < ia[y]) == (ib[x] < ib[y]):
            agree += 1
    return agree / tot


def adjacency(obs, cand):
    ic = {t: i for i, t in enumerate(cand)}
    pairs = [(obs[i], obs[i + 1]) for i in range(len(obs) - 1)]
    if not pairs:
        return None
    ok = sum(1 for x, y in pairs if x in ic and y in ic and abs(ic[x] - ic[y]) == 1)
    return ok / len(pairs)


def unit_days(blob, team, days):
    """[(day, unit, dawn_square, [worked tiles in order])]"""
    names = list((blob.get("info") or {}).get("TeamNames") or [])
    seat = names.index(team) if team in names else 0
    steps = blob["steps"]
    out = []
    for day in days:
        seq = collections.defaultdict(list)
        dawn = {}
        for h in range(TPD):
            t = day * TPD + h
            if t >= len(steps):
                break
            obs = steps[t][seat].get("observation") or {}
            act = steps[t][seat].get("action") or {}
            farms = obs.get("farms") or []
            if len(farms) <= seat:
                continue
            farm = farms[seat]
            pos = [tuple(farm.get("farmer") or (0, 0))] + [tuple(x) for x in (farm.get("hands") or [])]
            acts = [act.get("farmer")] + list(act.get("hands") or [])
            for u, p in enumerate(pos):
                dawn.setdefault(u, p)
                a = acts[u] if u < len(acts) else None
                if a and a[0] in WORK:
                    if not seq[u] or seq[u][-1] != p:
                        seq[u].append(p)
        for u, s in seq.items():
            if len(s) >= 3:
                out.append((day, u, dawn[u], s))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", default="3-20")
    ap.add_argument("--team", default="SpaTaro")
    ap.add_argument("--replays", nargs="+", default=None)
    a = ap.parse_args()

    lo, hi = (int(x) for x in a.days.split("-"))
    days = range(lo, hi + 1)
    if a.replays:
        reps = a.replays
    else:
        import scripts.breakdown as B
        reps = sorted({B.TAPES[k][0] for k in B.TAPES if k.startswith("spa")})

    score = {c: {"exact": 0, "adj": [], "ken": []} for c in CANDIDATES}
    n = 0
    boxes = []
    for rp in reps:
        p = ROOT / rp
        if not p.exists():
            continue
        blob = json.loads(p.read_text())
        for day, u, start, obs in unit_days(blob, a.team, days):
            n += 1
            tiles = list(dict.fromkeys(obs))
            boxes.append((max(t[0] for t in tiles) - min(t[0] for t in tiles) + 1)
                         * (max(t[1] for t in tiles) - min(t[1] for t in tiles) + 1))
            for c, fn in CANDIDATES.items():
                cand = fn(tiles, SHED, start)
                if cand == tiles:
                    score[c]["exact"] += 1
                ad = adjacency(tiles, cand)
                kn = kendall(tiles, cand)
                if ad is not None:
                    score[c]["adj"].append(ad)
                if kn is not None:
                    score[c]["ken"].append(kn)
        print(f"  read {p.name}", flush=True)

    print(f"\n{n} unit-days over {len(reps)} seasons, days {lo}-{hi}")
    print(f"mean worked-tile bounding box {sum(boxes)/max(1,len(boxes)):.1f}\n")
    print(f"{'candidate':16s} {'exact':>8s} {'adjacent':>10s} {'kendall':>9s}")
    rows = []
    for c, d in score.items():
        adj = sum(d["adj"]) / len(d["adj"]) if d["adj"] else 0
        ken = sum(d["ken"]) / len(d["ken"]) if d["ken"] else 0
        rows.append((ken, c, d["exact"] / max(1, n), adj))
    for ken, c, ex, adj in sorted(rows, reverse=True):
        print(f"{c:16s} {ex:7.1%} {adj:9.1%} {ken:8.1%}")
    print("\n`nearest` is the null -- a candidate only means something if it beats it.")


if __name__ == "__main__":
    main()
