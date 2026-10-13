# Improving from the imported bundles — triage, 2026-09-10

Written against `submission/shop0909/` and `submission/e182/`, both Apache-2.0 imports.
No experiment has been run from this document yet.
Every number below that is marked *measured* came from engine 1.32.7 on this Mac today; everything else is named as an assumption.

## What the tars already give us

Two of the three hard parts are in the archive already.

`unit_model.py` is an **exact deterministic model of own-farm semantics**, extracted from kaggle-environments 1.32.7 and pinned to the engine source hash `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e`.
Crops, animals, moves, decay. No market, no opponent.
That is a verified forward model we did not have to write and do not have to trust blindly — it names the source file it came from.

`policy.py` and `terminal_planner.py` are an **accept-tested overlay harness**: the parent router runs untouched, a deep-copied shadow state is planned against, and a proposal is taken only if it preserves every worker's cumulative deliveries, loses no sold unit, avoids shed overflow and strictly increases what is delivered and sold.
The budget is a setting, not a constant: `max_simulations`, `passes`, `proposals_per_actor`.

So the shape of any improvement is **another overlay against the same accept test**, not a new agent.
Keep `router_parent.py` byte-identical so `scripts/build_imported_submission.py` keeps verifying provenance, and so every change is a diff against a known-good artifact.

## Budget

*Measured:* the tape router plays a full 719-turn season in **2 seconds** locally, about 3 ms a turn against a 1 s per-turn limit.
E182's terminal planner adds nothing detectable at 128 simulations.
Compute is not the constraint at these window sizes.
Kaggle's box is slower than this Mac and that has not been measured.

## The three arms

### A. Widen the repair window

**Mechanism.** The tape was recorded on one board. The live board drifts — weeds spawn at 0.005 on the ladder, shops unlock on different turns — and every drifted action is a wasted turn the tape cannot see. E182 already repairs the last seven turns; the same accept test can run at more windows.

**What must be true.** There is measurable waste before step 712.

**Smallest ablation.** Instrument the unmodified parent and count, per season over 32 seeds: weed `DIG` repairs fired, `PLANT` actions the engine rejected, `WATER` onto tiles with nothing planted, sales pulled forward that found no stock.
Cost about 1 minute of wall clock. No agent change.

**Disproof.** Under about five wasted actions a season, the tape has no slack, and the seven-turn rescue's *measured* +$5 on seed 4242 is the whole story rather than an artifact of where the window sits.

### B. Replace only the market layer

**Mechanism.** Both seats price into one shared order book. The tape sells on a fixed schedule, so it sells into the hole it just dug, and it does that identically no matter what the other farm is dumping.

**What must be true.** The fixed schedule was tuned against a flow that the current field does not produce.

**Evidence.** *Measured:* between the 13 tapes the `market` list differs on 216 to 380 of 719 steps, while farmer and hand ops differ on 383 to 498 — the authors' own search moved the book nearly as much as the field. Our own earlier finding stands on the other side of the same mechanic: wool went $239 to $11 over 57 units on ladder game 99114898.

**Smallest ablation.** Keep `farmer` and `hands` verbatim from the tape; replace only `market` with a price-aware seller that holds when the quote is below a depth-dependent floor. Paired seeds, seats swapped, against the unmodified parent.
Cost about 4 minutes for 16 paired games per candidate.

**Disproof.** Mean gain at or under about $200 a season over 16 paired games means the book is not where the money is, and arm B closes.

### C. More branch points

**Mechanism.** The router branches exactly twice: step 144 picks one of 11 distinct plans from the first two unlocked shops, and step 648 forces the shared ending. Eleven continuations are selected once, on two observable bits, at day 6. `kaitofukami/238-238-known-streams-v58-minimax-closed-loop` keeps this tape family and best-responds on public state at four checkpoints instead.

**What must be true.** The best tape for a game is not knowable at day 6.

**Smallest ablation — and this is the one to run first.** For each of 16 seeds, force `state.plan` to each of the 13 tapes in turn, play the season out, and record which tape actually wins.
Compare that against what the day-6 shop-pair rule picks.
The gap is a **regret number, in dollars, that bounds every possible routing improvement** — including v58's.
Cost 13 x 16 x 2 s, about 7 minutes. It needs no new agent code, only a forced plan index.

**Disproof.** If the day-6 rule already picks the best or near-best tape on most seeds, no amount of extra checkpointing pays, and the ceiling is the tape set itself rather than the selection over it.

## Recommendation

Run **C's ablation first.** It is seven minutes, it needs no new code, and its output is a bound rather than an opinion: if regret is small, arms B and A are the only places left to look and arm C is closed before a day is spent on it. If regret is large, it says exactly how large, and v58's design becomes the obvious next import rather than a guess.

## Rules this must not break

- Select on **win rate against a field**, never on money against one opponent. The ladder is Elo; a $40k win and a $4k win score the same.
- Never gate any of this on `starter`.
- The opponents in any local field must be frozen, and must include the imported tapes themselves — they are what the current top of the ladder is tuned to beat.
