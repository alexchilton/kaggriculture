# Is this a market game? Kimi's framing, and what the measurements say

Kimi (K2.6 Instant) reviewed the project on 2026-08-05 and argued that two independent boards sharing
one market make this "a market game with a farming backend" — that the spatial chains are mere resource
extraction and the real competition is price discovery.
It proposed three regimes and three experiments.
This file records the argument and then answers it with measurements, because two of the three
experiments turned out to be already answerable from data on disk.

## Kimi's argument, preserved

The only coupling between the two players is the market clearing price, making this structurally like
two oil producers sharing a pipeline.
So the question is not "how do I farm better?" but "how does my opponent's trading affect my prices,
and can I exploit it?"

| Regime | Description | Strategic implication |
|---|---|---|
| A. Thin market, high impact | Selling 9 wheat crashes the price for both | Market timing is everything; sell before the opponent |
| B. Thick market, low impact | Individual trades barely move price | Boards effectively independent; open-loop is near-optimal |
| C. Asymmetric impact | One player's trades move price more | The leader can manipulate prices to starve the opponent |

Its proposed tests:

1. **Sell-timing sensitivity** — shift our sell of product X one day earlier, measure the bank delta.
   More than ~2% means thin market.
2. **Manipulation** — dump 9 units of everything on day 10 and see whether the *opponent's* bank drops.
3. **Cross-correlation of sell days** — if every top player sells wheat on day 28, the market crashes
   that day and a script selling on day 27 gets a better price. A classic tragedy of the commons.

On method, Kimi's answer to "is it RL?" was: no.
Exact dynamics plus known opponent scripts means best-response computation, not learning — a
low-dimensional deviation search (sell offsets, withhold percentages, counter-buys) evaluated by exact
simulation, with Monte Carlo used only to average over which opponent you face.
Optimise **win probability, not money**, because destructive strategies that cost you $5k and cost the
opponent $15k are winning strategies under Elo.

Its stated bet: market impact is weak but non-zero, and shifting sell days by 1–2 turns might capture a
free 3–5%.

## What the measurements say

### Test 3 is already answered: the market never crashes, because it never saturates

`scripts/measure_true_drain.py` reads the town inventory trace straight off a real leader replay.
Inventory starts at 10,000 per product, rises with player fills and falls with shop demand.

| product | drain | absorbed ≥ | ratio | inv final | price first → last |
|---|---|---|---|---|---|
| WHEAT | 662 | 2,257 | 3.41 | 9,136 | 25 → 54 |
| STRAWBERRY | 572 | 504 | 0.88 | 9,958 | 120 → 174 |
| MILK | 500 | 486 | 0.97 | 9,906 | 160 → 244 |
| WOOL | 284 | 286 | 1.01 | 10,016 | 200 → 185 |
| MELON | 140 | 132 | 0.94 | 10,100 | 250 → 150 |

Seven of eight products **cleared** — the shops ate everything both players offered and ended *below*
the 10,000 they started with.
Prices **rose all season**: wheat +116%, milk +53%, strawberry +45%.
A saturated market falls to its floor; this one did the opposite.

MELON is the sole exception and behaves exactly as regime A predicts: inventory up +100, price halved
250 → 150.
That is why "melon saturates at ~11–16 tiles" was the one saturation finding in this project that ever
held up.

So we are in **regime B for seven products and regime A for melon alone**.
The tragedy of the commons cannot be biting when combined supply never reaches demand.

The cause of the price ramp is not subtle: the town's eight shops unlock across days 3–24
(`jax_sim.random_unlock_days`), so demand *grows* all season while supply is roughly flat.

### Test 1 run directly: timing moves money a little and wins not at all

`scripts/measure_sell_timing_impact.py` takes a fixed production plan and shifts **only** the sell days,
so any difference is pure market impact.
Baseline 16/16 wins, us $40,540 against $18,857.

Uniform shift of every sell:

| shift | wins | our bank | vs base |
|---|---|---|---|
| −3 | 13/16 | 29,258 | −11,281 |
| −1 | 16/16 | 35,416 | −5,124 |
| 0 | 16/16 | 40,540 | — |
| +1 | 16/16 | 38,657 | −1,883 |
| +3 | 16/16 | 34,510 | −6,029 |

Per-product, the largest effect anywhere was WHEAT at +2 days: **+$1,467, or +3.6%**.
MELON was uniformly negative in both directions, i.e. its timing was already optimal.

**The win rate did not move.** 16/16 in every case but one.
That is the result that matters, because the ladder is an Elo rating and a $43k win scores exactly what
a $4k win scores.
Kimi's own numeric bet — 3–5% of revenue — turns out to be right in magnitude and irrelevant in effect.

Caveat that bounds this: our opponent pool banks $18.8k against our $40.5k, so wins are not close and
timing cannot flip them.
Against a peer 3% away the same 3.6% could matter.
But the leader's own tape shows no crash to exploit.

### The replays are mirror matches, which reframes "he wins by 3%"

`scripts/measure_realised_revenue.py` found the two seats' spend to be **byte-identical** in all four
replays — same $43,475 of BUY_PRODUCT, same $16,638 of seed, same $7,916 of hires.
These are one script playing itself.

So `somewhere after` winning by 1.7–4.2% is not a 3% strategic edge over a field.
It is the seat tie-break when two identical tapes contest the same fills.
That answers the question of whether `OPPONENT_SHARE` should be 0.97: the margin it was inferred from
is not a strategic quantity at all.

## Verdict

Kimi's method prescription is right and is already what this project does: exact best-response search
over a low-dimensional plan space, selected on win rate.
`scripts/local_search.py` is that, and it proved a 1-change local optimum over 26,421 neighbours.

Kimi's *strategic* prescription does not apply, because the premise fails on measurement.
Economic warfare needs a thin market; ours is thick for everything except melon.
Front-running, withholding and flooding all trade on price impact that is worth ~3% of money and 0% of
wins.

Two things follow that are worth more than the market layer:

1. **Late capacity is worth ~1.5–2× early capacity**, because prices ramp with shop unlocks.
   Neither `DRAIN_UNITS` (a flat season total) nor `scheduler.payback_days` models this time shape.
   This is a real, unexploited edge and it is a *production* edge, not a market one.
2. **Wheat moves through his farm at 3.41× its drain.** Whether that is a trade we cannot express or
   feed we can is settled below.

## Follow-up: the wheat audit (Kimi's item 3)

Kimi's second round proposed a `CommodityArbitrage` chain — buy wheat at 25, sell at 54, ~2× on capital,
no tiles or units needed — and predicted our library cannot express it.
`scripts/audit_leader_wheat.py` reads every wheat order and every FEED op off the tape.

| quantity | value |
|---|---|
| wheat SEEDS bought (tiles planted) | 66 |
| wheat PRODUCT bought from town | 967, costing **$43,475** |
| wheat SOLD to town | 1,131, taking **$52,581** |
| FEED ops emitted (1 wheat each) | 319 |
| mean buy price | $44.96 |
| mean sell price | $46.49 — spread **+3.4%** |
| net trade P&L | **+$9,106** |

**It is not arbitrage.** The realised spread is 3.4%, not the 2× the hypothesis needs — he buys and sells
at much the same price nearly every day, rather than buying cheap early and selling dear late.

What the volume actually is: **he buys his animal feed instead of growing it.** 319 units go straight to
FEED, and the surplus 648 is flipped at a small margin.
Buying feed is something our library already expresses — `ranch(buy_feed=True)` is the *default* — so
this is not a representation gap.
The whole operation nets $9,106, about 6.5% of his bank: real, but not where the game is won.

One methodological note worth keeping. The first run of this audit reported **FEED = 0** for a farm with
14 animals, because it read a non-existent `action["units"]` key; unit ops actually live under
`action["farmer"]` and `action["hands"]`.
A missing key reads as a confident zero, and a confident zero would have "confirmed" the arbitrage
hypothesis outright.
That is the same silent-zero failure class as the fertilizer and land-buy bugs.

So of Kimi's two remaining edges, **the price ramp survives and the trading layer does not.**

Test 2 (manipulation) was not run.
Given that seven of eight products clear with prices rising, a flood has nothing to crash, so its
expected value is low — but it is cheap and remains open.