"""Classify the current top 30 as tape, router or adaptive from the daily replays.

Pools every summary we hold. For one team, two seasons in the SAME world are the
test: a tape or a router cannot vary inside a world, so any difference there is
reactivity. Between different worlds, a difference means routing, not adaptation.

    fixed tape   same actions in different worlds
    routing      identical within a world, different between worlds
    adaptive     differs within a world
    1 season     cannot be told apart; reported as unknown
"""
import json, statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-13", "data/replays_live", "data/replays_2026-09-07", "data/replays_2026-09-08",
        "data/replays_2026-09-09", "data/replays_2026-09-11", "data/replays_hayashi"]


def main():
    top = json.loads((ROOT/"data/logs/top30.json").read_text())
    rank = {n: i+1 for i, n in enumerate(top)}
    rank["Yusuke Hayashi"] = 34

    seasons = defaultdict(list)
    seen = set()
    for d in DIRS:
        for p in sorted((ROOT/d/"summaries").glob("*.summary.json")):
            rec = json.loads(p.read_text())
            if rec["episode"] in seen:
                continue
            seen.add(rec["episode"])
            for seat, team in enumerate(rec["teams"]):
                seasons[team].append({"episode": rec["episode"],
                                      "world": "|".join(rec["world"]),
                                      "bank": rec["rewards"][seat],
                                      "actions": rec["actions"][seat]})
    print(f"{len(seen)} episodes, {len(seasons)} distinct teams\n")

    def diff(a, b):
        return sum(1 for x, y in zip(a, b) if x != y)

    print(f"{'rk':>3} {'team':28} {'n':>3} {'worlds':>6} {'within-world':>20} "
          f"{'cross-world':>18}  verdict")
    rows = []
    for team in sorted(seasons, key=lambda t: rank.get(t, 999)):
        if team not in rank:
            continue
        g = seasons[team]
        byw = defaultdict(list)
        for s in g:
            byw[s["world"]].append(s)
        within = [diff(a["actions"], b["actions"])
                  for ss in byw.values() for i, a in enumerate(ss) for b in ss[i+1:]]
        cross = [diff(a["actions"], b["actions"])
                 for i, a in enumerate(g) for b in g[i+1:]
                 if a["world"] != b["world"]]
        if not within and not cross:
            verdict = "unknown (1 season)"
        elif within and max(within) == 0:
            verdict = "FIXED TAPE" if (cross and max(cross) == 0) else "ROUTER"
        elif within:
            verdict = "ADAPTIVE" if min(within) > 40 else f"tape+repair (min {min(within)})"
        else:
            verdict = "FIXED TAPE" if max(cross) == 0 else f"router or adaptive (cross {min(cross)}-{max(cross)})"
        wstr = (f"{min(within)}-{max(within)} ({len(within)})" if within else "-")
        cstr = (f"{min(cross)}-{max(cross)} ({len(cross)})" if cross else "-")
        print(f"{rank[team]:>3} {team[:28]:28} {len(g):>3} {len(byw):>6} {wstr:>20} "
              f"{cstr:>18}  {verdict}")
        rows.append(team)
    missing = [t for t in top if t not in rows]
    print(f"\n{len(rows)-1} of the top 30 appear in the replays we hold")
    if missing:
        print("no replay held for:", ", ".join(missing))


if __name__ == "__main__":
    main()
