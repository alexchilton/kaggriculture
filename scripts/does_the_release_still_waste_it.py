"""Re-run the two downloaded games on the current build and check the two wastes directly.

Both were read off games played by submission 55764542 on 2026-08-25:

    99067358   seed 0, mirror (validation)   546 CARROT seeds held at the bell, 45 ever planted
    99071595   seed 1976966647, our seat 1   2 COW + 2 SHEEP in the shed from d12, never placed

The carrot swap was cut in `76fb0ab`, so the first should now be zero excess. NOTHING has been
changed about the animals, so the second is expected to still be there -- this run is to confirm the
mechanism survives the carrot removal and the re-solve, not to claim a fix.

`--mirror` plays our agent against itself on the given seed, which is what a Kaggle validation
episode is. Otherwise the recorded opponent's actions are replayed from the file, verbatim, in their
own seat.
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24


def _agent(seat):
    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    return SA.make_agent(sched, seat), sched


def play(seed, rec=None, seat=0, mirror=False):
    """Returns (money_ours, money_theirs, per-day rows for our seat)."""
    import us_in_his_seat as U
    from kaggle_environments import make

    ours, sched = _agent(seat)
    theirs = _agent(1 - seat)[0] if mirror else None
    steps = (rec or {}).get("steps") or []
    them = 1 - seat
    cfg = dict((rec or {}).get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)

    rows = {}
    placed_ops = collections.Counter()
    for t in range(30 * TPD):
        o = env.state[seat].observation
        day = int(o.get("day", 0) or 0)
        n_us = len(o["farms"][seat].get("hands") or [])
        a = ours(o)
        for act in [a["farmer"]] + list(a["hands"] or [])[:n_us]:
            if act and act[0] in ("PLACE_ANIMAL", "PLACE") and len(act) > 1:
                placed_ops[(day, act[1])] += 1
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        if mirror:
            o2 = env.state[them].observation
            n2 = len(o2["farms"][them].get("hands") or [])
            b = theirs(o2)
            yours = {"farmer": b["farmer"], "hands": list(b["hands"] or [])[:n2],
                     "market": b["market"]}
        else:
            n2 = len(o["farms"][them].get("hands") or [])
            at = U._recorded(steps, t, them)
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n2],
                     "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])

        if int(o.get("hour", 0) or 0) == 23:
            priv = o.get("private") or {}
            f = o["farms"][seat]
            cow = sheep = weeds = 0
            for row in f["tiles"]:
                for x in row:
                    if not isinstance(x, dict):
                        continue
                    if x.get("animal") == "COW":
                        cow += 1
                    if x.get("animal") == "SHEEP":
                        sheep += 1
                    if x.get("kind") == "WEED" or x.get("crop") == "WEED":
                        weeds += 1
            shed = priv.get("shed") or {}
            seeds = priv.get("seeds") or {}
            rows[day] = dict(
                carrot_seed=int(seeds.get("CARROT", 0) or 0),
                wheat_seed=int(seeds.get("WHEAT", 0) or 0),
                shed_cow=int(shed.get("COW", 0) or 0),
                shed_sheep=int(shed.get("SHEEP", 0) or 0),
                cow_tiles=cow, sheep_tiles=sheep, weeds=weeds,
                money=float(f["money"]))
        if env.done:
            break

    f = env.state[seat].observation["farms"]
    return float(f[seat]["money"]), float(f[them]["money"]), rows, placed_ops


def report(label, seed, ours, theirs, rows, placed):
    print(f"\n=== {label}   seed {seed}")
    print(f"    ours ${ours:,.0f}   theirs ${theirs:,.0f}   "
          f"{'WIN' if ours > theirs else 'LOSS'} by ${abs(ours - theirs):,.0f}")
    print(f"    {'day':>4} {'CARROT_seed':>12} {'WHEAT_seed':>11} {'shed_COW':>9} "
          f"{'shed_SHEEP':>11} {'cow_tiles':>10} {'sheep_tiles':>12} {'weeds':>6} {'money':>10}")
    for d in sorted(rows):
        if d < 10 and not any(rows[d][k] for k in ("carrot_seed", "shed_cow", "shed_sheep")):
            continue
        r = rows[d]
        print(f"    {d:>4} {r['carrot_seed']:>12} {r['wheat_seed']:>11} {r['shed_cow']:>9} "
              f"{r['shed_sheep']:>11} {r['cow_tiles']:>10} {r['sheep_tiles']:>12} "
              f"{r['weeds']:>6} {r['money']:>10,.0f}")
    last = rows[max(rows)]
    stranded = last["shed_cow"] + last["shed_sheep"]
    print(f"    ANIMALS: {last['cow_tiles'] + last['sheep_tiles']} placed, {stranded} stranded "
          f"in the shed  (${last['shed_cow'] * 400 + last['shed_sheep'] * 500:,} of stock)")
    print(f"    CARROT SEED at the bell: {last['carrot_seed']}  "
          f"(${last['carrot_seed'] * 20:,} if never sown)")
    print(f"    PLACE ops by day: {dict(sorted(placed.items()))}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="'mirror' or 'ladder'")
    a = ap.parse_args()

    if a.only in ("", "mirror"):
        o, t, rows, pl = play(0, mirror=True)
        report("99067358 re-run: mirror, the validation condition", 0, o, t, rows, pl)

    if a.only in ("", "ladder"):
        p = pathlib.Path("/Users/alexchilton/Downloads/99071595.json")
        rec = json.loads(p.read_text())
        names = rec["info"]["TeamNames"]
        seat = names.index("alex chilton")
        seed = rec["info"]["seed"]
        o, t, rows, pl = play(seed, rec=rec, seat=seat)
        report(f"99071595 re-run: our seat {seat} vs the recorded {names[1 - seat]}",
               seed, o, t, rows, pl)


if __name__ == "__main__":
    main()
