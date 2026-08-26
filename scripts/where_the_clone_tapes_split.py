"""Where do the clone tapes stop agreeing, and what could a selector key on at that turn?

Alex, 2026-08-26: *"so to confirm this is still 3 different tapes split somewhere?"* -- and the
answer was no, because the split was never built. This is the measurement it has to be built on.

A tape split is only implementable if two things line up:

    the SPLIT turn      the first turn at which the tapes' actions differ. Before it, one tape
                        serves all arms and no selector is needed at all.
    the SIGNAL turn     the first turn at which the observation can tell the arms apart. Shops
                        unlock on a fixed 3-day cadence from d3 and the DRAW varies, so a
                        selector keyed on the shop list learns nothing before the unlock that
                        distinguishes them.

**If the split turn comes BEFORE the signal turn, the split cannot be made.** The tapes would have
diverged on information we do not have yet, and any selector would be guessing. That is the same
failure the existing `(melon_armed, q4_armed)` latch documents at d3: replaying a branch day before
its latch decides measured mean -$96,897 over 14 games (`schedule_agent.py:3826`).

So this prints, per pair of tapes, the first differing turn, and per tape the shop unlock schedule.
Actions are compared as submitted -- farmer op, hand ops, market orders -- from each tape's own
seat.
"""

import argparse
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
TAPES = {
    "clone_open": ("data/seed_scripts/clone_open/98907591.json", "UjjwalPardeshi"),
    "clone_late": ("data/seed_scripts/clone_late/98898511.json", "G!vIOne"),
    "clone_yarn3": ("data/seed_scripts/clone_yarn3/98889302.json", "WeAreFarmers"),
    "clone_yarn6": ("data/seed_scripts/clone_yarn6/98857364.json", "Bharath Varma"),
}


def load(path, team):
    """`(actions, shops)` -- per-turn action tuple and per-turn unlocked-shop tuple, that seat's."""
    rep = json.loads((REPO / path).read_text())
    seat = rep["info"]["TeamNames"].index(team)
    acts, shops = [], []
    # **`steps[1:]`, matching `build_planner_submission._opening`.** Step 0 is the initial state and
    # carries no action, so indexing `steps[t]` shifts every turn label by one: this script first
    # reported the `clone_open`/`clone_yarn3` split at d3h17 and the builder found it at d3h16, the
    # same turn under two conventions. The builder's is the one the shipped replay was verified on.
    for step in (rep.get("steps") or [])[1:]:
        s = step[seat] if seat < len(step) else {}
        a = (s.get("action") or {})
        acts.append(json.dumps([a.get("farmer") or ["PASS"],
                                list(a.get("hands") or []),
                                list(a.get("market") or [])], sort_keys=True))
        town = ((step[0] or {}).get("observation") or {}).get("town") or {}
        shops.append(tuple(sorted(town.get("unlocked_shops") or [])))
    return acts, shops


def turn(t):
    return f"d{t // TPD}h{t % TPD:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", default="clone_open,clone_yarn3,clone_yarn6,clone_late")
    args = ap.parse_args()

    names = [n for n in args.tapes.split(",") if n in TAPES]
    data = {n: load(*TAPES[n]) for n in names}

    print("shop unlocks, by the turn the list first grows\n")
    signal = {}
    for n in names:
        _acts, shops = data[n]
        prev = ()
        line = []
        for t, s in enumerate(shops):
            if s != prev:
                new = [x for x in s if x not in prev]
                line.append(f"{turn(t)} +{','.join(new) if new else '?'}")
                prev = s
        signal[n] = shops
        print(f"  {n:<13}{'  '.join(line[:8])}")

    print("\nfirst turn the ACTIONS differ, and first turn the SHOP LIST differs\n")
    print(f"  {'pair':<28}{'actions split':>15}{'shops differ':>15}{'buildable':>12}")
    for a, b in itertools.combinations(names, 2):
        aa, _ = data[a]
        bb, _ = data[b]
        n = min(len(aa), len(bb))
        split = next((t for t in range(n) if aa[t] != bb[t]), None)
        sa, sb = signal[a], signal[b]
        m = min(len(sa), len(sb))
        sig = next((t for t in range(m) if sa[t] != sb[t]), None)
        ok = "-" if split is None or sig is None else ("YES" if sig <= split else "NO (blind)")
        print(f"  {a + ' vs ' + b:<28}"
              f"{(turn(split) if split is not None else 'never'):>15}"
              f"{(turn(sig) if sig is not None else 'never'):>15}{ok:>12}")


if __name__ == "__main__":
    main()
