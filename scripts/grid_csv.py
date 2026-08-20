"""The per-day grid as CSV: one ROW per day, one column per field, ours / tape / difference.

The terminal grid in `breakdown.py` is transposed -- fields down the side, days across -- because
that is what fits an 80-column terminal. It is also what makes it unreadable past about day 10.
This writes the same numbers the other way up, which is the orientation a spreadsheet sorts,
filters and charts.

It reuses `breakdown.run` rather than reimplementing it, so the numbers are the same numbers:
`sell`, `buy_product`, `buy_seed` and `buy_animal` are EXACT FILLS read per unit from `_commit_unit`
via `kagg/analysis/fills.py`; every other op column is an OFFER, and its header says so.

**The tape choice also chooses OUR OWN schedule** (`breakdown.py:330` hands `TAPES[tape]`'s schedule
straight to `make_agent`), so running this against Seb does not merely compare us to Seb -- it makes
our agent play Seb's four-quadrant plan. We ship Victor's. That is why `victor` is the default here.

    python -u scripts/grid_csv.py --tape victor    --days 30 --out data/logs/grid_victor.csv
    python -u scripts/grid_csv.py --tape kawashigi --days 30 --out data/logs/grid_kawashigi.csv
"""
import argparse
import collections
import csv
import importlib
import json
import pathlib
import sys

sys.path.insert(0, ".")

import scripts.breakdown as B

#: カワシギ is #1 on the ladder and had no entry in `breakdown.TAPES`. His best downloaded game:
#: $149,998 against Yusuke Hayashi, seated FIRST, `townCenterSellInterval = 24` -- the rebalanced
#: economy we actually play, unlike the `seb*` tapes. No schedule has been extracted from him, and
#: the schedule slot drives OUR agent rather than the tape column, so it stays on Victor's -- the
#: plan we ship. The tape column is his real actions either way.
B.TAPES.setdefault("kawashigi", ("data/seed_scripts/kawashigi/92498144.json",
                                 "data/seed_scripts/kawashigi/schedule.json", "カワシギ"))

COMPASS = {"NORTH", "SOUTH", "EAST", "WEST"}
#: Read per unit out of `_commit_unit`; everything else in the op set is what was emitted.
FILLS = {"SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default=B.DEFAULT_TAPE, choices=sorted(B.TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--module", default="schedule_agent")
    #: **The apples-to-apples arm.** By default the tape's own `TAPES` entry supplies the schedule
    #: OUR agent runs, and for `kawashigi` that is deliberately Victor's, because no schedule had
    #: been extracted from him. Comparing our Victor plan against his tape measures two different
    #: plans and cannot show where we execute his badly. Point this at his own extracted schedule
    #: and the two columns are running the same plan, so a divergence is ours.
    ap.add_argument("--schedule", default=None,
                    help="override the schedule OUR agent runs, e.g. "
                         "data/seed_scripts/kawashigi/schedule.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    B.schedule_agent = importlib.import_module("kagg.search." + args.module)

    replay, schedule, team = B.TAPES[args.tape]
    schedule = args.schedule or schedule
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(replay)
    horizon = args.days + 1

    # **The shop draw comes from the recording, not from the seed.** `env_config` already took the
    # sell interval off the tape; the draw is the other half of the same economy, and building it
    # from a fixed seed made the tape's actions meet a town wanting different things. Un-injected,
    # カワシギ's $149,998 season replayed as $68,080 and the wool rule -- which reads
    # `unlocked_shops` directly -- fired on a draw neither player ever saw.
    shops = B.recorded_shops(replay)

    his, his_ops, _hc, _h0 = B.run(lambda: B.tape_policy(replay, team, 0),
                                   lambda: B.tape_policy(replay, team, 1),
                                   args.seed, args.weeds, stop_day=horizon, economy=economy,
                                   shops=shops)
    ours, our_ops, _oc, _o0 = B.run(lambda: (lambda a: (lambda o, t: a(o)))(
                                        B.schedule_agent.make_agent(thin, 0, router=True)),
                                    lambda: B.tape_policy(replay, team, 1),
                                    args.seed, args.weeds, stop_day=horizon, economy=economy,
                                    shops=shops)

    state = ([("money", "money"), ("hands", "hands"), ("owned", "tiles"), ("pen", "pens"),
              ("weed", "weeds")]
             + [("crop_" + c, c.lower()) for c in B.CROPS]
             + [("an_" + x, x.lower()) for x in B.ANIMALS])
    ops = sorted((set(B.OPS) | FILLS | {"BUY_LAND", "HIRE", "OTHER"}) - COMPASS)

    header = ["day"]
    for _k, lab in state:
        header += ["%s_ours" % lab, "%s_tape" % lab, "%s_diff" % lab]
    for o in ops:
        tag = "fill" if o in FILLS else "offer"
        lab = "%s(%s)" % (o.lower(), tag)
        header += ["%s_ours" % lab, "%s_tape" % lab, "%s_diff" % lab]

    rows = []
    for d in range(args.days):
        row = [d]
        for k, _lab in state:
            a, b = ours[d][k], his[d][k]
            row += [a, b, a - b]
        for o in ops:
            a, b = our_ops[d][o], his_ops[d][o]
            row += [a, b, a - b]
        rows.append(row)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)

    diffs = sum(1 for r in rows for i, v in enumerate(r)
                if i and header[i].endswith("_diff") and v)
    print("%s   tape=%s (%s)  seed=%s  economy=%s" % (out, args.tape, team, args.seed, economy))
    print("  %d days x %d fields, %d differing cells" % (len(rows), len(state) + len(ops), diffs))


if __name__ == "__main__":
    main()
