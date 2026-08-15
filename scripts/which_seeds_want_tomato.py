"""Per seed: how far the town drains TOMATO and CARROT when neither farm grows them.

**Tomato and carrot are the only two products whose undersupply curve is `hinge`**, which is
quadratic past `u = x/T > 1`. That makes their upside unbounded in a way no other product's is:

    deficit    -400    -800   -1200
    TOMATO     $300  $1,884  $5,004      base $60
    CARROT      $66    $267    $906      base $35
    MELON      $303    $309    $312      base $250, `log` -- never spikes
    WHEAT       $45     $53     $60      base $25,  `sqrt` -- never spikes

So the question "is tomato worth planting" has no season-wide answer. It is worth planting exactly
when the town is draining it and nobody is supplying it -- and the top players supply zero tomato
across 40+ recorded games, so the supply side is empty by construction. The 2026-08-15 note that
tomato is viable in ~50% of games is a statement about the SHOP DRAW, not about the crop.

This measures the draw directly. Both seats play the shipped agent, which grows no tomato, so the
tomato price is the town's appetite alone. A seed whose tomato price climbs to $300 by d12 with
nobody growing it is a seed where a few tomato tiles are worth more than the whole rest of the
board; a seed that sits at $60 is one where tomato can never be more than a wash.

The price is readable live from `observation["market"]["prices"]`, so anything this finds is
detectable in-game rather than needing a seed lookup table.

    python -u scripts/which_seeds_want_tomato.py --seeds 1 2 3 4 5 6 7 8
"""
import argparse
import importlib
import importlib.util
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

import reference.kaggriculture as KG

REPO = pathlib.Path(__file__).resolve().parent.parent
WATCH = ("TOMATO", "CARROT", "EGG", "MELON", "STRAWBERRY", "WHEAT", "MILK", "WOOL")


def probe(seed, opponent):
    """One season, both seats shipped, recording each product's price at four checkpoints."""
    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")
    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))

    sp = importlib.util.spec_from_file_location("opp", opponent)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    opp = mod.agent

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)

    marks, shops = {}, []
    for t in range(719):
        o = env.state[0].observation
        if t % 24 == 0:
            day = t // 24
            if day in (6, 12, 20, 29):
                marks[day] = {p: o["market"]["prices"].get(p, 0) for p in WATCH}
            if day <= 6:
                shops = list(o["town"]["unlocked_shops"])
        env.step([me(o, t), opp(env.state[1].observation, t)])
        if env.done:
            break
    o = env.state[0].observation
    marks[29] = {p: o["market"]["prices"].get(p, 0) for p in WATCH}
    return dict(seed=seed, marks=marks, shops_by_d6=shops,
                money=env.steps[-1][0]["reward"], opp=env.steps[-1][1]["reward"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(1, 21)))
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--one", type=int, default=None, help="internal: probe a single seed as JSON")
    a = ap.parse_args()

    if a.one is not None:                       # child process, one measurement, then exit
        print(json.dumps(probe(a.one, a.opponent)))
        return

    # One OS process per seed: the first run in a process differs from later ones (measured
    # 2026-08-15, $134,665 then $94,523 three times on identical inputs).
    def child(s):
        p = subprocess.run(
            [sys.executable, "-u", __file__, "--one", str(s), "--opponent", a.opponent],
            capture_output=True, text=True, cwd=REPO,
            env={**__import__("os").environ, "PYTHONPATH": "."})
        try:
            r = json.loads(p.stdout.strip().splitlines()[-1])
            # json turns int keys into strings on the way through the pipe
            r["marks"] = {int(k): v for k, v in r["marks"].items()}
            return r
        except Exception:
            return dict(seed=s, failed=(p.stderr or p.stdout)[-200:])

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        rows = list(ex.map(child, a.seeds))

    print("Both seats play the shipped agent, which grows NO tomato. So the TOMATO column is the "
          "town's appetite alone.\n")
    print(f"{'seed':>5}{'TOMATO d6':>11}{'d12':>7}{'d20':>7}{'d29':>7}"
          f"{'CARROT d12':>12}{'d29':>7}{'EGG d29':>9}{'  shops unlocked by d6'}")
    hot = []
    for r in sorted(rows, key=lambda r: r.get("seed", 0)):
        if r.get("failed"):
            print(f"{r['seed']:>5}  FAILED {r['failed'][:80]}")
            continue
        m = r["marks"]
        print(f"{r['seed']:>5}{m[6]['TOMATO']:>11,}{m[12]['TOMATO']:>7,}{m[20]['TOMATO']:>7,}"
              f"{m[29]['TOMATO']:>7,}{m[12]['CARROT']:>12,}{m[29]['CARROT']:>7,}"
              f"{m[29]['EGG']:>9,}   {','.join(r['shops_by_d6']) or '-'}")
        if m[12]["TOMATO"] >= 2 * KG.MARKET_PARAMS["TOMATO"]["base"]:
            hot.append((r["seed"], m[12]["TOMATO"], m[20]["TOMATO"]))

    base = KG.MARKET_PARAMS["TOMATO"]["base"]
    print(f"\nTOMATO base is ${base}. A seed at ${base} all season can never pay -- 8 units a tile "
          f"over 11 days is ~$400 gross, the same per watering-day as the wheat it replaces.")
    if hot:
        print(f"\nSEEDS WHERE TOMATO IS ALREADY 2x BASE AT d12 WITH NOBODY GROWING IT:")
        for s, p12, p20 in hot:
            print(f"  seed {s:>3}  d12 ${p12:,}  d20 ${p20:,}   <-- run the swap matrix HERE")
    else:
        print("\nNo seed in this set drains tomato. Swapping tiles to tomato on these seeds "
              "measures nothing about tomato -- it measures the wheat it displaced.")


if __name__ == "__main__":
    main()
