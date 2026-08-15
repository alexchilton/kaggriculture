# After the closing-day release: what shipped, and the three things measured since

Written 2026-08-15, after submission `55530699`.

## What shipped

`55530699`, built from `2a2e291`, merged at `081c24f`.
Eight deltas that stop the season ending with produce in the crew's hands.

    season close vs kawashigi tape   150,728 -> 152,974   (tape 150,076)
    stranded at the close            62 units -> 16       (tape 7)
    d29 feed 14->0  care 14->0  drop 3->7  sell fills 96->154  harvest 22->19

We harvest LESS and bank more, because produce not walked to the shed on d29 is discarded by
`_end_of_day` after the final turn and `_commit_unit` will not sell from a hand.

d0-d27 byte-identical. d28 moves only on the last delta.
Detail and every grid: `fable_close_the_season_2026-08-15.md`. Brief: `fable_brief_sell_the_close_2026-08-15.md`.

Measured on seed 11 and the kawashigi tape only.
No held-out seeds and no arena pool, by explicit decision — the slot was spent to get it on the
board rather than to validate it first.

The previous build, `55527916`, is at **1855.0**.

## 1. The fourth quadrant

Two losses downloaded after the release, neither close:

    93335778   us $89,518  vs Artem Voronov $103,607   -$14,089
    93337672   us $74,289  vs Anhad Mahajan  $77,703    -$3,414

Artem owns FOUR quadrants and 100 tiles to our 75.
Anhad owns three, like us, and that game is inside the close-day margin.

Quadrant unlock turns, from `data/logs/quadrant_timing_leaders.log`:

    player                  games   4q      NE       SW       SE
    alex chilton (archive)     69   66    d4h22    d8h20    d11h1
    カワシギ                    16    4     d6h5    d11h1    d12h1
    Seb (allegedly)            16   16    d4h22    d6h15   d10h14
    Victor @ Tufa Labs          7    0    d6h17    d10h1        -
    Francesco Montone           2    2     d5h0    d8h22   d10h16

Artem's line is `NE d6h5, SW d11h1, SE d12h1` — カワシギ's median to the hour.

Two facts that bound this:

- **We used to buy the fourth in 66 of 69 archived games, and EARLIER than Artem does** (SE d11h1
  against his d12h1, SW d8h20 against his d11h1). We stopped when we rebased onto Victor, who takes
  it in 0 of 7. That was not a decision about land; it arrived with the plan.
- Across all five downloaded losses our unlock turns are byte-identical — NW d0h0, NE d6h10,
  SW d11h1. Our opponents vary (NE d6h5 to d7h2). We do not adapt at all.

So the open question is not "can we afford a fourth" — demonstrably we could, sooner. It is what
the rebase traded that land for, and whether the trade still holds on 1.32.7.
The old timing is pre-rebalance, so its affordability does not carry over unexamined.

## 2. Tomato is conditional, and seed 11 is the wrong board to test it on

Both losses show TOMATO and EGG closing ABOVE base with real town demand and **nobody producing
either**:

                    93335778              93337672
    TOMATO    $74 of $60, drained 179   $165 of $60, drained 358
    EGG       $67 of $50, drained 537    $66 of $50, drained 358
    MILK       $1 of $160  FLOOR          $1 of $160  FLOOR
    STRAWBERRY $5 of $120                $43 of $120

The machinery to act on this already exists and is inert: `WHEAT_TILES_TO_TOMATO = 0`,
`WHEAT_TILES_TO_CARROT = 0`, `LATE_CROP_FROM_DAY = 12`.

Swept on seed 11 against the kawashigi tape (`data/logs/tomato_sweep.log`):

    tomato tiles   our money      tape     closing TOMATO   STRAWBERRY
          0         84,945      66,801          70              12
          4         83,203      69,250          74              12
          8         81,842      68,568          66              14
         12         82,888      69,779          69              12
         16         80,727      69,163          61              16
         24         78,231      69,781          53              20

**Unconditional tomato loses money on this board, monotonically.** The price column says why: TOMATO
never leaves 53-74, so the hinge never fires, and our own production pushes it DOWN.

This is not a verdict on tomato. The 2026-08-15 balance note states the intent directly: these
products become viable in roughly **50% of games for tomato, 26% carrot, 22% eggs** — deliberately
not universally, to create end-game decisions. At zero production seed 11 closes tomato at $70
against base $60, so seed 11 is one of the boards where it does not pay.

The switch is the shop draw's seasonal drain, which varies per game. A constant in the schedule can
only ever be right about half the time. `SHOP_ADAPT_CROPS` is the disabled machinery for exactly
this, and its own docstring says the pairs as written should not be re-enabled — but names the axis
it believes in: wheat against strawberry+melon.

Next step is `scripts/crop_seed_sweep.py`: the knobs crossed with 24 seeds against a field, with each
seed's drain recorded alongside, so the question "is the optimum a constant or a function of the
draw" can be answered rather than assumed.

## 3. The goose kill was 23 hours too early

`REGISTER.md`'s third version caveat already voids every geese/eggs verdict taken before `c99a8a5`
(2026-08-13), when `SELLABLE` finally held all nine products. The dating makes it sharper:

    2026-08-12 06:34   7a88d30   "Delete the geese rather than leave a losing flag in the tree"
    2026-08-13         c99a8a5   CARROT, TOMATO and EGG become sellable at all

The geese were deleted **before** an egg could be sold at any price. That measurement could only
have come out negative.

What it never saw:

    animal   cost  structure  first yield  interval  max_held  product
    GOOSE    $300  COOP       d4           1         4         EGG
    COW      $400  PASTURE    d8           2         6         MILK
    SHEEP    $500  PASTURE    d6           3         6         WOOL

The goose is the cheapest, the earliest and the fastest of the three, and EGG closed above base in
both losses while MILK sat at the floor.

Cautions before this becomes work. Animals in this repo have produced a **wrong negative five
separate times**; the standing lesson is to ask what the code could not express before trusting a
mechanic-level result, which is precisely what happened here. The real cost of an animal is the
daily FEED/CARE action load, not the purchase price. And EGG demand saturates at 358-537 units a
season, so this is a few geese, not a herd.

`plan.py` still carries `GOOSE`, `COOP` and `BUILD_COOP`, so the machinery is present.
