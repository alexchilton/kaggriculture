"""What does a checkpoint actually DO, on the same board the teacher faced?

Two questions this answers that no aggregate can.

**1. Is the spawn no-op fixed?** The parked BC track was gated on `P(noop) = 0.9920` at the daily
spawn state against a 0.98 bar. That is an absorbing state: nothing planted means no new jobs, so
every subsequent morning looks like day 0 and reproduces the same decision, which is why that
checkpoint banked exactly its $3,000 start rather than some variable small number. The number to
watch is `P(noop)` for a live unit on a fresh board -- and, because a single scalar hides which way
the mass went, the whole op distribution next to it.

**2. Given the state a $120k player was in, does it do what they did?** Aggregate accuracy cannot
show this: a model can score well by matching the easy idle turns and still never act. Printing the
teacher's action beside the model's, on the same board, is the replay-not-a-rate rule applied to
behaviour cloning.

Several checkpoints can be passed and are shown side by side, which is the point -- BC against the
PPO run that started from it says whether PPO kept the behaviour or destroyed it.

    .venv/bin/python -u scripts/compare_on_positions.py data/bc_runs/*/latest.pkl \\
        data/jax_rl_runs/ppo-*/latest.pkl --positions 8
"""

import argparse
import collections
import pathlib
import pickle

import jax
import jax.numpy as jnp
import numpy as np

from kagg.il import bc, replays
from kagg.rl import adapter, jax_act as A, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

OP_NAMES = ("NOOP", "N", "S", "E", "W", "WATER", "HARV", "PLANT", "DIG",
            "PICKUP", "DROP", "PLACE", "FEED", "CARE", "COLLFERT", "FERTIL",
            "COOP", "PASTURE")


def load(path):
    with pathlib.Path(path).open("rb") as fh:
        ck = pickle.load(fh)
    saved = ck.get("args") or {}
    model = P.Policy(d_model=saved.get("d_model", 128), n_heads=saved.get("heads", 4),
                     n_layers=saved.get("layers", 3))
    return pathlib.Path(path).parent.name, jax.device_put(ck["params"]), model, ck.get("update")


def op_distribution(params, model, state, seat=0, unit=0):
    """The policy's full op distribution for one unit, **after legality masking**.

    Masked because that is the distribution it will actually sample from; the raw head can put mass
    on options that never reach the simulator, which flatters or damns it for free.
    """
    tiles, units, glob = jax_obs.encode(state)
    masks = A.masks_for(state)
    heads, value = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
    logits = P._masked_logits(heads["op"], masks["op"])          # [B*P, U, N_OPS]
    probs = jax.nn.softmax(logits, axis=-1)
    row = seat                                                    # batch of one -> row == seat
    return np.asarray(probs)[row, unit], float(np.asarray(value).reshape(-1)[row])


def spawn_report(models):
    """`P(noop)` and the top ops on a fresh board -- the state the parked track died on."""
    state = J.reset(1)
    print("=" * 78)
    print("SPAWN STATE (fresh board, day 0, one farmer)  --  the parked BC track read "
          "P(noop)=0.9920 here")
    print("=" * 78)
    for name, params, model, upd in models:
        probs, v = op_distribution(params, model, state)
        top = np.argsort(-probs)[:6]
        mix = "  ".join(f"{OP_NAMES[i]}:{probs[i]:.3f}" for i in top)
        verdict = "NOOP-LOCKED" if probs[O.NOOP] > 0.98 else "acts"
        print(f"  {name[:34]:34s} upd {str(upd):>5s}  P(noop) {probs[O.NOOP]:.4f}  "
              f"[{verdict}]  V {v:.3f}")
        print(f"  {'':34s} {mix}")


def position_report(models, n_positions, replay_index):
    """Teacher action vs each model's most-likely action, on the same board."""
    ref = bc.rank_seats(bc.find_replays("data"))[replay_index]
    turns = list(replays.iter_turns(ref.path, winners_only=False, seats={ref.seat}))
    if not turns:
        print("no turns"); return
    step = max(1, len(turns) // n_positions)
    picked = turns[::step][:n_positions]

    print("\n" + "=" * 78)
    print(f"POSITIONS from {pathlib.Path(ref.path).name} seat {ref.seat} "
          f"(final bank ${ref.bank:,.0f})")
    print("=" * 78)

    agree = collections.Counter()
    seen = collections.Counter()
    for obs, privates, action, seat in picked:
        state = adapter.state_from_obs(obs, privates)
        day = int(np.asarray(state.step_index)[0]) // J.TURNS_PER_DAY
        farm = obs["farms"][seat]
        n_animals = int((np.asarray(state.tiles.animal)[0, seat] != J.NO_ANIMAL).sum())
        n_plants = int((np.asarray(state.tiles.kind)[0, seat] == J.PLANT).sum())
        crew = 1 + len(farm.get("hands") or [])
        teach = replays.encode_action(action, J.MAX_UNITS)

        print(f"\n  day {day:2d}  ${farm['money']:>8,.0f}  crew {crew:2d}  "
              f"crops {n_plants:2d}  animals {n_animals:2d}")
        # Unit 0 is the farmer; enough to show the pattern without dumping 24 rows.
        t_op = int(teach["op"][0])
        print(f"    {'TEACHER':<34s} -> {OP_NAMES[t_op]}")
        for name, params, model, _upd in models:
            probs, _v = op_distribution(params, model, state, seat=seat, unit=0)
            best = int(np.argmax(probs))
            mark = "==" if best == t_op else "  "
            print(f"    {name[:34]:<34s} {mark} {OP_NAMES[best]:<9s} "
                  f"p={probs[best]:.2f}  (p[teacher]={probs[t_op]:.2f})")
            agree[name] += best == t_op
            seen[name] += 1

    print("\n  farmer-slot agreement with the teacher over these positions:")
    for name in seen:
        print(f"    {name[:40]:40s} {agree[name]}/{seen[name]}")


def action_census(models, n_replays=12, per_replay=25):
    """Does it ACT? Rate of non-NOOP over live units, on real winner boards.

    On teacher states, not its own -- the question is whether it responds to a real board, which is
    the thing the parked checkpoint could not do.
    """
    refs = bc.rank_seats(bc.find_replays("data"))[:n_replays]
    tally = {name: np.zeros(len(OP_NAMES)) for name, _, _, _ in models}
    live_total = 0

    for ref in refs:
        turns = list(replays.iter_turns(ref.path, winners_only=False, seats={ref.seat}))
        if not turns:
            continue
        step = max(1, len(turns) // per_replay)
        for obs, privates, _action, seat in turns[::step][:per_replay]:
            state = adapter.state_from_obs(obs, privates)
            tiles, units, glob = jax_obs.encode(state)
            masks = A.masks_for(state)
            live = np.asarray(units)[0, seat, :, 0] > 0.5
            n_live = int(live.sum())
            if not n_live:
                continue
            live_total += n_live
            for name, params, model, _u in models:
                heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
                logits = P._masked_logits(heads["op"], masks["op"])
                best = np.asarray(jnp.argmax(logits, axis=-1))[seat][live]
                tally[name] += np.bincount(best, minlength=len(OP_NAMES))

    print("\n" + "=" * 78)
    print(f"WHAT IT WOULD DO on {live_total:,} live-unit decisions across real winner boards")
    print("=" * 78)
    for name, counts in tally.items():
        tot = max(1.0, counts.sum())
        acting = 100 * (1 - counts[O.NOOP] / tot)
        top = np.argsort(-counts)[:7]
        mix = "  ".join(f"{OP_NAMES[i]}:{100*counts[i]/tot:.1f}%" for i in top)
        print(f"  {name[:40]:40s} acts {acting:5.1f}% of the time")
        print(f"  {'':40s} {mix}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoints", nargs="+")
    ap.add_argument("--positions", type=int, default=8)
    ap.add_argument("--replay-index", type=int, default=0)
    args = ap.parse_args()

    models = [load(p) for p in args.checkpoints]
    spawn_report(models)
    position_report(models, args.positions, args.replay_index)
    action_census(models)


if __name__ == "__main__":
    main()
