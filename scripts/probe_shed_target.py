"""`scripts/breakdown.py --diff` with the tape's own end-of-day shed injected into the schedule.

The sell rows are absolute counts read off the tape's board, so they only fit our board while the
two produce the same amount -- and they do not: we run 44 more CARE ops on the `seb` tape and finish
day 28 holding 67 milk to his 16, having met every milk row exactly. No rule written over `sells`
alone can close that, because closing it means selling down to a number the schedule does not carry.

This measures what happens if it does. `shed_dusk` is read straight out of the replay's
`private.shed` at the FOLLOWING dawn -- the same instant `breakdown.snap` samples, and after the env
has dropped every unit's inventory into the shed, so it is the exact figure the `sh:*` rows score.
The schedule on disk is NOT modified; the field is injected in memory.

    python -u scripts/probe_shed_target.py --tape seb --seed 11 --days 30
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import CROPS, ANIMALS, PRODUCTS, TAPES, TAPE_ONLY, run, tape_policy


def shed_dusk(replay, team, days):
    """`{day: {product: units}}` -- what he was holding when day `d` ended.

    Read at dawn of `d + 1`, not at hour 23 of `d`: `_drop_inventories_to_shed` runs overnight, so at
    hour 23 several units are still carrying produce that the shed has not seen yet. On the tape's
    day 14 that is 20 in the shed and 4 in pockets, and 24 is the number the breakdown compares.
    """
    d = json.loads(pathlib.Path(replay).read_text())
    seat = d["info"]["TeamNames"].index(team)
    steps = d["steps"][1:]
    out = {}
    for day in range(days):
        t = (day + 1) * 24
        if t >= len(steps):
            continue
        obs = (steps[t][seat] or {}).get("observation") or {}
        shed = (obs.get("private") or {}).get("shed") or {}
        out[day] = {p: int(shed.get(p, 0) or 0) for p in PRODUCTS}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--off", action="store_true", help="do not inject, i.e. reproduce the baseline")
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    if not args.off:
        for d, shed in shed_dusk(replay, team, args.days).items():
            if d in thin:
                thin[d]["shed_dusk"] = shed
    opp = lambda: tape_policy(replay, team, 1)

    his, _ = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours, _ = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)

    fields = ([("money", "money"), ("hands", "hands"), ("owned", "tiles"), ("pen", "pens"),
               ("weed", "weeds")]
              + [("crop_" + c, c.lower()[:6]) for c in CROPS]
              + [("an_" + x, x.lower()[:6]) for x in ANIMALS]
              + [("shed_" + p, "sh:" + p.lower()[:5]) for p in PRODUCTS])
    rows = [(lab, [(ours[d][k], his[d][k]) for d in range(args.days)]) for k, lab in fields]
    live = [(lab, c) for lab, c in rows if any(o != h for o, h in c)]

    print(f"shed_dusk injected: {not args.off}   tape {args.tape}   seed {args.seed}")
    head = "".join(f"{('d' + str(d)):>7}" for d in range(args.days))
    print(f"  {'field':<12}{head}{'days':>6}{'total':>9}")
    for lab, cells in live:
        body = "".join(f"{'' if o == h else f'{o - h:+d}':>7}" for o, h in cells)
        n = sum(1 for o, h in cells if o != h)
        print(f"  {lab:<12}{body}{n:>6}{sum(o - h for o, h in cells):>+9}")
    diff = sum(sum(1 for o, h in c if o != h) for _lab, c in live)
    print(f"\n  {diff} differing STATE cells over {len(fields)} fields x {args.days} days")
    print("  per-day: " + "  ".join(
        f"d{d}={sum(1 for _lab, c in live if c[d][0] != c[d][1])}" for d in range(args.days)))


if __name__ == "__main__":
    main()
