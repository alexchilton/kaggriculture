"""How far into the season does the clone script stay the SAME across its own seats?

Alex, 2026-08-26: *"can the tape not play longer? the reason we had the solver start at d12 was the
kawa tapes diverged too much at d12 but maybe the newguy doesnt?"*

d12 is not a law. It is where カワシギ's recordings stopped agreeing with each other, so a replay
past it was replaying one game's accidents. If a different lineage stays coherent longer, its tape
can play longer -- and **a tape is exact where the solver is an approximation**, so every day the
tape can cover is a day we do not have to solve.

Measured within a branch, not across branches. Seats are grouped by their d0-d11 opening hash --
49 of them share `d1f515b59d`, 40 share `62d81623f9` -- and inside each group this asks, per day,
what fraction of turns every seat in the group plays identically.

    1.00 through dN   the script is deterministic to dN and a tape covers it exactly
    falls at dK       the seats start responding to something -- the opponent, the market, weeds --
                      and a tape past dK is copying one game's luck

**Seats in a group are from DIFFERENT games**, so they differ in opponent, shop draw and weed rolls.
That is the point: agreement across those is what makes a tape safe to replay. The start state is
fixed (`project_kaggriculture_start_state_is_fixed`), which is why the comparison is meaningful at
all.
"""

import collections
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
NEW = "data/seed_scripts/daily_2026-08-26"
OPEN_TO = 11
MIN_GROUP = 6


def streams(replay, seat):
    out = []
    for t, step in enumerate(replay.get("steps") or []):
        if seat >= len(step):
            out.append(None)
            continue
        act = (step[seat] or {}).get("action") or {}
        ops = [act.get("farmer")] + list(act.get("hands") or [])
        out.append(tuple(tuple(o) if o else None for o in ops))
    return out


def open_hash(s, last_day=OPEN_TO):
    parts = ["|".join("-".join(str(x) for x in o) if o else "." for o in turn)
             for turn in s[:(last_day + 1) * TPD] if turn is not None]
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()[:10]


def main():
    groups = collections.defaultdict(list)
    for f in sorted(pathlib.Path(NEW).glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            r = json.loads(f.read_text())
        except Exception:                                                 # noqa: BLE001
            continue
        names = (r.get("info") or {}).get("TeamNames") or []
        for seat in range(min(2, len(names))):
            s = streams(r, seat)
            if len(s) < 700:
                continue
            groups[open_hash(s)].append(s)

    big = [(h, v) for h, v in groups.items() if len(v) >= MIN_GROUP]
    big.sort(key=lambda hv: -len(hv[1]))
    print(f"{sum(len(v) for v in groups.values())} seats, "
          f"{len(big)} groups with >= {MIN_GROUP} seats\n")

    for h, seats in big:
        print(f"=== {h}   {len(seats)} seats")
        print("   day  identical   first day below 100%")
        first_break = None
        for day in range(30):
            vals = []
            for hour in range(TPD):
                t = day * TPD + hour
                turn = {tuple(s[t]) if s[t] else None for s in seats if t < len(s)}
                vals.append(len(turn) == 1)
            frac = sum(vals) / len(vals)
            if frac < 1.0 and first_break is None:
                first_break = day
            flag = "  <-- diverges here" if day == first_break else ""
            if day <= 20 or frac > 0.0:
                print(f"   {day:>3}   {100*frac:>6.0f}%{flag}")
        print(f"   -> a tape is EXACT through d{(first_break or 30) - 1}\n")


if __name__ == "__main__":
    main()
