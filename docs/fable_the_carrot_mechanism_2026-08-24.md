# Fable, second pass: the carrot mechanism read off the tape

Verbatim, saved before relaying. Prompt: `docs/prompt_for_review_carrot_stuck_2026-08-24.md`.
Fable's own scripts and raw outputs are saved alongside as
`data/logs/tape_98495047.py`, `tape_98495047.log`, `scan_withholders.py`, `withholders.csv`.

---

# Answers, game 98495047 and the corpus

## Strongest disagreement: "it flipped ZERO games" is a statement about your harness, not about the rule

Two constructions make the acceptance run incapable of detecting a flip, and both are visible in your own section 5 table:

1. **The level bias exceeds five of the six margins.** The handover harness shifts every game by −$8k to −$20k (recorded −$614 → replayed −$11,885; −$3,472 → −$24,350). Five margins are ≤ $6,070. A lever whose true effect is +$2k-$6k cannot flip a game that the harness has already moved by −$10k. Only 98495047 (−$29,384) is measurable at all, and there the widened window already recovered $17,788; a residual −$5,313 inside a harness with −$10k-class bias is consistent with a real-world win.
2. **Control ≡ treatment by construction at d21.** At d21 the opponent holds 0 carrot tiles, so `CARROT_OPP_MAX` passes trivially and both gates fire. Then sizing doesn't differ either: at d21 the projection gives headroom ≈ 497, `units = 298`, `tiles = min(40, 74) = 40` — a budget larger than every planting the window will ever schedule, so the treatment's sizing never binds. You did not measure the deficit rule; you measured that two gates which agree at d21 agree at d21.

Fix the measurement before touching the rule: either a d24 handover, or a tape-vs-tape control arm per game so the level bias is subtracted, and grade on "enters d29 with ≥90 carrots in shed" as an intermediate assertion.

## Q1: the frame is right, and the tape proves it more strongly than you claimed

I checked every alternative you listed. Each dies on a number:

- **Crew turns / hires:** hands count and hires are **identical for both seats every single day of the season** (5,0,4,5,5,4,4,8,11,12,11,12,10,11,8,12,9,12×8,11×4,10,8). Days 4 and 7 are identical action-for-action, all 24 steps.
- **Land timing:** identical — both unlock NE at d6, SW at d11, neither buys SE. Money tracks within ~$30 through d10.
- **Sell cadence generally:** he flooded milk and wool to $1 exactly as we did (milk < $20 from d15 in this game). Milk: he sold 164 units for ~$2.9k, we sold 243 for ~$4.4k.
- **d24-d28 harvest:** his non-carrot season revenue is ~$52.7k against our ~$62.2k — he made **$9.5k less than us on everything that is not carrot**, because he sacrificed producing ground to grow it.

Full decomposition: carrot +$38.8k (77 units) vs our +$6.0k (14 units); everything else −$9.5k; net ≈ the $29,384 margin. This was a market play that *cost* him a working farm's output, and it paid ~3.5:1. The whole margin arrived in **one order**: `['SELL','CARROT',72]` submitted at d29 h0, executed as a walk from $517 down to $427 (+$33,936 in a single step including the wheat/milk/fert/wool riding along), after which the drain rebuilt the price to $498 by close. You have not mistaken something else for a market play.

One correction to your section 3 narrative: "d28: 0 carrot tiles, 76 held" — at d28 h0 he still had 24 tiles standing with 36 units on them; the shed shows only 16 carrots most of d28 because **his hands carried the harvest all day** (88 units in hand inventories at d28 h23) and deposited at the day boundary.

## Q2 / section 6: all four unexplained things, explained

**Where the 32 tiles came from.** 34 tiles, planted d22:1, d23:1, d24:8, d25:13, d26:11 (32 is a d27-h0 snapshot). Previous occupants: **13 WHEAT, 11 STRAWBERRY, 7 EMPTY, 2 CARROT, 1 WEED**. He tore out live strawberry beds (his strawberry sales: 152 units vs our 252) and wheat. No land purchase, no held-empty ground beyond 7 tiles.

**Why 2.4 units/tile.** Three reasons, none of them "harvest-turn limited":
- The carrot yield ceiling without fertilizer is **3, not 4**: `_new_plant` starts `yield_units = 1`; WATER adds +1 only at ages 2-3 (`reference/kaggriculture.py:431-444`), +2 only if fertilized. `YIELD_PER_TILE["CARROT"] = 4` in `corner_the_book.py` is the fertilized maximum, and `opponent_units()`'s `max(yield_units, 4)` overstates opponent supply by the same amount. d26-sown tiles can reach only 2 by d28.
- **~15 units were destroyed by shed overflow** at the d28→d29 boundary: shed 27 + hands 88 = 115 against cap 100; `_drop_inventories_to_shed` discards the excess. He overshot deliberately (planting slack against partial yields) and paid for it.
- So 76 banked ≈ the physical maximum of his schedule minus junk slots. Which leads to:

**The operative number is neither 32 tiles nor D=975. It is shed slots.** He entered d29 with the shed at exactly 100/100: 72 carrot + 28 junk (WHEAT 11, FERT 7, MILK 6, WOOL 4). Those 28 junk units sold in the same dump at ~$45 average while each displaced carrot was worth ~$470 — **he left roughly $12k on the table** by not clearing junk on d28 and filling all 100 slots with carrot. The play that beat us by $29k is itself ~$12k below its own ceiling. Tiles are derivative: `tiles ≈ (100 − junk) / expected_yield(sow_day)` with expected yield 3 for d24-25, 2 for d26.

**Deficit 975 vs ~850 — no missing mechanism, it is arithmetic.** First, a units fix: your "drain 11" is per *tick*; per day it is 67 (six PET_CAFE draws in this town: ×2 single-product, ×6 ticks/day, +1 town centre; ramp 13→25→37→43→55→67/day as they unlocked d3/6/15/21/24). Closed-form check: cumulative drain to d29 h0 ≈ 1,007, minus ~20 units both seats sold mid-season (his probe sells: 2 on d26, 3 on d27, 4 at d28 h23; our 11) = 987 vs observed 991. ✓. Your arms stall at 743-913 because **your own units go back into the book**: each sale adds +1 inventory, and your variants dumped 130-135 units against his 76 (−60 deficit) plus mid-window carrot sells. Abstention is not a separable "missing half" — it is the same accounting, and yes, your d21/22/24/25 carrot sells are refilling the book you are starving, but the bigger term is over-dumping at the close.

## Q3: when to read the decision

**Daily, from d22, with the size finalized at d24 h0 — never latched at the window's first day.** The information argument is exact: shops unlock at the end of days divisible by 3, capped at `MAX_SHOP_INSTANCES = 8`, so the **8th and final shop lands at end of d23 and the drain schedule is fully known at d24 h0** — and still in time to sow at yield 3 (d24-25) with a yield-2 tail on d26. SOUTA's ramp (1, 1, 8, 13, 11 tiles) is exactly what a daily re-read produces: token commitment while the roster is incomplete, bulk conversion beginning the day the sixth PET_CAFE appeared. SPECULATION: that correlation is in the tape but I cannot see his rule. Structure it as: re-read `plan()` each day of d22-d26, commit only *additional* tiles (`tiles_needed(day) = target_units/expected_yield(day) − already_committed`), never un-sow; and set `target_units = shed_cap − junk you will still be holding`, which also implies **sell the junk on d28**, a lever the winner himself missed.

## Q4: Elo against a field — measured base rates

Scan of all downloaded games, deduped by episode id: **1,792 episodes / 3,584 seat-rows** (one file skipped, `data/seed_scripts/top_guys/91023699-1.json`, different schema). Caveat stated up front: this corpus is Alex-selected and leader-heavy — these are base rates for *the field we actually meet*, not the whole ladder.

- Revenue share landing on d28+d29, opponents: p50 = 10.2%, p95 = 15.1%. Seats with ≥25% late share: **14 of 3,235 (0.4%)** — and 10 of those 14 won (71% vs 50.8% base).
- Seats holding **≥20 carrots in shed at d29 h0: 74 (2.3%), winning 64%**.
- Deep carrot towns (drain ≥43/day at d25): **4.2% of episodes**. Only **9.3%** of those contain a withholder (withholders win 75% there). Drain distribution/day at d25: 1:197, 7:239, 13:381, 19:360, 25:292, 31:161, 37:87, 43:42, 49:17, 55:13, 67:3.
- **Us:** 10 of our 340 episodes were deep towns; we won 4, lost 6, and exactly **one** had a withholding opponent — 98495047. In the other deep-town games the book sat there and nobody took it.

So the Elo answer: the (hold, hold) mirror arises in ~9% of the ~4% of games where the gate fires — rare, and per-unit lockstep makes it a near-tie, not a self-destruct. In the other ~91% of deep towns you are in the (hold, not) branch, which is the observed +$30k branch. In shallow towns the gate stands down and costs nothing. Cornering is a nearly free option against this field. Two named leaders already run it as standard equipment: **Thomas Tschinkel holds exactly 63 carrots across at least 10 games and Xiaowenhao404 62-68**, firing in ordinary drain-25-37/day towns and dumping down *through* the knee (closes $64-$105) — profitable and mostly winning. Their practice says `U_MIN = 1.3` is conservative relative to what already works on the ladder; the safe experiment is to keep 1.3 for firing but size the dump to the knee, then sweep the gate downward.

## Q5: the one measurement, and the kill condition

Re-run the paired six-loss replay with (a) handover at **d24**, (b) the daily re-read + shed-slot sizing + d28 junk-clear, and (c) a tape-vs-tape arm per game to measure the harness's level bias explicitly. Intermediate assertion that must hold before looking at money: on 98495047 the treatment enters d29 with ≥90 carrots in shed. **The line is wrong if**: with the bias subtracted, the treatment gains under ~$15k on 98495047, or the realized dump price averages under ~3× base on any fired game — that would mean the closed-form walk-down (which I re-verified against his actual fill: $517→$427 over 76 units, drain rebuild to $498) does not survive contact with our own execution, and the edge is in something the tape is hiding from both of us.
