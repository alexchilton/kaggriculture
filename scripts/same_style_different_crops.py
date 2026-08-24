"""Is SOUTA a different STYLE, or the same style with a different crop mix?

This repo has been wrong about that distinction before.
`CLAUDE.md`: *"The opponent pool is diverse in crop allocation, not in play style. Every member is
`heuristic.make_agent` with different dials -- same routing, hiring and sell cadence."*
Calling that "8 competing strategies" oversold it, and the agents that actually beat us differed in
**how** they played, not in what they planted.

So compare the two axes separately:

    CROP MIX     what is in the ground and in the pens
    PLAY STYLE   the op histogram, hires, land, and the sell cadence -- normalised per unit-turn,
                 so a player with more hands is not counted as more active

If two players match on style and differ on mix, the difference is a dial.
If they differ on style, it is a different agent.

`--no-animals` drops FEED, CARE, COLLECT and the pen builds from the histogram and renormalises, to
answer Alex's question directly: with the animals taken out, is the remaining play similar?
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
#: Read off a real replay, not guessed. Movement is four compass ops, not "MOVE"; the pen collect
#: is "COLLECT_FERTILIZER"; pens are built as "BUILD_PASTURE"/"BUILD_COOP" and stocked with "PLACE".
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
ANIMAL_OPS = {"FEED", "CARE", "PLACE", "BUILD_PASTURE", "BUILD_COOP"}
CROP_OPS = {"PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG"}
#: COLLECT_FERTILIZER is manure from a pen, so it is animal-side work even though what it yields is
#: an input to the crops.
FERT_OPS = {"COLLECT_FERTILIZER"}


def ops_of(steps, seat, days=30):
    """Histogram of the ops this seat submitted, plus market and structural counts."""
    ops = collections.Counter()
    market = collections.Counter()
    hires = land = 0
    for t in range(min(days * TPD, len(steps) - 1)):
        a = steps[t + 1][seat].get("action")
        if not isinstance(a, dict):
            continue
        acts = [a.get("farmer")] + list(a.get("hands") or [])
        for x in acts:
            if isinstance(x, (list, tuple)) and x:
                ops[x[0]] += 1
        for o in (a.get("market") or []):
            if isinstance(o, (list, tuple)) and o:
                market[o[0]] += 1
                if o[0] == "HIRE":
                    hires += 1
                elif o[0] == "BUY_LAND":
                    land += 1
    return ops, market, hires, land


def crops_at(steps, seat, day=25):
    t = min(day * TPD, len(steps) - 1)
    farm = steps[t][seat]["observation"]["farms"][seat]
    crop = collections.Counter()
    animal = collections.Counter()
    for row in (farm.get("tiles") or []):
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("crop"):
                crop[tile["crop"]] += 1
            if tile.get("animal"):
                animal[tile["animal"]] += 1
    return crop, animal


def profile(files, who, days, no_animals):
    ops = collections.Counter()
    market = collections.Counter()
    crop = collections.Counter()
    animal = collections.Counter()
    hires = land = n = 0
    money = 0.0
    for f in files:
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        # These directories also hold `schedule.json`, which is a plan and not a replay.
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if who not in names:
            continue
        seat = names.index(who)
        steps = rec["steps"]
        o, m, h, l = ops_of(steps, seat, days)
        c, an = crops_at(steps, seat)
        ops += o
        market += m
        crop += c
        animal += an
        hires += h
        land += l
        money += (rec.get("rewards") or [0, 0])[seat]
        n += 1
    if not n:
        return None
    # Fold the four compass ops into one MOVE bucket -- the question is how much of the day is
    # walking, not which way.
    ops["MOVE"] = sum(ops.pop(k, 0) for k in list(MOVES))
    if no_animals:
        for k in list(ops):
            if k in ANIMAL_OPS or k in FERT_OPS:
                del ops[k]
    total = sum(ops.values()) or 1
    return {"n": n, "ops": ops, "total": total, "market": market,
            "hires": hires / n, "land": land / n, "crop": crop, "animal": animal,
            "money": money / n}


def show(label, p, keys):
    if p is None:
        print(f"{label:>12}  no games")
        return
    row = "  ".join(f"{100.0 * p['ops'].get(k, 0) / p['total']:>5.1f}" for k in keys)
    print(f"{label:>12} {p['n']:>3} {p['money']:>10,.0f}  {row}   "
          f"{p['hires']:>5.1f} {p['land']:>4.1f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--no-animals", action="store_true")
    a = ap.parse_args()

    dl = sorted(glob.glob("/Users/alexchilton/Downloads/*.json"))
    ours = sorted(glob.glob(str(REPO / "data/seed_scripts/losses/*.json")))
    kawa = []
    for name in ("kawashigi", "kawashigi_b3", "kawashigi_q4c"):
        kawa += sorted(glob.glob(str(REPO / f"data/seed_scripts/{name}/*.json")))

    who = [("SOUTA", dl, "SOUTA Sakurai"),
           ("kawashigi", kawa, "カワシギ"),
           ("us", ours, "alex chilton")]

    keys = [k for k in ("MOVE", "PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG",
                        "FEED", "CARE", "COLLECT_FERTILIZER", "PLACE", "PICKUP", "DROP", "PASS")
            if not (a.no_animals and (k in ANIMAL_OPS or k in FERT_OPS))]

    print(f"op mix as % of all ops submitted{'  (animals removed)' if a.no_animals else ''}\n")
    print(f"{'who':>12} {'n':>3} {'mean $':>10}  "
          + "  ".join(f"{k[:5]:>5}" for k in keys) + "   hires land")
    profs = {}
    for label, files, name in who:
        p = profile(files, name, a.days, a.no_animals)
        profs[label] = p
        show(label, p, keys)

    print("\ncrop tiles at d25 (mean per game)")
    for label, _f, _n in who:
        p = profs[label]
        if p is None:
            continue
        c = ", ".join(f"{k} {v / p['n']:.1f}" for k, v in p["crop"].most_common(6))
        an = ", ".join(f"{k} {v / p['n']:.1f}" for k, v in p["animal"].most_common(4))
        print(f"{label:>12}  crops: {c or '-'}")
        print(f"{'':>12}  pens : {an or '-'}")

    print("\nmarket orders submitted (mean per game)")
    for label, _f, _n in who:
        p = profs[label]
        if p is None:
            continue
        m = ", ".join(f"{k} {v / p['n']:.0f}" for k, v in p["market"].most_common(6))
        print(f"{label:>12}  {m}")


if __name__ == "__main__":
    main()
