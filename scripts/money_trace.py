"""Dawn money, dusk money, and what moved in between -- ours beside his, day by day.

The hires are ISSUED exactly as the row asks and then fail on the bank: the ladder for 7 hires is
$33 and d7 opens on $12. So the question is not "does the planner do what it is told" -- it does --
but where the money that should have been there went. Alex: "it will be the buying and selling --
due to not bringing in a harvest or fertilizer to sell fast enough".

So this prints, per day and for both sides: money at dawn, money at dusk, units SOLD and what they
raised, units BOUGHT and what they cost, and the harvest and fertilizer collected that day. The
board is the tape's own world (the recorded shop draw), and days 0-6 are the tape's, so every row
from d7 is the planner on his board.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
TPD = 24


def day_flows(steps, seat, day, price_of):
    """(sold units, sale value, bought units, buy cost, harvests, fert collected) for one day."""
    sold = bought = 0
    sale = cost = 0.0
    harvest = fert = 0
    for hour in range(TPD):
        i = day * TPD + hour + 1
        if i >= len(steps):
            break
        a = (steps[i][seat] or {}).get("action") or {}
        for c in [a.get("farmer") or []] + list(a.get("hands") or []):
            if not c:
                continue
            if c[0] == "HARVEST":
                harvest += 1
            elif c[0] == "COLLECT_FERTILIZER":
                fert += 1
        # Money moved is read from the FARM, not from the orders: an order is a request and the
        # engine fills what it can. The per-turn delta is the only honest measure of a fill.
        for o in (a.get("market") or []):
            if not o:
                continue
            q = o[2] if len(o) > 2 and isinstance(o[2], int) else 1
            if o[0] == "SELL":
                sold += q
                sale += q * price_of(o[1])
            elif o[0] in ("BUY_PRODUCT", "BUY_SEED"):
                bought += q
                cost += q * price_of(o[1])
    return sold, sale, bought, cost, harvest, fert


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", type=int, default=107068412)
    ap.add_argument("--handover", type=int, default=7)
    ap.add_argument("--days", type=int, default=13)
    ap.add_argument("--schedule", default="data/seed_scripts/spataro/schedule.json")
    args = ap.parse_args()

    import kagg.plan as P
    from kagg.search import routines as R
    from kagg.search import schedule_agent as SA
    from kaggle_environments import make

    r = json.loads((ROOT / f"data/replays_spa_sub/{args.episode}.json").read_text())
    seat = r["info"]["TeamNames"].index("SpaTaro")
    seed = r["info"]["seed"]

    def price_of(p):
        return float(getattr(R, "BASE_PRICE", {}).get(p, 0) or 0)

    sched = {int(k): {kk: vv for kk, vv in row.items() if kk not in P.TAPE_ONLY}
             for k, row in json.loads((ROOT / args.schedule).read_text()).items()}
    agent = SA.make_agent(dict(sched), 0, router=True)
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": 0.0}, debug=False)
    env.run([agent, str(ROOT / "submission/shop0909/main.py")])

    def money(steps, st, day, hour):
        i = day * TPD + hour
        if i >= len(steps):
            return None
        farms = ((steps[i][st] or {}).get("observation") or {}).get("farms") or []
        return round(float(farms[st]["money"])) if len(farms) > st else None

    print(f"ep {args.episode}  seed {seed}  tape drives d0-d{args.handover-1}\n")
    print(f"{'':4} {'OURS: dawn':>11} {'dusk':>8} {'sold':>6} {'bought':>7} {'harv':>5} {'fert':>5}"
          f"   {'HIS: dawn':>10} {'dusk':>8} {'sold':>6} {'bought':>7} {'harv':>5} {'fert':>5}")
    for day in range(args.days):
        o_dawn, o_dusk = money(env.steps, 0, day, 0), money(env.steps, 0, day, TPD - 1)
        h_dawn, h_dusk = money(r["steps"], seat, day, 0), money(r["steps"], seat, day, TPD - 1)
        os_, osv, ob, obc, oh, of = day_flows(env.steps, 0, day, price_of)
        hs, hsv, hb, hbc, hh, hf = day_flows(r["steps"], seat, day, price_of)
        mark = "   " if day < args.handover else ">> "
        print(f"{mark}{day:<1} {o_dawn if o_dawn is not None else 0:>11,} {o_dusk or 0:>8,} "
              f"{os_:>6} {ob:>7} {oh:>5} {of:>5}   "
              f"{h_dawn or 0:>10,} {h_dusk or 0:>8,} {hs:>6} {hb:>7} {hh:>5} {hf:>5}")


if __name__ == "__main__":
    main()
