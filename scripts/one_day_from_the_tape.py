"""Play ONE day from the leader's raw actions and our planner everywhere else.

## Why

At d5 dusk our board and his are identical on seed 11 -- melon 12/12, strawberry 4/4, wheat 3/3,
weed 0/0, pen 6/6, money 43/43. Two players in the same position, so his d6 actions are legal for
us, unit for unit and turn for turn. If we replay them and d6 still does not match, the problem is
not the planner's choices; if it does match, this measures exactly what a perfect d6 is worth to
d7, d8 and the season.

This is a MEASUREMENT, not a proposal to ship a tape. It answers "how much is this day worth"
before any more time goes into the planner that produces it.

## What can still drift, and it is worth reading before trusting a null

- `_do_hire` fails silently on a thin bank (`reference:691`), and a missed hire shifts every later
  hand index. The replay is indexed by unit slot, so that would scramble the rest of the day.
- Money-gated actions slide. We sell into the same book he does, so his replayed bank is not his
  real bank -- measured at d4 h22, $718 real against $683 replayed, enough to refuse a parcel.
- A PLANT with no seed that turn no-ops silently and the tile stays empty for every later action
  scripted onto it.

    python -u scripts/one_day_from_the_tape.py --day 6
    python -u scripts/one_day_from_the_tape.py --day 6 --days 8
"""
import argparse
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

MELON_SEASON = "data/seed_scripts/kawashigi/92498144.json"
STRAWBERRY_SEASON = "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"
TPD = 24
ROWS = ("PLANT", "WATER", "HARVEST", "FEED", "CARE", "COLLECT_FERTILIZER", "DIG",
        "BUILD_PASTURE", "PLACE", "BUY_SEED", "BUY_ANIMAL", "BUY_LAND", "HIRE", "SELL",
        "crop_MELON", "crop_STRAWBERRY", "crop_WHEAT", "weed", "pen", "hands", "money")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="melon")
    ap.add_argument("--day", default="6",
                    help="days to take from the tape: '6', '0-3', or '0,1,2,3'")
    ap.add_argument("--days", type=int, default=8, help="how many days of grid to print")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    a = ap.parse_args()

    spec = str(a.day)
    if "-" in spec:
        lo, hi = spec.split("-")
        tape_days = set(range(int(lo), int(hi) + 1))
    else:
        tape_days = {int(x) for x in spec.split(",") if x.strip()}

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if a.arm == "straw" else MELON_SEASON))
    opp = lambda: B.tape_policy(replay, TEAM, 1)                      # noqa: E731
    economy, shops = B.env_config(replay), B.recorded_shops(replay)

    def hybrid():
        """Ours every turn except `--day`, where the leader's own actions are played instead."""
        agent = SA.make_agent(sched, 0)
        tape = B.tape_policy(replay, TEAM, 0)

        def step(o, t):
            mine = agent(o)                 # always stepped, so its per-day state stays honest
            if t // TPD in tape_days:
                return tape(o, t)
            return mine
        return step

    h_d, h_ops, _c, _dd = B.run(hybrid, opp, a.seed, a.weeds, stop_day=a.days + 1,
                                economy=economy, shops=shops)
    t_d, t_ops, _c2, _dd2 = B.run(lambda: B.tape_policy(replay, TEAM, 0), opp, a.seed, a.weeds,
                                  stop_day=a.days + 1, economy=economy, shops=shops)

    print(f"seed {a.seed}, weeds {a.weeds}, arm {a.arm!r}, "
          f"days {sorted(tape_days)} PLAYED FROM THE TAPE")
    print("cells are OURS(hybrid)/TAPE\n")
    print(f"{'row':>20}" + "".join(f"{'d' + str(x):>11}" for x in range(a.days + 1)))
    bad_total = 0
    for r in ROWS:
        cells, bad = [], False
        for x in range(a.days + 1):
            m = h_ops[x][r] if r.isupper() else h_d[x].get(r, 0)
            h = t_ops[x][r] if r.isupper() else t_d[x].get(r, 0)
            if isinstance(m, float):
                m, h = round(m), round(h)
            cells.append(f"{m}/{h}")
            bad = bad or m != h
            bad_total += 1 if m != h else 0
        print(f"{r:>20}" + "".join(f"{c:>11}" for c in cells) + ("   <--" if bad else ""))
    total = len(ROWS) * (a.days + 1)
    print(f"\n{bad_total} of {total} cells differ ({100 * bad_total / total:.1f}%)")


if __name__ == "__main__":
    main()
