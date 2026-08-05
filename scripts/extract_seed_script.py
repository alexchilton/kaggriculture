"""Record OUR OWN agent's 720-turn action sequence, as the seed for trajectory optimisation.

Task #9. `docs/tutorial_how_this_game_is_actually_optimised.md` establishes that the winning play in
this game is an open-loop 720-turn script, and `docs/the_winners_are_open_loop_2026-08-04.md` shows our
simulator now reproduces a real $145k season to 0.2%, so offline evaluation is trustworthy.

**The seed is our own agent's trajectory, deliberately.** Seeding from a leaderboard replay would be
copying another competitor's play. What we take from the replays is *knowledge* -- that the artifact is
a sequence, that labour is nearly free, that ~35% of revenue is livestock, that their no-op rate is
7.2% against our 88% -- which is ordinary competitive analysis. The actions being optimised are ours.

Writes a `.npz` of the recorded per-turn action arrays plus the baseline this run is expected to beat.

    PYTHONPATH=. python3 -u scripts/extract_seed_script.py --agent heuristic
"""

import argparse
import pathlib
import time

import jax
import jax.numpy as jnp
import numpy as np

from kagg.sim import jax_sim as J
from kagg.sim import ops as O

AGENTS = {
    "heuristic": "kagg.rl.jax_heuristic",
    "rancher": "kagg.rl.jax_rancher",
    "homestead": "kagg.rl.jax_homestead",
    "carrot": "kagg.rl.jax_carrot",
}

ap = argparse.ArgumentParser()
ap.add_argument("--agent", default="heuristic", choices=sorted(AGENTS))
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--weeds", type=float, default=0.0,
                help="0 keeps the recording deterministic; the script is validated on weeds later")
ap.add_argument("--out", default="data/seed_scripts")
args = ap.parse_args()

import importlib
mod = importlib.import_module(AGENTS[args.agent])

FIELDS = ("unit_op", "unit_crop", "unit_item", "unit_qty",
          "sell", "buy_seed", "buy_product", "buy_animal", "hire", "buy_land")

state = J.reset_with_shops(1, seed=args.seed)
act_fn = jax.jit(mod.actions)
step_fn = jax.jit(lambda s, a: J.step(s, a, weed_chance=args.weeds))

frames = {f: [] for f in FIELDS}
money_curve = []
crew_curve = []
t0 = time.time()
for t in range(J.LAST_STEP + 1):
    a = act_fn(state)
    for f in FIELDS:
        frames[f].append(np.asarray(getattr(a, f))[0])       # drop the batch axis
    # **Crew size per turn, recorded because the optimiser needs it.** There are 24 unit slots against
    # a crew that starts at 1 and is rebuilt every dawn, so most slots hold no unit. A mutation aimed
    # at an empty slot is a guaranteed no-op, and without this the search wastes most of its budget
    # editing units that do not exist.
    crew_curve.append(np.asarray(state.farm.n_units)[0].copy())
    state = step_fn(state, a)
    money_curve.append(np.asarray(state.farm.money)[0].copy())

script = {f: np.stack(frames[f]) for f in frames}            # [T, P, ...]
money = np.stack(money_curve)                                # [T, P]
crew = np.stack(crew_curve)                                  # [T, P]

# ---- the two numbers this seed exists to improve -------------------------------------------------
ops = script["unit_op"]                                      # [T, P, MAX_UNITS]
# Only slots that actually held a unit count. A share over all MAX_UNITS slots is mostly padding --
# a mistake this project has made in three separate places.
live_hint = ops != O.NOOP
noop_share = {}
for p in (0, 1):
    # Crew size is not recorded per turn here, so report both the all-slot and the acted-slot views
    # rather than a single number that could be the misleading one.
    acted = int(live_hint[:, p].sum())
    total = live_hint[:, p].size
    noop_share[p] = (1.0 - acted / total, acted)

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
path = out / f"{args.agent}_seed{args.seed}.npz"
np.savez_compressed(path, **script, money=money, crew=crew)

print(f"agent {args.agent}   seed {args.seed}   weeds {args.weeds}   {time.time() - t0:.0f}s")
print(f"recorded {ops.shape[0]} turns, {ops.shape[2]} unit slots, both seats")
print(f"final money  seat0 ${money[-1, 0]:,.0f}   seat1 ${money[-1, 1]:,.0f}")
print("money by day: " + " ".join(f"d{d}:{money[d*24+23,0]:,.0f}" for d in range(0, 30, 5)))
for p in (0, 1):
    share, acted = noop_share[p]
    print(f"seat{p}: {acted:,} non-NOOP unit-slot-turns of {live_hint[:, p].size:,} "
          f"({100*(1-share):.1f}% acted, {100*share:.1f}% idle-or-empty)")
    # The honest denominator: slots that actually held a unit. The all-slot share above is mostly
    # padding, which is the reading this project has got wrong three times.
    live_slots = int(np.minimum(crew[:, p], ops.shape[2]).sum())
    if live_slots:
        print(f"       of {live_slots:,} slot-turns that held a real unit, "
              f"{100*acted/live_slots:.1f}% acted -- leader farmer no-op is 7.2%")
print(f"crew size: mean {crew[:,0].mean():.1f}, max {crew[:,0].max()}")
print(f"\nHIRE orders issued: seat0 {int(script['hire'][:,0].sum())}, "
      f"seat1 {int(script['hire'][:,1].sum())}   (leaders log ~300)")
print(f"BUY_ANIMAL orders:  seat0 {int(script['buy_animal'][:,0].sum())}   "
      f"(leaders buy 14; ~35% of their revenue is livestock)")
print(f"\nwrote {path}  ({path.stat().st_size/1e6:.1f} MB)")
