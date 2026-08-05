"""Does the real environment actually execute what our tape orders?

Our search reports 16/16 wins in the JAX sim. The real `kaggle_environments` arena reports a 0.450 pool
win rate for the same tape, losing every game to `contrarian` and 18 of 20 to `rancher`. One of those
two numbers is measuring something other than what it claims.

There are only two candidate explanations and they call for different fixes:

1. **The opponents differ.** The search plays 4 *recorded tapes* of one seat of one seed with weeds off;
   the gate plays 6 *live agents* with weeds on. Then our tape is fine and the objective is wrong.
2. **The tape does not execute.** Orders are silently dropped -- this project's signature failure, seen
   in `_do_buy_land` no-opping when money is short, PICKUP no-opping off the shed, PLANT no-opping on
   occupied ground, and movement no-opping onto LOCKED tiles. Then our own scoring is fiction.

This separates them by auditing the one thing both stories agree on: the tape. For each resource it
prints what the tape *ordered* against what the farm *ended up holding*. A gap is a silent no-op, and
its size says how much of the plan is imaginary.

Nothing here compares against the leader. It compares our plan against itself, which is the only way to
tell a bad plan from a plan that never ran.
"""

import argparse
import collections
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
ap.add_argument("--opponent", default="contrarian")
args = ap.parse_args()


def resolve(name):
    import importlib
    try:
        return getattr(importlib.import_module(f"kagg.agents.{name}"), "agent")
    except ModuleNotFoundError:
        return name


genome = np.asarray(np.load(args.genome)["genome"], dtype=np.int64)
script, used, skipped = C.decode(genome, args.slots)
arr = script.arrays()

print("=" * 96)
print(f"WHAT THE TAPE ORDERS  ({args.genome}, {len(used)} chains, {skipped} skipped)")
print("=" * 96)
for u in used:
    print("   ", u)
ordered = {
    "animals": int(arr["buy_animal"].sum()),
    "seeds": int(arr["buy_seed"].sum()),
    "land": int(arr["buy_land"].sum()),
    "max hands in a day": int(arr["hire"].max()),
    "sell units": int(arr["sell"].sum()),
    "buy_product units": int(arr["buy_product"].sum()),
    "non-PASS unit ops": int((arr["unit_op"] != 0).sum()),
}
for k, v in ordered.items():
    print(f"  ordered {k:>22}: {v:>6}")

# ---------------------------------------------------------------- play it and watch
from kaggle_environments import make

plan = B.build_plan(arr)
seen = {"ops_submitted": 0, "hands_truncated": 0}


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
    wanted = sum(1 for h in hands if h and h[0] != "PASS")
    kept = sum(1 for h in hands[:n_hands] if h and h[0] != "PASS")
    seen["ops_submitted"] += kept
    seen["hands_truncated"] += wanted - kept
    return {"farmer": farmer, "hands": hands[:n_hands], "market": market}


env = make("kaggriculture", debug=False)
res = env.run([agent, resolve(args.opponent)])

# Walk the recorded steps for what the farm actually held.
peak = collections.Counter()
animals_seen, planted_seen, money_curve = set(), set(), []
for t, step in enumerate(res):
    obs = (step[0] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    if not farms:
        continue
    me = farms[0]
    money_curve.append(float(me.get("money", 0)))
    peak["hands"] = max(peak["hands"], len(me.get("hands") or []))
    peak["quadrants"] = max(peak["quadrants"], len(me.get("unlocked_quadrants") or []))
    # `tiles` is a 10x10 NESTED list of dicts with no x/y keys -- iterating it directly yields rows,
    # so `isinstance(row, dict)` is always False and every count silently came out 0. The position is
    # the index pair, not a field.
    for y, row in enumerate(me.get("tiles") or []):
        if not isinstance(row, list):
            continue
        for x, cell in enumerate(row):
            if not isinstance(cell, dict):
                continue
            if cell.get("animal") or cell.get("kind") in ("PASTURE", "COOP"):
                animals_seen.add((x, y))
            if cell.get("kind") == "PLANT" or cell.get("crop"):
                planted_seen.add((x, y))

final = res[-1][0].get("observation", {}).get("farms") or []
print()
print("=" * 96)
print(f"WHAT ACTUALLY HAPPENED  (real kaggle_environments vs {args.opponent})")
print("=" * 96)
print(f"  realised {'peak hands owned':>22}: {peak['hands']:>6}   "
      f"(tape asked for {ordered['max hands in a day']})")
print(f"  realised {'quadrants unlocked':>22}: {peak['quadrants']:>6}   "
      f"(tape bought {ordered['land']} parcel(s), so expect {1 + ordered['land']})")
print(f"  realised {'distinct animal tiles':>22}: {len(animals_seen):>6}   "
      f"(tape bought {ordered['animals']} animals)")
print(f"  realised {'distinct planted tiles':>22}: {len(planted_seen):>6}   "
      f"(tape bought {ordered['seeds']} seeds)")
print(f"  realised {'hand ops accepted':>22}: {seen['ops_submitted']:>6}")
print(f"  {'hand ops TRUNCATED by the n_hands clamp':>40}: {seen['hands_truncated']:>6}")
if final and len(final) == 2:
    print()
    print(f"  final bank: us ${float(final[0]['money']):>10,.0f}   "
          f"them ${float(final[1]['money']):>10,.0f}")
if money_curve:
    print(f"  bank at day 10 ${money_curve[min(240, len(money_curve) - 1)]:>9,.0f}   "
          f"day 20 ${money_curve[min(480, len(money_curve) - 1)]:>9,.0f}   "
          f"peak ${max(money_curve):>9,.0f}")

print()
print("=" * 96)
print("A gap between ordered and realised is a silent no-op and means our own scoring is fiction.")
print("No gap means the tape executes faithfully and the 16/16 was an artifact of WHO we played:")
print("recorded tapes of one seat of one seed, weeds off -- not live agents with weeds on.")