"""Turn by turn: does our EMITTER waste the day, or is our SCHEDULE wrong?

Alex's diagnostic, and it is the right one. We believe the target numbers match the winner -- 8 cows,
6 sheep, land on days 7 and 10, ~12 hands. Feed those numbers into the emitter, then walk the season
turn by turn against his actual tape and see where it goes wrong. Two candidates, and they need
different fixes:

- **the schedule** is wrong: we own the right things but start them on the wrong days, so capacity
  arrives too late or unfunded.
- **the emitter** is wrong: we own the right things on the right days but `routines.py` spends the
  day badly -- walking instead of working.

The census separates them cleanly, because a turn is either productive or it is not. Every one of the
23 work turns in a day goes to exactly one of:

    productive   WATER HARVEST PLANT FEED CARE COLLECT_FERTILIZER FERTILIZE DIG BUILD_* PLACE
    logistics    PICKUP DROP            (necessary, but only to enable the above)
    movement     NORTH SOUTH EAST WEST  (pure overhead)
    wasted       PASS                   (a turn thrown away)

If our productive fraction is far below his, the emitter is the problem and no amount of rescheduling
helps. If the fractions match but the days differ, the schedule is the problem.

His side is read from a real replay, which carries every hand's op at every turn. Ours is the tape our
own routines emit, at his allocation, so the only difference is how each side spends its turns.
"""

import argparse
import collections
import json
import pathlib

import numpy as np

from kagg.search import chains as C
from kagg.search import routines as R

LEADER = "somewhere after"
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
LOGISTICS = {"PICKUP", "DROP"}
PRODUCTIVE = {"WATER", "HARVEST", "PLANT", "FEED", "CARE", "COLLECT_FERTILIZER",
              "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE", "PLACE"}

ap = argparse.ArgumentParser()
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--genome", default="data/chain_search_local/best_beam_genome.npz")
ap.add_argument("--slots", type=int, default=8)
args = ap.parse_args()


def classify(counter):
    prod = sum(v for k, v in counter.items() if k in PRODUCTIVE)
    move = sum(v for k, v in counter.items() if k in MOVES)
    logi = sum(v for k, v in counter.items() if k in LOGISTICS)
    pas = counter.get("PASS", 0)
    return prod, logi, move, pas


# ------------------------------------------------------------------ his season, off the tape
def leader_census(path):
    d = json.load(open(path))
    seat = d["info"]["TeamNames"].index(LEADER)
    per_day = collections.defaultdict(collections.Counter)
    hands_per_day = collections.defaultdict(int)
    for t, step in enumerate(d["steps"]):
        day = t // R.TURNS_PER_DAY
        a = (step[seat] or {}).get("action") or {}
        farmer = a.get("farmer") or []
        if farmer:
            per_day[day][farmer[0]] += 1
        hands = a.get("hands") or []
        hands_per_day[day] = max(hands_per_day[day], len(hands))
        for h in hands:
            if h:
                per_day[day][h[0]] += 1
    return per_day, hands_per_day


# ------------------------------------------------------------------ ours, off the emitter
def our_census(genome_path, n_slots):
    genome = np.asarray(np.load(genome_path)["genome"], dtype=np.int64)
    script, used, skipped = C.decode(genome, n_slots)
    ops = np.asarray(script.unit_op)
    per_day = collections.defaultdict(collections.Counter)
    hands_per_day = collections.defaultdict(int)
    hire = np.asarray(script.hire)
    for t in range(ops.shape[0]):
        day = t // R.TURNS_PER_DAY
        hands_per_day[day] = max(hands_per_day[day], int(hire[day * R.TURNS_PER_DAY])
                                 if day * R.TURNS_PER_DAY < len(hire) else 0)
        for u in range(ops.shape[1]):
            name = R.OP_NAMES[int(ops[t, u])]
            # Only count units that exist: a PASS on a unit we never hired is not a wasted turn, it is
            # a unit that is not there. Counting them would drown the census in phantom PASSes.
            if u <= hands_per_day[day]:
                per_day[day][name] += 1
    return per_day, hands_per_day, used, skipped


him, him_hands = leader_census(args.replay)
us, us_hands, used, skipped = our_census(args.genome, args.slots)

print("=" * 108)
print("WHERE THE TURNS GO.  productive / logistics / movement / PASS, per day")
print("=" * 108)
print(f"{'day':>4} | {'hands':>5} {'prod':>5} {'logi':>5} {'move':>5} {'PASS':>5} {'prod%':>6} "
      f"| {'hands':>5} {'prod':>5} {'logi':>5} {'move':>5} {'PASS':>5} {'prod%':>6}")
print(f"{'':>4} | {'---- OURS ----':^37} | {'---- HIS ----':^37}")

tot_us = collections.Counter()
tot_him = collections.Counter()
for day in range(R.SEASON_DAYS):
    up, ul, um, ux = classify(us[day])
    hp, hl, hm, hx = classify(him[day])
    tot_us.update(us[day])
    tot_him.update(him[day])
    u_active = up + ul + um
    h_active = hp + hl + hm
    print(f"{day:>4} | {us_hands[day]:>5} {up:>5} {ul:>5} {um:>5} {ux:>5} "
          f"{(up / max(u_active, 1)) * 100:>5.0f}% "
          f"| {him_hands[day]:>5} {hp:>5} {hl:>5} {hm:>5} {hx:>5} "
          f"{(hp / max(h_active, 1)) * 100:>5.0f}%")

print()
print("=" * 108)
print("SEASON TOTALS")
print("=" * 108)
for label, tot in (("OURS", tot_us), ("HIS", tot_him)):
    p, l, m, x = classify(tot)
    active = p + l + m
    print(f"{label:>5}: productive {p:>6}  logistics {l:>6}  movement {m:>6}  PASS {x:>6}   "
          f"productive share of worked turns {p / max(active, 1):>5.1%}")

print()
print(f"{'op':>20} {'OURS':>8} {'HIS':>8}   {'ratio':>7}")
for op in sorted(set(tot_us) | set(tot_him), key=lambda o: -(tot_him.get(o, 0) + tot_us.get(o, 0))):
    a, b = tot_us.get(op, 0), tot_him.get(op, 0)
    if not a and not b:
        continue
    print(f"{op:>20} {a:>8} {b:>8}   {(a / b) if b else float('inf'):>7.2f}")

print()
print("=" * 108)
print("READ IT LIKE THIS")
print("=" * 108)
print("  Our productive share far below his  -> the EMITTER wastes the day (routing/walking).")
print("  Shares similar, but our totals arrive later -> the SCHEDULE is wrong.")
print("  Our PASS count high on hired hands  -> we pay for hands we do not use, which is both.")
