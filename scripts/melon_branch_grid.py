"""d0-d8, ours-with-the-melon-branch against the season it is meant to reproduce.

The branch installs his STRAWBERRY season (92466371) from d5. This prints our play against that
tape's own column, cell by cell, so the question "does the branch land his board" is answered on
the rows rather than on a season total.

Our agent is driven by the SHIPPED schedule (his melon season) plus the branch, which is exactly
what a submission does. The tape column is his strawberry season replayed against the same
opponent, so both columns face the same market.

The trigger is forced on rather than waited for: the tape's own opponent does not hold nine melon
tiles at d3, so the branch would stay quiet and the comparison would measure nothing.

    python -u scripts/melon_branch_grid.py --days 8
"""
import argparse
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from kagg.search import melon_branch as _MB          # noqa: E402

B3 = "data/seed_scripts/kawashigi/92466371.json"   # his strawberry season
A3 = "data/seed_scripts/kawashigi/92498144.json"   # his melon season
TEAM = "カワシギ"
#: `WATER` counts ACTIONS SUBMITTED. A second water on a tile the same day returns immediately
#: (`reference/kaggriculture.py:434`), so it costs the turn and changes nothing. `water_tiles` is
#: the row that means something: how many DISTINCT tiles were served. Measured d6, the two sides
#: read 17/19 on `WATER` and 16/16 on `water_tiles`.
ROWS = ("PLANT", "WATER", "water_tiles", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
        "BUILD_PASTURE", "PLACE", "BUY_SEED", "BUY_ANIMAL", "BUY_LAND", "HIRE", "SELL",
        "crop_MELON", "crop_STRAWBERRY", "crop_WHEAT", "weed", "pen", "hands", "money")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=8)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--arm", choices=("straw", "melon"), default="straw",
                    help="straw: branch armed, compared against 92466371. "
                         "melon: branch quiet, compared against 92498144.")
    a = ap.parse_args()

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    # The tape's own opponent does not hold nine melon at d3, so the trigger is forced
    # rather than waited for. 0 arms it on any opponent, 99 on none.
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (B3 if a.arm == "straw" else A3))
    opp = lambda: B.tape_policy(replay, TEAM, 1)                      # noqa: E731
    economy, shops = B.env_config(replay), B.recorded_shops(replay)

    # Positions are read from the SAME observation the action was built from -- not the previous
    # turn's, which is `day_ops.py`'s replay convention and is one turn stale for a live policy.
    def watch(policy, into):
        def step(o, t):
            act = policy(o, t)
            farm = o["farms"][0]
            at = [tuple(farm.get("farmer") or (4, 4))]
            for h in (farm.get("hands") or []):
                at.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
            n = len(farm.get("hands") or [])
            for u, a in enumerate([act["farmer"]] + list(act.get("hands") or [])[:n]):
                if a and a[0] == "WATER" and u < len(at):
                    into.setdefault(t // 24, set()).add(at[u])
            return act
        return step

    o_water, t_water = {}, {}

    def ours():
        agent = SA.make_agent(sched, 0)
        return watch(lambda o, t: agent(o), o_water)

    o_d, o_ops, _c, _dd = B.run(ours, opp, a.seed, a.weeds, stop_day=a.days + 1,
                                economy=economy, shops=shops)
    t_d, t_ops, _c2, _dd2 = B.run(lambda: watch(B.tape_policy(replay, TEAM, 0), t_water),
                                  opp, a.seed, a.weeds,
                                  stop_day=a.days + 1, economy=economy, shops=shops)
    for x in range(a.days + 1):
        o_d[x]["water_tiles"] = len(o_water.get(x, ()))
        t_d[x]["water_tiles"] = len(t_water.get(x, ()))

    which = ("92466371, his STRAWBERRY season, $147,059" if a.arm == "straw"
             else "92498144, his MELON season, $149,998")
    print(f"seed {a.seed}, weeds {a.weeds}, arm {a.arm!r}, tape {which}")
    print("cells are OURS/TAPE\n")
    mismatched = [0]
    print(f"{'row':>20}" + "".join(f"{'d' + str(x):>11}" for x in range(a.days + 1)))
    for r in ROWS:
        cells = []
        bad = False
        for x in range(a.days + 1):
            m = o_ops[x][r] if r.isupper() else o_d[x].get(r, 0)
            h = t_ops[x][r] if r.isupper() else t_d[x].get(r, 0)
            if isinstance(m, float):
                m, h = round(m), round(h)
            cells.append(f"{m}/{h}")
            bad = bad or m != h
        print(f"{r:>20}" + "".join(f"{c:>11}" for c in cells) + ("   <--" if bad else ""))
        mismatched[0] += sum(1 for x in range(a.days + 1)
                             if (o_ops[x][r] if r.isupper() else o_d[x].get(r, 0))
                             != (t_ops[x][r] if r.isupper() else t_d[x].get(r, 0)))


    total = len(ROWS) * (a.days + 1)
    print(f"\n{mismatched[0]} of {total} cells differ from the tape "
          f"({100 * mismatched[0] / total:.1f}%)  -- money counted, it never matches")


if __name__ == "__main__":
    main()
