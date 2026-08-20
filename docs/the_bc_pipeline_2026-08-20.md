# The BC pipeline, 2026-08-20: what was broken and what the numbers actually mean

Written the day BC round 0 first ran on 920,320 teacher turns.
Every claim here has a measurement behind it; where something is unmeasured it says so.

## The headline

**Nine defects were found, and seven of them were invisible to a passing test suite.**
Six would have silently wasted or corrupted the training run.
The pattern is the one CLAUDE.md already names: code that runs, returns something plausible, and is
wrong only where nothing looks.

## Defects, in the order they would have cost time

### 1. `fit_bc` could not have taken a single gradient step

`jax.value_and_grad` was called without `has_aux=True` while `bc.loss` returns `(total, per_head)`.
Every run would have died on "Gradient only defined for scalar-output functions" — after labelling
finished.

Nothing caught it because `label_games`, `build_bc_rows` and `fit_bc` each had passing tests and the
three had never been run in sequence.
`scripts/bc_smoke.sh` is now that sequence: 2 games, rows, 2 epochs, about 60 seconds.

### 2. Every SELL was emitted LAST at play time

A bundle is a sorted multiset and that sort is alphabetical, so
`BUY_ANIMAL < BUY_LAND < BUY_PRODUCT < BUY_SEED < HIRE < SELL`.
`orders_from_heads` walked that stored order verbatim.

The environment settles order slots **in sequence** — slot *i* takes its money before slot *i+1* is
quoted — and both simulators lay slots out sells-first (`game.py:70-77`, `jax_sim._order_book`).
That order exists precisely so the same turn's sells fund the ten hires.

So the jit path sold first and the real-environment path sold last.
A student replaying the teacher's exact bundle had its hires refused on a thin bank.
**No sim-side number could show it, because the sim path was the correct one.**

Found by review, not by us.
The three-decoder property test whose absence let it ship now exists.

### 3. The row build was killed by the OOM killer, all 16 workers

`build_bc_rows` read a whole 1.2 GB shard into a list of dicts before sizing the arrays.
No traceback: the logs stop after "vocabulary 197 of 256 slots", `free` showed nothing alive, and
the output directory was empty.

Rows now stream, and shards run in waves of 4 — 13 GB does not hold sixteen jax interpreters plus
their output arrays even after the fix.

### 4. Market quantities were rounded to ladder rungs

`SELL_BUCKETS = [0,1,3,10,30]` and `BUY_BUCKETS = [0,1,2,5]` were written down, never measured.
Measured against the teacher's own play, 20,000 turns per shard:

| op | orders | max | mean projection error |
|---|---|---|---|
| SELL | 70,411 | 68 | **27.2%** |
| BUY_PRODUCT | ~18,000 | 134 | **35.3%** |
| BUY_SEED | 28,123 | 23 | **16.5%** |

The distribution is flat, not peaky — SELL uses every value from 1 to 24 with no gaps — so the
ladder was a lossy encoding of a continuous quantity, not a coarse view of a clustered one.
`SELL WHEAT 18`, which the teacher played 2,983 times, came out as 30.

In imitation that error is a floor no training removes, against a number we already know exactly.
Replaced with a categorical whose class index **is** the quantity, capped at 64: exact for 99.79% of
SELL and 97.50% of BUY_PRODUCT.

HIRE is untouched and must stay so — all 123,520 of its orders are quantity 1, because `HIRE ×10` is
ten orders and its multiplicity lives in the bundle symbol.

### 5. `replays.encode_action` wrote `hire = 1`

The exact bug the bundle head exists to fix, alive in the label path.
The teacher hires ten hands in one turn on 18,666 of 920,320 turns.

### 6. The play mask vetoed sells the teacher makes constantly

`masks_for` refused any bundle selling a product the shed did not hold. Three measurements killed
the rule:

- The reference simply declines an unbacked sell — `reference/kaggriculture.py:653`,
  `if private["shed"].get(item, 0) <= 0: return False`. No penalty, no error.
- **48.75% of the teacher's own SELL orders have a pre-turn shed of zero** for that product, and
  **zero** of those 9,222 coincide with a same-turn DROP. They are the hourly re-offer.
- The BC loss is permissive, because the teacher's action is legal by construction. So the strict
  mask vetoed bundles the student was trained to emit — 52% of sell-turns — and the masked argmax
  handed that probability to the **next-ranked bundle**, which can be a live trade the teacher never
  made. A wrong trade, not a missing one.

A student that cannot emit what its teacher emitted cannot imitate it.

### 7. `masks_for` read a field that does not exist

`state.private.shed` on a `State` with no `private`. It crashed on every call and 18 green tests
never called it. Found by review.

### 8. Two solve-cost probes were invalid in the same way

The first set `mod.UNSOLVE_DAYS = ()` on a module with no such attribute.
The second patched `SOLVED_DAYS` in the source and then checked
`getattr(mod, "PRECOMPUTED_ROUTES", {})` — also absent, so the guard read the **default** and passed
for the wrong reason.
Both returned ~1.0× and both nearly got reported as measurements.

The bundle keeps its planner sources in `_SOURCES` as strings and execs them into `sys.modules`.
The name the code actually reads is `sys.modules["kagg.search.cover"].PRECOMPUTED_ROUTES`.

### 9. The instrument measured the shard it had just trained on

And compared only the marginal rate of empty bundles, which a model that is empty on exactly the
wrong 78.9% of turns passes perfectly.

## The numbers that turned out to mean nothing

**`0.788` bundle agreement is what an UNTRAINED network scores.**
Every head is zero-initialised (`jax_policy.py:195`, `kernel_init=zero`), so the logits are uniform,
argmax picks index 0, and index 0 is the empty bundle — which the teacher plays on 78.9% of turns.

Without a fresh-init baseline on the same rows, "learned the prior" and "learned nothing" are the
same number.
`scripts/compare_checkpoints.py` exists for this.

What does carry signal, smoke run, 3 epochs on 2 games:

```
                      entropy   of max   distinct   agree   agree/tr
UNTRAINED  bundle       5.545    1.000          1   0.788      0.000
           op           3.135    1.000          1   0.139          -
after ep2  bundle       4.068    0.734          1   0.788      0.000
           op           2.639    0.842          3   0.273          -
```

An **untrained** head is at maximum entropy with one distinct argmax — uninformative.
A **collapsed** head is at low entropy with one distinct argmax — confidently wrong.
Different failures, identical agreement number.
At 73% of maximum entropy the bundle head is underfit, not collapsed, so the earlier COLLAPSED
warnings were reading the wrong side of that line.

## What is genuinely sound

- **Normalisation.** Measured on the real npz, 20,000 rows: tiles `[-0.900, 1.750]` std 0.269, units
  `[-1.000, 2.699]` std 0.259, glob `[-1.394, 4.500]` std 0.442. Zero features with `|max| > 10`,
  zero inf, zero nan, nothing within 10% of the float16 ceiling. Money is scaled before storage, so
  the float16 overflow worry (65,504) does not arise.
- **The agent plays legally.** 2,876 turns through `kaggle_environments`, zero exceptions, zero
  orders out of slot order, zero bad quantities, zero over-length turns.
- **DAgger labelling is cheap.** Forcing every day through the live solver costs **1.2×**
  (0.0108 vs 0.0092 s/turn, seed 12345, d0–d12), not the ~100× assumed. 640 games on 16 workers:
  5 minutes solved against 4 shipped.

## The constraint nobody chose

**13 of 115 input features are identically zero across 20,000 rows** — TOMATO as crop tile, carried
item, seed and shed; GOOSE as animal tile, carried and shed; EGG as carried and shed.

The cause is the teacher's repertoire, not the encoder. It never plants tomato and has no geese, so
it never holds eggs.
**Imitation cannot reach a mechanic the teacher never demonstrates, at any data volume.**

The Kaggle replays do contain them (25 replays):

| mechanic | turns | games |
|---|---|---|
| PLANT TOMATO | 164 | 17/25 |
| BUY_SEED TOMATO | 106 | 17/25 |
| SELL TOMATO | 90 | 15/25 |
| BUY_ANIMAL GOOSE | 45 | 7/25 |
| SELL EGG | 210 | 7/25 |

So BC on the tapes could reach what BC on this planner cannot. Two caveats before that is a plan:

- The downloads are **selected losses**. Common is not winning.
- 164 tomato turns against 920,320 planner turns is **0.02%** of a naive mixture. The student would
  ignore it. It needs upweighting or a separate stage, not concatenation.

And note this interacts with a known bug: `SELLABLE` blocked CARROT, TOMATO and EGG from being sold
at all for a period, which invalidated four carrot arms and the goose verdict. Two of the three dead
features are exactly those products, so "our teacher does not do it" may descend from that bug
rather than from a judgement.

## Still open

- **Per-day op-for-op agreement** — the acceptance measure. `scripts/per_day_agreement.py` reports it
  both off-policy (teacher drives, pure imitation) and on-policy (student drives, what play looks
  like); the gap between them is the covariate shift.
- **`bc_dagger.py`'s loss** is missing both padding corrections `bc.py` documents. Not on the DAgger
  path — `dagger_round.sh` uses `fit_bc` — but it is the RL warm-start path.
- **MLflow** is installed (3.10.1) and wired to nothing.
- **The value head is untrained** by BC, correctly: `bc.loss` has no value target. It enters RL at
  its initialisation.
