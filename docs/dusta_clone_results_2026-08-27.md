# Cloning Crop Dusta: one win, three nulls, one disaster

Measured 2026-08-27. All duels 24 seeds (9000-9023), `weedSpawnChance` 0.005, seats swapped every
other seed, via `scripts/duel_dusta_vs_diment.py`. Logs in `data/logs/`, rows in the matching `.csv`.

## Results

| change | result | verdict |
|---|---|---|
| land retry | **+$5,570/game, 14-7-3** | KEEP |
| 8-arm selection | -$824, 11-13 | null |
| no-op substitution | -$61, 4-12-8 | null |
| d8-d13 live board | **-$64,326, 0-24** | broke the market coupling |
| Dusta tape vs Diment tape | -$13,896, 5-19 | Dusta transplants worse |

Builds: `scripts/build_dusta_clone.py`, `scripts/build_dusta_8arm.py`, `scripts/build_dusta_basics.py`.

## The one thing that worked: re-ask for the land

His tape issues `BUY_LAND` at fixed turns (ep 97710447: t=121 and t=218). `_do_buy_land` returns
SILENTLY when the bank is short (`reference/kaggriculture.py:717`) and a verbatim replay never asks
again. On seed 9023 that single refused order at t=218 on a $1,515 bank was the entire $59,463 gap:

```
   day |  DUSTA bank quad  crop |  DIMENT bank quad  crop
     9 |       1,515    2    38 |          220    2    30     <- dusta AHEAD
    13 |      13,290    2    37 |       15,430    3    49
    29 |      71,986    2     4 |      127,697    3    34
```

The rule: count how many `BUY_LAND` the tape had issued by turn t; if we own fewer parcels and a
market slot is free (cap 10, `:551`), re-issue it. `LAND_TURNS` is read off the tape at build time,
so it can never buy a parcel the tape did not.

**Why this survives when the d8-d13 rewrite did not:** it only ADDS an order. It changes no unit op,
so the shed contents and the goods flow are untouched and the tape's SELLs still find what they
expect. Cost is visible and bounded -- the 7 losses average -$407, from the $4,000 starving a later
order.

## Why the d8-d13 live board was a disaster

Replacing every tile-op with a board-derived one inside d8-d13 lost **0-24, -$64,326**.

The tile-ops and the market stream are COUPLED. `SELL WHEAT 150` assumes a specific shed; harvesting
on different turns changes what is in it, so sells and buys fail. It also overrode `PASS`, which in
his stream is often a deliberate wait inside a walk, so units worked instead of arriving.

**You cannot re-derive the unit ops and replay the market orders.**

## There is no d8-d14 problem

The claim "the tape royally screws up from d8" was WRONG, and it came from cross-game count spread
across 66 games -- which are 66 different seeds. Alex caught it: *"the opponent does NOT change our
board - you are playing it back on a different seed"*.

Direct measurement, tape replayed on 4 foreign seeds, counting tile-ops that do nothing:

```
   day  tile-ops   no-ops  % wasted
     0-8      ...        0        0%
     9        316        5        2%
    11        420       15        4%
    13        396        9        2%
    21        452       23        5%   <- worst day of the season
```

Zero waste through d8, at most 5% ever. That is why the no-op substitution measured null: there was
nothing to recover.

## The duel measures transplantation, not schedule quality

Home-and-away, each tape on its own seed against the other (`data/logs/home_and_away.log`):

```
  dusta HOME   dusta seat 0:  +48,621  dusta
  dusta HOME   dusta seat 1:  +69,687  dusta
  diment HOME  dusta seat 0:  -11,334  diment
  diment HOME  dusta seat 1:  -11,334  diment
```

Each wins at home, and Dusta wins bigger at home than Diment does. So -$13,896 on foreign seeds says
Diment's tape transplants better -- NOT that his schedule is better. Any ranking conclusion needs the
ladder, not this.

(Diment's two seatings are identical to the dollar. A seat swap should not be a no-op -- unchecked.)

## The identity gate

`data/logs/dusta_identity_gate.log`: our clone in his seat, on his seed, against his recorded
opponent.

```
main_dusta_clone_land: 0 of 719 turns differ   final $167,126 vs his $167,126
main_dusta_basics:     0 of 719 turns differ   final $167,126 vs his $167,126
```

Op-for-op, bank to the dollar. Every future variant should pass this before any duel. Note it CANNOT
fail for a pure replay -- it only has teeth for variants that add behaviour.

## Why the 8 arms bought nothing

`PREFIX_GATE` passes; 8 arms cover 64 of his 66 games:

```
    main       latch t=0     15 games   ep 97710447   $167,126
    d1_rich4   latch t=25    13         ep 97605226   $149,307
    d4_alt     latch t=115   13         ep 97680628   $134,182
    d3_gap     latch t=73     8         ep 97671475   $113,522
    d1_rich3   latch t=25     5         ep 100415025   $92,340
    d2_thin    latch t=49     5         ep 97641695   $156,697
    d1_lean    latch t=25     3         ep 97623441   $120,914
    d3_broke   latch t=73     2         ep 97701289   $107,415
```

11-13 against its own single-tape parent. The latch reads OUR bank at t=25/49/73/115, but on a
foreign seed that bank is not the bank that made him choose the arm. The tree was fitted on his
games and the feature is out of distribution -- the same failure as the `farm:0.445` lesson in
CLAUDE.md: a correct rule evaluated on the wrong unit.

## Process failures this session

- **Cross-seed comparison read as tape drift.** Twice. The second time cost a run that "proved" a
  tape replays identically on its own seed -- a tautology.
- **A decision-tree fit read features 2 turns late** and its winning feature (`seed_WHEAT`) was the
  result of the `BUY_SEED` it was predicting. Void; refit at the exact divergence turn.
- **A quantity-clipping fix was designed on a false premise.** `_process_market` commits sub-op by
  sub-op (`:619`), so a short bank already yields a partial fill. Caught before building.

## Behaviour cloning from Dusta (started 2026-08-27)

The tape route is closed at both ends: his actions diverge by d1 so there is only one legal latch
(turn 25), and the only feature varying there is our own bank, which does not transplant. A policy
conditioned on the board is the thing that can transfer.

### Dataset

`scripts/emit_dusta_bc_dataset.py` -> `data/bc/`

```
  per_turn.jsonl  217,031 rows  192 MB  60 classes   (movement EXCLUDED)
  per_day.jsonl     1,980 rows    2 MB               (66 games x 30 days)
  vocab round-trip: 0 failures over 486,483 actions  (data/logs/dusta_vocab_audit.log)
```

Movement is 55% of his actions and is excluded on purpose: a wrong step is LEGAL, so masking cannot
catch it, and one wrong step puts a unit out of position for a routed day. The router owns it.

### Per-turn head

`scripts/train_bc_perturn.py`, split by GAME (13 held out), 12s to train.

```
  majority class (WATER)  29.6%   <- meaningless
  TILE RULE               43.1%   <- the baseline that matters
  MODEL                   89.9%   +46.8%

  WATER          98% vs rule 28%      PICKUP WHEAT 2  91% vs 0%
  PLANT WHEAT    93% vs rule  0%      DIG            100% vs 0%
  FERTILIZE      30% vs rule  0%      HARVEST         96% vs rule 100%
```

Learning curve over games (13/26/39/52): 85.8 / 88.0 / 88.7 / 89.9. Still climbing, ~1.2 points per
doubling. **More episodes is the weakest lever.** The residual sits in classes the features cannot
express -- `FERTILIZE` at 30% because nothing in the row carries `fertilized_until_day`, the tile's
crop, or days since planting.

### Per-day head

`scripts/train_bc_perday.py`. Baseline is the per-day mean, which already encodes his fixed calendar.

```
  BUY_PRODUCT WHEAT   36%      BUY_SEED WHEAT        5%
  BUY_LAND            41%      BUY_SEED STRAWBERRY  -2%
  HIRE                31%      BUY_SEED MELON      -16%
  BUY_SEED CARROT     21%      BUY_ANIMAL COW      -28%
  total gain 32%
```

**Seeds and animals are not learnable beyond the calendar** -- a model is WORSE than just following
it. What is learnable is the wheat-loop volume, hires, land timing, and carrot (+21%, the drain
signal showing up where `data/logs/dusta_carrot_shops.log` measured it).

### First playable agent: BROKEN, and not because of the net

`scripts/build_bc_agent.py` -> `submission/main_bc.py`. Seed 9000 vs the Dusta clone:

```
  bc $136   dusta $76,628      (first version, no market layer at all: $3,000 -- untouched)
  ops:    PICKUP 2408, DROP 1515, BUILD_PASTURE 1065, PLACE 271, FEED 57, HARVEST 13
  market: BUY_LAND 579, SELL 492, HIRE 256, BUY_SEED 28
  final board: EMPTY 95, WEED 3, PASTURE 2
  11 ms worst turn against the 1000 ms limit
```

Four faults, all in the plumbing around the policy:

1. **PICKUP/DROP thrash (3,923 ops).** `private["inventories"]` is PER UNIT and was aggregated into
   one shed total, so the net cannot see what the unit is carrying. This is the top fix.
2. **BUILD_PASTURE 1,065 times for 2 pastures.** `_legal` permits building on any empty tile, so it
   is the default everywhere and fails almost always. The teacher built at four fixed tiles only
   (66/66 games at (4,4), (4,3), (3,4), (4,2)).
3. **BUY_LAND spam, 579 orders.** The retry fires every turn while the bank is short, burning slots
   against the 10-order cap and crowding out seed buys.
4. **Never planted or watered** -- 95 empty tiles, because seeds were never bought.

### Next steps, in order

1. Per-unit inventory as a feature (fixes 1).
2. Restrict BUILD/PLACE legality to tiles the teacher used (fixes 2).
3. Rate-limit the land retry to once per day (fixes 3).
4. Split the 60-class label into op / item / quantity heads -- `PLACE MILK 3` and `PLACE MILK 6`
   currently compete as separate classes.
5. Add `fertilized_until_day`, tile crop, days-since-planted; add the unit's previous op.

### Geometry, for whoever builds the placement head

```
  BUILD_PASTURE  identical in ALL 66 games: (4,4) (4,3) (3,4) (4,2), 66 each
  PLACE          the shed: (4,4) 3284, (5,4) 2688, (4,5) 1039 of 7,820
  PLANT          first 10 plants same tile in 94-100% of games; 26% by the 20th; noise after
```

Pens, shed drops and the first ~14 plants are constants. Only late planting needs a learned head.
