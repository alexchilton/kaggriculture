# Why planted ground stops producing from d19: it is ground-turnover latency, not digs, fert or caps

2026-08-15, seed 11, tape `kawashigi`, weeds 0.0, worktree at `af3db5d` with the OLD
(victor-solved) `solved_days.py`. 30-day replay on the grid environment (recorded economy + shop
draw). Probe: scratchpad `decay_probe.py`, logs `data/logs/fable_decay_probe.log` / `_v2.log`,
`fable_spent_dig_trace.log`. **Per-tile counts here are route-sensitive and will shift when the
solved_days regeneration lands; the rule-level mechanics will not.**

## The mechanics that govern everything below (from `reference/kaggriculture.py`)

- An ongoing crop has exactly `max_yield` production events (strawberry: 4, every 2 days from age
  10). Each event adds 1 unit (2 if the tile was watered that day AND fertilized), **clamped at
  `max_yield` held** (`:795-800`).
- At the final production, `max_lifespan_step` is set (`:801-802`) and from the NEXT day the tile
  DECAYS: `_decay_plants` runs **every step** (`:944`), eats 1 held unit every 2 steps, and turns
  the tile into a WEED when it hits 0 (`:752-766`). A harvested spent tile (0 units held) weeds
  **within 2 turns of the next dawn**. So the final-production day is a one-day window to harvest
  AND dig, or the square stalls as a weed.
- Weeds therefore have TWO origins with weeds off: thirst (`consecutive_unwatered >= 2`) and
  decay. The project's standing memory "every weed is a missed water" is incomplete -- decay weeds
  outnumber thirst weeds on both farms.

## Q1 -- Are we digging crops he keeps? NO. We dig the same things, LATE.

Every DIG classified by what stood under it (ours 54 / tape 40 this run):

    ours, season:  18 PLANT(STRAWBERRY, y=0, SPENT)   21 WEED(decay)   14 WEED(thirst)   1 other
    tape, season:  31 PLANT(STRAWBERRY, y=0, SPENT)    5 WEED(decay)    0 WEED(thirst)   4 other

`DIG_A_SPENT_ONGOING_CROP` (`router.py:1096`, offer at `:765-769`) is correct and both sides play
it -- the tape digs MORE spent strawberries than we do, promptly, and replants behind them. Our
surplus digs are the bill for weeds we created: **34 weed births vs his 10**
(ours: 13 thirst + 21 decay; his: 0 thirst + 10 decay). Nothing fires too early; tiles die and the
corpse then sits as a WEED holding ground that late-season replanting could use (strawberry
replant stops paying at d19: `plant_prize` needs `days_left >= first = 10`).

No rule digs live crops: zero PLANT digs with units held, zero unspent PLANT digs, both farms.

## Q2 -- Is the extra fertilize buying anything? YES, at near-tape efficiency. Not the thief.

    ours:  100 ops  = 49 STRAWBERRY + 51 WHEAT, 98 effective / 2 no-op
           bonus units actually banked: 88 ongoing + 97 one-shot = 185  ->  1.85 units/op
    tape:   72 ops  = 72 STRAWBERRY, all effective
           bonus units banked: 142 ongoing + 0 one-shot         ->  1.97 units/op

The +28-45 op gap is us fertilizing WHEAT, which he never does, at 1.9 banked units/op -- each op
costs a turn plus a fertilizer that would sell for $20-50 late, against ~2 wheat units (~$50 base).
Marginal in dollars, defensible, and NOT a mechanism for the harvest gap. If anything is trimmed
here it should be measured on its own; expected effect is small either way.

## Q3 -- Are ongoing tiles sitting at cap discarding production? NO. Zero, both farms, all season.

Replaying the refresh arithmetic on every h23 board: **0 production units discarded at cap for us,
0 for the tape, over 30 days**. Harvests always intervene before a tile fills. The cap-discard
theory is dead; do not re-derive it.

Units lost to DECAY of spent tiles are near-parity too: ours 92, tape 82 -- both sides harvest the
final production a little late sometimes; this is not where the gap lives either.

## What the d19+ decay actually is: standing-crop attrition + stalled squares

    harvest d19+ (this run):   ours 247 / tape 275
    weed births:               ours 34  / tape 10
    strawberry lifecycles completed:  ours 13 / tape 31

Two attrition channels, neither of them the briefed hypotheses:

1. **Thirst kills our live strawberries mid-life** (13 vs his 0), so the ongoing population that
   should still be producing at d19-d27 is 5/14. Each death also removes every future production
   and leaves a WEED to dig.
2. **One-shots left past their window rot into decay weeds** (the bulk of our 21 vs his 10) --
   yield already grown is eaten at 1 unit per 2 turns and the square stalls until dug.

Fewer standing producers -> fewer harvests -> the late sell collapse. The board-state rows
(animals/pens/tiles/hands identical) stay clean because none of this touches the herd.

Caveat on the 13 thirst weeds: `LATE_SEASON_TRIAGE` deliberately stops watering tiles that cannot
produce again before d29, so part of the post-d19 thirst count is policy, not defect. Splitting
those by remaining value is the first step of any fix here.

## The spent-tile DIG lifecycle, traced (`fable_spent_dig_trace.log`)

Caveat first: one-shots carry `max_lifespan_step >= 0` from PLANTING (`kaggriculture.py:224`), so
"spent" filters must be ongoing-only; the trace's clean rows are the strawberries, d23-d28.

    our spent strawberries, whole season:            13   (the tape completes 31)
      DIG offered same day:                          11   (the 2 d28 non-offers are correct:
      dug same day:                                   9    `plant_prize` = 0, digging pays nothing)
      DIG covered but LOST at execution:              2   (9,4)@d23 cost 23/23, (9,2)@d24 cost 22/23
                                                          -- both on OLD precomputed days, both
                                                          zero/one-margin tours, only HARVEST ran

Two conclusions. First, the reason the tape digs 31 spent strawberries to our 18 is not diligence
we lack -- it is that **2.4x more of his strawberries live long enough to finish**. Ours die young
of thirst (the lost-rescue family in the watering doc); his 0 thirst weeds against our 13 is the
same fact from the other side. Second, our 21 decay weeds are mostly NOT strawberries at all: they
are **one-shots (wheat/melon) left past their window holding yield until `_decay_plants` rots them
to weeds** -- the already-documented unharvested-wheat defect (`_one_shot_is_finished`'s TRIED
note: 32 of 66 wheat standing at season end; the forced-harvest fix measured -$92 and was
reverted because the harvest could not reach a sale in time).

## The shared root, and the candidate lever (NOT implemented -- routes are being regenerated)

This is the same single-window reliability shape as the watering deaths in
`docs/fable_watering_post_d8_2026-08-15.md`: a job that MUST run on one specific day, seated in
zero-margin or over-budget tours (packing cost model vs shipped `materialise` disagree on
RESERVE_DAYS; 25/23 and 26/23 tours observed on d15), where a 1-2 turn arrival slip
(`docs/spawn_ring_misprediction_2026-08-12.md`) deletes the tail stop. Two symptoms, one defect.

Candidate rule-level delta for after the regen: `_at_risk_tiles` (`schedule_agent.py:142`) marks
"skipping today's work destroys something tonight" for unfed animals and unwatered crops -- but a
tile on its final-production day IS in that class (it decays and weeds overnight) and is not
marked. Marking `max_lifespan_step >= 0` (or final-production-today) tiles at_risk would route
their harvest+dig early through the exact machinery that already protects feeds and brink waters.
Red-first test shape: "a tile whose last production lands today is covered as at_risk". Must be
day-gated >= 9 (d0-d8 tape-match) -- first spent strawberries appear ~d17-d19, so the gate is free.

## Route-sensitive vs durable

Route-sensitive (will shift with solved_days regen): every per-day count, the 46%/76% split, the
specific tours. Durable: the decay clock and one-day window, two weed origins, zero cap discards,
fertilize efficiency ratios, `plant_prize` positivity through ~d28, the at_risk gap for spent
tiles, and the negative verdicts on all three briefed hypotheses.
