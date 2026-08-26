"""Before the sweep: prove the arm CHANGES something, and that the harness plays a real season.

The rule in `~/.claude/CLAUDE.md`: *"Before any sweep, state in one sentence what the arm changes
and what would have to be true for it to win."* For this arm the sentence is

    `_sow_carrot_instead` rewrites this turn's `PLANT WHEAT` to `PLANT CARROT`, and the matching
    `BUY_SEED WHEAT` to `BUY_SEED CARROT`, on days in `CARROT_SWAP_DAYS`, up to `budget` tiles,
    where `budget` is what `corner_the_book.plan` sizes off the town's carrot deficit.

So it can only win if the day it fires on actually contains `PLANT WHEAT`. If the planner plants no
wheat on d21-d27, EVERY arm is byte-identical to the control and the sweep measures nothing -- which
is exactly the 6,048-season `add_land` mistake, where the arm inserted one order and no unit could
ever reach the new ground.

This runs a handful of the recorded losses under the control and under one live arm, and prints,
per day, the ops that the rewrite touches. It is a wiring check, not a result:

    plants   what went in the ground, by crop
    seeds    what was bought, by crop
    sold     CARROT units FILLED (shed/money deltas, never the offer stream)
    plan()   what `corner_the_book.plan` returned on the first turn of the window, and why

Read the two columns side by side. If they are identical, stop -- the sweep cannot answer anything.
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24


def trace(rec, seat, seed, tiles, start):
    """Play one recorded game with one arm installed. Returns (ours, theirs, per-day trace)."""
    import us_in_his_seat as U
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    CORNER = importlib.import_module("kagg.search.corner_the_book")
    import breakdown as B
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    live_days, live_plan = SA.CARROT_SWAP_DAYS, CORNER.plan
    said = []

    def spy(*ar, **kw):
        out = live_plan(*ar, **{**kw, "max_tiles": tiles})
        said.append(out)
        return out

    SA.CARROT_SWAP_DAYS = tuple(range(start, 28))
    CORNER.plan = (lambda *ar, **kw: (0, "control")) if tiles == 0 else spy
    try:
        steps = rec["steps"]
        them = 1 - seat
        cfg = dict(rec.get("configuration") or {})
        cfg.pop("seed", None)
        env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
        env.reset(2)
        agent = SA.make_agent(sched, seat)

        # `plants` and `seeds` count what we SUBMIT; `sold` is read off the shed, because the agent
        # re-posts the same SELL every turn and summing offers over-counts by ~24x
        # (`feedback_offers_are_not_fills`).
        per_day = collections.defaultdict(lambda: collections.Counter())
        prev_shed, prev_money = {}, None
        for t in range(30 * TPD):
            o = env.state[seat].observation
            day = int(o.get("day", 0) or 0)
            shed = dict((o.get("private") or {}).get("shed") or {})
            money = float(o["farms"][seat]["money"])
            if prev_money is not None:
                drop = int(prev_shed.get("CARROT", 0) or 0) - int(shed.get("CARROT", 0) or 0)
                if drop > 0 and money > prev_money:
                    per_day[day]["sold_CARROT"] += drop
            prev_shed, prev_money = shed, money

            n_us = len(o["farms"][seat].get("hands") or [])
            n_them = len(o["farms"][them].get("hands") or [])
            a = agent(o)
            acts = [a["farmer"]] + list(a["hands"] or [])[:n_us]
            for act in acts:
                if act and len(act) >= 2 and act[0] == "PLANT":
                    per_day[day][f"plant_{act[1]}"] += 1
            for od in (a["market"] or []):
                if od and len(od) >= 3 and od[0] == "BUY_SEED":
                    per_day[day][f"seed_{od[1]}"] += int(od[2])

            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
            at = U._recorded(steps, t, them)
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n_them],
                     "market": at.get("market") or []}
            env.step([mine, yours] if seat == 0 else [yours, mine])
            if env.done:
                break
        f = env.state[seat].observation["farms"]
        return float(f[seat]["money"]), float(f[them]["money"]), per_day, said
    finally:
        SA.CARROT_SWAP_DAYS, CORNER.plan = live_days, live_plan


def main():
    from does_the_carrot_flip_a_loss import our_losses

    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3, help="how many recorded losses to trace")
    ap.add_argument("--tiles", type=int, default=40)
    ap.add_argument("--start", type=int, default=21)
    ap.add_argument("--episodes", default="", help="comma-separated episode ids instead of --n")
    a = ap.parse_args()

    losses = our_losses()
    if a.episodes:
        want = set(a.episodes.split(","))
        losses = [L for L in losses if L[0] in want]
    else:
        losses = losses[:a.n]
    print(f"tracing {len(losses)} recorded losses\n", flush=True)

    for ep, f, seat, seed, margin, opp in losses:
        rec = json.loads(pathlib.Path(f).read_text())
        print(f"=== {ep}  seat {seat}  seed {seed}  recorded margin ${margin:,.0f}  vs {opp}",
              flush=True)
        rows = {}
        for label, tiles in (("control", 0), (f"tiles={a.tiles}", a.tiles)):
            ours, theirs, per_day, said = trace(rec, seat, seed, tiles, a.start)
            rows[label] = (ours, theirs, per_day)
            for got in said[:1]:
                print(f"    plan() -> {got[0]} tiles :: {got[1]}", flush=True)
            print(f"    {label:>10}: ours ${ours:,.0f}  theirs ${theirs:,.0f}  "
                  f"margin ${ours - theirs:,.0f}", flush=True)

        keys = ["plant_WHEAT", "plant_CARROT", "seed_WHEAT", "seed_CARROT", "sold_CARROT"]
        print(f"    {'day':>4} | " + " | ".join(f"{k.replace('_', ' '):>14}" for k in keys),
              flush=True)
        for day in range(18, 30):
            cells = []
            for k in keys:
                c = int(rows["control"][2][day][k])
                v = int(rows[f"tiles={a.tiles}"][2][day][k])
                cells.append(f"{c:>6}/{v:<7}")
            if any(int(rows[lbl][2][day][k]) for lbl in rows for k in keys):
                print(f"    {day:>4} | " + " | ".join(cells), flush=True)
        print("    (cells are control/arm)\n", flush=True)


if __name__ == "__main__":
    main()
