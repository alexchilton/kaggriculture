# d16 `fertilize 6/13` is a d11-d14 selling decision, not a d16 routing bug

2026-08-12, seed 11, tape `victor`.
Found while looking for an easier problem than the d11 spawn-ring misprediction.

## Why d16 looked easy, and was the wrong day

```
d16  unit-turns 320/316   work 122/139   idle 60/49
     UNCOVERED 0          priced slack 96 turns
     offered:  WATER 39   FERTILIZE 12   HARVEST 11
     emitted:  WATER 50   FERTILIZE  6   HARVEST 11
     tape:     WATER 59   FERTILIZE 13   HARVEST 14
```

Nothing uncovered and 96 turns of priced slack, so the crew was neither busy nor failing to reach
anything.
The work simply was not doable.

## The mechanism

`_apply_unit_action` fails FERTILIZE **silently** on an empty hand — `if not _inv_take(inv,
"FERTILIZER", 1): return` (`kaggriculture.py:465`).
`_live_ops` re-derives at each stop, so a unit that arrives with nothing emits nothing and walks on.
The stop is planned, the walk is paid for, the fertilize never happens, and nothing reports it.

Per-unit on d16 — planned depot draw vs what actually reached the hand:

| unit | planned pick | got | FERTILIZE fired |
|---|---|---|---|
| u8 | FERTILIZER 3 | 3 | 3 of 3 |
| u3 | FERTILIZER 2 | 1 | 2 (one from a COLLECT) |
| u12 | FERTILIZER 1 | 0 | 1 (from a COLLECT at h10) |
| u13 | **FERTILIZER 6** | **0** | **0 of 6** |

Total planned draw 12. The units that reach the shed first drain it; u13 plans a six-unit draw
against an empty shed and walks six stops for nothing.

## The actual cause is four days earlier

Dawn shed fertilizer, ours/tape:

```
sh:ferti  d0 0/0  d1 5/5  d2 5/5  d3 5/5  d4 5/5  d5 5/5  d6 3/3  d7 7/7  d8 10/10  d9 12/12
          d10 15/15  d11 10/12  d12 4/9  d13 4/12  d14 1/12  d15 4/12  d16 10/12
```

We track the tape **exactly** through d10, then diverge and never recover.
`collect_fert` is `12/12` every day from d9 to d16 — identical production.
So it is not made differently, it is **spent** differently: the sell rows ask for
`FERTILIZER: 24` on d11, `14` on d12, `8` on d14, and we fill them out of the same stock the
fertilizing needs.

`fertilize` first goes wrong at **d12 (`2/3`)** — the day after the stock first diverges — not at d16.

## Why it is worth more than the op count

FERTILIZE sets `fertilized_until_day = day + 2` (`kaggriculture.py:468`), which doubles the yield
each WATER adds for three days.
A missed fertilize is not one op; it is every water on that tile for three days at half value.
That is part of why the `water` row also trails (`d16 50/59`) without any routing problem.

## The landmine to avoid

`cover.py:170-187` already records that refusing a job whose supply is short measured **worse three
times** — work down, idle up, d16 money 7,293 -> 3,280 -> 0.
`SUPPLY_LIMITS_EVERY_DRAW` is off for that reason, and the note ends: *"Turn this on only together
with a rule that raises the shortfall as a purchase."*

So the fix is NOT to refuse the stops.
The candidates, in the order I would try them:

1. **Do not sell fertilizer the day's own plan is going to spend.** The row is a target, not a
   command; reserve the planned FERTILIZE draw before filling the FERTILIZER sell quota.
   This is where the divergence is actually created (d11-d14).
2. **Buy the shortfall.** `BUY_PRODUCT` accepts FERTILIZER (`kaggriculture.py:585`), base price 100,
   and we hold $14,407 at dawn on d16 with 96 idle turns. This is the precondition the `cover.py`
   note names.
3. Cap the planned depot pick at the shed's real stock so the plan stops lying to itself, and give
   the surplus FERTILIZE stops to units whose tour already includes COLLECT_FERTILIZER.

## Artifacts

- `tests/test_a_fertilize_stop_is_given_the_fertilizer_it_needs.py` — RED at 12 planned / 6 emitted.
  Asserts the plan against itself, so it cannot be satisfied by lowering the target.
- `data/logs/why_idle_2026-08-12.log` — offered / uncovered / priced-slack for d11,12,14,16,18,19.
- `data/logs/fert_hands_2026-08-12.log` — the per-unit draw table above.
- `data/logs/shed_d17_2026-08-12.log` — the `sh:ferti` row.
- `data/logs/day16_fert_2026-08-12.log` — hour-by-hour d16, ours vs tape.

## Two other things the same run found

- **d18 has exactly one uncovered job: `(0,0)` `[WATER, FERTILIZE, HARVEST]`** — and d18 is where
  weeds go 2 -> 4 and `strawb` drops 35 -> 33. That one uncovered job is a tile dying.
- **d19 is where the season turns.** We lead $23,454/$22,551 at d18 and trail $26,215/$27,133 at d19.
