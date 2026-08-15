"""Play a candidate against every 1.32.6 tape we hold, both seatings, with market jitter.

**This replaces the synthetic pool, and the reason is in `kagg/arena/pool.py`'s own numbers.** That
pool builds eight of its nine members from `heuristic.make_agent` with different crop dials -- same
routing, same hiring, same sell cadence. It tests robustness to crop mix and nothing else, we beat it
94.4%, and a gate that cannot lose cannot rank anything. `LATE_SELL_BIAS` measured as inert there for
exactly that reason.

The tapes are real ladder agents. 86 non-us seats across 66 distinct opponents on `1.32.6`, median
final bank $67,819 and max $138,262 -- including the fixed-playbook agents that repeat the same trace
every game, and Seb, who does not.

**A tape cannot be reproduced and does not need to be.** Kaggle publishes `configuration.seed` as
`null`, so replaying one banks a different number than it did on the day (measured: 61% off on one
seat, 19% on the other). That is irrelevant here -- both players share one board, and the question is
who won, not whether the recording reproduced. Re-seeding turns a fixed matchup into a distribution,
which is the variation the synthetic pool never had.

**What a tape is not: an adversary.** It is open-loop. It cannot see our farm, so it will not contest
a market it did not expect to be contested, and it will not punish anything we do specifically.
Beating a field of tapes is necessary, not sufficient. `--jitter` perturbs the MARKET orders only --
never `farmer` or `hands`, which are board-dependent and would produce an illegal or self-harming
season and measure us against a cripple.

    PYTHONPATH=. python3 -u scripts/tape_gate.py --label shipped
    PYTHONPATH=. python3 -u scripts/tape_gate.py --label units1 --feed-turn-cap 1
"""

import argparse
import collections
import concurrent.futures as cf
import glob
import json
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PLAN = REPO / "data/seed_scripts/top_guys/90976060/schedule.json"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
US = "alex chilton"


def opponents(limit=None):
    """Every non-us seat of every 1.32.6 tape, as `(path, recorded_seat, name, their_bank)`."""
    out = []
    for p in sorted(glob.glob(str(REPO / "data/seed_scripts/top_guys/*.json"))):
        try:
            d = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        if (d.get("configuration") or {}).get("townCenterSellInterval") != 24:
            continue          # 1.32.2 is a dead economy; see project_kaggriculture_ladder_is_1326
        names = (d.get("info") or {}).get("TeamNames") or ["?", "?"]
        rew = d.get("rewards") or [None, None]
        for s in (0, 1):
            if s < len(names) and names[s] != US and rew[s] is not None:
                out.append((p, s, names[s], float(rew[s])))
    return out[:limit] if limit else out


def _thin():
    sched = {int(k): v for k, v in json.loads(PLAN.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def one_match(job):
    """One game. Builds BOTH agents inside the worker.

    Never hand a prebuilt agent to a match runner: the tape agent holds a turn counter and our agent
    holds a whole season of state, and reusing either across games cost 17.8x once already
    (`docs/arena_state_leak_2026-08-09.md`).
    """
    path, rec_seat, name, our_seat, seed, flags = job
    from kaggle_environments import make

    import importlib
    SA = importlib.import_module("kagg.search." + (flags.pop("_module", None) or "schedule_agent"))
    for k, v in (flags or {}).items():
        setattr(SA, k, v)
    from kagg.arena.tape import build_tape_agent

    ours = SA.make_agent(_thin(), our_seat, router=True)
    theirs = build_tape_agent(path, rec_seat, jitter_seed=seed, drop=0.10, scale=0.20)
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.reset(2)
    agents = {our_seat: ours, 1 - our_seat: theirs}
    for _t in range(24 * 30):
        if env.done:
            break
        acts = []
        for p in (0, 1):
            o = env.state[p].observation
            a = agents[p](o)
            n = len(o["farms"][p].get("hands") or [])
            acts.append({"farmer": a["farmer"], "hands": list(a["hands"])[:n],
                         "market": a["market"]})
        env.step(acts)
    farms = env.state[0].observation["farms"]
    us, them = float(farms[our_seat]["money"]), float(farms[1 - our_seat]["money"])
    return name, us, them


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="candidate")
    ap.add_argument("--module", default="schedule_agent",
                    help="which agent module to play, e.g. schedule_agent")
    ap.add_argument("--limit", type=int, default=None, help="cap the number of tape seats")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--seed", type=int, default=101)
    ap.add_argument("--feed-turn-cap", type=int, default=None,
                    help="units per feed order; the size knob on the wheat buy")
    ap.add_argument("--feed-buy-turns", type=int, default=None,
                    help="turns per day that may buy feed")
    args = ap.parse_args()

    flags = {"_module": args.module}
    if args.feed_turn_cap is not None:
        flags["FEED_TURN_CAP"] = args.feed_turn_cap
    if args.feed_buy_turns is not None:
        flags["FEED_BUY_TURNS_PER_DAY"] = args.feed_buy_turns

    opps = opponents(args.limit)
    jobs = []
    for i, (path, rec_seat, name, _bank) in enumerate(opps):
        for our_seat in (0, 1):      # both seatings, so a seat advantage cannot masquerade as skill
            jobs.append((path, rec_seat, name, our_seat, args.seed + i, flags))

    print(f"{args.label}: {len(opps)} tape seats x 2 seatings = {len(jobs)} games, "
          f"flags={flags or 'none'}", flush=True)

    w = d = l = 0
    banks = []
    per_opp = collections.Counter()
    done = 0
    with cf.ProcessPoolExecutor(max_workers=args.workers) as ex:
        for name, us, them in ex.map(one_match, jobs):
            done += 1
            banks.append(us)
            if us > them:
                w += 1
                per_opp[name] += 1
            elif us == them:
                d += 1
            else:
                l += 1
            if done % 20 == 0:
                print(f"  {done}/{len(jobs)}  W{w} D{d} L{l}", flush=True)

    n = max(1, w + d + l)
    print(f"\n{args.label}: W{w} D{d} L{l}  win rate {100.0 * (w + 0.5 * d) / n:.1f}%  "
          f"mean bank ${statistics.mean(banks):,.0f}  median ${statistics.median(banks):,.0f}")
    # Who we never beat at all is the useful residue: a win rate hides an opponent we lose to 2/2.
    never = sorted({j[2] for j in jobs} - set(per_opp))
    if never:
        print(f"never beat ({len(never)}): " + ", ".join(never[:15])
              + ("..." if len(never) > 15 else ""))


if __name__ == "__main__":
    sys.exit(main())
