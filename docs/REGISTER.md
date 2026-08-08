

# Register — what is open, what is closed, and what keeps reopening

Last updated 2026-08-08, on `shaping-potential` at the three-branch merge.

This file exists because items in this project get closed under one name and reopen under another.
Melon has been opened and closed at least four times.
Before opening anything, check the CLOSED section — and check whether your item is really OPEN-1 wearing a new label.

Ground rules for this file:

- An item is CLOSED only if there is a measurement or a test that would go red if it came back.
  "We tried it and it seemed fine" is not closed.
- Every claim here names the file that proves it.
  A claim with no artifact is marked UNVERIFIED and must not be quoted as fact.
- The reference tape is a **diagnostic**, not the goal.
  Beating it is the goal, so "the tape doesn't do this" is never an argument against a change.

---

## The thing that keeps reopening

**OPEN-1 is one defect that has been worked under at least six different names.**

Melon timing, the stranded carrier, the return leg, the delivery node, the sell-row delivery, and
"shed to shop" are all the same failure: **product is harvested late in the day and is still in a
unit's hands at dusk, so it reaches the shed via the overnight sweep and cannot be sold until
tomorrow.**

Each label got investigated, partially disproved on its own terms, and closed — and then the defect
resurfaced under the next label, because what was disproved was that particular *mechanism*, never
the *symptom*.
That is why it reads as "opened and reopened like mad and never solved".

Seven separate arms have been attempted against it and all seven were reverted.
**All seven were judged on season totals**, which is the wrong metric (see SELECTION RULE below), and
none checked field-by-field whether the arm moved the field it targeted.
So "seven failures" is much weaker evidence than it sounds.

Anything that looks like late selling, idle hands at dusk, product sitting in inventories, or a
missed same-day sale belongs to OPEN-1. Do not open it as a new item.

---

## OPEN

### OPEN-1 — DIAGNOSED, NOT FIXED. The WATER ran seven hours late, not the delivery

Owner: open. Commit `4df96e2`, merged. See `docs/harvest_ordering_2026-08-08.md`,
`scripts/when_the_melon_fills.py`, `tests/test_the_filling_water_carries_the_harvest.py`.

**Status is deliberately "diagnosed", not "solved".** The cause is established and the arm helps the
day it targets, but it costs more on the days after it than it gains:

```
money      d10     d11     d12     d13     d14     d15   |  season   cells
before   -3082    -422   -1014    -227    -172    +230   | -103724     414
after    -1548   -1516   -3107   -1567   -1564    -732   | -106686     419
```

Target day **+$1,534**. The five days after it **−$8,700**. Season **−$2,962**, five more differing
cells, and `sh:melon` overshoots from `+24` to `−24` — we went from holding too much melon to
holding too little.

Under the SELECTION RULE that is a good fix for d10 with a later-day problem of separate origin
(OPEN-11), which is why it is merged rather than reverted. But the register does not get to call
this closed, and an earlier draft of this entry did. The diagnosis below is what is genuinely
banked; the arm is provisional.

**Six labels and seven reverted arms all pointed downstream of the real cause.**

```
hour each ripe MELON tile first fills 6/6 and becomes harvestable at all
SEB   (4,2) h6    (3,1) h9    (4,1) h9
OURS  (2,0) h15   (1,0) h16   (0,0) h18
```

Both sides wake on d10 with the same three tiles at **5/6**.
MELON is a one-shot and `_one_shot_is_finished` refuses HARVEST while `room > 0` — correctly, since
HARVEST demolishes the tile.
So **neither side could harvest before the fill**, and our harvests at h17/h19/h20 land one to three
turns *after* our fills.
The harvest was always prompt. The drop was always prompt behind it.

The defect was the WATER. `crop_ops` priced an in-window one-shot water at the single unit it adds,
**$250**, while an out-of-window survival water on an *immature* melon priced at `_crop_remaining` —
the whole tile, **$1,250–$1,500**.
The planner therefore ranked insurance on a tile that could not yield for two more days at
**six-to-one** over the one water that unlocks same-day cash.

Fix (`FILLING_WATER`): when a water fills the tile, the node also offers the HARVEST it unlocks.
No new mechanism — `_live_ops` already emits WATER then HARVEST at the same stop next turn.

Day 10, the day it targets: `money -3082 -> -1548`, `sh:melon +12 -> 0`, fills
`h15/h16/h18 -> h10/h15/never`. **d0–d9 byte-identical.**

Reverting the flag turns 2 of 3 new tests red. The third passes either way *on purpose*: it proves
the WATER→HARVEST pair was always executable, i.e. execution was never the defect.

A rejected arm is recorded at the emission site: pricing the harvest at `held` rather than
`held + gain` is the strictly correct marginal, and it gives back the entire gain, because an
immature melon's survival water prices at *exactly* $1,500 too and the surplus $250 is the only
thing breaking the tie.

**Lesson for the register:** every one of the six labels described a *symptom at a later leg*. The
question that cracked it was asked about the **tile**, not about the unit, the route, or the shed.

### OPEN-11 — Survival water is never discounted for how far off the yield is

Owner: nobody. Split out of OPEN-1, d11 regresses `-422 -> -1516` with `weeds +3`, `strawb -3`,
`water -3`.

`_crop_remaining` prices a survival water as the whole tile regardless of how many days away that
tile's yield is, so insurance on an immature crop is never discounted for waiting.

Do **not** fix this by weakening `FILLING_WATER` — that is precisely what the rejected arm above did,
and it gave back the whole d10 gain.

This is almost certainly the same mispricing behind OPEN-10 (strawberries dying eleven days early):
a survival water that is over-priced early is also over-priced late.

### ~~OPEN-1 (original framing) — Harvest lands too late in the day to be sold~~

Kept for the audit trail. Task #13.

The measurement, `data/logs/melon_d10_side_by_side.log`, day 10, seed 11, weeds off:

```
SEB   h6 HARVEST, h9 HARVEST x2, h12, h14  ->  SELL 12 @h13, SELL 6 @h15
      MELON in shed at d11 dawn: 0      bank 3912
OURS  h17 HARVEST, h19, h20              ->  hands reach 18 at h21, never dropped
      MELON in shed at d11 dawn: 18     bank 3273
```

Same eighteen melons, same board.
He harvests in the **morning** and sells the same day; we harvest in the **evening** and bank it
tomorrow.
`money` at d10 on the merged baseline is **−3082**.

The reframe that has never been tested: every prior attempt asked *why do we deliver late*.
The trace says we also **harvest late** — his first melon harvest is h6, ours is h17.
If harvest ordering within the day is the cause, all seven prior arms were treating a symptom.

Related shed rows: `sh:straw −78`, `harvest −51`.
**`sh:wheat −139` was listed here as "probably the same defect" and it is NOT — see C-18.**

Dossier: `melon_reality_check_2026-08-07.md`, `fable_stranded_carrier_2026-08-07.md`,
`fable_return_leg_2026-08-07.md`, `fable_delivery_node_2026-08-07.md`,
`fable_sell_row_delivery_2026-08-07.md`, `idle_at_h10_2026-08-07.md`,
`service_undercount_2026-08-07.md`, and the reverted-with-numbers comments at the return leg in
`kagg/search/schedule_agent.py`.

### ~~OPEN-2 — `sh:wheat` first diverges at day 8~~  → CLOSED, see C-18

Not a defect. Two equally valid routing orders, and the day-8 −1 is fully accounted for.

### OPEN-3 — `sh:milk +464` and `buy_product −164`

Owner: agent running (opus, worktree). Task #21.

The two largest unowned rows on the corrected baseline.
We hold up to **+50** more milk in the shed than the tape at d22.
The tape **buys 164 more product units** than we do across 27 of 30 days.

Possibly one mechanism, not two: buy wheat → feed animals → produce milk.
The teardown of the top two agents (`episode_teardown_2026-08-03.md`) found the winner drew ~83% of
revenue from milk and wool by converting **bought** wheat into animal products.
So `buy_product −164` may not be a bug at all — it may be the one strategic play we never make.

Constraint on any fix: CARE correlates **+0.441** with money across 312 real leaderboard seats, so
"do less CARE" is not a safe inference from the diff alone.

### OPEN-8 — Two sheep STARVE on day 16  ← correctness floor breached

Owner: nobody yet. Measured 2026-08-08, `data/logs/two_missing_sheep.log`,
`scripts/the_two_missing_sheep.py`.

```
        d13  d14  d15  d16  d17 ... d28
OURS      9   11   11    9    9        9    empty_pens 0,0,0,2,2..2   in_shed 0
SEB       9   11   11   11   11       11    empty_pens 0 throughout
```

We reach eleven standing sheep on d14, **the same as the tape**, and then lose two between d15 and
d16.
The pens stay empty for the remaining fourteen days, nothing sits in the shed to refill them, and no
PLACE op is emitted again all season.

This is **not** a failure to buy and **not** the shed-stranding bug — it is a death.
It is the starvation floor, and the register's own rule says correctness floors are never traded
away.
It appeared as a consequence of fixing C-12: placing more animals filled 19 pens, and the feed
cadence cannot carry 19 pens.

Note the shape — this is the third time a fix has exposed a defect the old bug was masking.

CORRECTION on the record: this was first reported as "-2 from d10". That was a column-offset
miscount of the diff table. It is **d16**, and the `sheep` row is `an_SHEEP`, animals standing
(`breakdown.py:249`), not an op count.

### OPEN-9 — Milk is capped at the tape's sell rate, so the shed fills

Owner: folded into OPEN-3.

The mechanism, `kagg/search/schedule_agent.py:1649,1655`:

```python
n = min(have, allow, rate[prod])
n = min(n, allow - state["ordered"][("sold", prod)])    # allow = the schedule row for the DAY
```

We sell **exactly the quantity the schedule row names and no more**, however much the shed holds.
This is why "we sell every day" and "the shed has heaps in it" are both true and are not a
contradiction: the cap is Seb's production rate, and we produce more than Seb.

The row is an absolute count read off *his* trajectory. He reaches the last day holding little milk
having sold all season; we reach it holding four times the row.

A parked arm nearly fixes it — sell down to a `shed_dusk` target: `sh:milk` +446 → +46, and the
final bank lands within **$62** of his.
It costs d4 and d5, which currently match, via an unexplained `sh:wheat -2` from d4.
The obvious explanation (the WHEAT/FERTILIZER reserve being subtracted twice) was tested and is NOT
the cause. Left unfed until the cause is found. See the comment block at `schedule_agent.py:1630`.

### OPEN-10 — The strawberries die eleven days too early

Owner: nobody. Measured 2026-08-08, `scripts/thirsty_strawberries.py`,
`data/logs/thirsty_strawberries.log`.

A PLANT tile becomes a WEED at `consecutive_unwatered >= 2` (`reference/kaggriculture.py:753`).
Counting every tile transition across the season, both seats:

```
                 died of THIRST              first death
OURS   STRAWBERRY 41, WHEAT 2                d11
SEB    STRAWBERRY 41, WHEAT 1                d22
```

**The totals are identical.** Forty-one strawberries die of thirst on each side, so we are not
losing crops that Seb keeps alive.

The difference is entirely *when*:

```
OURS  d11 1, d13 1, d15 2, d16 3, d21 2, d22 5, d23 6, d24 4, d26 9, d27 3, d28 5
SEB                                        d22 3, d23 8, d24 8, d26 9, d27 3, d28 10
```

Seb loses his **entirely from d22** — the final week, when another watering cannot pay itself back.
That is a deliberate end-of-season abandonment, not neglect.
We start losing them at **d11**, when each tile still had ten or more days of yield left.

Same deaths, ours eleven days early. That is the whole of `strawb -94` and `sh:straw -78`.

This is NOT caused by the sheep-placement fix or by FEED_TURN_CAP — the first death is d11, which
precedes both.

### OPEN-4 — Idle diverges only when the board gets busy

Owner: nobody. Task #18.

`idle +427` over the season; `pass` is the same row.
It is small early and grows with board complexity: d5 +25, d9 +24, d10 +39, d27 +54.
d5 is the isolation point — 208 unit-turns and 9 pens, against d10's 294 and 15.

Recurring shape, observed twice and not yet explained: *early there is budget but no free unit; late
there is a free unit but no budget.*

### OPEN-5 — The PLACE gate is fitted to one seed

Owner: agent running (opus, worktree). Task #22.

`PLACE_IS_MANDATORY_FROM_DAY = 14` in `kagg/search/router.py` works and is a day number read off
seed 11.
The general rule is believed to be "this animal was already in the shed yesterday", which needs shed
age plumbed through `build_nodes`.

### ~~OPEN-6 — `weeds −174`: we beat the tape~~  → CLOSED, see C-16

We do not beat the tape here. We spend 35 unit-turns tidying up after ourselves.

### OPEN-7 — Merge to `main`

Task #24. Unblocked as of the green slow suite; see STATE below.

---

## CLOSED — with the artifact that would go red

Do not reopen these without new evidence that contradicts the named artifact.

| # | Item | Why it is closed | Artifact |
|---|---|---|---|
| C-1 | Melon "refuses to harvest" | `first_yield_day` is 10; a HARVEST below it is a no-op that still costs the turn. Our gate matches the env rule exactly. | `ruled_out_melon_harvest_gate_2026-08-06.md`, `router.py:243` |
| C-2 | "We never plant day 6's six melons" | FALSE. We buy 6 and plant 6, funded at h8 by a same-turn `SELL WOOL 6`. The probe simply stopped printing once the order landed. | `melon_reality_check_2026-08-07.md` |
| C-3 | "Day 6's melons are never harvested by d11" | Correct but not a defect — day 6 + 10 = day 16. Seb's own tape leaves its d6 batch equally unharvested. | `melon_reality_check_2026-08-07.md` |
| C-4 | "Melon is never sold, so land can't be funded" | 18 units sold at d11; it funds the $4,000 parcel same-turn. The first two parcels predate any melon harvest. | `melon_reality_check_2026-08-07.md` |
| C-5 | Milk is under-sold | FALSE. We meet every sell row the schedule names. We over-**produce**. The open question moved to OPEN-3. | commit `cdac079`, `tests/test_stock_the_schedule_never_names.py` |
| C-6 | Pens on the depot ring block delivery | Clean negative, 7 tests. | `pens_on_the_depot_ring_2026-08-08.md`, `tests/test_pens_do_not_block_the_depot_ring.py` |
| C-7 | PLACE is under-priced | Prize sweep 2×–10× changes nothing. It is a **budget** refusal, not a price. | commit `9a89ecd`; the superseded arm is in `git stash` |
| C-8 | `buy_seed +42` at d6 | Logging bug. `breakdown.py` counted offers; we re-offer every turn. Season total went to 0 once fills were counted. | commit `096d581` |
| C-9 | `sell` overstated 11× | Same root cause as C-8: 165 offers → 15 fills. Every number taken before 2026-08-08 used the wrong yardstick. | `breakdown_fills_not_offers_2026-08-08.md` |
| C-10 | d10 `tiles −25` is a lost quadrant | FALSE. It is a one-day delay; `tiles` is a dawn snapshot at the window edge. We buy the parcel on d10, same as the tape. | verified on this tree |
| C-11 | Feed bought in one block | `FEED_TURN_CAP = 6`; the herd bypassed the drip. Animals-in-pens went 17 → 18, not down. | commit `260db7a`, `tests/test_router.py` |
| C-12 | The sheep never get placed | Fixed. d14 sheep −2 → 0, place −2 → 0, d0–d13 byte-identical. | commit `9a89ecd` |
| C-13 | `sh:wheat −2` at d4 | Does not exist on our tree. It was a mis-relayed figure from an agent branch. | verified d0–d7 exact |
| C-14 | The tape idles 0 turns on day 1 | Harness artifact — the tape was replayed into seat 1 with truncated hands. Real figures 144/131. | test removed |
| C-15 | GPU thermal throttling | Ruled on and closed. Do not re-rank it into any review. | — |
| C-16 | `weeds −174` means we beat the tape | FALSE, and it is the opposite. Seb finishes with **42 weeds standing** and we finish with **8**, because we DIG ours (`dig +35`) and he leaves his alone. Weeded ground he was never going to replant costs him nothing; clearing it costs us 35 unit-turns. Final board: ours `WEED=8 empty=72`, his `WEED=42 empty=37`. | `data/logs/thirsty_strawberries.log` |
| C-18 | `sh:wheat −139` from d8 is a defect | NOT a defect. On d8 the `HARVEST` op count is identical (2/2) and the net market delta is identical (+10/+10), so "we harvest less" and "we sell more" are both ruled out. The −1 lives entirely in the DROP / dusk-sweep / PICKUP mix, and it is the OPPOSITE way round from the assumption: **the tape** holds 3 units until the dusk auto-drop; we drop mid-day. Two equally valid routing orders. Verified by an exact accounting identity — `start + DROP + dusk_drop + PICKUP + PLACE + market == end` — holding on every day for both sides. No fix written, deliberately: there is no defect to write a failing test against, and forcing our order to match would be cloning the tape. | `docs/wheat_d8_2026-08-08.md`, branch `worktree-agent-ad4be40e954a71ed5` |
| C-17 | Feeding the animals starves the crops of water | FALSE. Thirst deaths are **41 STRAWBERRY on each side**, ours 41 + 2 wheat, his 41 + 1 wheat. Feeding is not stealing waters Seb keeps. The real difference is timing, now OPEN-10. Also: the first strawberry death is d11, which precedes both the sheep-placement fix and `FEED_TURN_CAP`, so neither can be the cause. | `scripts/thirsty_strawberries.py` |

---

## SELECTION RULE — how to judge any arm

Alex's, and it governs everything above.

- Judge a fix at the **day it targets**, field by field.
- Target day improves → good fix, take it.
- A **later** day regresses → a different problem with its own origin. Log it, do **not** revert.
- An **earlier** day regresses → a question, not an automatic veto. It may mean the earlier fix was
  wrong and this change exposed it.
- Season totals and single-seed dollar swings are **weak** signals.
  Judging by totals is the error that ran through the whole late-delivery effort.
- Hard constraint: do not regress d0–d5. Their differing-cell floor is currently `3,3,3,5,3,3`.
- Correctness floors are not metrics and are never traded away. The herd must not starve — measure
  **animals in pens per day**, because a previous change collapsed that 17 → 8 and was nearly
  shipped on cells and money alone.

If the behaviour is now correct and a number got worse, the old bug was probably **masking** a second
defect that the change exposed. Reverting hides it again.

---

## STATE at last update

```
branch          shaping-potential @ b81f04b   (114 ahead of main; main has nothing we lack)
unpushed        93 on shaping-potential, 4 on main
fast suite      805 passed,  70 skipped, 7 xfailed, 0 failed
slow suite      240 passed,  25 skipped, 4 xfailed, 0 failed   (3m31s)
baseline        seed 11, weeds 0.0, tape seb, days 0-29
                0/30 days exact, 414/1020 cells differ, money total -103,724
                d0-d5 money exact except +1/-1 at d3/d4
```

Baseline command, and the only metric that counts:

```
python -u scripts/breakdown.py --tape seb --seed 11 --weeds 0.0 --days 30 --diff --no-moves
```

Market rows (`sell`, `buy_product`, `buy_animal`, `buy_seed`) are **fills**; everything else,
including `hire` and `buy_land`, is still an **offer**.
Fill rows are a lower bound — a turn dirtied by DROP/PICKUP/PLACE contributes zero — so confirm a
difference is real before explaining it.
