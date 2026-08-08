"""EXACT market fills, both sides, by patching the env's own `_commit_unit`.

`scripts/breakdown.py` reads sell/buy_product/buy_animal off the shed delta and can only do so on
turns clean of DROP/PICKUP/PLACE, so those rows are a disclosed LOWER BOUND (coverage ~25-70%).
That is fine for "did it land at all" and useless for "is the gap real", because our coverage and
the tape's differ -- a row can read -164 purely because we were dirtier.

This is the ground truth instead. `_commit_unit` in `reference/kaggriculture.py:626` is the single
place every SELL / BUY_PRODUCT / BUY_SEED / BUY_ANIMAL unit settles, it returns True exactly when
one unit changed hands, and it is a module-level function so it can be wrapped. Every call is
recorded with the seat, the day, the quoted price, whether it committed, and the money the buyer
held at the moment of refusal -- so a refusal is attributable to budget (money < price) or to an
empty shed, rather than guessed at.

    python -u scripts/probe_market_fills.py --op BUY_PRODUCT
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

REC = []
_SEAT = {}


def install():
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg
    if getattr(kg, "_probe_installed", False):
        return
    orig_pm, orig_cu = kg._process_market, kg._commit_unit

    def pm(state, env):
        _SEAT.clear()
        for i, f in enumerate(state[0].observation.farms):
            _SEAT[id(f)] = i
        return orig_pm(state, env)

    def cu(op, item, price, farm, private, market):
        money_before = int(farm["money"])
        shed_before = int((private.get("shed") or {}).get(item, 0) or 0)
        ok = orig_cu(op, item, price, farm, private, market)
        REC.append({"t": TURN[0], "seat": _SEAT.get(id(farm), -1), "op": op, "item": item,
                    "price": int(price), "ok": bool(ok), "money": money_before,
                    "shed": shed_before})
        return ok

    kg._process_market, kg._commit_unit, kg._probe_installed = pm, cu, True


TURN = [0]


def run(make0, opp, seed, weeds):
    from kaggle_environments import make
    install()
    REC.clear()
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    offers = collections.defaultdict(collections.Counter)  # day -> (op,item) -> units offered
    for t in range(719):
        TURN[0] = t
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for o in (a0["market"] or []):
            if o and len(o) > 2:
                offers[t // 24][(o[0], o[1])] += int(o[2])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    return list(REC), offers


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--op", default="BUY_PRODUCT")
    args = ap.parse_args()

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    his, his_off = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds)
    a = schedule_agent.make_agent(thin, 0, router=True)
    ours, our_off = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds)

    def fills(rec, seat):
        by_day = collections.defaultdict(collections.Counter)
        for r in rec:
            if r["seat"] != seat or r["op"] != args.op:
                continue
            by_day[r["t"] // 24][r["item"] if r["ok"] else "REFUSED:" + r["item"]] += 1
        return by_day

    of, hf = fills(ours, 0), fills(his, 0)
    items = sorted({k for d in list(of.values()) + list(hf.values()) for k in d
                    if not k.startswith("REFUSED")})

    print(f"{args.op}   tape {args.tape} seed {args.seed} weeds {args.weeds}   "
          f"seat 0 only.  EXACT fills from `_commit_unit`, not a shed-delta estimate.")
    hdr = "".join(f"{('ours ' + i[:5]):>13}{('tape ' + i[:5]):>13}" for i in items)
    print(f"{'day':>4}{hdr}{'ours off':>10}{'tape off':>10}{'ours ref':>10}{'tape ref':>10}")
    tot = collections.Counter()
    for d in range(args.days):
        cells = ""
        for i in items:
            cells += f"{of[d][i]:>13}{hf[d][i]:>13}"
            tot["o" + i] += of[d][i]
            tot["h" + i] += hf[d][i]
        oo = sum(v for (op, it), v in our_off[d].items() if op == args.op)
        ho = sum(v for (op, it), v in his_off[d].items() if op == args.op)
        orf = sum(v for k, v in of[d].items() if k.startswith("REFUSED"))
        hrf = sum(v for k, v in hf[d].items() if k.startswith("REFUSED"))
        tot["oo"] += oo
        tot["ho"] += ho
        tot["orf"] += orf
        tot["hrf"] += hrf
        print(f"{d:>4}{cells}{oo:>10}{ho:>10}{orf:>10}{hrf:>10}")
    cells = "".join(f"{tot['o' + i]:>13}{tot['h' + i]:>13}" for i in items)
    print(f"{'TOT':>4}{cells}{tot['oo']:>10}{tot['ho']:>10}{tot['orf']:>10}{tot['hrf']:>10}")

    for lab, rec in (("ours", ours), ("tape", his)):
        why = collections.Counter()
        for r in rec:
            if r["seat"] != 0 or r["op"] != args.op or r["ok"]:
                continue
            # `_commit_unit` has exactly two ways to return False: a SELL with an empty shed, and
            # a buy the farm cannot afford. Naming which one fired is the difference between
            # "we chose not to" and "the env said no".
            why["empty shed" if r["op"] == "SELL"
                else "no money" if r["money"] < r["price"]
                else "other"] += 1
        print(f"  {lab} refusals: {dict(why)}")


if __name__ == "__main__":
    main()
