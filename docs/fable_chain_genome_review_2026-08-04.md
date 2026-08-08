# Fable: chain-genome and search design review (2026-08-04)

Fable read `reference/kaggriculture.py` in full (1054 lines), `kagg/search/routines.py`,
`tests/test_routines.py` and `docs/kimi_take_chain_optimisation_2026-08-04.md`.
Saved before relaying, per standing instruction.
Every claim below is anchored to a reference line number; the ones marked UNVERIFIED are Fable's
reading that we have not yet independently confirmed.

## 1. Genome shape: chain-tuple, but the search is day-indexed

Kimi's `[(chain_id, start_day, params), ...]` decodes more cleanly than a 30-slot-per-day genome,
for a reason neither of us stated: `ranch()` already writes ops for every day from `start_day` to
day 29, so a per-day genome would re-express "still feeding the cow" as content in 29 separate
slots. Mutation and crossover would then have to know those slots belong together anyway.
The chain-tuple is the natural indivisible gene.

But genome shape is not the search algorithm. The Markov structure lives at the **day boundary**,
not in the tuple list. So: genome = set of chain instances; search = day-indexed beam/DP that at
each day asks only "which new chains can legally start today, given the *real* simulator state".
Use the real simulator, not Kimi's virtual resource-budget estimate (his §5A).

    ChainInstance = {chain_type, start_day, unit_id, tile, params}
    genome = [ChainInstance, ...]        # unordered; sorted by start_day at decode time

    beam = [initial_state]
    for day in range(30):
        candidates = []
        for node in beam:
            for choice in legal_new_chains(node.sim_state, day, library):   # incl. "nothing new"
                new_state = simulate_one_day(node.sim_state, decode_day(node.genome + [choice]))
                candidates.append(Node(new_state, node.genome + [choice]))
        beam = diversity_top_k(candidates, value_fn, K)

## 2. It really is DP — the Markov claim holds, with one gap in our state list

Fable verified line-by-line against `_end_of_day` (ref 829-851) what survives the dawn reset:
`money`, `tiles` (crops, animals, weeds, structures and all their counters), `unlocked_quadrants`,
`private["shed"]`, **`private["seeds"]` — which we omitted from our own state vector**, the shared
`market`, and `town["unlocked_shops"]`.
Wiped: farmer/hand positions, the hands list, `hires_today`.
Town-shop unlock and weed spawn are RNG-driven by `(seed, day)` only (ref 838-840, 855-859), so they
are exogenous and hide no state.

**Do not look for an admissible heuristic — there isn't one.**
Rank beam nodes by a **short-horizon rollout** (H = 7-10 days, not all 30; full-horizon per node per
day is O(days^2) and unnecessary) under a fixed auto-pilot, in the same vmapped sim.
That prices the option value of "$500 cash + one live COW" against "$4,000 cash + nothing", because
the rollout actually cashes the cow in.
Note it stays a dense *search* proxy only: final selection is still win-rate against the pool, per
`CLAUDE.md`.

Two named failure modes:

- **Beam collapse on land timing.** Top-K by rollout value converges every node onto one
  land-purchase hypothesis within a few iterations, because short-horizon rollouts undervalue
  saving. Bucket the beam by land-purchase-day vector and animal-portfolio signature before pruning.
- **Two-stage filter.** Cut candidates on raw money (cheap) to ~3K, then spend rollout budget only
  on those.

## 3. Land funding is a decoder bug, not a search problem — the strongest finding

Two mechanics make this decisive (UNVERIFIED by us, to check next):

1. `_do_buy_land` (ref 680-693) silently no-ops on insufficient money, with **no side effect at all**
   on failure. Attempting costs nothing.
2. Atomic orders (`HIRE`, `BUY_LAND`) at queue position *i* resolve **before** the per-unit lockstep
   buy/sell at that same position (ref 546-556 runs before 558-602). So `BUY_LAND` at order-slot 0
   gets first claim on our own cash that turn, ahead of anything else queued that day.

Therefore: **emit `["BUY_LAND"]` at order-slot 0 on every single turn, from turn 0, unconditionally,
until all three parcels are bought.**
It fires the instant we cross the threshold and can never be forgotten.
This is strictly stronger than Kimi's Pareto-frontier variant, which *tolerates* the failure mode;
the decoder change *removes* it — the same move `routines.py` already made for the animal chain,
applied to land.

## 4. A measurable test for whether the library has capped the ceiling

Better than a gut check on "shape vs policy": mine 5-10 day-level blocks from real top-player
replays and check whether each is expressible as *some* combination of existing chains at *some*
parameters.
Any block that is not — simultaneous multi-tile crop rotation, wheat arbitrage via
`BUY_PRODUCT`/`SELL` round-trips, hire-wave-then-scatter-to-crops — is a **measured** coverage gap.
Do this before spending compute on the beam search; it tells us which chains to add first.

Where `ranch()` currently encodes policy rather than mechanics: the fixed daily sell cadence
(`sell[d+6] += max_held`), and the fact that animal chains are the *only* chains that exist. Given
that leaders draw ~83% of revenue from converting bought wheat into animal products, a library that
is 100% ranch caps the ceiling by omission rather than by being too prescriptive.

## 5. Adversarial findings — things we mis-read or missed

**(a) A hand that spawns on a LOCKED tile is paralysed for the whole day.**
`_spawn_hand` (ref 508-516) picks the least-occupied shed-access tile with no lock check, so the
first hand every day lands on `(5,4)` = NE.
`_apply_unit_action` returns early when `tile == "LOCKED"` (ref 320-324), which guards
DROP/PICKUP/PLACE/FEED/CARE.
So the parcel must be bought **before that hand's first working day** or the day is void.
Hand-hire order and `LAND_ORDER` are pre-aligned by the game's own design:
`(4,4) -> NE -> SW -> SE`.
A second, independent mechanism reinforcing land timing: land does not merely unlock tiles, it
unlocks a hired unit's ability to act at all.

**(b) `ranch()` never collects fertilizer, so our measured numbers are a LOWER bound.**
Every surviving animal tile gets `fertilizer_available = True` at every day-end unconditionally
(ref 800), collectible with `COLLECT_FERTILIZER` (ref 490-497) from the same tile within the same
turn budget as FEED/CARE.
So +$8,119 (COW) / +$6,510 (SHEEP) / +$1,604 (GOOSE) understate the chain before any search runs.
Fix: add `COLLECT_FERTILIZER` and either sell the FERTILIZER or route it to a crop tile via
`FERTILIZE` for the yield window (ref 373-386).

**(c) Shed capacity is GLOBAL — 100 units total across every product and animal combined**
(`_new_private` ref 154-160; `_drop_inventories_to_shed` ref 812-826 discards overflow silently, no
error).
This caps any hoard-and-sell-late strategy, which is otherwise incentivised by a structural fact we
had not flagged: `_town_consume` (ref 696-718) drains market inventory on an **accelerating**
schedule — more shops unlock over the season, and the town-centre multiplier steps up at **day 10
and day 20** (`TOWN_CENTER_DEMAND_SCHEDULE`, ref 103).
So prices drift structurally upward late-season *independently of the opponent*.
This partially explains the MILK climb $212 -> $333 we attributed solely to a do-nothing opponent.

**(d) Hiring scales crop coverage, and that is probably a bigger lever than a fifth animal.**
Ranch pens are hard-capped at 4 by the shed-tile geometry, but crop tiles are not — up to 100 once
land is bought — and the Fibonacci ladder resets daily, so an 8-hand crew costs about $1,600 across
the season.
The biggest unexploited lever is likely "many cheap hands routed to crop tiles across all four
quadrants", and we have no crop routine to test it with.

## What we act on, in order

1. Verify (a), (b), (c) and the slot-0 ordering claim in §3 against the reference ourselves.
2. Mine the 168 episode JSONs for the *plan-level* build order actually used by winning seats — land
   days, animal portfolio, tile roles, hire counts per day, sell cadence. This is Alex's direction:
   we know what works, so read it off rather than searching for it. It doubles as §4's coverage test.
3. Add `COLLECT_FERTILIZER` to `ranch()` and re-measure.
4. Add the unconditional slot-0 `BUY_LAND` standing order to the decoder.
5. Build a crop routine before any beam search, since its absence is the largest coverage gap.
