"""Of the turns our hands stand still, how many had work the ROUTER itself would offer?

**This supersedes `scripts/what_the_idle_units_could_have_done.py`, which over-counted.** That script
called a tile an opportunity whenever `yield_units > 0`, and that is not what harvestable means. For
a ONE-SHOT crop `router.crop_ops` offers HARVEST only once the tile can no longer grow
(`kagg/search/router.py:759-760` via `_one_shot_is_finished`), because HARVEST sets a one-shot tile
to `None` (`reference/kaggriculture.py:409`) -- taking it early is a demolition that forfeits every
unit still owed to the tile. Seed 11 lost five tiles on day 3 to precisely that bug, which is why
the gate exists.

`data/logs/ripe_offered.log` measured the consequence: on d12-d23, 394 ripe tiles produce only 147
HARVEST offers, with 0 skipped for being pinned and 0 for a locked quadrant. So the earlier
"191 unit-turns beside unclaimed ripe crop" figure counts a large number of tiles the router is
correctly declining.

This asks the honest version of the question. At every turn, for every unit of ours emitting PASS:

    offered_harvest   a tile whose OWN `crop_ops` output contains HARVEST today -- the real
                      predicate, called on the live cell, not a re-implementation of it
    unclaimed         no other unit of ours harvests that tile later the same day
    reachable         `cheb(unit, tile) + dist_to_shed(tile) + 1 <= turns_left`, an upper bound for
                      one unit acting alone
    thirsty_offered   likewise for a tile whose `crop_ops` contains WATER

A PASS with none of those is a correct PASS.

Run inside the sim rather than off a replay, so `crop_ops` sees exactly the cell the agent saw, with
the same `have_fertilizer` and live prices.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]
TPD = 24


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def home(t):
    return min(cheb(t, s) for s in SHED)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    from kaggle_environments import make

    from kagg.search import router as RT
    import scripts.breakdown as B

    replay, schedule, team = B.TAPES[B.DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    from kagg.search import schedule_agent

    economy = B.env_config(replay)
    shops = B.recorded_shops(replay)
    env = make("kaggriculture",
               configuration=dict(economy, seed=args.seed, weedSpawnChance=args.weeds), debug=True)
    env.reset(2)
    ours = schedule_agent.make_agent(thin, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    # First pass over the season, recording actions AND the board, so "another unit takes it later
    # today" can be answered without guessing.
    turns = []
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        a0 = ours(o0)
        farm = o0["farms"][0]
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        turns.append(dict(
            t=t,
            tiles=[[dict(c) if isinstance(c, dict) else c for c in row] for row in farm["tiles"]],
            shed=dict(farm.get("shed") or {}),
            prices=dict((o0.get("market") or {}).get("prices") or {}),
            pos=pos,
            ops=[a0.get("farmer")] + list(a0.get("hands") or []),
        ))
        env.step([a0, opp(o1, t)])
    print(f"final bank ours ${env.state[0].observation['farms'][0]['money']:,.0f}")
    print()

    # Tiles OUR units work later the same day, in (x, y) to match `crop_ops`/`build_nodes`.
    #
    # **Both ops need this, not just HARVEST.** The first cut filtered only the harvest column and
    # left the water column unfiltered, which counts a tile another hand waters an hour later as
    # work going begging. That is the same over-count this whole script exists to correct, one
    # column across.
    taken = {"HARVEST": collections.defaultdict(set), "WATER": collections.defaultdict(set)}
    for r in turns:
        for i, op in enumerate(r["ops"]):
            if op and op[0] in taken and i < len(r["pos"]):
                y, x = r["pos"][i]
                taken[op[0]][r["t"] // TPD].add((x, y))

    per_day = collections.defaultdict(collections.Counter)
    for r in turns:
        day, hour = r["t"] // TPD, r["t"] % TPD
        if not any(op and op[0] == "PASS" for op in r["ops"]):
            continue
        shed = r["shed"]
        have_fert = shed.get("FERTILIZER", 0) > 0
        harvestable, waterable, brink = [], [], []
        for y, row in enumerate(r["tiles"]):
            for x, cell in enumerate(row):
                if not isinstance(cell, dict) or not cell.get("crop"):
                    continue
                ops = RT.crop_ops(cell, day, have_fert, tile=(x, y),
                                  product_price=r["prices"].get(cell["crop"]))
                names = {o[0] for o in ops}
                if "HARVEST" in names:
                    harvestable.append((x, y))
                if "WATER" in names:
                    # **A brink water and a parity water are not the same offer and must not share
                    # a column.** `crop_ops` prices a tile at `consecutive_unwatered >= 1` at
                    # `_crop_remaining` -- the whole tile, because two dry nights weed it
                    # (`reference/kaggriculture.py:771`) -- and prices a safe tile on its parity day
                    # at `_crop_remaining / TOP_UP_DISCOUNT`. Skipping the second one is what the
                    # alternation is FOR: the tile is offered again tomorrow. Counting them together
                    # would call a deliberate, free skip a missed opportunity.
                    waterable.append((x, y))
                    if int(cell.get("consecutive_unwatered", 0) or 0) >= 1:
                        brink.append((x, y))
        left = TPD - hour
        for i, op in enumerate(r["ops"]):
            if not (op and op[0] == "PASS") or i >= len(r["pos"]):
                continue
            y, x = r["pos"][i]
            u = (x, y)
            c = per_day[day]
            c["pass"] += 1
            hv = [tl for tl in harvestable
                  if cheb(u, tl) + home(tl) + 1 <= left and tl not in taken["HARVEST"][day]]
            wt = [tl for tl in waterable
                  if cheb(u, tl) + home(tl) + 1 <= left and tl not in taken["WATER"][day]]
            bk = [tl for tl in brink
                  if cheb(u, tl) + home(tl) + 1 <= left and tl not in taken["WATER"][day]]
            if hv:
                c["harvest_available"] += 1
            if wt:
                c["water_available"] += 1
            if bk:
                c["BRINK_available"] += 1
            if not hv and not wt:
                c["correct"] += 1

    print(f"{'day':>5}{'PASS':>8}{'HARVEST avail':>15}{'WATER avail':>13}"
          f"{'of which BRINK':>16}{'correct':>9}")
    for day in sorted(per_day):
        c = per_day[day]
        print(f"{day:>5}{c['pass']:>8}{c['harvest_available']:>15}"
              f"{c['water_available']:>13}{c['BRINK_available']:>16}{c['correct']:>9}")
    for lo, hi, label in ((12, 23, "d12-d23 (solver)"), (24, 29, "d24-d29 (planner)")):
        tot = collections.Counter()
        for d in range(lo, hi + 1):
            tot.update(per_day[d])
        print(f"\n{label}: PASS {tot['pass']}   harvest available {tot['harvest_available']}   "
              f"water available {tot['water_available']} "
              f"(BRINK {tot['BRINK_available']})   correct {tot['correct']}")


if __name__ == "__main__":
    main()
