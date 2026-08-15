"""One day's SELLs, hour by hour, ours against the tape: offered, filled, and what backed them.

`sell 15/22` is a fill count, so it can be short for exactly three reasons -- we never offered,
we offered goods we did not hold, or the book took fewer than we posted. The row alone does not
say which. This prints all three per hour, per product, beside the shed level that had to back it.

    python -u scripts/sell_day.py --day 5
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int, default=5)
    ap.add_argument("--tape", default="victor")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--module", default="schedule_agent")
    args = ap.parse_args()

    import breakdown as B
    from kaggle_environments import make

    from kagg.analysis.fills import record_fills

    replay, schedule, team = B.TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    sa = __import__(f"kagg.search.{args.module}", fromlist=["make_agent"])

    cfg = dict(B.env_config(REPO / replay), seed=args.seed, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    rows = []
    with record_fills(env) as fills:
        prev = {0: collections.Counter(), 1: collections.Counter()}
        for t in range(24 * (args.day + 1)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), tape(o1, t)
            offers = {0: [o for o in (a0.get("market") or []) if o and o[0] == "SELL"],
                      1: [o for o in (a1.get("market") or []) if o and o[0] == "SELL"]}
            shed = {p: collections.Counter(o0["farms"][p].get("shed") or {}) for p in (0, 1)}
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            got = {}
            for p in (0, 1):
                cur = collections.Counter()
                for item in fills.products():
                    n = fills.units(p, "SELL", item)
                    if n:
                        cur[item] = n
                got[p] = cur - prev[p]
                prev[p] = cur
            if t // 24 == args.day:
                rows.append((t % 24, offers, got, shed))

    print(f"day {args.day}   tape {args.tape}   seed {args.seed}")
    print(f"{'h':>3}  {'OUR OFFER':<26} {'our fill':<16} {'our shed':<22} "
          f"{'TAPE OFFER':<24} {'tape fill':<14}")
    tot = {0: collections.Counter(), 1: collections.Counter()}
    for h, offers, got, shed in rows:
        for p in (0, 1):
            tot[p] += got[p]
        if not (offers[0] or offers[1] or got[0] or got[1]):
            continue

        def fmt(os_):
            return " ".join(f"{o[1]}x{o[2]}" for o in os_) or "-"

        def fc(c):
            return " ".join(f"{k}x{v}" for k, v in sorted(c.items())) or "-"

        sh = " ".join(f"{k}{v}" for k, v in sorted(shed[0].items()) if v) or "-"
        print(f"{h:>3}  {fmt(offers[0]):<26} {fc(got[0]):<16} {sh:<22} "
              f"{fmt(offers[1]):<24} {fc(got[1]):<14}")
    print(f"\n  filled  ours {fc_total(tot[0])}  ({sum(tot[0].values())})")
    print(f"          tape {fc_total(tot[1])}  ({sum(tot[1].values())})")


def fc_total(c):
    return " ".join(f"{k}x{v}" for k, v in sorted(c.items())) or "-"


if __name__ == "__main__":
    main()
