"""Which tiles does each unit work, in what order? Ours against the tape, same format.

Alex's question: does the leader use the same lawnmower pattern we do? The op counts in
`breakdown.py` cannot answer it -- `water 21/46` says we watered less, not that we walked worse.
The geometry is the thing, and it is recoverable exactly: a unit's op acts on the tile it is
standing on, and the observation records every position each turn.

Read a row as one unit's whole day. A repeated tile is several ops at one stop, which is the number
that matters: a unit that does four things per stop pays one walk for four ops, and one that does
one thing per stop pays four walks for four ops.

**Positions are read from the PREVIOUS turn's observation**, because `steps[t]` records where the
unit ended up after acting, not where it stood when it acted -- the same off-by-one that shifted
every tile one move forward in `extract_tape.py`. At dawn the units are teleported home
(`reference/kaggriculture.py:848-849`), so turn 0 of a day reads its own record instead.

    python -u scripts/walk_pattern.py --days 9
"""

import argparse
import collections
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

import breakdown as B

TD = 24
WORK = {"PLANT", "WATER", "HARVEST", "FERTILIZE", "DIG", "BUILD_PASTURE", "BUILD_COOP",
        "PLACE", "FEED", "CARE", "COLLECT", "COLLECT_FERTILIZER"}


def positions(obs, seat):
    farm = obs["farms"][seat]
    out = [tuple(farm.get("farmer") or (4, 4))]
    for h in (farm.get("hands") or []):
        out.append(tuple(h if isinstance(h, (list, tuple)) else h.get("pos", (4, 4))))
    return out


def trace(make0, opp, seed, weeds, economy, stop_day):
    """Run one policy and return {(day, unit): [(tile, op), ...]} for WORK ops only."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration=dict(economy or {}, seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    p0, p1 = make0(), opp()
    seq = collections.defaultdict(list)
    prev = None
    for t in range(min(719, TD * stop_day)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        here = positions(o0, 0)
        # At dawn the previous turn's record is the END of yesterday, before the teleport home.
        at = here if t % TD == 0 else (prev or here)
        a0, a1 = p0(o0, t), p1(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        for u, a in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
            if a and a[0] in WORK and u < len(at):
                seq[(t // TD, u)].append((at[u], a[0]))
        prev = here
        env.step([a0, a1])
    return seq


def show(title, seq, days, min_ops):
    print(f"\n{title}")
    for day in range(days):
        rows = [(u, seq[(day, u)]) for u in range(24) if len(seq.get((day, u), [])) >= min_ops]
        if not rows:
            continue
        for u, s in rows:
            tiles = [p[0] for p in s]
            stops = 1 + sum(1 for i in range(1, len(tiles)) if tiles[i] != tiles[i - 1])
            print(f"  d{day} u{u}: {len(s):2d} ops / {stops:2d} stops  "
                  + " ".join(f"{r},{c}" for r, c in tiles))
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="victor", choices=sorted(B.TAPES))
    ap.add_argument("--module", default="schedule_agent_1455mh")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--days", type=int, default=9)
    ap.add_argument("--min-ops", type=int, default=3)
    args = ap.parse_args()

    import importlib
    B.schedule_agent = importlib.import_module("kagg.search." + args.module)

    replay, schedule, team = B.TAPES[args.tape]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(replay)
    opp = lambda: B.tape_policy(replay, team, 1)

    his = trace(lambda: B.tape_policy(replay, team, 0), opp, args.seed, args.weeds,
                economy, args.days)
    mine = lambda: (lambda a: (lambda o, t: a(o)))(
        B.schedule_agent.make_agent(thin, 0, router=True))
    ours = trace(mine, opp, args.seed, args.weeds, economy, args.days)

    def stats(seq):
        ops = sum(len(v) for v in seq.values())
        stops = sum(1 + sum(1 for i in range(1, len(v)) if v[i][0] != v[i - 1][0])
                    for v in seq.values() if v)
        return ops, stops, ops / max(stops, 1)

    show(f"TAPE ({team}) -- work-tile sequence per unit-day", his, args.days, args.min_ops)
    show(f"OURS ({args.module}) -- work-tile sequence per unit-day", ours, args.days, args.min_ops)

    print(f"{'':22} {'ops':>6} {'stops':>6} {'ops/stop':>9}")
    for name, seq in (("tape", his), ("ours", ours)):
        o, s, r = stats(seq)
        print(f"  {name:20} {o:6d} {s:6d} {r:9.2f}")
    print("\nops/stop is the payoff per walk. Lower means more walking for the same work.")

    # **The lawnmower test.** A sweep steps to an ADJACENT tile between stops; a chooser that ranks
    # tiles by value teleports across the field and pays a walk turn per square it crosses. So the
    # distribution of Manhattan distance between consecutive work stops IS the pattern, and the
    # backtrack rate says whether a column is finished before the next one starts.
    # **Split at `crew.ACTIVE_UNTIL_DAY`.** Days below it are planned by `crew.cover`, the
    # contiguous-run planner; days at or above fall through to `cover.cover`. An average across the
    # boundary describes neither, and the whole question is whether the sweep survives the handover.
    from kagg.search import crew as CREW
    bands = [("d0-d%d  crew.cover" % (CREW.ACTIVE_UNTIL_DAY - 1), 0, CREW.ACTIVE_UNTIL_DAY),
             ("d%d+    cover.cover" % CREW.ACTIVE_UNTIL_DAY, CREW.ACTIVE_UNTIL_DAY, 99)]
    print(f"\n{'':22} {'adj 1':>7} {'2':>6} {'3-4':>6} {'5+':>6} | {'mean':>6} {'backtrack':>10}")
    rows = [("tape  all", his), ("ours  all", ours)]
    for band, lo, hi in bands:
        for who, s in (("tape", his), ("ours", ours)):
            rows.append((f"{who}  {band}", {k: v for k, v in s.items() if lo <= k[0] < hi}))
    for name, seq in rows:
        hist = collections.Counter()
        tot = back = n = 0
        for (day, u), v in seq.items():
            tiles = [p[0] for p in v]
            stops = [tiles[0]] + [tiles[i] for i in range(1, len(tiles))
                                  if tiles[i] != tiles[i - 1]]
            for i in range(1, len(stops)):
                a, b = stops[i - 1], stops[i]
                d = abs(a[0] - b[0]) + abs(a[1] - b[1])
                hist["1" if d == 1 else "2" if d == 2 else "3-4" if d <= 4 else "5+"] += 1
                tot += d
                n += 1
            # A backtrack is a step that reverses the previous step's sign on either axis.
            for i in range(2, len(stops)):
                p, q, r_ = stops[i - 2], stops[i - 1], stops[i]
                if ((q[0] - p[0]) * (r_[0] - q[0]) < 0) or ((q[1] - p[1]) * (r_[1] - q[1]) < 0):
                    back += 1
        print(f"  {name:20} {hist['1']:7d} {hist['2']:6d} {hist['3-4']:6d} {hist['5+']:6d} | "
              f"{tot / max(n, 1):6.2f} {back / max(n, 1):9.1%}")


if __name__ == "__main__":
    main()
