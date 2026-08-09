"""Task #51: confirm LATE_SELL_BIAS on a seed block disjoint from the one that found it.

Fable measured +12.5pp of pool win rate on seeds 20-27 (docs/fable_market_shape_2026-08-09.md §4).
`CLAUDE.md` requires a search winner be confirmed on a fresh draw -- a fixed 3-seed objective once
reported +40% where held-out seeds said +12.8%, and seed variance here is ~15%. This re-measures on
seeds 40-47, disjoint from 20-27 and from the 2/11 used to find the candidate, and replays 20-27
alongside as a control.

**One agent instance per match, deliberately -- this is not how `run_arena` does it.**
`kagg.arena.run_arena` takes an agent *value* and reuses that one object across every seed and both
seatings, while `make_agent`'s closure builds its `state` dict once (`day=-1`, `hired`, `bought`,
`assigned`) and never resets on a new game. Driving `run_arena` directly therefore carries hiring
counts and purchase tallies from one game into the next. This walks `run_match` itself and rebuilds
the agent per match. Aggregation is otherwise identical to `run_arena`: both seatings per seed, win
on strict `>`, money oriented to our seat.

The opposite error is equally fatal and was made first here: a factory that rebuilds the agent on
every OBSERVATION destroys per-day state and banks $77 a season instead of tens of thousands. If a
mean money figure below is in the hundreds, that is the bug, not the flag.

Selection is on WIN RATE, not money -- the ladder is Elo.
"""
import argparse
import importlib
import json
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.agents import contrarian, heuristic, rancher
from kagg.arena.arena import run_match

#: `rancher` exposes a bare `agent`; the other two expose a `make_agent` factory.
POOL = {"heuristic": heuristic.make_agent,
        "rancher": (lambda: rancher.agent),
        "contrarian": contrarian.make_agent}

SCHED = pathlib.Path("data/seed_scripts/top_guys/90976060/schedule.json")
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")


def _thin():
    sched = {int(k): v for k, v in json.loads(SCHED.read_text()).items()}
    return {d: {k: v for k, v in r.items() if k not in TAPE_ONLY} for d, r in sched.items()}


def _ours(thin, flag, value, me):
    """One fresh agent, with `flag` forced to `value`. The arms differ by exactly that line."""
    import kagg.search.schedule_agent as SA
    importlib.reload(SA)
    setattr(SA, flag, value)
    inner = SA.make_agent(thin, me, router=True)
    return lambda obs, cfg=None: inner(obs)


def sweep(flag, value, seeds, pool, thin):
    rows, wins, games, money = [], 0, 0, 0.0
    for name in pool:
        w = g = 0
        m = 0.0
        for seed in seeds:
            for swapped in (False, True):
                us = _ours(thin, flag, value, 1 if swapped else 0)
                opp = POOL[name]()
                a, b = (opp, us) if swapped else (us, opp)
                res = run_match(a, b, seed)
                ours, theirs = (res.money[1], res.money[0]) if swapped else res.money
                w += ours > theirs
                m += ours
                g += 1
        rows.append((name, m / g, w / g))
        wins, games, money = wins + w, games + g, money + m
    return wins / games, money / games, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="40-47")
    ap.add_argument("--control", default="20-27", help="Fable's block; empty to skip")
    ap.add_argument("--pool", default="heuristic,rancher,contrarian")
    a = ap.parse_args()

    def span(s):
        lo, hi = s.split("-")
        return list(range(int(lo), int(hi) + 1))

    thin, pool = _thin(), a.pool.split(",")
    blocks = [(f"CONFIRM  seeds {a.seeds}", span(a.seeds))]
    if a.control:
        blocks.append((f"CONTROL  seeds {a.control}  (Fable's block, fresh-agent-per-match)",
                       span(a.control)))

    for label, seeds in blocks:
        print(f"\n===== {label} =====", flush=True)
        print(f"{'LATE_SELL_BIAS':<15}{'win rate':>9}{'mean money':>13}   per-opponent (money, win%)",
              flush=True)
        base = None
        for value in (False, True):
            wr, mm, rows = sweep("LATE_SELL_BIAS", value, seeds, pool, thin)
            per = "  ".join(f"{n} {m:,.0f}/{w:.1%}" for n, m, w in rows)
            print(f"{str(value):<15}{wr:>8.1%}{mm:>13,.0f}   {per}", flush=True)
            if base is None:
                base = (wr, mm)
            else:
                print(f"{'delta':<15}{wr - base[0]:>+8.1%}{mm - base[1]:>+13,.0f}", flush=True)


if __name__ == "__main__":
    main()
