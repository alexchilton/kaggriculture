"""Every unit of wheat, day by day, ours beside the tape's -- because a fix is a claim until it is a number.

The one-shot harvest fix was justified with a unit test on one tile and a two-point ladder move. Neither
says the wheat now BEHAVES like the tape's. Wheat is the only commodity in the game with four separate
lives -- a seed, a crop, a traded product and the animals' feed -- so it is also the only one where a
single ledger can catch a routing bug, a market bug and a herd bug at once.

Every column is measured off the board rather than off the order list, because an order is a request:
a SELL walks the shed one unit at a time and stops when it runs out, and a BUY stops when the money
does. `ordered` and `realised` are printed side by side for exactly that reason.

    tiles       wheat plants standing at dawn
    planted     PLANT/WHEAT ops that turned a seed into a tile
    harvest     units banked, read from `yield_units` of the tile under each HARVEST at the instant
                it is emitted -- this is the number the fix was supposed to move
    fed         FEED ops that will actually consume a wheat (animal present, not yet fed, unit holding
                one), replicating `_inv_take` rather than trusting the op count
    bought/sold ordered against realised
    holdings    shed + every unit's inventory at dawn; seeds are a separate pool and counted apart
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import router as RT
from kagg.search import schedule_agent
import agent_ladder as L


def _holdings(obs):
    priv = obs["private"]
    n = int((priv.get("shed") or {}).get("WHEAT", 0))
    for iv in priv.get("inventories") or []:
        n += int(iv.get("WHEAT", 0))
    return n


def run(seed, make_us=None, tape=None, theirs=None):
    env = L._env(seed, 0.0)
    us = make_us() if make_us else None
    rows = collections.defaultdict(collections.Counter)
    for t in range(719):
        obs = env.state[0].observation
        day, hour = int(obs.get("day", 0)), int(obs.get("hour", 0))
        farm, priv = obs["farms"][0], obs["private"]
        tiles = farm["tiles"]
        r = rows[day]
        if hour == 0:
            r["tiles"] = sum(1 for row in tiles for c in row
                             if isinstance(c, dict) and c.get("crop") == "WHEAT")
            r["hold"] = _holdings(obs)
            r["shed"] = int((priv.get("shed") or {}).get("WHEAT", 0))
            r["seeds"] = int((priv.get("seeds") or {}).get("WHEAT", 0))
        if us is not None:
            a = us(obs)
            f0, h0, m0 = a["farmer"], a["hands"], a["market"]
        else:
            f0, h0, m0 = tape[t] if t < len(tape) else (["PASS"], [], [])
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        invs = priv.get("inventories") or []
        acts = [f0, *list(h0)][:len(pos)]
        for i, (cell, act) in enumerate(zip(pos, acts)):
            if not (isinstance(act, list) and act):
                continue
            x, y = cell
            tile = tiles[y][x] if 0 <= y < len(tiles) and 0 <= x < len(tiles) else None
            if act[0] == "PLANT" and len(act) > 1 and act[1] == "WHEAT":
                r["planted"] += 1
            elif act[0] == "HARVEST" and isinstance(tile, dict) and tile.get("crop") == "WHEAT":
                r["harvest"] += int(tile.get("yield_units", 0))
                r["hv_n"] += 1
                # A wheat is created holding 1 and the window (ages 2-4) offers three more waters, so
                # 4 is the plain ceiling and 6 the fertilized one. The shape of this histogram says
                # whether a tile was harvested early or simply never watered enough.
                r["hv@%d" % min(6, int(tile.get("yield_units", 0)))] += 1
            elif act[0] == "FEED" and isinstance(tile, dict) and "animal" in tile:
                # Replicates the env's own three guards, so this is realised feeding, not intent.
                if not tile.get("fed_today") and int((invs[i] if i < len(invs) else {}).get("WHEAT", 0)):
                    r["fed"] += 1
        for o in m0:
            if len(o) > 2 and o[1] == "WHEAT":
                if o[0] == "BUY_PRODUCT":
                    r["buy_ord"] += int(o[2])
                elif o[0] == "SELL":
                    r["sell_ord"] += int(o[2])
                elif o[0] == "BUY_SEED":
                    r["seed_ord"] += int(o[2])
        n1 = len(obs["farms"][1].get("hands") or [])
        f1, h1, m1 = theirs[t] if t < len(theirs) else (["PASS"], [], [])
        env.step([{"farmer": f0, "hands": list(h0)[:len(pos) - 1], "market": m0},
                  {"farmer": f1, "hands": list(h1)[:n1], "market": m1}])
        if env.state[0].status == "DONE":
            break
    # Realised market flow is whatever the day's holdings did that the board cannot account for.
    for d in sorted(rows):
        nxt = rows.get(d + 1)
        end = nxt["hold"] if nxt else _holdings(env.state[0].observation)
        rows[d]["net_mkt"] = end - rows[d]["hold"] - rows[d]["harvest"] + rows[d]["fed"]
    return rows, float(env.state[0].observation["farms"][0]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", nargs="?", type=int, default=11)
    args = ap.parse_args()
    mine, theirs = L.tape_plans()
    sched = {int(k): v for k, v in json.loads(pathlib.Path(L.SCHEDULE).read_text()).items()}
    for r in sched.values():
        for k in L.TAPE_ONLY:
            r[k] = []

    tape_rows, tape_money = run(args.seed, tape=mine, theirs=theirs)
    our_rows, our_money = run(args.seed,
                              make_us=lambda: schedule_agent.make_agent(sched, 0, router=True),
                              theirs=theirs)

    print(f"seed {args.seed}   tape ${tape_money:,.0f}   ours ${our_money:,.0f} "
          f"({100 * our_money / tape_money:.0f}%)\n")
    cols = [("tiles", "TILES"), ("planted", "PLANTED"), ("harvest", "HARVEST"), ("fed", "FED"),
            ("buy_ord", "BUY ord"), ("sell_ord", "SELL ord"), ("net_mkt", "NET MKT"),
            ("shed", "SHED"), ("hold", "HELD"), ("seeds", "SEEDS")]
    print("     " + " ".join(f"{lab:>13}" for _k, lab in cols))
    print(f"{'day':>4} " + " ".join(f"{'ours':>6}{'tape':>7}" for _k, _l in cols))
    tot = collections.Counter()
    match = collections.Counter()
    for d in sorted(set(our_rows) | set(tape_rows)):
        o, t = our_rows.get(d, {}), tape_rows.get(d, {})
        line = []
        for k, _lab in cols:
            a, b = int(o.get(k, 0)), int(t.get(k, 0))
            tot["o_" + k] += a
            tot["t_" + k] += b
            if k not in ("shed", "hold", "seeds", "tiles"):
                match[k] += (a == b)
            line.append(f"{a:>6}{b:>7}")
        print(f"{d:>4} " + " ".join(line))
    print()
    n = len(set(our_rows) | set(tape_rows))
    for k, lab in cols:
        a, b = tot["o_" + k], tot["t_" + k]
        extra = f"   days equal {match[k]}/{n}" if k in match else ""
        print(f"  {lab:<10} season   ours {a:>7}   tape {b:>7}   "
              f"{100 * a / max(1, b):>5.0f}%{extra}")


if __name__ == "__main__":
    main()
