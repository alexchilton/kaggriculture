"""Cluster the field by its opening. Players who share one are running the same code.

Alex, 2026-08-21: *"i suspect the ones reacting at d3 are kawa clones"*.

It matters well beyond curiosity. If ten of the eighteen opponents in a pool are the same agent, the
pool's effective sample size is not eighteen, every aggregate is weighted toward one strategy, and
an arm that happens to beat that strategy looks general when it is not. This is the unstable-label
failure from `CLAUDE.md`, one level up: the rows are right and the POPULATION is wrong.

The opening is the right fingerprint. Turns 0-71 run before any shop unlocks, both boards start
identical every game (`project_kaggriculture_start_state_is_fixed`), and weeds need two unwatered
days -- so two players who emit the same 72 turns are running the same code, not converging on it.

Each player is represented by their MODAL opening across their games, not their first one: a player
who resubmits gets several openings over weeks, and picking one arbitrarily assigns them to a
cluster by accident of ordering. The share of their games carrying that modal opening is printed,
because a low share means the player changed agent mid-archive and the label is unreliable.

    python -u scripts/who_is_a_clone_of_whom.py
    python -u scripts/who_is_a_clone_of_whom.py --turns 24 --min-games 4
"""

import argparse
import collections
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

CACHE = REPO / "data/action_cache.jsonl"
LB = REPO / "data/leaderboard_2026-08-21.json"

#: Turns 0-71 -- the whole of d0, d1 and d2, ending one turn before the first shop unlocks at d3 h0.
OPENING_TURNS = 72


def fingerprint(actions, turns):
    """A stable hash of the first `turns` unit actions. Market orders are excluded deliberately --
    they carry quantities that a thin bank can truncate, so two runs of one agent can differ there
    while the unit plan is identical."""
    h = hashlib.sha1()
    for f, hands, _ in actions[:turns]:
        h.update(json.dumps([f, hands], sort_keys=True).encode())
    return h.hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=int, default=OPENING_TURNS)
    ap.add_argument("--min-games", type=int, default=3)
    args = ap.parse_args()

    if not CACHE.exists():
        raise SystemExit("no %s -- run: python -u scripts/build_action_cache.py" % CACHE)
    lb = json.loads(LB.read_text()) if LB.exists() else {}

    per_player = collections.defaultdict(collections.Counter)
    with open(CACHE) as fh:
        for line in fh:
            d = json.loads(line)
            for seat, nm in enumerate(d["names"]):
                per_player[nm][fingerprint(d["actions"][seat], args.turns)] += 1

    modal = {}
    for nm, c in per_player.items():
        n = sum(c.values())
        if n < args.min_games:
            continue
        fp, k = c.most_common(1)[0]
        modal[nm] = (fp, k, n)

    clusters = collections.defaultdict(list)
    for nm, (fp, k, n) in modal.items():
        clusters[fp].append((nm, k, n))

    print("%d players with >=%d games, %d distinct openings over turns 0-%d\n"
          % (len(modal), args.min_games, len(clusters), args.turns - 1))

    ranked = sorted(clusters.items(), key=lambda kv: -len(kv[1]))
    for fp, members in ranked:
        if len(members) < 2:
            continue
        members.sort(key=lambda m: lb.get(m[0], (99999, 0))[0])
        best = lb.get(members[0][0])
        print("=== opening %s -- %d players, best rank %s ==="
              % (fp, len(members), best[0] if best else "-"))
        for nm, k, n in members:
            e = lb.get(nm)
            print("    %-28s rank %5s  %7s   modal opening in %d/%d games"
                  % (nm[:28], e[0] if e else "-", ("%.1f" % e[1]) if e else "-", k, n))
        print()

    singles = [m[0] for fp, ms in ranked if len(ms) == 1 for m in ms]
    print("=== unique openings (%d players) ===" % len(singles))
    singles.sort(key=lambda nm: lb.get(nm, (99999, 0))[0])
    for nm in singles[:25]:
        e = lb.get(nm)
        print("    %-28s rank %5s  %7s" % (nm[:28], e[0] if e else "-",
                                           ("%.1f" % e[1]) if e else "-"))

    big = sum(len(ms) for fp, ms in ranked if len(ms) >= 2)
    print("\n%d of %d players share an opening with someone else (%.0f%%)."
          % (big, len(modal), 100.0 * big / max(1, len(modal))))
    print("An opponent pool that samples players uniformly over-weights whichever agent has")
    print("the most clones; sample over OPENINGS instead.")


if __name__ == "__main__":
    main()
