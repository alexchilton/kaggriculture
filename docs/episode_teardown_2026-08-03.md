# What a $145k agent actually does — measured from real episode replays

First teardown of real leaderboard episodes in this project.
Everything here is counted from the replay JSON, not inferred from a notebook or a forum post.

Source: `kaggle/kaggriculture-episodes-index` -> `kaggriculture-episodes-2026-08-02`, four episodes at
~27 MB each.
Script: `scratchpad/analyse_eps.py`, output in `data/logs/episode_analysis.log`.

**Alex said the leaders were more diverse and I treated it as unverified.
The data says he was right, and the margin is not small.**

---

## The headline: they are ~50/50, not specialists

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

**Animal products 45.1% · crops 48.3% · fertiliser 6.7%.**

Three crops carrying real weight, two animal species, and a fertiliser side-business.
This is not the "83% from milk and wool" single-episode figure in `CLAUDE.md` -- that was one agent in
one episode and reads as an animal specialist.
A genuinely mixed economy is a different target.

## Four things that contradict what we have been building

### 1. Melon is not the meta crop

Strawberry out-earns melon nearly 2:1 ($42,942 against $24,489) on 309 units against 123.
Seeds bought: `STRAWBERRY 44, WHEAT 34, MELON 21`.

Our policy is **93% melon** (`crop MELON:0.93`), and `jax_heuristic`'s `MELON_TILES` is the constant we
were about to raise.
`docs/public_meta_2026-08-03.md` already said "melon is the wrong crop" from notebook reading; this is
the measured confirmation.

### 2. Wheat is an input, not a crop to specialise in

They **buy 1,055 units of wheat for $47,594** and **sell 855 units for $38,632**.
Wheat is bought to FEED animals -- `jax_masks.py:96` requires `carrying_wheat` -- and the surplus is
traded.
Net cash on wheat is negative; the return arrives as milk and wool.

A cash-only reward view would score that wheat purchase as a $47k loss, which is exactly the objection
that produced `kagg/rl/net_worth.py`.

### 3. Fertiliser is a revenue stream, not an expense

271 units sold for **$14,698**, sourced from `COLLECT_FERTILIZER` -- no action cost, one per animal per
day (`jax_masks.py:98`, gated on `has_animal`).
Free money, and only available if you own animals.

Ours **buys** fertiliser on 19.3% of turns, sells on 24.5%, and applies it **zero** times in 8 full
seasons (`FERTILIZE: raw 0`). We pay the spread for what they harvest free.

### 4. Cows and sheep. No geese.

`COW 8, SHEEP 6, GOOSE 0`. `BUILD_PASTURE 14, BUILD_COOP 0`.
Also **304 hires** and 2 land purchases.

Goose is the cheapest animal ($300) and the one our own toy and agents reach for first.
The measured meta skips it entirely.

## The op census, theirs against ours

| op | them | us |
|---|---:|---:|
| FEED | 4.45% (324) | **0.00%** |
| CARE | 4.27% (311) | **0.01%** |
| COLLECT_FERTILIZER | 4.38% (319) | **0.00%** |
| FERTILIZE | 1.24% (90) | **0.00%** |
| WATER | 10.9% | 19.0% |
| PASS | 7.0% | 5.6% |

Every one of the four ops carrying their animal economy is at literal zero in ours, and we water
roughly twice as much.
`CLAUDE.md` already measured WATER at **+0.100** correlation with money against FEED **+0.452** and
CARE **+0.441** over 312 seats; this is the same finding from the other direction.

## Two caveats, stated because they change what the numbers mean

**This is a mirror match.**
`senkin13` and `syouya tobita` submitted **identical action dicts on 536 of 720 turns** -- verified, not
assumed. They are near-identical forks of one strategy. Where they diverge is only the market list, and
seat 0 gets orders filled that seat 1 does not, which is the seat-0 market priority our own sim models.
`CLAUDE.md`: *"A mirror match is not a best response."* So this is one popular strategy well executed,
not the field's answer to it.

**These are not the top five.**
The 2026-08-03 leaderboard reads `Dmitry Larko 2942.8, li jiaqi77 2933.3, manual player 2911.7,
IY 2869.2, Juste Me`. Neither name here appears in it.
What is measured above is a strong mid-field agent at ~$145k. The leaders may differ again, and the
episodes for those names still need pulling.

## Rating inflation, from the index manifest

| date | episodes | top avg score | median avg score |
|---|---:|---:|---:|
| 2026-07-30 | 864 | 1,152.4 | 669.8 |
| 2026-07-31 | 928 | 1,427.0 | 1,175.3 |
| 2026-08-01 | 829 | 1,580.6 | 1,348.2 |
| 2026-08-02 | 793 | **2,627.2** | **2,319.2** |

The **median** competitor went 670 -> 2,319 in four days, and the top-to-median gap narrowed from 483
to 308 points.
The field is converging upward fast, so any target read off a notebook from a few days ago is stale --
including the $90k-$123k range in `public_meta_2026-08-03.md`.

## What follows

1. **Pull episodes for the top-five names.** This teardown measured whoever was in the first listing
   page. The leaders are the actual reference.
2. **Strawberry, not melon.** Re-measure `MELON_TILES` against a strawberry allocation, with weeds on
   (the old constant sweep is void -- see `jax_frontier.py`).
3. **The animal economy is worth ~45% of a $220k gross and we score 0.00% on all four of its ops.**
   Ours is not refusing a marginal option; it has never seen the option work. No scripted agent we own
   beats `farm`'s $28,168 using animals, so there is nothing in the pool to learn it from.
4. **COLLECT_FERTILIZER is free money nobody in our pool takes**, already noted in
   `jax_frontier.py`'s docstring and still unbuilt.

Related: [[ideas]], [[public_meta_2026-08-03]], [[fable_review_animal_chain_2026-08-03]].
