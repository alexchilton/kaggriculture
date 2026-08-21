"""Is the mid-season wheat count board CAPACITY, or a DECISION?

`docs/kawashigi_algorithm_2026-08-21.md` asserts, from the shape of the distribution alone, that
the d14-d27 wheat count is "a property of the board, not a decision". That is the single most
load-bearing unverified claim in the doc: if the count is capacity, the greedy planner already
produces the middle and no library is needed there. If it is not, the middle is a real decision.

This measures it directly, off the raw replays. Nothing here is simulated -- every tile state is
read out of a recorded observation, so no model of the game can be wrong in it.

Four capacity measures, tightest first:

  free_dawn    tiles[y][x] is None at hour 0. Empty, unlocked, plantable right now.
  ever_free    distinct tiles that were None at ANY hour of the day. This is the true board-side
               ceiling: it is free_dawn plus every tile a HARVEST or CLEAR opened mid-day. WHEAT is
               `ongoing: False`, so harvesting one clears its tile and it can be replanted the same
               day -- which is why 54% of his days plant MORE wheat than free_dawn.
  free_h12     distinct tiles that were None at some hour <= 12, i.e. capacity he had half a day
               left to reach.
  free_dusk    tiles still None at hour 23. **This is the decisive one.** Capacity he had, did not
               use, and left empty overnight. If the middle were "plant every tile you can reach",
               this is ~0.

Seed and money are the two other binding constraints, so both are reported:

  seed_cap     WHEAT seeds held at dawn + WHEAT seeds bought during the day
  money_dawn   bank at hour 0 (a WHEAT seed is $10 base)

    python -u scripts/is_the_middle_capacity.py \
        --targets data/target_rows_kawa_norm.json --lo 14 --hi 27
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
WHEAT_SEED_COST = 10


def index_replays():
    idx = {}
    for p in glob.glob(str(REPO / "data/seed_scripts/**/*.json"), recursive=True):
        idx.setdefault(pathlib.Path(p).stem, p)
    return idx


def empties(farm):
    """Coordinates of empty unlocked tiles. `None` is the only plantable tile (kaggriculture:425)."""
    out = set()
    for y, row in enumerate(farm.get("tiles") or []):
        for x, t in enumerate(row):
            if t is None:
                out.add((x, y))
    return out


def day_facts(rep, seat, lo, hi):
    """Per day, straight off the recorded observations. No simulation."""
    out = {}
    for step in rep.get("steps") or []:
        if seat >= len(step):
            continue
        cell = step[seat]
        obs = cell.get("observation") or {}
        day = int(obs.get("day", 0) or 0)
        hour = int(obs.get("hour", 0) or 0)
        if day < lo or day > hi:
            continue
        rec = out.setdefault(day, {"dawn": None, "ever": set(), "h12": set(), "dusk": None,
                                   "unlocked": 0, "seed_dawn": 0, "seed_buy": 0, "turns": 0,
                                   "units": 0, "money_dawn": 0.0, "harvests": 0})
        farms = obs.get("farms") or []
        farm = farms[seat] if seat < len(farms) else {}
        free = empties(farm)
        rec["ever"] |= free
        if hour <= 12:
            rec["h12"] |= free
        if hour == 0:
            rec["dawn"] = len(free)
            rec["unlocked"] = sum(1 for r in farm.get("tiles") or [] for t in r if t != "LOCKED")
            rec["money_dawn"] = float(farm.get("money") or 0.0)
            rec["seed_dawn"] = int(((obs.get("private") or {}).get("seeds") or {})
                                   .get("WHEAT", 0) or 0)
        if hour == TURNS_PER_DAY - 1:
            rec["dusk"] = len(free)

        act = cell.get("action")
        if act is None:
            continue
        rec["turns"] += 1
        rec["units"] = max(rec["units"], 1 + len(act.get("hands") or []))
        for u in [act.get("farmer")] + list(act.get("hands") or []):
            if u and str(u[0]) == "HARVEST":
                rec["harvests"] += 1
        for o in (act.get("market") or []):
            if o and str(o[0]) == "BUY_SEED" and len(o) > 1 and str(o[1]) == "WHEAT":
                rec["seed_buy"] += int(o[2]) if len(o) > 2 else 1
    return {d: r for d, r in out.items()
            if r["turns"] == TURNS_PER_DAY and r["dawn"] is not None and r["dusk"] is not None}


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
    idx = index_replays()

    by_game = collections.defaultdict(dict)
    for r in rows:
        if a.lo <= r["day"] <= a.hi:
            by_game[(r["game"], r["seat"])][r["day"]] = r["target"]

    recs = []
    for (game, seat), days in sorted(by_game.items()):
        path = idx.get(game)
        if not path:
            continue
        rep = json.loads(pathlib.Path(path).read_text())
        facts = day_facts(rep, seat, a.lo, a.hi)
        for day, target in days.items():
            f = facts.get(day)
            if not f:
                continue
            plants = list(target.get("plants") or [])
            wheat = sum(1 for p in plants if p == "WHEAT")
            recs.append({"game": game, "seat": seat, "day": day, "wheat": wheat,
                         "planted": len(plants),
                         "dawn": f["dawn"], "ever": len(f["ever"]), "h12": len(f["h12"]),
                         "dusk": f["dusk"], "seed_cap": f["seed_dawn"] + f["seed_buy"],
                         "unlocked": f["unlocked"], "units": f["units"],
                         "money": f["money_dawn"], "harvests": f["harvests"]})

    n = len(recs)
    print("seasons: %d   day-rows measured: %d   days d%d-d%d\n"
          % (len(by_game), n, a.lo, a.hi))

    def pct(k, d):
        return 100.0 * k / d if d else 0.0

    print("MEAN PER DAY.  'planted' is every crop, 'wheat' only WHEAT.")
    print("%4s %5s %7s %8s %7s %8s %7s %7s %8s %8s"
          % ("day", "n", "planted", "wheat", "dawn", "everfree", "h12", "dusk", "seedcap", "money"))
    by_day = collections.defaultdict(list)
    for r in recs:
        by_day[r["day"]].append(r)
    for day in sorted(by_day):
        rs = by_day[day]
        k = len(rs)
        def m(f):
            return sum(r[f] for r in rs) / k
        print("%4d %5d %7.2f %8.2f %7.2f %8.2f %7.2f %7.2f %8.2f %8.0f"
              % (day, k, m("planted"), m("wheat"), m("dawn"), m("ever"), m("h12"), m("dusk"),
                 m("seed_cap"), m("money")))

    print("\nSATURATION.  What fraction of the board-side ceiling did he actually use?")
    print("%4s %5s %11s %12s %12s %12s"
          % ("day", "n", "wheat/ever", "wheat==ever", "dusk==0", "dusk>=3"))
    for day in sorted(by_day):
        rs = by_day[day]
        k = len(rs)
        ratio = sum(r["wheat"] / r["ever"] for r in rs if r["ever"]) / max(1, sum(1 for r in rs if r["ever"]))
        print("%4d %5d %10.2f  %11.1f%% %11.1f%% %11.1f%%"
              % (day, k, ratio,
                 pct(sum(1 for r in rs if r["wheat"] == r["ever"]), k),
                 pct(sum(1 for r in rs if r["dusk"] == 0), k),
                 pct(sum(1 for r in rs if r["dusk"] >= 3), k)))

    print("\nPOOLED d%d-d%d, %d day-rows" % (a.lo, a.hi, n))
    print("  planted == ever_free      %6.1f%%   (planted EVERY tile the board offered)"
          % pct(sum(1 for r in recs if r["planted"] == r["ever"]), n))
    print("  wheat   == ever_free      %6.1f%%" % pct(sum(1 for r in recs if r["wheat"] == r["ever"]), n))
    print("  wheat   == free_dawn      %6.1f%%" % pct(sum(1 for r in recs if r["wheat"] == r["dawn"]), n))
    print("  dusk    == 0              %6.1f%%   (board full overnight)"
          % pct(sum(1 for r in recs if r["dusk"] == 0), n))
    print("  dusk    >= 3              %6.1f%%   (three or more tiles left empty)"
          % pct(sum(1 for r in recs if r["dusk"] >= 3), n))
    print("  mean tiles left empty at dusk   %.2f" % (sum(r["dusk"] for r in recs) / n))
    print("  mean board-side ceiling unused  %.2f" % (sum(r["ever"] - r["planted"] for r in recs) / n))

    w = [r["wheat"] for r in recs]
    for f, lab in (("dawn", "free_dawn"), ("ever", "ever_free"), ("h12", "free_by_h12"),
                   ("seed_cap", "seed_cap"), ("units", "units"), ("money", "money_dawn"),
                   ("unlocked", "unlocked")):
        print("  corr(wheat, %-11s) %7.3f" % (lab, corr(w, [r[f] for r in recs])))

    print("\nCOULD MONEY EXPLAIN THE SHORTFALL?  A WHEAT seed is $%d." % WHEAT_SEED_COST)
    left = [r for r in recs if r["dusk"] > 0]
    afford = sum(1 for r in left if r["money"] >= r["dusk"] * WHEAT_SEED_COST)
    print("  %d rows left a tile empty overnight; %d (%.1f%%) could have afforded the seed for"
          " every one of them at dawn." % (len(left), afford, pct(afford, len(left))))

    print("\nDISTRIBUTION of tiles left empty at dusk")
    c = collections.Counter(r["dusk"] for r in recs)
    for k in sorted(c):
        print("  %3d  %5d  %5.1f%%" % (k, c[k], pct(c[k], n)))


if __name__ == "__main__":
    main()
