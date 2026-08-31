"""Which opponent behaviour actually beats us? Sweep the holding strategy, not the crop mix.

## What each arm changes, and what would have to be true for it to win

Read this before the numbers, because the last carrot sweep cost 12,096 seasons answering a question
its own field could not pose.

An arm is a `heuristic` opponent varying three dials:

    filler_crop   which product it accumulates      CARROT/TOMATO are on the `hinge` curve,
                                                    STRAWBERRY and WHEAT are not
    hold_days     how long before the close it      0 = sell as you harvest, our pool's only mode
                  stops selling entirely            until today
    max_tiles     how much ground it commits

**An arm wins only if the town's book for its crop is ABOVE the hinge knee when it finally sells.**
The price runs away only when the shops have drained the town's stock past `T` and nobody has
replenished it (`reference/kaggriculture.py:61-73`, `HINGE_GAIN = 8.0`). So an arm that plants its
hinge crop from day one keeps its own book under the knee and is a null BY CONSTRUCTION -- exactly
what a first attempt at this opponent did: it held 66 units and carrot never left $23-28, while the
real opponent it was copied from reached $498.

That is the falsifiable prediction this sweep tests: **hold_days should only pay for a crop the arm
does not supply early**, and it should pay far more for CARROT/TOMATO than for STRAWBERRY/WHEAT.
If hold_days pays uniformly across crops, the hinge is not the mechanism and this whole line is
wrong.

## Why it is worth running at all

Our pool's nine members all sell as they harvest, so no arm about WITHHOLDING has ever been
measurable here. `CARROT_OPP_MAX = 7` shipped on that null. And the gate has read 94.4% for a week
because `(8 * 1.0 + 0.5) / 9` is exactly 0.9444 -- it is saturated, not stable.

Measured on real ladder losses, the opponent's terminal shed beat ours in four of six games, and in
98495047 the difference ($31,116) was the whole $29,384 margin.

    python -u scripts/what_beats_us.py --seeds 3 --out data/logs/what_beats_us.csv
"""

import argparse
import collections
import itertools
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
FILLERS = ("CARROT", "TOMATO", "STRAWBERRY", "WHEAT")
HOLD_DAYS = (0, 6, 12)


def arms():
    """`(name, param-overrides)` for every cell of the grid."""
    for crop, hold in itertools.product(FILLERS, HOLD_DAYS):
        yield (f"{crop.lower()}_h{hold}",
               {"filler_crop": crop, "melon_tiles": 0, "strawberry_tiles": 0, "cow_tiles": 0,
                "max_tiles": 100, "hold_days": hold, "endgame_day": 29})


def play(us_path, opp_params, seed, us_seat):
    """One game: our built submission against a heuristic arm. Returns a row dict."""
    from kaggle_environments import make                                     # noqa: PLC0415

    from kagg.agents import heuristic                                        # noqa: PLC0415
    from kagg.arena.pool import BASELINE                                     # noqa: PLC0415

    p = dict(BASELINE)
    p.update(opp_params)
    opp = heuristic.make_agent(p)

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    agents = [str(us_path), opp] if us_seat == 0 else [opp, str(us_path)]
    env.run(agents)

    st = env.steps
    last = st[-1][0]["observation"]
    px = (last.get("market") or {}).get("prices") or {}
    banks = [st[-1][s]["observation"]["farms"][s]["money"] for s in (0, 1)]
    them = 1 - us_seat

    def shed_value(seat, step_i):
        pr = st[step_i][seat]["observation"]["private"]
        c = collections.Counter(pr.get("shed") or {})
        for inv in (pr.get("inventories") or []):
            c.update(inv)
        return sum(n * float(px.get(k, 0) or 0) for k, n in c.items() if k in px)

    d29 = min(29 * TPD, len(st) - 1)
    return {
        "seed": seed, "our_seat": us_seat,
        "ours": round(banks[us_seat]), "theirs": round(banks[them]),
        "margin": round(banks[us_seat] - banks[them]),
        "win": int(banks[us_seat] > banks[them]),
        "our_d29_shed": round(shed_value(us_seat, d29)),
        "their_d29_shed": round(shed_value(them, d29)),
        "close_price": round(float(px.get(opp_params["filler_crop"], 0) or 0)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="submission/e2500_close.py")
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--first-seed", type=int, default=700)
    ap.add_argument("--out", default="data/logs/what_beats_us.csv")
    a = ap.parse_args()

    seeds = list(range(a.first_seed, a.first_seed + a.seeds))
    grid = list(arms())
    total = len(grid) * len(seeds) * 2
    print(f"{len(grid)} arms x {len(seeds)} seeds x 2 seatings = {total} games", flush=True)
    print(f"agent: {a.agent}", flush=True)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    # Header first, then one flushed row per game: a sweep that writes at the end loses everything
    # when it is killed. 29,568 planned seasons once produced 0 rows in this repo.
    fh = out.open("w")
    cols = ["arm", "crop", "hold_days", "seed", "our_seat", "ours", "theirs", "margin",
            "win", "our_d29_shed", "their_d29_shed", "close_price"]
    fh.write(",".join(cols) + "\n")
    fh.flush()

    t0 = time.time()
    done = 0
    for name, params in grid:
        for seed in seeds:
            for us_seat in (0, 1):
                try:
                    r = play(REPO / a.agent, params, seed, us_seat)
                except Exception as e:                                       # noqa: BLE001
                    print(f"  {name} seed {seed} seat {us_seat}: {e!r}", flush=True)
                    continue
                r.update(arm=name, crop=params["filler_crop"], hold_days=params["hold_days"])
                fh.write(",".join(str(r[c]) for c in cols) + "\n")
                fh.flush()
                done += 1
                print(f"  {done:>3}/{total} {name:<16} seed {seed} seat {us_seat}  "
                      f"margin {r['margin']:>+9,}  close ${r['close_price']:>4}  "
                      f"their shed ${r['their_d29_shed']:>8,}", flush=True)
    fh.close()
    print(f"\n{done} games in {time.time() - t0:.0f}s -> {out}", flush=True)


if __name__ == "__main__":
    main()
