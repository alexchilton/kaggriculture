"""At dawn on each day: how many ripe tiles exist, and how many become HARVEST jobs?

`data/logs/solver_drops.log` closed the first question. On d12-d23 the solver seats 739 of 748 jobs
and drops 9 -- so the 191 idle unit-turns beside unclaimed ripe crop are NOT jobs the router refused
to route. The day's job LIST is simply smaller than the crew's capacity.

That moves the question upstream to `build_nodes` (`kagg/search/router.py:1448`), which walks every
tile and can skip one before `crop_ops` is ever consulted:

    router.py:1467   `if tile in pinned or not isinstance(cell, dict): continue`
    router.py:1469   `if R.quadrant_of(x, y) not in unlocked: continue`

and then `crop_ops` itself may return no HARVEST for a ripe tile.

So this counts, at hour 0 of each day, over OUR farm:

    ripe            tiles with a crop and `yield_units > 0`
    pinned_out      ripe tiles skipped because the tile was pinned
    locked_out      ripe tiles skipped because their quadrant is not unlocked
    no_harvest_op   ripe tiles that reached `crop_ops` and got no HARVEST op back
    offered         ripe tiles that did become a HARVEST job

**Tile order matters here and is easy to get backwards.** `build_nodes` stores `tile = (x, y)`
(router.py:1466) while it iterates `tiles[y][x]`. The replay analysis scripts in this repo use
`(y, x)`. Everything below is kept in `(x, y)` to match the router, and the ripe scan converts.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

ROWS = []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    from kaggle_environments import make

    from kagg.search import router as RT
    # `router.py:65` does `from . import routines as R` -- the same module the skip test uses.
    from kagg.search import routines as R
    import scripts.breakdown as B

    replay, schedule, team = B.TAPES[B.DEFAULT_TAPE]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    real = RT.build_nodes

    def wrapped(tiles, day, shed, carried, unlocked, pinned, hour=0, **kw):
        nodes = real(tiles, day, shed, carried, unlocked, pinned, hour=hour, **kw)
        if hour != 0:
            return nodes
        have_fert = shed.get("FERTILIZER", 0) > 0 or carried.get("FERTILIZER", 0) > 0
        prices = kw.get("prices") or {}
        c = collections.Counter()
        offered = set()
        for n in nodes:
            if any(o[0] == "HARVEST" for o in n.ops):
                offered.add(tuple(n.tile))
        for y, row in enumerate(tiles):
            for x, cell in enumerate(row):
                if not isinstance(cell, dict) or not cell.get("crop"):
                    continue
                if int(cell.get("yield_units", 0) or 0) <= 0:
                    continue
                tile = (x, y)
                c["ripe"] += 1
                if tile in pinned:
                    c["pinned_out"] += 1
                elif R.quadrant_of(x, y) not in unlocked:
                    c["locked_out"] += 1
                elif tile in offered:
                    c["offered"] += 1
                else:
                    ops = RT.crop_ops(cell, day, have_fert, kw.get("fertilizer_price"), tile=tile,
                                      product_price=prices.get(cell["crop"]))
                    if any(o[0] == "HARVEST" for o in ops):
                        c["offered_elsewhere"] += 1
                    else:
                        c["no_harvest_op"] += 1
                        c["units_no_harvest_op"] += int(cell.get("yield_units", 0) or 0)
        c["nodes"] = len(nodes)
        ROWS.append((day, c))
        return nodes

    RT.build_nodes = wrapped
    # schedule_agent imports the module, not the symbol -- checked: it calls RT.build_nodes.
    from kagg.search import schedule_agent
    assert schedule_agent.RT.build_nodes is wrapped, "wrap did not take"

    economy = B.env_config(replay)
    shops = B.recorded_shops(replay)
    env = make("kaggriculture",
               configuration=dict(economy, seed=args.seed, weedSpawnChance=args.weeds), debug=True)
    env.reset(2)
    ours = schedule_agent.make_agent(thin, 0, router=True)
    opp = B.tape_policy(replay, team, 1)
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        env.step([ours(o0), opp(o1, t)])

    print(f"final bank ours ${env.state[0].observation['farms'][0]['money']:,.0f}")
    print()
    print(f"{'day':>5}{'nodes':>8}{'ripe':>7}{'offered':>9}{'pinned':>8}{'locked':>8}"
          f"{'NO_HARV_OP':>12}{'units':>8}")
    by = collections.defaultdict(collections.Counter)
    for day, c in ROWS:
        by[day].update(c)
    for day in sorted(by):
        c = by[day]
        print(f"{day:>5}{c['nodes']:>8}{c['ripe']:>7}"
              f"{c['offered'] + c['offered_elsewhere']:>9}{c['pinned_out']:>8}"
              f"{c['locked_out']:>8}{c['no_harvest_op']:>12}{c['units_no_harvest_op']:>8}")
    sel = [d for d in sorted(by) if 12 <= d <= 23]
    tot = collections.Counter()
    for d in sel:
        tot.update(by[d])
    print()
    print(f"d12-d23  ripe {tot['ripe']}   offered {tot['offered']+tot['offered_elsewhere']}   "
          f"pinned {tot['pinned_out']}   locked {tot['locked_out']}   "
          f"NO HARVEST OP {tot['no_harvest_op']} ({tot['units_no_harvest_op']} units)")


if __name__ == "__main__":
    main()
