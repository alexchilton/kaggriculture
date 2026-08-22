# The fourth quadrant, reopened against the 2026-08-14 field (Fable, 2026-08-15)

Data: the 60 fresh episodes (`data/9*.json`, 120 seats), extracted to
`data/logs/fable_field_seats.jsonl` (per seat, per day: money, quadrants, hires, per-quadrant
planted/weed/pen counts, plant/water op counts, opening fingerprint).
Scratch: `extract_field.py`, `field_analysis.py`, `buy_land_mechanism.py`, `trigger_test.py`.

## 1. The $21,960 crew number: RETRACTED as the closer

My number priced full cultivation of 25 new tiles (~60-65 unit-turns/day) bought with marginal
hires on the fib curve. The field does neither:

- All three 100-tile seats run **277 season hires — zero more than the 75-tile seats** (264-277).
- Plant ops d13-29: 100-tile 100 vs same-script 75-tile 107. Waters: 616-628 vs 649-655.
  **The quadrant is worked by RELOCATING the same ops, not adding any.**
- SE utilisation: ~5-11 planted tiles (of 25) plus 3-4 pens, weeds 0-4. Half the ground stays
  empty. Extra tiles that cannot be reached are simply not planted — they are worth zero, not
  negative, because nobody plants what they cannot water.

What the fixed-ops quadrant actually buys is **slots the full 75-tile board cannot host**:
every 100-tile seat carries **18 animals against the 75-tile seats' 14** (the +4 are SHEEP, in
SE, from d12), plus 6-8 planted tiles of headroom. The SE crop is **WHEAT in all three games**
(tile-days: wheat 110-129, sheep 56-62; nothing else) — consistent with my earlier finding that
wheat's own starved book pays ~$45/unit and needs no premium story.

My crew arithmetic was correct about the plan it priced; the field plays a different plan.
What survives of the original answer: nothing at quadrant-cultivation scale was ever the play,
and the seating/deadline risk still applies to whatever IS planted there (weeds 1-4 appear in
SE in two of three games).

## 2. The selection problem — the mechanism, measured

The purchase is **not bank selection, and not a symptom of a rich first half.** Direct reads:

- The script family emits `BUY_LAND` at d6h5 and d11h1 in ALL 17 cluster games. The d12h1
  order for the 4th parcel is emitted **only in the three games that end at 100 tiles.**
- Every 75-tile seat had $13,173-$15,480 at d12h1 — ample for a $4,000 parcel — and did not
  order. The three that DID order held $7,953-$10,425, the POOREST of the cluster at that turn
  (they had just bought extra animals). Wealth anti-selects; the purchase is a deliberate
  conditional in the script.
- Before any divergence (d10), the eventual-100 games sit INSIDE the 75-tile money range
  (16,363 vs [15,253..17,282]). The d1-d12 trajectory is NOT already better.

I could not pin the trigger from 17 games. It is not yarn count alone (100T draws: yarn 2,1,1;
five 75T games also show yarn=1), not milk-carrier count, not bank. What is unambiguous is that
the parcel fires as one PACKAGE with the herd expansion: +1 animal by d12, +4 by d18, all
sheep, all in SE, wheat around them.

**Consequently the headline gap (100-tile mean $131,344 vs 75-tile $89,229) is mostly the
trigger's selection, not the parcel.** The script buys in games its condition says are good for
an expanded herd, and those are exactly the games wool/milk print in. Cross-game comparison
overstates the parcel ~5-10x.

The cleanest causal number that exists: **the within-game pair.** `92816217` holds a 75-tile
variant (s0, fp a014, $120,160) and a 100-tile variant (s1, fp fe64, $127,645) of the same
meta-script family against the same market, same draw: **+$7,485 for the expansion package.**
One pair, different script variants, so it is an estimate, not a proof — but it agrees with
the bottom-up arithmetic: 4 extra sheep on a wool-friendly draw ~ $8-15k gross minus $2,000
animals minus $4,000 land minus ~zero marginal crew.

## 3. The buy rule, if we adopt it

What the evidence supports (and no more):

- **Conditional, at d12, as a package: $4,000 parcel + 4 sheep + relocate ~8 wheat plantings
  onto SE.** Never unconditional: the 75-tile mode is the majority mode of the best scripts
  (14 of 17 cluster games), and the field's top-vs-bottom split shows tiles/herd do NOT
  separate seats on average.
- **Trigger, ours to define since the field's is unreadable at n=3:** the draw must support
  the extra herd's OUTPUT. Given Alex's own calibration measurement (8 sheep on 1 yarn floods
  by 61 units, wool $35; on 2 stores $243) the defensible trigger is **2+ YARN_STORE visible
  by d12** for the sheep package (P ~ 8% of games), or — per my earlier conditional-tomato
  work — **2+ tomato-stocking instances by d12** (P ~ 26%), in which case the ground takes the
  gated tomato stops instead of wheat and the timing lines up exactly (parcel d12, plant
  d12-13, first fruit d20-23, hinge fires with certainty in that bucket).
- Bank is never the constraint: our shipped plan closes d11 at $12,699 and d12 at $16,246;
  the field buys on less.
- Expected value if the trigger fires: ~+$7.5k (within-game pair) against seed-noise of ~15%
  of an ~$150k season — real but small, and it inherits the same seating discipline the
  quadrant's weeds (1-4 even in the field's games) warn about.

## 4. Corrections to my previous answer, stated plainly

1. **$21,960 marginal crew: retracted.** It priced a plan (full cultivation, hired crew) that
   no one plays. The field's marginal crew cost is zero by relocation.
2. **"Extra tiles that cannot be reached are worth NEGATIVE": wrong in practice.** Nobody
   plants them; unreachable ground is worth zero minus the $4,000 gate.
3. **"No path" -> there IS a narrow path**, and it is the one the best seat in the field
   (One-For-All, $143,621) walks: a conditional d12 package of land + sheep + relocated wheat,
   in a minority of games. Its honest value is ~+$7.5k per triggered game, not the +$42k the
   raw 100-vs-75 means suggest.
4. What my original answer got right and keep: affordability was never the question; full
   cultivation is uneconomic; and the cross-game bank gap is selection — Alex's instinct to
   distrust the n=3 comparison was correct, just with wealth-selection replaced by
   trigger-selection.
