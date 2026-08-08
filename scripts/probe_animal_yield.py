"""Where an animal product is actually MADE, per day, both sides.

`sh:milk` is a state row, so it is exact -- but a shed level is a stock, and a stock differs because
of production, harvesting or selling, which a stock cannot tell apart. This wraps
`_daily_refresh_animals` (`reference/kaggriculture.py:773`, the ONLY place `yield_units` grows for an
animal) and records, per dusk and per species:

    made        units added to `yield_units` this dusk (base 1 on a production day, plus any
                pending CARE bonus that a FEED that day unlocked)
    lost        units the `max_held` clamp threw away -- production that happened and was
                discarded because nobody harvested the tile
    bonus       units of `made` that came from the CARE bonus rather than the base rate
    fed/cared   tiles that were fed / cared today, at the moment of the dusk refresh
    escaped     animals removed for two consecutive unfed days

plus, from outside the patch, the herd standing in pens per species and the units of that product
held across shed and unit inventories.

    python -u scripts/probe_animal_yield.py --species COW
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent
from scripts.breakdown import TAPES, TAPE_ONLY, tape_policy

REC = collections.defaultdict(collections.Counter)
DAY = [0]
CALLS = [0]


def install():
    from kaggle_environments.envs.kaggriculture import kaggriculture as kg
    if getattr(kg, "_yield_probe", False):
        return
    orig = kg._daily_refresh_animals
    ANIMALS = kg.ANIMALS

    def wrapped(farm, day):
        # `_end_of_day` calls this once per farm, in `enumerate(obs0.farms)` order
        # (`reference/kaggriculture.py:842`), so the call parity IS the seat. Identity of the farm
        # dict is not usable: the framework hands out a fresh observation each step.
        seat = CALLS[0] % 2
        CALLS[0] += 1
        before = {}
        for y, row in enumerate(farm["tiles"]):
            for x, t in enumerate(row):
                if isinstance(t, dict) and "animal" in t:
                    before[(x, y)] = (t["animal"], int(t["yield_units"]),
                                      bool(t["fed_today"]), bool(t["cared_today"]),
                                      int(t.get("pending_care_bonus", 0) or 0))
        orig(farm, day)
        for (x, y), (sp, yu, fed, cared, pend) in before.items():
            t = farm["tiles"][y][x]
            key = (seat, day, sp)
            if not (isinstance(t, dict) and "animal" in t):
                REC[key]["escaped"] += 1
                continue
            a = ANIMALS[sp]
            due = (day + 1 - t["placed_day"] - a["first_yield_day"])
            made_raw = 0
            if due >= 0 and due % a["interval"] == 0:
                made_raw = 1 + (pend if fed else 0)
            got = int(t["yield_units"]) - yu
            REC[key]["made"] += got
            REC[key]["lost"] += max(0, made_raw - got)
            REC[key]["bonus"] += (pend if (fed and made_raw) else 0)
            REC[key]["fed"] += int(fed)
            REC[key]["cared"] += int(cared)
            REC[key]["tiles"] += 1
    kg._daily_refresh_animals, kg._yield_probe = wrapped, True


def run(make0, opp, seed, weeds, species, product):
    from kaggle_environments import make
    install()
    env = make("kaggriculture", configuration={"seed": seed, "weedSpawnChance": weeds}, debug=True)
    env.reset(2)
    CALLS[0] = 0
    REC.clear()
    p0, p1 = make0(), opp()
    held = {}
    for t in range(719):
        DAY[0] = t // 24
        o0, o1 = env.state[0].observation, env.state[1].observation
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if t % 24 == 23:
            o = env.state[0].observation
            priv = o.get("private") or {}
            shed = int((priv.get("shed") or {}).get(product, 0) or 0)
            inv = sum(collections.Counter(iv).get(product, 0)
                      for iv in (priv.get("inventories") or []))
            pen = sum(1 for r in o["farms"][0]["tiles"] for c in r
                      if isinstance(c, dict) and c.get("animal") == species)
            onbeast = sum(int(c["yield_units"]) for r in o["farms"][0]["tiles"] for c in r
                          if isinstance(c, dict) and c.get("animal") == species)
            held[t // 24] = (shed, inv, pen, onbeast)
        if env.state[0].status == "DONE":
            break
    return held


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="seb", choices=sorted(TAPES))
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--species", default="COW")
    args = ap.parse_args()
    product = {"COW": "MILK", "SHEEP": "WOOL", "GOOSE": "EGG", "CHICKEN": "EGG",
               "PIG": "FERTILIZER"}[args.species]

    replay, schedule, team = TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}
    opp = lambda: tape_policy(replay, team, 1)

    # **One REC per run.** Both runs write seat-0 and seat-1 keys, so sharing the dict adds the
    # tape's seat 0 into ours and doubles the (identical) opponent. Snapshot and clear between them.
    hheld = run(lambda: tape_policy(replay, team, 0), opp, args.seed, args.weeds,
                args.species, product)
    HIS = {k: collections.Counter(v) for k, v in REC.items()}
    a = schedule_agent.make_agent(thin, 0, router=True)
    oheld = run(lambda: (lambda o, t: a(o)), opp, args.seed, args.weeds,
                args.species, product)
    OUR = {k: collections.Counter(v) for k, v in REC.items()}

    print(f"{args.species} -> {product}   tape {args.tape} seed {args.seed} weeds {args.weeds}"
          f"   ours | tape,  both seat 0.  dusk refresh, from `_daily_refresh_animals`.")
    print(f"{'day':>4} | {'pen':>4}{'made':>5}{'lost':>5}{'bonu':>5}{'fed':>4}{'care':>5}"
          f"{'onan':>5}{'shed':>5}{'inv':>4} | "
          f"{'pen':>4}{'made':>5}{'lost':>5}{'bonu':>5}{'fed':>4}{'care':>5}"
          f"{'onan':>5}{'shed':>5}{'inv':>4}")
    tot = collections.Counter()
    for d in range(args.days):
        o = OUR.get((0, d, args.species), collections.Counter())
        h = HIS.get((0, d, args.species), collections.Counter())
        os_, oi, op_, oa = oheld.get(d, (0, 0, 0, 0))
        hs, hi, hp, ha = hheld.get(d, (0, 0, 0, 0))
        for k in ("made", "lost", "bonus", "fed", "cared"):
            tot["o" + k] += o[k]
            tot["h" + k] += h[k]
        tot["oesc"] += o["escaped"]
        tot["hesc"] += h["escaped"]
        print(f"{d:>4} | {op_:>4}{o['made']:>5}{o['lost']:>5}{o['bonus']:>5}{o['fed']:>4}"
              f"{o['cared']:>5}{oa:>5}{os_:>5}{oi:>4} | "
              f"{hp:>4}{h['made']:>5}{h['lost']:>5}{h['bonus']:>5}{h['fed']:>4}"
              f"{h['cared']:>5}{ha:>5}{hs:>5}{hi:>4}")
    print(f"\n  season   made {tot['omade']}/{tot['hmade']}   lost-to-max_held "
          f"{tot['olost']}/{tot['hlost']}   care-bonus {tot['obonus']}/{tot['hbonus']}   "
          f"fed-tile-days {tot['ofed']}/{tot['hfed']}   cared-tile-days "
          f"{tot['ocared']}/{tot['hcared']}   escaped {tot['oesc']}/{tot['hesc']}")


if __name__ == "__main__":
    main()
