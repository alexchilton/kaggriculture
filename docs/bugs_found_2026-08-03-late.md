# Bug sweep — 2026-08-03, after the evening handoff

Prompted by "bugs and problem identification first, before P2b".
Every item below was measured, and the command that measured it is quoted.
`kagg-train` was stopped before this sweep (`systemctl is-active` → `inactive`, no orphaned python on the box).

---

## B1 — The training market has every shop permanently locked, so the town buys 1/5 the wheat it really does · MEASURED · UNFIXED

**This is the largest finding of the sweep and it is upstream of P4.**

`jax_sim.reset(batch, ..., unlock_schedule=None)` fills `unlock_day` with `J.NEVER` (`1 << 24`).
`_drain` (`jax_sim.py:967`) is `shops + centre`, where `shops = (unlock_day <= day) @ SHOP_PULL`.
With every entry at `NEVER`, **the shop term is zero for the whole season, forever.**
Only the town centre drains.

No RL or evaluation entry point passes an `unlock_schedule`:

| caller | passes a schedule? |
|---|---|
| `train_jax_rl.py:1605`, `:127` (`staggered_states`) | **no** |
| `curriculum.py:169` (`chain_states`), `:516` (day-0 rung) | **no** |
| `eval_policy.py:77`, `play_checkpoint.py:104`, `diagnose_policy.py:84`, `compare_on_positions.py:69`, `bc_dagger.py:135` | **no** |
| `search/rollout.py:72`, `search/cem.py:76` (`sample_unlock_schedule`) | yes |
| `sim/parity.py:268` | yes |

`train_jax_rl.py` has no `--unlock` flag of any kind. There is no way to switch it on.

The reference unlocks one shop every `townShopUnlockInterval = 3` game-days
(`reference/kaggriculture.py:836,855`), so all 8 shops are open by day 24.
Season drain, computed by walking `_drain` over all 720 steps:

```
product        training (NEVER)   real schedule   ratio
  WHEAT              140              698         4.99x
  STRAWBERRY         140              446         3.19x
  EGG                140              428         3.06x
  MILK               140              428         3.06x
  WOOL               140              356         2.54x
  CARROT             140              320         2.29x
  TOMATO             140              320         2.29x
  MELON              140              140         1.00x
  TOTAL            1,120            3,136         2.80x
```

Fewer units left in town inventory means a higher price (`above_func` is `log`, never floors).
End-of-season prices, drain only, no trading:

```
              training   real    ratio
  WHEAT         $37      $51     1.38x
  STRAWBERRY   $219     $297     1.36x
  EGG           $58      $76     1.31x
  MILK         $263     $340     1.29x
  TOMATO        $77      $98     1.27x
  CARROT        $41      $42     1.02x
  WOOL         $242     $250     1.03x
  MELON        $293     $293     1.00x
```

**Why this matters more than its size suggests.**

1. **It is a train/deploy mismatch, and every local instrument shares it.** The policy learns
   sell timing and whether farming pays at prices 27–38% below the ones it meets on Kaggle,
   and `eval_policy`, `play_checkpoint` and `diagnose_policy` all measure it in the same
   discounted market. The gap is invisible locally by construction.
2. **It undercuts P4's conclusion.** P4 reports the season as `SELL +2,381` against `buy -3,206`
   and concludes "the farm is run at a loss — a unit-economics failure". That was measured in a
   market where the town buys a fifth of the wheat. The buy side is mostly fixed shop prices
   (seed, animals); the sell side is market-priced and ~30% low at the tail. **P4's loss must be
   re-priced under a real schedule before it can be called a unit-economics failure at all.**
   It may be an artifact of B1.
3. **The heuristics and the RL policy were developed under different market physics.** CEM tuned
   the heuristic agents through `search/rollout.py`, which samples a real schedule. The RL policy
   never saw one. Cross-comparisons between them inherit that difference.

**Why parity never caught it.** `parity.py:268` passes the *same* schedule to both simulators, so
the gate proves jax-vs-numpy agreement given a schedule and says nothing about whether the
training entry point supplies one. This is `CLAUDE.md`'s standing lesson — "a gate only tests
what it exercises" — for the fourth time.

**Where the default came from.** `adapter.py:163` sets `unlock_day = NEVER` with a correct
justification: the schedule is a per-episode RNG artifact and cannot be recovered from an
observation. That reasoning applies to reconstructing a replayed board. It does not apply to
`J.reset` starting a fresh training game, which could sample one — and the `NEVER` default
propagated from the justified case into the unjustified one.

**Fix:** sample an unlock schedule per game in `J.reset` (or add a flag and default it on), and
re-run P4's decomposition under it. Cheap. Needs the restart we now have anyway.

---

## B2 — `--n-phases` is inert whenever a curriculum mix is set · MEASURED · UNFIXED

The evening handoff lists `--n-phases 12` as one of "two mitigations [that] already ship and are
active and insufficient" for P1. It is not active.

```
1494:  state = staggered_states(args.batch, args.n_phases, seed=args.seed)
...
1518:  if cur_mix:
1524:      state = seed_states          # <-- overwrites the staggered state
```

`--n-phases` has exactly two remaining effects: the divisibility check at `:1492`, and building a
`state` that `:1524` throws away. Inside `make_rollout`, `per_group = batch // n_phases`
(`:241`) is **assigned and never read** — `grep -n per_group` returns one line.

So under the live run's `--curriculum-mix length:0:0.6,10:0.1,15:0.1,20:0.1,25:0.1`, episode start
staggering is done by the *mix* (five start points, 60% of slots at day 0), not by twelve evenly
spread phases.

**Consequence for P1.** The handoff's step 1 is "how much of the value-loss gradient comes from
terminal-adjacent rows *with staggering on*", reasoned as "719/32 ≈ 22, so each phase group still
touches its own terminal about once every 22 updates". That model is not the one in force. The
figure to reason about is the mix's own terminal-episode share, which the trainer already computes
and prints at `:1529`. Staggering changes *when* terminals arrive, never what fraction of rows
they are — so no staggering setting can move the 0.14% density that P1 is about.

**Fix:** either honour `n_phases` by composing it with the mix, or delete the flag and the dead
`per_group`. Deleting is the honest option unless someone wants the composition.

---

## B3 — The synthetic chain rung gets ~6x the slots it asked for · MEASURED · UNFIXED

Directly blocks P7 (deploying the chain rung).

`length_weighted_mix` sets `weights[d] = want[d] * (season_days - d)` so that
`episodes ∝ slots / length` is constant. For the synthetic rung `d = -1` that computes
`30 - (-1) = 31` — it is weighted as a **31-day** episode. But `chain_states(start_day=25)`
produces a ~5-day, ~120-turn episode. The length is overstated 6.2x, so the rung receives 6.2x
the slots needed for the share requested.

```
parse_mix('length:0:0.6,-1:0.1,15:0.1,20:0.1,25:0.1')
  -> {25: 0.0207, 20: 0.0415, 15: 0.0622, 0: 0.7469, -1: 0.1286}
```

Rung `-1` and rung `25` are the same actual episode length and asked for the same 0.1 share.
`-1` got **6.2x** the slots. Self-evidencing: two rungs of identical length and identical
requested share cannot correctly receive different allocations.

**Fix:** map synthetic rungs to their effective start day (`-1 → 25`) before weighting.

---

## B4 — NOT A BUG. Retracted. · The rejection is deliberate and tested

Reported first as "the two mix parsers disagree about the key space": `parse_mix('-1:0.5,0:0.5')`
raises while `parse_mix('length:-1:0.5,0:0.5')` is accepted.

**It was already pinned by a test** — `test_curriculum_mix.py::test_a_day_outside_the_season_is_refused`
asserts the plain form refuses `-1`. Changing it turned that test red, which is how the mistake
surfaced.

The reason holds on inspection, so the test is right and the report was wrong. A synthetic rung's
entire defect (B3) is that its key is not its episode length, so it only means anything once length
weighting is applied — which is exactly what the `length:` prefix turns on. Accepting `-1:0.1` in
the plain form would hand it a raw *slot* share and reintroduce B3's mis-allocation from the other
direction.

**Kept, with the message improved only.** The plain form still raises, and now says which spelling
to use. `CLAUDE.md`'s "re-read the reason a thing was rejected before assuming it still holds"
applies to a test as much as to a comment.

---

## B7 — `--curriculum-behind` is a coin flip, and it INVERTS on the late rungs · MEASURED · FIXED

**Found by a pre-existing red test**, not by reading: `test_curriculum.py::test_the_behind_dial_actually_puts_the_trainee_in_the_poorer_seat`
fails on unmodified code. Confirmed by stashing every change and re-running.

`states_at_day` chose which seat the trainee occupied from `ref.seat` — the seat `bc.rank_seats`
ranked, which ranks by **final** bank. That is not the seat that is ahead *at the seed turn*, and
the gap is not small. Measured over 24 boards per rung:

```
  rung     trainee bank, behind=False   behind=True   ranked seat led at seed
  day 10        $5,095                    $3,362              62%
  day 15       $13,403                   $12,103              50%
  day 20       $27,647                   $28,180   <-- inverted   58%
  day 25       $54,052                   $58,391   <-- inverted   50%
```

So the flag delivered a coin flip, and at days 20 and 25 it handed the trainee the **richer** seat.
Its own docstring says `behind=True` is where "a win cannot be inherited and has to be earned"; on
the late rungs it was where a win was *most* inheritable. That silently voided the one guard the
curriculum has against confirming itself — and the late rungs are exactly the ones P2 and P2b are
about.

**Fix:** compare the two banks in the drawn state instead of consulting `ref.seat`. This is the
flag's documented contract, not a new behaviour, and it makes the dial exact:

```
  day 10   ahead $7,186   behind $1,270    100% of boards poorer
  day 15   ahead $18,478  behind $7,028    100%
  day 20   ahead $34,895  behind $20,932   100%
  day 25   ahead $63,818  behind $48,624   100%
```

`mirror` still works: two calls with the same seed draw the same boards and place the richer seat at
index 0 in one and index 1 in the other, which is the exchange it wants.

### Consequence for the live config, which needs a decision

The stopped `league1` run used **`--curriculum-symmetric`**, which calls `_duplicate_seat(seat=0)`
— it copies whatever sits at index 0 onto both sides. Index 0 used to be the *final-bank-ranked*
seat and is now deterministically the *richer-at-seed* seat, so symmetric rungs are now
systematically richer than before: the day-25 rung's start money moves **$54,052 → $63,818, about
18%**.

Neither choice is obviously right — under symmetric seats the pick is arbitrary by construction,
which is precisely why it should be *stated* rather than inherited from a ranking that means
something else. **Flagging rather than deciding: if the symmetric rungs should stay at their old
wealth, the fix is to duplicate the poorer seat, and that is a one-word change.**

---

## B5 — `virgin` discards the first legitimate episode of every slot under a curriculum · MEASURED · UNFIXED

`virgin = jnp.ones((batch,), dtype=bool)` at `:1729`, unconditionally.

The guard exists because `staggered_states` starts a slot mid-season on an *empty* board, which is
an inconsistent position whose terminal reward is an artifact (the comment at `:462` documents this
well). But with a curriculum mix, `state = seed_states` — real recorded boards, or `J.reset` at
turn 0 for the day-0 rung. **Those first episodes are legitimate**, and `virgin` suppresses their
reward and remarks them as truncations.

Cost is one episode per slot per process start, and it resets on `--resume` too, so the first ~6
updates after any restart have suppressed rewards for the 60% day-0 majority. Modest, but it
biases exactly the window a human reads after relaunching.

**Fix:** set `virgin` to `False` when `state` came from `seed_states` rather than
`staggered_states`.

---

## B6 — `states_at_day(0)` targets day 1, not day 0 · MEASURED · UNFIXED · (this is P5)

Confirmed as recorded. `_turn_indices(n, 0)` returns `(1, 48)`:

```
  day  0: turn range (1, 48)     <-- median turn 24 = game-day 1
  day 10: turn range (216, 288)
  day 25: turn range (576, 648)
```

Two separate defects in one line. `lo = max(1, (day - window) * TURNS_PER_DAY)` clamps to 1 for
day 0, so (a) the window is not centred on day 0 — it spans days 0–2 with a median in day 1 — and
(b) **turn 0 is never drawn at all**. Matches the handoff's measured $476 / 7 units / median
`step_index` 24.

Training special-cases day 0 to `J.reset` (`:516`), so the live run is unaffected and the function
was never actually fixed. No restart needed to fix it; nothing calls the broken path.

---

## Not a bug, checked and cleared

- **`unlock_day` is not restored on restart** (`:523` picks `step_index`, `tiles`, `farm`,
  `inventory` and not `unlock_day`). Harmless *today* only because `unlock_day` is the constant
  `NEVER` everywhere. **Fixing B1 makes this a live bug**: a restarting slot would keep the
  finished game's schedule while its board came from the seed. Fix the two together.
- `_stack` taking `key` from `states[0]` rather than concatenating — `key` is a single `[2]` array
  for the whole state, not per game. Correct as written.
- `mix_counts` largest-remainder allocation and its zero-slot guard — correct.
- `states_at_day`'s consecutive-miss bail and `top=None` — correct.

---

## B1's measured impact — and it does NOT rescue P4

A/B on the stopped `league1` checkpoint (`league1-20260803-054444/latest.pkl`), 32 games vs the
scripted farmer, both seatings, **same weights, the market as the only difference**
(`--frozen-town` against the fix). Log: `data/logs/ab_frozen_town.log`.

```
                        SELL      buy      hire     land    sell-buy
  A frozen  seat 0    +1,525   -2,224   -2,365      -0       -699
            seat 1    +1,518   -2,002   -2,600      -0       -484
  B fixed   seat 0    +2,300   -3,302   -2,122      -0     -1,002
            seat 1    +2,648   -3,400   -2,280      -0       -752
```

**Revenue rose 51-74% and the input deficit got WORSE, from -$699 to -$1,002.** Trading also starts
earlier and runs harder — day-20 sales go $16 → $124, day-22 $68 → $210.

**This settles the ambiguity against the estimate I gave before measuring.** I said the loss would
shrink from ~$825 to ~$160 because the sell side is market-priced and the buy side mostly is not.
Measured, buying rose almost exactly as much as selling (+48% against +51%): the policy is a **net
dollar buyer** on the market, so a richer price curve costs it more than it earns. **P4's
unit-economics finding survives the fix and is stronger under it.** B1 was a real bug and a real
train/deploy mismatch; it is not P4's cause.

**What the same table points at instead.** `hire` is **-$2,122 to -$2,600** — larger than the entire
season's gross sales, and roughly double the -$1,192 the evening handoff recorded. It is by a wide
margin the biggest drain, in both markets. That is **P3**, the missing "cost to keep the crew I
already have" feature, and it now looks more urgent than P2b rather than a follow-up to it.

Also worth noting against P2: **`land` is -$0 in all four runs.** This checkpoint never buys a
quadrant, so P2's `P(buy_land)`-peaks-at-day-28 propensity does not convert into spend here.

Both arms end on a median bank of **$0-2** and lose **0/0/32** in every seating, so nothing here is
a win-rate claim.

---

## Suggested order

All of B1, B2, B3, B5, B6 and B7 are **fixed**; B4 was retracted as not-a-bug. Full suite
**496 passed, 2 xfailed**, parity green, and B7's previously-red test now passes
(`data/logs/pytest_full_2026-08-03_v2.log`).

What the sweep changed about the plan:

1. **P3 moves up, ahead of P2b.** Hire is the largest drain in the season by a wide margin
   (-$2,122 to -$2,600, more than all sales) and it is unaffected by the market fix. P2b addresses
   the state distribution; nothing in P2b tells the policy what its crew costs to keep.
2. **P4 stands.** It is not a measurement artifact of B1. Do not re-open it as one.
3. **P1's step 1 needs no instrumentation.** See B2 — staggering cannot move terminal-row density,
   only its arrival time, so the analytic answer is the answer.
4. **P7 is now safe to run** — B3 was the confound sitting under it.
5. **One decision outstanding:** whether `--curriculum-symmetric` should keep duplicating the seat
   that is now richer-at-seed (day-25 rung start money $54,052 → $63,818, ~18%), or the poorer one.
   See B7.

**Still true that B1 had to land before P2b**, and it has: harvesting resume states from the
policy's own rollouts under a frozen market would have baked the wrong prices into the resume
distribution.

---

## Since written

**P3 is built and merged.** `rehire_afford = sum(HIRE_COST[:n_units-1]) / money`, clipped at 4.0 like
its two neighbours; `glob` 59 → 60. Two latent blockers surfaced with it and are fixed:
`migrate_params` had no branch for **leading**-axis growth (every prior case was trailing-axis, so no
checkpoint would have loaded at all, `--kl-prior` included), and `--resume` never routed through
`load_or_migrate` in the first place — it assigned `ck["params"]` straight through while `--init` and
`--kl-prior` both migrated. It now migrates, discards the Adam moments, and says so.
`GLOBAL_FEATURES` is derived rather than hand-counted, which is how it had gone stale before.

**Point 5 above is still the one open decision.**

**Point 1 needs qualifying.** P3 moving ahead of P2b was argued from the hire drain. The stronger
reason arrived afterwards: P2b's state source does not exist. `league1` loses 128/128 and banks
single-digit dollars, so there is nothing in its trajectories that is "just before a payoff" to
resume from. See `p2b_state_source_2026-08-03.md`.

**Test suite split.** The suite was 387s serial, which meant it was not being run per-edit. It is now
58s: `-n auto` in `addopts` (14 cores; 387s → 131s on its own) plus a `slow` mark on the ten genuine
integration tests -- the CEM search, the replay-archive scans, the ladder, the plan-transfer seasons.
The marker already existed in `pyproject.toml` and was applied to three tests, none of them
expensive. Parity and the PPO invariants stay in the default set regardless of cost, because those
are the ones that have to run on every edit. `-m 'not slow'` = 502 tests in 58s; plain `pytest` still
runs all 514.
