# Fable review: where the money is, 2026-08-24

Verbatim, saved before relaying. Prompt was `docs/where_we_lose_2026-08-24.md` plus the six-loss
measurements. Fable ran read-only in an isolated worktree.

---

One correction to the brief before anything else: point 6 is stale — `kagg/arena/pool.py` already contains a withholding opponent (`carrot_hinge`, added 2026-08-24, `hold_days: 6`, in `COMPETITIVE`, now 10 members). The 94.4% saturation claim was true of the 9-member pool; gate numbers before/after today are not comparable, and the pool file says so itself.

## Strongest disagreement: the realized-price table does not clear the sell cadence, and "terminal inventory" is a corollary, not the frame

Point 5 says "our realized price per unit is FINE (96-111%), so we lose on WHAT we hold and WHEN we release, not on execution." The 96-111% metric is computed on **the same book, both seats** — it is controlled for exactly the variable your cadence destroys. When you flood milk to $1 by d13, the opponent's milk sales also clear near $1, and the ratio reads ~100% while both seats got paid nothing. A per-transaction parity metric is structurally blind to book-level destruction that both seats share. So the table proves execution parity; it proves nothing about cadence, and cadence is what sets the book. This is the same class of error as the win-rate-that-was-all-draws lesson in CLAUDE.md: an aggregate whose reference point moves with the thing being measured.

The right frame, and it is exact, not a metaphor: **price is a pure function of town inventory** (`market_price`, `reference/kaggriculture.py:192-207`), inventory starts at I0=10000 for every product (`_new_market`, line 178), and only three things move it — your sales (+1/unit), their sales (+1/unit), and a deterministic drain (`_town_consume`, lines 728-749: 6 ticks/day per shop instance, x2 for single-product shops, +1/day town center). So each product has a **season supply budget**: cumulative sales beyond cumulative drain push inventory above I0 and earn the floor; sales withheld below the budget let the deficit grow and compound. Terminal inventory accumulation is just the disciplined way to spend the unspent part of that budget. It is not a separate endgame trick, and framing it as one leads to endgame-only fixes (like `e2500_close.py`) that, as section 4 of your own doc says, cannot reach it.

## (a) The error is earlier, and it is cadence + herd sizing, not "animals produce into a dead book"

Producing is not the sin; selling past the budget is, and it happens by ~d13. Milk's above-curve is linear with `above_target 1.6`, T=122: price = 160 − 2.098·(inv − I0), which hits $1 at a surplus of ~76 units. Milk at $1 from d13 means that by d13 we had sold ~76 units more than the town had drained. Everything after that is consequence:

- Each further milk sale earns $1-5. The counterfactual — selling at the drain rate (two milk shops ≈ 13/day) — clears the same daily flow at ~$160. That is the $11k gap in the standing milk-flooring note, and it is a cadence number, not an endgame number.
- Once the book is floored AND remaining supply exceeds remaining drain, FEED/CARE/haul turns for that pen are pure waste — but that is the *third-order* cost. Fixing the crew turns without fixing the cadence just wastes fewer turns servicing a book you still killed.
- The machinery for the cadence fix already exists and is good: `reservation_units` in `kagg/search/schedule_agent.py:3489` computes exactly the right quantity (`N(L) = deficit gap + remaining drain`), and `HOLD_A_FLOORED_BOOK` (line 3545) holds when `d_rem >= supply`. The recorded losses were played by artifacts that either predate this or have it "barely tuned" per your own doc. The question is not what rule to invent; it is whether the shipped `ead81e2` lineage actually runs this rule with parameters that bind before d13. That is a grep-and-replay question, not a design question.

The herd-sizing half: milk season drain is ~300-400 units in a two-shop town; a 4-6 cow herd at interval 2 out-produces that. The pool's `cow_heavy` opponent and the "cow COUNT is causal" memory both point the same way. Sizing the herd to the drain schedule (observable from `town.unlocked_shops` at buy time) is the upstream fix; the stop rule is the downstream guard.

So: argue for "earlier." The terminal-inventory play is what you do with the withheld budget — it falls out of the cadence frame for free.

## (b) The two held-more-and-lost games: two different failures, neither contradicts the frame

First, a metric problem that affects both rows: "terminal inventory priced at the closing book" is endogenous. The closing book is *post-dump* — their 58-unit wheat sale in 98499540 depressed the very quote your unsold wheat is valued at, and your unsold stock is valued at a price it never attempted to realize. Held-value comparisons at closing prices systematically flatter the holder who didn't sell. Price both sheds at the *start-of-d29* book, or better, skip valuation and decompose flows.

- **98499540** (−1,940, held $4,008 vs $2,666, they out-banked us $6,954 to $5,520 on d29): their d29 bank exceeds their held value by ~$4,300. That money is not inventory — it is **d29 harvest**: crops ripening on the last day, plus that day's animal products, sold same-day. Your section-3 "reachable standing" number ($380-1,566) counts what was ripe *by d28*; a wheat tile ripening d29 is invisible to it. Measure: run `scripts/what_the_last_two_days_banked.py` on **their** seat and split their d29 fills into held-at-d29h0 stock vs d29-harvested stock. If the harvested share is ~$4k, the failure is ours in d24-d26 planting (nothing timed to ripen into the close), which is your own untested hypothesis #1 in the handoff doc.
- **98501831** (−6,070, gone by d28, gap grew +3,929@d20 → +6,384@d28): different failure, and note they won while carrying 31 milk worth $31 — they made the flooding mistake too and beat us anyway, which says the margin came from production or spend, not the market. Measure three cumulative curves per seat, d0-d28: banked-by-product per day (fills from shed/money deltas, never the action stream), land/hire/animal spend timing, and — the one I would bet on — **crew-turns/day spent servicing products quoted under $20** (FEED, CARE, pen harvests, hauls of floored goods). If we spent 15-25 turns/day of a ~100-turn crew budget on $1 milk logistics from d19 while they spent those turns watering wheat, that is the $2,455 of d20-d28 bleed, and it is the third-order cost from (a) made visible. SPECULATION until the turn count is read.

Also: 4 of the 6 margins are under $3,560. Section 3 dismisses board clearing as "noise" against the $29,384 game, but $380-1,566 reachable-standing plus the d29 four-leg conversion slack is decisive-sized for the other four. The dismissal used the wrong denominator.

## (c) The hinge does not self-destruct; it self-limits, and holding is weakly dominant — but the gate must be on the deficit, not the opponent

The numbers, from `market_price` with CARROT (base 35, T 450, hinge, target 1.00): the $498 close implies deficit D ≈ 975, u ≈ 2.17. Now dump both sheds — 148 units combined: u falls to 1.84, price to ~$297, average over the walk ~$390. Each seat still banks ~$28k. The deficit pool the drain built over 30 days is large relative to what two 100-cap sheds can throw at it. That is why "they cleared 72 units without collapsing it" — and it is why the mirror does not destroy the play.

Payoff structure in a genuine carrot town (D projected well above T):

- (hold, not): holder wins by ~$30k. Observed, game 98495047.
- (hold, hold): both bank ~$25-30k extra; per-unit lockstep (`_process_market`, line 590: both players quoted at the same pre-commit inventory each unit) splits the walk-down fairly *within* a turn, so the money margin between the seats ≈ 0 and the game is decided elsewhere. One real asymmetry: across turns, earlier d29 sales catch the deeper deficit, so get stock to the shed and start selling at the first d29 hour the four legs allow, not h21.
- (not, not): also decided elsewhere.

So against a field this is not a coin flip: holding never costs you the relative game, and wins it outright against the non-holding majority. The cost side is small — carrot seed $20, ripe in 3 days, ~4 units/tile; even the marginal post-dump price ($297) is ~$1,200/tile against a d26-planted wheat tile's ~$228.

The failure mode is not the mirror, it is **misjudging D**. If the town is not a carrot town (your four drain-2/3 games), the dump crosses the knee: at D=400, u=0.89, price ~$66, and carrot roughly ties late wheat per tile. So the principled gate replaces both `CARROT_DRAIN_MIN` and `CARROT_OPP_MAX` with one computable quantity — everything needed is in shared obs (`market.inventory`, `town.unlocked_shops`, opponent's visible carrot tiles):

```
u_residual = (D_projected_at_d29 − our_planned_units − 4·opp_carrot_tiles) / 450
fire iff u_residual > ~1.3
```

This *inverts* `CARROT_OPP_MAX` exactly where your one game says it is wrong (D≈975: subtracting their ~72 units leaves u≈2.0 — fire) and *keeps* its protective content where it was right (small D: their tiles push you under the knee — stand down). Tune-vs-invert-vs-delete answer: **delete both constants, replace with the deficit projection.** The convincing result: on replays it must fire on 98495047 and stand down on all four drain-2/3 games, which the current gate pair also does — the discriminating test is a synthetic mid-drain town (drain 5-7, opponent holding 8-12 tiles), which `jax_sim` plus the new `carrot_hinge` pool member can generate.

Same instrument, unpriced so far: EGG is a hinge product (target 0.40, T=332), geese are cheap ($300, egg/day from d4), and we sell zero eggs. A two-bakery town drains ~13-19 eggs/day; a season of that is a deficit worth $120-300/egg at the close. The goose verdict has been invalidated once already (SELLABLE bug). Not the first experiment, but the 0% row in the realized-price table is a live lead, and it is the same lead.

## (d) The single experiment: drain-budget cadence + deficit-gated terminal dump, graded on flipped games

Build one arm on the `ead81e2` lineage combining the two halves of the frame:

1. Mid-season: enforce the reservation/stop rule so no product's inventory is pushed above I0 (verify the shipped constants actually bind by d10-d13 — the recorded losses say the shipped artifact's did not).
2. Endgame: the deficit-projection gate above for hinge products, dump sized to shed cap, d29 sales starting at the earliest four-leg-feasible hour.

Measure by **paired tape replay over the full downloaded corpus** — all ~54 losses plus the won games you hold, opponent's recorded actions verbatim, game's own seed (the `scripts/rematch_the_losses.py` / `scripts/the_close_on_the_real_book.py` method; the opponent's recorded sells still execute, so their supply stays in the book). The metric is **flipped games**, not mean money — that is the Elo-aligned statistic, and 11 of 54 losses sit inside $2,100 where this lever is exactly the right size. 16-core box, no GPU, existing harnesses.

Results that would change minds, stated in advance:

- **Ship it if:** 98495047 gains >= $15k; at least 3 of the 11 narrow losses flip; no more than 1 formerly-won replay flips the other way.
- **My model is wrong if:** on games where the carrot gate fires, the realized dump averages under ~3x base — that means the deficit projection (or the opponent-units subtraction) is miscalibrated, and the hinge play is not as forgiving as the closed-form says.
- **The cadence half is a null if:** holding milk/wool to the drain rate does not move the paired margin on the five floored-book games — that would mean the flooding is a symptom of something upstream (herd size alone), not a cadence defect, and the fix moves to the buy decision.

One cheap companion measurement, worth an hour before believing any of it generalizes: scan *all* downloaded games (not the selected losses) for how much of each opponent's season revenue lands on d28-d29. That is the base rate of withholders in the field — it tells you how many ladder games the (hold, not) branch of the payoff matrix actually describes, which is the number the Elo argument rests on. The losses cannot give you that; they are selected.

---

Files referenced: `reference/kaggriculture.py` (pricing 192-207, market init 178-185, drain 728-749, lockstep 544-625), `kagg/search/schedule_agent.py` (reservation_units 3489, HOLD_A_FLOORED_BOOK 3545, sell block ~4980-5115), `kagg/arena/pool.py` (carrot_hinge 90-92, COMPETITIVE 100-103), and the three briefs in `docs/`.
