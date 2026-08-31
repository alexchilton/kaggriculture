# The mask and the logits were indexing different vocabularies

2026-08-28.
**Corrected.** The first version of this document blamed covariate shift. That was wrong, it was
asserted without measurement, and Alex rejected it on a fact this repo has recorded all along: the
start board is FIXED across every game (`project_kaggriculture_start_state_is_fixed` -- same tiles,
NW only, $3,000, no shops; only the opponent, shop-unlock timing and weeds vary). The wrong version
is left described below rather than deleted, because how it was reached is the reusable part.

## The contradiction

`scripts/the_planner_drives_and_the_net_supplies_the_market.py`, epoch-23 kawa clone
(`data/bc_runs/bcr_kawa_v2-20260828-094747/latest.pkl`), planner replay OFF, idle opponent:

```
        seed      planner       hybrid       delta   net traded
        9000      150,396          112    -150,284      11/719
        9137      179,719           72    -179,647      12/719
        9274      135,885          194    -135,691      47/719
        9411      187,461            9    -187,452      39/719
      median      165,058           92    -164,966
  net playing EVERYTHING (units and market): $25 on all four seeds
```

`scripts/is_the_market_head_empty_or_just_never_decoded.py`, same checkpoint, 8,000 of the 145,815
cache rows where the teacher traded:

```
  top-1 (as decoded today)            86.7%
  top-1 with EMPTY suppressed         88.8%
  truth in top-3                       97.9%
  median rank of the true bundle          0 of 256
  mean P(EMPTY)                        2.6%
  mean P(true bundle)                 75.8%
```

86.7% exact-basket accuracy at 75.8% confidence, against 11 market orders in 719 turns.

## The cause

`kagg/agents/neural.py` resolved the vocabulary correctly for DECODING -- preferring the
checkpoint's own, and printing that it did:

```
neural: checkpoint vocabulary is 256 bundles, data/il/bundle_vocab.json holds 197 --
        using the CHECKPOINT's, which is the one these weights were fitted against.
```

and built the legality MASK from a different one:

```python
_BUNDLE_SELLS = _MB.valid_table(_MB.load_vocab(), pad_to=_PP.N_BUNDLES)   # no path -> the 197
```

Measured, on the same checkpoint:

```
  index 1: ckpt = [SELL FERTILIZER]              mask table = [HIRE x10]
  index 2: ckpt = [SELL FERTILIZER, SELL WHEAT]  mask table = [BUY_PRODUCT WHEAT]
  index 3: ckpt = [SELL WHEAT]                   mask table = [SELL FERTILIZER]
  index 4: ckpt = [BUY_PRODUCT WHEAT]            mask table = [SELL WHEAT]
```

Every index means a different basket on the two sides. `masks_for` therefore asked whether some
*other* basket was affordable and in stock, `_masked_logits` sent the network's actual choice to
`-inf`, and EMPTY at index 0 -- legal in every state -- won the argmax.

**Invisible in every offline number.** The loss and the agreement metric take labels and mask from
the same `bc._vocab()`, so they agree with each other. Only play crosses the two.

`bc._bundle_sells` states the rule and gets it right: *"`_vocab()`, not a second independent
`load_vocab()`: the mask and the labels must be the same file or a bundle legal under one is a
different basket under the other."* `neural.py` is the copy of that pairing that was never fixed.

Fix: `_bundle_sells(vocab)` takes the resolved vocabulary, cached per vocabulary object.
Pinned by `tests/test_the_mask_and_the_logits_agree_about_what_a_bundle_index_means.py`.

## The wrong answer, and why it was reached

The first reading was: the head is fitted on カワシギ's boards and asked about the planner's, so it
is off-distribution and emits EMPTY.

It is wrong because the start state is identical for both, and -- more to the point -- because it
was never measured. `CLAUDE.md` states the rule that was broken, in the exact situation it was
written for: *"Two numbers that cannot both be true mean the metric is misread, not that reality is
surprising. Do not invent a mechanism to reconcile them. Go and read what the quantity counts."*

Covariate shift is a real phenomenon and it is the standard explanation for a BC clone playing worse
than it scores, which is precisely what made it easy to reach for and hard to doubt. The
distinguishing question -- what differs between the offline path and the play path *other than the
board* -- takes one grep and finds a vocabulary mismatch in five lines of source.

The earlier decode hypothesis in the same session was also wrong, and was killed by the same script
that produced the 86.7%: `mean P(EMPTY)` is 2.6%, and suppressing index 0 moves top-1 by 2.1 points.
There was no mass on EMPTY to reclaim, because the mass was never the problem -- the mask was.

## What follows

- Re-measure the hybrid on the corrected mask before drawing any conclusion about the clone. The
  earlier table measured a masking bug, not the clone.
- The same question applies to every other consumer of a bundle mask. `bc.py` is correct;
  `neural.py` was not; `eval_policy.py` and `play_checkpoint.py` are already recorded as rotted in
  neighbouring ways and have not been checked for this one.
- `ACTED 0.727` still is not evidence for play, for the reason it never was: it is measured with the
  labels and the mask drawn from one vocabulary, which is the configuration play does not use.
