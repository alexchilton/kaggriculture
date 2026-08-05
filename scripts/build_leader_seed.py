"""Build a search seed at the leader's SCALE, because `seeded_genome` seeds the smallest of everything.

Measured 2026-08-05. `seeded_genome(16)` decodes to **10 chains of 2 tiles each and a single pen** --
20 crop tiles and one animal, against his 14 pens and ~61 tiles. The block library is not the problem:
it holds 63 eight-tile blocks and 25 four-pen groups. The seed simply never picks them, so a
single-gene local search starts from a farm one twelfth of his and has to climb there one gene at a
time, which it never does inside its sweep budget.

That mattered less when every chain cost a hand: 16 chains meant 16 hands and $77,490 of crew a season,
so a big farm was genuinely unaffordable and the small seed was accidentally near the optimum. With the
emission-time packer in `chains.decode` a hand now carries several jobs -- 9 chains on 4 hands, $210 a
season -- so scale is affordable for the first time and the seed is what caps us.

This builds the seed greedily: animals first (they are the working capital -- fertilizer sells from day
1, seven days before milk), then the largest crop blocks that do not overlap ground already taken. It
writes a genome, decodes it, and prints the farm it actually produces so the seed can be checked against
his numbers before any search time is spent on it.
"""

import argparse
import sys

import numpy as np

sys.path.insert(0, ".")

from kagg.search import chains as C
from kagg.search import routines as R

ap = argparse.ArgumentParser()
ap.add_argument("--slots", type=int, default=16)
ap.add_argument("--out", default="data/chain_search_local/leader_seed.npz")
ap.add_argument("--pens", type=int, default=14, help="his measured herd: 8 cow + 6 sheep")
ap.add_argument("--land-days", default="7,10", help="his tape buys NE on 7 and SW on 10")
args = ap.parse_args()

N = len(C.GENES)
GI = {name: i for i, name in enumerate(C.GENES)}
KIND_GROW = C.KINDS.index("grow")
KIND_RANCH = C.KINDS.index("ranch")
KIND_OFF = C.KINDS.index("off")
LAND_NEVER = C.LAND_DAY_CHOICES.index(99)
LAND_DAYS = [int(x) for x in args.land_days.split(",")]


def parcels_at(day):
    """How many parcels the farm owns on `day`, given the land schedule this seed will write."""
    return sum(1 for d in LAND_DAYS if d <= day)


def ground_ok(tiles, day):
    """Every tile buyable by `day`. A chain on locked ground does not fail -- the walk stops at the
    border and a whole season of work lands on the wrong tile."""
    return all(R.land_purchases_for(tuple(t)) <= parcels_at(day) for t in tiles)


def slot(kind, what, block, start_day, land_day, fertilize=0, fert_trade=0, feed_loop=0):
    row = np.zeros(N, np.int64)
    row[GI["kind"]] = kind
    row[GI["what"]] = what
    row[GI["block"]] = block
    row[GI["start_day"]] = C.START_DAY_CHOICES.index(start_day)
    row[GI["land_day"]] = land_day
    row[GI["fertilize"]] = fertilize
    row[GI["fert_trade"]] = fert_trade
    row[GI["feed_loop"]] = feed_loop
    return row


rows, taken = [], set()

# **Crop blocks are placed FIRST, and that ordering is the whole point of this file.**
# An 8-tile block uses 22 of the 23 work turns on its own (measured), so a hand holds *either* one big
# block or a pen group -- never both, whatever the packer does. His 12 hands are therefore about 8
# blocks (~64 tiles) plus 4 pen groups (14 pens), which is exactly his measured farm.
#
# The consequence is geometric: a big block needs eight *contiguous* tiles, and a pen group needs only
# one to four. Placing the pens first scatters four-tile clumps across NW and leaves no strip long
# enough for a block -- measured, that lost 6 of 12 chains and the seed decoded to 15 pens and **8 crop
# tiles**. Blocks first, pens into the gaps, costs the pens nothing because they fit anywhere.
#
# Melon is capped near its 140-unit town drain -- it is the one product that actually gluts (+100
# inventory, 250 -> 150) -- so the bulk is strawberry, matching his 44 plantings against 21 melon.
# **NW is reserved for the herd, and that is the load-bearing decision.**
# NW is the only quadrant unlocked on day 0, and the herd is the only thing that must start on day 0 --
# it is the working capital, selling fertilizer from day 1 while milk does not arrive until day 8. Crops
# can wait for a parcel; the herd cannot wait for anything.
#
# Measured both ways on the same seed, with the land gate forced open so the plan really was emitted:
#   pens first  -> 15 pens,  8 crop tiles   (blocks fragmented out of existence)
#   blocks first -> 1 pen,  72 crop tiles, banks **$2** and is dead by day 8 (no fertilizer income)
# Neither is a farm. The board has room for both only if they are in different quadrants, which is what
# his tape does: herd near the shed in NW, crop blocks in NE and SW behind the day-7 and day-10 parcels.
NW_FOR_PENS = True
grow_order = sorted(range(len(C.BLOCKS)),
                    key=lambda i: (0 if max(R.land_purchases_for(tuple(t))
                                            for t in C.BLOCKS[i]) > 0 else 1,
                                   -len(C.BLOCKS[i])))
tiles, melon_tiles = 0, 0
n_grow_slots = max(0, args.slots - 4)          # reserve four slots for the pen groups
for i in grow_order:
    if len(rows) >= n_grow_slots:
        break
    block = C.BLOCKS[i]
    if set(block) & taken:
        continue
    if NW_FOR_PENS and all(R.land_purchases_for(tuple(t)) == 0 for t in block):
        continue                                # pure-NW block: leave the ground for the herd
    # Start the day after the block's quadrant can be bought, never before: `_apply_unit_action` bails
    # on a LOCKED tile before it reaches PLANT, so an early block plants nothing, silently, all season.
    need = max(R.land_purchases_for(tuple(t)) for t in block)
    start = 0 if need == 0 else (sorted(LAND_DAYS)[need - 1] + 1 if need <= len(LAND_DAYS) else None)
    if start is None or start >= R.SEASON_DAYS or not ground_ok(block, start):
        continue
    crop = "MELON" if melon_tiles < 20 else "STRAWBERRY"
    if crop == "MELON":
        melon_tiles += len(block)
    # **`land_day` is a DEADLINE carried by the chain that needs the ground, not a farm-level
    # schedule.** `_land_requests` reads it only off slots whose own tile needs a parcel, and takes the
    # earliest such day per parcel. Writing 7 and 10 onto two NW slots -- which need no land -- left
    # every NE and SW slot at 99, so `land_schedule` returned `[99, 100]`, `parcels_by(day)` was 0 all
    # season, and all six big off-NW blocks were skipped as unreachable. That is why the farm never
    # left NW's 25 tiles no matter which order pens and blocks were placed in.
    rows.append(slot(KIND_GROW, R.CROPS.index(crop), i, start,
                     LAND_NEVER if need == 0 else C.LAND_DAY_CHOICES.index(sorted(LAND_DAYS)[need - 1])))
    taken.update(block)
    tiles += len(block)

# ---------------------------------------------------------------- animals into what is left
# The herd is the working capital, not the yield: a fed animal sets `fertilizer_available` every night
# and COLLECT_FERTILIZER costs no action, so it sells from day 1 while milk does not arrive until day 8.
# Measured -- withhold that income and the same farm banks $0. So pens start on day 0 regardless of
# what else is scheduled, and `fert_trade=0` keeps `sell_fertilizer` on.
ranch_order = sorted(range(len(C.RANCH_GROUPS)), key=lambda i: -len(C.RANCH_GROUPS[i]))
pens = 0
for i in ranch_order:
    if pens >= args.pens or len(rows) >= args.slots:
        break
    group = C.RANCH_GROUPS[i]
    if set(group) & taken or not ground_ok(group, 0):
        continue
    what = R.ANIMAL_NAMES.index("COW" if pens < 8 else "SHEEP")
    rows.append(slot(KIND_RANCH, what, i, 0, LAND_NEVER, fert_trade=0))
    taken.update(group)
    pens += len(group)

while len(rows) < args.slots:
    rows.append(slot(KIND_OFF, 0, 0, 0, LAND_NEVER))

genome = np.vstack(rows).reshape(-1)
np.savez(args.out, genome=genome)

script, used, skipped = C.decode(genome, args.slots)
hands = int(np.asarray(script.hire).max())
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
got_pens = sum(len(u[2]) for u in used if u[0] == "ranch")
got_tiles = sum(len(u[2]) for u in used if u[0] == "grow")

print(f"wrote {args.out}")
print(f"  asked for   {args.pens} pens, land on {LAND_DAYS}, {args.slots} slots")
print(f"  decodes to  {len(used)} chains ({skipped} skipped), {got_pens} pens, {got_tiles} crop tiles, "
      f"{hands} hands = ${sum(FIB[:hands]) * R.SEASON_DAYS:,}/season crew")
print(f"  his farm    14 pens, ~61 crop tiles, 12 hands = $11,280/season crew")
print()
for u in used:
    print(f"    {u[0]:>5} {u[1]:>11} {len(u[2]):>2} at {tuple(u[2])[0]}  start day {u[3]}")