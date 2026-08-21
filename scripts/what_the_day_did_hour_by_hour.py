"""One day, hour by hour, ours against the tape. Names the turn a divergence starts.

`can_the_executor_play_his_own_row.py` grades whole days. When it fires BRANCH B the next question
is always "which op, on which turn", and a day-level count cannot answer it.

Same harness as everything else: `breakdown.run`'s economy and injected shop draw, weeds 0.0.

    python -u scripts/what_the_day_did_hour_by_hour.py --day 0 --seed 11
"""

import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import scripts.breakdown as BD                                              # noqa: E402
from kagg.search import kawa_library_agent                                  # noqa: E402

TAPE = "kawashigi"
GAME = "92498144"
WEEDS = 0.0
TPD = 24


def trace(policy_factory, opp, seed, economy, shops, day):
    """`{hour: (unit ops, market orders, money at the START of the turn)}` for one day."""
    from kaggle_environments import make

    cfg = dict(economy, seed=seed, weedSpawnChance=WEEDS)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    p0, p1 = policy_factory(), opp()
    out = {}
    for t in range((day + 1) * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        if shops is not None:
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // TPD == day:
            ops = collections.Counter()
            for u in [a0["farmer"]] + list(a0["hands"] or [])[:n0]:
                if u:
                    ops[str(u[0]) + ("" if len(u) < 2 else " " + str(u[1]))] += 1
            orders = ["%s %s x%s" % (o[0], o[1] if len(o) > 1 else "",
                                     o[2] if len(o) > 2 else 1)
                      for o in (a0["market"] or [])]
            out[t % TPD] = (ops, orders, float(o0["farms"][0]["money"]),
                            dict((o0.get("private") or {}).get("seeds") or {}))
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", type=int, default=0)
    ap.add_argument("--seed", type=int, default=11)
    a = ap.parse_args()

    BD.schedule_agent = BD.load_agent_module("schedule_agent")
    replay, _s, team = BD.TAPES[TAPE]
    economy = BD.env_config(replay)
    shops = BD.recorded_shops(replay)
    opp = lambda: BD.tape_policy(replay, team, 1)                           # noqa: E731

    def mine():
        agent = kawa_library_agent.make_agent(None, 0, router=True, opening_from=GAME)
        return lambda o, t: agent(o)

    ours = trace(mine, opp, a.seed, economy, shops, a.day)
    his = trace(lambda: BD.tape_policy(replay, team, 0), opp, a.seed, economy, shops, a.day)

    print("day %d, ours vs tape, hour by hour. seed %d, weeds %.3f\n" % (a.day, a.seed, WEEDS))
    for h in range(TPD):
        o_ops, o_ord, o_money, o_seed = ours.get(h, (collections.Counter(), [], 0.0, {}))
        h_ops, h_ord, h_money, h_seed = his.get(h, (collections.Counter(), [], 0.0, {}))
        mark = " " if o_ops == h_ops and o_ord == h_ord else "*"
        print("%s h%-2d  $%-8.0f ours  %-52s %s" % (mark, h, o_money,
              " ".join("%s x%d" % (k, v) for k, v in sorted(o_ops.items()))[:52],
              "; ".join(o_ord)[:44]))
        print("%s      $%-8.0f tape  %-52s %s" % (" ", h_money,
              " ".join("%s x%d" % (k, v) for k, v in sorted(h_ops.items()))[:52],
              "; ".join(h_ord)[:44]))
        if mark == "*":
            ours_seeds = {k: v for k, v in o_seed.items() if v}
            his_seeds = {k: v for k, v in h_seed.items() if v}
            if ours_seeds != his_seeds:
                print("        seeds held  ours %-28s tape %s" % (ours_seeds, his_seeds))


if __name__ == "__main__":
    main()
