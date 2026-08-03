"""Round-robin every numpy agent against every other, both seatings, and print the table.

**Why this exists.** `docs/public_meta_2026-08-03.md` puts the public field at $90k-$123k while our
best training opponent banks $27,340 -- but that figure comes from each agent's own docstring,
measured at different times against different opponents. Nobody has ever played our agents against
each other and written the numbers down in one place. `kagg/agents/homestead.py` in particular is 328
lines that no doc mentions and no benchmark has ever run.

**Both seatings, always.** `_process_market` quotes both players against the same inventory but
commits in seat order, so seat 0 has a real edge on contested trades. `run_arena` already plays every
seed twice with the seats exchanged for that reason; a one-seated number flatters or damns an agent
for free.

**Win rate, not money, is the ranking.** `CLAUDE.md`: the ladder is an Elo-style rating, so a $43k
win and a $4k win score identically. Money is printed beside it because it is the thing that
transfers to the public-meta comparison, not because it is the criterion.

    python3 scripts/bench_agents.py --seeds 8
"""

import argparse
import itertools
import os
import sys

# `scripts/` is not a package and the arena spawns worker processes that re-import this file.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kagg.arena import run_arena          # noqa: E402

AGENTS = ("homestead", "contrarian", "converter", "rancher", "shepherd", "heuristic", "starter")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--agents", default=",".join(AGENTS))
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()

    names = [a.strip() for a in args.agents.split(",") if a.strip()]
    seeds = range(args.seeds)
    print(f"{len(names)} agents, {args.seeds} seeds x 2 seatings = {args.seeds * 2} games per pair, "
          f"{args.workers} workers\n")

    wins = {n: 0.0 for n in names}
    games = {n: 0 for n in names}
    money = {n: [] for n in names}

    hdr = f"{'pair':<26} {'A wins':>7} {'draws':>6} {'A $':>10} {'B $':>10}"
    print(hdr)
    print("-" * len(hdr))
    for a, b in itertools.combinations(names, 2):
        try:
            r = run_arena(a, b, seeds=seeds, workers=args.workers)
        except Exception as e:                                        # noqa: BLE001
            print(f"{a} vs {b:<14} FAILED: {type(e).__name__}: {e}")
            continue
        # `run_arena` reports from A's point of view; a draw counts half to each, matching the
        # ladder's treatment and `arena.py:91-92`.
        n = r.games
        a_pts = r.win_rate * n + 0.5 * r.draw_rate * n
        wins[a] += a_pts
        wins[b] += n - a_pts
        games[a] += n
        games[b] += n
        ma = getattr(r, "mean_money", None)
        mb = getattr(r, "mean_money_b", None)
        if ma is not None:
            money[a].append(ma)
        if mb is not None:
            money[b].append(mb)
        print(f"{a + ' vs ' + b:<26} {r.win_rate:>7.3f} {r.draw_rate:>6.3f} "
              f"{(ma if ma is not None else float('nan')):>10,.0f} "
              f"{(mb if mb is not None else float('nan')):>10,.0f}")

    print(f"\n{'agent':<14} {'score':>7} {'games':>6}   (score = wins + half-draws, all pairs)")
    print("-" * 46)
    for n in sorted(names, key=lambda x: -(wins[x] / max(games[x], 1))):
        rate = wins[n] / max(games[n], 1)
        print(f"{n:<14} {rate:>7.3f} {games[n]:>6}")


if __name__ == "__main__":
    main()