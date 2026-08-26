# Reply: herd COUNT item refuted — 2026-08-25

I was wrong on item #1: I recommended an arm without reading that `bought` floors the split, so the code could never reach the total-12 I promised. Same class of error as the `add_land` sweep.

## 1. Do I want total 12 retested with the day-0 branch suppressed?

No. Withdraw the item, do not rerun it.

The run tested 8/6 = 14, not 6/6 = 12, but the per-world rows still answer the 12 case,
because sheep count is the dominant variable and both arms put it at 6.
Ship plays 6/12 in every wool world and wins; the arm's 8/6 loses by five figures in three of them
(worst wool6_milk0: 81,017 -> 61,960).
A true 6/6 arm keeps the same 6 sheep — so it inherits the same wool-book collapse —
and removes two cows of milk/beef income on top.
The only term that could rescue it is the FEED/CARE cost of those two cows,
which is second-order against a -$19,057 swing.
There is no world in the table where 6/6 projects better than 8/6, and 8/6 lost 15% vs 54%.

For the record, if anyone ever does run it: d0-d2 with no shop drawn should buy only the
78/78 opening commitment (SHEEP SHEEP SHEEP COW COW) and defer the rest,
exactly as the guard at `kagg/search/schedule_agent.py:2970` ("An undrawn deck is not a known deck")
already does.
The `corner` branch should get that same guard regardless of the herd question —
it is a correctness fix, not an arm.

Standing caveat, weighed: this is a mirror, and mirrors have inverted findings here before.
But my claim was "12 beats 18 because freed turns become crops" —
a mechanism internal to our own seat, which a mirror measures fine.
The mirror caveat protects equilibrium claims, not this one.

## 2. The freed-capacity argument

Withdrawn.
The decisive number is not the opponent's bank rising — that is the shared-market channel,
real but separate.
It is OUR bank falling in three of five firing worlds despite the freed FEED/CARE turns.
If the 21-31 standing harvestables were turn-starved by animal upkeep,
freeing those turns would have converted some of them; the bank says it converted nothing.
The original parking reason — "we have no logic that turns freed capacity into crops" —
was correct and had not expired.
I asserted it "may have expired" from a standing-inventory count, without checking that any code
routes a freed turn to a harvest.
That is the same unread-mechanism error as the flag floor.

One thing survives, reframed: 21-31 harvestable units standing at d24-29 is still measured waste.
The fix, if there is one, is in harvest/sell cadence at the end of the season,
not in herd size — nothing in this run connects the two.

And the opponent's bank rising is affirmative evidence for sheep at 12 on this seat:
wool revenue we vacate is collected by whoever still sells.
On an Elo ladder that is a double loss.
It also puts a bound on the old "we flood our own book" worry:
even at the flooded price, holding the book beat vacating it in every wool world here.

## 3. Re-ranking the three open items

The lesson from item #1's failure: I ranked by story; only one of the three has a measured
dollar figure attached to the exact change.
Rank by that.

1. **The wool / yarn-store branch, $18,908 on identical production.** Spend the next run here.
   Identical production means the delta is pure sell-path — no board change, no census-vs-decision
   exposure, and the branch decides after the draw lands, on a drawn deck.
   The mechanism is nameable in one sentence, which item #1's was not.
   The run should confirm the $18,908 on fresh seeds and check the arm actually reaches its
   branch — read the code path first, per the flag-floor lesson.
2. **HOLD_A_FLOORED_BOOK vs dawn-overflow projection.** Demoted by this result:
   the run just showed a floored book is worth more than I priced it —
   the field collects whatever we vacate — so any change that releases a hold needs a higher bar now.
   Its upside is bounded by overflow events, and it needs a projection, a new mechanism that can be
   wrong the same way the day-0 branch was.
3. **The seed cutoff.** Cheap, bounded, small. Last.
