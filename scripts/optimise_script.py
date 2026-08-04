"""Direct trajectory optimisation: hill-climb a 720-turn action script against the validated sim.

Task #9. The premise, established in `docs/tutorial_how_this_game_is_actually_optimised.md`:

- The winning artifact in this game is an **open-loop 720-turn action script**, not a reactive policy.
- Our simulator reproduces a real $145k leaderboard season to **0.2%**, so offline evaluation is
  trustworthy (`docs/the_winners_are_open_loop_2026-08-04.md`).
- The sim is **deterministic** at `weed_chance=0`, so one perturbation's effect is an exact finite
  difference rather than a noisy estimate. That is the quantity PPO spends a critic, GAE and 719 steps
  of credit assignment approximating, and it is the whole reason this approach is cheap.

**The seed is our own agent's recorded trajectory** (`scripts/extract_seed_script.py`), not a
leaderboard replay. What the replays contributed is knowledge -- that the artifact is a sequence, that
labour is nearly free, that ~35% of leader revenue is livestock, that their farmer no-op rate is 7.2%
against our 88.1% -- which is ordinary competitive analysis.

**No legality machinery is needed, and that is deliberate.** An illegal op degrades to NOOP inside the
simulator, so an illegal mutation simply wastes that unit-turn and scores worse. The optimiser rejects
it on its own. This is a real advantage over the policy-gradient route, which needed
`jax_masks.py` and where a mask bug silently taught the policy to request cows it did not own.

**Selection is on wins across a fixed opponent set, with money only as a tie-break.** `CLAUDE.md` is
explicit that the ladder is Elo and money is the wrong criterion. Four opponents give a very coarse
0-4 win count, hence the tie-break -- but the ordering is wins first. The remaining compromise is that
the opponents are our *own* recorded agents with weeds off, so the resulting script must still be
scored against the real pool (`kagg.arena`) and across weed seeds before it is believed (task #11).
Do not report a money figure from this script as a competitive result.

    PYTHONPATH=. python3 -u scripts/optimise_script.py --iters 200 --batch 192
"""

import argparse
import pathlib
import time

import jax
import jax.numpy as jnp
import numpy as np
from jax import lax

from kagg.search import boards, chain_mutate
from kagg.search.script_mutate import FIELDS, mutate
from kagg.sim import jax_sim as J

ap = argparse.ArgumentParser()
ap.add_argument("--seed-script", default="data/seed_scripts/heuristic_seed0.npz")
ap.add_argument("--opponents", default="heuristic,rancher,homestead,carrot",
                help="seed scripts to play against; selection is on WINS across all of them")
ap.add_argument("--iters", type=int, default=20000)
ap.add_argument("--batch", type=int, default=192, help="candidates evaluated per iteration")
ap.add_argument("--mutations", type=int, default=8, help="edits per candidate")
ap.add_argument("--sim-seed", type=int, default=0)
# **Every candidate is scored on the same set of boards, and this is a correctness fix, not a knob.**
# `reset_with_shops` draws a fresh shop-unlock order per batch element, which is right for training
# and wrong for selection: one identical tape scored $107,661-$152,867 across six batch positions, a
# 27% spread, while this search's recorded "improvement" was 1.6%. The argmax was ranking boards.
# Pinned by `tests/test_selection_boards_are_shared.py`; the mapping lives in `kagg/search/boards.py`.
ap.add_argument("--boards", type=int, default=4,
                help="unlock schedules every candidate is scored on; the score is the mean over them")
ap.add_argument("--rng", type=int, default=0)
ap.add_argument("--out", default="data/opt_scripts")
ap.add_argument("--ckpt-every", type=int, default=10,
                help="iterations between checkpoint writes; this run must survive a closed laptop")
ap.add_argument("--resume", default=None, help="checkpoint .npz to continue from")
# **The operator is a flag so the two can be compared on equal budget**, which is the only way to tell
# a local maximum from a broken mutation. `slot` edits one [turn, unit] cell; on the winner's tape it
# accepted 3 moves in 70 iterations and stalled at +1.6% after iteration 30
# (`data/logs/optimise_from_winner.log`). That reads as "the tape is optimal" and may instead be that
# a single-slot edit strands a unit mid-chain, so the rest of its day walks to places that no longer
# matter. `chain` moves whole unit-days, which are closed sequences because the crew respawns on the
# shed each dawn. Acceptance rate is the discriminator, so the acceptance RULE is held fixed here and
# only the operator changes -- one delta at a time.
ap.add_argument("--operator", choices=("slot", "chain"), default="slot",
                help="mutation operator: per-slot (script_mutate) or per-unit-day (chain_mutate)")
args = ap.parse_args()

blob = np.load(args.seed_script)
seed_script = {f: np.asarray(blob[f]) for f in FIELDS}      # [T, P, ...]
T = seed_script["unit_op"].shape[0]
U = seed_script["unit_op"].shape[2]
# **Crew size per turn.** 24 slots against a crew averaging 5, so a mutation aimed above `crew[t]`
# edits a unit that does not exist and is a guaranteed no-op. Without this the search spends ~80% of
# its budget on slots that cannot matter. `crew` is recorded by `extract_seed_script.py`.
crew = np.asarray(blob["crew"])[:, 0] if "crew" in blob else np.full(T, U)
crew = np.minimum(np.maximum(crew, 1), U).astype(int)
print(f"crew per turn: mean {crew.mean():.1f}, max {crew.max()} "
      f"-- mutations are restricted to live slots")
print(f"seed {args.seed_script}: {T} turns, {U} unit slots")
print(f"seed final money: seat0 ${blob['money'][-1,0]:,.0f}  seat1 ${blob['money'][-1,1]:,.0f}\n")

# Seat 0 is ours and is optimised. Seat 1 is drawn from a FIXED SET of recorded opponent trajectories,
# which keeps the objective exactly deterministic while not being a single-opponent objective.
#
# **Selection is on wins across the set, not on money.** `CLAUDE.md` is explicit -- "Select on win rate,
# not money. The leaderboard is an Elo-style rating; a $43k win and a $4k win score identically" -- and
# separately records that building the opposition from the candidate's own parameters "produced a
# confounded result that fully reversed". Optimising money against one frozen mirror of ourselves is
# both of those mistakes at once. Money survives only as a tie-break, because a handful of opponents
# gives a very coarse win count.
OPPONENTS = []
for name in args.opponents.split(","):
    p = pathlib.Path("data/seed_scripts") / f"{name.strip()}_seed{args.sim_seed}.npz"
    if not p.exists():
        raise SystemExit(f"missing opponent script {p}; run scripts/extract_seed_script.py --agent {name}")
    b = np.load(p)
    OPPONENTS.append((name.strip(), {f: jnp.asarray(np.asarray(b[f])[:, 1]) for f in FIELDS}))
print(f"opponents ({len(OPPONENTS)}): " + ", ".join(n for n, _ in OPPONENTS))


N_OPP = len(OPPONENTS)
N_BOARDS = args.boards
# A "pair" is one (opponent, board) combination, and every candidate plays all of them. The opponent
# script is repeated across the board axis so pair `p` belongs to opponent `p // N_BOARDS`, matching
# `boards.unlock_array`'s layout exactly -- the two must agree or candidates face mismatched markets.
N_PAIRS = boards.pair_count(N_OPP, N_BOARDS)
OPP_XS = {f: jnp.stack([OPPONENTS[o][1][f] for o in boards.opponent_of_pair(N_BOARDS, N_PAIRS)],
                       axis=1) for f in FIELDS}
print(f"boards: {N_BOARDS} unlock schedules x {N_OPP} opponents = {N_PAIRS} games per candidate")


def _expand(mine_t, theirs_t, n_opp, b):
    """One turn's actions for every (opponent, candidate) pair -> the `[n_opp*b, 2, ...]` sim wants.

    `mine_t` is `[b, ...]` and `theirs_t` is `[n_opp, ...]`. Both are broadcast rather than tiled, so
    the full-length opponent scripts are never replicated across the candidate axis -- replicating
    `unit_op` alone would be ~100 MB per copy.
    """
    tail = mine_t.shape[1:]
    m = jnp.broadcast_to(mine_t[None], (n_opp, b) + tail).reshape((n_opp * b,) + tail)
    th = jnp.broadcast_to(theirs_t[:, None], (n_opp, b) + tail).reshape((n_opp * b,) + tail)
    return jnp.stack([m, th], axis=1)


@jax.jit
def _run(state0, cand):
    """Final money for every candidate against EVERY opponent, in a single scan.

    **One scan, not one per opponent.** The season is 719 *sequential* steps, so the cost is
    dominated by that chain rather than by its width; four separate scans paid the chain four times
    for the same total work. Folding the opponent set into the batch axis pays it once.

    `state0` is passed in rather than built here: `reset_with_shops` calls `np.asarray` on the unlock
    schedule, which cannot be traced. The initial state is fixed for a given sim seed anyway.
    """
    b = cand["unit_op"].shape[0]
    xs = {f: jnp.swapaxes(cand[f], 0, 1) for f in FIELDS}     # [T, B, ...]

    def body(st, slice_pair):
        mine, theirs = slice_pair
        acts = J.Actions(**{f: _expand(mine[f], theirs[f], N_PAIRS, b) for f in FIELDS})
        return J.step(st, acts, weed_chance=0.0), None

    state, _ = lax.scan(body, state0, (xs, OPP_XS), length=T)
    # [n_opp*b] -> [n_opp, b], so a row is one candidate across the whole opponent set.
    mine = state.farm.money[:, 0].reshape(N_PAIRS, b)
    theirs = state.farm.money[:, 1].reshape(N_PAIRS, b)
    return mine, theirs


_STATES = {}


def evaluate(cand):
    """Returns `(wins[B], mean_money[B])` over the whole opponent set.

    Wins is the selection criterion; mean money only breaks its ties.
    """
    b = cand["unit_op"].shape[0]
    if b not in _STATES:
        # `reset`, not `reset_with_shops`: the schedule is built so a board depends on the pair
        # slot and never on the candidate index. That is the whole fix.
        unlocks = boards.unlock_array(N_OPP, N_BOARDS, b, seed=args.sim_seed)
        _STATES[b] = J.reset(len(unlocks), unlock_schedule=unlocks, seed=args.sim_seed)
    mine, theirs = _run(_STATES[b], cand)
    mine = np.asarray(mine)
    wins = (mine > np.asarray(theirs)).sum(axis=0).astype(float)
    return wins, mine.mean(axis=0)


def better(a, b):
    """Lexicographic: more wins, then more money."""
    return (a[0], a[1]) > (b[0], b[1])


def propose(base, rng, n_cand, n_edits):
    """`mutate` plus the host-to-device hand-off. The operator itself lives in
    `kagg/search/script_mutate.py` so it can be unit-tested -- both defects it now pins
    (`hire` clamped to 0/1 by a bool dtype, `buy_land` never mutated at all) were invisible in a
    script that no test could import."""
    op = mutate if args.operator == "slot" else chain_mutate.mutate
    return op(base, rng, n_cand, n_edits, crew)


print(f"operator: {args.operator}")

out = pathlib.Path(args.out)
out.mkdir(parents=True, exist_ok=True)
path = out / f"opt_{pathlib.Path(args.seed_script).stem}_{args.operator}.npz"

rng = np.random.default_rng(args.rng)
start_iter = 0
if args.resume:
    ck = np.load(args.resume)
    best = {f: np.asarray(ck[f], dtype=np.int64) for f in FIELDS}
    start_iter = int(ck["iter"]) + 1
    print(f"resumed from {args.resume} at iteration {start_iter}")
else:
    # int64 throughout. The recorder stores the seed agent's own dtypes, and `jax_heuristic`
    # emits a BOOL `hire`; carrying that into the candidate array clamped every hire mutation to
    # 0/1 with no error anywhere. Pinned by `tests/test_script_mutation_space.py`.
    best = {f: np.asarray(seed_script[f][:, 0], dtype=np.int64) for f in FIELDS}

w0, m0 = evaluate({f: v[None] for f, v in best.items()})
base = (float(w0[0]), float(m0[0]))
print(f"start: {base[0]:.0f}/{N_PAIRS} wins, mean money ${base[1]:,.0f}")
if not args.resume:
    print("(the money figure must match the extractor's seat0 vs heuristic; "
          "a mismatch means the harness is wrong)")
print()

# **Neutral drift is allowed, and it is the whole point.**
#
# The first version accepted a candidate only on STRICT improvement, and that cannot build the animal
# economy no matter how long it runs. `BUILD_PASTURE` earns nothing by itself: it costs a unit-turn and
# pays back only once an animal has been bought, carried, placed and fed. Every prefix of that chain
# therefore scores neutral-or-worse, so a strict hill-climber rejects the first step every time. The
# chain is fully inside the search space -- `OP_ALPHABET` contains every op and `buy_animal` is mutated
# -- but it sits behind a PLATEAU, and a strict rule cannot cross flat ground.
#
# So `cur` accepts equal-scoring candidates and is free to wander sideways, while `best` keeps the
# best-ever script so drift can never lose a real gain. This is the standard fix for a plateau in a
# (1+lambda) search, and it is what makes the livestock chain reachable at all.
cur = base            # the wanderer: accepts ties
best_score = base     # the record: strict improvements only
best_ever = {f: v for f, v in best.items()}
t0 = time.time()
accepted = 0
improved = 0
for it in range(start_iter, args.iters):
    cand = propose(best, rng, args.batch, args.mutations)
    wins, money = evaluate(cand)
    # Lexicographic argmax: wins first, money as the tie-break.
    k = int(np.lexsort((money, wins))[-1])
    cand_score = (float(wins[k]), float(money[k]))
    if cand_score >= cur:                       # >= so flat ground can be crossed
        cur = cand_score
        best = {f: cand[f][k] for f in FIELDS}
        accepted += 1
        if cand_score > best_score:
            best_score = cand_score
            best_ever = {f: cand[f][k] for f in FIELDS}
            improved += 1
    if it % 10 == 0 or it == args.iters - 1:
        print(f"iter {it:>6} | BEST wins {best_score[0]:.0f}/{N_PAIRS} "
              f"money ${best_score[1]:>11,.0f} (+${best_score[1]-base[1]:>10,.0f}, "
              f"{100*(best_score[1]/max(base[1],1)-1):+.1f}%) | cur ${cur[1]:>11,.0f} "
              f"| improved {improved} drifted {accepted-improved} "
              f"| accept {100*improved/max(it-start_iter+1,1):.1f}% "
              f"| {time.time()-t0:.0f}s", flush=True)
    # **Checkpoint often.** This is expected to run on a laptop that gets closed and carried around,
    # so an un-checkpointed run is an un-finished run.
    if it % args.ckpt_every == 0:
        np.savez_compressed(path, iter=it, wins=best_score[0], money=best_score[1],
                            **{f: np.asarray(v) for f, v in best_ever.items()})

np.savez_compressed(path, iter=args.iters - 1, wins=best_score[0], money=best_score[1],
                    **{f: np.asarray(v) for f, v in best_ever.items()})
print(f"\nwrote {path}")
print(f"start {base[0]:.0f} wins / ${base[1]:,.0f}  ->  "
      f"{best_score[0]:.0f} wins / ${best_score[1]:,.0f}  "
      f"in {improved} improvements ({accepted-improved} neutral drift steps)")
print("\nNOT a competitive result yet: this is a fixed set of OUR OWN recorded opponents with weeds "
      "off. Score the saved script on kagg.arena and across weed seeds before believing it "
      "(tasks #11).")
