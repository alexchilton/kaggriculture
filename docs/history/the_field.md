# What the opponents actually do

Measured from leaderboard replay JSON, not inferred from notebooks or forum posts.
This file exists because "the leaders" get described from memory and the description drifts.

> **Version and currency caveat, added 2026-08-09.** The replays analysed below predate the
> 2026-08-07/08 move to `kaggle-environments` 1.32.6, so absolute dollar figures (bank totals,
> revenue splits) are not directly comparable to a 1.32.6 game. The structural finding — winners
> submit fixed 720-turn open-loop scripts — is a claim about *behaviour*, not price level, and is
> independently reconfirmed on 1.32.6 by `docs/what_the_leaders_actually_grow_2026-08-09.md` and
> `docs/the_top_five_clusters_2026-08-09.md`, which also show our own ladder position (1,123.5)
> against the current field floor (~3,117) — read those two before treating this file's field as
> "close."
>
> **2026-08-11 addendum.** `docs/the_ladder_is_two_scripts.md` measures 2,744 ladder seats directly
> and reconfirms the open-loop finding at population scale: most of the field is scripted, two shared
> scripts dominate, and the one clearly reactive top player (#1) beats the fixed scripts by ~110
> rating points through an adaptive herd, not a different opening.
>
> **2026-08-21 addendum.** `docs/the_field_is_a_monoculture_2026-08-21.md` is the current, larger
> sample (1,010 games) for "what opponents do": of 58 sampled players only the top 4 ranked ones are
> genuinely distinct agents, and 38 of 58 share one byte-identical opening. Read that file for the
> current opponent-diversity picture; this file's "five distinct signatures" framing is thinner.

## The winners submit fixed 720-turn scripts

Six replays, five distinct players. For each player appearing in more than one replay, every turn's
action was split into `units` (`farmer` + `hands`) and `market` (trading orders) and compared
turn-by-turn between episodes:

```
senkin13        4 episodes, 6 pairwise comparisons, different opponents AND swapped seats
                units  identical 720/720  (100.0%)  in all six
                market identical 720/720  (100.0%)  in all six
                banks $121,538 - $145,034

syouya tobita   units  identical 720/720       (100.0%)  in all six
                market identical 716-720/720   ( 99.4-100.0%)

Dmitry Larko    units  701/720 (97.4%)   market 689/720 (95.7%)
```

Independently confirmed on the later leader `somewhere after` (four replays, 2026-08-05): every
derived quantity — land days, herd, seed counts, fertilizer flows, crew ramp — is **byte-identical
across all four**, in both seats, against four different opponents. The only variation anywhere is
107 vs 106 `FERTILIZE` ops.

**Reactivity is worth approximately nothing at the top of this leaderboard.** Two design questions
close on it: no opponent model, no market policy.

**But the artifact is a genuine 720-step program, not a repeated routine.** Every player shows
**30/30 distinct daily unit-routines**. There is seasonal phase structure; "one routine, repeated"
cannot express what they play.

**Open-loop does not mean unoptimised.** Reactivity is conditioning on state at play time, which
they have none of. Optimisation is searching for a good sequence before play time, which they
clearly did a great deal of.

### Caveats that must travel with the claim

- **`senkin13` and `syouya tobita` are not confirmed top-ranked** — a strong mid-field agent at
  ~$145k — and they are a **mirror match**: 536/720 identical action dicts between the two of them.
  `CLAUDE.md`: a mirror match is not a best response.
- The only confirmed top-tier games are the `Dmitry Larko` pair, which is the *weakest* open-loop
  evidence in the table. Our own docs disagreed on that figure (97.4% here, 93.5% elsewhere for the
  same pair).
- **Zero `WEED` tiles across all 720 turns of all six replays**, despite `weedSpawnChance: 0.005`.
  "The winners ignore weeds" is untested, not proven harmless. Validate any open-loop script across
  many fresh seeds before submitting.
- The claim that survives independently of rank: **"manual player" ranked #3 at 2,911.8.** A human
  cannot compute reactive per-turn decisions across 720 turns under a one-second clock.

## The mixed economy, torn down

`senkin13`, episode 89541819, final reward **$145,034**, gross sales **$220,542**:

| product | revenue | share | units |
|---|---:|---:|---:|
| MILK | $58,505 | 26.5% | 235 |
| STRAWBERRY | $42,942 | 19.5% | 309 |
| WOOL | $40,112 | 18.2% | 190 |
| WHEAT | $38,632 | 17.5% | 855 |
| MELON | $24,489 | 11.1% | 123 |
| FERTILIZER | $14,698 | 6.7% | 271 |
| EGG | $769 | 0.3% | 12 |
| CARROT | $395 | 0.2% | 10 |

**Animal products 45.1% · crops 48.3% · fertiliser 6.7%.** Three crops carrying real weight, two
animal species, a fertiliser side-business. Not the "83% from milk and wool" single-episode figure
that circulated for a while, which was one agent in one episode.

Four things this contradicted:

1. **Melon is not the meta crop.** Strawberry out-earns it nearly 2:1 on 309 units against 123.
   Seeds bought: `STRAWBERRY 44, WHEAT 34, MELON 21`.
2. **Wheat is an input.** They buy 1,055 units for $47,594 and sell 855 for $38,632. Net cash on
   wheat is negative; the return arrives as milk and wool.
3. **Fertiliser is a revenue stream**, not an expense — 271 units for $14,698, from
   `COLLECT_FERTILIZER`, which costs one action and is available only if you own animals.
4. **Cows and sheep, no geese.** `COW 8, SHEEP 6, GOOSE 0`, `BUILD_PASTURE 14, BUILD_COOP 0`, plus
   **304 hires** and 2 land purchases. Goose is the cheapest animal and the one our agents reach
   for first; the measured meta skips it entirely.

## The leader `somewhere after`, four replays 2026-08-05

| episode | seat | opponent | his | theirs | margin |
|---|---|---|---|---|---|
| 90016067 | 1 | haoran huang430 | 160,593 | 157,959 | +1.7% |
| 90018004 | 1 | manual player | 134,780 | 130,777 | +3.1% |
| 90020633 | 1 | Savko | 137,667 | 133,335 | +3.2% |
| 90023239 | 0 | Savko | 123,443 | 118,437 | +4.2% |

4/4, mean bank **$139,121**, mean margin **+3.1%**.

**The margin is the point.** Everyone at the top banks $120k-160k and the leader edges it by a few
thousand. On an Elo ladder a $2,634 win scores what a $50,000 win scores, so the top of this board
is a knife-edge contest between several near-equal fixed scripts — and because they are fixed, they
cannot punish anything. They are a stationary target to compute a best response against.

His farm: land on **days 7 and 10**, two parcels, never SE. **8 COW + 6 SHEEP = 14 pens.**
WHEAT 66 (50%), STRAWBERRY 44 (34%), MELON 21 (16%). 318 fertilizer collected, **107 applied**,
0 bought, 445 offered. Crew 4 on day 0 ramping 4-6-5-5-6-6-6-8-10-11-12, flat 12 from day 10.
`DIG` 103 times.

Op census, four replays aggregated:

```
NORTH 4,943 16.8%   WEST 4,392 15.0%   SOUTH 3,716 12.7%   EAST 3,428 11.7%
WATER 3,404 11.6%   PASS 1,427 4.9%    PICKUP 1,356 4.6%   HARVEST 1,352 4.6%
FEED 1,276 4.3%     COLLECT_FERTILIZER 1,272 4.3%          CARE 1,232 4.2%
PLANT 524 1.8%      FERTILIZE 427 1.5%  DROP 320 1.1%      PLACE 108 0.4%
DIG 103 0.4%        BUILD_PASTURE 56 0.2%
```

**56% of his ops are movement and `PASS` is only 4.9%.** His units are spread across the board
rather than working compact adjacent blocks — he spends the turns to reach better tiles. Our own
serpentine blocks minimise walking by construction, which looks efficient and may be the wrong
objective.

`PLANT` 524 across four replays is 131 per replay, matching 66 + 44 + 21 = 131 seeds exactly.

## How he funds it

From `data/seed_scripts/new_leader/90016067.json`:

```
day  0  $3,000   BUY_ANIMALx4 BUY_PRODUCTx16 BUY_SEEDx4 HIREx4 SELLx12
day  1  $   42   <-- forty-two dollars
day  2  $  141
day  3  $  217
day  5  $  621
day  7  $1,719   BUY_LANDx1
day 10  $1,278   BUY_LANDx1     <-- a $2,000 parcel on a $1,278 dawn bank
day 11  $3,236
day 12  $6,828
day 13  $14,622
```

- **He goes all-in on day 0 and ends it on $42.** Four animals, ~51 wheat bought in small lots
  across all 24 hours, 18 seeds, 4 hires. His day-0 SELL orders are speculative over-requests
  against an empty shed and mostly no-op — exactly like ours.
- **His early revenue is FERTILIZER.** Day 1 hour 8: `SELL FERTILIZER x4`. Four day-0 animals
  produce it nightly, collecting costs no action, and he sells it daily from day 1 — long before
  milk arrives on day 8. Our census: 83 collections against his 318.
- **He funds purchases from same-day sales.** The $2,000 parcel on a $1,278 dawn bank works because
  his sells land earlier in the same day. He runs at the edge of insolvency the whole ramp.
  **We hoard, he compounds.**
- Wheat is **not** arbitrage: he buys 967 at mean $44.96 and sells 1,131 at $46.49, a 3.4% spread,
  with 319 units going to FEED. He buys feed instead of growing it.

## The public meta (2026-08-03 notebooks, `reference/community_notebooks/`)

Live market prices in that meta: `STRAWBERRY 280 · MILK 263 · WOOL 235 · MELON 54 · WHEAT 58`
against bases of 120/160/200. Strawberry, milk and wool trade **well above base** because the town
drains faster than two farms can supply; **melon collapsed to 22% of base** because everyone dumps
it on day 10.

Three clusters: pure cow ranch (3-10 cows), melon IPO (16 melons + 2 cows, day-10 dump), and the
staged economic herd (`C0x` family), which is the strongest public code. The common plan (c16) is
**8 cows, 5 sheep, 5 strawberry plots, 12 hands**.

Hands are nearly free at the bottom of the Fibonacci ladder and expensive fast at the top:

| hands | 6 | 8 | 10 | **12** | 14 | 16 |
|---|---|---|---|---|---|---|
| coins/day | 20 | 54 | 143 | **376** | 986 | 2583 |

Twelve hands is 376 coins for 288 extra actions — about **1.3 coins each**, against one in-window
melon watering worth $250.

Value per action, measured:

| action | value |
|---|---:|
| melon, in-window watering | ~$250 (while price holds) |
| cow, fed + cared | ~$95 |
| sheep, fed + cared | ~$86 |
| **`COLLECT_FERTILIZER`** — free, every animal, every day | **~$85** |
| goose, fed + cared | ~$32 |
| strawberry | ~$37 |
| wheat | ~$17 |

## Our own reference tape: Seb

`data/seed_scripts/top_guys/90494364.json` is the tape `scripts/breakdown.py --tape seb` diffs
against, day by day, on seed 11 with weeds off. It is a **diagnostic, not the goal** — beating it
is the goal, so "the tape doesn't do this" is never an argument against a change.

Its own metadata is not trustworthy: `build_tiles` day 0 says `[[4,4] COW]` while a SHEEP stands
there all season. The ordered `places` list is the good metadata; `build_tiles` labels are not.

## What the field says about our own numbers

- Ladder targets go stale in days. A field that reached 2,700 in four days keeps climbing.
- **Imitation learning off the daily top-episodes datasets was checked and rejected**: those are
  ordered by *current* rating, so on 2026-07-31 they contained agents near the $3,512 baseline while
  we banked $43k. Their value is an opponent pool and scouting. Re-check only once leaderboard
  scores exceed our own.
- **Self-play pressure is bounded by the pool it plays.** A pool of frozen copies of an $18k policy
  plus scripts topping out at $27k demands nothing, and nothing in it plays cows, sheep, strawberry,
  fertiliser collection or a twelve-hand crew — so those strategies are not merely undiscovered,
  they are never *demonstrated*.
