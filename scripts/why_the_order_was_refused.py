"""Hour by hour on one day: what we OFFERED, what FILLED, and the bank at that moment.

`breakdown.py` says `HIRE 9/11` and `BUY_SEED 1/5`. It cannot say whether the two missing hands were
never asked for or were asked for and refused, and those are opposite defects. `_do_hire` and
`_do_buy_land` fail SILENTLY on a thin bank (`reference/kaggriculture.py:691`), and a hire costs
`mult * fib(hires_today)` on a per-DAY counter, so the tenth hand of a day is not the price of the
first.

This prints, for each hour of a day and each side:

    offered   the market orders the policy emitted that turn
    filled    `_commit_unit` / `_do_hire` / `_do_buy_land` fills, from `kagg/analysis/fills.py`
    bank      `farms[seat]["money"]` at the START of the turn, before the market runs

An order that appears in `offered` and never in `filled` on a turn whose bank is below its price is
a refusal. One that never appears in `offered` at all is a planning miss.

    python -u scripts/why_the_order_was_refused.py --arm straw --day 7 --day 8
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
MELON_SEASON = "data/seed_scripts/kawashigi/92498144.json"
STRAWBERRY_SEASON = "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"
WATCH = ("HIRE", "BUY_SEED", "BUY_LAND", "BUY_ANIMAL", "SELL", "BUY_PRODUCT")


def trace(make0, opp, seed, weeds, economy, shops, days):
    """`{(day, hour): {"bank", "offered", "filled", "work"}}` for seat 0."""
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills
    env = make("kaggriculture", configuration=dict(economy or {}, seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    out = {}
    seen = 0
    last = 24 * (max(days) + 1)
    with record_fills(env) as fills:
        for t in range(last):
            o0, o1 = env.state[0].observation, env.state[1].observation
            if shops is not None:
                env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            a0, a1 = p0(o0, t), p1(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o1["farms"][1].get("hands") or []) if len(o1["farms"]) > 1 else 0
            d, h = divmod(t, TPD)
            row = None
            if d in days:
                offered = collections.Counter()
                for o in (a0["market"] or []):
                    if o and o[0] in WATCH:
                        offered[(o[0], o[1] if len(o) > 1 else None)] += (
                            int(o[2]) if len(o) > 2 else 1)
                work = collections.Counter()
                for a in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                    if a and a[0] not in ("PASS", "NORTH", "SOUTH", "EAST", "WEST"):
                        work[a[0]] += 1
                pv = (env.state[0].observation.get("private")
                      or o0.get("private") or {})
                shed = dict((pv.get("shed") or {}))
                carry = collections.Counter()
                for inv in (pv.get("inventories") or []):
                    carry.update(inv or {})
                row = {"bank": o0["farms"][0]["money"], "offered": offered, "work": work,
                       "hands": n0, "shed": shed, "carry": dict(carry)}
                out[(d, h)] = row
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if row is not None:
                got = collections.Counter()
                for e in fills.events[seen:]:
                    if e["seat"] == 0:
                        got[(e["op"], e.get("item"))] += 1
                row["filled"] = got
            seen = len(fills.events)
    return out


def show(name, tr, day):
    print(f"\n### {name}  d{day}")
    print(f"{'h':>3} {'bank':>8} {'hands':>5}  {'shed MILK/WHEAT/FERT':<22} {'carried':<22} "
          f"{'work':<30} {'OFFERED':<32} FILLED")
    for h in range(TPD):
        r = tr.get((day, h))
        if r is None:
            continue
        off = " ".join(f"{o}{'/' + str(i) if i else ''}x{n}" for (o, i), n in
                       sorted(r["offered"].items()))
        fil = " ".join(f"{o}{'/' + str(i) if i else ''}x{n}" for (o, i), n in
                       sorted(r["filled"].items()))
        wk = " ".join(f"{k}x{v}" for k, v in sorted(r["work"].items()))
        sh = r.get("shed") or {}
        st = f"{sh.get('MILK',0)}/{sh.get('WHEAT',0)}/{sh.get('FERTILIZER',0)}"
        cy = " ".join(f"{k}:{v}" for k, v in sorted((r.get("carry") or {}).items()) if v)
        print(f"{h:>3} {round(r['bank']):>8} {r['hands']:>5}  {st:<22} {cy:<22} "
              f"{wk:<30} {off:<32} {fil}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="straw")
    ap.add_argument("--day", type=int, action="append", default=None)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    a = ap.parse_args()
    days = set(a.day or [7, 8])

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if a.arm == "straw" else MELON_SEASON))
    economy, shops = B.env_config(replay), B.recorded_shops(replay)

    ours = trace(lambda: SA.make_agent(sched, 0), lambda: B.tape_policy(replay, TEAM, 1),
                 a.seed, a.weeds, economy, shops, days)
    tape = trace(lambda: B.tape_policy(replay, TEAM, 0), lambda: B.tape_policy(replay, TEAM, 1),
                 a.seed, a.weeds, economy, shops, days)
    print(f"seed {a.seed}, weeds {a.weeds}, arm {a.arm!r}")
    for d in sorted(days):
        show("OURS", ours, d)
        show("TAPE", tape, d)


if __name__ == "__main__":
    main()
