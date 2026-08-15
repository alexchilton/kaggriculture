"""Geese vs no geese, scored on WIN RATE against the opponent pool over many seeds.

## Why not a single-seed A/B

Measured 2026-08-15, seed 1136131795: swapping ONE sheep for ONE goose moved our bank
$82,953 -> $105,738 and the frozen opponent's $82,615 -> $119,462. One sheep is ~8 wool units a
season. Wool's curve is quadratic (`above_func sq`, `T=105`), so those 8 units really do take it
from $1 to $49 -- but that is worth a couple of thousand, not thirty-six.

The rest is **chaos, not causation**. The season is deterministic, which means repeatable; it does
not mean small changes have small effects. One animal changes a placement, which changes a route,
which changes what is in the shed at the hour a price is quoted, and the seasons diverge. So a
single-seed delta of +$22,785 and one of -$4,996 are the same measurement: noise with a big
amplitude.

This is also why the melon/wool "the opponent gains what we give up" story cannot be read off one
game. Real evidence for it: game `93372504`, where our 10 cows against their 8 left milk floored at
d24 and wool at d16 for BOTH seats. Neither side profited from the extra animals.

## What this measures

- **Win rate first.** The ladder is Elo: a $43k win and a $4k win score the same. Money is reported
  second and is the noisier number.
- **Against a FIELD, not a mirror.** A mirror answers "what if both sides do it", which is a
  symmetric equilibrium, not a best response. Geese specifically break the mirror: vacating the wool
  book lifts the price for an opponent who kept their sheep, so a mirror over-punishes the move.
- `pool.evaluate` looks opponents up as `OPPONENTS[name]`, so every spec here must be a dict KEY.

## The known defect in the knob

`HERD_GEESE >= 2` returns a herd of 13 where 0 and 1 return 14 -- the second conversion places its
goose and loses the animal it replaced. `HERD_GEESE = 4` is byte-identical to 3. **So only arms 0
and 1 are trustworthy today**; 2 and 3 are included to size the bug, not to choose a setting.

    python -u scripts/geese_pool_eval.py --seeds 1 2 3 4 5 6 7 8 9 10 11 12
"""
import argparse
import json
import pathlib
import shutil
import sys
import time

sys.path.insert(0, ".")

REPO = pathlib.Path(__file__).resolve().parent.parent
WORK = REPO / "data" / "sweep"

#: Pool members that actually contest the book. `starter` and `pass` are excluded: they sell almost
#: nothing, so the market is never contested and every number against them is roughly 2x reality.
FIELD = ("mirror", "contrarian", "wheat_only", "melon_heavy", "cow_heavy", "carrot_25")


def write_candidate(geese):
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / f"geese_{geese}.py"
    path.write_text(
        f"import sys\n"
        f"sys.path.insert(0, {str(REPO)!r})\n"
        f"import kagg.search.schedule_agent as A\n"
        f"import kagg.plan as PLAN\n"
        f"A.HERD_GEESE = {geese}\n"
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(1, 17)))
    ap.add_argument("--geese", type=int, nargs="+", default=[0, 1, 2, 3])
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    from kagg.arena import pool

    print(f"geese arms {a.geese}, seeds {a.seeds}, field {FIELD}", flush=True)
    print(f"{len(a.geese)} arms x {len(a.seeds)} seeds x {len(FIELD)} opponents = "
          f"{len(a.geese) * len(a.seeds) * len(FIELD)} games\n", flush=True)
    print(f"{'arm':<10}{'WIN':>8}{'DRAW':>8}{'mean $':>12}   per-opponent win rate", flush=True)

    rows = []
    for g in a.geese:
        t0 = time.time()
        cand = write_candidate(g)
        try:
            res = pool.evaluate(cand, a.seeds, opponents=FIELD, workers=a.workers)
        except Exception as e:
            print(f"{('geese ' + str(g)):<10}  FAILED {type(e).__name__}: {e}", flush=True)
            continue
        per = "  ".join(f"{k[:9]}:{v[0]:.0%}" for k, v in sorted(res.per_opponent.items()))
        print(f"{('geese ' + str(g)):<10}{res.win_rate:>7.1%}{res.draw_rate:>8.1%}"
              f"{res.mean_money:>12,.0f}   {per}   [{time.time()-t0:.0f}s]", flush=True)
        rows.append(dict(geese=g, win_rate=res.win_rate, draw_rate=res.draw_rate,
                         mean_money=res.mean_money,
                         per_opponent={k: list(v) for k, v in res.per_opponent.items()}))
        json.dump(rows, open(REPO / "data/logs/geese_pool.json", "w"), indent=1)

    if len(rows) > 1:
        base = next((r for r in rows if r["geese"] == 0), rows[0])
        best = max(rows, key=lambda r: r["win_rate"])
        print(f"\nbaseline geese 0 : {base['win_rate']:.1%} win, ${base['mean_money']:,.0f}")
        print(f"best             : geese {best['geese']}  {best['win_rate']:.1%} win, "
              f"${best['mean_money']:,.0f}")
        print(f"\ndelta on win rate: {best['win_rate'] - base['win_rate']:+.1%}  "
              f"over {len(a.seeds) * len(FIELD)} games per arm")
    print("\nArms 2 and 3 carry a herd of 13 against 0 and 1's 14 -- a placement bug, not a "
          "setting. Do not read them as a dose curve.")


if __name__ == "__main__":
    main()
