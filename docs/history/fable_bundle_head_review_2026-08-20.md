# Fable's review of the bundle head, before any long training run

Requested 2026-08-20, read-only, on branch `bundle-head`.
Two headline claims verified independently before relaying; both hold.

## The two that stop everything

### 1. The branch has never executed. `masks_for` crashes on every call.

`kagg/rl/jax_act.py:80` reads `state.private.shed`. Verified:

    State fields: ('step_index', 'tiles', 'farm', 'inventory', 'unlock_day', 'unlock_shop', 'key')
    has private: False
    farm.shed shape: (1, 2, 12)   N_PRODUCTS 9   N_ITEMS 12

The shed is `state.farm.shed` and it is `N_ITEMS` wide (products AND animals), so even the corrected
attribute needs `[..., :N_PRODUCTS]` before it can meet `bundle_sells [N_BUNDLES, N_PRODUCTS]`.

**The flagship legality mask has never once been computed.**
`tests/test_the_bundle_head_reaches_the_simulator.py` passes because it hand-builds action dicts and
never calls `masks_for` or `sample`.
That is CLAUDE.md's "a gate only tests what it exercises", for the fourth recorded time.

### 2. The teacher is an open-loop tape for 24 of 30 days.

    UNSOLVE_DAYS = tuple(range(24, 30))                                  submission/main.py:3349
    PRECOMPUTED_ROUTES = {d: ... for d in SOLVED_DAYS if d not in UNSOLVE_DAYS}

So d0-d23 replay `PRECOMPUTED_ROUTES` and only d24-d29 are solved live.
The 0.04s/turn labelling cost that made "640 games in 50 minutes" possible **depends on** that.

Queried on a student's divergent state before d24, the teacher returns route slots for a board the
student does not have -- precisely the failure `docs/the_tape_dies_at_d13_2026-08-20.md` measured
rotting a board from d13.
`cover._apply_precomputed` keys stops on `(tile, ops)` and drops mismatches **silently**
(main.py:3322, 4574, 4783), so on a divergent board the teacher degrades rather than adapts.

**DAgger's corrective labels are therefore wrong exactly where correction was the point.**

The fix exists -- label with full solving, `UNSOLVE_DAYS = ()` style -- but at ~4s per dawn solve
instead of 0.04s/turn. That is roughly **two orders of magnitude** on the labelling budget: the
difference between 50 minutes for 640 games and days.

This must be priced before committing a long run. It is the load-bearing assumption of the whole
plan and neither of us checked it.

Caveat in the other direction, measured: our planner holds 57.5 crops / 2.4 weeds at d18 and never
rots **on its own trajectory**. The teacher is sound on-distribution and unproven off-distribution,
which is exactly where DAgger needs it.

## P0, the rest

3. **Bundle mask width is `vocab.size` (197), head width is `N_BUNDLES` (256).** `sell_table` returns
   `vocab.size` rows and nothing pads. Reproduced: `sample_head FAILS: Incompatible types for
   broadcasting: bool[2,197] vs bool[2,256]`. The fix must pad AND mark the 59 padding rows illegal:
   JAX gathers clamp out-of-range indices under jit, so an unmasked dead index would silently play
   the highest-ranked real bundle instead of erroring.

4. **Seven-plus call sites still use the one-argument `masks_for`**, including `train_jax_rl.py:316`
   (the only leg that can beat the teacher) and `play_checkpoint.py:120` (the replay check the plan
   names as its main dead-policy detector). Plus four test files. The red tests say the suite was not
   run after the signature change.

5. **`kagg/agents/neural.py` was never migrated.** Its local `MARKET_HEADS` is still the old six;
   `decode_action` reads `heads["sell"]`, `heads["hire"]`, `heads["buy_land"]`, which `Policy` no
   longer emits. No vocabulary is loaded anywhere in the file. Consequence: no out-of-scan DAgger,
   no submission, no replay check. Prerequisite, not cleanup.

6. **`kagg/il/replays.py:112` still does `hire = np.int32(1)`** -- the exact bug this change exists to
   fix, still live in the replay-label path. `bc.build_rows` will KeyError on `y_bundle`.

## P1, design faults that survive the syntax fixes

7. **The sell mask models FILLS; the teacher's labels are POSTS.** The unit phase runs before the
   market phase (`kaggriculture.py:922` then `:928`), so a DROP-at-shed lands before that hour's sell
   settles, while `masks_for` reads the pre-turn shed. The teacher's signature move -- the h23 block
   sell that funds the next dawn's hires -- is exactly this coordination. `bc_dagger.py:181` zeroes
   illegal labels, so those turns silently leave the loss.
   **Measure before training: fraction of teacher sell-bundle turns where a sold product has
   pre-turn `shed == 0`.** If not ~0, drop the sell mask or compute it against shed-plus-carried.
   Note the asymmetry: the docstring's reason for NOT masking buys is the same "the turn mutates
   state before the order settles" argument that invalidates the sell mask it kept.

8. **`bundle_index_of`'s empty-bundle fallback is silent, and DAgger is where it fires.** The
   vocabulary came from mirror self-play; DAgger queries the teacher on STUDENT states, where it can
   emit combinations self-play never produced -- so the fallback teaches "do nothing" precisely on
   the recovery states DAgger exists to label. Thread `same.any(-1)` out and print the fallback rate.

9. **The qty heads are ungated in `_score` and in `bc_dagger`'s loss.** `build_bc_rows.py` got the
   gating right; `bc_dagger.py` -- the script the plan runs -- did not. With 78.9% empty turns the
   head collapses to bucket 0, and the floor-at-1 decode then turns every sell and buy into
   quantity 1.

10. **The quantity ladders cannot express the teacher.** `BUY_BUCKETS = [0,1,2,5]` against a measured
    `BUY_SEED CARROT 8 / WHEAT 9` in one order: `nearest()` maps both to 5, a ~40% under-buy on the
    purchase that gates planting.

## P2, and where the framing was wrong

11. **The factorisation worry was misdirected.** What is implemented is not `p(qty | bundle)` at all
    -- the qty heads read `gtok` only; the bundle gates which entries are READ, never the
    distribution. And for imitating a DETERMINISTIC teacher any state-conditioned factorisation is
    exact in principle, because the target conditional is a point mass; the 3,233 quantity vectors
    are variation across states, and the shed and bank that determine them are in the observation.
    Two genuine leaks: the planner's dawn plan is hidden state (an h12 label depends on a plan made
    at h0, so the label is multimodal given only the current observation), and in stage-3 RL a
    stochastic policy's sampled bundle cannot covary with its sampled quantities. Both second-order.
    **Do not restructure the heads for this now.**

12. **Delete the threshold calibration.** The old failure was a product of independent marginals. A
    single categorical fitted to a deterministic teacher has per-state argmax equal to the teacher's
    action regardless of the 78.9% marginal. If a replay later shows under-firing, the right form is
    ONE scalar -- fire argmax over non-empty bundles when `1 - P(empty)` clears a threshold
    calibrated to 21.1% -- not six.

13. Minor: `bundle_index_of` compares sells as flags so duplicate `(op,item)` pairs alias; stale
    measurement snapshots disagree across files (78.7%/117/5,752 vs 78.9%/197/920,320);
    `build_bc_rows.market_labels` sets `w_qty_*` even when `vocab.index` fell back to EMPTY.

## What I take from it

The bundle-not-marginals argument and the hire-count fix both survive review. Everything else needs
work, and the honest summary is that I built a design on top of code that had never run, and priced
a plan on a teacher property I never checked.
