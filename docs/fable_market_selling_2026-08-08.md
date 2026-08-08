do # Fable: market selling, 2026-08-08

Agent `a58cf8c35f1f2b12d`.
**The agent deadlocked before writing its own report** -- it stopped six times to "wait for the
background task notification", which only fires *after* it stops, so it never resumed to write up
the run it had already finished.
This file is reconstructed from what it left on disk: the code it shipped, the docstrings it wrote,
and the two arena logs.
Nothing here is inferred; every number is quoted from an artifact named below.

**Status of the work: `PRICE_AWARE_SELL_CAP` ships OFF (`kagg/search/schedule_agent.py:883`).**
Nothing of this is live.

## The claim

`allow` -- the ceiling on how much of a product we will sell across a whole day -- is derived from
`still_owed` / `carry`, which are keyed to the day total *the tape's schedule row asked for*.
That row was transcribed off `data/seed_scripts/top_guys/90976060/schedule.json`, a **1.32.2** tape.

So it is a fact about one replay's production, not a fact about what the market can absorb.
`market_price` is public and exact (`kaggriculture.py:179`), so whether a product is glutted does
not have to be guessed from a copied number.

The symptom, from `docs/brief_market_selling_2026-08-08.md`: top 1.32.6 plans sell **305-649 WHEAT**
across a season.
We sell **71**.
Not because the market refused it -- because the row we imitate never asked for more.

## The measurement that matters: the price curve is per-product

Measured on five of **our own live 1.32.6 ladder games** (`data/seed_scripts/ours_1326/`, three wins
and two losses, against opponents that react -- not against a tape).

| product | realised price | volume | same game / comparison |
|---|---|---|---|
| WHEAT | $46.8/unit | 1,105 units | game `91041929` (a loss) |
| WHEAT | $47.8/unit | 125 units | game `91041864` (also a loss) |
| MELON | $75.6/unit | 120 units | vs opponent $112.4/unit at 144 units |

**WHEAT holds its price at nearly nine times the volume.** Its own-tile production is small next to
the town-plus-shop drain, so the curve barely moves.
A day-total quota on wheat is throttling a product the market was never close to flooding.

**MELON is the opposite and is why this must be a per-product PRICE test rather than a blanket
removal.** It has no shop at all, and it is the one product that visibly responds to volume --
`scripts/measure_sell_timing_impact.py` had already found seven products cleared and *rose* all
season while melon alone glutted, base 250 -> $150.

## The trap: two caps, and only one of them is a replay artifact

- `allow` -- **the day total.** A fact about one replay. Safe to drop when the live price says the
  product is not glutted.
- `rate[prod]` -- **the size of a single offer.** A real market fact. Must not move.

The first version of the flag dropped both at once (`n = have`, uncapped).
The arena caught it (`data/logs/price_aware_arena_2026-08-08.log`, seeds 500-505):

```
baseline (flag OFF)        win 94.4%   mean $111,238
PRICE_AWARE_SELL_CAP=True  win 94.4%   mean  $77,587
```

**Win rate identical, mean money down ~30% against every single opponent.**
A large `have` right after a harvest lands goes out as one order and walks its whole size down the
price curve in a single turn's lockstep, instead of being spread across turns the way `rate[prod]`
has always spread it.
This is the same dump shape already recorded on wool in `LIQUIDATE_FROM_HOUR`'s docstring:
123 units -> 138 units took revenue **$29,041 -> $21,811**.

## The corrected version: neutral

Only `allow` moves; `rate[prod]` still bounds every single offer even when the flag fires.
`data/logs/price_aware_arena_v2_2026-08-08.log`, same seeds:

```
baseline (flag OFF)        win 94.4%   mean $103,932
PRICE_AWARE_SELL_CAP=True  win 94.4%   mean $102,095
```

Within seed noise. No reason to turn it on, and no reason to delete it.

**Read the win rate carefully: 94.4% with `mirror` at 50% means the pool is saturated.**
Every non-mirror opponent loses 100% of the time either way, so the pool *cannot* discriminate
these two variants -- mean money is the only signal available, and it says nothing happened.
A flag that is neutral on a saturated pool has not been tested against a real opponent.
Against Seb's 1.32.6 tape we still lose.

## What shipped

- `kagg/search/schedule_agent.py:883` -- `PRICE_AWARE_SELL_CAP = False`, and the branch at ~2125.
- `tests/test_price_aware_sell_cap.py` -- 5 tests, all passing. One per claim, including the
  flag-OFF byte-identity rail and the `rate[prod]` invariant the arena caught.
- `kagg/agents/_price_aware_baseline.py`, `kagg/agents/_price_aware_probe.py` -- probe agents that
  set the flag, used only to run the two arena arms.
- `data/logs/price_aware_arena_2026-08-08.log`, `..._v2_2026-08-08.log`.

## What this does not answer

The pool cannot see the difference, so the flag is unevaluated where it counts.
The open question is not "is `allow` a replay artifact" -- it is, and that is now measured -- but
what the sell *program* should be.
See the fertilizer and hand-carry findings from the same day: Seb's market behaviour is a
continuous small-sell/small-buy working-capital cycle, and grafting it wholesale onto our board is
worth +28% on seed 11 (`data/logs/graft.log`).
