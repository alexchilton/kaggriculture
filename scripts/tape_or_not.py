"""Fixed tape or not, tested on the ONE comparison that discriminates: the same board twice.

`scripts/classify_top30.py` groups seasons by the town's first shop and calls a within-group
difference "adaptive". Two seasons sharing a first shop do NOT share a board -- the seed differs, so
the tiles, the weeds and the shop draw all differ, and a perfectly deterministic policy is obliged
to act differently. That test cannot separate a tape from an adaptive agent, and its verdicts should
not be read as if it could.

The seed fixes the board. So:

    same seed, same seat, different opponent  ->  identical actions  =  the agent ignores the game
    same seed, same seat, different opponent  ->  differing actions  =  it is reading something

Prints every seed a team played more than once, and how many of the 719 turns differ.

    python -u scripts/tape_or_not.py
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = ["data/replays_2026-09-13", "data/replays_live", "data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]


def main():
    top = json.loads((ROOT / "data/logs/top30.json").read_text())
    rank = {n: i + 1 for i, n in enumerate(top)}
    # team -> (seed, seat) -> [(episode, actions)]
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    seen, n = set(), 0
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            rec = json.loads(p.read_text())
            if rec["episode"] in seen or rec.get("seed") is None:
                continue
            seen.add(rec["episode"])
            n += 1
            for seat, team in enumerate(rec["teams"]):
                if seat < len(rec["actions"]):
                    by[team][(rec["seed"], seat)].append((rec["episode"], rec["actions"][seat]))
    print(f"{n} episodes with a seed, {len(by)} teams\n")
    # **No seed is ever repeated.** Measured 2026-09-12 over 414 episodes: every one is a distinct
    # board, so the same-board test below can never fire on this data. What still discriminates is
    # the OPENING: a fixed tape plays the same turns whatever board it is handed, so its streams
    # agree for a long prefix across different seeds. An agent reading the board diverges at the
    # first turn the board matters.
    print(f"{'rk':>3} {'team':26} {'n':>3} {'pairs':>6} {'common prefix turns':>20} "
          f"{'turn-0 variants':>15}")
    for team in sorted(by, key=lambda t: rank.get(t, 999)):
        if team not in rank:
            continue
        runs = [a for v in by[team].values() for _e, a in v]
        if len(runs) < 2:
            continue
        pref = []
        for i, a in enumerate(runs):
            for b in runs[i + 1:]:
                k = 0
                for x, y in zip(a, b):
                    if x != y:
                        break
                    k += 1
                pref.append(k)
        t0 = len({a[0] for a in runs if a})
        print(f"{rank[team]:>3} {team[:26]:26} {len(runs):>3} {len(pref):>6} "
              f"{min(pref)}-{max(pref):<14} {t0:>15}")
    print()
    print(f"{'rk':>3} {'team':26} {'repeat boards':>13} {'turns differing (min-max)':>26}  verdict")
    for team in sorted(by, key=lambda t: rank.get(t, 999)):
        if team not in rank:
            continue
        diffs = []
        for _k, v in by[team].items():
            for i, (_e1, a) in enumerate(v):
                for _e2, b in v[i + 1:]:
                    diffs.append(sum(1 for x, y in zip(a, b) if x != y))
        if not diffs:
            verdict, ds = "no repeated board -- cannot tell", "-"
        elif max(diffs) == 0:
            verdict, ds = "FIXED TAPE (identical on every repeat)", "0"
        else:
            verdict = ("reads the game" if min(diffs) > 40
                       else f"tape + repair (min {min(diffs)})")
            ds = f"{min(diffs)}-{max(diffs)}"
        print(f"{rank[team]:>3} {team[:26]:26} {len(diffs):>13} {ds:>26}  {verdict}")


if __name__ == "__main__":
    main()
