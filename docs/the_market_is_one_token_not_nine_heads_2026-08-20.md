# The market is one token, not nine heads

Measured 2026-08-20 over tetsuya's 78 downloaded games, 56,082 seat-turns
(`data/seed_scripts/downloads_2026-08-19/`).

## The measurement

Treating each turn's whole `market` list as a single symbol (op+item set, quantities ignored):

    distinct market bundles: 346

      count   cum%   bundle
      45231   80.7  (empty)
       1504   83.3  SELL FERTILIZER
       1180   85.4  SELL WHEAT
       1057   87.3  SELL FERTILIZER, SELL MILK
        448   88.1  SELL STRAWBERRY
        400   88.8  SELL FERTILIZER, SELL WOOL
        271   89.3  HIRE x7, SELL MILK, SELL STRAWBERRY, SELL WHEAT
        268   89.8  BUY_SEED WHEAT, HIRE x5
        232   90.2  BUY_PRODUCT WHEAT
        231   90.6  BUY_PRODUCT WHEAT, HIRE x7
        217   91.0  BUY_SEED WHEAT, HIRE x6
        206   91.4  SELL STRAWBERRY, SELL WHEAT

    top 20  bundles cover 93.5% of turns
    top 50  bundles cover 96.5% of turns
    top 100 bundles cover 98.5% of turns

## Why the independent heads emitted no orders

**80.7% of his turns carry no market action at all.** Every marginal's base rate is therefore
overwhelmingly "no", and nine independent "probably no" decisions multiply into "certainly no".

That is the arithmetic behind the result already in `CLAUDE.md` -- greedy argmax over per-head
marginals emits zero market orders while the marginals themselves discriminate 12:1 on
`buy_product`. The information is in the marginals and the *product* of them destroys it. No amount
of head tuning fixes a product of nine sub-0.5 probabilities.

`kagg/rl/jax_act.py` already recognises this and mitigates it with a trade-mode latent
(`CONDITIONED_HEADS = ("sell", "buy_product")`), which is a low-rank version of the same idea. The
measurement above says the full version is cheap: the joint has only ~100 symbols worth modelling.

## The bundle that matters

    HIRE x7, SELL MILK, SELL STRAWBERRY, SELL WHEAT      271 turns

Seven hires and three sells in ONE turn. The sells occupy earlier order slots and settle first, so
they fund the hires in the same turn -- the mechanism recorded in `.claude/skills/matching-the-tape`
("the tape hires ten hands at h1-h2 from a five dollar bank while we reach nine hands late on $4").

This is exactly the coordination we lose. On d10, units 8 and 9 were never hired and 20 planned ops
died with them (`docs/plant_is_a_money_problem_2026-08-20.md`). As nine independent heads that
bundle is close to unemittable. As one token it is free, and the coordination is preserved by
construction rather than learned.

## What this implies for the BC track

- Replace the nine market heads with **one categorical over observed bundles**. ~100 classes covers
  98.5% of turns; 346 covers all of it. An incoherent order combination becomes unrepresentable
  rather than merely unlikely.
- **Quantities still need a head**, conditioned on the drawn bundle. This is the right place to
  spend the modelling: a wrong quantity is graceful (sell 4 instead of 5), a wrong bundle is
  catastrophic (never sell at all).
- The 80.7% empty rate also explains the parked BC track's absorbing state -- `bc.py` records
  `P(move) = 6e-5 per unit-turn` and a checkpoint banking exactly its $3,000 start. "Do nothing" is
  the majority label on both axes, so an unsmoothed clone converges to it. Label smoothing is
  already on by default in `kagg/il/bc.py`; the bundle head reduces how much work smoothing has to do.

## Caveats

- Quantities are ignored in the counts above, so 346 is a lower bound on the full joint. It is the
  right lower bound for the decode question, which is about WHICH orders are emitted together.
- This is tetsuya only. A second player's vocabulary has not been measured and there is no reason
  to assume it is the same size.
- tetsuya is **no longer #1** as of the 2026-08-20 leaderboard (Ryo Hasegawa 3153.4 against his
  3101.4), and we hold **zero** games of the current leader. Choosing the imitation target is a
  decision that should be made before a dataset is built around anyone.
