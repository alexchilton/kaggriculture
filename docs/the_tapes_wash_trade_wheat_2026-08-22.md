# Every tape we replay sells and buys WHEAT in the same turn, 18-39 times a season

Measured 2026-08-22, straight off the four recordings in `REPLAY_OPENING_TAPE`, own seat only.

| key | tape | bank | turns that SELL and BUY_PRODUCT the same good |
|---|---|---|---|
| `(False, False)` | `92498144` | 149,998 | **18** |
| `(False, True)` | `91907974` | 88,763 | **39** |
| `(True, False)` | `92466371` | 147,059 | **22** |
| `(True, True)` | `91906088` | 128,408 | **32** |

Every single one is WHEAT.
No other product appears once, on any tape.

They cluster late.
On the shipped `(True, True)` tape the offending turns are d10, then d18-d19, then d21, d23, d24,
d25, d26 and d27 — twenty-three of the thirty-two fall on or after d21.

## Why this matters

We replay these tapes on 719 of 720 turns, market orders included.
`schedule_agent.py:5830` — *"The rest of the market is the tape's, sells included."*
So every one of those turns is ours too, and each pays the spread twice for nothing: the SELL walks
the wheat price down, the BUY_PRODUCT walks it back up, and the net position barely moves.

This is not a hypothetical inefficiency.
It is the same class of thing as the `BUY_SEED` count trim already shipping on the melon arm, which
is worth +$240 on seed 11 — the turn stays the tape's, only the quantity becomes ours.

## What was nearly concluded instead, and why that was wrong

`tests/test_we_never_sell_and_buy_the_same_good_in_one_turn.py` has asserted this invariant since
2026-08-10 and has been red.
Its docstring blames **our** reserve arithmetic:

> the sell guard nets off wheat carried in hands and the dusk top-up does not, so the same 7-unit
> floor is short and satisfied in one turn

That was true when Fable found it, and it is not what fires now.
Measured both ways on the same file:

    replay ON   (shipped)   1 turn    d10 h14   SELL WHEAT 6 + BUY_PRODUCT WHEAT 11
    replay OFF  (planner)   2 turns   d4 h1, d9 h0

The replay-OFF turns are our planner's, and the planner is archived — it decides 1 turn in 720.
The replay-ON turn is the **tape's own**, and reading the tapes directly turns that one visible
turn into 18-39 per season, because the test only drives d0-d16.

The test also drives Seb's schedule on seed 11 while the agent replays カワシギ, so its board and
its orders come from different players.
Same incoherence as `test_the_first_seven_days_match_the_plan.py`, deleted earlier today.

## Recommendation, not implemented

**Net the two legs on a replayed turn.** Where a turn's market list contains both
`SELL X n` and `BUY_PRODUCT X m`, send only the difference, on the same turn, in the same
direction the tape intended.
The turn stays the tape's; only the quantity becomes ours — the exact rule already justified for
`BUY_SEED` and for the `BUY_ANIMAL` species re-label.

**This is a candidate, not a verdict.** Three things have to be checked before it goes anywhere
near the artifact, and two of them have bitten before:

1. **The bank is shared state on a replayed day.** `b105d05` is the standing warning: the
   `BUY_SEED` trim saved $60 at d6, which bought us a hire at d8 the tape was refused, and the
   seasons diverged for the rest of the run — 132 differing cells against 40. Netting changes the
   bank on the same turn, so it can do the same thing.
2. **The wheat is FEED.** A BUY_PRODUCT that looks redundant may be restocking the shed for the
   herd while the SELL is clearing a hand. `_commit_unit` sells from the shed, so the two legs may
   not be touching the same units at all.
3. **Measure on win rate, over contested seasons only.** `scripts/land_grid_verdict.py`, the same
   method as the tape shootout: a $43k win and a $4k win score identically.

Do not implement it on the reasoning in this document.
Run it as an arm on the town grid and let the number decide.
