"""Planner units + the NET's market, with our sell rule overriding the net's SELLs. Does it pay?

    python -u scripts/does_the_net_market_survive_the_sell_override.py --seeds 3

THE QUESTION
------------
Two rows are already measured, on this harness, these seeds, 719 turns, idle opponent, tape off
(`REPLAY_OPENING_DAYS = ()`):

    planner units + planner's own market                 150,396
    planner units + naive sell h16, reserve from d26     147,368     <- no net anywhere
    planner units + the net's market head                 62,427     <- the only net row

The config asked for is neither: **the net supplies the market, and its SELL orders are then
thrown away and replaced by the h16 / d26-dump rule.** Buys and hires -- which is what the bundle
head mostly emits -- survive; the timing decision the net is worst at is taken off it.

That is a real hypothesis and it is worth stating what would have to be true for it to win: the
net's $62,427 has to be caused by its SELLS (bad cadence, bad quantity, or none at all) rather than
by its BUYS. If the net is losing because it never buys seed or never hires, overriding the sells
changes nothing and this lands near $62,427. If it is losing because it floods or never sells, this
lands near $147,368.

Either answer is useful, and the two control arms are re-run rather than quoted so a harness that
has drifted since cannot be mistaken for a result.

THE NET RUNS THROUGH THE SHIPPABLE PATH
---------------------------------------
`kagg.agents.numpy_neural`, not `neural` -- pure numpy, the thing a submission can carry. Pinned to
the jax agent action-for-action by `tests/test_the_numpy_agent_plays_the_same_game.py`. Measuring
the jax one and shipping the numpy one would be measuring something we cannot upload.
"""
import argparse
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

CKPT = REPO / "data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl"
MAX_ORDERS = 10


def idle(_obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def feed_reserve(obs, seat, day, keep_wheat, release_from):
    """Wheat the herd still needs. Zero once nothing can eat it into product before the bell.

    `consecutive_unfed >= 2` removes the animal outright, so selling the feed is not a smaller sale,
    it is a dead cow. Past the last yield the wheat can only become cash, which is why it is
    released rather than held to the end.
    """
    return 0 if day >= release_from else keep_wheat


def naive_sells(obs, seat, keep_wheat):
    """Everything in the shed, less the herd's wheat reserve."""
    shed = dict((obs.get("private") or {}).get("shed") or {})
    out = []
    for item, n in sorted(shed.items()):
        n = int(n or 0)
        if item == "WHEAT":
            n = max(0, n - keep_wheat)
        if n > 0:
            out.append(["SELL", item, n])
    return out


def play(seed, turns, arm, net_agent=None, sell_hour=16, keep_wheat=20, release_from=26):
    """One season, seat 0 driven by `arm`, opponent idle. Returns the final bank."""
    from kaggle_environments import make

    from kagg import plan as PLAN
    from kagg.search import schedule_agent as SA

    planner = SA.make_agent(PLAN.load(), 0)
    env = make("kaggriculture", configuration={"seed": int(seed), "weedSpawnChance": 0.0},
               debug=False)
    env.reset(2)

    for turn in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        act = planner(obs)
        day, hour = int(obs.get("day", 0) or 0), int(obs.get("hour", 0) or 0)

        if arm in ("net", "net+override"):
            # The net supplies the whole market. Units stay the planner's.
            act["market"] = list(net_agent(obs).get("market") or [])

        if arm in ("planner+override", "net+override"):
            # Strip whatever SELLs are in there and put ours back, once a day.
            others = [o for o in (act.get("market") or []) if not (o and o[0] == "SELL")]
            mine = []
            if hour == sell_hour:
                keep = feed_reserve(obs, 0, day, keep_wheat, release_from)
                mine = naive_sells(obs, 0, keep)
            act["market"] = (mine + others)[:MAX_ORDERS]

        env.step([act, idle(env.state[1].observation)])

    return float(env.state[0].observation["farms"][0]["money"])


ARMS = ["planner", "planner+override", "net", "net+override"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--base-seed", type=int, default=9000)
    ap.add_argument("--turns", type=int, default=719)
    ap.add_argument("--ckpt", default=str(CKPT))
    args = ap.parse_args()

    from kagg.agents import numpy_neural as NN
    from kagg.search import schedule_agent as SA

    # **The planner arm, not the tape.** `REPLAY_OPENING_DAYS` ships as every day, which replays
    # カワシギ's recorded ops onto a fresh seed regardless of the board -- and would make every
    # number here a statement about his season rather than about the market rule under test.
    SA.REPLAY_OPENING_DAYS = ()

    net_agent = NN.make_agent(args.ckpt)
    seeds = [args.base_seed + 137 * i for i in range(args.seeds)]

    print("%d seeds, %d turns, idle opponent, planner replay OFF, net = %s"
          % (args.seeds, args.turns, pathlib.Path(args.ckpt).parent.name), flush=True)
    print("  %8s" % "seed" + "".join("%22s" % a for a in ARMS), flush=True)

    banks = {a: [] for a in ARMS}
    for s in seeds:
        row = []
        for a in ARMS:
            # A fresh memo per arm: `make_agent` holds one across the episode and resets on a
            # non-advancing step, but re-using it across arms would date this season's shops from
            # the previous one.
            agent = NN.make_agent(args.ckpt) if a.startswith("net") else None
            b = play(s, args.turns, a, net_agent=agent)
            banks[a].append(b)
            row.append("%22s" % format(b, ",.0f"))
        print("  %8d" % s + "".join(row), flush=True)

    print("  %8s" % "median" + "".join("%22s" % format(statistics.median(banks[a]), ",.0f")
                                       for a in ARMS), flush=True)
    print(flush=True)
    print("HOW TO READ IT", flush=True)
    print("  net+override near planner+override   the net's SELLS were the problem; its buys and", flush=True)
    print("                                       hires are fine and the config is shippable.", flush=True)
    print("  net+override near net                the net's BUYS are the problem; overriding the", flush=True)
    print("                                       sells changes nothing and this config is not it.", flush=True)
    if net_agent is None:
        print("  net agent failed to build", flush=True)


if __name__ == "__main__":
    main()
