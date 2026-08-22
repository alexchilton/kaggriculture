# The student was taught to do nothing — 12.3% of the teacher's trades are labelled EMPTY

2026-08-22.
Measured on this Mac, `.venv`, `data/il/bundle_vocab.json` (197 entries), the four tape teachers over
719 turns each. Logs: `data/logs/probe_send.log`, `data/logs/probe_vocab_miss.log`.

**This supersedes `docs/the_student_never_hires_2026-08-22.md`.** That document blamed class
imbalance. The imbalance is real but it is not why the student emits nothing on turn 0. The label
itself says "emit nothing".

## The measurement

```
teacher market   : [['HIRE'],['HIRE'],['HIRE'],['HIRE'],['HIRE'],
                    ['BUY_ANIMAL','COW',2],['BUY_ANIMAL','SHEEP',2],
                    ['BUY_SEED','WHEAT',7],['BUY_SEED','MELON',12],['BUY_PRODUCT','WHEAT',6]]
teacher bundle ix: 0
greedy   bundle ix: 0   (match True)
greedy   decoded  : []
greedy   sendable : []
```

Identical on all four tapes. The student's bundle **matches the label exactly**. The label is wrong.

## The mechanism

`replays.encode_action` (`kagg/il/replays.py:128`) resolves the bundle through
`MB.load_vocab().index(...)`, and `Vocabulary.index` (`kagg/il/market_bundles.py:120`) is:

```python
def index(self, bundle):
    """Unseen bundles fall back to EMPTY -- a labellable decision, not a crash."""
    return self._index.get(tuple(bundle), 0)
```

The opening bundle is not in the file:

```
bundle_of(opening) = (('BUY_ANIMAL','COW'), ('BUY_ANIMAL','SHEEP'), ('BUY_PRODUCT','WHEAT'),
                      ('BUY_SEED','MELON'), ('BUY_SEED','WHEAT'),
                      ('HIRE',''), ('HIRE',''), ('HIRE',''), ('HIRE',''), ('HIRE',''))
in data/il/bundle_vocab.json?   False
```

The file holds `HIRE x10` and `BUY_PRODUCT WHEAT` as separate entries, but not this combination.
So the ten-order opening is labelled 0, index 0 is the empty bundle, and the student is trained to
send nothing on the most consequential turn of the game.

## How much of the teacher is unspeakable

```
tape                  seat   traded turns   not in vocabulary
92498144 (F,F)          0        333             45   (13.5%)
91907974 (F,T)          0        391             56   (14.3%)
92466371 (T,F)          0        366             31   ( 8.5%)
91906088 (T,T)          1        361             47   (13.0%)
TOTAL                            1451            179  (12.3%)
```

The misses are not the tail. They are the structural purchases:

```
turn  0 (d0 h0)   the whole opening -- 5 HIRE, 2 COW, 2 SHEEP, wheat + melon seed, wheat stock
turn 48 (d2 h0)   HIRE x4          -- the second crew
turn 72 (d3 h0)   SELL FERTILIZER 4, BUY_ANIMAL COW 1, HIRE x2
turn 73 (d3 h1)   BUY_ANIMAL COW 1, BUY_SEED CARROT 1
```

Every one of those is a commitment the rest of the season depends on.

## Why no metric caught it

Three at once, and they reinforce each other:

- **`bundle` agreement counted these as correct.** The student emitted 0 and the label was 0, so
  every mislabelled turn scored a hit. 0.9983 was a real number about a corrupted target.
- **`traded` agreement excluded them by construction.** It is gated on `t_bundle != 0`, so the
  179 turns where the teacher traded and the label says otherwise were dropped from the
  denominator — the exact turns worth measuring.
- **The fallback is silent and returns a valid index.** `load_vocab`'s own docstring warns about
  this class of failure: "nothing offline shows it because every index is still a valid index".
  It warns about two vocabularies disagreeing. This is one vocabulary that is simply too small,
  and the same sentence applies.

## The earlier coverage number was wrong

`docs/dagger_tape_teacher_2026-08-22.md` records:

```
existing vocab   197 entries
coverage         2876/2876 tape turns  100.000%, 0 missing bundles
```

That is false and it is my error. The correct figure over the same four tapes is **179 of 1451
traded turns missing, 12.3%**. The 100% number was measured against the recorded tape JSON rather
than against what `TapeTeacher` actually emits per turn, and the two are not the same object — the
teacher's market list is built live and includes the hires.

## What this invalidates

- Every bundle-head number in the tape-v2 run, rounds 0-31.
- The class-weighting work done this session. It is not wrong, and the loss change is tested
  (`tests/test_the_opening_bundle_is_weighted_by_how_rare_it_is.py`), but it was aimed at the wrong
  cause and cannot fix a label that says EMPTY.
- The d0-d1 gate result. `turn0 bundle 4/4` at round 0 of the d01 run means the student matched a
  corrupted label four times out of four, not that it plays the opening.

## What it does not invalidate

The unit heads. `op`, `crop`, `item` and `qty` come from `action["farmer"]` and `action["hands"]`
and never touch the vocabulary. `greedy op 0.9785` over 719 turns and 0.9939 over 48 stand, and the
HARVEST split in `docs/harvest_is_one_tape_not_one_op_2026-08-22.md` is unaffected.

## What the fix then exposed: the anneal gate reads the wrong decode

Rebuilding the vocabulary made the opening learnable, and the first run on it found a second defect
immediately.

```
round 0  sample op 0.9923 bundle 0.0104 | greedy op 0.9939 bundle 0.8958 | turn0 0/4  fresh 1.5074
round 1  sample op 0.9939 bundle 0.0104 | greedy op 0.9939 bundle 1.0000 | turn0 4/4  fresh 1.2203
round 2  beta 0.89
         sample op 0.5539 bundle 0.0052 | greedy op 0.5548 bundle 0.9635 | turn0 4/4
```

One round after the bundle head was reset, the GREEDY decode emits the opening on all four tapes.
Good. But beta annealed at round 1, on `greedy op` 0.9939 clearing the 0.99 bar, while the market
head the student would actually play was at `sample bundle` **0.0104** -- reset one round earlier and
barely trained. `op` agreement fell 0.9939 -> 0.5539 on the next round.

Two mistakes in one gate:

- **It read `greedy` while the rollout plays `sample`.** The stated reason was that greedy is the
  ceiling and sampled agreement can sit low purely from entropy. That argument holds for a trained
  head. For an untrained one, low sampled agreement is not entropy, it is ignorance -- and the
  entropy case is exactly when handing over the wheel is wrong anyway, because the game receives the
  sample.
- **It read `op` only.** A head that had never been trained could not count against it.

Fixed in `dagger_tape.anneal_agreement`: the minimum over the SAMPLED `op` and `bundle` rates, with
an empty denominator scoring 0 rather than 1. Pinned by
`tests/test_the_anneal_gate_reads_the_decode_that_drives.py`, which uses the round-1 numbers above
as its first case.

## The fix

Rebuild the vocabulary from the bundles `TapeTeacher` actually emits, not from the recorded JSON,
and make the fallback loud. Two parts, and the second one matters more than the first:

1. `scripts/build_bundle_vocab.py` over the four teachers' live output. The union must fit
   `P.N_BUNDLES = 256`; the current file is 197 and 179 misses will not all be distinct, so the
   headroom needs measuring before assuming it fits.
2. **A silent fallback to index 0 must not survive.** Labelling is not inference: at label time an
   unknown bundle is a bug, and the run should refuse rather than teach the policy to do nothing.
   Whatever replaces it, the count of fallbacks belongs in the round log.
