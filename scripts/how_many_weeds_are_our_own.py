"""Weeds per day, ours against カワシギ -- the outcome test for the missed brink waters.

`data/logs/idle_offered3.log`: on d12-d23 of seed 11, **58** idle unit-turns had a reachable tile at
`consecutive_unwatered >= 1` that no other hand watered that day. A second dry night turns that tile
into a WEED (`reference/kaggriculture.py:771`), which is why `crop_ops` prices a brink water at
`_crop_remaining` -- the whole tile -- rather than at the one unit a water normally adds.

If those misses are real, they must show up as weeds. The op histogram already points that way:
DIG runs **39.4** per season for us against **23.8** for him (`data/logs/op_histogram.log`).

Counted here as a STOCK, at the last turn of each day:

    weeds     tiles whose `kind` is WEED
    brink     crop tiles sitting at `consecutive_unwatered >= 1` -- tonight's candidates
    crops     crop tiles, so the weed count can be read as a rate

**`weedSpawnChance` is 0.005 on the ladder, not 0.** So a small number of weeds are the town's and
not ours; a difference of 16 a season between two players on the same setting is not.
"""

import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
US = "alex chilton"
DIRS = ("downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "kawa_2026-08-24", "leaders_2026-08-24")


def per_day(replay, seat):
    out = {}
    steps = replay.get("steps") or []
    for t, step in enumerate(steps):
        if t % TPD != TPD - 1:
            continue
        obs = (step[0] or {}).get("observation") or {}
        farms = obs.get("farms") or []
        if seat >= len(farms):
            continue
        weeds = brink = crops = 0
        for row in (farms[seat].get("tiles") or []):
            for c in row:
                if not isinstance(c, dict):
                    continue
                if c.get("kind") == "WEED":
                    weeds += 1
                if c.get("crop"):
                    crops += 1
                    if int(c.get("consecutive_unwatered", 0) or 0) >= 1:
                        brink += 1
        out[t // TPD] = (weeds, brink, crops)
    return out


def collect(pairs):
    acc = collections.defaultdict(lambda: collections.defaultdict(list))
    n = 0
    for replay, seat in pairs:
        n += 1
        for day, (w, b, c) in per_day(replay, seat).items():
            acc[day]["weeds"].append(w)
            acc[day]["brink"].append(b)
            acc[day]["crops"].append(c)
    return acc, n


def main(our_files):
    kawa = []
    for d in DIRS:
        p = REPO / "data/seed_scripts" / d
        if not p.exists():
            continue
        for f in sorted(p.glob("*.json"))[:60]:
            try:
                r = json.loads(f.read_text())
            except Exception:                                             # noqa: BLE001
                continue
            names = (r.get("info") or {}).get("TeamNames") or []
            if KAWA in names:
                kawa.append((r, names.index(KAWA)))
    ours = []
    for path in our_files:
        f = pathlib.Path(path)
        if f.name.startswith("_"):
            continue
        r = json.loads(f.read_text())
        names = (r.get("info") or {}).get("TeamNames") or []
        ours.append((r, names.index(US) if US in names else 0))

    ka, kn = collect(kawa)
    oa, on = collect(ours)
    print(f"kawa {kn} seats   ours {on} seats\n")
    print(f"{'day':>5}{'weeds K':>10}{'weeds US':>10}{'brink K':>10}{'brink US':>10}"
          f"{'crops K':>10}{'crops US':>10}")
    for day in sorted(set(ka) | set(oa)):
        def m(a, k):
            v = a.get(day, {}).get(k) or [0]
            return sum(v) / len(v)
        print(f"{day:>5}{m(ka,'weeds'):>10.1f}{m(oa,'weeds'):>10.1f}"
              f"{m(ka,'brink'):>10.1f}{m(oa,'brink'):>10.1f}"
              f"{m(ka,'crops'):>10.1f}{m(oa,'crops'):>10.1f}")
    for lo, hi in ((12, 23), (24, 29)):
        def s(a, k):
            return sum((sum(a.get(d, {}).get(k) or [0]) / max(1, len(a.get(d, {}).get(k) or [1])))
                       for d in range(lo, hi + 1))
        print(f"\nd{lo}-d{hi} mean weed-days per seat: kawa {s(ka,'weeds'):.1f}   "
              f"ours {s(oa,'weeds'):.1f}      brink-days: kawa {s(ka,'brink'):.1f}   "
              f"ours {s(oa,'brink'):.1f}")


if __name__ == "__main__":
    main(sys.argv[1:])
