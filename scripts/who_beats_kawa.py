"""When カワシギ loses, what does the winner plant?

Alex, 2026-08-21: *"kawa is now at position 8 - and i strongly suspect those above him are probably
using them"* -- them being TOMATO and GOOSE.

`scripts/who_plays_tomato_or_geese.py` answered a different question and I reported it as this one.
It ranked 4,022 seats by BANK. The ladder is Elo, so a big bank in a downloaded game says nothing
about rank, and "best bank touching neither token" is not "the best players do not use them".

This asks the question that has a defensible label: **take only the games カワシギ actually lost, and
count what the player who beat him used.** The unit is a head-to-head result, not a bank, and the
opponent's rank is implied by the outcome rather than assumed from a number.

Two limits that stay, and neither is fixable from disk:

  The archive is SELECTED -- Alex downloads losses -- so this is a sample of his defeats, which is
  exactly the right population for this question and the wrong one for "how often does he lose".

  A player who beats him once may be below him on the ladder. Elo is not transitive over one game.

    python -u scripts/who_beats_kawa.py --out data/logs/who_beats_kawa.log
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

LEADER = "カワシギ"
TOKENS = ("TOMATO", "GOOSE", "CARROT", "EGG", "MELON", "STRAWBERRY", "WHEAT")


def game(path):
    """`(winner_name, winner_bank, loser_bank, winner_ops)` when the leader is in it and loses."""
    try:
        d = json.loads(path.read_text())
        names, steps = d["info"]["TeamNames"], d["steps"]
    except Exception:
        return None
    if not steps or LEADER not in names:
        return None
    seat = names.index(LEADER)
    other = 1 - seat
    last = steps[-1]
    farms = ((last[seat] if seat < len(last) else {}) or {}).get("observation", {}).get("farms") or []
    if len(farms) < 2:
        return None
    mine, theirs = farms[seat].get("money") or 0, farms[other].get("money") or 0
    if theirs <= mine:
        return None                                   # he won or drew; not this question
    ops = collections.Counter()
    for s in steps[1:]:
        a = ((s[other] if other < len(s) else None) or {}).get("action") or {}
        for x in [a.get("farmer")] + list(a.get("hands") or []):
            if x and len(x) > 1:
                ops[str(x[1])] += 1
        for m in (a.get("market") or []):
            if len(m) > 1:
                ops[str(m[1])] += 1
    return str(names[other]), theirs, mine, ops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/seed_scripts")
    ap.add_argument("--top", type=int, default=30)
    args = ap.parse_args()

    rows = []
    for p in sorted(pathlib.Path(args.root).rglob("*.json")):
        if p.name == "schedule.json":
            continue
        r = game(p)
        if r:
            rows.append(r + (p.parent.name + "/" + p.stem,))
    rows.sort(key=lambda r: -r[1])

    print("games where %s LOSES: %d\n" % (LEADER, len(rows)))
    print("%-22s %9s %9s %s  %s" % ("winner", "their $", "his $",
                                    "".join("%7s" % t for t in TOKENS), "game"))
    print("-" * 128)
    for name, theirs, mine, ops, g in rows[:args.top]:
        print("%-22s %9.0f %9.0f %s  %s"
              % (name[:22], theirs, mine, "".join("%7d" % ops[t] for t in TOKENS), g))

    print("\nwinners using each token at all, out of %d wins over him:" % len(rows))
    for t in TOKENS:
        n = sum(1 for _, _, _, ops, _ in rows if ops[t])
        heavy = sum(1 for _, _, _, ops, _ in rows if ops[t] >= 20)
        print("  %-12s %4d  (%4.1f%%)   heavy (>=20 ops): %3d" % (t, n, 100 * n / max(1, len(rows)), heavy))

    beat = collections.Counter(name for name, _, _, _, _ in rows)
    print("\nwho beats him most:")
    for name, n in beat.most_common(12):
        print("  %-24s %3d" % (name[:24], n))


if __name__ == "__main__":
    main()
