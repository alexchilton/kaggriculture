"""Day by day, us against the leader: where does the first real difference appear?

We now match the leader's *allocation arithmetic* -- `allocation_calculator.py` derives 7.6 cows against
his 8 and 47.7 strawberry tiles against his 41 -- and our farm still banks $81,102 against his $139,121.
So the divergence is not in what the economics say to own. It is somewhere in the sequence.

This walks both seasons side by side on the same axes -- bank, land, animals, tiles planted, hires,
sales -- and reports the first day each one separates, so the gap can be attributed to a day and a
mechanic rather than to "capacity" in the abstract.

His side is read from a real replay (`data/seed_scripts/new_leader/90016067.json`), which carries the
observation at every turn, so his bank is measured rather than modelled. Ours is our genome run through
`jax_sim` against the recorded pool. Different opponents, so the *levels* are not strictly comparable --
but the shape, the timing and the first divergence are, and those are the question.
"""

import argparse
import collections
import json
import pathlib

import numpy as np
import jax.numpy as jnp

from kagg.search import chains as C
from kagg.search import routines as R
from kagg.sim import jax_sim as J

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty", "sell", "buy_seed",
          "buy_product", "buy_animal", "hire", "buy_land")
LEADER = "somewhere after"

ap = argparse.ArgumentParser()
ap.add_argument("--genome", default="data/chain_search_local/best_beam_genome.npz")
ap.add_argument("--slots", type=int, default=8)
ap.add_argument("--replay", default="data/seed_scripts/new_leader/90016067.json")
ap.add_argument("--seed", type=int, default=0)
args = ap.parse_args()


# ---------------------------------------------------------------- his season, off the tape
def leader_timeline(path):
    d = json.load(open(path))
    seat = d["info"]["TeamNames"].index(LEADER)
    days = R.SEASON_DAYS
    bank = [None] * days
    land = collections.Counter()
    animals = collections.Counter()
    planted = collections.Counter()
    hires = collections.Counter()
    sold = collections.Counter()
    for t, step in enumerate(d["steps"]):
        day = t // R.TURNS_PER_DAY
        if day >= days:
            break
        st = step[seat] or {}
        obs = st.get("observation") or {}
        farms = obs.get("farms")
        if farms and seat < len(farms) and bank[day] is None:
            bank[day] = float(farms[seat]["money"])
        a = st.get("action") or {}
        for o in (a.get("market") or []):
            if not o:
                continue
            if o[0] == "BUY_LAND":
                land[day] += 1
            elif o[0] == "HIRE":
                hires[day] += 1
            elif o[0] == "BUY_ANIMAL":
                animals[day] += int(o[2]) if len(o) > 2 else 1
            elif o[0] == "BUY_SEED":
                planted[day] += int(o[2]) if len(o) > 2 else 1
            elif o[0] == "SELL":
                sold[day] += int(o[2]) if len(o) > 2 else 1
    return dict(bank=bank, land=land, animals=animals, planted=planted, hires=hires, sold=sold)


# ---------------------------------------------------------------- our season, through the sim
def our_timeline(genome, n_slots, seed):
    script, used, skipped = C.decode(genome, n_slots)
    arrs = script.arrays()
    state = J.reset_with_shops(1, seed=seed)
    days = R.SEASON_DAYS
    bank = [None] * days
    for t in range(script.T):
        day = t // R.TURNS_PER_DAY
        if bank[day] is None:
            bank[day] = float(np.asarray(state.farm.money)[0, 0])
        acts = {f: jnp.asarray(np.stack([np.asarray(arrs[f][t]),
                                         np.zeros_like(np.asarray(arrs[f][t]))])[None])
                for f in FIELDS}
        state = J.step(state, J.Actions(**acts), weed_chance=0.0)

    def per_day(arr, reduce_=None):
        out = collections.Counter()
        a = np.asarray(arr)
        for t in range(min(len(a), script.T)):
            v = int(a[t].sum()) if a[t].ndim else int(a[t])
            if v:
                out[t // R.TURNS_PER_DAY] += v
        return out

    return dict(bank=bank, land=per_day(script.buy_land), animals=per_day(script.buy_animal),
                planted=per_day(script.buy_seed), hires=per_day(script.hire),
                sold=per_day(script.sell), used=used, skipped=skipped,
                final=float(np.asarray(state.farm.money)[0, 0]))


him = leader_timeline(args.replay)
genome = np.asarray(np.load(args.genome)["genome"], dtype=np.int64)
us = our_timeline(genome, args.slots, args.seed)

print("our farm:")
for u in us["used"]:
    print("   ", u)
print(f"   final bank ${us['final']:,.0f}   ({us['skipped']} chains skipped)\n")

print("=" * 104)
print("DAY BY DAY. `cum` columns are running totals; bank is the bank at that dawn.")
print("=" * 104)
print(f"{'day':>4} | {'OUR bank':>10} {'land':>5} {'anml':>5} {'seed':>5} {'hire':>5} "
      f"| {'HIS bank':>10} {'land':>5} {'anml':>5} {'seed':>5} {'hire':>5} | {'bank gap':>10}")
cu = collections.Counter()
ch = collections.Counter()
for day in range(R.SEASON_DAYS):
    for k in ("land", "animals", "planted", "hires"):
        cu[k] += us[k].get(day, 0)
        ch[k] += him[k].get(day, 0)
    ob = us["bank"][day] or 0.0
    hb = him["bank"][day] or 0.0
    print(f"{day:>4} | {ob:>10,.0f} {cu['land']:>5} {cu['animals']:>5} {cu['planted']:>5} "
          f"{us['hires'].get(day,0):>5} | {hb:>10,.0f} {ch['land']:>5} {ch['animals']:>5} "
          f"{ch['planted']:>5} {him['hires'].get(day,0):>5} | {hb - ob:>+10,.0f}")

print()
print("=" * 104)
print("FIRST DIVERGENCE per axis -- the day each one separates, and by how much")
print("=" * 104)


def cum(counter):
    out, run = [], 0
    for d in range(R.SEASON_DAYS):
        run += counter.get(d, 0)
        out.append(run)
    return out


for label, key in (("land parcels", "land"), ("animals bought", "animals"),
                   ("seeds bought", "planted")):
    a, b = cum(us[key]), cum(him[key])
    first = next((d for d in range(R.SEASON_DAYS) if a[d] != b[d]), None)
    if first is None:
        print(f"{label:>16}: identical all season")
        continue
    print(f"{label:>16}: first differs on DAY {first:>2} -- us {a[first]}, him {b[first]}"
          f"   (end of season: us {a[-1]}, him {b[-1]})")

# Hires: the crew ramp, which is a rate rather than a total.
ours_h = [us["hires"].get(d, 0) for d in range(R.SEASON_DAYS)]
his_h = [him["hires"].get(d, 0) for d in range(R.SEASON_DAYS)]
print(f"{'crew per day':>16}: us {ours_h[:14]}...")
print(f"{'':>16}  him {his_h[:14]}...")
first_h = next((d for d in range(R.SEASON_DAYS) if ours_h[d] != his_h[d]), None)
print(f"{'':>16}  first differs on DAY {first_h}: us {ours_h[first_h]} hands, him {his_h[first_h]}")

# The bank is the summary axis: when does he pull away, and does he ever dip below us?
gaps = [(him["bank"][d] or 0) - (us["bank"][d] or 0) for d in range(R.SEASON_DAYS)]
ahead = [d for d in range(R.SEASON_DAYS) if gaps[d] > 0]
print()
print(f"{'bank':>16}: he is ahead from day {min(ahead) if ahead else '-'} onward; "
      f"largest gap ${max(gaps):,.0f} on day {int(np.argmax(gaps))}")
print(f"{'':>16}  we are ahead on days {[d for d in range(R.SEASON_DAYS) if gaps[d] < 0] or 'never'}")
