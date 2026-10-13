"""Where does a team's play first leave its own previous season?

The starting board is identical for every seed (verified: one tile hash across six
seeds, $3,000, NW only, no shops). So the only thing that can make two seasons
differ is the shop unlock schedule and the shared market the opponent moves.

Splitting the turn into its two ledgers separates those causes:
  field   farmer + hands. Diverges when the agent's OWN plan reacts to something.
  market  orders. Diverges as soon as shared prices differ, so it says little.

A rule cascade latched on the shop draw keeps an identical field plan until the
latch fires. A policy reading the whole state diverges in the field almost at once.
"""
import json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08",
        "data/replays_2026-09-09", "data/replays_hayashi"]


def split(a):
    o = json.loads(a)
    return (json.dumps([o.get("farmer"), o.get("hands")], sort_keys=True),
            json.dumps(o.get("market"), sort_keys=True))


def first(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y: return i
    return len(a)


def main():
    top = json.loads((ROOT/"data/logs/top30.json").read_text())
    rank = {n: i+1 for i, n in enumerate(top)}; rank["Yusuke Hayashi"] = 34

    seasons, seen = defaultdict(list), set()
    for d in DIRS:
        for p in sorted((ROOT/d/"summaries").glob("*.summary.json")):
            rec = json.loads(p.read_text())
            if rec["episode"] in seen: continue
            seen.add(rec["episode"])
            for seat, team in enumerate(rec["teams"]):
                f, m = zip(*(split(a) for a in rec["actions"][seat]))
                seasons[team].append({"field": list(f), "market": list(m),
                                      "world": "|".join(rec["world"])})

    print(f"{'rk':>3} {'team':24} {'pairs':>5} "
          f"{'field first div':>24} {'market first div':>18}")
    print(f"{'':>3} {'':24} {'':>5} {'min  p50  max':>24} {'min  p50':>18}")
    for team in sorted(seasons, key=lambda t: rank.get(t, 999)):
        if team not in rank: continue
        g = seasons[team]
        if len(g) < 2: continue
        fd, md = [], []
        for i, a in enumerate(g):
            for b in g[i+1:]:
                fd.append(first(a["field"], b["field"]))
                md.append(first(a["market"], b["market"]))
        fd.sort(); md.sort()
        print(f"{rank[team]:>3} {team[:24]:24} {len(fd):>5} "
              f"{fd[0]:>6} {fd[len(fd)//2]:>5} {fd[-1]:>5}  (day {fd[len(fd)//2]//24}) "
              f"{md[0]:>8} {md[len(md)//2]:>5}")


if __name__ == "__main__":
    main()
