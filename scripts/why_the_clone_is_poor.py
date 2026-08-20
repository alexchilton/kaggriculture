"""The clone matches the teacher's ops and banks a seventh of his money. Find the day it breaks.

`clone_play.py` grades OPS. It counts them from the action dict BEFORE `env.step`, so a HARVEST on
a bare tile scores as a HARVEST: the grid measures what the clone ASKED for, never what the board
recorded. A tape can therefore read 6.5% wrong and earn nothing.

This prints, per day, the three things that turn ops into money, clone against teacher:

    money      the bank at hour 0
    shops      the town's unlocked shops -- the price drain the tape sells into
    hands      hired crew: `_do_hire` fails SILENTLY on a thin bank (kaggriculture.py:691)
    quads      owned quadrants: BUY_LAND is refused silently too

`configuration.seed` is None in every downloaded replay, so `env.reset()` draws a fresh one. The
start board is fixed, but weeds and shop-unlock timing are not -- and the tape sells at fixed hours
into whatever town happens to exist.

    python -u scripts/why_the_clone_is_poor.py --team カワシギ --holdout 94439800 --arm 0.02 \
        --dirs data/seed_scripts/downloads_2026-08-14to16 ...
"""

import argparse
import collections
import importlib.util
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

_spec = importlib.util.spec_from_file_location("clone_play", REPO / "scripts" / "clone_play.py")
CP = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CP)


def _get(ob, key):
    """Observations are dict-like in the replay and attribute-like live."""
    if isinstance(ob, dict) and key in ob:
        return ob[key]
    return getattr(ob, key, None)


def tile_census(farm):
    c = collections.Counter()
    for row in (farm.get("tiles") or []):
        for cell in row:
            if cell is None:
                c["locked"] += 1
            elif isinstance(cell, dict):
                if "animal" in cell:
                    c["animal"] += 1
                else:
                    c[str(cell.get("kind"))] += 1
            else:
                c[str(cell)] += 1
    return c


def farm_state(ob, seat):
    farm = ((_get(ob, "farms") or [None, None])[seat]) or {}
    shops = sorted(str(v) for v in ((_get(ob, "town") or {}).get("unlocked_shops") or []))
    priv = _get(ob, "private") or {}
    shed = {k: v for k, v in (priv.get("shed") or {}).items() if v}
    seeds = {k: v for k, v in (priv.get("seeds") or {}).items() if v}
    return (float(farm.get("money") or 0.0),
            len(farm.get("hands") or []),
            len(farm.get("unlocked_quadrants") or []),
            shops, shed, seeds, tile_census(farm))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--dirs", nargs="+", required=True)
    ap.add_argument("--holdout", required=True)
    ap.add_argument("--days", type=int, default=29)
    ap.add_argument("--arm", type=float, default=None)
    args = ap.parse_args()

    from kaggle_environments import make

    paths = []
    for dd in args.dirs:
        paths.extend(sorted(pathlib.Path(dd).glob("*.json")))
    held = next(p for p in paths if p.stem == args.holdout)
    d = json.loads(held.read_text())
    names = [str(n) for n in ((d.get("info") or {}).get("TeamNames") or [])]
    seat = names.index(args.team)
    other = 1 - seat

    if args.arm is not None:
        paths = CP.arm_mates(paths, args.team, args.holdout, args.arm)
        print("arm: %d games within %.2f of the holdout's mix" % (len(paths), args.arm), flush=True)
    ut, mt, games = CP.build_tables(paths, args.team, args.holdout)
    print("tape from %d games, holding out %s\n" % (games, args.holdout), flush=True)
    CP.TAPE_MODE = True
    clone = CP.make_clone((ut, mt))

    # The teacher's own day-by-day state, straight out of his replay.
    his = {}
    steps = d["steps"]
    for i, step in enumerate(steps):
        prev = (steps[i - 1][seat] or {}).get("observation") or {} if i else {}
        if "day" not in prev or "farms" not in prev:
            continue
        day = int(prev.get("day", 0) or 0)
        if int(prev.get("hour", 0) or 0) == 12:
            his[day] = farm_state(prev, seat)

    cfg = dict(d.get("configuration") or {})
    cfg.pop("steps", None)
    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    opp = [((f[other] or {}).get("action") or {}) for f in d["steps"][1:]]

    mine = {}
    # Emitted vs executed: the same op counted before the step and after it.
    emitted, executed = collections.Counter(), collections.Counter()
    for t in range(719):
        if env.done:
            break
        ob = env.state[seat].observation
        day = int(ob.get("day", 0) or 0)
        if day > args.days:
            break
        # Sample at MIDDAY, not hour 0. Crew is rented daily, so a dawn sample reads zero hands
        # every day of the season and says nothing -- an error already made once in `money.py`.
        if int(ob.get("hour", 0) or 0) == 12:
            mine[day] = farm_state(ob, seat)
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        m = clone(ob, seat)
        acts = [m["farmer"]] + list(m["hands"])[:n[seat]]
        for a in acts:
            emitted[CP.op_label(a)] += 1
        before = json.dumps((ob.get("farms") or [None])[seat])
        st = opp[t] if t < len(opp) else {}
        a2 = [None, None]
        a2[seat] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[seat]],
                    "market": m["market"]}
        a2[other] = {"farmer": st.get("farmer") or ["PASS"],
                     "hands": list(st.get("hands") or [])[:n[other]],
                     "market": st.get("market") or []}
        env.step(a2)
        after = json.dumps((env.state[seat].observation.get("farms") or [None])[seat])
        if after != before:
            executed["board changed"] += 1

    blank = (0, 0, 0, [], {}, {}, collections.Counter())

    def cens(c):
        return "crop %-3d weed %-3d empty %-3d pen %-3d lock %-3d" % (
            c.get("PLANT", 0), c.get("WEED", 0), c.get("EMPTY", 0) + c.get("SOIL", 0),
            c.get("animal", 0) + c.get("PASTURE", 0), c.get("locked", 0))

    print("== bank, crew and board, sampled at HOUR 12 ==\n")
    print("%-4s %10s %10s  %4s %4s  %4s %4s  %s"
          % ("day", "clone $", "his $", "hand", "his", "quad", "his", "clone board / his board"))
    print("-" * 130)
    for day in range(args.days + 1):
        a, b = mine.get(day) or blank, his.get(day) or blank
        if a is blank and b is blank:
            continue
        print("%-4d %10s %10s  %4d %4d  %4d %4d  %s"
              % (day, format(int(a[0]), ","), format(int(b[0]), ","),
                 a[1], b[1], a[2], b[2], cens(a[6])))
        print("%-4s %10s %10s  %4s %4s  %4s %4s  %s" % ("", "", "", "", "", "", "", cens(b[6])))

    print("\n== shed and seeds at HOUR 12 (clone, then teacher) ==\n")
    for day in range(args.days + 1):
        a, b = mine.get(day) or blank, his.get(day) or blank
        if a is blank and b is blank:
            continue
        print("d%-3d shed %-58s seeds %s" % (day, a[4], a[5]))
        print("     shed %-58s seeds %s" % (b[4], b[5]))

    print("\n== town ==\n")
    for day in range(args.days + 1):
        a, b = mine.get(day) or blank, his.get(day) or blank
        if a is blank and b is blank:
            continue
        sa = ",".join(s[:4] for s in a[3]) or "-"
        sb = ",".join(s[:4] for s in b[3]) or "-"
        print("d%-3d %-42s | %s%s" % (day, sa, sb, "   <<<" if sa != sb else ""))

    print("\nturns where the board changed after our step: %d of %d"
          % (executed["board changed"], sum(emitted.values()) and t + 1))


if __name__ == "__main__":
    main()
