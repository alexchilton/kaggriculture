"""What does "somewhere after" -- the new leader -- actually do?

Four fresh replays, and he wins all four by **2 to 4 percent** on banks of $120k-160k. Everyone at the
top is within a few thousand dollars of everyone else, which is the shape an Elo ladder rewards: a
$2,634 win scores exactly what a $50,000 win scores. So the question is not "how does he score big",
it is "what does he do slightly better than four other very strong players".

Read straight off the tape rather than from any summary, because every wrong conclusion this project
has produced came from trusting a derived number:

  * land -- how many parcels, on which days (our own search hardcoded day 0 and it cost dearly);
  * herd -- how many of each animal, and when;
  * crops -- the planting mix by tile count, against our melon monoculture;
  * fertilizer -- collected, applied, bought, sold: the loop we have only just made expressible;
  * sell cadence -- daily like ours, or spaced against the price curve;
  * crew -- hands hired per day, since the previous leader held 2-3 for 25 days then jumped.
"""

import collections
import glob
import json
import os

import numpy as np

LEADER = "somewhere after"
FILES = sorted(glob.glob(os.path.expanduser("~/Downloads/new/*.json")))
TURNS_PER_DAY = 24


def leader_seat(d):
    teams = d["info"]["TeamNames"]
    return teams.index(LEADER) if LEADER in teams else None


def actions_of(d, seat):
    """Per-turn submitted action for `seat`, as the env recorded it."""
    out = []
    for step in d["steps"]:
        entry = step[seat] if seat < len(step) else None
        out.append((entry or {}).get("action") or {})
    return out


def summarise(path):
    d = json.load(open(path))
    seat = leader_seat(d)
    if seat is None:
        return None
    acts = actions_of(d, seat)
    rewards = d["rewards"]
    them = rewards[1 - seat]
    mine = rewards[seat]

    land_days, hire_by_day = [], collections.Counter()
    animals_offered, seeds_offered, sells_offered, buys = collections.Counter(), collections.Counter(), \
        collections.Counter(), collections.Counter()
    sell_turns = collections.defaultdict(list)
    ops = collections.Counter()
    for t, a in enumerate(acts):
        day = t // TURNS_PER_DAY
        for order in (a.get("market") or []):
            kind = order[0] if order else None
            if kind == "BUY_LAND":
                land_days.append(day)
            elif kind == "HIRE":
                hire_by_day[day] += 1
            elif kind == "BUY_ANIMAL":
                animals_offered[order[1]] += int(order[2]) if len(order) > 2 else 1
            elif kind == "BUY_SEED":
                seeds_offered[order[1]] += int(order[2]) if len(order) > 2 else 1
            elif kind == "SELL":
                sells_offered[order[1]] += int(order[2]) if len(order) > 2 else 1
                sell_turns[order[1]].append(day)
            elif kind == "BUY_PRODUCT":
                buys[order[1]] += int(order[2]) if len(order) > 2 else 1
        for who in ("farmer",):
            op = a.get(who)
            if op:
                ops[op[0]] += 1
        for op in (a.get("hands") or []):
            if op:
                ops[op[0]] += 1
    return dict(path=os.path.basename(path), seat=seat, mine=mine, them=them,
                opponent=d["info"]["TeamNames"][1 - seat], land_days=sorted(set(land_days)),
                hire_by_day=hire_by_day, animals=animals, seeds=seeds, sells=sells,
                buys=buys, sell_turns=sell_turns, ops=ops)


rows = [r for r in (summarise(p) for p in FILES) if r]
print(f"{len(rows)} replays with `{LEADER}` in them\n")
print("=" * 96)
print("RESULTS -- the margins are the headline")
print("=" * 96)
print(f"{'episode':>16} {'seat':>5} {'opponent':>18} {'his bank':>11} {'theirs':>11} "
      f"{'margin':>10} {'%':>7}")
for r in rows:
    print(f"{r['path'][:-5]:>16} {r['seat']:>5} {r['opponent'][:18]:>18} {r['mine']:>11,.0f} "
          f"{r['them']:>11,.0f} {r['mine'] - r['them']:>+10,.0f} "
          f"{(r['mine'] - r['them']) / r['them']:>+7.1%}")
print(f"\nwins {sum(1 for r in rows if r['mine'] > r['them'])}/{len(rows)}   "
      f"mean bank ${np.mean([r['mine'] for r in rows]):,.0f}   "
      f"mean margin {np.mean([(r['mine']-r['them'])/r['them'] for r in rows]):+.1%}")

print()
print("=" * 96)
print("LAND -- ours was hardcoded to day 0; the previous leader bought on days 7 and 10")
print("=" * 96)
for r in rows:
    print(f"  {r['path'][:-5]}: {len(r['land_days'])} parcel-days {r['land_days']}")

print()
print("=" * 96)
print("HERD -- we field 4 cows and no sheep; the previous leader ran 8 cows + 6 sheep")
print("=" * 96)
for r in rows:
    print(f"  {r['path'][:-5]}: {dict(r['animals_offered'])}")

print()
print("=" * 96)
print("CROPS -- BUY_SEED units OFFERED. NOT tiles planted: a re-posted order is counted\n      once per turn it stood, and on our own games it runs up to 20x the tiles that\n      changed. Use kagg.analysis.replay_fills.real_plants for the plant count.")
print("=" * 96)
for r in rows:
    tot = sum(r["seeds"].values()) or 1
    mix = ", ".join(f"{k} {v} ({v/tot:.0%})"
                    for k, v in sorted(r["seeds"].items(), key=lambda kv: -kv[1]))
    print(f"  {r['path'][:-5]}: {mix}")

print()
print("=" * 96)
print("FERTILIZER -- the loop we only just made expressible. Bought? Sold? Applied?")
print("=" * 96)
for r in rows:
    print(f"  {r['path'][:-5]}: collected {r['ops'].get('COLLECT_FERTILIZER', 0):>4}  "
          f"applied {r['ops'].get('FERTILIZE', 0):>4}  "
          f"bought {r['buys'].get('FERTILIZER', 0):>4}  sold {r['sells_offered'].get('FERTILIZER', 0):>4}")

print()
print("=" * 96)
print("SELL CADENCE -- ours is hardcoded daily, which walks our own price down the glut curve")
print("=" * 96)
for r in rows:
    parts = []
    for prod, days in sorted(r["sell_turns"].items(), key=lambda kv: -len(kv[1])):
        uniq = sorted(set(days))
        gaps = np.diff(uniq) if len(uniq) > 1 else np.array([0])
        parts.append(f"{prod}: {len(uniq)} days, mean gap {gaps.mean():.1f}")
    print(f"  {r['path'][:-5]}: " + " | ".join(parts[:5]))

print()
print("=" * 96)
print("CREW -- hands hired per day. The previous leader held 2-3 for 25 days, then jumped.")
print("=" * 96)
for r in rows:
    per_day = [r["hire_by_day"].get(d, 0) for d in range(30)]
    print(f"  {r['path'][:-5]}: {per_day}")

print()
print("=" * 96)
print("OP CENSUS -- what his units spend turns on")
print("=" * 96)
agg = collections.Counter()
for r in rows:
    agg.update(r["ops"])
tot = sum(agg.values()) or 1
for op, n in agg.most_common(18):
    print(f"  {op:>20} {n:>7,} {n/tot:>7.1%}")
