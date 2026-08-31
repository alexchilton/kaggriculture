# Four defects made 595 of 27,652 teacher labels unlearnable, and the parity gate could not see any of them

Measured 2026-08-22/23.
Fixed in `0f27ae8`, `d23fc85`, `5ee1044`.
Tooling in `3a4d1e3`, `ffe5593`.

## The one sentence

`560b95b` migrated **both simulators** to kaggle-environments 1.32.6 on 2026-08-09.
`kagg/rl` was never migrated with them, so for thirteen days the RL-side masks described a game nobody was playing.

## What was broken

| commit | defect | labels made unlearnable |
|---|---|---|
| `0f27ae8` | `jax_masks.can_move` forbade a LOCKED destination | 259 |
| `d23fc85` | `jax_masks.on_shed` required `kind != LOCKED`, killing PICKUP/DROP/PLACE | 29 |
| `d23fc85` | `commit._candidates` carried the same term; `COMMIT_PICKUP` could target only `(4,4)` | -- |
| `5ee1044` | `state_from_obs` read `obs["step"]`, which seat 1 never receives | 300 |

**595 of 27,652 unit labels — 2.15%.**
Each was blocked twice over: `greedy_action` argmaxes over `_masked_logits`, so the op carried `-1e9` and was unemittable at any parameter setting; and `bc.py:232` gives an illegal label weight zero, so it never reached the gradient either.
A masking mistake is therefore invisible in the loss, invisible in sampled agreement, and shows up only as one op sitting at a value that never moves.

After the fixes: **7 forbidden of 27,652 (0.025%)**, all DIG on an EMPTY tile, which `reference/kaggriculture.py` genuinely no-ops.
That gives DIG a hard ceiling of `97/104 = 0.933`, and the converged net sits at exactly `0.933`.

## Why the 300-episode parity gate cannot catch this class

The gate drives `game.py` and `jax_sim.py` against the reference from one action stream.
`jax_masks.py` and `commit.py` are RL-side only and are compared to nothing.
`jax_sim.py:683` had **no** lock term on `on_shed` and was right the whole time — which is why 300/300 passes while the mask disagreed with it.

`scripts/probe_teacher_labels_the_mask_forbids.py` is now that check.
It walks every teacher label against the mask and would have found all three LOCKED bugs in one run, in about three minutes.
Each was instead found by chasing a single stuck op backwards from an agreement table, which only works for an op the training samples often enough to notice.

## The seat-1 clock

`kaggle_environments` puts `step` in seat 0's observation only.
Measured at true turn 100 (day 4):

    92498144.json  seat 0 -> step_index 100  day 4
    91907974.json  seat 0 -> step_index 100  day 4
    92466371.json  seat 0 -> step_index 100  day 4
    91906088.json  seat 1 -> step_index   0  day 0

Every crop and animal rule keys off `step_index // TURNS_PER_DAY`.
HARVEST suffers worst: `(day - planted_day) >= FIRST_YIELD_DAY` goes negative, nothing is ever ripe, and the op is masked illegal all season.
**300 of 1,585 HARVEST labels**, all on that one tape — a quarter of the imitation training set running on a wrong clock.

`curriculum.py:114` found this independently and worked around it locally with `_with_step_index`.
The workaround never reached `dagger_tape`.

## Two harness defects found alongside

**The playout measured a policy we do not ship.**
`neural.py:255`, inside `make_agent`, is `jnp.argmax`.
The training log's `PLAYOUT` line called `run_episode(..., beta=0.0, ...)` — the rollout *collector*, where sampling is correct because beta<1 needs stochasticity — and inherited it.
Nothing chose sampling for the playout.
On the same checkpoint the sampled decode reported `student 29 vs opponent 392` while the greedy decode replayed d0-d4 **exactly**, banks matching the tape on all four tapes.

The reason argmax was once forbidden had expired and `neural.py` says so: `_fire`/`calibrate` guarded six independent binary market marginals where six base-rate "no"s composed into "never trade".
The market is one categorical now.

**The training pool held 21 copies of everything.**
At beta=1 the rollout is deterministic — fixed start state, `weedSpawnChance = 0.0`, deterministic teacher, recorded opponent.
Measured: **477 unique rows in a pool of 12,000, each stored 25.2 times.**
The cost was never the rollout (41.1 s for a 719-turn episode, ~205 s of an 868 s round); it was the fit doing ~20x the gradient steps an epoch needs.

Determinism was verified rather than assumed, twice and on the full season:

- two rollouts of each tape, hashing obs+masks+labels: **0 differences in 719 turns, 4/4**
- the box re-ran round 2 after a resume and landed on the same `greedy op 0.4014`, `bundle 0.0181`, `traded 0.0034`, `fresh 2.7199`

Same result, quarter the compute:

    BOX   (no dedup)  30 rounds  9h16m  greedy op 0.9991  bundle 0.9993  n 60000
    LOCAL (dedup)     24 rounds  2h15m  greedy op 0.9990  bundle 0.9903  n  2876

## What was retracted

Five explanations for the `op ~0.78` whole-season figure were offered before the cause was found, and all five were explaining a masking bug: observation aliasing, spurious opponent conditioning, network capacity, the beta anneal being harmful, and a transposition in the tile index.
`docs/the_net_replays_the_market_not_the_routing_2026-08-22.md` carries a header saying it is superseded.

Two further corrections worth keeping:

- **A different opponent cannot make the teacher misplay.** The teacher is time-indexed, so its emitted action stream is identical whoever it plays; imitation clones actions, not outcomes. The `$35 flips Seb's d4 land buy` example is from `breakdown.py`, which replays a tape against *our agent* in a contested market — a different setup.
- **`opponent_pool_ranked.json` is real recorded players**, not `heuristic.make_agent` with crop dials. The synthetic pool was deleted.

## The measurement that is still missing

Town and arm are one-to-one in the current dataset:

    92498144  (False,False)  seed 1240813987
    91907974  (False,True)   seed  244615642
    92466371  (True,False)   seed   70683142
    91906088  (True,True)    seed 1851650268

The observation carries market prices, and prices are a function of the town's shop draw.
So "which arm am I on" and "which town am I in" are the same signal, and **nothing measured so far distinguishes a net that learned the two latches from one that learned four price vectors.**

The held-out probe exists for exactly this and its own comment says so — *"the only thing that differs is the town draw, so a gap between this and the training number is the net having memorised prices rather than the program"* — and it is switched off (`--seeds 1 --holdout 0`) in every run to date.

The latch conditions are learnable in principle:

- **melon**, `count_tiles(obs, opponent_seat, "MELON") >= 9` at d3, reaches the net through `jax_obs`'s 14-wide opponent board summary as one scalar `/100.0`. A monotone threshold at `0.09` on a single input.
- **q4**, the yarn store open at d5, reaches it through the open-shop bits, which were added to `glob` for this.

What is missing is examples either side of each threshold.
The ranked pool gives melon counts `0, 5, 5, 7, 8` below the line and thirteen at `11-12` above, with `Subramanya N 8` the nearest miss.
A dozen combinations covers it; a product of axes does not, and 304 was a bad proposal.

**Draw the towns first** and count how many have the yarn store open by d5.
If that split is lopsided, a seed count picked at random teaches nothing about q4.

## Open

- The day-9 collapse in the student-driven season playout is **unconfirmed**: it was measured on round 23 of a still-training run, and a d3 divergence in the same table had vanished one round later. `pinned_round24.pkl` exists so probes stop reading a moving `latest.pkl`.
- `train_jax_rl.py` references `actions["trade"]`, `["sell"]`, `["buy_product"]`, `["buy_animal"]` — dead head names, four lines, diagnostics only.
- The trainer uses **gamma 0.9987/turn**; `CLAUDE.md` says **1.0**. Unresolved.
- The KL anchor to a cloned policy does not exist. `hand_prior_heads` anchors to a *shape*.
- `commit.py`'s motivating measurement (4,591 animals placed, 12 fed; `MAX_COMMIT_TURNS = 4` as "a median walk") is dated 2026-08-02, from the 1.32.2 game where a hand at `(5,5)` genuinely could not move and three of four spawn tiles could not PICKUP. Nobody re-measured it after the rules changed.
