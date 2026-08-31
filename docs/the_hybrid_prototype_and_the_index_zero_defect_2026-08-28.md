# The hybrid prototype, and the index-0 defect that made the first one meaningless

2026-08-28.
Two things happened in one session and they are connected: the vocabulary rebuild had a defect that
inverted its own purpose, and the hybrid prototype's first number is a measurement of that defect
rather than of the hybrid.

## 1. Index 0 means DO NOTHING, and a basket was sitting in it

`Vocabulary.index` returns 0 for any basket it does not hold, and `Vocabulary.from_bundles` pins
`EMPTY` at 0 for exactly that reason.
`load_vocab` does **not** go through `from_bundles` -- it builds `Vocabulary(raw)` straight from the
file -- so the invariant lives in the artifact and nothing checked it.

`scripts/build_recorded_player_bundle_vocab.py` wrote its 256 baskets most-frequent-first with no
`EMPTY`, so `data/il/bundle_vocab_kawa.json` had `SELL FERTILIZER` at index 0.
That breaks in two directions and only one of them is visible:

| | what happens |
|---|---|
| labelling | every `SELL FERTILIZER` turn labels to 0 = "place no orders", and is counted as a miss |
| playing | every genuinely silent turn *also* labels to 0, and `to_orders(0)` is `[["SELL","FERTILIZER"]]` -- the student posts a fertilizer sale on every turn the teacher trades nothing, and agreement scores all of it correct |

The row build reported **16,600 of 287,600 rows (5.77%)** against the 0.38% the builder had
predicted, which is what exposed it.
The second failure would not have shown in a miss count at all.

Fixed:

- `market_bundles.load_vocab` refuses a file whose entry 0 is a real basket.
- the builder reserves the slot (top 255 baskets + `EMPTY`) and reports its coverage by loading the
  file *back through `load_vocab`* -- the in-memory count is a different quantity from the one the
  row build reports, which is how 0.38% and 5.77% coexisted.
- `tests/test_the_vocabulary_reserves_index_zero_for_doing_nothing.py`, red first on both the
  loader and the artifact.

Miss rate for カワシギ's own play, same 400 seats, through the labeller that trains:

```
data/il/bundle_vocab.json          197 entries    14.5%   (5,641 HIRE, 4,894 SELL taught as nothing)
bundle_vocab_kawa.json  v1  256 entries, no EMPTY  5.77%
bundle_vocab_kawa.json  v2  256 entries, EMPTY@0   0.19%   554 of 287,600 rows
```

## 2. `bc_replay.py` checkpoints did not carry their vocabulary

`neural.make_agent` reads `ckpt["vocab"]` and falls back to `bundle_vocab.json` without it, printing
a warning.
Correct for the epoch-6 checkpoint, which was fitted against that file.
Silently wrong for anything fitted against the 256-entry player vocabulary: every bundle index would
decode to a different basket, all season, with nothing to read anywhere.
`bc_replay.py` now writes `vocab`, `vocab_size` and `epoch` into every checkpoint.

## 3. The hybrid prototype

`scripts/the_planner_drives_and_the_net_supplies_the_market.py`.
Alex's split: the planner routes the crew, the clone decides the trades.
It targets the measured shape of the clone's error -- MOVEMENT 60.3% against WORK 84.9%, with
routing being the half the planner exists for and the market being the half a router cannot see.

One delta between the two arms: identical planner, identical routes, identical seed, and
`action["market"]` replaced.
`REPLAY_OPENING_DAYS` is emptied in memory so the planner plays the board rather than replaying
カワシギ's recorded ops keyed on turn index.

Epoch-6 checkpoint, 719 turns, idle opponent:

```
        seed      planner       hybrid       delta   net traded
        9000      150,396        2,940    -147,456      24/719
        9137      179,719        2,251    -177,468       6/719

      median      165,058        2,596    -162,462
```

**This is not a verdict on the split.**
カワシギ trades on **51.0%** of his turns (155,211 traded of 423 x 719).
This clone trades on 0.8% and 3.3%.
Its market head is silent, which is what a head fitted through a vocabulary that taught 14.5% of the
teacher's trades -- the whole opening, every crew hire -- as DO NOTHING should do.
The hybrid ends *below* its $3,000 start: it spends a little and never sells.

The planner baseline reproduces independently, which is the one thing this run does establish:
$150,396 and $179,719 here against a median of $167,828 over six seeds measured earlier.

**Re-run on the corrected-vocabulary checkpoint before concluding anything about the hybrid.**
If the market head still will not fire at the teacher's rate, the next thing to test is the other
split -- planner routes and forces the tile work, net picks crops -- which does not touch the market
head at all.
