# Leaderboard snapshot — 2026-08-03, day 4 of 62

Pulled from the live public leaderboard
(`kaggle competitions leaderboard kaggriculture`), CSV timestamped 2026-08-03T06:24:50.
**615 teams.**

## The field has moved and we have not

| | rating |
|---|---|
| Top (batuhan kalem, 2026-08-02) | **2723.3** |
| 2nd / 3rd | 2718.7 / 2679.9 |
| 20th | 2463.5 |
| **Median team** | **818.6** |
| Nominal starting rating | 600 |
| **Our best ever — v8 converter, 2026-08-01** | **600.5** |
| Our latest — v9 shepherd, 2026-08-01 | 548.4 |

**Our best submission would rank ~416 of 615. Our latest would rank ~459.**
We are in the bottom third and sitting on the starting rating, i.e. beating the field about as
often as we lose to it.

Top-20 ratings are a dense cluster from 2463 to 2723 — that is not one outlier who found an
exploit, it is a peloton. The median at 818 means the typical team has moved off the baseline and
we have not.

## What this does and does not change

- **It does not invalidate any of the RL diagnosis.** The critic terminal-blindness finding
  (`critic_terminal_blindness_2026-08-03.md`) stands on its own measurements.
- **It does invalidate any plan whose implicit target is "beat our v8 heuristic".** A 600-rated
  heuristic is not a rung on the way to 2700; the gap is 4.5x the baseline. Beating v8 by a wide
  margin locally still lands nowhere on this ladder.
- **`CLAUDE.md`'s "the ladder starts at 600, not 1000" is still correct and now reads differently.**
  It was written to stop us judging scores too harshly. Against a field whose median is 818 and
  whose top is 2723, the same rule says our submissions have gone essentially nowhere in four days.
- Our last submission was **2026-08-01**. Nothing has been submitted in two days.

## Worth knowing before the next planning pass

The competition launched 2026-07-30 and this is day 4 of 62. A field that reaches 2700 in four days
is very likely to keep climbing, so any target set against *today's* top is already stale. Whatever
gets built has to be aimed at where this curve goes, not where it is.

Nobody has yet checked **what the top teams are actually doing** — whether 2700 is reachable with a
strong heuristic or requires learning. That is a cheap and high-value question and it has not been
asked once.

Regenerate this snapshot with:

```
kaggle competitions leaderboard kaggriculture --download
```
