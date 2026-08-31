# Why the clone memorises the four tapes

2026-08-28.
The DAgger clone reproduces its four teachers to within $63 and banks $300 on seed 9000.
Three measurements taken today say why, and they replace the explanation given earlier in the
session, which was wrong.

## The tape is not a clock lookup after day 3

`scripts/when_do_the_four_teachers_stop_agreeing.py`, over the four tapes' recorded action streams:

```
FIRST DISAGREEMENT at turn 72  (day 3, hour 0)
  92498144  farmer ('PICKUP','WHEAT',4)  market [HIRE x5, SELL FERTILIZER 4]
  92466371  farmer ('PICKUP','WHEAT',4)  market [BUY_ANIMAL COW 1, HIRE x2, SELL FERTILIZER 4]
  91906088  farmer ('PICKUP','WHEAT',4)  market [BUY_ANIMAL COW 1, HIRE x2, SELL FERTILIZER 4]
  91907974  farmer ('PICKUP','WHEAT',4)  market [HIRE x5, SELL FERTILIZER 4]

turns 0..71 are IDENTICAL across all four tapes (72 turns, exactly 3.0 days)
turns 72..718: all four agree on 74 of 647 (11.4%)

distinct actions at the same turn index, across the four tapes:
  1 distinct     146 turns   20.3%
  2 distinct      44 turns    6.1%
  3 distinct      59 turns    8.2%
  4 distinct     470 turns   65.4%
  mean 3.186
```

The correction this forces: `REPLAY_OPENING_DAYS` replays by turn index, so the *mechanism* is a
clock lookup, and it was described here earlier as if the *labels* were too.
They are not.
The same clock index carries a mean of 3.19 distinct actions across the four tapes, so no clock
lookup exists to be learned.
After day 3 a tape is a board-conditioned policy that we have sampled four times.

The agreement breaks at turn 72 because that is when the first shop unlocks -- the draw lands at the
end of day 2 for day 3 (`kaggriculture.py:886`).
The four tapes are the four `(melon_armed, q4_armed)` arms of `REPLAY_OPENING_TAPE`
(`schedule_agent.py:3933`), and market agreement between any two of them, on turns where either
traded, is 14.2%-19.9%.
They are four different seasons, not one plan with a fork.

## The opponent block is a partial game ID, from turn 1

`scripts/is_the_opponent_block_a_game_id.py`.
`jax_obs` gives the net 14 opponent features; `melon_branch.trigger` consults exactly one of them,
once, on day 3.
Each tape was played against a different opponent.

```
distinct opponent blocks across the four tapes, at the same turn index:
  4 distinct     547 turns   76.1%
  3 distinct     167 turns   23.2%
  first turn the blocks differ at all: 1  (day 0, hour 1)

1-NN on the 14 opponent features -- train days 0-14, test days 15-29
          92498144   51.3%      92466371   73.8%
          91906088   56.3%      91907974   76.0%
               ALL   64.3%      (chance = 25.0%)

separability by day window (train first half, test second):
   0-3  75.0%     3-6  75.0%     6-12  56.9%     12-30  54.9%

per-feature (each alone):  f13 50.0%  f9 41.0%  f12 38.4%  f5 36.0%
```

64.3% against 25% chance, and 75% during days 0-3 -- the window in which all four tapes play
identical actions, so the tell precedes any behavioural divergence.

This says the information is present, not that the net uses it.
The ablation is what would say that, and it is one delta: blank 13 of the 14 and keep the melon
count.

**Do not narrow `_OPPONENT_WIDTH`.** `GLOBAL_FEATURES = 122` is baked into every checkpoint and row
cache. Zeroing preserves every shape.

**And do not blank it in `jax_obs.encode`.** Alex's point, and it is right: the block is a shortcut
for IMITATION, where the target is a teacher that consults one number, and it is potentially
valuable for RL, where the target is winning and there is no teacher to shortcut.
`jax_obs.py:11` already records that `contrarian`'s entire edge is reading the opponent's crop mix.
Two things a reward could find there that no teacher will teach: contested-crop avoidance, and
price-impact timing against a shared book we already know we flood (12 sheep took WOOL $239 to $11).
So the blanking belongs in the BC row build, not in the encoder.

## A method note

The first version of the separability test held out by TAPE, which is unanswerable by construction:
the held-out tape's label is absent from the training set, so the correct answer is unreachable and
every arm scored exactly 0.0%.
A uniform 0.0% across four independent arms is a design error, not a finding.
The fix was to hold out by time, which keeps all four labels present.
