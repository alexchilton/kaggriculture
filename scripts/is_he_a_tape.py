"""Is this player replaying a fixed script, or adapting to the board?

The start state is identical in every game -- same board, NW quadrant only, $3,000, no shops
(`project_kaggriculture_start_state_is_fixed`). So a pure open-loop tape emits the SAME actions on
day 0 in every game it plays. The first day on which its actions differ across games is the first
day it reads anything.

This is the same question `project_kaggriculture_leader_replans_on_shops` answered for カワシギ: a
fixed 74-turn opening ending exactly at the d3 first shop unlock, then adaptation all season.

Method: for each day, hash the player's full action list for that day in each game. Count distinct
hashes. `1` means every game played that day identically -- scripted. More than 1 means the day
depends on something.

Caveat, stated because it changes the reading: a day can differ because the agent adapted, OR
because an earlier failed purchase left it with a different bank. So the first day with more than
one hash is an UPPER bound on how long the script runs, not proof of deliberate adaptation. Read it
with the shop-unlock day alongside.
"""

import argparse
import collections
import glob
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24


def _day_hash(steps, seat, day):
    """Hash of every action this seat submitted on `day`."""
    h = hashlib.sha1()
    for t in range(day * TPD, min((day + 1) * TPD, len(steps) - 1)):
        a = steps[t + 1][seat].get("action")
        h.update(json.dumps(a, sort_keys=True, default=str).encode())
    return h.hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", default="/Users/alexchilton/Downloads/*.json")
    ap.add_argument("--who", default="SOUTA Sakurai")
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    per_day = collections.defaultdict(list)
    shop_days = []
    n = 0
    for f in sorted(glob.glob(a.glob)):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        steps = rec["steps"]
        n += 1
        for d in range(a.days):
            if (d + 1) * TPD >= len(steps):
                break
            per_day[d].append(_day_hash(steps, seat, d))
        # first day any shop is unlocked
        for d in range(a.days):
            t = d * TPD
            if t >= len(steps):
                break
            if ((steps[t][seat]["observation"].get("town") or {}).get("unlocked_shops") or []):
                shop_days.append(d)
                break

    if not n:
        print(f"no games for {a.who}")
        return

    print(f"{a.who}: {n} games.\n")
    print("PREFIX CLUSTERS: distinct action-sequences over days 0..d.")
    print("A player who is k fixed tapes plateaus at k and stays there. A player who reads the")
    print("board keeps splitting. Per-day variant counts CANNOT tell these apart -- once two games")
    print("hold different banks, every later day differs mechanically whether or not anything was")
    print("read. カワシギ is 4 tapes and his per-day counts fan out all the same")
    print("(`project_kaggriculture_only_two_bits_vary`).\n")
    print(f"{'thru day':>9} {'clusters':>9} {'block sizes':>28}")
    prefixes = collections.defaultdict(str)
    order = list(range(len(per_day[0])))
    for d in sorted(per_day):
        for g in order:
            if g < len(per_day[d]):
                prefixes[g] += per_day[d][g]
        c = collections.Counter(prefixes[g] for g in order)
        sizes = " ".join(str(v) for _k, v in c.most_common(8))
        print(f"{d:>9} {len(c):>9} {sizes:>28}")
    if shop_days:
        print(f"first shop unlock: d{min(shop_days)}-d{max(shop_days)} "
              f"(median d{sorted(shop_days)[len(shop_days)//2]})")


if __name__ == "__main__":
    main()
