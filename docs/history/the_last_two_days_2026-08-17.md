# The last two days: what was dead, what was fixed, what is still open

Measured 2026-08-17, branch `kawashigi-plan`, seed 11, shipped `kawashigi` plan.
Grids: `data/logs/d29_baseline_2026-08-17.log`, `data/logs/d29_after_2026-08-17.log`.

## The mechanism

`_end_of_day` runs `_drop_inventories_to_shed`, so a load carried at dusk reaches the shed for free.
On d29 that same drop lands AFTER the final `_process_market` (`kaggriculture.py:942` then `:946`),
so produce held at the close is discarded and produce left standing is never money.
d28 is therefore the last day a harvest banks itself.

## Two things were dead or stale

**`banking = False`** (`schedule_agent.py:137`) gated the d28 "bank the field" branch on a hardcoded
False, pointing at a `BANK_THE_FIELD_ON_D28` constant that no longer existed anywhere in `kagg/`.
It measured a null originally because d28 is a SOLVED day with slack, so promoting a ripe tile into
the at-risk set changed no route.
Deleted; the deadline belongs in the price, not in that set.

**The stranded-load gap is CLOSED.**
`test_the_season_does_not_end_with_the_crew_holding_sellable_goods` was `xfail(strict=True)` over 51
units (~$1,192).
It went XPASS: the marker did its job and reported the day had landed.
d29 `drop` is now 9/9 against the tape.
`NO_UPKEEP_ON_THE_LAST_DAY` freed the turns and `cover.MATCH_THE_LAST_DAY_STOP_ON_ITS_TILE` reseated
the reduced stop; both halves the old note asked for.
Marker removed so a regression is a plain failure.

## The one real gap, implemented

A ripe **pen** on d28 was never promoted.
A crop reaches CRITICAL through `_last_safe_age` because it has a filling window that closes; a pen
has no such window, so nothing ever promoted it.
`router.animal_ops` now adds CRITICAL to a HARVEST prize on `SEASON_DAYS - 2`, d28 only.

Red first, on record in `data/logs/lastday_tests_2026-08-17.log`:
`d28 pen HARVEST priced at 640, below CRITICAL`.
All 20 last-day tests pass after.

## What it measured, and the ceiling it hit

    row          d25      d26      d27      d28        d29
    harvest    27/29    24/14    26/35    32/32      19/19      unchanged, before and after
    sell       95/149   87/80    92/72    84 -> 87   160 -> 159
    drop        2/0      2/0      0/0      0 -> 1     9/9
    pass        2/0      0/1      0/0      0 -> 13    22/56

    final money   154,740 -> 155,155   (+$415), tape 150,076

**d0-d27 money is byte-identical between the two runs**, so the delta is attributable, not seed
noise.

**Harvest did not move, and that is the finding.**
d28 and d29 are both in `SOLVED_DAYS` (12-29, `UNSOLVE_DAYS = ()`); d29 is a stored solution of 37
stops.
`_apply_precomputed` seats stops by their `(tile, ops)` key and never prices them, so changing a
job's prize cannot move a solved day -- it only reaches the leftover greedy.
The +$415 is that margin and nothing more.

**A price change to a solved day requires re-solving that day.**
`scripts/resolve_days.py --days 28,29` was running when this was written; its result is not in here.

## Traps hit today, recorded so they are not re-hit

- `scripts/diagnose_season.py` hardcodes `top_guys/90976060/schedule.json`, NOT the shipped
  `kawashigi` plan. It reports a $52k season against the real $155k. Numbers read off it early in
  this session were discarded.
- **Seeds do not vary this harness.** `--seed 11` and `--seed 14` produce a byte-identical grid:
  shops come from the replay, `--weeds 0`, and board terrain is a pure function of coordinates.
  A "second seed" check here is vacuous.
- `tests/test_the_second_to_last_day_banks_the_field.py` quotes d28 27/32 and d29 27/19 in its
  docstring. The live grid is 32/32 and 19/19 -- the back-loading it was written against is gone.

## Open: eight red tests in the planner gate

`tests/test_the_first_seven_days_match_the_plan.py`, 8 failed / 6 passed, and they PRE-DATE this
work (confirmed by stashing the edits and re-running).
They are live defects with coordinates, not test rot:

- a hand walks off a tile holding a hungry animal **while carrying its feed**, 14 times over d0-d6
- animals unfed at dusk with wheat on the farm: d0 leaves 4 hungry with 8 WHEAT in the shed
- a PLACE planned onto a hand that does not build that pen (d0, tile (4,3): BUILD u1, PLACE u4)
- SELL and BUY_PRODUCT diverge from the plan on d2-d6

## The four new losses are a different shape

`data/seed_scripts/ladder_2026-08-17/`, 23 replays now.
93850943 and 93849246 are byte-identical in every op count for BOTH seats -- same board, same
opponent script, different names. Three distinct games, not four.

                           water       harvest     plant      feed       care
    93850943 / 93849246   1221/1010    386/390    194/199    316/290    318/967
    93850122              1225/946     385/394    182/187    321/321    323/318
    93846497              1171/947     385/394    176/187    321/321    321/318

    93850943  vs kaggricultureomnidimensionalut  100,033/106,095  LOSS -6,062
    93850122  vs Пётр П                          125,613/131,285  LOSS -5,672
    93849246  vs Panchajanya Banerjee             54,940/ 60,306  LOSS -5,366
    93846497  vs Sirui Zeng                       89,509/ 98,615  LOSS -9,106

**Harvest is LEVEL in all of them.** These are not harvest-deficit losses, so the d28/d29 work in
this doc would not have flipped any of the four.
We out-water by 200-275, as in every game including the wins.
Plant is 5-11 behind.
One opponent runs CARE 967 to our 318 -- above the ~570 ceiling of one-per-pen-per-day, so it is
re-emitting CARE on already-cared pens; offers, not fills, and unchecked.

Losses of $5.4k-$9.1k against this morning's $158-$1,521.

**Correction on the CARE number above.** 967 is CARE EMITTED, not CARE landed. `cared_today` gates
the effect, so a repeat CARE on an already-cared pen is a silent no-op and at most one lands per pen
per day (~570 ceiling). It says their agent spams CARE. It does NOT say they care 3x more than us.
Same class of error as summing sell offers; see `feedback_offers_are_not_fills`.

## The herd never moves, and one board had ZERO milk shops

Milk slots counted from the FINAL town draw; cow/sheep counted off the final board.

    game       milk slots   our herd            their herd          result
    93849246       0        COW 10 / SHEEP 4    COW  8 / SHEEP 4    LOSS -5,366
    93846497       2        COW 10 / SHEEP 4    COW 10 / SHEEP 4    LOSS -9,106
    93850943       3        COW 10 / SHEEP 4    COW  8 / SHEEP 4    LOSS -6,062
    93839424       3        COW 10 / SHEEP 4    COW  9 / SHEEP 4    LOSS   -158
    93836751       3        COW 10 / SHEEP 4    COW 10 / SHEEP 4    LOSS -7,727
    93850122       5        COW 10 / SHEEP 4    COW 10 / SHEEP 4    LOSS -5,672

**We run 10 cows / 4 sheep in all six, across milk slots of 0, 2, 3, 3, 3 and 5.**
The split never moves.
On 93849246 the town draws NO milk shop at all and we still stock ten cows -- milk floors at $1 with
zero drain and we flood a book with no buyer.
The opponents do vary (8 cows on the milk=0 board, 10 on milk=5), though not cleanly monotone: at
milk=2 they also run 10.

This is `MILK_POOR_SHOP_COUNT = 1` again, now with a milk=0 board proving it does not fire.

**Caveat that has to be checked before acting.** Milk slots here are the FINAL town; the herd is
committed around d3-d7 when few shops have unlocked. This is not yet evidence the decision was
knowable at the time it was made. Measure the shop set AT the herd decision before changing the
rule.
