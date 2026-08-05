"""Hand-build the leader's farm and see what OUR machinery banks with it.

The diagnostic Alex asked for: hard-code the values we believe are right instead of searching for them,
and find out whether the ceiling is in the harness, the routines, or the search.

The reasoning. We keep reporting agreement with the leader on *derived targets* -- 8 cows, 6 sheep, land
on days 7 and 10, 12 hands -- while the plan our search actually emits is 3 cows, 0 sheep, 6 crop tiles
on 25 of 100 tiles. Those are not the same claim, and conflating them has been the single most
misleading thing in this project's reporting. This script separates them:

- If a hand-built plan at the leader's allocation banks near his $139k, then `routines.py` and the
  simulator are fine and **the search is the problem** -- it cannot find a plan we can already express.
- If it banks near our usual $40-80k, then the representation cannot express his farm at all, and no
  amount of searching will close the gap. The bug is upstream of the optimiser.

That is a genuine fork, and the answer changes what to work on next. It is also only possible now:
until today one unit could not hold a pen and a crop block, so his 12-hand layout was inexpressible by
construction (`Script.claim`).

Three plans are measured, so the difference between them is attributable:

1. `ours`        -- whatever the current best genome decodes to. The baseline.
2. `leader_mix`  -- his allocation on OUR one-thing-per-unit layout. Tests the mix alone.
3. `leader_full` -- his allocation using combined chains, i.e. pens and crops sharing units, which is
                    what lets 14 pens and ~60 tiles fit in ~12 hands.

Everything is played in the real `kaggle_environments`, not our JAX sim, because the JAX sim and the
real environment disagreed today by a factor of ten on an inert-looking tape and only the real one
decides a submission.
"""

import argparse
import sys

import numpy as np

sys.path.insert(0, ".")
sys.path.insert(0, "scripts")

from kagg.search import chains as C
from kagg.search import routines as R
import build_script_submission as B

ap = argparse.ArgumentParser()
ap.add_argument("--genome", default="data/chain_search_local/best_beam_genome.npz")
ap.add_argument("--slots", type=int, default=8)
ap.add_argument("--opponent", default="starter")
ap.add_argument("--games", type=int, default=2)
args = ap.parse_args()

SHED = R.shed_access_tiles()


def owned(quadrant=None):
    """Tiles we can legally work, nearest the shed first -- distance is what kills combined chains."""
    out = [(x, y) for y in range(R.BOARD_SIZE) for x in range(R.BOARD_SIZE)]
    if quadrant:
        out = [t for t in out if R.quadrant_of(*t) == quadrant]
    out.sort(key=lambda t: abs(t[0] - 4) + abs(t[1] - 4))
    return out


def cluster(quadrant, n, taken):
    """`n` mutually ADJACENT tiles in `quadrant`, grown outward from the one nearest the shed.

    **Compactness, not proximity, is what decides whether a group fits a day.** Sorting a quadrant by
    distance from the shed returns a diagonal ring -- `[(4,1),(3,2),(2,3),(2,4)]` -- and each diagonal
    step costs two moves, so four such pens need 25 turns of a 23-turn day and `ranch()` refuses them.
    Four *adjacent* pens are walked in three. This is why the first run of this script built 4 animals
    when asked for 14, and why the refusals all named scattered tile lists.
    """
    pool = [t for t in owned(quadrant) if t not in SHED and t not in taken]
    if not pool:
        return []
    out = [pool[0]]
    while len(out) < n:
        nxt = min((t for t in pool if t not in out
                   and any(abs(t[0] - o[0]) + abs(t[1] - o[1]) == 1 for o in out)),
                  key=lambda t: abs(t[0] - 4) + abs(t[1] - 4), default=None)
        if nxt is None:
            break
        out.append(nxt)
    return R.serpentine(out)


def pens_for(n, quadrants=("NW", "NE", "SW"), taken=None):
    """`n` pasture tiles as same-quadrant groups of at most `PER_GROUP`, one group per hand.

    **Group size is capped at 3, not 4, and only NW can do 4.** A hand has 23 work turns; each animal
    costs ~5 (draw feed, FEED, CARE, COLLECT_FERTILIZER, HARVEST, halved by `feed_every=2`) plus the
    walk out and between pens. Measured: 4 pens fit in NW at 22 turns because those tiles are nearest
    the shed, but NE needs 25 and SW 24, and `ranch()` refuses both. So 14 animals is **5 hands minimum**.

    The first version took one group per quadrant and dropped the remainder, which is why the ceiling
    test built 4 animals when it was asked for 14 -- and it counted them as `skipped` without printing
    why, so the failure looked like a result.
    """
    PER_GROUP = {"NW": 4}
    taken = set() if taken is None else taken
    groups, remaining = [], n
    for q in quadrants:
        cap = PER_GROUP.get(q, 3)
        while remaining > 0:
            group = cluster(q, min(cap, remaining), taken)
            if not group:
                break
            groups.append(group)
            taken.update(group)
            remaining -= len(group)
        if remaining <= 0:
            break
    return groups


def crop_block(crop, n, quadrant, taken):
    """A COMPACT block, for the same reason pens must be compact: the walk, not the count, is the cost."""
    return cluster(quadrant, n, taken)


# --------------------------------------------------------------------------- the three plans
def plan_ours():
    genome = np.asarray(np.load(args.genome)["genome"], dtype=np.int64)
    script, used, skipped = C.decode(genome, args.slots)
    return script, used, skipped


def _leader_plan(combined):
    """His measured allocation: 8 cows, 6 sheep, ~41 strawberry, ~20 melon, wheat bought not grown.

    `combined=True` puts a pen group and a crop block on the SAME unit, which is the only way 14 pens
    and ~60 tiles fit inside ~12 hands. `combined=False` gives every chain its own unit, which is what
    we have been searching over, and forces the crew up the hire ladder.

    Land on days 7 and 10 and never SE, exactly as his tape does it. He never pays $7,000 for the third
    parcel, so neither do we.
    """
    script = R.Script()
    used, skipped = [], 0
    # Land first: two parcels, one per day, farm-level rather than per-chain (decode() owns this
    # normally, and double-buying is how three parcels once cost $7,000 for a $3,000 need).
    for k, day in enumerate((7, 10)):
        t = day * R.TURNS_PER_DAY
        if 0 <= t < script.T:
            script.buy_land[t] += 1

    taken = set()
    # 8 cows + 6 sheep = 14 pens, in same-quadrant groups of at most 3 (4 in NW). NW is free from turn
    # 0; NE and SW unlock on days 7 and 10, so their pens cannot start before that or BUILD fires on
    # locked ground.
    cow_groups = pens_for(8, ("NW", "NE"), taken)
    sheep_groups = pens_for(6, ("SW", "NE"), taken)
    start_for = {"NW": 0, "NE": 8, "SW": 11}

    unit = 0
    for animal, groups in (("COW", cow_groups), ("SHEEP", sheep_groups)):
        for group in groups:
            q = R.quadrant_of(*group[0])
            try:
                R.ranch(script, animal=animal, tile=group, start_day=start_for[q],
                        unit=unit, buy_land=False, feed_every=2)
                used.append(("ranch", animal, tuple(group), start_for[q]))
            except ValueError as e:
                # **Printed, not counted.** Swallowing these is what made a 4-animal farm look like a
                # measurement of a 14-animal one.
                skipped += 1
                print(f"    REFUSED ranch {animal} {group}: {str(e)[:110]}")
            if combined:
                # Same hand also takes a crop block, in the same quadrant so the walk is short. This is
                # the whole point of Script.claim: 2-3 pens plus a block on one hand.
                block = crop_block("STRAWBERRY", 6, q, taken)
                if block:
                    taken.update(block)
                    try:
                        R.grow(script, "STRAWBERRY", block, plant_day=start_for[q] + 1,
                               unit=unit, buy_land=False, water_every=2)
                        used.append(("grow", "STRAWBERRY", tuple(block), start_for[q] + 1))
                    except ValueError as e:
                        skipped += 1
                        print(f"    REFUSED grow on the pen's hand {block}: {str(e)[:100]}")
            unit += 1

    # Whatever crop capacity is left, on fresh units: strawberry is the biggest market we can serve,
    # melon saturates at ~11-16 tiles (the one product whose drain is real), wheat he BUYS not grows.
    for crop, n, q, day in (("STRAWBERRY", 8, "NW", 1), ("MELON", 8, "NW", 2),
                            ("STRAWBERRY", 8, "NE", 9), ("MELON", 4, "SW", 12)):
        block = crop_block(crop, n, q, taken)
        if not block:
            continue
        taken.update(block)
        try:
            R.grow(script, crop, block, plant_day=day, unit=unit, buy_land=False, water_every=2)
            used.append(("grow", crop, tuple(block), day))
        except ValueError as e:
            skipped += 1
            print(f"    REFUSED grow {crop} {block}: {str(e)[:110]}")
        unit += 1
    return script, used, skipped


# --------------------------------------------------------------------------- play it for real
def _resolve(name):
    """Our pool agents live in `kagg.agents`; only `starter`/`pass` are kaggle_environments built-ins."""
    import importlib
    try:
        return getattr(importlib.import_module(f"kagg.agents.{name}"), "agent")
    except ModuleNotFoundError:
        return name


def play(script, label, opponent, games):
    from kaggle_environments import make

    opponent = _resolve(opponent)
    plan = B.build_plan(script.arrays())

    def agent(obs, config=None):
        step = int(obs.get("step", 0) or 0)
        if step >= len(plan):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farmer, hands, market = plan[step]
        farms = obs.get("farms")
        n_hands = 0
        if farms:
            me = int(obs.get("player", 0) or 0)
            if me < len(farms):
                n_hands = len(farms[me].get("hands", []) or [])
        return {"farmer": farmer, "hands": hands[:n_hands], "market": market}

    mine, theirs = [], []
    for g in range(games):
        env = make("kaggriculture", debug=False)
        pair = [agent, opponent] if g % 2 == 0 else [opponent, agent]
        res = env.run(pair)
        seat = 0 if g % 2 == 0 else 1
        obs = res[-1][0].get("observation") or {}
        farms = obs.get("farms") or []
        if len(farms) == 2:
            mine.append(float(farms[seat]["money"]))
            theirs.append(float(farms[1 - seat]["money"]))
    return (float(np.mean(mine)) if mine else 0.0,
            float(np.mean(theirs)) if theirs else 0.0,
            sum(1 for a, b in zip(mine, theirs) if a > b), len(mine))


PLANS = [("ours", plan_ours),
         ("leader_mix (one thing per unit)", lambda: _leader_plan(combined=False)),
         ("leader_full (combined chains)", lambda: _leader_plan(combined=True))]

print("=" * 100)
print(f"CEILING TEST -- hand-built vs searched, real kaggle_environments, vs {args.opponent}")
print("=" * 100)

for label, builder in PLANS:
    script, used, skipped = builder()
    a = script.arrays()
    pens = sum(1 for u in used if u[0] == "ranch")
    animals = sum(len(u[2]) for u in used if u[0] == "ranch")
    tiles = sum(len(u[2]) for u in used if u[0] == "grow")
    print(f"\n{label}")
    print(f"  chains {len(used):>2}  pens {pens:>2} ({animals} animals)  crop tiles {tiles:>3}  "
          f"skipped {skipped}  max hire {int(a['hire'].max())}  land {int(a['buy_land'].sum())}")
    mine, theirs, wins, n = play(script, label, args.opponent, args.games)
    print(f"  BANK ${mine:>10,.0f}   opponent ${theirs:>10,.0f}   wins {wins}/{n}")

print()
print("=" * 100)
print("If leader_full lands near $139k, the representation is fine and the SEARCH is the bottleneck.")
print("If it lands near ours, the representation cannot express his farm and searching harder is futile.")