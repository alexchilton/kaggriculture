"""Replay a tape's own actions for the first N days, then hand the farm to our agent.

## Why this exists

Every measurement of our selling used to be confounded by our opening. We reached day 11 with a
different board from the tape -- a parcel late, fewer pens, a smaller herd -- so a late-season
deficit could always be blamed upstream, and usually was.

Replaying the tape's own actions from turn 0 removes that. The starting board is deterministic (both
sides open on `wheat 14, melon 3, cow 2, sheep 2`) and with weeds off the only unmatched RNG is the
shop unlock order, so the replay reproduces the tape's board field for field. On `seb1326`, seed 11:

    day    owned      plant       pen      animal        ours/his
      4    25/25     17/17       8/8        6/6
      5    50/50      3/3        8/8        7/7      parcel 1, bought d4
      7    75/75     22/22      10/10       7/7      parcel 2, bought d6
     11   100/100    43/43      17/17      14/14     parcel 3, bought d10   <- handover

At the handover we hold $3,950 against his $3,864. Anything measured after that is our selling.

**It only works from day 0.** Splicing days 4-10 instead is a wipeout -- $345 final, herd at zero by
day 7 -- because hand ops are position-dependent (`["FEED"]` applies wherever that unit is standing)
and by day 4 our crew is not where the tape's crew is. See
`docs/the_shed_destroys_the_harvest_2026-08-08.md`.

## What it reports

    destroyed   `_drop_inventories_to_shed` (`kaggriculture.py:813`) banks every hand into the shed
                at the rollover up to capacity and DISCARDS the overflow, so
                `(shed + hands)@dusk - shed@dawn` is exactly what was binned. This is the number the
                whole late season turns on: 331 units with `PRICE_AWARE_SELL_CAP` off, 82 with it on.
    turns@cap   turns spent with a full shed, the window in which a HARVEST also silently loses the
                difference (`kaggriculture.py:470`).

## Examples

    python -u scripts/handover.py                          # d0-d10 replayed, ours from d11
    python -u scripts/handover.py --handover 0             # control: our agent drives everything
    python -u scripts/handover.py --weeds 0.005            # does the splice survive real weeds?
    python -u scripts/handover.py --set PRICE_AWARE_SELL_CAP=False
    python -u scripts/handover.py --seeds 11,12,13,14      # a sweep, one line each
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

DAYS = 30
FIELDS = ("money", "hands", "owned", "plant", "weed", "pen", "animal", "shed")


def board(obs, seat):
    """The eight scalars `scripts/fidelity.py` uses, so the two harnesses are comparable."""
    farm = obs["farms"][seat]
    n = collections.Counter()
    for row in farm["tiles"]:
        for c in row:
            if c == "LOCKED":
                continue
            n["owned"] += 1
            if isinstance(c, dict):
                if c.get("kind") == "PLANT":
                    n["plant"] += 1
                elif c.get("kind") == "WEED":
                    n["weed"] += 1
                else:
                    n["pen"] += 1
                if c.get("animal"):
                    n["animal"] += 1
    n["money"] = int(farm["money"])
    n["hands"] = len(farm.get("hands") or [])
    n["shed"] = sum(int(v) for v in ((obs.get("private") or {}).get("shed") or {}).values())
    return n


def play(tape, seed, handover, weeds, capacity, quiet):
    """One season. Returns the final banks and the per-day trace."""
    from kaggle_environments import make

    replay, schedule, team = TAPES[tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}

    raw = json.loads(pathlib.Path(replay).read_text())
    tseat = raw["info"]["TeamNames"].index(team)
    steps = raw["steps"][1:]
    idle = {"farmer": ["PASS"], "hands": [], "market": []}
    tape_act = [dict(farmer=((s[tseat] or {}).get("action") or {}).get("farmer") or ["PASS"],
                     hands=list(((s[tseat] or {}).get("action") or {}).get("hands") or []),
                     market=list(((s[tseat] or {}).get("action") or {}).get("market") or []))
                for s in steps]

    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds})
    env.reset(2)
    # `start_day` so the days the tape played are treated as met rather than as ten days of missed
    # sell rows -- see `make_agent`. `handover=0` means we play everything, so it stays None.
    ours = SA.make_agent(thin, 0, router=True, start_day=handover or None)
    opp = tape_policy(replay, team, 1)

    out = {"destroyed": 0, "at_cap": 0, "rows": [], "dusk": None}
    for t in range(24 * DAYS - 1):
        o0, o1 = env.state[0].observation, env.state[1].observation
        priv = o0.get("private") or {}
        total = sum(int(v) for v in (priv.get("shed") or {}).values())
        day, hour = t // 24, t % 24

        if hour == 0:
            if out["dusk"] is not None and out["dusk"] - total > 0:
                out["destroyed"] += out["dusk"] - total
            his = board(steps[t][tseat]["observation"], tseat) if t < len(steps) else None
            out["rows"].append((day, board(o0, 0), his))
        if total >= capacity:
            out["at_cap"] += 1

        a1 = opp(o1, t)
        if day < handover:
            # Our agent still sees every turn, so its per-day state is warm at the handover.
            ours(o0)
            a0 = dict(tape_act[t]) if t < len(tape_act) else idle
        else:
            a0 = ours(o0)

        out["dusk"] = total + sum(int(v) for iv in (priv.get("inventories") or [])
                                  for v in (iv or {}).values())
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])

    f = env.state[0].observation["farms"]
    out["ours"], out["opp"] = int(f[0]["money"]), int(f[1]["money"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb1326", choices=sorted(TAPES))
    ap.add_argument("--handover", type=int, default=11, help="first day OUR agent drives")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--seeds", default=None, help="comma-separated; one summary line each")
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--capacity", type=int, default=100, help="env `shedCapacity`, for the report")
    ap.add_argument("--set", action="append", default=[],
                    help="FLAG=True/False on `schedule_agent`, applied before the run")
    args = ap.parse_args()

    for kv in args.set:
        k, _, v = kv.partition("=")
        if not hasattr(SA, k):
            sys.exit(f"schedule_agent has no flag {k!r}")
        setattr(SA, k, {"True": True, "False": False}.get(v, v))
        print(f"  set {k} = {getattr(SA, k)!r}")

    seeds = [int(s) for s in args.seeds.split(",")] if args.seeds else [args.seed]
    for seed in seeds:
        r = play(args.tape, seed, args.handover, args.weeds, args.capacity, len(seeds) > 1)
        verdict = "WIN " if r["ours"] > r["opp"] else "LOSS"
        head = (f"seed {seed:>4}  handover d{args.handover}  weeds {args.weeds}  "
                f"ours ${r['ours']:>9,}  opp ${r['opp']:>9,}  {verdict}  "
                f"destroyed {r['destroyed']:>4}  turns@cap {r['at_cap']:>3}")
        print(head)
        if len(seeds) > 1:
            continue
        print("\n  ours / tape -- dawn state    (`hands` is read from the public farm view and is"
              " 0 for our own seat; ignore that column)")
        print(f"  {'day':>4} " + " ".join(f"{k:>13}" for k in FIELDS))
        for day, mine, his in r["rows"]:
            mark = "  <- ours from here" if day == args.handover else ""
            cells = " ".join(f"{mine[k]:>6}/{(his[k] if his else 0):>6}" for k in FIELDS)
            print(f"  {day:>4} {cells}{mark}")


if __name__ == "__main__":
    main()
