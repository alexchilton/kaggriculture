"""Sell against the OPPONENT, not just against the book. And score it on WIN, not on our bank.

Every sell arm built on 2026-08-25 optimised our own money and was reported on our own money. On an
Elo ladder that is the wrong objective: `docs/` and `CLAUDE.md` both record that a $43k win and a
$4k win score identically. A move that costs us $5,000 and costs the opponent $15,000 is a WIN, and
not one of eight arms could express it.

**What is actually observable about him.** Measured, not assumed:

    obs["farms"][1]["tiles"]     VISIBLE -- every crop he has planted and its maturity
    obs["farms"][1]["money"]     VISIBLE
    obs["market"]["inventory"]   VISIBLE -- and it is the SHARED book, so his fills are exactly
                                 recoverable as  book(t+1) - book(t) - our_fills + our_buys + drain
    his shed / inventories       NOT visible (`private` is per-seat)

So we cannot see what he is holding, but we can see what he is GROWING and what he has SOLD. Both
are enough to know when a wave of supply is coming.

Three arms, all reported against `ours` on our bank, HIS bank, and win rate:

- `frontrun` -- when his visible tiles say a crop lands within `--lead` days, sell ours of that
                product NOW, ahead of him, while the book is still high.
- `wait`     -- the mirror: after his supply of a product lands in the book, hold ours until the
                town has drained it back, then sell.
- `spoil`    -- when he is heavier in a product than we are (his tile count vs our holding), dump
                ours into it deliberately. We lose money. He should lose more. Only rational
                because margin does not score.

**The tile encoding is not uniform.** A cell can be `None`, a dict, or a plain string -- a probe
crashed on `'str' object has no attribute 'get'`. Anything that is not a dict is skipped rather
than guessed at.

    python -u scripts/play_the_opponent.py --range 700 6 --opponent contrarian
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
ARMS = ("ours", "frontrun", "wait", "spoil")


def _his_crops(farm, KG, day):
    """(product -> tiles ready within `lead` days) from his VISIBLE tiles, plus his total."""
    soon = collections.Counter()
    total = collections.Counter()
    for row in (farm.get("tiles") or []):
        for cell in row:
            if not isinstance(cell, dict):        # may be None or a bare string
                continue
            if cell.get("kind") != "PLANT":
                continue
            crop = cell.get("crop")
            spec = KG.CROPS.get(crop)
            if not spec:
                continue
            total[crop] += 1
            planted = int(cell.get("planted_day", day) or 0)
            first = planted + int(spec.get("first_yield_day", 99))
            soon[(crop, first)] += 1
    return soon, total


def _play(job):
    arm, seed, opponent, from_day, module_name, lead = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    # **The opponent has to be worth spoiling.** Against `contrarian`, which banks $15,869 to our
    # $169,056, there is nothing to take away: the first run of these arms cost us $4,484-$8,938
    # and cost him $66-$90. A tape opponent banks $93,963 and competes for the same book.
    steps = him = them = None
    cfg = {}
    if opponent.startswith("tape:"):
        rec = json.loads((REPO / "data/seed_scripts/kawa_2026-08-24/97466318.json").read_text())
        steps = rec["steps"]
        names = (rec.get("info") or {}).get("TeamNames") or []
        him = names.index("カワシギ") if "カワシギ" in names else 0
        cfg = dict(rec.get("configuration") or {})
        cfg.pop("seed", None)

    fired = 0
    prev_book = None
    his_flow = collections.Counter()          # product -> units he has put into the book lately
    cm = record_fills()
    fills = cm.__enter__()
    try:
        env = make("kaggriculture", configuration=dict(cfg, seed=int(seed)), debug=False)
        env.reset(2)
        me = SA.make_agent(sched, 0, router=True)
        if steps is None:
            them = _build(OPPONENTS[opponent], None)

        for t in range(30 * TPD):
            o0 = env.state[0].observation
            day = t // TPD
            priv = o0.get("private") or {}
            shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}
            book = {k: int(v or 0) for k, v in
                    (((o0.get("market") or {}).get("inventory")) or {}).items()}

            # His net flow into the book since last turn. The book is shared and public, so this
            # needs no inference about his private state -- only our own fills subtracted out.
            if prev_book is not None:
                ours_last = collections.Counter()
                for d, h, op, item, price in fills.at_turn(0, op="SELL"):
                    if d * TPD + h == t - 1:
                        ours_last[item] += 1
                for p in book:
                    delta = book[p] - prev_book.get(p, 0) - ours_last[p]
                    if delta > 0:
                        his_flow[p] += delta
                    else:
                        his_flow[p] = max(0, his_flow[p] + delta)   # town drain decays it
            prev_book = dict(book)

            a0 = me(o0, env.configuration)
            market = a0["market"]

            if arm != "ours" and day >= from_day:
                soon, total = _his_crops(o0["farms"][1], KG, day)
                incoming = collections.Counter()
                for (crop, first), n in soon.items():
                    if day <= first <= day + lead:
                        incoming[crop] += n

                new_sells = []
                for o in (a0["market"] or []):
                    if not (isinstance(o, (list, tuple)) and len(o) > 2
                            and str(o[0]).upper() == "SELL"):
                        continue
                    p, n = o[1], int(o[2])
                    have = shed.get(p, 0)
                    if arm == "frontrun" and incoming.get(p, 0) >= 4:
                        # His wave lands within `lead` days: take the good price first.
                        n = have
                    elif arm == "wait" and his_flow.get(p, 0) >= 10:
                        # He has just flooded it. Let the town drain before we add to it.
                        n = 0
                    elif arm == "spoil" and total.get(p, 0) >= 8 and have > 0:
                        # He is heavier in this product than we are: dump into it. We lose money;
                        # he should lose more. Only sane because the ladder scores wins.
                        n = have
                    if n > 0:
                        new_sells.append(["SELL", p, int(min(n, have))])

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
            if steps is not None:
                at = steps[t + 1][him].get("action") if t + 1 < len(steps) else None
                at = at if isinstance(at, dict) else {}
                n1 = len(o0["farms"][1].get("hands") or [])
                yours = {"farmer": at.get("farmer") or ["PASS"],
                         "hands": list(at.get("hands") or [])[:n1],
                         "market": at.get("market") or []}
            else:
                yours = them(env.state[1].observation, env.configuration)
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                       "market": market}, yours])
            if env.done:
                break

        farms = env.state[0].observation["farms"]
        units = revenue = 0
        for d, h, op, item, price in fills.at_turn(0, op="SELL"):
            units += 1
            revenue += price
        return (float(farms[0]["money"]), float(farms[1]["money"]), units, revenue, fired)
    finally:
        cm.__exit__(None, None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default=None)
    ap.add_argument("--range", nargs=2, type=int, default=[700, 6], metavar=("FIRST", "COUNT"))
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--from-day", type=int, default=12)
    ap.add_argument("--lead", type=int, default=2)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", default="data/logs/play_the_opponent.csv")
    a = ap.parse_args()

    seeds = ([int(x) for x in a.seeds.split(",")] if a.seeds
             else list(range(a.range[0], a.range[0] + a.range[1])))
    jobs = [(arm, s, a.opponent, a.from_day, a.module, a.lead) for arm in ARMS for s in seeds]
    print(f"{len(ARMS)} arms x {len(seeds)} seeds vs {a.opponent} = {len(jobs)} seasons")
    print(f"seeds {seeds}   lead {a.lead} days\nrows -> {a.out}\n", flush=True)

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("arm,seed,ours,theirs,margin,win,units,revenue,fired\n")
    fh.flush()

    cell = collections.defaultdict(lambda: [0, 0, 0.0, 0.0, 0, 0.0, 0])
    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        for job, r in zip(jobs, pool.map(_play, jobs)):
            arm, seed = job[0], job[1]
            ours, theirs, units, revenue, fired = r
            win = 1 if ours > theirs else 0
            fh.write(f"{arm},{seed},{ours:.0f},{theirs:.0f},{ours - theirs:.0f},{win},"
                     f"{units},{revenue:.0f},{fired}\n")
            fh.flush()
            c = cell[arm]
            c[0] += win
            c[1] += 1
            c[2] += ours
            c[3] += theirs
            c[4] += units
            c[5] += revenue
            c[6] += fired
            print(f"  {arm:<9} seed {seed:<5} fired {fired:>4}  ours {ours:>10,.0f}  "
                  f"theirs {theirs:>10,.0f}  margin {ours - theirs:>+11,.0f}  "
                  f"{'WIN' if win else 'loss'}", flush=True)
    fh.close()

    print(f"\n**Win rate is the criterion. Our bank is context.**\n")
    print(f"{'arm':<10}{'fired':>7}{'WIN':>7}{'ours':>12}{'theirs':>12}{'margin':>12}"
          f"{'units':>8}{'revenue':>12}")
    b = cell["ours"]
    for arm in ARMS:
        w, n, ours, theirs, units, rev, fired = cell[arm]
        if not n:
            continue
        print(f"{arm:<10}{fired / n:>7.0f}{w / n:>6.0%}{ours / n:>12,.0f}{theirs / n:>12,.0f}"
              f"{(ours - theirs) / n:>+12,.0f}{units / n:>8.0f}{rev / n:>12,.0f}")
    print(f"\n{'arm':<10}{'vs ours: our bank':>20}{'their bank':>14}{'margin':>12}")
    for arm in ARMS[1:]:
        w, n, ours, theirs, units, rev, fired = cell[arm]
        if not n or not b[1]:
            continue
        print(f"{arm:<10}{ours / n - b[2] / b[1]:>+20,.0f}"
              f"{theirs / n - b[3] / b[1]:>+14,.0f}"
              f"{(ours - theirs) / n - (b[2] - b[3]) / b[1]:>+12,.0f}")
    print("\nAn arm that costs us money and costs him MORE is a win on this ladder.")
    print("Read the `their bank` column before the `our bank` one.")
    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
