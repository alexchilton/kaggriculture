"""Our shipped plan against the recorded field, over many seeds.

The five tapes in `breakdown.TAPES` are the ones that carry a derived `schedule.json`, and that is a
fact about OUR side of the board. It has nothing to do with who we can play: our planner always runs
the plan we intend to ship, so any recorded seat in `data/seed_scripts/` is a usable opponent -- 106
replays, not 5.

One seed says nothing. `env.reset()` draws a fresh seed unless one is pinned and identical play has
measured $48k and $59k on two draws, so every figure is a median with its range and the per-seed rows
print as they land -- a run that is killed half way is still worth reading.

**Only interval-24 recordings by default.** `townCenterSellInterval` went 12 -> 24 in 1.32.6 and the
ladder runs 24; the economy is taken from each recording, so a 12 tape is replayed at 12 and is a
measurement of a game nobody plays any more.

**A replayed opponent is not that player.** Their recorded actions were chosen against somebody else,
so they do not adapt to us, and they sell into a book our sales have already moved. It is a sparring
measure, not a prediction of the ladder.

    python -u scripts/tape_sweep.py --seeds 8 --top 20 | tee data/logs/tape_sweep.log
"""

import argparse
import collections
import importlib
import json
import pathlib
import statistics
import sys
import time

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

import breakdown as B
from kaggle_environments import make

from kagg.logs import get_logger

log = get_logger(__name__)

TPD = 24
#: The plan we intend to ship, and the one `build_planner_submission.py` embeds.
OURS = "data/seed_scripts/top_guys/90976060/schedule.json"
#: Our own past agents. Playable, but a mirror answers "what beats me", not "what beats the field",
#: so they are excluded unless asked for.
US = "alex chilton"


def opponents(root="data/seed_scripts", interval=24, allow_us=False):
    """`[(label, replay, team)]` -- every recorded seat we can drive, best-scoring seat first."""
    out, seen = [], set()
    for p in sorted(pathlib.Path(root).rglob("*.json")):
        if p.name == "schedule.json":
            continue
        try:
            d = json.loads(p.read_text())
        except Exception:                                               # noqa: BLE001
            continue
        if not isinstance(d, dict):
            continue
        if ((d.get("configuration") or {}).get("townCenterSellInterval")) != interval:
            continue
        names = (d.get("info") or {}).get("TeamNames") or []
        rewards = d.get("rewards") or []
        if len(names) != 2 or len(rewards) != 2 or any(r is None for r in rewards):
            continue
        # Drive the seat that WON, unless it is us. The point is to face the strongest recorded play.
        order = sorted(range(2), key=lambda i: -float(rewards[i]))
        for i in order:
            if not allow_us and names[i] == US:
                continue
            key = (names[i], p.stem)
            if key in seen:
                continue
            seen.add(key)
            out.append((f"{names[i]} @{p.stem}", str(p), names[i], float(rewards[i])))
            break
    out.sort(key=lambda r: -r[3])
    return out


def play(replay, team, seed, days, weeds, module, schedule):
    """One full game: our plan in seat 0, the recording in seat 1. Returns `(ours, theirs)`."""
    raw = json.loads(pathlib.Path(schedule).read_text())
    sched = {int(k): {a: b for a, b in v.items() if a not in B.TAPE_ONLY}
             for k, v in raw.items()}
    B.schedule_agent = SA = importlib.import_module(module)
    CREW = importlib.import_module("kagg.search.crew")
    was, CREW.STRICT_FEASIBILITY = CREW.STRICT_FEASIBILITY, False
    try:
        env = make("kaggriculture",
                   configuration=dict(B.env_config(replay), seed=seed, weedSpawnChance=weeds),
                   debug=False)
        env.reset(2)
        agent = SA.make_agent(sched, 0, router=True)
        opp = B.tape_policy(replay, team, 1)
        # 719, not 720: the env is DONE on the last step and stepping it again raises.
        for t in range(min(719, TPD * days)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
            if env.state[0].status == "DONE":
                break
        farms = env.state[0].observation["farms"]
        return float(farms[0]["money"]), float(farms[1]["money"])
    finally:
        CREW.STRICT_FEASIBILITY = was


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--first-seed", type=int, default=11)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--interval", type=int, default=24)
    ap.add_argument("--top", type=int, default=20, help="strongest N recorded seats")
    #: **`--top` ranks by RECORDED BANK, which is not the same as "who beat us".** Every seat in
    #: `data/seed_scripts/ladder` is a game we actually lost, and they bank $96k-$105k against the
    #: archive's $106k-$138k -- so the whole ladder set sits at rank 10 and below and `--top 8`
    #: faces none of it. Point `--root` at a subdirectory to sweep a specific field.
    ap.add_argument("--root", default="data/seed_scripts",
                    help="restrict the field to one directory, e.g. data/seed_scripts/ladder")
    ap.add_argument("--allow-us", action="store_true", help="include our own past agents")
    ap.add_argument("--module", default="kagg.search.schedule_agent_1455mh")
    ap.add_argument("--schedule", default=OURS)
    #: `crew.ACTIVE_UNTIL_DAY` decides which days the crew planner owns; everything else falls
    #: through to `cover.cover`. It is 7 at HEAD and 30 in the working tree, and the difference has
    #: never been measured over a full season -- only on the d0-d6 grid it was tuned for.
    ap.add_argument("--active-until", type=int, default=None)
    args = ap.parse_args()

    if args.active_until is not None:
        importlib.import_module("kagg.search.crew").ACTIVE_UNTIL_DAY = args.active_until

    seeds = [args.first_seed + i for i in range(args.seeds)]
    field = opponents(root=args.root, interval=args.interval, allow_us=args.allow_us)[:args.top]

    print(f"module   {args.module}")
    print(f"schedule {args.schedule}")
    print(f"field    {args.root}")
    print(f"days {args.days}   weeds {args.weeds}   interval {args.interval}")
    print(f"seeds {seeds}")
    log.info("field of %d recorded seats", len(field))

    rows, wins_all, t_start = collections.defaultdict(list), [], time.time()
    for label, replay, team, banked in field:
        log.info("=== %s   recorded $%,.0f ===".replace("%,", "%"), label, banked)
        for s in seeds:
            t0 = time.time()
            try:
                ours, theirs = play(replay, team, s, args.days, args.weeds,
                                    args.module, args.schedule)
            except Exception as exc:                                    # noqa: BLE001
                log.warning("seed %3d  ERROR  %s: %s", s, type(exc).__name__, exc)
                continue
            res = "WIN" if ours > theirs else ("LOSS" if ours < theirs else "DRAW")
            rows[label].append((ours, theirs, res))
            wins_all.append(res)
            log.info("seed %3d  ours $%9s   them $%9s   %-4s  %5.0fs",
                     s, f"{ours:,.0f}", f"{theirs:,.0f}", res, time.time() - t0)
        got = rows[label]
        if got:
            mine = [r[0] for r in got]
            w = sum(1 for r in got if r[2] == "WIN")
            log.info("-> median $%s  range $%s-$%s  WIN %d/%d",
                     f"{statistics.median(mine):,.0f}", f"{min(mine):,.0f}",
                     f"{max(mine):,.0f}", w, len(got))

    print("=== summary ===")
    print(f"{'opponent':<44} {'n':>3} {'ourMedian':>11} {'theirMedian':>12} {'wins':>8}")
    for label, _r, _t, _b in field:
        got = rows[label]
        if not got:
            continue
        mine = [r[0] for r in got]
        theirs = [r[1] for r in got]
        w = sum(1 for r in got if r[2] == "WIN")
        print(f"{label[:44]:<44} {len(got):>3} {statistics.median(mine):>11,.0f} "
              f"{statistics.median(theirs):>12,.0f} {w:>4}/{len(got)}")
    if wins_all:
        w = wins_all.count("WIN")
        d = wins_all.count("DRAW")
        print(f"\nOVERALL  {w}W {wins_all.count('LOSS')}L {d}D of {len(wins_all)} games"
              f"   win rate {(w + 0.5 * d) / len(wins_all):.3f}"
              f"   ({time.time()-t_start:.0f}s)")


if __name__ == "__main__":
    main()
