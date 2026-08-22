> **SUPERSEDED, added 2026-08-11.** This doc's central conclusion — "we do not need a new day-0-10
> tape" and "our schedule already matches Seb's build on the levers that matter most" — is
> contradicted by `docs/the_ladder_is_two_scripts.md`, measured from 2,744 ladder seats: the field
> plants 108-147 WHEAT tiles a season and our schedule plants 24, which is the single largest gap to
> the field found so far. Seb's tape (what this doc says we already match) was optimal under the OLD
> `townCenterSellInterval=12` economy; his median bank halved and he has since withdrawn from the
> ladder. This doc's 20-episode sample predates that population-scale measurement — read
> `the_ladder_is_two_scripts.md` first.

# What the leaders actually grow, measured from `data/ladder/leaders_0808/`

20 real episodes from the top of the ladder on 2026-08-08, plus our two named losses (91229682,
91231728), read directly off the board state and the raw action stream — not off any summary.
Extraction script for this session only, not committed to the repo (this analysis pass wrote only
this doc under `docs/`): `/private/tmp/claude-501/-Users-alexchilton-DataspellProjects-kaggriculture/5fb520ea-bfb5-460d-aaa7-d7f197a84d9e/scratchpad/extract_leader_mix.py`.
Re-derive from the raw episode JSON in `data/ladder/leaders_0808/` and `data/ladder/losses/` if that
scratchpad file is gone — the method is: for crops, count cumulative `PLANT` actions in the raw
`steps[t][seat]["action"]["farmer"|"hands"]` stream (see Method note below on why final-tile counts
are misleading); for animals, read `steps[-1][seat]["observation"]["farms"][seat]["tiles"]` for
dicts with an `"animal"` key; for sells, read `["action"]["market"]` entries with `order[0] ==
"SELL"`, priced at that turn's `["observation"]["market"]["prices"]`.

## Answer up front

**We do not need a new day-0-10 tape.** The crop tile mix our schedule ships (strawberry-heavy,
moderate melon, thin standing wheat) is close to what the one player in this sample who
consistently beats the field actually runs, and the existing `we_oversell_into_a_contested_book`
/ `geometry_of_the_herd` analyses already measured, on these same two loss episodes, that the
opening is not where we lose (own-opening 0/6 vs tape-opening 4/6; geometry is not a lever).

**What the fresh 20-episode sample adds, and what it changes:**

1. **18 of the 20 leader episodes are one public reference script playing itself or a near-copy of
   itself** (`the_field.md`'s open-loop finding, reconfirmed here on new data — see Table 1). Any
   win/loss or win-rate reading off those 18 rows is mirror noise, not a strategy signal. Per
   CLAUDE.md's own trap: do not rank by money, and here the mirror cluster banks the *most* money
   ($105k-$110k in several rows) while the actual best player banks the *least* ($88,007 and
   $45,892) — exactly the "rank-1 banks least" trap named in the task.
2. **Only one build in this sample beats that public script consistently: `Seb (allegedly)`, 2/2**,
   and it differs from the mirror baseline in land timing (day 4/6/10 vs day 7/11), crew ramp
   (front-loaded to 7 hires on day 0 vs a ragged 5,0,2,1,4... ramp), herd ratio (sheep-heavy,
   10-15 sheep to 7-9 cow, vs the baseline's fixed 6 sheep/8 cow), and total wheat volume (22-25
   PLANT ops vs the baseline's 103-108) — but **not** in crop *tile* mix: both run ~40-43
   strawberry tiles concurrently and both stop new planting almost entirely after day ~12.
3. **Our own schedule already matches Seb's build on the levers that matter most** (land days,
   crew ramp, strawberry-heavy tile allocation) — this was not obvious before reading the raw
   tiles, because final-day tile snapshots badly undercount annual crops (see Method note below)
   and the season *seed-purchase* totals in `data/seed_scripts/new_leader/schedule.json` come from
   a *different* leader than Seb's tape.
4. **The one clear, fresh, measured mismatch is herd ratio: Seb runs more sheep than cows; our
   schedule (and both loss episodes) run more cows than sheep, or a near-even split** — COW 13/
   SHEEP 8 and COW 9/SHEEP 7 against Seb's SHEEP 15/COW 7 and SHEEP 10/COW 9. The saturation model
   in `what_saturates_and_what_does_not_2026-08-09.md` says a cow's flat-max value ($1,164/head)
   is *higher* than a sheep's ($897/head), which argues the other way — this is a real, open
   tension between the model and the one winning build, not resolved here.
5. **Our two actual losses were not against Seb-style opponents at all.** `Shivam_2212`
   (91229682) is a byte-for-byte match to the 18-episode mirror baseline (WHEAT 108, STRAWBERRY
   42, MELON 24 PLANT ops — identical to `kakuteki`'s numbers in Table 1) and beat us by 34%. `As
   Wasti` (91231728) runs a five-crop build including CARROT and TOMATO that appears nowhere in
   the 20-leader sample, and beat us by 9%. **Since 18 of 20 real top-ladder games in this sample
   are the wheat-heavy mirror-baseline style, and that is exactly what beat us in one of our two
   losses**, matching Seb's mix is necessary but not sufficient — most of the field is not
   Seb-shaped.
6. **The animal-saturation model's corrected numbers (16 cow, 16 sheep, 8 goose flat-points) are
   not contradicted by this sample — they are untested by it.** Every real herd observed, Seb's
   included, stays under 16 of either species, and nobody fields a goose. The model cannot be
   confirmed past a boundary nobody in the sample approaches.

---

## Method note — read this before trusting any "final board" number

The final-day tile snapshot **badly undercounts annual crops**. WHEAT, MELON and CARROT are
harvested and, in the closing days of a 30-day season, frequently left bare rather than replanted,
so a day-29 snapshot can show `STRAWBERRY: 1` for a farm that planted 41 strawberry tiles across
the season. `scripts/why_the_land_is_bare.py` already established that the schedule's `plants` /
PLANT-op count is the correct season measure and the final tile is not.

This document therefore reports **two different things and does not mix them**:

- **Season PLANT-op totals** (cumulative `PLANT` actions issued by farmer + hands, all 720 turns)
  — the right measure of total crop *activity*, used in Tables 1, 2, 4, 9.
- **Mid-season snapshots** (day 15 / day 20 board state) — the right measure of *concurrent* tile
  occupancy, which is what the saturation model's "N tiles" actually means. Used in the
  cross-check section below.
- **Final animal pen counts** are reliable as-is: pens persist once built, so a day-29 snapshot is
  the correct season measure for COW/SHEEP/GOOSE. Used throughout.

---

## Table 1 — every leader seat, 40 rows (20 episodes x 2 seats)

Season PLANT ops, final animal pens, bank, result.

```
   episode seat                     team result      bank quads                                season PLANTs            final animal pens
  90849277    0                 kakuteki   WIN    54,528     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90849277    1             Akhil Chinta  LOSS    52,963     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90849281    0                 BHackers  LOSS    75,943     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90849281    1                 kakuteki   WIN    79,805     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90849357    0          Leon Christians  LOSS    36,398     3                     WHEA:105,STRA:42,MELO:24                 COW:8,SHEE:6
  90849357    1                 kakuteki   WIN    40,230     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90850167    0  ╰┈➤ˎˊ˗ www.sleepyai.org  LOSS    88,917     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90850167    1                 kakuteki   WIN    95,366     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90850170    0          Seb (allegedly)   WIN    88,007     4                      STRA:40,MELO:25,WHEA:22                SHEE:15,COW:7
  90850170    1                 BHackers  LOSS    67,676     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90850292    0                  Yvonne.   WIN    78,814     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90850292    1              Wufang Hong  LOSS    76,086     3                     WHEA:105,STRA:42,MELO:24                 COW:8,SHEE:6
  90851011    0                 kakuteki   WIN    76,639     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90851011    1             Akhil Chinta  LOSS    76,045     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90851012    0                    venks  LOSS    34,500     3                     WHEA:109,STRA:42,MELO:24                 COW:8,SHEE:6
  90851012    1                 BHackers   WIN    36,791     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90851033    0            ArturoSirvent  LOSS   105,743     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90851033    1              Wufang Hong   WIN   106,619     3                     WHEA:105,STRA:42,MELO:24                 COW:8,SHEE:6
  90851845    0                 kakuteki  LOSS    32,889     3                     WHEA:108,STRA:42,MELO:24                 SHEE:3,COW:3
  90851845    1          Seb (allegedly)   WIN    45,892     4                      STRA:43,WHEA:25,MELO:20                SHEE:10,COW:9
  90851847    0                 BHackers   WIN    92,727     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90851847    1       Knight of Favonius  LOSS    92,656     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90852679    0                 kakuteki   WIN   100,057     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90852679    1          Leon Christians  LOSS    93,954     3                     WHEA:105,STRA:42,MELO:24                 COW:8,SHEE:6
  90852682    0              Wufang Hong  LOSS    69,203     3                     WHEA:105,STRA:42,MELO:24                 COW:8,SHEE:6
  90852682    1                 BHackers   WIN    70,367     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90853512    0                 kakuteki   WIN   101,749     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90853512    1             Akhil Chinta  LOSS    99,335     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90853513    0             onlysmrtsumx   WIN    68,167     3                     WHEA:103,STRA:42,MELO:24                 COW:8,SHEE:6
  90853513    1                 BHackers  LOSS    67,302     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854359    0            Sasha Turutin  LOSS    89,872     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854359    1                 kakuteki   WIN    92,414     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854360    0                 BHackers   WIN   109,836     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854360    1            Yoganjaneyulu  LOSS   109,728     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854462    0                Mohit Rao   WIN    88,958     3                     WHEA:103,STRA:42,MELO:24                 COW:8,SHEE:6
  90854462    1                Dandan Li  LOSS    87,367     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854463    0                 kakuteki   WIN    86,774     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90854463    1                Dandan Li  LOSS    85,098     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90855210    0                 kakuteki   WIN    48,974     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
  90855210    1             Akhil Chinta  LOSS    46,100     3                     WHEA:108,STRA:42,MELO:24                 COW:8,SHEE:6
```

Read the shape of this table before anything else: **35 of the 40 rows carry the identical
signature** `WHEAT ~103-109, STRAWBERRY 42, MELON 24, COW 8, SHEEP 6`, land days `[7, 11]`, and the
identical hire ramp (Table 5). Only `Seb (allegedly)`'s two rows and its two direct opponents'
rows differ in any material way. This is `the_field.md`'s "winners submit fixed 720-turn scripts"
finding landing again on completely fresh data — 18 of 20 episodes are the same public reference
agent (almost certainly `kaitofukami v23`, per `the_top_five_clusters_2026-08-09.md`) playing
itself or a near-identical relative under a different team name.

## Table 2 — our two losses, our seat only

```
  91229682 seat=0 team=alex chilton vs Shivam_2212 result=LOSS bank=61,427 opp_bank=94,412 quads=4
    season PLANT ops: STRAWBERRY:41, WHEAT:24, MELON:16
    final tile snapshot (crops): STRAWBERRY:1        <- see Method note; this number is misleading
    final animal pens: COW:13, SHEEP:8
    land days: [4, 6, 12]

  91231728 seat=1 team=alex chilton vs As Wasti result=LOSS bank=89,433 opp_bank=98,581 quads=4
    season PLANT ops: STRAWBERRY:41, WHEAT:24, MELON:16
    final tile snapshot (crops): STRAWBERRY:1        <- see Method note; this number is misleading
    final animal pens: COW:9, SHEEP:7
    land days: [4, 6, 16]
```

Both loss episodes carry **identical season PLANT-op totals** (STRAWBERRY 41, WHEAT 24, MELON 16)
— essentially the totals baked into the embedded schedule in `submission/main.py`'s `_PLAN_JSON`
(STRAWBERRY 41, WHEAT 24, MELON 17; one plant short of an exact match). That means **our live
planner, after the tape hands over, adds almost no new planting for the rest of the season** — the
crop mix in a real game is, to first order, whatever the day-0-10 tape already planted.

### Who beat us

**91229682 — `Shivam_2212`**, season PLANT ops `MELON:24, WHEAT:108, STRAWBERRY:42`. This is the
**exact same signature as the 18-episode mirror baseline in Table 1** — same land-day-adjacent
wheat volume, same crop ratio. We lost to the plain public reference script by 34%
($61,427 vs $94,412), a far bigger margin than the 1-8% internal variance the mirror cluster shows
against itself in Table 1.

**91231728 — `As Wasti`**, season PLANT ops `CARROT:40, WHEAT:79, MELON:20, STRAWBERRY:18,
TOMATO:6`. A five-crop build including CARROT and TOMATO, which **appear in zero of the 40
leaders_0808 rows**. Beat us by 9% ($89,433 vs $98,581).

Neither opponent that actually beat us resembles Seb. This directly extends the existing
`we_oversell_into_a_contested_book_2026-08-09.md` addendum finding — "we lose 4/4 to `oldleader`,
beat `seb`'s own tape by $98k" — with a fresh, independent confirmation on two previously-unread
episodes: the opponent that is shaped like our own schedule's source (Seb) is not the opponent we
actually lose to.

## Table 3 — per-player win rate across the 20-episode sample

**Read with the mirror-match caveat from CLAUDE.md applied explicitly: 16 of these 16 rows below
`Seb (allegedly)` are the same public script under different team names, so their win/loss column
is near-coin-flip noise (1-8% margins), not a strategy signal.**

```
                    team   n  wins   win%   mean bank
         Seb (allegedly)   2     2   100%      66,950
                 Yvonne.   1     1   100%      78,814
            onlysmrtsumx   1     1   100%      68,167
               Mohit Rao   1     1   100%      88,958
                kakuteki  11    10    91%      73,584
                BHackers   7     4    57%      74,377
             Wufang Hong   3     1    33%      83,969
            Akhil Chinta   4     0     0%      68,611
         Leon Christians   2     0     0%      65,176
               Dandan Li   2     0     0%      86,232
 ╰┈➤ˎˊ˗ www.sleepyai.org   1     0     0%      88,917
                   venks   1     0     0%      34,500
           ArturoSirvent   1     0     0%     105,743
      Knight of Favonius   1     0     0%      92,656
           Sasha Turutin   1     0     0%      89,872
           Yoganjaneyulu   1     0     0%     109,728
```

**Both traps named in the task are visible directly in this table.** `Seb (allegedly)` is the only
row that beat the mirror baseline both times it played it, and its mean bank ($66,950) is **the
lowest of the four 100%-win-rate rows** and lower than eight of the eleven 0%-win-rate rows —
`ArturoSirvent` banked $105,743 and lost, `Yoganjaneyulu` banked $109,728 and lost.
**Money and outcome are visibly decoupled in this exact table**; win rate is the only column worth
reading. `kakuteki`'s 91% and `BHackers`'s 57% are mirror-vs-mirror noise, not a difference in
skill — they are (almost certainly) the same script, or scripts close enough to it that they
cannot be told apart on 1-4 samples each.

## Table 4 — mix by result (WIN vs LOSS), pooled across all 40 leader rows

```
WIN (n=20): seeds bought {WHEAT: 1993, MELON: 477, STRAWBERRY: 839}   mix WHEAT 60%, STRAWBERRY 25%, MELON 14%
WIN (n=20): animals bought {COW: 160, SHEEP: 133}
LOSS (n=20): seeds bought {WHEAT: 2163, MELON: 480, STRAWBERRY: 840}  mix WHEAT 62%, STRAWBERRY 24%, MELON 14%
LOSS (n=20): animals bought {COW: 160, SHEEP: 120}
```

**This table is close to uninformative on its own** — it is dominated 18:2 by the mirror-baseline
rows on both the WIN and LOSS side, so WIN and LOSS look almost identical (60% vs 62% wheat). It is
included for completeness and to make the contamination visible, not as evidence. The real
contrast is Seb vs the mirror baseline specifically (Table 1 rows), not WIN vs LOSS pooled.

## Table 5 — land days and hire ramp, WIN rows only

```
    90849277 seat0             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90849281 seat1             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90849357 seat1             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90850167 seat1             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90850170 seat0      Seb (allegedly): land_days=[4, 6, 10]  hires(d0-14)=[7, 7, 7, 7, 7, 7, 4, 8, 9, 10, 11, 12, 12, 12, 12]
    90850292 seat0              Yvonne.: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90851011 seat0             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90851012 seat1             BHackers: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90851033 seat1          Wufang Hong: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90851845 seat1      Seb (allegedly): land_days=[4, 6, 10]  hires(d0-14)=[7, 7, 7, 7, 7, 7, 7, 8, 9, 12, 12, 12, 12, 12, 12]
    90851847 seat0             BHackers: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90852679 seat0             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90852682 seat1             BHackers: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90853512 seat0             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90853513 seat0         onlysmrtsumx: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90854359 seat1             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90854360 seat0             BHackers: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90854462 seat0            Mohit Rao: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90854463 seat0             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
    90855210 seat0             kakuteki: land_days=[7, 11]  hires(d0-14)=[5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7]
```

For comparison, our two loss episodes' hire ramps (`d0-19`), computed separately:

```
    91229682 (our seat 0):  [7, 7, 7, 7, 7, 7, 8, 8, 9, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
    91231728 (our seat 1):  [7, 7, 7, 7, 7, 7, 8, 8, 9, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
    Seb      (90850170):    [7, 7, 7, 7, 7, 7, 4, 8, 9, 10, 11, 12, 12, 12, 12, ...]
    mirror baseline:        [5, 0, 2, 1, 4, 1, 2, 8, 5, 7, 8, 14, 7, 11, 7, ...]
```

**Our crew ramp is almost identical to Seb's** (front-loaded to 7 hires on day 0, holding until day
6, ramping to 12 by day 10) and clearly different from the mirror baseline's ragged ramp. Land
timing likewise matches Seb closely: our two losses bought land on `[4, 6, 12]` and `[4, 6, 16]`
against Seb's `[4, 6, 10]`. **This is a lever we already copied correctly.**

## Table 6 — selling patterns, pooled

```
-- ALL WIN SEATS (leaders_0808) (20 episode-seats) --
     product  orders  orders/ep   units  units/order  sell-days/ep  mean price
        MILK     849      42.45    8258         9.73         17.85       113.0
  FERTILIZER     769      38.45    5428         7.06         22.70        56.7
       WHEAT     741      37.05    8408        11.35         18.20        39.2
  STRAWBERRY     716      35.80    9133        12.76         12.30        85.0
        WOOL     433      21.65    6141        14.18         14.90       123.7
       MELON     222      11.10    4854        21.86          5.55        87.7
      TOMATO       1       0.05     999       999.00          0.05        98.0
      CARROT       1       0.05     999       999.00          0.05        41.0
         EGG       1       0.05     999       999.00          0.05        67.0

-- OUR LOSSES (our seat) (2 episode-seats) --
     product  orders  orders/ep   units  units/order  sell-days/ep  mean price
       WHEAT     463     231.50    1658         3.58         25.00        45.6
  FERTILIZER     244     122.00     550         2.25         28.50        54.2
        MILK     102      51.00     438         4.29         20.00       166.1
  STRAWBERRY      92      46.00     534         5.80         15.00       169.3
        WOOL      51      25.50     294         5.76         15.50        58.7
       MELON      19       9.50     152         8.00          7.50       172.6
```

This pooled table is dominated by the mirror baseline's much larger production base (108 wheat
plants vs Seb/us ~22-25), so it is not apples-to-apples. Isolated per-build instead:

```
-- v23-CLONE baseline (kakuteki, 90849277 seat0) --
     product  orders orders/ep  units  u/order  days/ep   price
  STRAWBERRY      32     32.00    320    10.00    12.00    15.1
       WHEAT      40     40.00    305     7.62    20.00    37.9
        MILK      46     46.00    214     4.65    18.00    19.5
  FERTILIZER      29     29.00    212     7.31    22.00    59.7
        WOOL      19     19.00    148     7.79    15.00   248.0
       MELON       9      9.00    144    16.00     5.00    98.4

-- SEB (allegedly), both episodes --
     product  orders orders/ep  units  u/order  days/ep   price
  FERTILIZER     214    107.00    638     2.98    14.50    52.7
  STRAWBERRY      92     46.00    567     6.16     7.00    19.2
        WOOL      90     45.00    487     5.41     9.00   200.7
        MILK      75     37.50    386     5.15    10.50   111.9
       MELON      33     16.50    264     8.00     5.50    85.4
       WHEAT      13      6.50    148    11.38     2.50    36.0

-- OUR TWO LOSSES --
     product  orders orders/ep  units  u/order  days/ep   price
       WHEAT     463    231.50   1658     3.58    13.00    45.6
  FERTILIZER     244    122.00    550     2.25    14.50    54.2
  STRAWBERRY      92     46.00    534     5.80     7.50   169.3
        MILK     102     51.00    438     4.29    10.50   166.1
        WOOL      51     25.50    294     5.76     9.00    58.7
       MELON      19      9.50    152     8.00     4.00   172.6
```

**Wheat is the one product where we visibly diverge in order count** — 231.5 orders/episode
against Seb's 6.5 and the mirror baseline's 40 — but this does **not** read as a pricing problem:
our realized wheat price ($45.6) is *higher* than both comparison builds, matching the already-
measured verdict in `we_oversell_into_a_contested_book_2026-08-09.md` that "WHEAT ... 1.0x — no
gain, ever" from cutting supply, and that wheat price is *better*, not worse, in our losses than
our wins on that project's own 12-game ladder sample. **Do not read the order-count gap as a new
finding to fix**; it is more likely a mechanical artifact of how our sell orders are constructed
(one small order per turn rather than batched), and the existing, more rigorous counterfactual-
repricing analysis in that doc already isolated where the real money is: MILK, STRAWBERRY and WOOL
sold at too much volume into thin books, recoverable by scaling those three down to 0.5-0.7x, not
by changing wheat or the crop mix.

## Table 7 — op census

```
-- ALL WIN SEATS (leaders_0808) --
                  PASS   20,254   15.0%
                  WEST   18,646   13.9%
                 WATER   17,830   13.2%
                 NORTH   17,415   12.9%
                  EAST   13,378    9.9%
                 SOUTH   11,101    8.2%
               HARVEST    7,072    5.3%
                  CARE    6,246    4.6%
                  FEED    6,213    4.6%
    COLLECT_FERTILIZER    6,083    4.5%
                 PLANT    3,294    2.4%
                PICKUP    3,004    2.2%
             FERTILIZE    1,654    1.2%
                  DROP    1,330    1.0%
                   DIG      494    0.4%
                 PLACE      313    0.2%
         BUILD_PASTURE      293    0.2%

-- OUR LOSS SEATS --
                  PASS    3,258   21.6%
                  WEST    1,992   13.2%
                 NORTH    1,753   11.6%
                  EAST    1,328    8.8%
                 WATER    1,168    7.7%
                 SOUTH    1,072    7.1%
    COLLECT_FERTILIZER      836    5.5%
                  CARE      799    5.3%
                  FEED      765    5.1%
               HARVEST      659    4.4%
                PICKUP      658    4.4%
                  DROP      351    2.3%
                 PLANT      162    1.1%
             FERTILIZE      155    1.0%
                   DIG       61    0.4%
         BUILD_PASTURE       42    0.3%
                 PLACE       41    0.3%
```

**Our PASS share (21.6%) is well above the leader-seat average (15.0%), and our WATER share (7.7%)
is well below it (13.2%)** — we idle more and tend crops less, proportionally, than the field. This
is consistent with (and adds a fresh number to) `geometry_of_the_herd_2026-08-09.md`'s footnote on
these same two episodes: "PASS 1512 vs 1005 and 1746 vs 354, WATER 578 vs 930 and 590 vs 1133,
PLANT 81 vs 174 and 81 vs 163 — not where the pens sit." That doc flagged this as outside its own
scope (it was investigating geometry); it is squarely inside this document's scope (mix and
activity), and it means our two actual opponents plant roughly **twice** what we do over the
season (174 and 163 vs our 81 each) while passing far less. This is not explained by crop *tile*
mix — it is idle capacity: turns spent doing nothing instead of watering or replanting.

## Table 8 — final animal pen totals across WIN rows

```
     COW: [7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9]  mean=8.0  median=8.0
   SHEEP: [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 10, 15]  mean=6.7  median=6.0
   GOOSE: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  mean=0.0  median=0.0
  our losses:
    91229682: COW=13 SHEEP=8 GOOSE=0
    91231728: COW=9 SHEEP=7 GOOSE=0
```

Every real herd in this sample — Seb's included — stays well under the corrected model's 16/16
flat point for cow and sheep, and nobody fields a goose. **The model is not contradicted here; it
is untested past a boundary nobody approaches.** Goose's "flat from 8" claim similarly cannot be
checked: n=0 across every leader seat and both our losses.

## Table 9 — season PLANT-op totals across WIN rows, by crop

```
       MELON: n_nonzero=20/20  values=[20, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 25]  mean=23.9
  STRAWBERRY: n_nonzero=20/20  values=[40, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43]  mean=42.0
       WHEAT: n_nonzero=20/20  values=[22, 25, 103, 103, 105, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108]  mean=98.9
      CARROT: n_nonzero=0/20  values=[0]*20  mean=0.0
      TOMATO: n_nonzero=0/20  values=[0]*20  mean=0.0
  our losses (season PLANT ops):
    91229682: STRAWBERRY:41, WHEAT:24, MELON:16
    91231728: STRAWBERRY:41, WHEAT:24, MELON:16
```

**CARROT and TOMATO are planted by zero of the 40 leader seats.** Both are, however, planted by
one of our two actual opponents (`As Wasti`, CARROT 40 + TOMATO 6) — the field this 20-episode
sample describes is not the whole field.

---

## Cross-check against `kagg/search/scheduler.py`'s saturation model

Mid-season snapshots (day 15 / day 20, where concurrent-tile counts are meaningful — see Method
note) against the corrected numbers in `docs/what_saturates_and_what_does_not_2026-08-09.md`
(8 melon tiles, 16 cows, 16 sheep, 8 geese):

```
                              day 15                          day 20
v23-clone (kakuteki)  WHEA:7  STRA:42 MELO:12  COW:8 SHEE:6    WHEA:7  STRA:42 MELO:12  COW:8 SHEE:6
Seb (90850170)         MELO:18 STRA:39 WHEA:1  SHEE:14 COW:7   MELO:7  STRA:40 WHEA:1   SHEE:15 COW:7
Seb2 (90851845)         --                                     MELO:8  STRA:43 WHEA:1   SHEE:10 COW:9
our loss1 (91229682)  MELO:13 STRA:40 WHEA:1   COW:13 SHEE:8   MELO:3  STRA:40 WHEA:1   COW:13 SHEE:8
our loss2 (91231728)   --                                      MELO:3  STRA:41 WHEA:1   SHEE:7  COW:9
```

**Melon concurrent tiles range 3-18 across the sample** (it cycles through plant/harvest, so a
single snapshot catches it at different points in the cycle) — this brackets the model's 7.3-8
tile saturation estimate reasonably rather than contradicting it. **Strawberry sits at 39-43 tiles
for every single build in this cross-check, including ours** — the most stable number in the
entire dataset, and one we already match closely (our schedule plants 41 strawberry tiles). **Wheat
concurrent tiles are ~1 for everyone at mid-season** despite the mirror baseline's 108 season
PLANT-ops — wheat is being replanted in small, frequent batches rather than held as standing
acreage, which is a *cadence* fact the season-total table (Table 9) alone would not show.

**Cow and sheep counts (Table 8) never approach the model's 16-head flat point for anyone in this
sample.** The model's claim that a cow's flat-max value ($1,164/head) exceeds a sheep's
($897/head) is not contradicted by anyone's head *count*, but it does sit in tension with Seb's
*ratio* — the only build that consistently wins runs more sheep than cows (15:7, 10:9), while our
schedule and both loss episodes run more cows than sheep or a near-even split (13:8, 9:7). The
scheduler's per-head model has no term for this (it prices each species independently, not as a
joint allocation with a shared budget), so it cannot currently explain or rule out Seb's ratio.
**This is the one open, unresolved economic tension in this document** — flagged, not resolved.

---

## Answer: do we need a new schedule?

**No — not a new day-0-10 tape.** Three independent pieces of evidence converge on this:

1. `we_oversell_into_a_contested_book_2026-08-09.md`'s own-opening-vs-tape-opening test: **our own
   planner driving from day 0 loses 0/6 seeds; the Seb-tape opening wins 4/6.** Replacing the tape
   with something built from scratch has already been tried and lost every seed.
2. This document's Table 1/5/9: on the levers that are cheap to compare — land days, crew ramp,
   strawberry tile count — **our schedule already matches the one demonstrably-winning build in
   this sample** (Seb), not the mirror baseline. There is no material crop-*mix* gap to close by
   rewriting the tape.
3. `geometry_of_the_herd_2026-08-09.md`, run on these exact two loss episodes, already ruled out
   pen placement and walking distance as the cost.

**What the evidence does point at, concretely, none of which is "write a new opening":**

- **Herd ratio.** Test shifting the schedule's animal allocation toward sheep (Seb runs
  roughly 1.5-2 sheep per cow; we run the reverse). This is a parameter change to
  `data/seed_scripts/new_leader/schedule.json` / the embedded `_PLAN_JSON`'s `animals_bought` rows,
  not a new tape — and it should be tested on bank/win-rate, not assumed, because the scheduler's
  own per-head economics currently argue the opposite direction and that tension is unresolved
  (see above).
- **Post-handover planting volume.** Both loss episodes plant almost nothing new after day ~12
  (Table 2), while both real opponents that beat us plant roughly double our total over the season
  (Table 7's PLANT counts, corroborating `geometry_of_the_herd`'s own PLANT figures on the same
  episodes). This is a live-planner behavior question — is there unclaimed land or unused hand
  capacity sitting idle in the second half of the season? — not a tape-content question, since the
  tape only covers days 0-10 in the first place.
- **Sell-side volume on MILK, STRAWBERRY, WOOL.** Already measured and quantified in
  `we_oversell_into_a_contested_book_2026-08-09.md` (12 of 14 real losses become wins by scaling
  those three products to 0.5-0.7x, recovering $7k-$33k per game). This document's own selling
  table does not contradict that finding and adds one clarification: **wheat's high order count is
  not part of the problem** — its realized price is fine, matching the existing doc's own verdict
  that wheat needs no correction.
- **Field diversity beyond the 20-episode sample.** Our own two losses were against a mirror-
  baseline-style opponent and a five-crop CARROT/TOMATO opponent, *neither* of which appears as a
  winning build inside the 20-leader sample itself. Beating Seb's tape (which our schedule is
  built from) is not the same as beating the field, and this is worth remembering before reading
  too much into any Seb-vs-tape win.

## Gaps — explicitly flagged, not papered over

- **n=2 for Seb** and **n=2 for our losses**. Every Seb-specific and loss-specific number above is
  a two-episode measurement; treat magnitudes as indicative, not precise, and do not further
  subdivide them.
- **The herd-ratio tension (cow-favoring model vs sheep-favoring winner) is not resolved.** It
  needs either a joint-allocation version of `revenue_rate`/`best_revenue` that shares a budget
  across species, or a direct bank/win-rate sweep of the schedule's cow:sheep ratio — neither was
  run here.
- **The realized-price numbers in Table 6/6b use the market price snapshot at the turn the SELL
  order was submitted**, not a confirmed fill price from the order book resolution. This matches
  the approximation used elsewhere in this project's analyses but is not exact; treat mean-price
  columns as directionally reliable, not to the dollar.
- **Whether the "idle after day 12" pattern (Table 7, PLANT counts) is a hand-capacity problem, a
  land problem, or a scheduling-logic problem was not diagnosed here** — only measured as present
  on both loss episodes and absent (or much smaller) for both real opponents that beat us. That is
  the next thing to trace, not something this document had time to trace itself.
