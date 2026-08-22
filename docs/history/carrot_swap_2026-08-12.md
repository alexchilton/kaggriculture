> SUPERSEDED by docs/carrot_and_the_empty_book_2026-08-19.md - the clean measurement of carrot vs
> wheat this file's own retraction below calls for. `CARROT_SWAP` no longer exists in the code
> (`kagg/`, `scripts/`, `tests/` — checked 2026-08-15). Kept for the method lesson (winner's curse,
> tape-instrument noise floor); the retractions below are already in force, read them first.

# The carrot swap, measured on Victor's tape — CLOSED, and it is not the town

> **RETRACTED 2026-08-12, same day. Every arm in this file is invalid.**
>
> The schedule's `sells` rows never mention CARROT, so nothing below ever SOLD any carrot it grew.
> Measured directly: 2 carrot tiles put 6 units (seed 13) and 3 units (seed 14) into the shed and
> **0 units out of it** for the whole season. Every arm therefore paid the $20 seed, spent the tile
> and the turns, and banked nothing — a loss by construction, on any crop, whatever the market says.
>
> That applies to ALL of it: the tape arms, the 384-game `CARROT_SWAP` pool sweep, the
> `CARROT_TILES` sweep, and the 2-for-2 substitution. None of them measured carrot's economics.
>
> A second, independent defect compounds it: carrot is `max_yield_day 3` against wheat's `4`, and
> the schedule's harvest cadence is built for wheat, so the tile is visited a day late and does not
> deliver its 4 units either (6 and 3 units from 2 tiles, against 8 expected).
>
> **Carrot is UNTESTED, not disproven.** A real test needs CARROT in the sells row and a harvest on
> carrot's own clock. The market analysis below (the pocket ledger, the price curves) is still
> correct as arithmetic and is still the right way to size the prize — it is just not what decided
> any of these arms.

> **THE FRAME WAS ALSO WRONG — 2026-08-13, from the leader's own tapes.**
>
> Every arm in this file is a **swap**: `PLANT WHEAT -> PLANT CARROT` from day D, replacing a crop
> that pays with one that pays less. At base prices wheat is $140/tile against carrot's $120, so
> that question has a correct answer and the answer is no. It is not the question the leader is
> answering.
>
> カワシギ (#1, 15-1 over 16 games, `docs/kawashigi_one_board_2026-08-13.md`) buys **8 carrot seeds
> on d3/d6 in all 16 games** and then plants **no carrot at all until d21**. From d21 to d26 he
> plants carrot in every game, 1-8 tiles, on ground that is otherwise finished:
>
>     2407  d22:4 d25:4        0434  d21:3 d22:1 d25:1 d26:2
>     8461  d21:2 d22:1 d24:3 d25:1    8144  d21:2 d22:2 d24:2 d25:2
>     2932  d21:2 d22:2 d24:2 d25:1 d26:1   6371  d21:1 d22:1 d24:1 d25:1 d26:1
>
> Carrot is `first_yield_day 2, max_yield_day 3` against wheat's `2, 4`. A wheat sown on d26 reaches
> its window on d30, which does not exist; a carrot sown on d26 finishes. **Carrot is not a
> competitor to wheat, it is the crop for the window in which wheat is unplantable** — additive on
> dead tiles, never a substitution.
>
> **And the frame was forced by the fixture, which is the part that generalises.** These arms were
> run by mutating a BAKED tape. Its sell rows, its harvest cadence and its seed purchases are all
> fixed to wheat's clock, so the only carrot experiment such a fixture can express is "rewrite some
> wheat tokens as carrot tokens". A crop on a different clock has nowhere to live in it. That single
> cause produces all three recorded symptoms: the harvest lands a day late (cadence baked to
> `max_yield_day 4`), nothing is ever sold (no CARROT sell row), and `D=26` starves (seed buys baked
> to wheat). It also rules out the leader's actual play by construction, because planting into empty
> late tiles is an ADDITION and a tape has no free slots to add to.
>
> The same trap is live in `SOLVED_DAYS` / `PRECOMPUTED_ROUTES`: routes solved against a job pool
> that contains no carrot cannot route a carrot. Testing any new mechanic against baked routes
> measures whether the baked plan absorbs it, not whether the mechanic pays.
>
> This is the CLAUDE.md rule verbatim: evaluate a technique against the problem it was built for.
> Every arm here asked "is carrot better than wheat", got a correct no, and never asked "what can be
> planted once wheat can no longer finish".
>
> The real test: carrot planted d21-d26 on tiles the plan leaves empty, with CARROT in the sells row.
> `LATE_TRUNCATED_PLANT_DAY = 26` (2026-08-13) opened that window and fills it with wheat.


Alex's method call, 2026-08-12: test the crop change on **Victor's tape**, not on our agent.
Sweeping a crop flag on our agent conflates "is carrot worth planting" with "does our planner cope
with a different job mix", and our planner's behaviour shifts unpredictably when the job mix changes.
The same call had just reversed the cow-cap result, so it was applied here too.

Harness: `scratchpad/tape_carrot.py` and `scratchpad/carrot_by_town.py`.
Logs: `data/logs/tape_carrot_2026-08-12.log`, `data/logs/tape_carrot_wheattiming_2026-08-12.log`,
`data/logs/carrot_by_town_2026-08-12.log`.

## What was rewritten

For turns on day >= D, on his own action stream: `PLANT WHEAT -> PLANT CARROT` and
`BUY_SEED WHEAT -> BUY_SEED CARROT`.
Every `SELL WHEAT q` is mirrored by an appended `SELL CARROT q` so the carrot can reach the book at
all — a SELL against an empty shed fails per unit with no penalty (`kaggriculture.py:_commit_unit`),
so the mirror cannot cost anything.

`BUY_PRODUCT WHEAT` is deliberately **not** rewritten.
FEED takes WHEAT 1 (`kaggriculture.py:495`) and he runs 14 animals over 299 FEED ops, so leaving his
wheat purchases alone keeps the herd alive and the result measures crop economics rather than
starvation.
The `starved` column counts FEED ops submitted with an empty wheat shed; the control's own baseline
is 11 a season, and any arm where it moves is contaminated.

The control arm (D=99, nothing swapped) reproduces the tape at **$101,917** mean over seeds 11-14,
identical to `tape_cap.py`'s uncapped arm. That is the gate that says the harness is faithful.

## The first result was entirely a lifecycle artifact — read the weeds column, not the money

```
     D  plants  seeds  starved   mean bank  weeds     delta
    99       0      0       11     101,917    1.5        +0
    26      11      2       11     100,900    1.5    -1,017
    23      55     34       11      93,472   29.2    -8,446
    20      81     89       18      83,835   44.2   -18,082
    16      97    105       33      77,726   45.2   -24,191
    10     114    123       37      59,262   45.2   -42,656
     6     127    136       47      43,522   45.2   -58,395
     0     139    148       73      26,498   45.2   -75,419
```

Weeds go **1.5 -> 45**. Forty-five of his tiles die, in two independent ways:

- **Lifecycle.** Wheat is `first_yield_day 2, max_yield_day 4`; carrot is `2, 3`.
  Past `max_lifespan_step` a tile sheds a yield unit every 2 steps and turns to `WEED`
  (`kaggriculture.py:745-752`). His HARVEST and WATER turns are baked to wheat's window, so a carrot
  tile rots before he reaches it.
- **Seed matching at the boundary.** He front-buys seed — 48 wheat seeds on d20 alone.
  At D=26 only 2 seeds were swapped against 11 plants, so 9 of those plants failed for want of
  carrot seed. D=26 and D=23 are seed-starved; D<=20 are seed-fine but lifecycle-broken.

**This is the difference between a crop swap and the cow cap.** Dropping a `BUY_ANIMAL` leaves every
timing untouched. Relabelling a crop moves the tile's clock while the tape's turns stay fixed.
A tape-side test is only valid for a change that does not move the schedule's own clock.

## Neutralising the lifecycle does not recover the money

Giving CARROT wheat's yield *days* while keeping carrot's own `max_yield` 4, seed $20 and market
prices:

```
     D  plants  starved   mean bank  weeds     delta
    99       0       11     101,917    1.5        +0
    20      81       18      83,782    1.5   -18,135
    16      97       33      76,866    1.5   -25,052
    10     114       37      56,826    1.5   -45,091
     6     127       50      35,064    1.5   -66,853
     0     139       78      14,917    2.8   -87,000
```

Weeds return to the control's 1.5 and **the loss is unchanged** (-18,135 against -18,082 at D=20).
So the dead tiles were never what cost the money.
D=20 is the clean arm: 81 tiles swapped, weeds flat, starvation +7 of 299 FEEDs, **-$224 per tile**.

## The town does not rescue it — 0 of 16 seeds

Alex's hypothesis: the shop draw is per-seed, carrot is carried by only `PET_CAFE` (single-product,
so it drains double) and `FARMERS_MARKET` against wheat's five, so a town drawing PET_CAFE repeatedly
should let carrot hold price while wheat collapses.

Sixteen towns, D=20, control and arm on the same seed, sorted by carrot-minus-wheat weighted drain:

```
   c-w carr  wht   seed    control     carrot     delta  starv   shops
    -6    0    6     14    102,696     82,936   -19,760     18   BAKER BRUNCx2 ICE PIZZAx2 YARNx2
    -5    0    5     12    119,458     95,817   -23,641     18   BAKER BRUNCx2 ICE PIZZA SMOOTx3
    -4    1    5     15    145,607    119,313   -26,294     18   BAKER BRUNC FARME ICEx2 SMOOTx2 YARN
    -2    5    7     19     69,329     58,891   -10,438     18   BAKER BRUNC FARMEx3 PET PIZZAx2
    -1    4    5     11     83,632     69,842   -13,790     18   BAKER BRUNCx2 FARMEx2 PET SMOOT YARN
    +1    6    5     18     45,626     36,430    -9,196     18   BAKERx2 BRUNC ICE PETx3 PIZZA
    +2    6    4     22     72,616     60,682   -11,934     54   FARMEx2 ICEx2 PETx2 SMOOT YARN
```

(abridged; full 16 rows in the log)

**The trend runs the way the hypothesis predicted and never crosses zero.**
The smallest losses cluster at the top of the `c-w` column and the largest at the bottom, so the shop
draw genuinely modulates the size of the loss.
But the two seeds where carrot's weighted drain actually *exceeds* wheat's still lose: seed 18
(`PET_CAFE x3`) by $9,196, and seed 22 by $11,934 — and seed 22's `starved 54` against everyone
else's 18 means it is feed-contaminated, so **seed 18 is the true best case in sixteen towns, and it
is still a $9.2k hole on 81 tiles.**

## Why the hole is five times the yield-table gap

At base prices wheat is 6 units at $25 less a $10 seed = $140/tile; carrot is 4 at $35 less $20 =
$120. That gap is $20/tile, or $1,620 over 81 tiles. The measured best case is $9,196.

The missing factor is that **wheat is not only a crop for this build, it is the feed supply**.
He buys 246 WHEAT as product across the season to feed 14 animals. Growing his own wheat puts supply
into the book and holds the wheat price down; swapping wheat out leaves those purchases quoting
against a scarcer book, so his feed bill rises at the same time his crop revenue falls.
A crop that feeds nothing cannot substitute 1:1 for one that does, whatever the town draws.

**This is measured but not yet isolated** — the decomposition of the $9.2k into lost crop revenue
versus raised feed cost has not been run. That is the one open thread here.

## There IS a sweet spot, it is tiny, and it does not survive a fixed setting

Alex, on being shown the 81-tile arms: "surely there is a sweet spot?? keep enough wheat for the
animal feed and then only swap x carrots".
Correct on both counts, and the day-boundary sweep above could not see it — it conflated HOW MANY
tiles with WHEN, and every arm was 81+ tiles, far past the peak.

Re-run by COUNT with the seed purchases explicitly paired (`scratchpad/carrot_n.py`: each swapped
plant claims an earlier unclaimed wheat seed unit, or it is not swapped, so a starved pairing can
never be misread as an economic result).

**Early tiles are the herd's feed and swapping them is catastrophic.** Swapping the first 2 wheat
tiles costs **$26,405** and drives `starv` 11 -> 34: an animal missing two FEEDs is REMOVED outright
(`kaggriculture.py:804`). The surplus wheat is late-season only.

Amount x start-day, seeds 18 and 11 (`data/logs/carrot_grid_2026-08-12.log`):

```
     D    N    delta   per-seed (18, 11)
    14    2     +122   +217  +28
    20    2     +300   +300  +301
    20    4     +260   +399  +121
    20    8   -1,072   -114  -2,030
    24    2       -4   +1    -8          <- too late to yield before the season ends
```

So the pocket is real and sits at **D=20, N=2-4, worth ~$300**.
The ledger (below) put the peak at k=16; the simulator says negative by N=8, so the ledger
overstated the width by ~4x.

**But at a fixed setting across all sixteen towns it loses** (`data/logs/carrot_optN_2026-08-12.log`):

```
  fixed N=1  mean  -$486
  fixed N=2  mean  -$573
  per-seed argmax over 7 arms, 10 of 16 positive, mean  +$284   <- WINNER'S CURSE, not a result
```

Six seeds (12, 14, 15, 23, 25, 26) lose at every N, and three of those have carrot weights of 4, 3
and 3 — perfectly good carrot towns.
The argmax does **not** track the town's carrot drain (`carrot_w 3 -> argmax 1.5`,
`carrot_w 6 -> 2.5`, `carrot_w 2 -> 3.3`), so the good seeds cannot be identified in advance.
A per-seed optimum we cannot predict is worth nothing on the ladder.

## The pocket is small because carrot's book is one of the worst in the game

Generalising the question Alex asked — "check it with the other items too" — the premium available
in a book nobody supplies is the integral of `(price(inv) - base)` over the town's season drain.
`scratchpad/pocket_all.py`, town seed18 (the most carrot-favourable of sixteen):

```
  product       drain   pocket$    p1   base   half@   glut     yield/op  seed$  fyd
  STRAWBERRY      300    29,172   265    120     226   linear          4    100   10
  MILK            210    17,696   286    160     157   linear          -      -    -
  WHEAT           696    12,246    51     25     514   log             6     10    2
  EGG             516     8,035    81     50     259   log             -      -    -
  CARROT          570     3,502    42     35     550   sqrt            4     20    2
  TOMATO           84       428    70     60      39   sqrt            4     50    8
```

Carrot drains 570 units and the price only reaches **$42**, because its scarcity curve is
`log/0.20` — the flattest of any crop. It gains almost nothing from being scarce and collapses on
`sqrt/0.70` when supplied. **Wheat is the exact inverse and is the best book in the game to dump
into**: `log/0.20` on the glut side, still above base after 500+ units. That is the quantitative
reason every carrot arm lost — we kept swapping out of the widest book into the shallowest.

`fyd` (`first_yield_day`) also settles which crops can take a LATE swap at all: 2 for wheat and
carrot, 8 for tomato, 10 for strawberry and melon. A tile swapped on d20 has ten days, so carrot is
structurally the only candidate for the late pocket regardless of how attractive tomato looks.

**The pocket ceiling is a property of the town and the market, not of the agent.** That is what makes
it decision-relevant despite everything here being measured on the tape: no planner, ours or a
perfect one, can extract more than ~$3,502 from carrot's book on the best of sixteen towns, or $91
on the worst.

## What the tape test can and cannot say

Worth stating plainly, because it is the opposite caveat to the cow cap.
The tape is a fixed script tuned to wheat: it cannot redeploy the freed cash, cannot re-route to the
carrot tiles, cannot harvest on carrot's own clock (the timing had to be overridden or 45 tiles
rot), and sells carrot only through mirrored orders.
**So the tape UNDERSTATES carrot**, where for the cow cap it removed a planner artifact that was
flattering the result.
A negative here is therefore not by itself a negative for our agent — the pocket ledger is, because
it is planner-independent.

## THE DECIDING MEASUREMENT — our agent, the real pool, win rate. CARROT_SWAP is OFF.

Everything above is tape-side diagnostics. This is the artifact that ships, scored the way the
ladder scores it. Run on the Windows box, `data/logs/carrot_swap_sweep_2026-08-12.log`
(pull with `scp alex@192.168.1.128:~/kaggriculture/data/logs/carrot_swap_sweep_2026-08-12.log .`).

```
  seeds 1300-1303, 24 recorded ladder opponents, both seatings, 192 games per arm
     value  games     win   mean ours  mean theirs  mean margin
         0    192  65.1%     130,168      109,698       20,470
         1    192  54.7%     124,304      111,341       12,963

  seeds 1306-1309 (chosen because the flag fires on 3 of 4), 192 games per arm
         0    192  67.2%     131,387      108,988       22,399
         1    192  59.4%     127,108      109,569       17,539
```

**-10.4 and -7.8 points, two independent seed sets, 384 games.** It is not one bad matchup: the flag
degrades `Subin An` 38->25 then 25->0, `YassY` 100->50, `Ahmet Abdullah Gültekin` 100->75,
`Lemmes Yad` 100->75, `Farm-ops` 100->88, `MakiMakiAi` 100->88, `UwU` 25->12, and improves against
**nobody**. Money and margin fall together.

`CARROT_SWAP = False` stays False. Do not re-enable it.

**The cheap ledger and the expensive sweep agree, by different routes.** `pocket_all.py` costs
seconds and put carrot's whole book at $3,502 on the best of sixteen towns and $91 on the worst,
planner-independently; the 384-game sweep costs ~40 minutes of box time and says -7.8 points. That
is worth remembering as method: the pocket ledger would have killed this before any of the tape work.

## What the tape work got WRONG, and why it is recorded anyway

Three things in this file were stated with more confidence than they deserved, and the sequence is
the lesson:

1. **"Net negative at any fixed setting"** was computed on arms that were all silently killing a
   SHEEP. Swapping ONE wheat tile takes the herd from 5 sheep to 4 (`starv` 11 -> 18): his SELL
   WHEAT orders are sized against a shed that used to hold those 6 units, so the sells drain it to
   zero and the FEED finds nothing. A $500 animal plus its wool, charged against a ~$200 book trade,
   on every arm -- the wins as well as the losses.
2. **The sweet-spot numbers** (+$300 at D=20 N=2, +$399 at N=4) were per-seed argmaxes over 7 arms.
   At a fixed N the same table is -$486 and -$573. Winner's curse, exactly as CLAUDE.md warns.
3. **The reserve fix made the instrument unusable, not better.** Holding wheat back from SELL cured
   the starvation (`starv` 18 -> 5) and the money went from -$1,199 to -$20,470, with one seed at
   +$8,614 and another at -$49,064. Suppressing three sell orders cannot move $49k economically --
   it moves the ORDER SLOTS. A turn's orders compact into ten slots walked in lockstep against the
   opponent's, so dropping one realigns every slot after it and changes who wins each contested
   unit. **The tape instrument has a ±$40k noise floor on a ±$400 signal.**

So the tape was the right tool for the cow cap -- where it REMOVED a planner artifact worth
thousands -- and the wrong tool here, where the effect is smaller than its own noise. The rule that
falls out: check the instrument's noise floor against the size of the effect before trusting its
sign. A tape is exact for a change the script can absorb and noisy for one it cannot.

## The small version was tested too, on the pool. Also a null.

Alex's version of the idea, which is NOT what `CARROT_SWAP` tested: a fixed handful of late carrot
tiles rather than converting the whole unplanted row. Implemented as `CARROT_TILES = 4` from day 20,
swept on the box against the same 24 recorded ladder opponents, both seatings.

```
  seeds 1300-1303   0: 70.3%   4: 71.9%   (+1.6)
  seeds 1306-1309   0: 74.0%   4: 70.3%   (-3.7)
                    ------------------------------
  mean over 768     0: 72.2%   4: 71.1%   (-1.1)
```

One seed set up, one down, net slightly negative — inside noise. **Flag deleted, not left at 0.**

Read what it actually measured before re-deriving it. Locally the arm planted
`{WHEAT 94, MELON 19, STRAWBERRY 31, CARROT 3}` against a control of
`{WHEAT 94, MELON 19, STRAWBERRY 31}` — **wheat is identical**. The rule cut the wheat *request*,
later schedule rows refilled it, and the carrot landed on three tiles that would otherwise have sat
empty. So this arm is "carrot versus bare dirt", the most favourable framing there is, with no feed
displaced and no opportunity cost. It is still a null.

That closes the last version of the question worth asking. The three framings are now all measured:
whole-row swap (-7.8/-10.4 points), small late swap (null), and carrot on idle ground (null, same
arm). Do not re-open without a mechanism none of these covers.

## Verdict

Carrot does not pay as a substitute for wheat on this build, on any of sixteen towns, with the
lifecycle confound removed and starvation controlled.
This is a *stronger* negative than C-23's `SHOP_ADAPT_CROPS` result, because it isolates
`WHEAT<->CARROT` alone (C-23 measured it jointly with `TOMATO<->STRAWBERRY` and never separated
them), removes our planner entirely, and varies the town.

Do not re-open on the argument that "CARROT closes above base in 10 of 10 games".
That is true and it is not sufficient: closing above base measures that nobody supplies carrot, not
that supplying it beats supplying wheat.

**Not tested and still open:** carrot as a substitute for something *other* than wheat, and TOMATO,
which `docs/ladder_losses_2026-08-11.md` argues for on different grounds — that it is the right home
for the ground currently growing the second melon wave, which is a denial play rather than a yield
play. Neither question is answered by this file.
