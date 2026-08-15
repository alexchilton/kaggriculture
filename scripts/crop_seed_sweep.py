"""Sweep the crop reallocation knobs across seeds and a FIELD of opponents.

Two things this does that `breakdown.py` cannot, and one it must not be asked to do.

- **It varies the seed.** The tape replays recorded ACTIONS, which are only valid on the board they
  were recorded against. A tape on a different seed plants into locked tiles and sells from an
  empty shed, so no cross-seed number from that harness means anything.
- **It plays a field, both seatings.** The ladder is Elo: a $40k win and a $400 win score the same,
  so the reported figure is WIN RATE and money is secondary. Market orders settle in seat order,
  so each seed is played twice with the seats exchanged.
- **It must not be read as a per-cell verdict.** Seed variance in this project is ~15%. With 24
  seeds a cell's mean is still soft; what the grid is for is finding the SHAPE, and whether the
  optimum is a constant or something that tracks the shop draw.

The last point is the real question. The 2026-08-15 balance change makes TOMATO viable in ~50% of
games, CARROT ~26%, EGG ~22% -- deliberately not universally. So a single best (tomato, carrot)
pair may not exist, and the per-seed drain recorded alongside is what a conditional would key on.
"""
import collections
import itertools
import json
import pathlib
import shutil
import sys
import time

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
WORK = REPO / "data" / "sweep"
FROZEN = WORK / "frozen_shipped.py"

SEEDS = list(range(1, 25))
TOMATOES = (0, 4, 8, 16)
CARROTS = (0, 4, 8, 16)
WORKERS = 14

#: The field. `mirror` follows the candidate; the named ones are our own heuristic on different
#: dials and test robustness to crop mix only; `contrarian` is the one member with genuinely
#: different routing, hiring and sell rules; the frozen file is what we actually ship, and is the
#: only opponent whose result answers "is this better than the build on the ladder".
OPPONENTS = ("mirror", "contrarian", "wheat_only", "melon_heavy", "cow_heavy", "carrot_25")


def seed_drain(seed):
    """Units of each product the town absorbs over the season, from the shop draw alone.

    `_town_consume` removes one unit of each product a shop sells every `townShopSellInterval`
    steps, doubled when the shop sells only one product. A shop unlocked on day D therefore drains
    for the 30-D days that remain.
    """
    from kaggle_environments import make
    import reference.kaggriculture as KG

    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    first_seen = {}
    for t in range(0, 719, 24):
        for s in env.state[0].observation.get("shops") or []:
            name = s if isinstance(s, str) else s.get("type")
            first_seen.setdefault((name, len(first_seen)), t // 24)
        for _ in range(24):
            env.step([[], []])
            if env.done:
                break
        if env.done:
            break
    total = collections.Counter()
    for (name, _), day in first_seen.items():
        prods = KG.SHOPS.get(name, {}).get("products", [])
        mult = 2 if len(prods) == 1 else 1
        for p in prods:
            total[p] += mult * (24 // KG.DEFAULTS.get("townShopSellInterval", 4)) * (30 - day)
    return total


def write_candidate(tomato, carrot):
    path = WORK / f"cand_t{tomato}_c{carrot}.py"
    path.write_text(
        f"import sys\n"
        f"sys.path.insert(0, {str(REPO)!r})\n"
        f"import kagg.search.schedule_agent as A\n"
        f"import kagg.plan as PLAN\n"
        f"A.WHEAT_TILES_TO_TOMATO = {tomato}\n"
        f"A.WHEAT_TILES_TO_CARROT = {carrot}\n"
        f"_S = PLAN.load({str(REPO / 'data/seed_scripts/kawashigi/schedule.json')!r})\n"
        f"_A = {{}}\n"
        f"def agent(obs, config):\n"
        f"    seat = obs['player']\n"
        f"    if seat not in _A:\n"
        f"        _A[seat] = A.make_agent(_S, me=seat)\n"
        f"    return _A[seat](obs, obs['step'])\n"
    )
    return str(path)


def main():
    from kagg.arena import pool

    WORK.mkdir(parents=True, exist_ok=True)
    (REPO / "data" / "logs").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO / "submission" / "main.py", FROZEN)

    field = OPPONENTS + (str(FROZEN),)
    n = len(TOMATOES) * len(CARROTS) * len(SEEDS) * 2 * len(field)
    print(f"seeds {SEEDS[0]}-{SEEDS[-1]}   tomato {TOMATOES}   carrot {CARROTS}")
    print(f"field {field}")
    print(f"{n:,} games, {WORKERS} workers\n", flush=True)

    print("per-seed town drain, units absorbed over the season:")
    print(f"{'seed':>5} {'TOMATO':>8} {'CARROT':>8} {'EGG':>8} {'WHEAT':>8} {'WOOL':>8} {'MILK':>8}")
    drain = {}
    for s in SEEDS:
        try:
            d = seed_drain(s)
            drain[s] = dict(d)
            print(f"{s:>5} {d['TOMATO']:>8} {d['CARROT']:>8} {d['EGG']:>8} "
                  f"{d['WHEAT']:>8} {d['WOOL']:>8} {d['MILK']:>8}", flush=True)
        except Exception as e:
            print(f"{s:>5}   FAILED {type(e).__name__}: {e}", flush=True)
    json.dump(drain, open(REPO / "data/logs/seed_drains.json", "w"), indent=1)

    print(f"\n{'tomato':>7} {'carrot':>7} {'WIN RATE':>10} {'mean $':>11} {'vs shipped':>11}   per-opponent")
    rows = []
    for tom, car in itertools.product(TOMATOES, CARROTS):
        t0 = time.time()
        cand = write_candidate(tom, car)
        try:
            res = pool.evaluate(cand, SEEDS, opponents=field, workers=WORKERS)
        except Exception as e:
            print(f"{tom:>7} {car:>7}   FAILED {type(e).__name__}: {e}", flush=True)
            continue
        shipped = res.per_opponent.get(str(FROZEN), (float("nan"), float("nan")))
        per = "  ".join(f"{k.split('/')[-1][:12]}:{v[0]:.0%}" for k, v in sorted(res.per_opponent.items()))
        print(f"{tom:>7} {car:>7} {res.win_rate:>9.1%} {res.mean_money:>11,.0f} "
              f"{shipped[0]:>10.0%}   {per}   [{time.time()-t0:.0f}s]", flush=True)
        rows.append(dict(tomato=tom, carrot=car, win_rate=res.win_rate,
                         mean_money=res.mean_money, vs_shipped=shipped[0],
                         per_opponent={k: list(v) for k, v in res.per_opponent.items()}))
        json.dump(rows, open(REPO / "data/logs/crop_sweep_rows.json", "w"), indent=1)

    print("\nwrote data/logs/seed_drains.json and data/logs/crop_sweep_rows.json")
    if rows:
        best = max(rows, key=lambda r: r["win_rate"])
        print(f"best by win rate: tomato={best['tomato']} carrot={best['carrot']} "
              f"{best['win_rate']:.1%}, mean ${best['mean_money']:,.0f}")


if __name__ == "__main__":
    main()
