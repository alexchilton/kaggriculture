"""The first day we are on our own: our ops against his, turn by turn.

Alex, 2026-08-26: *"start at the first day d12"*, *"and find the differences"*, after
*"you are always supposed to match the actions of the day of the tape ... we know his actions are
optimal for board and the schedule"*.

d0-d11 are his tape replayed verbatim, so the board at dawn on d12 is HIS board, exactly. From d12
our planner decides. Any difference from here is ours, and this prints it at the only resolution
that can be acted on: one row per turn, farmer and hands, ours against his.

Nothing here is a season total. Per the project rule, a fix is judged on the day it targets.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24


def ops_of(action):
    """`(farmer_op, [hand_ops])` as short strings."""
    a = action or {}
    f = a.get("farmer") or ["PASS"]
    hands = [h for h in (a.get("hands") or [])]
    short = lambda o: "-".join(str(x) for x in o) if o else "."      # noqa: E731
    return short(f), [short(h) for h in hands], [list(o) for o in (a.get("market") or [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="clone_open")
    ap.add_argument("--seed", type=int, default=123641874)
    ap.add_argument("--day", type=int, default=12)
    ap.add_argument("--handover", type=int, default=12)
    ap.add_argument("--weeds", type=float, default=0.005)
    args = ap.parse_args()

    from kaggle_environments import make
    import scripts.breakdown as B

    rel, sched_rel, team = B.TAPES[args.tape]
    path = str(REPO / rel)
    rep = json.loads(pathlib.Path(path).read_text())
    seat = rep["info"]["TeamNames"].index(team)

    economy = B.env_config(path)
    shops = B.recorded_shops(path)
    tape = B.tape_policy(path, team, 0)

    # Our agent, handed the season at `--handover` from his board.
    import kagg.plan as P
    from kagg.search import schedule_agent as SA
    sched = {int(k): v for k, v in json.loads((REPO / sched_rel).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()} \
        if hasattr(B, "TAPE_ONLY") else sched
    ours = SA.make_agent(thin, 0, router=True, start_day=args.handover)

    env = make("kaggriculture", configuration=dict(economy, seed=args.seed), debug=False)
    env.reset(2)
    opp = B.tape_policy(path, team, 0)

    lo, hi = args.day * TPD, (args.day + 1) * TPD
    rows, mine_counts, his_counts = [], collections.Counter(), collections.Counter()
    for t in range(719):
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        env.state[1].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        # Before the handover we ARE the tape; after it, our planner drives.
        a0 = tape(obs, t) if t < args.handover * TPD else ours(obs)
        if lo <= t < hi:
            his = (rep["steps"][t + 1][seat] or {}).get("action") if t + 1 < len(rep["steps"]) else {}
            mf, mh, mm = ops_of(a0)
            hf, hh, hm = ops_of(his)
            rows.append((t, mf, mh, mm, hf, hh, hm))
            for o in [mf] + mh:
                mine_counts[o.split("-")[0]] += 1
            for o in [hf] + hh:
                his_counts[o.split("-")[0]] += 1
        env.step([a0, opp(env.state[1].observation, t)])

    print(f"day {args.day}, tape {args.tape}, seed {args.seed}, handover d{args.handover}")
    print("ours on the left of each pair, his on the right\n")
    print(f"{'hour':>5}  {'farmer ours':<22}{'farmer his':<22}  hands ours -> his")
    for t, mf, mh, mm, hf, hh, hm in rows:
        flag = " " if mf == hf else "*"
        hands = ("  " + " ".join(mh) + "   ->   " + " ".join(hh)) if (mh or hh) else ""
        print(f"{t % TPD:>5}{flag} {mf:<22}{hf:<22}{hands}")
        if mm or hm:
            print(f"{'':>7} market {json.dumps(mm)}   ->   {json.dumps(hm)}")

    print(f"\n{'op':<16}{'ours':>6}{'his':>6}{'delta':>7}")
    for op in sorted(set(mine_counts) | set(his_counts)):
        a, b = mine_counts[op], his_counts[op]
        if a != b:
            print(f"{op:<16}{a:>6}{b:>6}{a - b:>+7}")


if __name__ == "__main__":
    main()
