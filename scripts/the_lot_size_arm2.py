"""Small lots at FULL volume. The v1 arm found +8%/unit and threw away 30% of the volume to get it.

v1 capped each SELL at `lot` units and dropped the remainder. Revenue per unit rose from $116.7 to
$126.2 as the cap fell -- the price walk-down is real and smaller lots avoid it -- but units sold
fell 1,449 -> 1,007 and every row lost money. The gain was real; the harness spent it.

**Why the volume drained, which v1 did not diagnose.** `LATE_SELL_FROM_HOUR = 16`
(`schedule_agent:2490`) means the agent only sells in the last 8 hours of the day. Eight turns at a
cap of 8 units is 64 units a day, against the ~80 we produce. The gate and the cap fight each
other, and the cap loses stock it never gets a turn to sell.

**So this arm changes two things together, and says so.** That breaks the one-delta rule
deliberately, because the two are not independent -- a lot cap without more turns is a volume cut,
which is a different experiment and already known to lose $87k. `--from-hour 16` reproduces v1's
coupling for comparison, so the 2x2 is available rather than assumed.

- a BACKLOG per product, carried across turns AND across days. Whatever the agent wanted to sell
  and did not get to still wants selling tomorrow. This is what preserves volume.
- `--from-hour`, how early in the day the backlog may be worked off.

Revenue is measured with `record_fills`, per unit, at the price each unit actually fetched --
v1 divided the final bank by units, which folds in wages, land and animal purchases.

Control is `--lot 999 --from-hour 16`, which cannot bind and must reproduce the shipped agent.

    python -u scripts/the_lot_size_arm2.py --range 700 6 --lots 999,20,12,8 --hours 16,8,0
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
    lot, from_hour, seed, opponent, from_day, module_name, shops = job
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    active = not (lot >= 999 and from_hour >= 16)
    backlog = collections.Counter()
    fired = 0

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

            a0 = me(o0, env.configuration)
            market = a0["market"]

            if active and day >= from_day:
                # Whatever the agent asks for is its REMAINING intent -- it re-posts the unfilled
                # part every turn -- so the backlog is the high-water mark, never a sum.
                req = collections.Counter()
                for o in (a0["market"] or []):
                    if (isinstance(o, (list, tuple)) and len(o) > 2
                            and str(o[0]).upper() == "SELL"):
                        req[o[1]] += int(o[2])
                for p, n in req.items():
                    if n > backlog[p]:
                        backlog[p] = n

                new_sells = []
                if hour >= from_hour:
                    for p in SA.SELLABLE:
                        n = min(int(lot), backlog[p], shed.get(p, 0))
                        if n > 0:
                            new_sells.append(["SELL", p, n])

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
                # Retire from the backlog exactly what actually filled, never what was offered.
                after = {k: int(v or 0) for k, v in
                         ((env.state[0].observation.get("private") or {}).get("shed") or {}).items()}
                for p in list(backlog):
                    gone = shed.get(p, 0) - after.get(p, 0)
                    if gone > 0:
                        backlog[p] = max(0, backlog[p] - gone)
            if env.done:
                break

        farms = env.state[0].observation["farms"]
        units = revenue = 0
        lots_seen = collections.Counter()
        for d, h, op, item, price in fills.at_turn(0, op="SELL"):
            units += 1
            revenue += price
            lots_seen[(d, h)] += 1
        turns = len(lots_seen)
        mean_lot = (sum(lots_seen.values()) / turns) if turns else 0.0
        return (float(farms[0]["money"]), float(farms[1]["money"]),
                units, revenue, turns, mean_lot, fired)
    finally:
        cm.__exit__(None, None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--lots", default="999,20,12,8")
    ap.add_argument("--hours", default="16,8,0")
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--from-day", type=int, default=12)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--worlds", default="WOOL:8")
    ap.add_argument("--out", default="data/logs/lot_size2.csv")
    a = ap.parse_args()

    seeds = ([int(x) for x in a.seeds.split(",")] if a.seeds
             else list(range(a.range[0], a.range[0] + a.range[1])))
    lots = [int(x) for x in a.lots.split(",")]
    hours = [int(x) for x in a.hours.split(",")]

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

    jobs = [(lot, hr, s, a.opponent, a.from_day, a.module, w[1])
            for lot in lots for hr in hours for w in worlds for s in seeds]
    print(f"{len(lots)} lots x {len(hours)} start-hours x {len(worlds)} worlds x {len(seeds)} "
          f"seeds = {len(jobs)} seasons vs {a.opponent}, {a.workers} workers")
    print(f"lots {lots}   hours {hours}   worlds {labels}   seeds {seeds}")
    print(f"rows -> {a.out}\n", flush=True)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("lot,from_hour,world,seed,ours,theirs,win,units,revenue,turns,mean_lot,fired\n")
    fh.flush()

    cell = collections.defaultdict(lambda: [0, 0, 0.0, 0, 0.0, 0, 0.0, 0])
    label_of = {id(w[1]): w[0] for w in worlds}
    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for job, r in zip(jobs, pool.map(_play, jobs)):
            lot, hr, seed, world = job[0], job[1], job[2], label_of.get(id(job[6]), "as_drawn")
            ours, theirs, units, revenue, turns, mlot, fired = r
            win = 1 if ours > theirs else 0
            fh.write(f"{lot},{hr},{world},{seed},{ours:.0f},{theirs:.0f},{win},{units},"
                     f"{revenue:.0f},{turns},{mlot:.1f},{fired}\n")
            fh.flush()
            c = cell[(lot, hr, world)]
            c[0] += win
            c[1] += 1
            c[2] += ours
            c[3] += units
            c[4] += revenue
            c[5] += turns
            c[6] += mlot
            c[7] += fired
            print(f"  lot {lot:<5} h{hr:<3} {world:<12} seed {seed:<5} fired {fired:>4} "
                  f"bank {ours:>10,.0f}  units {units:>5}  $/u {revenue / max(1, units):>6.1f}",
                  flush=True)
    fh.close()

    for lab in labels:
        base = cell[(lots[0], max(hours), lab)]
        b_bank = base[2] / base[1] if base[1] else 0.0
        print(f"\n=== {lab} ===  control (lot {lots[0]}, h{max(hours)}) bank {b_bank:,.0f}")
        print(f"{'lot':<6}{'h':<5}{'fired':>7}{'bank':>12}{'vs ctl':>10}"
              f"{'units':>8}{'revenue':>12}{'$/unit':>9}{'turns':>7}{'lot~':>7}")
        for lot in lots:
            for hr in hours:
                w, n, bank, units, rev, turns, mlot, fired = cell[(lot, hr, lab)]
                if not n:
                    continue
                print(f"{lot:<6}{hr:<5}{fired / n:>7.0f}{bank / n:>12,.0f}"
                      f"{bank / n - b_bank:>+10,.0f}{units / n:>8.0f}{rev / n:>12,.0f}"
                      f"{rev / max(1, units):>9.1f}{turns / n:>7.0f}{mlot / n:>7.1f}")

    print("\n$/unit is exact `record_fills` revenue, not bank/units. Volume must hold near the")
    print("control's for a row to be a lot-size result rather than a volume cut.")
    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
