# Does the wheat-fill middle generalise? Ryo and tetsuya vs Kawashigi

Measured 2026-08-21. Companion to `docs/kawashigi_algorithm_2026-08-21.md`.

Sample, as first reported: 228 カワシギ, 145 Ryo, 117 tetsuya.
**Those counts are inflated.** 167 episode ids sit in more than one directory under
`data/seed_scripts/`, so the extractors read the same replay several times:

| player | rows per day | distinct game-seats | copies |
|---|---|---|---|
| カワシギ | 228 | **213** | 15 |
| tetsuya | 117 | **106** | 11 |
| Ryo | 145 | **109** | 36 — a quarter of his rows |

Duplicates land in the same cross-validation fold (the split is on `(game, seat)`), so this is not
train/test leakage. It silently reweights the duplicated seasons, and every raw count below is over
the inflated row set. The purity and shape columns are means and are barely moved; the
distinct-multiset counts are the ones to treat as approximate.
Rows: `data/target_rows_kawa_norm.json`, `data/target_rows_ryo.json`, `data/target_rows_tets.json`.
Script: `scripts/crop_shape_by_day.py`.
Logs: `data/logs/crop_shape_kawa_2026-08-21.log`, `crop_shape_ryo2_2026-08-21.log`,
`crop_shape_tets2_2026-08-21.log`.

## Answer

**Two of the three have it. Ryo does not.**

Kawashigi and tetsuya both play a mid-season that is one crop with a varying count.
Ryo plays a real crop mix all the way through.

## The measure

`purity` is the share of all plants on that day, across all that player's seasons, that are the
day's single most common crop.
`shapes` is how many distinct crop *mixes* remain once magnitude is divided out — WHEAT:5 and
WHEAT:11 are the same shape.
**shapes == 1 and purity == 100% means the day is a scalar, not a plan.**

| day | カワシギ purity / shapes | tetsuya purity / shapes | Ryo purity / shapes |
|---|---|---|---|
| 14 | 100% / 2 | 100% / 2 | 81% / 6 |
| 15 | 100% / 1 | 100% / 3 | 86% / 7 |
| 16 | 100% / 1 |  99% / 3 | 76% / 8 |
| 17 | 100% / 3 |  98% / 2 | 81% / 6 |
| 18 | 100% / 3 |  99% / 3 | **53%** / 7 |
| 19 | 100% / 2 | 100% / 3 | 75% / 8 |
| 20 | 100% / 3 |  96% / 4 | 82% / 4 |
| 21 |  70% / 4 |  96% / 3 | 76% / 4 |
| 22 |  87% / 2 |  99% / 3 | 84% / 2 |
| 23 |  95% / 2 | 100% / 3 | 78% / 2 |
| 24 |  88% / 2 |  98% / 2 | 74% / 3 |
| 25 |  87% / 2 |  98% / 3 | 79% / 3 |
| 26 |  92% / 2 |  98% / 2 | 100% / 1 |
| 27 | 100% / 1 |  98% / 3 | plants nothing |

tetsuya is the cleanest: **96–100% wheat from d14 to d27 with no carrot phase at all.**
Kawashigi is pure wheat d14–d20, then a 1–2 CARROT phase d21–d26, then pure wheat d27.
Ryo never gets above 86% after d13 and drops to 53% at d18.

## Season crop totals

| crop | カワシギ | tetsuya | Ryo |
|---|---|---|---|
| WHEAT | 67.7% | 71.6% | 68.0% |
| STRAWBERRY | 21.0% | 19.8% | 14.7% |
| MELON | 8.1% | 6.8% | 5.6% |
| CARROT | 3.2% | 1.5% | **10.2%** |
| TOMATO | 0% | 0.4% | 1.5% |

The wheat/strawberry/melon shares are within a few points across all three. **Carrot is what
separates Ryo** — 10.2% against 1.5–3.2%, and it is spread through his middle rather than
confined to a late phase.

## The openings do NOT agree

The wheat middle generalises; the opening does not. These are three different games.

| | カワシギ | tetsuya | Ryo |
|---|---|---|---|
| d0 | MELON+WHEAT, 19 plants | STRAWBERRY+WHEAT, 13 plants | MELON+WHEAT, 17 plants |
| d1–d3 | plants nothing | nothing, then MELON:3 at d3 | WHEAT 1–3, nothing at d3 |
| d4–d8 | STRAWBERRY | MELON then STRAWBERRY | STRAWBERRY |
| ends planting | d28 | d28 | **d27** |

All three have a **single fixed d0** (1 distinct multiset over 117–228 seats) and plant nothing on
the last two days.

## What this changes

- The three-phase structure — fixed opening, scalar middle, fixed close — is **not Kawashigi's
  quirk**. Two independent strong players do it.
- Copying the middle from any of them is the same act: pin the crop to WHEAT and let the planner
  fill. There is nothing player-specific to copy there.
- The opening is where they differ, and it is also the part that is small enough to hold as a
  library (1–9 distinct rows to d6).
- Ryo is the wrong teacher for the middle. He is the interesting one for carrot, if carrot turns
  out to pay.

## Correction recorded

An earlier read of Ryo on a **9-seat** sample showed 87–100% mid-season purity and was reported as
"already looks the same". The full 145-seat sample gives 53–86%. The thin sample was wrong and the
conclusion drawn from it was wrong.

The 9-seat sample existed because a shell `DIRS=$(ls ... | tr ...)` produced an empty string — `ls`
failed but the pipeline's exit status came from `tr`, so `&&` did not catch it and the extraction
silently read one directory instead of 31. **A pipeline's exit status is the last command's.**

## Not established

- Whether the mid-season count is board capacity for any of the three. Being measured separately.
- What triggers Kawashigi's d21–d26 carrot, or Ryo's carrot generally.
- Whether Ryo's mix beats the wheat-fill. Nothing here compares outcomes — this is what they plant,
  not what it earned.
