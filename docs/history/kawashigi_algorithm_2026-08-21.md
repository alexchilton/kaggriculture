# What Kawashigi's season actually is

> **RETRACTED, same day: the middle is NOT board capacity.**
> Measured over 2,982 mid-season day-rows — `docs/the_middle_is_not_board_capacity_2026-08-21.md`.
> He leaves 6+ tiles empty on **85.7%** of mid-season days and could afford the seed on 100% of
> them. `corr(wheat, free_at_dawn) = 0.274`, `corr(wheat, ever_free_that_day) = 0.507`.
> What binds is the **turn budget** — 53.6% of his day is travel, 31.9% of the work is watering,
> 5.6% is planting, and 43.4% of days have zero idle unit-turns. "Plant every reachable tile"
> would roughly double his plant count with no turns to do it.
> The **crop-mix** half of this document survives unchanged. The claim that d14–d27 therefore needs
> no row library is not disproved, but it is now **unsupported**.
>
> **Also retracted: the sample is 213 game-seats, not 228.** 167 episode ids sit in more than one
> directory under `data/seed_scripts/`, so fifteen of Kawashigi's games were read twice. Every
> distinct-row and coverage figure below is computed over 228 rows a day of which 15 are copies.
> The *shape* of the tables is unaffected; the exact counts are not exact.

Measured 2026-08-21 on **228 game-seats** of カワシギ, extracted from the downloaded replays in
`data/seed_scripts/kawashigi` and the daily episode datasets.

Source data: `data/target_rows_kawa_norm.json` (6,840 day-rows).
Scripts: `scripts/extract_target_rows.py`, `scripts/what_varies_in_the_row.py`,
`scripts/executor_label.py`.
Logs: `data/logs/what_varies_2026-08-21.log`, `data/logs/label_no_sells_2026-08-21.log`,
`data/logs/label_plan_only_2026-08-21.log`, `data/logs/mid_plants_2026-08-21.log`.

## The result in one line

His season is **a fixed opening, a wheat-fill middle, and a fixed close**.
The middle is not a plan at all — it is "plant wheat on every tile you can reach today", and the
number of tiles is a property of the board, not a decision.

## How the label was wrong four times

This finding was invisible until the label stopped carrying things the executor generates itself.
Each of the four removals below was proposed as "the fix" and only one of them mattered much.
The lesson is the general one: **anything the executor computes must not be in the label**, and
which fields those are is a question for `grep`, not for judgement.

`grep -o 'row.get("[a-z_]*"' kagg/search/schedule_agent.py` — the executor reads **ten** keys:

    seeds  hands  buys  sells  land  plants  shed_dusk  places  hires  animals_bought

It never reads `builds`, `feeds`, `cares`, `harvests`, `fertilises` or `clears`.
The router re-derives all six from the live board.

| removed from the label | reason | distinct rows at d16 |
|---|---|---|
| (nothing) | — | 127 |
| movement, watering | the router routes; `_live_ops` waters | (already out) |
| herd species COW/SHEEP/GOOSE | the herd algorithm reads the shop draw | 127 |
| the six derived fields | the executor never reads them | 125 |
| `sells`, `buys` | h16 cadence once the land is bought | 80 |
| `places`, `animals_bought` | the herd algorithm | — |
| **`seeds`** | **buy what you are about to plant** | **10** |

The species normalisation removed **15 rows out of 6,840**, all on d9 and d11 — the two days he
buys animals. It was proposed as the main fix and was nearly nothing.
The six derived fields removed **2 rows at d16**. Also nearly nothing.
`seeds` was the one that mattered: d16 47 → 10, d20 53 → 13, d25 170 → 60.

A field can vary a great deal per-row and still contribute almost nothing to the distinct-row
count, because it varies *in step with* another field. Drop-one measurement is the only way to
see this; per-field distinct counts are misleading on their own.

## What varies, per phase

228 seasons, label = the crop multiset only.

| days | distinct crop multisets | what it is |
|---|---|---|
| d0–d2 | 1 | identical opening, every season |
| d3 | 1 (2 with seeds) | the melon split |
| d4–d6 | 2–4 | |
| d7–d13 | 6–30 | genuine per-day variation |
| d14–d21 | 6–24 | **wheat only, count varies** |
| d22–d26 | 34–60 | wheat + 0–2 CARROT |
| d27 | 17 | wheat only |
| d28 | 1 | |
| d29 | 1 | |

## The middle is a scalar

The mid-season "distinct plans" are a single number. Day 16, all 228 seasons:

    72  WHEAT:5      14  WHEAT:7       4  WHEAT:12
    47  WHEAT:8       5  WHEAT:11      4  WHEAT:10
    31  WHEAT:9                        2  WHEAT:3
    29  WHEAT:4
    20  WHEAT:6

Day 27, same shape, counts 7 through 18. Day 20, counts 0 through 11.
The counts form a **contiguous unimodal run** — that is a capacity variable, not a menu of plans.

Day 22 and day 25 are the only mid-season days with a second crop, and it is 1–2 CARROT:

    day 25, top rows:   CARR:2 WHEA:10  |  CARR:1 WHEA:10  |  WHEA:11  |  CARR:2 WHEA:6

**No melon, no tomato, no potato anywhere in the middle.**

## What this means for the agent

    d0-d6     library rows                1-9 distinct         lookup
    d7-d13    library rows or small tree  12-30 distinct
    d14-d27   greedy planner, crop pinned to WHEAT              no library needed
    d22-d26   + 1-2 CARROT                trigger UNKNOWN
    d28-d29   library rows                1-7 distinct         already shipped
    all days  animals substituted by the herd algorithm from the live shop draw

The middle needs **no tree and no row library**. If the wheat count is board capacity, our
existing greedy planner already produces it, and there is nothing left to copy there at all.

## Open, not established

- **The wheat count is asserted to be board capacity from the shape of its distribution, not
  measured against free/reachable tiles.** This is the single most load-bearing unverified claim in
  this document. If it is wrong, the middle is a real decision and needs a model.
- **The d22–d26 carrot trigger is unknown.** The shop draw is the obvious candidate. Not measured.
- **Whether `seeds` is genuinely derivable from `plants` plus the shed.** If he buys ahead for the
  next day, the executor must look one row forward rather than compute from today's planting.
- Everything here is one player. Ryo Hasegawa and tetsuya are being measured separately; Ryo is
  already known to differ (no geese, Q3 not Q4, wheat 70% / carrot 54% / tomato 25%), so the
  wheat-fill middle may be Kawashigi's alone.
