"""Is the solver zone idling? Count PASS per zone, in our wins against our losses.

`cover._apply_precomputed` keys a precomputed stop on `(tile, ops)`. A stop whose tile no longer
carries the ops it was solved for is **dropped silently** -- `solved_days.py` and `q4_branch` both
say so. So a board that has drifted from the solved trajectory does not fail loudly: the route
simply gets shorter and units stand still.

That predicts a specific, checkable signature: in games we lose, the d12-d23 zone should show more
idle unit-turns than in games we win, and more than the neighbouring zones.

An idle turn is a unit whose action is PASS (or absent). Counted over unit-turns, not turns, so a
day with 11 hands weighs more than a day with 4 -- which is right, because an idle hand at d20 is
the thing being measured.

Also reports the WORK mix per zone, because "not PASS" is not the same as "doing something useful":
a unit walking all day emits MOVE, not PASS.
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
ZONES = (("d0-d3", 0, 3), ("d4-d11 tape", 4, 11),
         ("d12-d23 solver", 12, 23), ("d24-d29 planner", 24, 29))
#: Ops that change the board or the book. Everything else is positioning or nothing.
WORK = {"PLANT", "WATER", "HARVEST", "FEED", "CARE", "DIG", "FERTILIZE",
        "PLACE_ANIMAL", "PLACE", "PICKUP", "DROP", "BUILD"}


def one(path):
    rec = json.loads(pathlib.Path(path).read_text())
    info = rec.get("info") or {}
    names = info.get("TeamNames") or []
    steps = rec.get("steps") or []
    if US not in names or not steps:
        return None
    me = names.index(US)
    them = 1 - me

    per = {z: collections.Counter() for z, _a, _b in ZONES}
    for t, st in enumerate(steps):
        day = t // TPD
        zone = next((z for z, a, b in ZONES if a <= day <= b), None)
        if zone is None:
            continue
        a = st[me].get("action")
        if not isinstance(a, dict):
            continue
        acts = [a.get("farmer")] + list(a.get("hands") or [])
        for act in acts:
            per[zone]["units"] += 1
            op = (act or ["PASS"])[0]
            if op == "PASS" or not act:
                per[zone]["pass"] += 1
            elif op in WORK:
                per[zone]["work"] += 1
            else:
                per[zone]["move"] += 1

    last = steps[-1][0]["observation"]["farms"]
    return dict(ep=pathlib.Path(path).stem, per=per,
                margin=float(last[me]["money"]) - float(last[them]["money"]))


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

    wins = [r for r in rows if r["margin"] > 0]
    losses = [r for r in rows if r["margin"] <= 0]
    print(f"{len(rows)} games: {len(wins)} won, {len(losses)} lost\n")

    def block(group, label):
        print(f"{'=' * 84}\n{label} -- {len(group)} games\n{'=' * 84}")
        print(f"{'zone':<18} {'unit-turns':>11} {'PASS':>9} {'idle %':>8} "
              f"{'work %':>8} {'move %':>8}")
        for z, _a, _b in ZONES:
            u = sum(r["per"][z]["units"] for r in group)
            p = sum(r["per"][z]["pass"] for r in group)
            w = sum(r["per"][z]["work"] for r in group)
            m = sum(r["per"][z]["move"] for r in group)
            if not u:
                continue
            print(f"{z:<18} {u:>11,} {p:>9,} {100*p/u:>7.1f}% "
                  f"{100*w/u:>7.1f}% {100*m/u:>7.1f}%")
        print()

    block(wins, "GAMES WE WON")
    block(losses, "GAMES WE LOST")

    print(f"{'=' * 84}\nper-game solver idle %, worst first\n{'=' * 84}")
    print(f"{'episode':>12} {'margin':>12} {'solver idle':>12} {'planner idle':>13} "
          f"{'tape idle':>11}")
    def idle(r, z):
        u = r["per"][z]["units"]
        return 100 * r["per"][z]["pass"] / u if u else 0.0
    for r in sorted(rows, key=lambda r: -idle(r, "d12-d23 solver")):
        print(f"{r['ep']:>12} {r['margin']:>12,.0f} {idle(r,'d12-d23 solver'):>11.1f}% "
              f"{idle(r,'d24-d29 planner'):>12.1f}% {idle(r,'d4-d11 tape'):>10.1f}%")


if __name__ == "__main__":
    main()
