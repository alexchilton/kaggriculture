# Ladder analysis — does local win rate predict anything?

Written 2026-07-31, after v4/v5/v6 were all live on the ladder for several hours.
Analysis only — no agent code, submissions, or commits happened as part of this file.

## 1. Current ladder state

Pulled via `kaggle competitions submissions -c kaggriculture` and
`kaggle competitions episodes <id>`, re-checked at the end of this session:

| Submission | Ref | Ladder score (now) | Episodes played | Non-validation games |
|---|---|---|---|---|
| v4 — melon quadrant | 55143831 | 526.4 | 13 | 12 |
| v5 — opponent-pool tuned | 55144539 | 590.8 | 14 | 13 |
| v6 — deferred selling | 55145002 | 622.0 | 9 | 8 |

**This already contradicts the framing this task started with.**
The task brief quoted v5 = 613.5 and v6 = 550.6 — v6 *below* v5, the "central question."
Re-pulled just now, the numbers are v5 = 590.8 and v6 = 622.0 — **v6 is now above v5.**
Nothing about either agent changed in between; six more games (v6 went from 3 to 9 total
episodes) were enough to flip the ordering. That is not a side note — it **is** the
answer to "does the ladder rating hold still long enough to read": no, not at these
sample sizes. Whatever conclusion gets drawn from a snapshot this small should be held
loosely, including everything below.

For scale: the field's day-1 median average score was 670 and the top was ~1400
(`docs/experiment_log.md`, `docs/competition_brief.md`). All three of our submissions
are still below the 600 starting rating or barely above it.

## 2. Replay-derived win rate, real ladder opponents

`kaggle competitions episodes <id>` lists every episode a submission has played; every
public (non-validation) one was downloaded and scored by comparing final bank
(`rewards`, which matches each farm's terminal `money`). This is **not** the curated
5-8-strategy local pool — every opponent here is a distinct ladder team, playing
whatever they actually submitted.

| Submission | W-L | Win rate | Mean our bank | Mean opponent bank |
|---|---|---|---|---|
| v4 | 5-7 | 41.7% | $27,188 | $31,989 |
| v5 | 6-7 | 46.2% | $30,008 | $33,127 |
| v6 | 5-3 | 62.5% | $32,604 | $18,363 |

The ordering (v6 > v5 > v4) matches both the ladder-score ordering above and the
direction of the local win-rate work (deferred selling measured +9pts locally, v6 > v5
here too). That agreement is worth noting. **It is not proof of anything by itself** —
see the significance check below.

95% Wilson confidence intervals on those win rates, and a two-proportion z-test between
each pair:

| Comparison | z | Significant at p<0.05? |
|---|---|---|
| v4 (5/12) vs v5 (6/13) | -0.23 | No |
| v5 (6/13) vs v6 (5/8) | -0.73 | No |
| v4 (5/12) vs v6 (5/8) | -0.91 | No |

None of the pairwise differences clear even a lenient significance bar. The 95% CIs are
roughly [19%, 68%], [23%, 71%], [31%, 86%] respectively — they overlap almost entirely.
**On this data alone, v4, v5 and v6 cannot be distinguished from each other.** The
apparent staircase (42% → 46% → 63%) is consistent with real improvement, but seven or
eight games is nowhere near enough to separate that from three draws of the same coin.

**How many games would settle it.** Using a standard two-proportion power calculation
(alpha=0.05, power=0.8) against the observed effect sizes:

| Comparison | Games per arm needed |
|---|---|
| v6 (62.5%) vs v5 (46.2%) | ~146 |
| v6 (62.5%) vs v4 (41.7%) | ~90 |
| v5 (46.2%) vs v4 (41.7%) | ~1,909 (effect is too small to ever resolve cheaply) |

At the pace observed in the episode timestamps (roughly one game every 3-4 minutes per
submission while matchmaking was active), ~146 games is several hours of continuous
play, not something that resolves overnight, and matchmaking activity is not guaranteed
to hold that pace once the field's rating spread widens. **The honest answer to "is v6
genuinely better than v5" is: consistent with yes, not proven, and needs on the order of
100+ more games each to say for sure.**

### A confound worth flagging: opponents are not frozen either

Four opponent team names appear against more than one of our submissions:

| Opponent | vs v4 | vs v5/v6 |
|---|---|---|
| Sayandeep Ghosh | LOSS $27,640 vs $41,595 (STRAWBERRY 5, 100 tiles, 11 hands) | vs v6: LOSS $29,360 vs $31,392 (STRAWBERRY 6+TOMATO 2, 100 tiles, 11 hands) — same shape, much closer margin |
| FOYSAL | WIN $37,370 vs $24,289 (50 tiles) | vs v5: LOSS $25,156 vs $39,681 (75 tiles) — opponent farm grew and the result flipped |
| Garigariyong | LOSS $19,229 vs $28,512 (50 tiles, 5 hands) | vs v5: WIN $28,762 vs $24,219 (25 tiles, 3 hands) — opponent farm shrank and the result flipped |
| Chirapathleo Saelim | — | vs v5: WIN $42,593 vs $16,068; vs v6: WIN $34,968 vs $19,196 — consistent both times |

Two of four repeat opponents changed their own farm size and won/lost differently
between our submissions. Kaggle lets every team update daily too, so a same-named
opponent across two of our episodes is not a controlled comparison — their agent may
literally be different code by the second game. This makes any pre/post story ("v6 beat
the opponent v5 lost to") weaker evidence than it looks; it is corroborating, not
conclusive.

## 3. Is v6 genuinely worse than v5, or just less converged?

**Verdict: not enough evidence either way, and the evidence that exists points toward
"not worse."**

- The rating itself has already reversed once (550.6→622.0 for v6, 613.5→590.8 for v5)
  purely from more games accumulating — this is the single strongest piece of evidence
  that early ladder ratings for a submission with <15 games are not stable numbers.
- Replay-derived win rate has v6 ahead of v5 (62.5% vs 46.2%), matching the rating
  ordering and matching the local deferred-selling measurement's direction. But the
  z-test says this gap is not distinguishable from noise at n=8 vs n=13.
- v6 has played the fewest games of the three (8 non-validation vs v5's 13), which
  is itself consistent with "less converged" rather than "worse" — there has been less
  opportunity for its rating to regress toward its true value either way.

What would resolve it: roughly 150 games per submission at the current effect size, or
fewer if the true gap is larger than what these first 8-13 games suggest. Re-check both
ratings and re-pull replays after both submissions have accumulated ~100+ games, and
prefer the replay-derived win rate over the raw ladder score, since the score is itself
just an Elo update built from the same small number of games.

## 4. What actually beats us

Pooling every loss across all three submissions (17 losses out of 33 downloaded real
ladder games) and looking at what the winning opponent's farm looked like at the final
step:

```
Opponent crop mix, summed across all 17 losses:
STRAWBERRY: 48   PASTURE: 30   CARROT: 16   COOP: 14   TOMATO: 6   WHEAT: 2
```

**MELON is never what beats us — zero units, across every loss.** The melon-quadrant
strategy holds up defensively; nobody is out-competing us on the one crop with no shop
demand. The threats are strawberry (high base price, $300+/unit observed repeatedly)
and animal products (PASTURE/COOP tiles → wool and milk, priced $246-370/unit in these
replays, against wheat's $40-53 and melon's volatile $7-220).

Some of our worst losses by margin are pure animal plays:

| Opponent | Their bank | Our bank | Their farm |
|---|---|---|---|
| KevlarZanderChi (v4) | $104,185 | $22,715 | 15 tiles: 12 PASTURE + 3 STRAWBERRY, 0 hands |
| Nabid Nur (v5) | $92,891 | $35,859 | 8 tiles: 7 PASTURE + 1 STRAWBERRY, 13 hands |
| Seok, Jeongeum (v5) | $84,446 | $40,004 | 13 tiles: 10 PASTURE + 3 STRAWBERRY, 0 hands |

All three of the largest single-game losses on record are small farms (8-15 tiles, a
fraction of our 50) built almost entirely around PASTURE. Two of the three used **zero**
hired hands. This sits in direct tension with `docs/experiment_log.md` section 5's
"Animals: measured, and switched off" finding — that finding was built by testing cows
specifically against our own opponent pool, where they were net negative because a cow
needs 4-6 actions/day of routing. These three opponents are getting enormous returns
from small, low-labor animal farms in the real field. Either they are using a different
animal (sheep/goat for wool/milk rather than cow), a different routing pattern, or
benefiting from prices ($300+/unit for milk and wool here) that were not the prices
used when animals were tested locally. **This is a flag, not a recommendation** — the
scope of this task is analysis only — but it is the single most concrete lead in this
data for what an opponent is doing that we are not: high-value animal products on a
small, low-tile-count farm, worth a dedicated re-measurement before ruling animals out
again.

Secondary pattern: the mean unlocked-tile count of opponents who beat us is 60 (larger
than our 50), but most of that land is *bare* at the final step in many of these games
(e.g. Sayandeep Ghosh has 100 unlocked tiles and only 8 planted at the end; Nabid Nur
has 75 unlocked and only 8 planted). That is consistent with our own deferred-selling
finding — harvest and dump late, leave the field empty at the terminal snapshot — showing
up independently in opponents we did not build. It corroborates the mechanism, not just
the number.

## 5. Bottom line

- **Local win rate cannot be trusted as a magnitude predictor.** Local pool win rates
  of 72-90% translate to real-ladder win rates of 42-63% against the actual field. The
  gap is not surprising — `docs/experiment_log.md` section 7 already found the local
  pool is self-similar (five to eight variants of our own heuristic) — but it means a
  number like "90.6% win rate" from the local arena should never be read as a probability
  of winning a real ladder game.
- **Local win rate's *ranking* (v6 > v5 > v4) is consistent with the ladder-derived
  ranking so far**, both in raw score and in replay win rate. That is a genuinely
  encouraging sign and the best evidence available that local tuning decisions are
  pointing the right direction. It is not statistically established at n=8-13 games per
  submission, and the ladder score for v6 already flipped once relative to v5 within the
  time this task was being written.
- **The honest status is: too early to tell, direction is favorable, here is exactly
  what would resolve it** — roughly 100-150 more real games per submission before the
  win-rate gaps found here clear a standard significance bar. Re-run this same replay
  pull and z-test once that many games exist.
- **The most concrete new lead**: small, low-labor PASTURE (animal) farms produced our
  three largest single-game losses across all three submissions, at prices well above
  what the local animal test used. Worth a dedicated re-measurement, not a rules-based
  conclusion — flagged here per scope, not acted on.

## Data and method notes

- Replays downloaded via `kaggle competitions replay <episode_id>`, one per non-validation
  episode for v4 (12), v5 (13, one of which — 89186921 — was already present in `data/`
  and had been mislabeled as a v4 loss in earlier notes; it is a v5 game, confirmed by
  cross-checking its episode timestamp against each submission's `episodes` listing),
  and v6 (8, its full history to date). 33 real games total, 4 v4/v5 were pre-existing.
- Farm tile parsing had one bug worth recording for future analysis scripts: a tile
  value of Python `None` means an **unlocked but bare/unplanted** tile, not a locked
  one. Locked tiles are the literal string `"LOCKED"`. An early version of the analysis
  script treated `None` as locked, which made every farm's unlocked-tile count look
  roughly half of its true value and made some opponents (e.g. LiXingtao, who dumped a
  full 25-tile quadrant right before the terminal snapshot) look like they had no farm
  at all. Fixed before any number in this document was produced.
- Win/loss is decided by comparing each side's terminal `money` from the replay's
  `rewards` field, matched to team name via `info.TeamNames`.
- Script used: `/private/tmp/claude-501/-Users-alexchilton/b000a5e4-fb05-4d3a-b2b4-a09ca96f7e2e/scratchpad/aggregate.py`
  (scratch, not committed — rerun logic if this needs repeating; it is about 80 lines
  and reads every `data/*.json` replay, maps episode id to submission, and prints a
  per-submission and pooled breakdown).
