"""Across our own ladder games: which of the four zones gives ground, and what is left at the bell.

The agent has four regimes and they are owned by different code:

    d0-d3    the authored opening (and d0-d2 are replayed since `305dc2b`)
    d4-d11   the tape replay        REPLAY_OPENING_DAYS
    d12-d23  the solver             cover.PRECOMPUTED_ROUTES
    d24-d29  the live planner       cover.UNSOLVE_DAYS

A season total cannot say which one is at fault. This measures, per game and per zone, how much
ground we take or give: our bank gain over the zone minus the opponent's over the same days. Summed
across games and split by arm, because the two arms play different seasons.

Also reports the waste that is visible at the bell and costs nothing to see: goods still in the
shed, yield still standing on tiles, and weeds -- every weed on our board is a crop we failed to
water twice (`kaggriculture.py:771`), since these boards spawn at 0.005.

Ground given in a zone is not proof the zone's code is wrong -- an earlier zone can hand it a worse
board. Read it with the day curve, not alone.
"""

import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

US = "alex chilton"
TPD = 24
OPPONENT_MELON = 9
ZONES = (("d0-d3 authored", 0, 3), ("d4-d11 tape", 4, 11),
         ("d12-d23 solver", 12, 23), ("d24-d29 planner", 24, 29))


def bank(steps, day, seat):
    t = min(day * TPD + 23, len(steps) - 1)
    return float(steps[t][0]["observation"]["farms"][seat]["money"])


def one(path):
    rec = json.loads(pathlib.Path(path).read_text())
    info = rec.get("info") or {}
    names = info.get("TeamNames") or []
    steps = rec.get("steps") or []
    if US not in names or not steps:
        return None
    me = names.index(US)
    them = 1 - me

    farms3 = steps[min(3 * TPD + 23, len(steps) - 1)][0]["observation"]["farms"]
    opp_melon = sum(1 for row in farms3[them]["tiles"] for t in row
                    if isinstance(t, dict) and t.get("crop") == "MELON")
    armed = opp_melon >= OPPONENT_MELON

    ground = {}
    for label, a, b in ZONES:
        start_us = bank(steps, a - 1, me) if a else 0.0
        start_th = bank(steps, a - 1, them) if a else 0.0
        ground[label] = (bank(steps, b, me) - start_us) - (bank(steps, b, them) - start_th)

    last = steps[-1]
    farms = last[0]["observation"]["farms"]
    priv = (last[me]["observation"].get("private") or {})
    shed = {k: int(v) for k, v in (priv.get("shed") or {}).items() if int(v or 0) > 0}
    seeds = {k: int(v) for k, v in (priv.get("seeds") or {}).items() if int(v or 0) > 0}
    weeds = standing = 0
    stand_by = collections.Counter()
    for row in farms[me]["tiles"]:
        for t in row:
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "WEED" or t.get("crop") == "WEED":
                weeds += 1
            u = int(t.get("yield_units") or 0)
            if u:
                standing += u
                stand_by[t.get("animal") or t.get("crop") or "?"] += u
    return dict(ep=pathlib.Path(path).stem, armed=armed, ground=ground,
                margin=float(farms[me]["money"]) - float(farms[them]["money"]),
                shed=shed, seeds=seeds, weeds=weeds, standing=standing,
                stand_by=dict(stand_by))


def main():
    rows = []
    for f in sorted(glob.glob(str(pathlib.Path.home() / "Downloads" / "*.json"))):
        try:
            r = one(f)
        except Exception as e:                                                # noqa: BLE001
            print(f"  {pathlib.Path(f).stem}: {e!r}", flush=True)
            continue
        if r:
            rows.append(r)
    print(f"{len(rows)} games\n")

    for armed, label in ((True, "STRAWBERRY arm"), (False, "MELON arm"), (None, "ALL")):
        arm = rows if armed is None else [r for r in rows if r["armed"] == armed]
        if not arm:
            continue
        print(f"{'=' * 92}\n{label} -- {len(arm)} games\n{'=' * 92}")
        print(f"{'zone':<18} {'mean ground':>13} {'median':>11} {'games ahead':>13} "
              f"{'worst':>12} {'best':>12}")
        for zl, _a, _b in ZONES:
            v = sorted(r["ground"][zl] for r in arm)
            n = len(v)
            med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
            print(f"{zl:<18} {sum(v)/n:>13,.0f} {med:>11,.0f} "
                  f"{sum(1 for x in v if x > 0):>7}/{n:<5} {v[0]:>12,.0f} {v[-1]:>12,.0f}")
        print(f"{'SEASON':<18} {sum(r['margin'] for r in arm)/len(arm):>13,.0f}")

        w = collections.Counter()
        sd = collections.Counter()
        for r in arm:
            w["weeds"] += r["weeds"]
            w["standing"] += r["standing"]
            for k, v in r["shed"].items():
                sd["shed_" + k] += v
            for k, v in r["seeds"].items():
                sd["seed_" + k] += v
        print(f"\n  left at the bell, TOTAL over {len(arm)} games:")
        print(f"    weeds {w['weeds']}  ({w['weeds']/len(arm):.1f} a game)")
        print(f"    standing yield {w['standing']} units ({w['standing']/len(arm):.1f} a game)")
        print(f"    shed  {dict(sd and {k: v for k, v in sd.items() if k.startswith('shed_')})}")
        print(f"    seeds {dict({k: v for k, v in sd.items() if k.startswith('seed_')})}\n")


if __name__ == "__main__":
    main()
