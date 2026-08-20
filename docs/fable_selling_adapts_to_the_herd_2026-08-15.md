# Selling adapts to the herd we actually have — findings, 2026-08-15

Task: make the selling adapt to the herd we actually have, from day 8 onward, without moving a single d0–d8 cell on the kawashigi tape grid.
Everything below was measured at `af3db5d` on `kaggle-environments` **1.32.7** (the venv held 1.32.6 and was upgraded first; the reference's `hinge` curve is now in the installed env too).

## 1. Can the tape grid detect a herd-adaptive sell rule at all?

**Yes — but only a rule that adapts the DAY TOTAL. The prior attempt adapted a term that never governs, and that is the whole story of its null.**

Two measurements settle it, both on the tape fixture (kawashigi, seed 11, weeds 0):

**(a) The herd genuinely diverges on the tape — the "our herd ≈ his herd" reading is wrong.**
Dusk board counts, our seat, versus the schedule's cumulative `animals_bought`:

    day    ours C/S    schedule C/S
     8       6/4          6/4
     9       6/4          8/4
    10       6/5          8/4
    11       6/6         10/4
    12       6/8         10/4      <- and stays 6/8 to d16

`SHOP_ADAPT_HERD` re-species the schedule's last four cow purchases into sheep on this board's shop draw.
From d12 we run COW 6 / SHEEP 8 against the COW 10 / SHEEP 4 the `sells` rows were recorded from.
So a herd-adaptive rule has a real signal to read on this fixture; the tape is **not** null-by-construction for the hypothesis in general.

**(b) Why the previous fix (subtract herd production from `still_owed`) was byte-identical anyway.**
A temporary env-var-gated trace at the `n = min(have, allow, rate)` computation, every turn of d0–d16 (3,672 sell computations), attributing each offer to its binding cap:

    MILK: 408 turns traced        WOOL: 408 turns traced
        shed empty        290         shed empty        321
        have (all stock)  103         have (all stock)   65
        day total spent    14         day total spent    12
        allow (day total)   1         allow (day total)  10

`still_owed` can only act through `allow = max(today + carry, have - still_owed)`, and `have - still_owed` sits at **6–18 in hand against 100–267 owed** on every traced turn — deeply negative, so `allow` is always `today + carry` on the whole 17-day grid.
The code's own comment ("the whole-season reserve only becomes binding on day 25") is confirmed by measurement.
Any modification to `still_owed`, herd-aware or not, is invisible on this horizon.
**The null was a property of the term chosen, not of the instrument.**

What CAN move: `have` binds on 103/118 non-empty MILK turns (our 6-cow herd under-produces his rows here — no milk surplus on this fixture), but WOOL stock is held back on 22 turns with the day total binding on ~22 — our 8 sheep produce roughly twice what his 4-sheep rows release.
A rule that widens the animal day total therefore moves the tape grid from d10 (first held-back wool), and it did — see §3.
The *size* of the effect on the tape is small; the field is still where the divergence is worth money.

## 2. The change

`kagg/search/schedule_agent.py`:

- `SELL_ADAPTS_TO_THE_HERD = True`, `HERD_SELL_FROM_DAY = 8`.
- `_herd_daily_rate(tiles)`: units/day the current herd adds to the shed, per product — `(1 + interval)/interval` per animal (a production day banks 1 base unit plus one care bonus per fed-and-cared day, `reference/kaggriculture.py:822-828`; our routine feeds and cares the whole herd daily).
- In the sell loop, a third `max` arm on the day total, animal products only:
  `allow = max(allow, _herd_daily_rate(tiles)[prod])` from day 8.

Guard-rails, against every recorded failure in this region:

- **`max`, never a cap** — a row asking more still fires in full; the refuse-to-sell arm (−$16,025) is unreachable.
- **`rate[prod]` per-offer bound untouched** — the one-turn dump that took mean money $111,238 → $77,587 is unreachable; stock leaves spread across turns and days.
- **FERTILIZER unreachable by construction** — `_herd_daily_rate` keys off `ANIMALS[..]["product"]`, which is MILK/WOOL/EGG only.
- **`n = min(have, ...)` still caps at the shed**, so the rate estimate can never oversell stock that does not exist.

## 3. Red-first test

`tests/test_the_sell_day_total_tracks_the_herd_we_actually_have.py` — two asserts:

- `test_the_herd_rate_is_read_off_the_board`: 6 cows + 8 sheep → MILK 9/day, WOOL 11/day, crops absent. Red first (`AttributeError`, function did not exist), green after.
- `test_a_row_from_his_herd_does_not_cap_milk_below_our_herds_rate` (slow, full env, seed 11 vs the kawashigi tape): schedule's MILK rows shrunk to 1 on d11–d13 **and zeroed on d8** — the d8 row would otherwise go down as missed and the carry would release 12 units whatever the day total says; the first fixture made exactly that mistake and passed on the old code. Red: **3 units filled** (the row's 1/day). Green with the floor: the shed's ~6/day clears.
- Revert check: flag forced `False` → the behavioral test goes red again (3 < 10). Restored `True`.

## 4. The 17-day grid, baseline vs floor — d0–d8 unchanged

Cell-level diff of the two grids: **95 changed cells, zero in d0–d8, zero in d9; first change is d10** (`sell 86/91 → 89/91` — wool the herd makes and no row names).
The tape side of every changed cell is identical, as it must be.
Both full tables are pasted in the task report; logs:

- baseline: `data/logs/baseline_breakdown_17d.log`
- floor on: `data/logs/herdfloor_breakdown_17d.log`

Notable cascade effects on the tape fixture (diagnostic only — selection is win rate):

- d10 close $13,218 → $13,913 (+$695, early wool).
- d11 feed/care/collect_fert move onto the tape's numbers (13/14 → 14/14, 11/12 → 12/12).
- d15/d16 weeds 2 → 1.
- d16 close $32,794 → $32,250 (−$544 at the horizon's edge; day totals redistribute).

## 5. The field — win rate against recorded ladder opponents

(filled in below when the sweep lands)

## 6. Nulls and losses recorded on the way

- The predecessor's `still_owed`-subtraction fix: byte-identical on both tapes — explained mechanically in §1(b), and the explanation ("herds match on the tape") that came with it is refuted by §1(a).
- First behavioral test fixture: passed on the old code because the d8 MILK 12 row was left standing and the carry released it on d11–d13. A fixture that owes a missed row cannot isolate the day total.
