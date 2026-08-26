"""The cheap arm: our shipped schedule with the clone's CROP MIX, and nothing else.

Alex, 2026-08-26: *"try the cheap one first and then when that doesnt work - cos it wont - try only
1 branch first - then go expensive"*.

The expensive path re-anchors the whole opening onto a clone tape, which needs `resolve_days.py`
re-run because `_apply_precomputed` keys a stop on `(tile, ops)` and a different opening gives a
different d12 board. This does none of that. It keeps our tape, our hiring, our pens, our routes,
and changes only the counts of what goes in the ground -- so if the composition IS the gap it should
show, and if it is not, we have paid nothing to find out.

**The base is `kawashigi`, which is what `kagg/plan.py:SHIPPED_PLAN` actually points at.** The first
cut of this script edited `kawa_straw` and would have measured a variant of a schedule we do not
ship -- the two differ by a lot (`melo12 carr8 whea119 stra42` against the shipped
`melo20 carr8 whea136 stra34`), and only the shipped one matches the 16.4 melon measured over 54
ladder games.

Season totals, ours against the clone (`data/logs/plant_days.log`, schedules side by side):

    crop         ship   clone
    WHEAT         136     134
    STRAWBERRY     34      38
    CARROT          8      20
    MELON          20      11

Two real differences: **melon -9 and carrot +12.** The edits below move only those, and move the
carrot to where they put it -- they plant it in two BLOCKS (8 on d11, 12 on d26); we dribble 2 a day
across d21/22/24/25. Plus the d24 wheat burst, 8 -> 18, which is the one big late planting they make
and we do not.

    day   ours              clone
    d0    melo12 whea7      melo7 whea5
    d6    melo2             stra5
    d7    melo6 stra3       stra8 whea5
    d11   stra16 whea8      carr8 melo4 stra8 whea4
    d21   carr2 whea3       whea8
    d24   carr2 whea8       whea18
    d26   whea9             carr12 whea9

**`seeds` is edited alongside `plants` and that is not cosmetic.** The row's `seeds` counter is what
drives BUY_SEED; leaving it alone would buy 12 melon seeds to plant 7 and refuse the carrot, which
measures the wrong thing entirely.

`hands` is deliberately NOT touched even though the clones open on 2 where we open on 5 and reach 15
where we reach 12. Hiring changes the turn budget of every day that follows and would confound the
crop question -- it is the next arm, not this one.

    python -u scripts/make_the_cheap_arm.py
"""

import collections
import json
import pathlib
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "data/seed_scripts/kawashigi"
DST = REPO / "data/seed_scripts/cheap_mix"

#: `day -> {crop: delta}`. Applied to `plants` and `seeds` together.
#: Melon 20 -> 11 (d0 7, d7 4, matching their d0 7 + d11 4).
#: Carrot 8 -> 20, moved out of the d21-d25 dribble and into their two blocks.
#: Wheat: -2 on d0 and +10 on d24, which is their burst; season stays ~136.
EDITS = {
    "0": {"MELON": -5, "WHEAT": -2},
    "6": {"MELON": -2},
    "7": {"MELON": -2},
    "11": {"CARROT": +8},
    "21": {"CARROT": -2},
    "22": {"CARROT": -2},
    "24": {"CARROT": -2, "WHEAT": +10},
    "25": {"CARROT": -2},
    "26": {"CARROT": +12},
    #: The d24 burst is +10 on top of a season already at 136, which lands wheat at 144 against
    #: their 134 -- an 8% difference in the one crop both sides agree on, and it would confound the
    #: carrot/melon question this arm exists to ask. Taken back off the three mid-season days where
    #: we out-plant them most: d18 10/7, d20 10/6, d23 10/4.
    "18": {"WHEAT": -3},
    "20": {"WHEAT": -4},
    "23": {"WHEAT": -3},
}


def apply(row, deltas):
    plants = collections.Counter(row.get("plants") or [])
    seeds = collections.Counter(row.get("seeds") or {})
    for crop, d in deltas.items():
        if d < 0:
            take = min(-d, plants[crop])
            plants[crop] -= take
            seeds[crop] = max(0, seeds.get(crop, 0) - take)
        else:
            plants[crop] += d
            seeds[crop] = seeds.get(crop, 0) + d
    row["plants"] = [c for c, n in sorted(plants.items()) for _ in range(max(0, n))]
    row["seeds"] = {c: n for c, n in seeds.items() if n > 0}
    return plants


def main():
    sched = json.loads((SRC / "schedule.json").read_text())
    before = collections.Counter()
    for r in sched.values():
        before.update(r.get("plants") or [])

    for day, deltas in EDITS.items():
        if day not in sched:
            print(f"day {day} not in schedule -- skipped", file=sys.stderr)
            continue
        was = collections.Counter(sched[day].get("plants") or [])
        now = apply(sched[day], deltas)
        print(f"   d{day:<3} " + " ".join(f"{c[:4].lower()}{was[c]}->{now[c]}" for c in deltas))

    after = collections.Counter()
    for r in sched.values():
        after.update(r.get("plants") or [])

    DST.mkdir(parents=True, exist_ok=True)
    (DST / "schedule.json").write_text(json.dumps(sched, indent=1))
    # The tape half is untouched -- this arm replays the same opening. Copied so the TAPES entry
    # can point at one directory and so nothing reads across into the source extraction by accident.
    for name in ("tape.json",):
        src = SRC / name
        if src.exists():
            shutil.copy2(src, DST / name)

    print()
    print(f"   {'crop':<12}{'was':>6}{'now':>6}{'clone':>8}")
    clone = {"WHEAT": 134, "STRAWBERRY": 38, "CARROT": 20, "MELON": 11}
    for c in sorted(set(before) | set(after) | set(clone)):
        print(f"   {c:<12}{before[c]:>6}{after[c]:>6}{clone.get(c, 0):>8}")
    print(f"\nwrote {DST/'schedule.json'}")


if __name__ == "__main__":
    main()
