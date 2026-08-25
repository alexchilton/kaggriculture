"""Read the live herd counter on a real season and find where the 18th animal is authorised.

The schedule builds 14 pens and buys 14 animals, all by d11, and buys nothing after. We finish with
14 placed and 4 stranded in the shed, so 18 were bought. The extra order lands on d12 -- the first
day after the d4-d11 tape replay.

`_herd_split(want_total, bought, day, hour, unlocked_shops, last_day)` is handed `state["bought"]`
itself, so patching it records the agent's OWN purchase counter rather than a reconstruction. The
buy loop then asks for `want_total[a] - state["bought"][a]` of each species, so those two numbers
are the whole story: if `bought` reads low at d12, the loop buys the difference.

Also reports whether the q4 (four-quadrant) latch armed, because a board that thinks it has four
quadrants has more pens to fill than one that never bought the land.
"""

import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24


def main():
    import breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    seen = {}
    live_split = SA._herd_split

    def spy(want_total, bought, day, hour, unlocked_shops, last_day=29):
        out = live_split(want_total, bought, day, hour, unlocked_shops, last_day)
        # First reading of each day wins: the buy loop runs at h0 with the counter it will act on.
        seen.setdefault(day, (dict(want_total), dict(bought), dict(out)))
        return out

    SA._herd_split = spy
    try:
        env = make("kaggriculture", configuration={"seed": 0}, debug=False)
        env.reset(2)
        a0, a1 = SA.make_agent(sched, 0), SA.make_agent(sched, 1)
        buys = collections.Counter()
        for t in range(30 * TPD):
            o0, o1 = env.state[0].observation, env.state[1].observation
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o1["farms"][1].get("hands") or [])
            x, y = a0(o0), a1(o1)
            for od in (x["market"] or []):
                if od and od[0] == "BUY_ANIMAL":
                    buys[(t // TPD, t % TPD, od[1])] += int(od[2]) if len(od) > 2 else 1
            env.step([{"farmer": x["farmer"], "hands": list(x["hands"] or [])[:n0],
                       "market": x["market"]},
                      {"farmer": y["farmer"], "hands": list(y["hands"] or [])[:n1],
                       "market": y["market"]}])
            if env.done:
                break
    finally:
        SA._herd_split = live_split

    print("q4 latch armed:", bool(getattr(SA._Q4.BRANCH, "armed", None)),
          " melon latch key:", SA._MB.BRANCH.armed_key,
          " q4 key:", SA._Q4.BRANCH.armed_key)

    season = collections.Counter()
    for dd in sched:
        for a, q in (sched[dd].get("animals_bought") or {}).items():
            season[a] += int(q)
    print(f"schedule: {dict(season)} = {sum(season.values())} animals, "
          f"{sum(int(sched[d].get('builds', 0) or 0) for d in sched)} pens\n")

    print(f"{'day':>4} | {'want_total (season)':>24} | {'state[bought]':>22} | "
          f"{'split out':>22} | orders that day")
    for d in sorted(seen):
        wt, bt, out = seen[d]
        od = {k[2]: v for k, v in buys.items() if k[0] == d}
        print(f"{d:>4} | {str(wt):>24} | {str(bt):>22} | {str(out):>22} | {od or ''}")

    print("\nBUY_ANIMAL orders emitted, (day, hour, species) -> qty  "
          "[re-posted turns inflate this; the DAY is what matters]:")
    for k in sorted(buys):
        print("   ", k, buys[k])


if __name__ == "__main__":
    main()
