"""Which seeds unlock the YARN STORE early enough to arm the four-quadrant branch.

The q4 branch is not a better plan to run always -- it is a plan for one kind of draw. Three top
players (Kawashigi, Emon xu, Yura) go to four quadrants and a sheep-heavy herd when the yarn store
appears by d3-d6, and stay at three otherwise. So the branch fires on a minority of games, and a
sweep that runs it on every seed measures something nobody would ship.

**The scan must play real agents.** The shop draw comes off the same `random.Random` that weed
spawning consumes, so a PASS-only game advances the stream differently and reports a shop list the
real game never sees. That is not hypothetical: it silently passed an entire identity test, where
seed 0 scanned as early-yarn and plays as `['BAKERY', 'PET_CAFE']`.

It stops at d7, because the trigger is read by d6 and the remaining 23 days cannot change it. That
makes it ~4x cheaper than a full season and is the only reason scanning 100 seeds is practical.

    python -u scripts/find_the_yarn_seeds.py --seeds 1 100
"""
import argparse
import collections
import importlib
import importlib.util
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
TRIGGER = "YARN_STORE"
LOOK_BY_DAY = 6


def scan(seed, opponent):
    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")
    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))

    sp = importlib.util.spec_from_file_location("opp", opponent)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    first_seen = {}
    for t in range((LOOK_BY_DAY + 1) * 24):
        o = env.state[0].observation
        for name in o["town"]["unlocked_shops"]:
            first_seen.setdefault(name, t // 24)
        env.step([me(o, t), mod.agent(env.state[1].observation, t)])
        if env.done:
            break
    return dict(seed=seed, shops=first_seen,
                armed=first_seen.get(TRIGGER) is not None
                and first_seen[TRIGGER] <= LOOK_BY_DAY)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs=2, default=[1, 64], metavar=("LO", "HI"))
    ap.add_argument("--opponent", default="data/sweep/frozen_1186_opponent.py")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="data/logs/yarn_seeds.json")
    ap.add_argument("--one", type=int, default=None, help="internal: scan one seed as JSON")
    a = ap.parse_args()

    if a.one is not None:
        print(json.dumps(scan(a.one, a.opponent)))
        return

    seeds = list(range(a.seeds[0], a.seeds[1] + 1))

    def child(s):
        p = subprocess.run([sys.executable, "-u", __file__, "--one", str(s),
                            "--opponent", a.opponent],
                           capture_output=True, text=True, cwd=REPO,
                           env={**__import__("os").environ, "PYTHONPATH": "."})
        try:
            return json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            return dict(seed=s, failed=(p.stderr or p.stdout)[-160:])

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        rows = sorted(ex.map(child, seeds), key=lambda r: r["seed"])

    armed = [r["seed"] for r in rows if r.get("armed")]
    ok = [r for r in rows if not r.get("failed")]
    freq = collections.Counter(n for r in ok for n in r["shops"])

    print(f"scanned {len(ok)} seeds to d{LOOK_BY_DAY}, opponent {a.opponent}\n")
    print(f"{TRIGGER} by d{LOOK_BY_DAY}: {len(armed)}/{len(ok)} seeds "
          f"= {len(armed)/max(1,len(ok)):.0%}")
    print(f"armed seeds: {armed}\n")
    print("shop frequency in the first 7 days:")
    for name, n in freq.most_common():
        print(f"  {name:<20}{n:>4}/{len(ok)}  {n/max(1,len(ok)):>5.0%}")
    json.dump({"armed": armed, "rows": rows}, open(REPO / a.out, "w"), indent=1)
    print(f"\nwrote {a.out}")
    print("Use `armed` as the q4 arm's seed set and the rest as the control. A q4 plan that also "
          "wins on unarmed seeds is not a branch -- it is just a better tape, which is a bigger "
          "and less likely claim.")


if __name__ == "__main__":
    main()
