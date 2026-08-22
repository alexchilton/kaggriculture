> Read together with docs/fable_bundle_head_review_2026-08-20.md (same day, same branch). That
> review found `masks_for` has never once executed (`state.private.shed` does not exist) — which
> undercuts this doc's P1-1 analysis, since it treats the sell-mask mechanism as live and firing.
> This file's P0 order-sort bug and its other findings are independent of that and still stand.

# BC pipeline review — bundle head, quantity heads, label paths (2026-08-20)

Read-only review of branch `bundle-head` (extracted from git at the repo root's checkout; nothing was modified).
Files reviewed: `kagg/il/market_bundles.py`, `kagg/rl/jax_act.py`, `kagg/rl/jax_policy.py`, `kagg/il/bc.py`, `kagg/il/replays.py`, `scripts/build_bc_rows.py`, `scripts/fit_bc.py`, `scripts/label_games.py`, `scripts/bc_dagger.py`, `kagg/agents/neural.py`, `scripts/measure_solve_cost.py`, `scripts/measure_quantity_ladders.py`, plus `reference/kaggriculture.py` (market phase), `kagg/sim/game.py` / `jax_sim.py` (`_order_book`), the relevant tests, and the live vocabulary artifact `data/il/bundle_vocab.json` (197 bundles, rewritten today 16:49).
Line numbers refer to the `bundle-head` tree.

Two measurements were run for this review; both are quoted with their source below.

---

## P0 — `orders_from_heads` emits the bundle in sorted order, which puts every SELL LAST; the env settles slots in sequence, so decoded buys and hires spend a bank the sells have not yet filled

This is a disagreement between two of the three decoders on the one thing slot order controls.

The mechanism, from the reference:

- `reference/kaggriculture.py:544` `_process_market` walks order slots `for i in range(max_len)` and fully settles slot `i` (atomic HIRE/BUY_LAND at `:571-580`, or the lockstep drain loop) before parsing slot `i+1`.
- `_commit_unit` (`:650+`) checks `farm["money"] < price` per unit, so a BUY or HIRE in an early slot fails on a bank that a SELL in a later slot would have filled.

The three decoders:

- `kagg/sim/game.py:70-77` and `:267-279` (`_order_book`), mirrored by `kagg/sim/jax_sim.py:869-905`: canonical slot order is **SELL, BUY_SEED, BUY_PRODUCT, BUY_ANIMAL, HIRE, BUY_LAND** — "the order `heuristic`, `contrarian`, `rancher` and `search/agent` all emit".
  So the jit path (`to_sim_actions` → `_order_book`) sells first. Correct.
- `kagg/il/market_bundles.py:59` — `bundle_of` returns `tuple(sorted(pairs))`.
  Tuples sort by op string: `BUY_ANIMAL < BUY_LAND < BUY_PRODUCT < BUY_SEED < HIRE < SELL`.
- `kagg/il/market_bundles.py:300` — `orders_from_heads` iterates `vocab.bundle(index)` in that stored sorted order and appends orders in it.
  So the real-env play path (`kagg/agents/neural.py:118-123` `decode_action`) emits BUY_ANIMAL first, then BUY_LAND, BUY_PRODUCT, BUY_SEED, HIRE, and **SELL last**.

Consequence: the student replays the teacher's exact bundle, and on any turn where the buys/hires are funded by the same turn's sells, they fail in the real env while the teacher's succeeded.
`market_bundles.py:23-26` itself states the flagship case depends on ordering: "the sells in earlier order slots settle first and fund all ten hires in the same turn."
Example from the live vocab: `(BUY_ANIMAL COW, BUY_ANIMAL SHEEP, HIRE x7, SELL FERTILIZER)` — decoded, the two animals and seven hires are attempted before the fertilizer sale settles.

The failure is silent (the env returns no error for an unaffordable buy; the order just dies), and it is invisible in every sim-side evaluation, because the sim path uses the correct order.
It appears only when `neural.make_agent` plays the real `kaggle_environments` env — which is exactly the DAgger loop about to be written and the eventual gate.

Fix (no flag): iterate the bundle in the sim's canonical kind order inside `orders_from_heads` (one sort key: `{SELL:0, BUY_SEED:1, BUY_PRODUCT:2, BUY_ANIMAL:3, HIRE:4, BUY_LAND:5}`), and add a test that decodes a mixed sell+hire bundle and asserts the SELL precedes the HIRE.
`Vocabulary.to_orders` (`market_bundles.py:130-142`) has the same ordering defect (and a second one, see P2 below); it has no callers, so fold it into the same fix or delete it.

---

## P1-1 — (D) the sell mask: mechanism confirmed strict, but what it actually collides with is offer-spam, and the pairing "permissive at train, strict at play" is the worst of the four combinations

Mechanism: confirmed.
`reference/kaggriculture.py:937-940` runs `_apply_unit_action` for every unit (including DROP into the shed) and `:941` calls `_process_market` after — so a same-turn drop makes a sell fillable, while `jax_act.masks_for:86` reads `state.farm.shed` pre-turn and rules the bundle illegal.

Measured (this review, 25 Kaggle replays under `data/[0-9]*.json`, both seats, pre-turn observation via `replays.iter_turns`):

    turns with a SELL:                         10,140
    SELL orders total:                         18,915
    SELL orders with pre-turn shed == 0:        9,222  (48.75%)
      of those, same-turn DROP of that product:     0
    sell-turns containing a masked-illegal sell: 5,286 (52.13% of sell-turns)

So on Kaggle teachers, the drop-then-sell-same-hour case the mask would wrongly forbid **never occurs** — but half of all submitted SELL orders name a product the shed does not hold, because agents re-offer quotas every hour (the standing "offers are not fills" finding, now appearing in the label path).
Those orders are no-ops in the env too (`_commit_unit` returns False on an empty shed), so the mask is not costing fills.
What it costs is different and worse:

1. `scripts/fit_bc.py:66-98` trains with all-permissive masks, so the student **is** trained to emit these shed-empty sell bundles (they are in the labels — `bundle_of` reads the submitted order list, spam included).
2. At play, `masks_for` vetoes exactly those bundles, and the masked argmax in `neural.py:222-229` renormalises: the trained probability mass lands on whichever bundle ranks next.
   That next-best bundle was never selected against anything, and unlike the vetoed offer it can be a **live** trade — the student converts the teacher's no-op offer into a real sale of something else.
3. Nothing offline shows any of this, because the offline instrument (`fit_bc.py:178-199`) runs unmasked.

Caveat: the 48.75% is measured on Kaggle winners, not on the planner teacher; the planner's 920,320-turn shards are on the box.
Measure it there before deciding — one pass over the JSONL:

    python -u - <<'EOF'
    import glob, json
    tot = zero = 0
    for p in sorted(glob.glob("/home/alex/labels_r0b/*.jsonl")):
        for line in open(p):
            r = json.loads(line)
            shed = ((r["obs"].get("private") or {}).get("shed") or {})
            for o in (r["act"] or {}).get("market") or []:
                if isinstance(o, list) and o and o[0] == "SELL" and len(o) > 1:
                    tot += 1
                    zero += (shed.get(o[1], 0) <= 0)
    print("SELL orders", tot, "pre-turn shed==0:", zero, "%.2f%%" % (100*zero/max(1,tot)))
    EOF

If the planner's rate is anywhere near the Kaggle 48.75%, pick ONE consistent side and hold it everywhere:
either drop the shed-empty sell constraint from the play/DAgger mask (the env rejects those orders safely, so at play the mask buys nothing the env does not already give — this makes play match the permissive training exactly), or keep the mask and apply the same mask in the BC loss so the student is never trained toward bundles it cannot emit.
The current split — trained on them, forbidden from them — is the only combination that redistributes trained probability to unvetted bundles.
(If the mask goes, PPO can reintroduce it later as its own measured change; that is an RL concern and RL is parked.)

Note the same 48.75% number also means the **bundle labels themselves** encode offer-spam as decisions.
For imitation that is internally consistent (reproducing the offer stream reproduces the fills, state by state) — but only if play is not masked against it, which is the point above.

---

## P1-2 — `bc_dagger.py`'s in-scan loss commits both padding mistakes that `bc.py` documents and avoids

`scripts/bc_dagger.py:179-202` (`loss_fn`):

- Unit heads are weighted by `unit_live * legal` only.
  There is no `active_unit_heads` factor, so `crop`, `item` and `qty` labels are scored on **every live slot regardless of the teacher's op**.
  The teacher's `sim_actions.unit_crop` is 0 on non-PLANT slots, so the crop head is trained toward WHEAT on every FEED/MOVE/NOOP slot — the exact failure `bc.py:22-24` names ("scoring it trains every non-PLANT slot toward crop index 0, which is WHEAT") and `bc.loss_terms:318-319` weights out.
- Market quantity heads are weighted by `legal` only, and their masks are all-ones (`masks_for:98-100`).
  There is no `w_qty_*` equivalent, so `qty_sell`/`qty_buy_product`/`qty_buy_seed` are scored on all 9 (or 5) products every turn, with label 0 everywhere the bundle selected nothing (`teacher_labels:103-105` labels straight off `sim_actions.sell`, which is 0 for unselected products).
  With ~79% empty turns this trains the quantity heads toward class 0 — and the floor-at-1 decode then turns every sell and buy into quantity 1, the exact scenario `build_bc_rows.py:78-85` built the weights to prevent.

The 920k-row run goes through `fit_bc.py` → `bc.loss`, which has both weightings, so this does not corrupt the imminent run.
But `bc_dagger.py` is the in-scan half of the chain and the docstrings present it as the same objective; if it labels any future round, the round is wasted.
Fix by mirroring `bc.loss_terms`: multiply unit-head weights by `A.active_unit_heads(labels["op"])`, and derive `w_qty_*` from the label bundle's table row (`tables["sell"][labels["bundle"]] > 0` etc. — the arrays are already in scope).

---

## P1-3 — the vocabulary is not pinned to the checkpoint, and the artifact was rewritten today

Every module says the vocab "must be the SAME file everywhere" (`market_bundles.py:319-345`, `bc.py:49-52`, `neural.py:32-35`, `bc_dagger.py:256-259`), but nothing enforces it:

- `fit_bc.py:205-210` stores only `vocab_size` and `n_bundles` in the checkpoint.
- `neural.make_agent:201` loads whatever `data/il/bundle_vocab.json` currently contains and never compares it to the checkpoint — not even the size it stored.
- `data/il/bundle_vocab.json` has mtime 2026-08-20 16:49, i.e. it was rewritten today; any checkpoint trained against an earlier build now silently reinterprets every bundle index at play.
- `load_vocab`'s default path is relative (`market_bundles.py:316`), so it additionally depends on the cwd.

The file is 18 KB.
Embed the vocab list (or at minimum its SHA) in the checkpoint at fit time and have `make_agent` load the vocab **from the checkpoint**, falling back to nothing.
That closes the class of bug rather than one instance.

Related fragility: three loaders exist for the same artifact — `load_vocab` (preserves file order), and `Vocabulary.from_bundles` in `fit_bc.py:113`, `build_bc_rows.py:185` and `bc_dagger.py:260` (re-orders by `Counter.most_common`).
Today they agree only because every entry in the file is distinct (all counts tie at 1, `sorted` is stable, and EMPTY is already at index 0 — verified on the live file).
That is an accident, not a property.
Use `load_vocab` everywhere.

---

## P1-4 — the fit_bc instrument can be satisfied by a model that fires on the wrong turns, probes only training data, and watches none of the quantity heads

`scripts/fit_bc.py:178-203`:

- The probe slice is `shards[0][0:4096]` — data the model trained on this same epoch.
  Nothing held out exists anywhere in the run, so memorisation and generalisation are indistinguishable.
- `empty_rate` compares **marginal frequencies**.
  A model that emits non-empty bundles 21% of the time on the wrong 21% of turns matches the teacher's 0.789 exactly.
  The instrument as written detects only total collapse (and only above the 0.98 tripwire — a student at 0.95 empty against a teacher at 0.789 passes without comment).
- No instrument reads the quantity heads at all.
  Their collapse mode (everything to class 0, decoded as quantity 1 by the floor) is the one the row-builder's weights exist to prevent, and if the weights are ever wrong (see P1-2 for how that looks) nothing in the printout would move.

Cheap additions that make it a real gate, all computable from arrays already in the probe pass:
(1) hold out one shard from training and probe that;
(2) per-row bundle agreement on the teacher's **non-empty** rows (top-1 and top-5);
(3) mean |argmax(qty) − y_qty| over cells where `w_qty_* == 1`.

---

## P2 — real, smaller, in rough priority order

1. **`scripts/measure_quantity_ladders.py` crashes at import.**
   Lines 29-32 read `P.SELL_BUCKETS` / `P.BUY_BUCKETS`, deleted from `jax_policy.py` today.
   Loud, not silent — but it is the instrument that justified `MAX_QTY`, its numbers are cited in three docstrings and a test, and it can no longer reproduce them.
   It still has a job (the histogram and the cap-coverage numbers when the teacher changes); point `LADDERS` at nothing and keep the histogram, or fix it to report cap coverage for `MAX_QTY`.
2. **`neural.py` carries dead code that references the removed heads.**
   `_fire` (:67-84), `calibrate` (:136-168) and `MARKET_HEADS` (:133) read `heads["sell"]`, `z["y_sell"]` etc. — heads and npz fields that no longer exist; any call is a KeyError.
   `make_agent`'s own comment says they are no longer called.
   House rule applies: delete dead code, don't document it.
   Same for `bc.conditioned_term` (`bc.py:263-274`) — the trade-mode latent it serves is gone and its only caller is its own test (`tests/test_bc_replay.py:265-269`).
3. **`bundle_of` counts orders the env rejects as decisions.**
   `_parse_order` (`reference/kaggriculture.py:632-651`) returns None for SELL/BUY_* orders with `len < 3` or `qty <= 0`; `bundle_of` (`market_bundles.py:52-59`) includes them, and `Vocabulary.to_orders:139` will itself emit a quantity-less SELL that `_parse_order` throws away — directly contradicting `to_sim_fields`' rule that "a missing quantity means ONE unit" (:158-159).
   `to_orders` has no callers; delete it or make it append the explicit 1.
   In `bundle_of`, skipping orders `_parse_order` would reject aligns labels with what the env can execute.
4. **`jax_act._score` scores the `qty_*` heads for all products on every turn** (`jax_act.py:227-232`: `active.get(k)` is None for market heads).
   The file's own header says "only the heads the chosen op actually consults are scored", and the module's argument about zero-mean gradient dilution applies verbatim to quantity entries the bundle never selected.
   This is the PPO path, so it wastes variance rather than corrupting BC — but a warm-started PPO run will pay it.
   Gate them the way BC does: active = `tables[...][bundle] > 0`.
5. **`sell_table` padding rests on "no shed ever holds all nine"** (`market_bundles.py:262-264`).
   Shed capacity is 100 across 12 items; holding one of each of the 9 products late-season is entirely possible, at which point the padding rows become legal.
   Consequence is graceful — a padding index decodes through all-zero table rows as the empty bundle, and `bundle_index_of` maps its pattern back to 0 — so this is a wart, not a wound.
   A padding row marked illegal unconditionally (e.g. a dedicated always-false column in the mask) would not depend on a game-state assumption.
6. **`replays.encode_action` re-loads and re-parses the vocab JSON on every call** (`replays.py:129`).
   Correct but quadratic-feeling on a 920k-row build through `bc.build_rows`; hoist it.
7. **Smoothing note (C).**
   `--smooth 0.02` through `head_term`'s legal-mean formulation puts `s/n ≈ 7.8e-5` per class on the 256-way head, bounding the label-vs-rest logit gap at ~9.4 nats (~8.1 for the 64-way).
   The parked BC track's absorbing-state gap was 9.7 nats — so at these widths the smoothing is a mild regulariser, not the gap-bound the `bc.py` docstring (point 3) credits it as.
   Not wrong, but do not rely on it to prevent that disease; the argmax-mix instrument is the real defence.
8. **Stale docstrings that will misdirect the next reader**: `market_bundles.py:14-16` still sizes the design on the 117-bundle four-game pilot and recommends a 128-class head against the shipped 197/256; `jax_policy.py:26-30` still describes drawing `trade` first and points at `condition_on_trade`, which does not exist; `jax_act.evaluate`'s docstring (:271-279) still scores `p(trade)`; `bc.py`'s module docstring point 1 still describes cloning under every trade mode.
   After the P0/P1 fixes these are the highest-value cheap edits, because this codebase's docstrings are load-bearing.

---

## Checks that came back clean (briefly, so they are not re-litigated)

- **Quantity round-trip**: label paths (`MB.clamp_qty`, `replays.py:100-106`, `build_bc_rows.py:104-110`) and the in-scan `_exact_qty` (`bc_dagger.py:74-81`) agree: clamp to 63, never wrap; all three decoders floor a selected product at 1; `tests/test_a_traded_quantity_survives_the_round_trip.py` pins the Python path.
- **Hire as a count**: consistent everywhere — bundle multiset in both label paths, count column in `tables`, count compare in `bundle_index_of`, one env order per hire in `orders_from_heads`, `n` unit candidates in both `_order_book`s.
- **The live vocabulary** (measured this review): 197 bundles, EMPTY at index 0, no bundle exceeds the 10-order cap, no repeated non-HIRE pair, and zero pattern-aliased groups — so `bundle_index_of`'s binarised pattern matching and the Python `Vocabulary.index` agree on every current entry.
  (They would diverge if a repeated non-HIRE pair ever entered the vocab; `tests/test_a_bundle_becomes_the_action_fields_the_sim_reads.py:68`'s `from_sim_fields` round-trip would start failing at that point, which is an acceptable tripwire.)
- **`fit_bc`'s permissive masks** are the right call for teacher-state BC (the teacher's action is legal by construction) — the problem is the asymmetry with play, covered in P1-1, not the permissiveness itself.
- **`bc.loss` weighting** (C): `w_qty_*` restricts quantity training to bundle-selected products, `active_unit_heads` restricts argument heads to the ops that read them, per-head averaging stops slot count deciding importance, and the bundle head is trained on every turn including empty ones.
  Correct as specified.
- **`label_games.obs_snapshot`** stores everything `adapter.state_from_obs` reads (checked key by key; the `"shops"` key it stores is unused, and shop unlocks are deliberately absent from the rebuilt state on both the training and the play path, so no skew).
- **`measure_solve_cost.py`** now patches the names the bundle actually reads (`sys.modules["kagg.search.cover"]`), prints route counts on both arms, and hard-stops on a zero-route shipped arm — the two prior invalid-probe modes are closed.
- **`masks_for` is now executed by tests** (`tests/test_the_policy_can_take_a_turn.py` calls it five times on a real state, including the padding-illegal and empty-shed cases), closing the `state.private.shed` class of failure.
- **Shed contents are in the observation** (`jax_obs.py:314`, `shed / 50` capped at 3.0), so the quantity heads have the signal they need.

## (E) What is missing that would make the result uninterpretable

1. **The real-env gate** (known): nothing plays `neural.make_agent` through `kaggle_environments` against the arena pool.
   `scripts/play_checkpoint.py` is in-sim only, so it can never surface the P0 ordering skew, adapter drift, or anything else that lives between `jax_sim` and the reference.
   The gate should report W/D/L (not a rate — draws dominate the failure modes here) plus the bank curve, and select on win rate per the standing rule.
2. **A per-day op-for-op agreement report against the teacher** on teacher states (the planner equivalent of the d0-d6 tape grid): op mix per day, bundle agreement per day, realised-fill comparison via shed/money deltas rather than offer sums.
3. **A three-decoder agreement test.**
   No test compares `orders_from_heads`, `to_sim_actions` and `to_sim_fields` on the same drawn heads across the whole vocabulary.
   One property test (for every vocab index and a random qty vector: decode via all three, push through `_order_book`/`_parse_order` semantics, assert identical fills) would have caught the P0 and will catch the next divergence.
4. **Vocab identity enforcement** (P1-3) — without it, a DAgger loop that rebuilds the vocab mid-chain silently re-indexes the student's whole market policy.
5. **A held-out shard and per-row/quantity instruments in fit_bc** (P1-4) — without them the 920k-row run produces numbers that cannot distinguish memorised from learned, or right-rate-wrong-turns from right.
6. **`dagger_planner.py`** (known, in progress): note when writing it that the planner labels arrive as order lists, so the Python `Vocabulary.index` path applies (not `bundle_index_of`), and OOV teacher bundles will be labelled EMPTY (`Vocabulary.index:111-113`) — log the OOV rate per round; if student states drive the planner into bundles the 197-entry vocab lacks, those turns are silently taught as "do nothing".

## What I did NOT check

- `adapter.state_from_obs`'s tile reconstruction (`_tile_arrays`) and `jax_obs.encode`'s feature semantics beyond the shed feature — taken on trust from the parity suite.
- `jax_masks.unit_op_mask` / `unit_crop_mask` / `unit_item_mask` correctness.
- `kagg/rl/commit.py` interaction with the op head beyond widths.
- float16 storage precision in `build_bc_rows` (tiles/units/glob stored as float16, trained as float32).
- Whether the planner teacher actually relies on same-turn sell→hire funding on specific days (the P0 argument is from the reference's settlement semantics plus the module's own docstring; the per-turn frequency is measurable on the label shards with the bank-vs-cost check but was not run here).
- Anything about the submission bundle itself, `train_jax_rl.py`, or the RL loss beyond `_score`.
- The 48.75% measurement is 25 of ~160 local Kaggle replays, both seats; not resampled.
