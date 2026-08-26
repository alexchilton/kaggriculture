"""Put a dollar value on the overnight rot, so the sell rule can be judged against it.

Three attempts at releasing the shed early have now measured NEGATIVE (-$4,385 for the paced
version recorded at `schedule_agent.py:4240`, -$7,617 for a full dump, -$533 metered to the
overflow), and every one of them was argued against the *price* it gives up. Nobody has ever
measured the thing on the other side of that trade: how much produce the dawn discard destroys,
and what it would have fetched.

**Where the rot actually happens.** Not in the shed -- stock in the shed persists. It is
`_drop_inventories_to_shed` (`reference/kaggriculture.py:843`, called at `:878`), which runs at
every dawn and deposits each unit's inventory "up to `capacity`; overflow is discarded". So the
units that die are the ones the CREW IS CARRYING at dusk, and they die because the shed had no
room for them.

That distinction decides whether a sell rule can help at all. Selling at h2 makes room in the
shed, but if harvesting refills that room before dusk the carry still overflows and the same units
still die -- we would have paid the price penalty and saved nothing.

**Avoiding the index bug.** An earlier pass tried to attribute carried units to the ACTING unit and
produced two contradictory answers, because the unit -> `private["inventories"]` index mapping was
wrong. This script never attributes anything to a unit. It sums ALL inventories, which is
well-defined regardless of ordering:

    destroyed_at_dawn = (shed_total_at_dusk + carried_total_at_dusk) - shed_total_at_dawn

Run it against two modules to compare a baseline with a candidate.
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
TAPES = {
    "kawashigi": ("data/seed_scripts/kawa_2026-08-24/97466318.json",
                  "data/seed_scripts/kawashigi/schedule.json", 1240813987),
    "kawa_straw": ("data/seed_scripts/kawa_2026-08-24/97466318.json",
                   "data/seed_scripts/kawa_straw/schedule.json", 468411728),
}


def run(module_name, tape_key):
    import breakdown as B
    from kaggle_environments import make

    tape_path, sched_path, seed = TAPES[tape_key]
    SA = importlib.import_module(f"kagg.search.{module_name}")
    B.schedule_agent = SA
    raw = json.loads((REPO / sched_path).read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads((REPO / tape_path).read_text())
    steps = rec["steps"]
    names = (rec.get("info") or {}).get("TeamNames") or []
    his = names.index("カワシギ") if "カワシギ" in names else 0

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, 0)

    prev = None          # (day, shed dict, carried dict) at the previous turn
    destroyed = collections.Counter()
    by_day = collections.Counter()

    for t in range(30 * TPD):
        o = env.state[0].observation
        priv = o.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        carried = collections.Counter()
        for inv in (priv.get("inventories") or []):
            for k, v in (inv or {}).items():
                carried[k] += int(v or 0)

        day, hour = t // TPD, t % TPD
        # At dawn the deposit has already run, so compare against the previous turn (dusk).
        if hour == 0 and prev is not None:
            _pd, pshed, pcarried = prev
            lost = (sum(pshed.values()) + sum(pcarried.values())) - sum(shed.values())
            if lost > 0:
                by_day[day - 1] = lost
                # Attribute per product by what the carry held; the env deposits in dict order,
                # so this is the composition of the carry, not a claim about which unit lost it.
                tot = sum(pcarried.values()) or 1
                for k, v in pcarried.items():
                    destroyed[k] += lost * v / tot

        prev = (day, shed, carried)

        n = len(o["farms"][0].get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n], "market": a["market"]}
        at = steps[t + 1][his].get("action") if t + 1 < len(steps) else None
        at = at if isinstance(at, dict) else {}
        n2 = len(o["farms"][1].get("hands") or [])
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n2],
                 "market": at.get("market") or []}
        env.step([mine, yours])
        if env.done:
            break

    money = float(env.state[0].observation["farms"][0]["money"])
    return destroyed, by_day, money


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modules", nargs="+", default=["schedule_agent"])
    ap.add_argument("--tape", default="kawa_straw")
    args = ap.parse_args()

    for mod in args.modules:
        destroyed, by_day, money = run(mod, args.tape)
        total = sum(destroyed.values())
        print(f"\n=== {mod}  on {args.tape} ===")
        print(f"  final bank            {money:>12,.0f}")
        print(f"  units destroyed       {total:>12,.1f}")
        if destroyed:
            print("  by product (share of the carry that overflowed):")
            for k, v in sorted(destroyed.items(), key=lambda kv: -kv[1]):
                if v > 0.05:
                    print(f"      {k:<12} {v:>8.1f}")
        if by_day:
            print("  by day (units lost at the following dawn):")
            print("     ", {d: v for d, v in sorted(by_day.items())})


if __name__ == "__main__":
    main()
