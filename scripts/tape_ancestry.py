"""Are the top agents built on the public tape, or independent of it?

Every published tape and every recovered Hayashi tape is identical on turns 0..143
-- the route branch is at step 144. So the opening is a fingerprint of ancestry:
a fork of the public notebook replays it verbatim until it decides to do otherwise.

Reported per team: first turn at which its stream leaves the published opening, and
how much of turns 0..143 and 144..718 it shares with the nearest published tape.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08",
        "data/replays_2026-09-09", "data/replays_hayashi"]


def main():
    pub = [[json.dumps(a, sort_keys=True) for a in t]
           for t in json.loads((ROOT/"submission"/"twocoins"/"actions.json").read_text())]
    hay = [[json.dumps(a, sort_keys=True) for a in json.loads(p.read_text())]
           for p in sorted((ROOT/"submission"/"hay_library").glob("tape_*.json"))]
    top = json.loads((ROOT/"data/logs/top30.json").read_text())
    rank = {n: i+1 for i, n in enumerate(top)}; rank["Yusuke Hayashi"] = 34

    seasons, seen = defaultdict(list), set()
    for d in DIRS:
        for p in sorted((ROOT/d/"summaries").glob("*.summary.json")):
            rec = json.loads(p.read_text())
            if rec["episode"] in seen: continue
            seen.add(rec["episode"])
            for seat, team in enumerate(rec["teams"]):
                seasons[team].append(rec["actions"][seat])

    def first_div(a, b):
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y: return i
        return len(a)
    def share(a, b, lo, hi):
        return sum(1 for x, y in zip(a[lo:hi], b[lo:hi]) if x == y)

    print(f"{'rk':>3} {'team':28} {'n':>3} {'first divergence':>17} "
          f"{'open 0-143 shared':>18} {'rest 144-718':>13}")
    for team in sorted(seasons, key=lambda t: rank.get(t, 999)):
        if team not in rank: continue
        g = seasons[team]
        divs, opens, rests = [], [], []
        for s in g:
            best = max(pub + hay, key=lambda t: share(s, t, 0, 719))
            divs.append(first_div(s, best))
            opens.append(share(s, best, 0, 144))
            rests.append(share(s, best, 144, 719))
        print(f"{rank[team]:>3} {team[:28]:28} {len(g):>3} "
              f"{min(divs):>7}-{max(divs):<9} "
              f"{min(opens):>8}-{max(opens):<3}/144 "
              f"{min(rests):>5}-{max(rests):<3}/575")


if __name__ == "__main__":
    main()
