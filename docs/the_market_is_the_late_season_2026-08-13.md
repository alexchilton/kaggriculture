# The late season is a market problem, not a turns problem or a routing problem

2026-08-13. Seed 11, tape victor, measured on `scripts/breakdown.py` and the new
`scripts/sell_when.py`.

Three explanations for the late-season gap were tested and killed in one session.
Recording them together because each was believed at the time and each cost a run.

## Turns are not the constraint

Raising the schedule's `hands` row from 10 to 14 on d26-d29 cost **-$3,350** and bought nothing:

    hire     d26 10->14   d27 10->14   d28 10->14   d29 9->14
    pass     d26 36->124  d27  1->89   d28  8->50   d29 27->123
    water    d26 36->36   d27 43->43   d28 26->27   d29 13->13

The extra hands stood still and drew wages.
This should have been predicted rather than measured: the control already idled 36 turns on d26,
which is the direct disproof of "the crew is 80 turns a day short".

The season totals say the same thing from the other side.
Ours against the tape: **work 2,978 / 2,800** and **idle 862 / 935**.
We already do 178 more ops than Victor and idle less, and finish $11k behind him.

Spare capacity is also the wrong SHAPE, which is the more useful half of the finding.
Idle turns per unit, by day: d20 0.1, d24 0.1, d21 0.4, d25 0.8, d22 1.1, d17 1.2.
One or two turns per unit at dusk cannot absorb a trip; work only fits where a unit already stands.
The only real slack is d28 (56 turns), d29 (89) and, earlier, d10 (98), d18 (73), d16 (63).

## Routing is not the constraint either

The late-season pair below changes the job pool, so d26-d29 were re-solved in day order
(`scripts/solve_day.py`, fixtures dumped from inside `breakdown.py`'s own harness).
Against the new pool the shipped greedy already covers almost everything:

    d26  60 jobs   greedy 60/60      d28  51 jobs   greedy 48/51 -> 51/51
    d27  61 jobs   greedy 61/61      d29  25 jobs   greedy 25/25

**But coverage is not the product.** Dropping d26/d27/d29 from `SOLVED_DAYS` on the reasoning that
"the greedy already covers them" cost **-$2,277** and put weeds back to 5 a day.
The solver also minimises turns and fixes the visit ORDER, and `_live_ops` re-derives work at each
stop, so a better order does strictly more work at identical coverage.
Coverage and order are two different claims; do not read one as the other.

## What the late-season pair is, and what it measured

Three changes, all gated to d26 and later, in `kagg/search/router.py` behind `LATE_SEASON_PAIR`:

- `FERTILIZE_UNTIL_DAY = 26` -- no tile is offered a FERTILIZE from d26. Ours ran 9/11/5 against the
  tape's 2/0/0 on d26-d28.
- `LATE_TRUNCATED_PLANT_DAY = 26` -- `plant_prize` stops returning 0 for a window the season cannot
  finish, so a wheat sown d26 prices at the two waters it can actually reach.
- `HARVEST_A_TRUNCATED_ONE_SHOT` -- `_one_shot_is_finished` takes a partial once the window cannot
  close before d29. Victor takes 26 wheat on d29 at `held 4 / max 6`.

They are a pair by construction and were measured as one, per
`docs/the_late_season_is_one_defect_in_two_halves_2026-08-12.md`.
Half one alone plants tiles nothing can collect; half two alone makes late plantings valuable with
no ground cleared for them.

Measured, control -> arm, season money:

    stale routes          72,184 -> 70,321   -1,863
    re-solved routes      72,184 -> 71,814     -370
    routes dropped        72,184 -> 69,537   -2,647

With the routes re-solved the rows land on the tape almost exactly:

    plant    d26  0 -> 12   (tape 11)
    weeds    d27  0 ->  1   d28 0 -> 1   d29 0 -> 1   (tape 0/1/1)
    water    d28 26 -> 38   (tape 39)
    harvest  d28 17 -> 30   (tape 20)

**-$370 on one seed is undecided, not a win.** It is well inside the ~15% seed variance, and the
ladder is an Elo rating, so the decider is `scripts/field_sweep.py` against recorded opponents, not
this grid. Note the grid CANNOT see the thing that matters: `breakdown.py` runs our agent and the
tape as separate seat-0 runs against their own recorded adversaries, so our sells never move the
tape column and a change that starves an opponent looks identical to one that does not.

## CORRECTION, same day: the milk floor is a HARNESS artefact

Three ladder episodes downloaded 2026-08-13 (92450417, 92443929, 92442061) carry the market price at
each day's close. MILK never floors on the ladder:

    92450417   169 -> 279 over the season
    92443929   169 -> 258
    92442061   169 -> 154   (and WOOL dips to 82 on d10, then recovers to 245)

`breakdown.py` seats our agent against a REPLAYED tape, and both sell into one book. A tape that
sold 303 milk in its own game sells it again next to us, so the harness gluts a book no real game
gluts. That is the identical failure `7a88d30` warned about for the mirror sweep.

The section below is therefore true OF THE HARNESS and unproven on the ladder. Re-measure it from a
ladder replay before acting on it. `SHOP_ADAPT_HERD` reading shops rather than prices is still a
real gap, but the evidence that it is COSTING anything is now withdrawn.

## Where the money actually is: we flood our own book

`scripts/sell_when.py` prints exact per-product SELL fills per day, per unit price, via
`kagg/analysis/fills.py`. Ours, d18-d29:

    MILK   units   18   3  14  21   3  12  21  11   3  12  15  26
           $/unit   4   1   3   1   1   2   3   5   2   5   3   3

    WOOL   units    0  16   0  16   0   0  12   4   0  18   4   0
           $/unit   0   1   0  25   0   0 160 109   0 181 146   0

    MELON  d20 60 units at $151, then d21 12 at $5 and d22 12 at $1

**159 units of milk at $1-$5.** Realised milk was $223.81 a unit in episode 92077611.
Wool is the control that proves the mechanism: $1 on d19, then $160/$109/$181/$146 on d24-d28 when
it goes out in smaller lots. The town's demand refills; we do not let it.

Total sell revenue is $214,385 against a final bank of $71,814. The revenue exists. The price we
accept for it does not.

This corroborates what `7a88d30` already recorded and nobody carried forward: across the eleven
newest ladder losses, every game where `SHOP_ADAPT_HERD` cut us to six cows closed MILK above base
($169, $235, $249) and every game at eight or nine floored it at $1. **The cow COUNT is causal.**

And `SHOP_ADAPT_HERD` cannot see any of it. It floats the cow/sheep split on which SHOPS exist --
three of eight carry milk, so it reads "well supported" and buys cows -- and never reads a realised
price. We run COW 10 / SHEEP 4 against every recorded opponent's COW 8 / SHEEP 6: heavy in the
floored product, light in the one paying $180.

Two pens also stand empty from d24 to the end. Pens 15, animals 13, tape 14.

## The geese verdict was measuring our own bug

`c9c1c18` and `7a88d30` killed geese on two sweeps, both **outcome-only** -- win rate and mean money.
An outcome test cannot separate "geese are bad" from "we play geese badly", and the fills were never
read.

Restored the machinery from `7a88d30` and ran `HERD_GEESE = 2` through `sell_when.py`:

    EGG fills, whole season          0
    animals                     10 (13 without geese)
    season money                48,196 (71,814 without)
    sell revenue               188,908 (214,385 without)

**Not one egg is ever sold.** The birds are bought, fed and cared for over thirty days and produce
nothing that reaches a sale. The -42 points of win rate is the cost of three animals' worth of turns
and money against zero revenue; it says nothing about whether a goose is worth owning.

The stale baked routes cost part of that $23k -- `SOLVED_DAYS` was solved on a goose-free pool -- but
stale routing cannot produce zero egg sales.

**Root cause found, same day, commit `c99a8a5`: `SELLABLE` held six of the env's nine product names.**
CARROT, TOMATO and EGG were absent from the tuple that is the *only* loop emitting a SELL, so an EGG
row was not deprioritised or outbid -- it was never looked at, by construction. Every goose verdict
in this project (`c9c1c18`, `7a88d30`, and this section above before this note) was measured while
EGG could not be sold under any flag or schedule row. `c99a8a5` fixed `SELLABLE`; the "not one egg is
ever sold" finding above is explained exactly, not just correlated, and the fifth-time-artefact verdict
holds for a sixth reason nobody had named yet. **Geese have not been re-measured with EGG sellable.**
Do not treat "geese lose" as settled until that run exists.

This is the fifth time an animal verdict here has turned out to be an artefact. The rule in CLAUDE.md
already covers it: ask what the code could not express before trusting a mechanic-level negative.
The addition this time is narrower and mechanical: **an outcome-only sweep is not a test of a
mechanic.** Before believing one, read the fills for the product the mechanic is supposed to produce.

## Open, in priority order

1. Meter the milk sell rate, or cut the cow count. This is where the $11k is.
2. Re-capture the tape side of `sell_when.py` -- the split-on-turn-wrap only caught one env, so
   whether Victor sells the same units in smaller lots is still unmeasured.
3. Re-run the geese properly: re-solve the routes for a goose pool, and require an EGG row with
   units before reading any money at all.
4. Field-sweep `LATE_SEASON_PAIR`. It needs a second route set so the off-arm is not seated with
   routes solved for the on-arm's job pool.
5. Fill the last two pens.
