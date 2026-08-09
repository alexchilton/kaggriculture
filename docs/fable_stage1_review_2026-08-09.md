# Stage-1 review: the $2,484 is a decode veto, not a pricing error

Fable, 2026-08-09.
Requested: is the `revenue_rate` cap the binding problem, why land lands on days 11/15,
should stage 1 exist, and what closes the ~2,000-point gap.
Everything below was verified against the actual saved artifact
(`data/chain_search_scheduled/best_beam_genome.npz`, money $2,484, land days 11/15 — the exact run in question)
and `data/logs/run_scheduler_v7.log`.
Installed env is now 1.32.6 (`kg.__version__` checked), so that landmine is closed.

## The headline: (b) is not a scheduling bug, it is a decode veto, and it is measured

Decoding the saved genome:

    reachable_quadrants(g, 12) = 0
    land_schedule(g, 12)       = [11, 15]
    decode -> used 7, skipped 5

The five skipped chains are **every chain that needs land**: the melon block, all three strawberry
blocks, and the fourth wheat block — the entire revenue expansion.
What actually plays is 2 cow pens, 2 sheep pens, and 12 wheat tiles in NW.
That farm banks $2,484 and wins 0/16. The schedule was never the thing being scored.

Worse: `decode` (`chains.py:687-691`) emits the `buy_land` orders from `land_schedule`
**unconditionally**, while `reachable_quadrants` gates only the *chains*.
So the tape spends $3,000 on parcels on days 11 and 15 and then refuses every chain that would
have used them. Ground with no crop on it, bought — the exact failure the module's own docstring
calls "worse than no ground". That is a straight bug independent of everything else.

### Why the gate says 0 parcels: three cash models that disagree by 10x

- `scheduler.schedule()` (line 241-245) walks a bank that charges seed/animals/feed but
  **no crew at all** — `daily_burn` is feed only, and hires never appear. Its day-11 bank for this
  plan: ~$742-$1,963 depending on reserve.
- `chains.cash_curve()` (line 591-593) charges the **full crew from day 0** —
  `hc[:max_unit].sum()` = $232/day for 11 hands here — even though half the slots start on days
  9-15 and no hand is needed before its chain runs. Its curve for the same genome:
  `[1823, 741, -366, ..., 188, 108, 76, ...]` — **$108 on day 11**.
- The jax sim is the truth, in between.

`reachable_quadrants` breaks at `spent + follow_on > curve[day]` (`chains.py:480`), i.e. it needs
~$1,040 on day 11 and sees $108, so parcel 0 is refused and everything behind it dies.
The comment at `chains.py:458` — "Same rule as `scheduler.schedule`, so the gate and the scheduler
agree" — is false in the one way that matters: same *rule*, different *bank*.
The optimistic model proposes days; the pessimistic model holds a veto; the plan is guaranteed to
be gutted whenever they straddle the affordability line, which is exactly where an aggressive
plan lives.

### Why days 11/15 and not the tape's 5/9/11

Secondary, but answerable. Inside `schedule()`:

1. **The inflow is a trickle, not a harvest** (line 242-244). `revenue_rate` spreads a
   drain-capped, price-halved, share-halved season total evenly over 30 days: a wheat block
   credits $140/day from day ~5. Real wheat cash is chunky — the leaders are buying land on
   day 5 out of day-3-4 harvests the trickle model cannot represent.
2. **Chains before land** (lines 255-265 before 276-287): every affordable pending chain drains
   the bank to below `cost + reserve` *before* land is considered each day, so the bank pins near
   `reserve` and land waits for the trickle to accumulate `price + follow_on + reserve` in one
   day's residual. With the v7 mix (3 cow + 2 sheep groups up front, $1,200-1,700 each) that
   crossing happens on day 11-12 for parcel 0 and 15-20 for parcel 1.
3. `reserve` is double-counted: chain placement already holds it back, and the land condition
   adds it again.

I re-ran `schedule()` on the reproduced mix: reserves 0/300/800/1500 give parcel days
7/11, 8/11, 5/13, 7/14. The days move ±4 with an arbitrary dial. The scheduler does not know
when money arrives, so the land day is noise around the trickle-crossing, not a decision.

## Answer to (1): no, the cap fix is not the binding problem

The cap is real, your measurements are right, and the flat melon estimate is exactly as bad as
`test_the_planner_prices_volume.py` says. But fix it and the pipeline still scores $2,484-class
results, because the decode veto guts the plan downstream of any pricing. Order of binding:

1. decode vetoes the plan (`reachable_quadrants` vs `schedule()` disagreement) — fatal today;
2. decode buys land for chains it refuses — pays for the veto twice;
3. the trickle inflow mistimes land by ±5 days;
4. the cap flattens the melon/milk/wool estimates — your (a).

And a marginal-revenue curve with a contest term is **still a proxy**, which is the deeper
objection: `run_scheduler.py` already runs the full jitted jax sim per reserve arm to *score* the
result. The sim is cheap enough to be the objective. Every hand cash model in this pipeline
(`revenue_rate`, `schedule()`'s bank, `cash_curve`, `_bank_estimate`) has a documented wrong
answer in its own comments — the file is a museum of them. Do not build a fifth model.
If stage 1 survives at all, replace "propose days from a cash model" with coordinate descent on
`start_day`/`land_day` genes scored directly by the sim. The scheduler's only irreplaceable output
is an *ordering* heuristic, and payback order survives as a search initialisation.

## Answer to (3): stage 1 in its current role should not exist

Blunt version: stage 1 optimises a proxy (`revenue_rate`) inside a proxy (genome → decode, with
decode holding an independent veto) against a phantom field (`heuristic,rancher,homestead,carrot`
tapes — a pool that predates the cluster data and contains zero of the three real archetypes).
Three layers of indirection, and the memory note — optimise the artifact, not a proxy — names
this exact shape. It has never shipped and its best output loses 16/16 to its own sibling.

What the cluster doc changes: **the floor of the top five is a public agent we have locally.**
Three of five run kaitofukami v23 byte-identical at 3,117-3,131, and we verified v23 runs locally.
We are at 1,123.5. The highest-EV sequence is therefore:

1. **Put v23 in the arena as the opponent.** Every number in this project is currently measured
   against a field that no longer exists. Our shipped agent vs v23, 16+ seeds, win rate — that one
   measurement reframes everything and costs an afternoon.
2. **Get into the v23 band first.** Hand-build the opening from the cluster signatures (or study
   v23's own action stream — it is public and deterministic). This is not "give up on search";
   it is the same move the field made, and it is worth ~2,000 points before any originality.
3. **Then search for the counter, which is where the sim is a real edge.** Seb is rank 1 *while
   banking the least money* because he beats the v23 cluster consistently. Beating a known, fixed,
   public opponent is precisely what an exact simulator plus search is for — score candidate
   openings by wins vs v23 in the jax sim, terminal win/loss, exactly as CLAUDE.md already
   prescribes. In that loop no revenue proxy exists to be wrong.

So: keep the chains/decode/sim machinery — it is the asset. Retire the
scheduler-as-cash-simulator and the drain-capped revenue model. Stage 1's question ("what mix,
what days") stays; its answer method (hand cash models feeding a genome the decoder second-guesses)
goes.

## (4) Everything else found, in one pass

- **`decode` buys land its own gate refused** (`chains.py:687-691` vs `674`). Fix regardless of
  any other decision: land orders must be gated by the same affordability the chains are.
- **`to_genome` silently truncates** (`scheduler.py:319`): v7 scheduled 14 chains into 12 slots;
  the last two strawberry blocks vanished without a count. Skips are counted everywhere else on
  principle; this one isn't.
- **The per-chain drain cap is not shared.** `revenue_rate` applies `min(units, DRAIN*share)` per
  *chain*, so four melon chains "sell" 4x15 units into a 30-unit drain. The model is not even
  internally consistent about the drain it believes in.
- **`OPPONENT_SHARE = 0.5` vs `--share 1.0`**: run_scheduler's mix deliberately un-halves the
  drain (with a comment explaining why halving is wrong) while `revenue_rate` still halves it two
  calls later. The mix and the cash model disagree about the market size by 2x.
- **CARE does not exist in the model.** HealthStone (rank 2) is built on CARE compounding from
  sheep (+3/yield at interval 3). No term in `revenue_rate`, `cash_curve`, or the mix targets
  knows CARE exists, so no stage-1 variant can ever find or price the rank-2 strategy. Same
  pattern as the animals verdict: ask what the code cannot express before trusting its negative.
- **`expected_first_demand_day` draws shops without replacement** (`scheduler.py:99`); 1.32.6
  draws with replacement (per chains.py's own 2026-08-08 comment), so payback ordering is
  computed on 1.32.2 unlock statistics. Minor next to the above, noted for when payback order
  is kept as an initialiser.
- **The opponent pool is the pre-cluster world.** Any stage-1 "wins" number, even after all fixes,
  is a statement about four of our own old tapes. Selecting on it repeats the frozen-opponents /
  wrong-field lesson already in CLAUDE.md.

## What I did not do

No files modified other than this one. No long jobs — the two `schedule()` traces and the genome
decode each ran in seconds. The 3-of-5-red test file is correct about the shape it pins; I would
hold it until the decision above is made, because if the cash models are retired in favour of
sim-scored day search, `revenue_rate` is deleted rather than fixed and the tests pin a corpse.
