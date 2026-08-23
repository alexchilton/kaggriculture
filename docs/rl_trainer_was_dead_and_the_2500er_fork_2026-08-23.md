# The RL trainer had been dead for three days, and the 2500er is a different agent

2026-08-23.
Two separate threads, recorded together because they were done in one session.

## 1. `scripts/train_jax_rl.py` could not run at all, and nobody had run it

Asked whether the RL was "ready to go", the answer given on several days was yes.
That answer was read off argument names in the source.
It was never run.

A 60-second smoke run — `--updates 2 --batch 16 --horizon 8` on CPU — found five consecutive
breakages, four of them dating from the same 2026-08-22 bundle refactor and one of them mine.

| break | cause | introduced |
|---|---|---|
| `to_sim_actions() missing 1 required positional argument: 'tables'` | `jax_act.to_sim_actions` gained a third parameter in `f75174e`; this file was last touched in `7f24249`, two days earlier | 22 Aug |
| `TypeError: where requires ndarray or scalar arguments, got NoneType` | all four heuristic opponents leave `order_op/order_item/order_qty` as `None`; `to_sim_actions` always fills them, so a plain `tree_map` over the two pytrees hands `jnp.where` a `None` | 22 Aug |
| `KeyError: 'trade'` | the market heads were replaced by one `bundle` index; `actions["trade"]`, `["sell"]`, `["buy_product"]`, `["buy_animal"]` no longer exist, and `P.N_TRADE_MODES` is gone | 22 Aug |
| `KeyError: 'buy_seed'` | same, for `_spend("buy_seed")`, `("hire")`, `("buy_land")` | 22 Aug |
| `UnexpectedTracerError` | my lazy `_bundle_tables()` global was first called *inside* the traced scan, so the tracer escaped into module state | today |

`git log -1 --format=%ad -- kagg/rl/jax_act.py` is 2026-08-22 20:06.
`git log -1 --format=%ad -- scripts/train_jax_rl.py` is 2026-08-20 19:07.
That gap is the whole story: the action space was rebuilt and its only consumer was never touched.

### What the fixes were

- `_bundle_tables()` — the decode tables, built **eagerly in `make_rollout`'s body**, not lazily
  inside the scan. Bound as `_TABLES` so the closure captures concrete arrays.
- `_blend_seat(mine, theirs, seat_mask)` — replaces four copies of the same `tree_map`.
  When a field is `None` on the heuristic's side it writes `ORDER_NONE` (zeros) instead.
  This is correct rather than a patch: `_explicit_orders` (`jax_sim.py:947`) keys presence off
  `order_op` **per seat** — `(e_op != ORDER_NONE).any(axis=2)` is `[B, P]` — so the heuristic's seat
  falls back to the canonical `_order_book` derivation while the policy's seat keeps its explicit
  order sequence. Dropping the columns batch-wide would have taken the sequence away from the
  policy too, and the sequence is load-bearing: measured at bank $484 with a sheep missing against
  the tape's $13 on one turn of the teacher's opening.
- The census block re-derived off the bundle tables rather than deleted.
  `trade_counts` is now (sells / buys seed / buys product / hires), read positionally by the
  existing print.

### Still broken, NOT fixed, because fixing it changes behaviour rather than restores it

`SPEND_HEADS = ("buy_seed", "buy_animal", "buy_land", "hire")` at line 874 names four heads that no
longer exist.
The consuming loop is `if k in SPEND_HEADS and spend_p > 0.0`, so it never matches.
**`--spend-prior` is now a flag that silently shapes nothing.**
Default is 0.0, so no run to date is affected — but anyone setting it gets a byte-identical result
and reads it as a measured null.
That is the exact failure `CLAUDE.md` records for `SOLVED_DAYS`/`PRECOMPUTED_ROUTES`.

Three other scripts still call `to_sim_actions` with the old two-argument signature and will die the
same way: `scripts/play_checkpoint.py:147`, `scripts/eval_policy.py:125`,
`scripts/diagnose_policy.py:114`.

## 2. `ROLE_TAPE` — a seat-1 opponent that replays a real recorded player

Every opponent this trainer has ever had is a heuristic, and the whole family tops out at
**$30,292** (`jax_heuristic`); the rest are $3,000-$24,957.
The ladder is decided at $130,000-$180,000.
So every "beats the pool" number this project has produced was a statement about $30k play.

`ROLE_TAPE` seats one of **31 downloaded games** at seat 1, replayed by turn index.

- Built by `scripts/build_opponent_tape_actions.py` into
  `data/il/opponent_tape_actions.npz`, `[31, 719, ...]` per head.
- The tape a slot faces is `slot_index % n_tapes` — sticky by construction, so it needs no room in
  the scan carry.
- Gathered at `(tape_id, clip(state.step_index, 0, 718))`. `step_index` is `[B]` per game, which is
  the one property that had to hold for this to work at all.

**Time-indexed, not state-conditioned.** On a board the student has pushed far off the tape's line
the recorded action can be a no-op or a refused purchase and the simulator rejects it. That is
acceptable for an *opponent* — it degrades toward a weaker player, not an illegal one — and it is
exactly why the same tapes **cannot** serve as a DAgger teacher, which needs a correct label rather
than a plausible one. See §4.

### A silent hole found by round-tripping the encoder, before the run

`encode_action` returns `bundle` as a 0-d `int32`.
`build_opponent_tape_actions.py:53` selected heads with `isinstance(v, np.ndarray)`, and a numpy
scalar fails that test — so **the bundle head was dropped without a word**.
The bundle names *which* products carry an order; the per-product quantities beside it are inert
without it.
A tape opponent built from that file would have farmed all season and never traded a single unit,
while reading as a working opponent.

Rebuilt. Coverage of the 151-entry vocabulary over the 31 tapes:

```
turns total       22,289
bundle MISS        1,202  = 5.39%   unexpressible, falls to EMPTY
trading turns      9,658  = 43.33%
distinct bundles     134
```

5.39% of the tape opponents' trades are dropped. Known leak, accepted for an opponent.

### The run

```
tag tape40   updates 2000   batch 504   horizon 128
seat-1 roles: self 30%  tape 40%  pool 20%  farm 10%
box 192.168.1.128, tmux session `rl`, /home/alex/kaggriculture/data/logs/rl_tape.log
XLA_PYTHON_CLIENT_PREALLOCATE=false   (see below)
[    0] ret +0.1215+/-0.0346  ev +0.580  ent 108.7 (op 0.42)  clip 0.331   613 t/s
```

613 t/s → one update ≈ 3.5 min; `vs tape` readable at ~update 6; 2,000 updates ≈ 117 h.

**Do not run with XLA preallocation on.** The first attempt aborted hard:

```
F0823 16:26:01 bfc_allocator.cc:1063] Check failed: central_gap_ == kInvalidChunkHandle
                                      (406 vs 18446744073709551615)
                                      spatial partitioning expects one central gap
```

after backing an allocation ladder from 12 GiB down to 4 GiB on the 16 GB card.

## 3. The 2500er is not what "planner24" reconstructed

The 2026-08-18 submission that scored **2472.7** is `ead81e2`.
A variant was built on HEAD by setting `REPLAY_OPENING_DAYS = tuple(range(24))` and called
`planner24`, described as "the 2500er's structure".
That was wrong.

```
2500er (ead81e2):   REPLAY_OPENING_DAYS = (4, 5, 6, 7, 8, 9, 10, 11)
planner24 (HEAD):   REPLAY_OPENING_DAYS = tuple(range(24))
```

The 2500er runs the **planner** for d0-d3 and d12-d29 and replays the tape only on d4-d11.
`planner24` is the inverse.
The 2500er also has no `replayed()`, no `_SELL_THE_WHOLE_SHED`, no `tape_edit.py`, and is 5,356
lines.
Between `ead81e2` and HEAD the agent moved by 1,155 lines in `schedule_agent.py`, a new 514-line
`tape_edit.py` and re-solved routes — 2,226 insertions over 9 files in 31 commits.

### The real fork, gated

Worktree at `ead81e2`, with the carrot sow and the whole-shed sell **ported** onto it (not
cherry-picked — the sell rules live inside `replayed()` on HEAD, which does not exist here, so both
go in one outermost `_with_the_late_field` wrapper that sees every turn).

```
opponent      2500er     2500er+carrot     delta      shed-clear(HEAD)
mirror        87,967          86,306      -1,661            71,837
wheat_only   174,149         174,203         +54           174,167
melon_heavy  172,301         172,094        -207           173,032
strawberry   159,934         159,942          +8           153,792
cow_heavy    159,606         158,367      -1,239           139,348
carrot_25    174,486         174,895        +409           175,186
small_farm   164,860         164,156        -704           173,829
straw_small  177,935         178,496        +561           185,202
contrarian   168,806         168,368        -438           143,975
             ---------------------------------
mean        $160,005        $159,647        -358
win rate       94.4%           94.4%          =             94.4%
```

Carrot is a **wash** on this pool: -$358 mean, wins unchanged.
Note the gate cannot test what the carrot was measured on — the original +9.1 to +20.6 was a
*win-rate* gain on towns with carrot drain >= 5, and this pool is already at 100% wins on 8 of 9
opponents, so only money is visible.

The carrot chain is confirmed end to end (`scripts/probe_the_carrot_chain.py`) — `sold` equals
`into shed` and `left` is 0 on all 9 rows, so the zeros in a plain shed check mean sold, not
never-grown.

The 2500er beats HEAD on mirror by **$16,130**, contrarian by **$24,831** and cow_heavy by
**$20,258**, at identical win rate. Mirror is the only opponent in that pool that plays as well as
we do, which is what makes that column the interesting one.

## 4. The clone run `season_final2` was behaviour cloning, not DAgger, and it was killed

Killed at round 11 of 30.

```
round   student bank   opponent    result       greedy op agreement
  0..9        0-1,778   ~165,000    loss        0.085 -> 0.997
 10          134,342    144,271     loss        0.9999
 11            8,429    155,721     loss        1.0000
```

Agreement reached **exactly 1.0000** on op, bundle and traded while the off-tape season collapsed.
The $134,342 at round 10 was a single unrepeated draw; round 11 fell back to $8,429.

Two reasons the remaining 19 rounds were worth nothing:

1. **`beta` never annealed.** `dagger_tape.py:804` starts annealing when
   `last_agree >= args.anneal_after_agree`, and the run was launched with
   `--anneal-after-agree 2.0`. Agreement is a rate and cannot exceed 1.0, so the condition was never
   true and the teacher drove 100% of every episode for all 30 rounds. That makes it plain
   behaviour cloning.
2. **Annealing would not have helped anyway**, which is Alex's point and is stated in the teacher's
   own docstring: the tape lookup is time-indexed, so on a damaged board it answers "at turn t, on
   this branch, do X" rather than re-planning. Only two bits are closed-loop (`melon_armed` at d3,
   `q4_armed` at d5) plus the COW/SHEEP relabel. A student driven into its own bad states would be
   labelled with the action that was correct on a *different* board — worse than no correction.

So the teacher's coverage **is** the tape, BC on the tape is the ceiling of that setup, and we
reached it. The off-tape gap is not an imitation problem; there is no teacher that can label those
states. That is what the RL is for.

## Submissions built and verified today

```
submission/shed_clear.py       $137,491 vs starter   HEAD 1926a2c, tape 30 days, wool+carrot shed sell
submission/e2500_carrot.py     $175,477 vs starter   ead81e2 exact, tape d4-d11, planner elsewhere, + carrot
```

Both import standalone and complete a 719-turn season.
Neither is committed.
