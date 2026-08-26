"""Size every sale from the BOOK, not from a quota. The thing the shipped agent has never done.

`schedule_agent` sells a fixed per-day quota per product, read off a schedule row, gated to hour 16+
(`:2489`, `:4626`). It never looks at `obs["market"]["inventory"]`. In a game where price is a pure
function of that book (`reference/kaggriculture.py:192`), a rule that ignores it cannot be optimal --
that is structural, not a measurement.

**Why a price-impact cap and not a lot cap.** The lot-size arm found revenue per unit rising from
$116.7 to $126.2 as lots shrank, but a fixed unit cap is the wrong shape, because the same number of
units costs wildly different amounts of price on different curves:

    units into an untouched book      +8            +50
    WOOL   (sq, T=105)            -3%            -72%
    WHEAT  (log, T=400)           -4%            -12%
    MILK   (sqrt->linear, T=122)  -8%            -66%

Eight units is nearly free on wheat and nearly free on wool; fifty is nearly free on wheat and
ruinous on wool. So the quantity that matters is not "how many units" but "how much price am I
willing to give up", and that can only be computed from the live book.

**The rule.** Each turn, for each product, sell the largest `k` such that

    market_price(p, book_p + k)  >=  market_price(p, book_p) * (1 - impact)

which is a per-product, per-turn quantity derived entirely from the book. `--impact 1.0` disables
the cap and must reproduce the shipped agent -- that is the control, and if it does not reproduce,
nothing below it counts.

**Volume is preserved by a backlog**, carried across turns and across days. The v1 lot arm lost 30%
of its volume because it truncated and dropped the remainder, and losing volume costs ~$87k. The
backlog is retired by what actually FILLED, read from the shed delta after the step, never by what
was offered.

**`--from-hour` is a second axis and has to be.** `LATE_SELL_FROM_HOUR = 16` leaves 8 selling turns
a day; small lots need more turns than that, so a cap without extra turns is a volume cut wearing a
different hat. The 2x2 is swept rather than assumed.

    python -u scripts/sell_by_the_book.py --range 700 6 --impacts 1.0,0.10,0.05,0.02 --hours 16,8,0
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
    impact, from_hour, seed, opponent, from_day, module_name, shops = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    active = not (impact >= 1.0 and from_hour >= 16)
    backlog = collections.Counter()
    fired = 0

    def cap_for(p, book_p):
        """Largest k whose LAST unit still fetches at least (1 - impact) of the first unit's price.

        Computed from the environment's own `market_price`, walked one unit at a time exactly as
        `_process_market` commits them. Not a model of the curve -- the curve itself.
        """
        top = KG.market_price(p, book_p)
        floor = top * (1.0 - impact)
        k = 0
        while k < 200 and KG.market_price(p, book_p + k) >= floor:
            k += 1
        return max(1, k)

    cm = record_fills()
    fills = cm.__enter__()
    try:
        env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
        env.reset(2)
        me = SA.make_agent(sched, 0, router=True)
        them = _build(OPPONENTS[opponent], None)

        for t in range(30 * TPD):
            if shops is not None:
                env.state[0].observation["town"]["unlocked_shops"] = list(shops)
            o0 = env.state[0].observation
            day, hour = t // TPD, t % TPD
            priv = o0.get("private") or {}
            shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
            book = {k: int(v or 0) for k, v in
                    (((o0.get("market") or {}).get("inventory")) or {}).items()}

            a0 = me(o0, env.configuration)
            market = a0["market"]

            if active and day >= from_day:
                req = collections.Counter()
                for o in (a0["market"] or []):
                    if (isinstance(o, (list, tuple)) and len(o) > 2
                            and str(o[0]).upper() == "SELL"):
                        req[o[1]] += int(o[2])
                # The agent re-posts its unfilled remainder every turn, so this is a high-water
                # mark of intent, never a running sum.
                for p, n in req.items():
                    if n > backlog[p]:
                        backlog[p] = n

                new_sells = []
                if hour >= from_hour:
                    for p in SA.SELLABLE:
                        want = min(backlog[p], shed.get(p, 0))
                        if want <= 0:
                            continue
                        n = min(want, cap_for(p, book.get(p, 0)))
                        if n > 0:
                            new_sells.append(["SELL", p, int(n)])

                rebuilt, placed = [], False
                for o in (a0["market"] or []):
                    if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                        if not placed:
                            rebuilt.extend(new_sells)
                            placed = True
                        continue
                    rebuilt.append(o)
                if not placed:
                    rebuilt.extend(new_sells)
                rebuilt = rebuilt[:10]
                if rebuilt != list(a0["market"] or []):
                    fired += 1
                market = rebuilt

            n0 = len(o0["farms"][0].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                       "market": market},
                      them(env.state[1].observation, env.configuration)])

            if active and day >= from_day:
                after = {k: int(v or 0) for k, v in
                         ((env.state[0].observation.get("private") or {}).get("shed")
                          or {}).items()}
                for p in list(backlog):
                    gone = shed.get(p, 0) - after.get(p, 0)
                    if gone > 0:
                        backlog[p] = max(0, backlog[p] - gone)
            if env.done:
                break

        farms = env.state[0].observation["farms"]
        units = revenue = 0
        per_turn = collections.Counter()
        for d, h, op, item, price in fills.at_turn(0, op="SELL"):
            units += 1
            revenue += price
            per_turn[(d, h)] += 1
        turns = len(per_turn)
        mean_lot = (sum(per_turn.values()) / turns) if turns else 0.0
        return (float(farms[0]["money"]), float(farms[1]["money"]),
                units, revenue, turns, mean_lot, fired)
    finally:
        cm.__exit__(None, None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--impacts", default="1.0,0.10,0.05,0.02")
    ap.add_argument("--hours", default="16,8,0")
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--from-day", type=int, default=12)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--worlds", default="")
    ap.add_argument("--out", default="data/logs/sell_by_the_book.csv")
    a = ap.parse_args()

    seeds = ([int(x) for x in a.seeds.split(",")] if a.seeds
             else list(range(a.range[0], a.range[0] + a.range[1])))
    impacts = [float(x) for x in a.impacts.split(",")]
    hours = [int(x) for x in a.hours.split(",")]

    worlds = [("as_drawn", None)]
    if a.worlds:
        from force_the_shops import shops_for_drain
        for spec in a.worlds.split(","):
            spec = spec.strip()
            if not spec:
                continue
            prod, _, lvl = spec.partition(":")
            got_shops, got = shops_for_drain(prod, int(lvl))
            worlds.append((f"{prod.lower()}{got}", got_shops))
    labels = [w[0] for w in worlds]

    jobs = [(imp, hr, s, a.opponent, a.from_day, a.module, w[1])
            for imp in impacts for hr in hours for w in worlds for s in seeds]
    print(f"{len(impacts)} impact caps x {len(hours)} start-hours x {len(worlds)} worlds "
          f"x {len(seeds)} seeds = {len(jobs)} seasons vs {a.opponent}, {a.workers} workers")
    print(f"impacts {impacts}   hours {hours}   worlds {labels}   seeds {seeds}")
    print(f"rows -> {a.out}\n", flush=True)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("impact,from_hour,world,seed,ours,theirs,win,units,revenue,turns,mean_lot,fired\n")
    fh.flush()

    cell = collections.defaultdict(lambda: [0, 0, 0.0, 0, 0.0, 0, 0.0, 0])
    label_of = {id(w[1]): w[0] for w in worlds}
    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for job, r in zip(jobs, pool.map(_play, jobs)):
            imp, hr, seed = job[0], job[1], job[2]
            world = label_of.get(id(job[6]), "as_drawn")
            ours, theirs, units, revenue, turns, mlot, fired = r
            win = 1 if ours > theirs else 0
            fh.write(f"{imp},{hr},{world},{seed},{ours:.0f},{theirs:.0f},{win},{units},"
                     f"{revenue:.0f},{turns},{mlot:.1f},{fired}\n")
            fh.flush()
            c = cell[(imp, hr, world)]
            c[0] += win
            c[1] += 1
            c[2] += ours
            c[3] += units
            c[4] += revenue
            c[5] += turns
            c[6] += mlot
            c[7] += fired
            print(f"  imp {imp:<6} h{hr:<3} {world:<12} seed {seed:<5} fired {fired:>4} "
                  f"bank {ours:>10,.0f} units {units:>5} $/u {revenue / max(1, units):>6.1f}",
                  flush=True)
    fh.close()

    for lab in labels:
        base = cell[(max(impacts), max(hours), lab)]
        b_bank = base[2] / base[1] if base[1] else 0.0
        b_units = base[3] / base[1] if base[1] else 0.0
        print(f"\n=== {lab} ===  control impact {max(impacts)} h{max(hours)}: "
              f"bank {b_bank:,.0f}, units {b_units:.0f}")
        print(f"{'impact':<8}{'h':<5}{'fired':>7}{'bank':>12}{'vs ctl':>10}{'units':>8}"
              f"{'vol %':>8}{'revenue':>12}{'$/unit':>9}{'turns':>7}{'lot~':>7}")
        for imp in impacts:
            for hr in hours:
                w, n, bank, units, rev, turns, mlot, fired = cell[(imp, hr, lab)]
                if not n:
                    continue
                print(f"{imp:<8}{hr:<5}{fired / n:>7.0f}{bank / n:>12,.0f}"
                      f"{bank / n - b_bank:>+10,.0f}{units / n:>8.0f}"
                      f"{100.0 * (units / n) / max(1.0, b_units):>7.0f}%"
                      f"{rev / n:>12,.0f}{rev / max(1, units):>9.1f}"
                      f"{turns / n:>7.0f}{mlot / n:>7.1f}")

    print("\n`vol %` is the guard: a row below ~95% is a volume cut, not a pricing result,")
    print("and its bank delta says nothing about whether reading the book helps.")
    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
