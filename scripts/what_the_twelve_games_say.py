"""One pass over the ladder games in ~/Downloads: which arm, what result, and is d8 clean.

Written 2026-08-25 because every claim about the strawberry tape so far came from replaying OTHER
people's games. These are ours, on the ladder, played by the submissions built today.

Splits by ARM first and never averages across them. `melon_branch` decides at d3 on the opponent's
MELON tile count (`OPPONENT_MELON`), and only the armed side -- the strawberry season -- uses the
`97466318` tape that `9ab0f19` swapped in. A melon-arm game says nothing about that swap.

Reports per game:

    arm         opponent MELON tiles at d3, and which tape that selects
    result      our bank, theirs, and the margin
    crew        hands owned at h12 on d5-d8 -- the thing the tape swap was picked to fix
    d3          bank and FERTILIZER in the shed, exact in 35/35 kawashigi replays before
    board       weeds, and what is still standing at the bell
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
#: `melon_branch.OPPONENT_MELON` -- at or above this at d3 and the strawberry season arms.
OPPONENT_MELON = 9
DECIDE_BY_DAY = 3


def tiles_of(farm, crop):
    n = 0
    for row in farm.get("tiles") or []:
        for t in row:
            if isinstance(t, dict) and t.get("crop") == crop:
                n += 1
    return n


def survey(path):
    rec = json.loads(pathlib.Path(path).read_text())
    info = rec.get("info") or {}
    names = info.get("TeamNames") or []
    steps = rec.get("steps") or []
    if US not in names or not steps:
        return None
    me = names.index(US)
    them = 1 - me
    ep = pathlib.Path(path).stem

    # The arm: the opponent's melon at the end of the decision day.
    t3 = min(DECIDE_BY_DAY * TPD + 23, len(steps) - 1)
    farms3 = steps[t3][0]["observation"]["farms"]
    opp_melon = tiles_of(farms3[them], "MELON")
    armed = opp_melon >= OPPONENT_MELON

    # d3 close: bank and fertilizer.
    d3_bank = float(farms3[me]["money"])
    d3_fert = int(((steps[t3][me]["observation"].get("private") or {}).get("shed") or {})
                  .get("FERTILIZER", 0) or 0)

    # Crew at h12 on d5-d8. `hands` is cleared at dawn, so h0 always reads 0.
    crew = {}
    for d in (5, 6, 7, 8):
        t = d * TPD + 12
        if t < len(steps):
            crew[d] = len(steps[t][0]["observation"]["farms"][me].get("hands") or [])

    last = steps[-1][0]["observation"]["farms"]
    ours, theirs = float(last[me]["money"]), float(last[them]["money"])
    weeds = standing = 0
    crops = collections.Counter()
    for row in last[me]["tiles"]:
        for t in row:
            if not isinstance(t, dict):
                continue
            if t.get("kind") == "WEED" or t.get("crop") == "WEED":
                weeds += 1
            if t.get("animal"):
                crops["an_" + t["animal"]] += 1
            elif t.get("crop"):
                crops[t["crop"]] += 1
            standing += int(t.get("yield_units") or 0)
    owned = sum(1 for row in last[me]["tiles"] for t in row if t != "LOCKED")

    return dict(ep=ep, seed=info.get("seed"), seat=me, opp=names[them], armed=armed,
                opp_melon=opp_melon, ours=ours, theirs=theirs, crew=crew, weeds=weeds,
                standing=standing, crops=dict(crops), owned=owned,
                d3_bank=d3_bank, d3_fert=d3_fert)


def main():
    rows = []
    for f in sorted(glob.glob(str(pathlib.Path.home() / "Downloads" / "*.json"))):
        try:
            r = survey(f)
        except Exception as e:                                                # noqa: BLE001
            print(f"  {pathlib.Path(f).stem}: {e!r}", flush=True)
            continue
        if r:
            rows.append(r)
            print(f"  read {r['ep']}", flush=True)

    for armed in (True, False):
        arm = [r for r in rows if r["armed"] == armed]
        label = ("STRAWBERRY arm (tape 97466318, the one 9ab0f19 swapped in)" if armed
                 else "MELON arm (tape 92498144, unchanged by 9ab0f19)")
        print(f"\n{'=' * 100}\n{label} -- {len(arm)} games\n{'=' * 100}")
        if not arm:
            continue
        print(f"{'episode':>12} {'seed':>12} {'st':>3} {'oppMEL':>7} "
              f"{'ours':>10} {'theirs':>10} {'margin':>10}  {'crew d5-d8':>12} "
              f"{'wd':>3} {'own':>4}  opponent")
        for r in sorted(arm, key=lambda r: r["ours"] - r["theirs"]):
            c = "/".join(str(r["crew"].get(d, "-")) for d in (5, 6, 7, 8))
            print(f"{r['ep']:>12} {str(r['seed']):>12} {r['seat']:>3} {r['opp_melon']:>7} "
                  f"{r['ours']:>10,.0f} {r['theirs']:>10,.0f} "
                  f"{r['ours'] - r['theirs']:>10,.0f}  {c:>12} "
                  f"{r['weeds']:>3} {r['owned']:>4}  {r['opp'][:24]}")
        w = sum(1 for r in arm if r["ours"] > r["theirs"])
        print(f"    won {w}/{len(arm)}   "
              f"mean margin ${sum(r['ours'] - r['theirs'] for r in arm) / len(arm):,.0f}")
        print(f"    d3 bank/fert: {sorted({(int(r['d3_bank']), r['d3_fert']) for r in arm})}")


if __name__ == "__main__":
    main()
