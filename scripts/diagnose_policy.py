"""Three measurements that the training log cannot make, on a trained checkpoint.

Each answers a question that is currently being argued from proxies. In order of how much they
would change the decision:

**1. What does DIG land on?** `DIG` climbed 5.6% -> 12.9% over 1,300 updates while `plant` sat at
~4% and `harv` fell to 0.03%. `jax_masks.py:88` makes DIG legal on `(kind == WEED) | is_plant |
empty_structure`, so it destroys a *healthy growing crop* just as happily as a weed. Two stories fit
the rates equally well and need different fixes:

  (a) it digs up its own healthy plants -- self-sabotage, and upstream of everything else;
  (b) it plants, never waters, the plant dies to WEED in two days, and it digs the *weed* -- in
      which case DIG is a symptom of not watering and the fault is upstream of DIG.

Weeds spawn at 0.005 per empty tile per day, so a whole season yields at most ~15 of them; a crew of
~1.8 over 720 turns digging 11% of the time is ~166 digs. The arithmetic says most digs cannot be
weeds, but arithmetic is not a measurement. This one is.

**2. Where does the $3,000 go?** Flagged as missing since session 6 and still inferred from attempt
rates, which cannot attribute dollars: every spending head is affordability-masked, so attempts
continue and silently fail once the bank is empty.

**Attribution is by counterfactual diff, not by re-deriving costs.** For each cause the turn is
re-stepped with that cause's orders zeroed and the resulting money differenced. That uses the
simulator's own logic, including every precondition -- which matters here, because a checker written
from the same misreading as the thing it checks agrees with it. That is precisely how the no-op
HARVEST loop survived, and `ladder.census` already applies this rule by pushing actions through the
environment's own `_apply_unit_action`.

The run prints a **reconciliation residual**: attributed costs plus revenue against the actual money
delta. Causes interact (spending on seed can make a later hire unaffordable), so the residual will
not be exactly zero -- but a large one means the attribution is not trustworthy and should not be
read. Say so rather than quietly reporting numbers that do not add up.

**3. Does the value head know an animal from a hole in the ground?** With terminal reward the
advantage on FEED is `gamma^(T-t) * win - V(s)`. If `V` cannot separate a board with four fed
animals from one with none, that advantage is noise and no amount of policy training reaches the
animal economy.

The states come from the **winners' replays** rather than from self-play, because a policy that owns
no animals cannot generate the states this probe needs -- which is the whole problem. `adapter.py`
rebuilds a real board from any recorded turn, verified 5/5 at turns 0/50/240/500/700.

    .venv/bin/python -u scripts/diagnose_policy.py <checkpoint> --games 8
"""

import argparse
import collections
import pathlib
import pickle

import jax
import jax.numpy as jnp
import numpy as np

from kagg.il import bc, replays
from kagg.rl import adapter, jax_act as A, jax_heuristic as HEUR, jax_obs, jax_policy as P
from kagg.sim import jax_sim as J
from kagg.sim import ops as O

EPISODE_TURNS = 719

# What a DIG can legally be standing on, per `jax_masks.py:88`.
DIG_TARGETS = {"WEED": J.WEED, "PLANT": J.PLANT, "COOP": J.COOP,
               "PASTURE": J.PASTURE, "EMPTY": J.EMPTY, "LOCKED": J.LOCKED}

# The market heads, one per spending or earning cause. `hire` and `buy_land` are booleans; the rest
# are per-item quantities. Zeroing a field is what "this cause did not happen" means.
CAUSES = ("hire", "buy_seed", "buy_animal", "buy_product", "buy_land", "sell")
_ZERO = {"hire": False, "buy_land": False}


def _sample(key, heads, masks):
    return A.sample(key, heads, masks)[0]


def rollout(params, model, batch, key, seat, turns):
    """Policy vs the scripted farmer, recording what DIG hit and money by cause.

    Both are computed on the policy's own seat and its **live** units only. `MAX_UNITS` is 24
    against a crew of about two, so anything averaged over every slot is padding -- the mistake this
    project has now made in three separate places.
    """
    state = J.reset(batch)

    def one_turn(carry, _):
        state, key = carry
        key, ka = jax.random.split(key)

        tiles, units, glob = jax_obs.encode(state)
        masks = A.masks_for(state)
        heads, _v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
        act = _sample(ka, heads, masks)

        sim_actions = A.to_sim_actions(act, batch)
        heur = HEUR.actions(state)
        seats = jnp.arange(2)[None, :]
        theirs = jnp.broadcast_to(seats != seat, (batch, 2))
        sim_actions = jax.tree_util.tree_map(
            lambda mine, other: jnp.where(
                theirs.reshape(theirs.shape + (1,) * (mine.ndim - 2)), other, mine),
            sim_actions, heur)

        # ---- what is under each unit that chose DIG, before the step resolves it
        pos = state.farm.unit_pos                                   # [B, P, U, 2]
        idx = pos[..., 1] * J.BOARD + pos[..., 0]
        kind_here = jnp.take_along_axis(state.tiles.kind[:, :, None, :], idx[..., None],
                                        axis=-1)[..., 0]            # [B, P, U]
        live = units[..., 0] > 0.5                                  # [B, P, U]
        digging = (sim_actions.unit_op == O.DIG) & live
        digging = digging & (jnp.arange(2)[None, :, None] == seat)
        dig_hits = jnp.stack([
            ((kind_here == k) & digging).sum() for k in DIG_TARGETS.values()])

        # A dug PLANT that was still alive is destruction; one already gone to WEED is cleanup.
        # `consecutive_unwatered` is the discriminator the environment itself uses.
        unwatered = jnp.take_along_axis(state.tiles.consecutive_unwatered[:, :, None, :],
                                        idx[..., None], axis=-1)[..., 0]
        dug_plant = digging & (kind_here == J.PLANT)
        dig_plant_dry = jnp.stack([(dug_plant & (unwatered == d)).sum() for d in range(3)])

        # ---- money by cause, via the simulator's own step with one cause removed
        nxt = J.step(state, sim_actions)
        base = nxt.farm.money[:, seat].sum()

        def without(cause):
            zeroed = sim_actions._replace(**{
                cause: jnp.full_like(getattr(sim_actions, cause), _ZERO.get(cause, 0))})
            return J.step(state, zeroed).farm.money[:, seat].sum() - base

        # Positive = this cause cost money over the turn; negative = it earned.
        deltas = jnp.stack([without(c) for c in CAUSES])
        actual = base - state.farm.money[:, seat].sum()

        return (nxt, key), dict(dig=dig_hits, dig_dry=dig_plant_dry, money=deltas,
                                actual=actual, live=(live[:, seat]).sum())

    (final, _), tr = jax.lax.scan(one_turn, (state, key), None, length=turns)
    return final, jax.tree_util.tree_map(lambda x: x.sum(axis=0), tr)


def value_vs_animals(params, model, n_replays=40, per_replay=12):
    """Does `V` rise with the number of animals on the board?

    Sampled across whole seasons of real winner play, so the animal counts span 0 to a full herd.
    Both seats are used: the *losing* seat of a top game is still a real board, and restricting to
    winners would confound "has animals" with "is winning", which is the confound this probe exists
    to avoid.
    """
    refs = bc.rank_seats(bc.find_replays("data"))[:n_replays]
    by_count = collections.defaultdict(list)

    for ref in refs:
        turns = list(replays.iter_turns(ref.path, winners_only=False, seats={ref.seat}))
        if not turns:
            continue
        step = max(1, len(turns) // per_replay)
        for obs, privates, _action, seat in turns[::step][:per_replay]:
            state = adapter.state_from_obs(obs, privates)
            n_animals = int((np.asarray(state.tiles.animal)[0, seat] != J.NO_ANIMAL).sum())
            tiles, units, glob = jax_obs.encode(state)
            _heads, v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
            by_count[n_animals].append(float(np.asarray(v).reshape(2)[seat]))
    return by_count


def value_by_day(params, model, n_replays=40, per_replay=24):
    """`V` grouped by the board's game-day, for driving a mixed curriculum's composition.

    **Why the animal probe cannot answer this.** `value_vs_animals` bins by animal count sampled
    across whole seasons, and day 0-8 boards carry ~0 animals on both sides, so every one of them
    lands in the same "0 animals" bucket. The animal gap can therefore read healthy while the critic
    is entirely blind to openings -- which is the one thing a day-0 slot share depends on.

    **What to read.** Not the mean. The *spread* of `V` within a day: it is the width that says the
    critic separates a good opening from a bad one, and a policy-gradient advantage on those states
    is exactly that separation. A flat `V` across day-0 boards means those slots are producing no
    usable advantage at any fraction, so raising the day-0 share would buy nothing and cost the
    day-25 signal. The mean across days is expected to rise with the day for a reason that is not
    about the critic at all -- later boards are richer and closer to a decided game -- so reading the
    mean would confuse "the season progresses" with "the critic can see".

    `per_replay` is higher than the animal probe's because the bins here are days, and 12 samples
    over a 30-day season leaves some days with too few boards to estimate a spread.
    """
    refs = bc.rank_seats(bc.find_replays("data"))[:n_replays]
    by_day = collections.defaultdict(list)

    for ref in refs:
        turns = list(replays.iter_turns(ref.path, winners_only=False, seats={ref.seat}))
        if not turns:
            continue
        step = max(1, len(turns) // per_replay)
        for i, (obs, privates, _action, seat) in enumerate(turns[::step][:per_replay]):
            state = adapter.state_from_obs(obs, privates)
            day = (i * step) // J.TURNS_PER_DAY
            tiles, units, glob = jax_obs.encode(state)
            _heads, v = model.apply(params, A._flat(tiles), A._flat(units), A._flat(glob))
            by_day[day].append(float(np.asarray(v).reshape(2)[seat]))
    return by_day


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkpoint")
    ap.add_argument("--games", type=int, default=8)
    ap.add_argument("--turns", type=int, default=EPISODE_TURNS)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--skip-value", action="store_true")
    ap.add_argument("--early-day", type=int, default=8,
                    help="upper bound of the 'early' band in section 4. Defaults to 8 because that "
                         "is where the strategic choice actually lives -- buy animals or plant "
                         "crops, build pastures or buy land -- so it is the band a mixed "
                         "curriculum's day-0 share exists to cover.")
    ap.add_argument("--late-day", type=int, default=22,
                    help="lower bound of the 'late' band in section 4, as the comparison")
    args = ap.parse_args()

    with pathlib.Path(args.checkpoint).open("rb") as fh:
        ck = pickle.load(fh)
    params = jax.device_put(ck["params"])
    saved = ck.get("args") or {}
    model = P.Policy(d_model=saved.get("d_model", 128), n_heads=saved.get("heads", 4),
                     n_layers=saved.get("layers", 3))
    print(f"checkpoint {args.checkpoint}  (update {ck.get('update')})", flush=True)

    key = jax.random.PRNGKey(args.seed)
    _final, tr = rollout(params, model, args.games, key, seat=0, turns=args.turns)

    # ------------------------------------------------------------------ 1. DIG
    hits = np.asarray(tr["dig"], dtype=float)
    total = hits.sum()
    print(f"\n=== 1. what DIG lands on  ({int(total):,} digs over {args.games} games) ===")
    if total:
        for name, n in sorted(zip(DIG_TARGETS, hits), key=lambda kv: -kv[1]):
            print(f"  {name:8s} {int(n):7,d}  {100 * n / total:5.1f}%")
        dry = np.asarray(tr["dig_dry"], dtype=float)
        print(f"  of the digs that hit a PLANT, by consecutive_unwatered: "
              f"0 (healthy):{int(dry[0]):,}  1:{int(dry[1]):,}  2+:{int(dry[2]):,}")
        print("  A dug PLANT at unwatered 0 was alive and thriving -- that is destruction, not "
              "cleanup.")
    else:
        print("  no digs at all")

    # ------------------------------------------------------------------ 2. money
    money = np.asarray(tr["money"], dtype=float) / args.games
    actual = float(tr["actual"]) / args.games
    print(f"\n=== 2. money by cause, per game (positive = cost, negative = earned) ===")
    for name, d in sorted(zip(CAUSES, money), key=lambda kv: -kv[1]):
        print(f"  {name:12s} {d:+10,.0f}")
    attributed = money.sum()
    resid = actual + attributed
    print(f"  {'-' * 24}\n  attributed   {attributed:+10,.0f}\n  actual delta {actual:+10,.0f}")
    print(f"  residual     {resid:+10,.0f}"
          + ("   <- small; attribution is readable" if abs(resid) < 0.15 * max(1.0, abs(attributed))
             else "   <- LARGE. Causes interact (spending on one makes another unaffordable), so "
                  "these numbers do not add up and should not be read as a breakdown."))

    # ------------------------------------------------------------------ 3. value
    if not args.skip_value:
        print(f"\n=== 3. does V rise with animals on the board? ===")
        by_count = value_vs_animals(params, model)
        if not by_count:
            print("  no replay states built")
        else:
            rows = sorted(by_count.items())
            for n, vs in rows:
                if len(vs) >= 5:
                    print(f"  {n:2d} animals  n={len(vs):4d}  V {np.mean(vs):.4f} "
                          f"+/- {np.std(vs):.4f}")
            none = by_count.get(0, [])
            some = [v for n, vs in by_count.items() if n >= 4 for v in vs]
            if len(none) >= 5 and len(some) >= 5:
                gap = np.mean(some) - np.mean(none)
                print(f"\n  V(4+ animals) - V(0 animals) = {gap:+.4f}")
                print("  Near zero means the critic cannot see animals, so the advantage on FEED "
                      "is noise\n  and no amount of policy training reaches the animal economy.")

    # ------------------------------------------------------- 4. value by day (mixed curriculum)
    if not args.skip_value:
        print("\n=== 4. can V separate boards WITHIN a game-day?  (drives --curriculum-mix) ===")
        by_day = value_by_day(params, model)
        if not by_day:
            print("  no replay states built")
        else:
            print("  Read the SPREAD, not the mean. The mean rises with the day because later "
                  "boards are\n  richer and nearer a decided game -- that is the season "
                  "progressing, not the critic seeing.")
            for day in sorted(by_day):
                vs = by_day[day]
                if len(vs) >= 5:
                    print(f"  day {day:2d}  n={len(vs):4d}  V {np.mean(vs):.4f} "
                          f"+/- {np.std(vs):.4f}  [{np.min(vs):.3f}, {np.max(vs):.3f}]")
            early = [v for d, vs in by_day.items() if d <= args.early_day for v in vs]
            late = [v for d, vs in by_day.items() if d >= args.late_day for v in vs]
            if len(early) >= 5 and len(late) >= 5:
                print(f"\n  spread within days 0-{args.early_day}:  {np.std(early):.4f}")
                print(f"  spread within days {args.late_day}-29: {np.std(late):.4f}")
                print("\n  The early spread is the number that licenses shifting a mixed "
                      "curriculum's weight\n  toward day 0. Flat there means those slots generate no "
                      "usable advantage at ANY fraction,\n  so raising the day-0 share would cost "
                      "the day-25 signal and buy nothing.")


if __name__ == "__main__":
    main()
