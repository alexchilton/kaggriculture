"""Stop hand-writing sell rules. SEARCH for the schedule, and find out what is actually on the table.

Eight hand-written arms all lost, and that says nothing about whether our selling is good -- it says
those eight rules were bad. Four of them could not have won by construction: they appended sells to
the agent's own, so they sold our full volume PLUS extra and walked every book down.

This does not propose a rule. It takes the agent's sell decisions as a starting point and hill-climbs
the QUANTITIES, in the real environment, and reports how much better the best schedule found is.

**What it optimises.** For each product, one multiplier on how much of the shed the agent is allowed
to release per turn, plus one "hold until day D" per product. That is 2 numbers per sellable product.
Small enough to search, expressive enough to contain: sell everything immediately (mult high),
withhold and dump at the close (D late), and everything between -- which is the shape
`carrot_hinge` uses to make $37,848 on the final day.

**Why a search and not another rule.** A rule encodes a theory. Today's theories were all wrong and
each one cost a run to find out. A search only needs the objective to be right, and the objective
here is the environment's own final bank.

**The number that matters is the GAP, not the winner.** If the best schedule found beats the shipped
agent by a few hundred dollars, our selling is close to optimal and this whole line should be
dropped. If it beats it by tens of thousands, it is not, and the rule can be reverse-engineered from
what the search chose. Either answer is worth having; today produced neither.

Coordinate ascent, one parameter at a time, accepting only improvements measured on the SAME seeds.
Seeds are fixed across the whole search so a step is never accepted on a lucky draw -- the winner's
curse is recorded in `CLAUDE.md` as having cost 11 accepted moves for +1.6% once already.

    python -u scripts/search_the_sell_schedule.py --seeds 4 --rounds 2 --workers 6
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
SHED_CAP = 100

#: The search space, per product: how much of the holding may go in one turn, and the first day any
#: of it may go at all. `mult = 1.0, hold = 0` reproduces "sell what the agent asked for".
MULTS = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)
HOLDS = (0, 12, 18, 22, 26, 29)


def _play(job):
    """One season under a parameter dict. Returns the final bank."""
    params, seed, opponent, module_name, shops = job
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build

    SA = importlib.import_module(f"kagg.search.{module_name}")
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)

    for t in range(30 * TPD):
        if shops is not None:
            env.state[0].observation["town"]["unlocked_shops"] = list(shops)
        o0 = env.state[0].observation
        day = t // TPD
        priv = o0.get("private") or {}
        shed = {k: int(v or 0) for k, v in (priv.get("shed") or {}).items()}

        a0 = me(o0, env.configuration)

        # **REPLACE the agent's sells, never append to them.** Appending was the defect in four of
        # today's arms: the farm sold its normal volume plus the arm's, so every book fell and the
        # comparison was rigged against the arm before it began.
        want = collections.Counter()
        for o in (a0["market"] or []):
            if isinstance(o, (list, tuple)) and len(o) > 2 and str(o[0]).upper() == "SELL":
                want[o[1]] += int(o[2])

        new_sells = []
        for p in SA.SELLABLE:
            mult, hold = params.get(p, (1.0, 0))
            have = shed.get(p, 0)
            if have <= 0:
                continue
            if day < hold:
                # Withheld -- unless it is about to rot, which no strategy can want.
                carried = 0
                for inv in (priv.get("inventories") or []):
                    carried += sum(int(v or 0) for k, v in (inv or {}).items()
                                   if k in SA.SELLABLE)
                if sum(shed.get(q, 0) for q in SA.SELLABLE) + carried <= SHED_CAP:
                    continue
            n = int(min(have, round(want.get(p, 0) * mult)))
            if day >= 29:                      # the close: nothing is worth holding past the end
                n = have
            if n > 0:
                new_sells.append(["SELL", p, n])

        market, placed = [], False
        for o in (a0["market"] or []):
            if isinstance(o, (list, tuple)) and o and str(o[0]).upper() == "SELL":
                if not placed:
                    market.extend(new_sells)
                    placed = True
                continue
            market.append(o)
        if not placed:
            market.extend(new_sells)
        market = market[:10]

        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": market},
                  them(env.state[1].observation, env.configuration)])
        if env.done:
            break
    del KG
    return float(env.state[0].observation["farms"][0]["money"])


def score(pool, params, seeds, opponent, module, shops):
    jobs = [(params, s, opponent, module, shops) for s in seeds]
    return sum(pool.map(_play, jobs)) / len(seeds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--first-seed", type=int, default=700)
    ap.add_argument("--opponent", default="contrarian")
    ap.add_argument("--module", default="schedule_agent")
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--world", default="", help="PRODUCT:drain to force, or blank for as-drawn")
    ap.add_argument("--out", default="data/logs/sell_schedule_search.csv")
    a = ap.parse_args()

    seeds = list(range(a.first_seed, a.first_seed + a.seeds))
    shops = None
    if a.world:
        from force_the_shops import shops_for_drain
        prod, _, lvl = a.world.partition(":")
        shops, got = shops_for_drain(prod, int(lvl))
        print(f"forced world {prod} drain {got}: {shops}")

    SA = importlib.import_module(f"kagg.search.{a.module}")
    products = list(SA.SELLABLE)

    # `mult = 1.0, hold = 0` for every product IS the shipped agent. The search must reproduce its
    # bank at this point or the harness is not neutral, and every delta below would be an artefact.
    base_params = {p: (1.0, 0) for p in products}

    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("round,product,mult,hold,mean_bank,accepted\n")
    fh.flush()

    clock = time.perf_counter()
    with ProcessPoolExecutor(max_workers=a.workers) as pool:
        control = score(pool, base_params, seeds, a.opponent, a.module, shops)
        print(f"control (mult=1, hold=0, i.e. the shipped agent): {control:,.0f}")
        print(f"seeds {seeds} vs {a.opponent}\n", flush=True)

        best_params = dict(base_params)
        best = control
        for rnd in range(a.rounds):
            for p in products:
                cur_mult, cur_hold = best_params[p]
                for mult in MULTS:
                    for hold in HOLDS:
                        if (mult, hold) == (cur_mult, cur_hold):
                            continue
                        trial = dict(best_params)
                        trial[p] = (mult, hold)
                        got = score(pool, trial, seeds, a.opponent, a.module, shops)
                        ok = got > best
                        fh.write(f"{rnd},{p},{mult},{hold},{got:.0f},{int(ok)}\n")
                        fh.flush()
                        if ok:
                            best, best_params = got, trial
                            print(f"  r{rnd} {p:<12} mult {mult:<5} hold {hold:<3} "
                                  f"-> {got:>10,.0f}  ACCEPT  (+{got - control:,.0f} vs control)",
                                  flush=True)
                print(f"  r{rnd} {p:<12} done, best {best:,.0f}", flush=True)

    fh.close()
    print(f"\ncontrol      {control:>12,.0f}")
    print(f"best found   {best:>12,.0f}")
    print(f"GAP          {best - control:>+12,.0f}   ({100.0 * (best - control) / control:+.1f}%)")
    print("\nbest parameters (product: sell-multiplier, hold-until-day)")
    for p in products:
        if best_params[p] != (1.0, 0):
            print(f"  {p:<12} mult {best_params[p][0]:<6} hold d{best_params[p][1]}")
    print("\nThe GAP is the answer. Small => our selling is near optimal and this line closes.")
    print("Large => it is not, and the rule can be read off the parameters above.")
    print(f"\n{time.perf_counter() - clock:.0f}s")


if __name__ == "__main__":
    main()
