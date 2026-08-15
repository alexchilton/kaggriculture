"""A/B the last-day walk-home slack across seeds: does one turn of head start bank the load?

Cross-seed, so the tape cannot be used -- it replays recorded ACTIONS, valid only on the board they
were recorded against. The opponent is the frozen shipped build, identical in both arms, so the
only thing that moves is `LAST_DAY_WALK_SLACK`.

Reports stranded units and their REALISED value (the book walked one unit at a time), because that
is what the change targets. Money is reported too but is the noisier number: seed variance in this
project is ~15%, which is far larger than the effect being measured.
"""
import collections
import importlib
import json
import pathlib
import sys

sys.path.insert(0, ".")

import reference.kaggriculture as KG

REPO = pathlib.Path(__file__).resolve().parent.parent
SEEDS = list(range(1, 17))
ARMS = (0, 1)


def realised(inventory, product, units):
    stock, total = inventory[product], 0.0
    for _ in range(int(units)):
        total += KG.market_price(product, stock)
        stock += 1
    return total


def play(seed, slack):
    from kaggle_environments import make

    A = importlib.import_module("kagg.search.schedule_agent")
    PLAN = importlib.import_module("kagg.plan")
    A.LAST_DAY_WALK_SLACK = slack

    sched = PLAN.load(str(REPO / "data/seed_scripts/kawashigi/schedule.json"))
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = str(REPO / "submission" / "main.py")
    env.run([me, opp])

    final = env.steps[-1]
    obs = final[0]["observation"]
    priv = obs["private"]
    inv = obs["market"]["inventory"]
    hands = collections.Counter()
    for h in (priv.get("inventories") or []):
        for k, v in (h or {}).items():
            hands[k] += v
    units = sum(n for p, n in hands.items() if p in inv and n > 0)
    value = sum(realised(inv, p, n) for p, n in hands.items() if p in inv and n > 0)
    return units, value, final[0]["reward"], final[1]["reward"]


def main():
    print(f"seeds {SEEDS[0]}-{SEEDS[-1]}, opponent = frozen submission/main.py\n")
    print(f"{'seed':>5} | {'slack=0 units':>13} {'value':>9} {'money':>10}"
          f" | {'slack=1 units':>13} {'value':>9} {'money':>10} | {'d value':>9} {'d money':>9}")
    rows = []
    for seed in SEEDS:
        out = {}
        for slack in ARMS:
            try:
                out[slack] = play(seed, slack)
            except Exception as e:
                print(f"{seed:>5}   slack={slack} FAILED {type(e).__name__}: {e}", flush=True)
                out[slack] = None
        if not all(out.values()):
            continue
        (u0, v0, m0, _), (u1, v1, m1, _) = out[0], out[1]
        rows.append((seed, u0, v0, m0, u1, v1, m1))
        print(f"{seed:>5} | {u0:>13} {v0:>9,.0f} {m0:>10,.0f}"
              f" | {u1:>13} {v1:>9,.0f} {m1:>10,.0f} | {v0-v1:>+9,.0f} {m1-m0:>+9,.0f}", flush=True)

    if rows:
        n = len(rows)
        print(f"\nover {n} seeds:")
        print(f"  stranded units  {sum(r[1] for r in rows)/n:>8.1f} -> {sum(r[4] for r in rows)/n:>8.1f}")
        print(f"  stranded value  {sum(r[2] for r in rows)/n:>8,.0f} -> {sum(r[5] for r in rows)/n:>8,.0f}")
        print(f"  mean money      {sum(r[3] for r in rows)/n:>8,.0f} -> {sum(r[6] for r in rows)/n:>8,.0f}")
        better = sum(1 for r in rows if r[6] > r[3])
        print(f"  money improved on {better}/{n} seeds; stranded improved on "
              f"{sum(1 for r in rows if r[5] < r[2])}/{n}")
        json.dump([list(r) for r in rows], open(REPO / "data/logs/walk_slack_ab.json", "w"), indent=1)


if __name__ == "__main__":
    main()
