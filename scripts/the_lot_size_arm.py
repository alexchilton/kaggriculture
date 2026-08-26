"""Same volume, same products, same days -- only the LOT SIZE changes. One variable.

The last hypothesis of 2026-08-25 that has not already been contradicted.

We sell about 1,442 units on about 65 fill turns, which is a mean lot of ~22 units. `market_price`
walks down as each unit commits, and 22 is exactly where that starts to bite:

    units into the book    +1    +2    +5   +10   +20   +50
    WOOL                  200   200   199   194   177    55
    MILK                  158   156   150   139   118    55
    STRAWBERRY            118   116   110   101    82    24

So every 22-unit wool lot is taken at about $177 where the first unit was worth $200. Kawashigi's
mean lot is 10.6 over 137 turns, and that is the ONE property of his selling never tested on its
own: `kawa_shape` changed his turns AND the product choice at the same time, so it could not
separate them.

**What this arm changes, and nothing else.** The agent's own sell decisions are taken as given --
same products, same days, same total quantity. Each order is capped at `--lot` units, and whatever
does not fit is carried to the next turn and offered again. Over a day the same stock leaves the
farm; it leaves in smaller pieces.

**What would have to be true for it to win.** Splitting a lot only helps if the book RECOVERS
between the pieces, which needs the town to drain it -- so the effect must be strongest where drain
is high and absent at drain 0. That is why it is swept across forced shop worlds rather than one
draw. If small lots win at drain 0 too, the mechanism is not the one claimed here and the result
should be distrusted.

The control is `--lot 999`, which cannot bind, and it must reproduce the shipped agent's bank. If
it does not, the harness is not neutral and no row means anything -- that check killed
`search_the_sell_schedule.py`, whose control banked $50,328 against a real $170,000.

    python -u scripts/the_lot_size_arm.py --range 700 6 --lots 999,20,12,8,5
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
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _play(job):
    lot, seed, opponent, from_day, module_name, shops = job
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)

    fired = 0
    fill_turns = units_sold = 0
    lots_seen = []
    prev_shed = prev_money = None

    for t in range(30 * TPD):
        if shops is not None:
            env.state[0].observation["town"]["unlocked_shops"] = list(shops)
        o0 = env.state[0].observation
        day = t // TPD
        priv = o0.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
        money = float(o0["farms"][0]["money"])
        if prev_shed is not None and money > prev_money:
            d = sum(max(0, prev_shed.get(k, 0) - shed.get(k, 0))
                    for k in set(prev_shed) | set(shed))
            if d > 0:
                fill_turns += 1
                units_sold += d
                lots_seen.append(d)
        prev_shed, prev_money = shed, money

        a0 = me(o0, env.configuration)
        market = a0["market"]

        if day >= from_day and lot < 999:
            # **Cap each SELL, keep everything else exactly where it was.** The order list also
            # carries HIRE, BUY_LAND, BUY_SEED and BUY_PRODUCT; rewriting the whole list switches
            # the farm's purchasing off, which is how an earlier arm measured a dead farm.
            capped = []
            for o in (a0["market"] or []):
                if (isinstance(o, (list, tuple)) and len(o) > 2
                        and str(o[0]).upper() == "SELL" and int(o[2]) > lot):
                    capped.append([o[0], o[1], int(lot)])
                else:
                    capped.append(o)
            if capped != list(a0["market"] or []):
                fired += 1
            market = capped

        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": market},
                  them(env.state[1].observation, env.configuration)])
        if env.done:
            break

    farms = env.state[0].observation["farms"]
    mean_lot = sum(lots_seen) / len(lots_seen) if lots_seen else 0.0
    return (float(farms[0]["money"]), float(farms[1]["money"]),
            fill_turns, units_sold, mean_lot, fired)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--lots", default="999,20,12,8,5")
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--from-day", type=int, default=12)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--worlds", default="CARROT:8,STRAWBERRY:6,WOOL:8")
    ap.add_argument("--out", default="data/logs/lot_size.csv")
    a = ap.parse_args()

    seeds = ([int(x) for x in a.seeds.split(",")] if a.seeds
             else list(range(a.range[0], a.range[0] + a.range[1])))
    lots = [int(x) for x in a.lots.split(",")]

    from force_the_shops import shops_for_drain
    worlds = [("as_drawn", None)]
    for spec in (a.worlds or "").split(","):
        spec = spec.strip()
        if not spec:
            continue
        prod, _, lvl = spec.partition(":")
        got_shops, got = shops_for_drain(prod, int(lvl))
        worlds.append((f"{prod.lower()}{got}", got_shops))
    labels = [w[0] for w in worlds]

    jobs = [(lot, s, a.opponent, a.from_day, a.module, w[1])
            for lot in lots for w in worlds for s in seeds]
    print(f"{len(lots)} lot caps x {len(worlds)} shop worlds x {len(seeds)} seeds "
          f"= {len(jobs)} seasons vs {a.opponent}, {a.workers} workers")
    print(f"lots {lots}   worlds {labels}   seeds {seeds}")
    print(f"rows -> {a.out}\n", flush=True)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("lot,world,seed,ours,theirs,win,fill_turns,units_sold,mean_lot,fired\n")
    fh.flush()

    cell = collections.defaultdict(lambda: [0, 0, 0.0, 0, 0, 0.0, 0])
    label_of = {id(w[1]): w[0] for w in worlds}
    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for job, r in zip(jobs, pool.map(_play, jobs)):
            lot, seed, world = job[0], job[1], label_of.get(id(job[5]), "as_drawn")
            ours, theirs, turns, units, mlot, fired = r
            win = 1 if ours > theirs else 0
            fh.write(f"{lot},{world},{seed},{ours:.0f},{theirs:.0f},{win},{turns},{units},"
                     f"{mlot:.1f},{fired}\n")
            fh.flush()
            c = cell[(lot, world)]
            c[0] += win
            c[1] += 1
            c[2] += ours
            c[3] += turns
            c[4] += units
            c[5] += mlot
            c[6] += fired
            print(f"  lot {lot:<5}{world:<12} seed {seed:<5} fired {fired:>4} "
                  f"lot~{mlot:>5.1f}  ours {ours:>10,.0f}  units {units:>5}", flush=True)
    fh.close()

    print(f"\nturns the cap actually bound (0 = it never bound, so the row is the control)\n")
    print(f"{'lot cap':<10}" + "".join(f"{lab:>14}" for lab in labels))
    for lot in lots:
        print(f"{lot:<10}" + "".join(
            f"{(cell[(lot, lab)][6] / cell[(lot, lab)][1] if cell[(lot, lab)][1] else 0):>14.0f}"
            for lab in labels))

    print(f"\nmean bank, and delta against lot={lots[0]} in the SAME world\n")
    print(f"{'lot cap':<10}" + "".join(f"{lab:>22}" for lab in labels))
    for lot in lots:
        row = f"{lot:<10}"
        for lab in labels:
            w, n, money, turns, units, mlot, fired = cell[(lot, lab)]
            bw, bn, bmoney, _t, _u, _m, _f = cell[(lots[0], lab)]
            if not n or not bn:
                row += f"{'-':>22}"
                continue
            row += f"{money / n:>13,.0f}{money / n - bmoney / bn:>+9,.0f}"
        print(row)

    print(f"\nunits sold / fill turns / realised mean lot\n")
    print(f"{'lot cap':<10}" + "".join(f"{lab:>26}" for lab in labels))
    for lot in lots:
        row = f"{lot:<10}"
        for lab in labels:
            w, n, money, turns, units, mlot, fired = cell[(lot, lab)]
            row += (f"{units / n:>10,.0f}{turns / n:>8.0f}{mlot / n:>8.1f}" if n
                    else f"{'-':>26}")
        print(row)

    print("\nIf small lots only help where drain is high, the recovery mechanism is real.")
    print("If they help at drain 0 as well, something else is doing the work -- distrust it.")
    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
