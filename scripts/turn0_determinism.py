"""Is a team deterministic? The turn-0 observation decides it.

At step 0 nothing has happened: day 0, hour 0, no shop unlocked, identical board
(one tile hash across every seed), identical market and private state. The only
thing that differs between two seasons is the seat index. So within one seat, a
deterministic policy MUST emit the same turn-0 action every time.

A team holds TWO active submissions, each with its own opening, so up to two
distinct turn-0 actions per seat is still deterministic play. More than two is not.

  1-2 distinct turn-0 actions  deterministic -- tape, router or rule cascade
  3 or more                    stochastic -- sampled policy, or anytime search
                               under the wall-clock budget the observation carries
                               as remainingOverageTime
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08",
        "data/replays_2026-09-09", "data/replays_hayashi"]


def main():
    top = json.loads((ROOT/"data/logs/top30.json").read_text())
    rank = {n: i+1 for i, n in enumerate(top)}; rank["Yusuke Hayashi"] = 34

    per = defaultdict(lambda: defaultdict(list))
    seen = set()
    for d in DIRS:
        for p in sorted((ROOT/d/"summaries").glob("*.summary.json")):
            rec = json.loads(p.read_text())
            if rec["episode"] in seen: continue
            seen.add(rec["episode"])
            for seat, team in enumerate(rec["teams"]):
                per[team][seat].append(rec["actions"][seat][0])

    print(f"{'rk':>3} {'team':24} {'seat0 n/distinct':>17} {'seat1 n/distinct':>17}  verdict")
    for team in sorted(per, key=lambda t: rank.get(t, 999)):
        if team not in rank: continue
        cols, total, distinct = [], 0, 0
        for seat in (0, 1):
            a = per[team][seat]
            cols.append(f"{len(a):>7}/{len(set(a)):<9}" if a else f"{'-':>17}")
            total += len(a); distinct += len(set(a))
        worst = max((len(set(per[team][s])) for s in (0, 1) if per[team][s]), default=0)
        enough = max((len(per[team][s]) for s in (0, 1) if per[team][s]), default=0)
        if total < 2:
            verdict = "unknown (1 season)"
        elif worst > 2:
            verdict = "STOCHASTIC at turn 0"
        elif enough >= 5:
            verdict = "DETERMINISTIC at turn 0"
        else:
            verdict = f"deterministic so far ({enough} seasons)"
        print(f"{rank[team]:>3} {team[:24]:24} {cols[0]} {cols[1]}  {verdict}")


if __name__ == "__main__":
    main()
