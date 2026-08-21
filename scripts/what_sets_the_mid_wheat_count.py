"""He does not fill the board. So what DOES set the mid-season wheat count?

`is_the_middle_capacity.py` kills "the count is board capacity": 91.8% of his d14-d27 days end with
empty unlocked tiles, a mean of 7.48, every one of them affordable. So the count is chosen. This
tries the next few candidate rules, all cheap, all read straight off the replays.

Candidates, in the order they are worth trying:

  freed_today   tiles that went from occupied to empty during the day (a harvested WHEAT clears its
                tile). "Replant exactly what you just harvested" is the obvious rule and would still
                need no library -- the greedy planner can produce it.
  harv_wheat    HARVEST ops on WHEAT tiles specifically.
  prev_wheat    WHEAT he planted yesterday. A fixed churn rate.
  season_mean   his own mean over d14-d27. Is the count a per-SEASON scalar rather than a per-day
                decision?

The last one matters most for the agent design: if the within-season spread is small next to the
between-season spread, one number per season is the whole middle.

    python -u scripts/what_sets_the_mid_wheat_count.py --lo 14 --hi 27
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TURNS_PER_DAY = 24


def index_replays():
    idx = {}
    for p in glob.glob(str(REPO / "data/seed_scripts/**/*.json"), recursive=True):
        idx.setdefault(pathlib.Path(p).stem, p)
    return idx


def empties(farm):
    return {(x, y)
            for y, row in enumerate(farm.get("tiles") or [])
            for x, t in enumerate(row) if t is None}


def wheat_tiles(farm):
    return {(x, y)
            for y, row in enumerate(farm.get("tiles") or [])
            for x, t in enumerate(row)
            if isinstance(t, dict) and t.get("crop") == "WHEAT"}


def corr(xs, ys):
    m = len(xs)
    if m < 2:
        return float("nan")
    mx, my = sum(xs) / m, sum(ys) / m
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / ((sxx * syy) ** 0.5) if sxx and syy else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default="data/target_rows_kawa_norm.json")
    ap.add_argument("--lo", type=int, default=14)
    ap.add_argument("--hi", type=int, default=27)
    a = ap.parse_args()

    rows = json.loads((REPO / a.targets).read_text())
    target_of = {}
    for r in rows:
        target_of[(r["game"], r["seat"], r["day"])] = r["target"]
    seats = {(r["game"], r["seat"]) for r in rows}
    idx = index_replays()

    recs = []
    for game, seat in sorted(seats):
        path = idx.get(game)
        if not path:
            continue
        rep = json.loads(pathlib.Path(path).read_text())
        acc = {}
        for step in rep.get("steps") or []:
            if seat >= len(step):
                continue
            cell = step[seat]
            obs = cell.get("observation") or {}
            day = int(obs.get("day", 0) or 0)
            hour = int(obs.get("hour", 0) or 0)
            if day < a.lo - 1 or day > a.hi:
                continue
            rec = acc.setdefault(day, {"dawn": None, "ever": set(), "wheat_dawn": 0,
                                       "harv": 0, "turns": 0})
            farms = obs.get("farms") or []
            farm = farms[seat] if seat < len(farms) else {}
            free = empties(farm)
            rec["ever"] |= free
            if hour == 0:
                rec["dawn"] = set(free)
                rec["wheat_dawn"] = len(wheat_tiles(farm))
            act = cell.get("action")
            if act is None:
                continue
            rec["turns"] += 1
            for u in [act.get("farmer")] + list(act.get("hands") or []):
                if u and str(u[0]) == "HARVEST":
                    rec["harv"] += 1

        for day in range(a.lo, a.hi + 1):
            rec = acc.get(day)
            tgt = target_of.get((game, seat, day))
            if not rec or rec["dawn"] is None or rec["turns"] != TURNS_PER_DAY or not tgt:
                continue
            wheat = sum(1 for p in (tgt.get("plants") or []) if p == "WHEAT")
            prev = target_of.get((game, seat, day - 1))
            recs.append({
                "game": game, "seat": seat, "day": day, "wheat": wheat,
                "freed": len(rec["ever"]) - len(rec["dawn"]),
                "harv": rec["harv"],
                "wheat_dawn": rec["wheat_dawn"],
                "prev_wheat": sum(1 for p in ((prev or {}).get("plants") or []) if p == "WHEAT")
                if prev else 0,
                "has_prev": prev is not None,
            })

    n = len(recs)
    print("day-rows: %d, d%d-d%d\n" % (n, a.lo, a.hi))

    w = [r["wheat"] for r in recs]
    print("CANDIDATE RULES, pooled")
    for f, lab in (("freed", "tiles freed today"), ("harv", "HARVEST ops today"),
                   ("wheat_dawn", "WHEAT tiles at dawn")):
        eq = 100.0 * sum(1 for r in recs if r["wheat"] == r[f]) / n
        print("  corr(wheat, %-20s) %7.3f    exact match %5.1f%%"
              % (lab, corr(w, [r[f] for r in recs]), eq))
    prevs = [r for r in recs if r["has_prev"]]
    print("  corr(wheat, %-20s) %7.3f    exact match %5.1f%%"
          % ("wheat planted d-1", corr([r["wheat"] for r in prevs], [r["prev_wheat"] for r in prevs]),
             100.0 * sum(1 for r in prevs if r["wheat"] == r["prev_wheat"]) / len(prevs)))

    # ---- is it a per-season scalar? -------------------------------------------------------------
    by_season = collections.defaultdict(list)
    for r in recs:
        by_season[(r["game"], r["seat"])].append(r["wheat"])
    means = []
    within = []
    for k, v in by_season.items():
        if len(v) < 5:
            continue
        m = sum(v) / len(v)
        means.append(m)
        within.append((sum((x - m) ** 2 for x in v) / len(v)) ** 0.5)
    gm = sum(means) / len(means)
    between = (sum((m - gm) ** 2 for m in means) / len(means)) ** 0.5
    print("\nIS THE COUNT A PER-SEASON SCALAR?  %d seasons" % len(means))
    print("  grand mean wheat/day        %.2f" % gm)
    print("  between-season SD of means  %.2f" % between)
    print("  mean within-season SD       %.2f" % (sum(within) / len(within)))
    print("  -> within/between ratio     %.2f   (>1 means the day matters more than the season)"
          % ((sum(within) / len(within)) / between if between else float("nan")))


if __name__ == "__main__":
    main()
