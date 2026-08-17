"""How much of our season is the SHOP DRAW? Run N seeds with the shops left free.

Every grid in this repo pins the shops -- `shops=B.recorded_shops(replay)` -- and that is correct
for tape-matching, because comparing op-for-op needs the draw held still. It is wrong for valuing an
arm: with the draw pinned and `weedSpawnChance 0.0` the game is deterministic, so every seed returns
the same number and a sweep reads its own noise as zero.

`reference/kaggriculture.py:869` is the whole of the randomness that survives:

    rng = random.Random((seed * 1_000_003) ^ day)
    if next_day % shop_interval == 0:
        town["unlocked_shops"].append(rng.choice(sorted(SHOPS)))

One shop every three days, drawn WITH REPLACEMENT, into a `town` both players share. Weeds are the
only other RNG and were measured at 0-2 crop-relevant events a season (`weedSpawnChance` fires on
EMPTY tiles only, and a full board has almost none).

So this number sizes every experiment that follows it: an arm worth less than the spread cannot be
selected on fewer seeds than the spread demands. It is also the reason a shop-dependent arm --
tomato needs `x ~ 2T`, i.e. a book the shops have drained hard -- has to be a BRANCH read off
`unlocked_shops`, not a tuned constant that assumes the average draw.

    python -u scripts/how_much_does_the_draw_move_us.py --seeds 12 --arm straw
"""
import argparse
import collections
import importlib
import json
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
MELON_SEASON = "data/seed_scripts/kawashigi/92498144.json"
STRAWBERRY_SEASON = "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"


def one(arm, seed, weeds, days, pin_shops):
    """`(our money, their money, won, shops drawn)` for one season."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if arm == "straw" else 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / (STRAWBERRY_SEASON if arm == "straw" else MELON_SEASON))
    economy = B.env_config(replay)
    shops = B.recorded_shops(replay) if pin_shops else None

    env = make("kaggriculture", configuration=dict(economy, seed=seed, weedSpawnChance=weeds),
               debug=True)
    env.reset(2)
    agent, opp = SA.make_agent(sched, 0), B.tape_policy(replay, TEAM, 1)
    for t in range(days * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if shops is not None:
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        a0, a1 = agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o1["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])
        if env.done:
            break
    fin = env.state[0].observation
    ours = fin["farms"][0]["money"]
    theirs = fin["farms"][1]["money"] if len(fin["farms"]) > 1 else 0.0
    drawn = tuple(sorted(collections.Counter(fin["town"]["unlocked_shops"]).items()))
    return ours, theirs, ours > theirs, drawn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="straw")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--first-seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.005,
                    help="the ladder's rate. The draw is the point, so do not pin this either.")
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    seeds = [a.first_seed + 97 * i for i in range(a.seeds)]
    print(f"arm {a.arm!r}, weeds {a.weeds}, {a.seeds} seeds, shops FREE\n")
    print(f"{'seed':>12} {'ours':>12} {'theirs':>12} {'win':>5}   shops drawn")
    rows = []
    for s in seeds:
        ours, theirs, won, drawn = one(a.arm, s, a.weeds, a.days, pin_shops=False)
        rows.append((s, ours, theirs, won))
        shops = " ".join(f"{k}x{v}" for k, v in drawn)
        print(f"{s:>12} {round(ours):>12,} {round(theirs):>12,} {'W' if won else 'L':>5}   {shops}",
              flush=True)

    mine = [r[1] for r in rows]
    wins = sum(1 for r in rows if r[3])
    print(f"\n  ours  mean {statistics.mean(mine):>12,.0f}   sd {statistics.pstdev(mine):>10,.0f}"
          f"   min {min(mine):>10,.0f}   max {max(mine):>10,.0f}")
    print(f"  spread max-min ${max(mine) - min(mine):,.0f} "
          f"= {100 * (max(mine) - min(mine)) / max(1, statistics.mean(mine)):.0f}% of the mean")
    print(f"  win rate {wins}/{len(rows)}")
    sd = statistics.pstdev(mine)
    if sd:
        print(f"\n  To resolve an arm worth $X at ~2 standard errors, you need about "
              f"(2*{sd:,.0f}/X)^2 seeds:")
        for x in (1000, 2000, 5000, 10000):
            print(f"     ${x:>6,}  ->  {max(1, round((2 * sd / x) ** 2)):>4} seeds")


if __name__ == "__main__":
    main()
