"""Across a fresh corpus: does anyone play a different GAME, or is the field one agent with dials?

SOUTA Sakurai and カワシギ matched to within 0.3 points on every op in the mix, on the same land,
with the same herd (`data/logs/style_with_animals.log`). That is one agent, not two. The question
this answers is whether the rest of the field is the same again.

`CLAUDE.md` records the trap: the built-in opponent pool *looks* diverse but is
`heuristic.make_agent` with different dials -- "diverse in crop allocation, not in play style".
Reading a crop histogram and calling it a strategy is how that was got wrong before. So the
fingerprint here is deliberately the things a DIAL cannot change:

    the op mix        what share of the day goes to each kind of work
    the day shape     when the herd is built and when it is wound down
    the close         how much is still standing on d29

and the crop histogram is reported BESIDE it, never folded into the distance.

`dist` is the mean absolute difference, in percentage points, between this player's op mix and
カワシギ's. Small means "same agent, maybe different dials". Large means a different game, and is
the only thing here worth reading a replay over.

Players with one game are listed but not ranked: a single game cannot separate a style from a draw.
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
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
KEYS = ["MOVE", "PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG",
        "FEED", "CARE", "COLLECT_FERTILIZER", "PLACE", "PICKUP", "DROP", "PASS"]


def game_profile(steps, seat):
    ops = collections.Counter()
    land = hires = 0
    for t in range(len(steps) - 1):
        a = steps[t + 1][seat].get("action")
        if not isinstance(a, dict):
            continue
        for x in [a.get("farmer")] + list(a.get("hands") or []):
            if isinstance(x, (list, tuple)) and x:
                ops["MOVE" if x[0] in MOVES else x[0]] += 1
        for o in (a.get("market") or []):
            if isinstance(o, (list, tuple)) and o:
                if o[0] == "BUY_LAND":
                    land += 1
                elif o[0] == "HIRE":
                    hires += 1
    total = sum(ops.values()) or 1
    mix = {k: 100.0 * ops.get(k, 0) / total for k in KEYS}

    def board(day):
        t = min(day * TPD, len(steps) - 1)
        farm = steps[t][seat]["observation"]["farms"][seat]
        crop = collections.Counter()
        pens = 0
        for row in (farm.get("tiles") or []):
            for x in row:
                if not isinstance(x, dict):
                    continue
                if x.get("crop"):
                    crop[x["crop"]] += 1
                if x.get("kind") in ("PASTURE", "COOP"):
                    pens += 1
        return crop, pens

    c25, pens25 = board(25)
    c29, _ = board(29)
    return {"mix": mix, "land": land, "hires": hires, "crop": c25, "pens": pens25,
            "standing29": sum(c29.values())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default=str(REPO / "data/seed_scripts/leaders_2026-08-24/*.json"))
    ap.add_argument("--min-games", type=int, default=2)
    a = ap.parse_args()

    kawa = []
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c"):
        kawa += glob.glob(str(REPO / f"data/seed_scripts/{name}/*.json"))

    acc = collections.defaultdict(list)
    for f in sorted(glob.glob(a.glob)) + sorted(kawa):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        rw = rec.get("rewards") or [0, 0]
        for seat, who in enumerate(names):
            p = game_profile(rec["steps"], seat)
            p["money"] = rw[seat]
            p["won"] = rw[seat] > rw[1 - seat]
            acc[who].append(p)
        print(f"  {pathlib.Path(f).stem}", flush=True)

    def mean_mix(ps):
        return {k: sum(p["mix"][k] for p in ps) / len(ps) for k in KEYS}

    ref = mean_mix(acc["カワシギ"]) if acc.get("カワシギ") else None
    rows = []
    for who, ps in acc.items():
        m = mean_mix(ps)
        d = (sum(abs(m[k] - ref[k]) for k in KEYS) / len(KEYS)) if ref else 0.0
        rows.append((d, who, len(ps), m, ps))

    ranked = sorted((r for r in rows if r[2] >= a.min_games), reverse=True)
    print(f"\n{len(acc)} players, {sum(len(v) for v in acc.values())} seats. "
          f"`dist` = mean |op-mix difference| from カワシギ, in points.\n")
    print(f"{'dist':>5} {'who':>26} {'n':>3} {'mean $':>9} {'W':>3}  "
          + " ".join(f"{k[:5]:>5}" for k in KEYS) + f" {'d29':>5}")
    for d, who, n, m, ps in ranked:
        wins = sum(1 for p in ps if p["won"])
        st = sum(p["standing29"] for p in ps) / n
        print(f"{d:>5.1f} {who[:26]:>26} {n:>3} {sum(p['money'] for p in ps) / n:>9,.0f} "
              f"{wins:>3}  " + " ".join(f"{m[k]:>5.1f}" for k in KEYS) + f" {st:>5.1f}")

    print("\ncrops at d25 for the five most DIFFERENT players")
    for d, who, n, _m, ps in ranked[:5]:
        c = collections.Counter()
        for p in ps:
            c += p["crop"]
        print(f"{who[:26]:>26} ({d:.1f})  "
              + ", ".join(f"{k} {v / n:.1f}" for k, v in c.most_common(5)))

    singles = [r[1] for r in rows if r[2] < a.min_games]
    print(f"\n{len(singles)} players with fewer than {a.min_games} games are not ranked "
          f"-- one game cannot tell a style from a draw.")


if __name__ == "__main__":
    main()
