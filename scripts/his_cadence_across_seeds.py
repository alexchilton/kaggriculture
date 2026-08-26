"""Force Kawashigi's sell cadence onto our board, across seeds, against a live opponent.

Alex's question, asked three times and still not answered with a number on more than one board:
he sells 1,397 units on 137 turns to our 1,419 on 59, and his selling is worth ~$7k more than ours
over the solver zone. **What happens if we just do what he does?**

Three arms, so the answer is not one number with no mechanism behind it:

- `ours`   -- our own market logic, untouched. The control.
- `his`    -- his FILLS replayed verbatim on the same turns, clamped to what our shed actually
              holds. Our unit actions are unchanged; only the market orders are his.
- `his-nf` -- the same, with FERTILIZER removed from his list. This tests the claim made in
              `docs/the_sell_side_2026-08-25.md` that his cadence fails on our board because
              **his fertilizer is surplus and ours is feedstock**: he sells 205 units of it over
              the season, and we need it to grow the crop. If that claim is right, `his-nf` should
              recover most of the gap to `ours`. If `his-nf` is still far behind, the claim is
              wrong and the cadence is failing for some other reason.

**Fills, not offers.** The action stream re-posts the same quota every turn, so replaying it
verbatim asks for the day's whole allowance 24 times -- the first attempt clamped away 2,589 of
2,649 units (98%) and measured a harness artefact. `data/logs/kawa_fill_schedule.json` is built
from his shed deltas on turns where his money rose.

*Known impurity in that file:* the shed also falls when he PLACES an animal or CONSUMES a product,
so `SHEEP 2` and part of `MELON 8` are not sales. They are dropped by the `SELLABLE` filter or are
too small to move the result, but the file is a lower bound on precision, not a clean ledger.

    python -u scripts/his_cadence_across_seeds.py --range 700 8 --opponent contrarian \
        | tee data/logs/his_cadence_across_seeds.log
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
import time
from concurrent.futures import ProcessPoolExecutor

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
ARMS = ("ours", "his", "his-nf")


def _play(job):
    """One season. Returns (ours, theirs, fill_turns, units_sold, asked, clamped, shed_by_day)."""
    arm, seed, opponent, lo, hi, module_name = job
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}
    fills = json.loads((REPO / "data/logs/kawa_fill_schedule.json").read_text())

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)

    fill_turns = units_sold = asked = clamped = 0
    shed_by_day = {}
    # **Where the money is read matters.** The arm only acts on d12-d23, so a d29 bank charges the
    # d24-d29 live planner with whatever board the arm handed it. `bank_at_zone_end` is the bank the
    # moment his cadence stops; the pair of numbers separates "his selling is worse" from "the
    # planner cannot recover from a shed pinned at the cap".
    bank_at_zone_end = shed_at_zone_end = None
    prev_shed = prev_money = None

    for t in range(30 * TPD):
        o0 = env.state[0].observation
        o1 = env.state[1].observation
        priv = o0.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        money = float(o0["farms"][0]["money"])
        if prev_shed is not None and money > prev_money:
            d = sum(max(0, prev_shed.get(k, 0) - shed.get(k, 0))
                    for k in set(prev_shed) | set(shed))
            if d > 0:
                fill_turns += 1
                units_sold += d
        prev_shed, prev_money = shed, money

        day = t // TPD
        if t % TPD == 0:
            shed_by_day[day] = sum(shed.values())
            if day == hi + 1 and bank_at_zone_end is None:
                bank_at_zone_end = money
                shed_at_zone_end = sum(shed.values())

        a0 = me(o0, env.configuration)
        market = a0["market"]
        if arm != "ours" and lo <= day <= hi:
            # **Only the SELLs are his.** `_process_market` carries HIRE, BUY_LAND, BUY_SEED,
            # BUY_PRODUCT and BUY_ANIMAL on the same channel (`reference/kaggriculture.py:930`
            # onward), so replacing the whole list switches our hiring and purchasing OFF for the
            # twelve days of the zone. The first version of this did exactly that and measured a
            # season with no crew growth and no seed, which is not a cadence.
            his_sells = []
            for prod, q in (fills.get(str(t)) or {}).items():
                if prod not in SA.SELLABLE:
                    continue
                if arm == "his-nf" and prod == "FERTILIZER":
                    continue
                asked += int(q)
                take = min(int(q), shed.get(prod, 0))
                clamped += int(q) - take
                if take > 0:
                    his_sells.append(["SELL", prod, take])
            # Splice his block in at the position of our FIRST sell and drop ours. Order matters:
            # orders settle in slot order, so a purchase funded by an earlier sell must keep its
            # sell in front of it (`schedule_agent:3062`). Appending at the end would refuse it.
            market, placed = [], False
            for o in (a0["market"] or []):
                is_sell = isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL"
                if is_sell:
                    if not placed:
                        market.extend(his_sells)
                        placed = True
                    continue
                market.append(o)
            if not placed:
                market.extend(his_sells)
            market = market[:10]                      # maxMarketOrdersPerTurn

        n0 = len(o0["farms"][0].get("hands") or [])
        mine = {"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0], "market": market}
        yours = them(o1, env.configuration)
        env.step([mine, yours])
        if env.done:
            break

    farms = env.state[0].observation["farms"]
    return (float(farms[0]["money"]), float(farms[1]["money"]),
            fill_turns, units_sold, asked, clamped, shed_by_day,
            float(bank_at_zone_end or 0.0), int(shed_at_zone_end or 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None, help="comma-separated seed list")
    ap.add_argument("--range", nargs=2, type=int, default=None, metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--zone", default="12-23")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="data/logs/his_cadence_across_seeds.csv")
    args = ap.parse_args()

    lo, hi = (int(x) for x in args.zone.split("-"))
    if args.seeds:
        seeds = [int(x) for x in args.seeds.split(",")]
    elif args.range:
        seeds = list(range(args.range[0], args.range[0] + args.range[1]))
    else:
        seeds = list(range(700, 708))

    jobs = [(arm, s, args.opponent, lo, hi, args.module) for arm in ARMS for s in seeds]
    print(f"{len(ARMS)} arms x {len(seeds)} seeds vs {args.opponent}, "
          f"his cadence on d{lo}-d{hi} = {len(jobs)} seasons, {args.workers} workers")
    print(f"seeds {seeds}")
    print(f"rows -> {args.out}\n", flush=True)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("arm,seed,ours,theirs,win,fill_turns,units_sold,asked,clamped,"
             "bank_at_zone_end,shed_at_zone_end\n")
    fh.flush()

    got = {}
    zone = {}
    zshed = {}
    agg = collections.defaultdict(lambda: [0, 0, 0.0, 0, 0, 0, 0, 0.0, 0])
    shed_track = {}
    clock = time.perf_counter()

    runner = (ProcessPoolExecutor(max_workers=args.workers) if args.workers > 1 else None)
    results = (runner.map(_play, jobs) if runner else (_play(j) for j in jobs))
    for job, r in zip(jobs, results):
        arm, seed = job[0], job[1]
        ours, theirs, turns, units, asked, clamped, shed_by_day, zbank, zshedn = r
        win = 1 if ours > theirs else 0
        fh.write(f"{arm},{seed},{ours:.0f},{theirs:.0f},{win},{turns},{units},{asked},{clamped},"
                 f"{zbank:.0f},{zshedn}\n")
        fh.flush()
        got[(arm, seed)] = ours
        zone[(arm, seed)] = zbank
        zshed[(arm, seed)] = zshedn
        a = agg[arm]
        a[0] += win
        a[1] += 1
        a[2] += ours
        a[3] += turns
        a[4] += units
        a[5] += asked
        a[6] += clamped
        a[7] += zbank
        a[8] += zshedn
        shed_track.setdefault(arm, shed_by_day)
        print(f"  {arm:<7} seed {seed:<6} d{hi + 1} bank {zbank:>9,.0f}  d29 bank {ours:>10,.0f}  "
              f"turns {turns:>3}  units {units:>5}  clamped {clamped:>5}", flush=True)
    if runner:
        runner.shutdown()
    fh.close()

    # **Two banks, because the arm only touches d12-d23.** `d{hi+1}` is the bank the moment his
    # cadence stops; `d29` includes the live planner cleaning up after it. If the gap is already
    # open at d{hi+1}, the selling is what lost it. If it opens after, the planner is what could
    # not recover.
    print(f"\n{'arm':<9}{'win':>7}{'d' + str(hi + 1) + ' bank':>12}{'d29 bank':>12}"
          f"{'shed d' + str(hi + 1):>11}{'fill turns':>12}{'units':>9}{'asked':>9}{'clamped':>9}")
    for arm in ARMS:
        w, n, money, turns, units, asked, clamped, zbank, zshedn = agg[arm]
        if not n:
            continue
        print(f"{arm:<9}{w / n:>6.0%}{zbank / n:>12,.0f}{money / n:>12,.0f}{zshedn / n:>11.0f}"
              f"{turns / n:>12.0f}{units / n:>9.0f}{asked / n:>9.0f}{clamped / n:>9.0f}")

    n0 = max(1, agg["ours"][1])
    base_d29 = agg["ours"][2] / n0
    base_zone = agg["ours"][7] / n0
    print(f"\n{'arm':<9}{'delta at d' + str(hi + 1):>16}{'delta at d29':>16}"
          f"{'planner zone':>15}")
    for arm in ARMS[1:]:
        n = agg[arm][1]
        if not n:
            continue
        dz = agg[arm][7] / n - base_zone
        dt = agg[arm][2] / n - base_d29
        print(f"{arm:<9}{dz:>+16,.0f}{dt:>+16,.0f}{dt - dz:>+15,.0f}")

    print(f"\n{'seed':<9}" + "".join(f"{a + ' d' + str(hi + 1):>16}" for a in ARMS)
          + "".join(f"{a + ' d29':>16}" for a in ARMS))
    for s in seeds:
        print(f"{str(s):<9}"
              + "".join(f"{zone.get((a, s), 0):>16,.0f}" for a in ARMS)
              + "".join(f"{got.get((a, s), 0):>16,.0f}" for a in ARMS))

    print(f"\nshed at dawn, day -> units (one representative season per arm)")
    for arm in ARMS:
        if arm in shed_track:
            row = shed_track[arm]
            print(f"  {arm:<8}" + " ".join(f"d{d}:{row[d]}" for d in sorted(row) if d % 2 == 0))

    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
