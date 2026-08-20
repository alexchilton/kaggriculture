# カワシギ's decision points, scored as SELECTORS

2026-08-16.
Script: `scripts/decision_points.py`.
Log: `data/logs/decision_points.log`.
Machine-readable result: `data/logs/decision_points.json`.
Classification cache: `data/logs/decision_points_classify.json`.

## What was measured, and why this is not the separation table again

The belief under test is that the #1 player's season is a fixed tape plus a small number of binary
decisions taken off the board.
A previous analysis reported the *separation* table -- the rule cleanly splits his own games -- as if
it were a result.
It is not.
A rule that separates 51 games perfectly and does not beat the better of the two branches it selects
between is worth nothing.

So each decision point has three arms, and the arm under test is the third:

    always-A    play branch A's tape for the whole season
    always-B    play branch B's tape for the whole season
    selector    play A up to the decision turn, then switch to B if the rule fires

Every arm is a RECORDED TAPE on our seat.
Our own planner is not in the measurement at all.

Method, in one list:

- 96 seeds x 2 seats per arm = **192 games per arm, 1,152 games total**.
- Both seats, always. `_process_market` walks player 0 then player 1 per unit, so a tape moved to
  the other seat loses price priority. Identical policies do not draw here.
- `weedSpawnChance = 0.005`, the ladder value.
- One OS process per game (`--child` subprocess).
- Opponent: `data/sweep/frozen_1186_opponent.py`, a built bundle loaded by path with
  `importlib.util.spec_from_file_location`. It carries its own module copies and cannot share dials
  with the arm under test. No arm is ever the opponent.
- **Win rate is the score.** Money is printed as a diagnostic column only.
- Noise floor `2*sqrt(0.25/192) = 7.2%`. Anything smaller is a null, not a small effect.

**Every arm is open-loop and therefore handicapped.**
A tape cannot react to an opponent it never met.
A tape arm that WINS has won despite that handicap; a tape arm that loses proves less.
The comparison *between* arms is still fair, because the handicap is the same for all three.

## Classifying his 51 games

`data/seed_scripts/downloads_2026-08-13/` holds 79 JSON files.
Two of them (`91304798-0.json`, `91304798-1.json`) are bare step lists with no `info` block, so the
seat cannot be identified and they are skipped rather than guessed.
Of the remaining 77, **51 contain カワシギ**, which matches the brief.

Counting his own PLANT emissions -- a PLANT is emitted once, unlike a market order our agent
re-posts every turn:

```
  MELON  STRAW         WHEAT  games   episodes
     20     34       120-147     41   91889284 91890202 91892046 91893908 91894829 91895772 ...
     12     42       117-130      9   91891131 91892982 91896693 91897619 91898549 91899475 ...
     20     33       159-159      1   91918341
```

**The brief's 42/9 split is 41/9 plus one outlier.**
41 games are exactly MELON 20 / STRAWBERRY 34.
One more (`91918341`) is MELON 20 / STRAWBERRY 33 with WHEAT 159, well outside the 120-147 wheat
range of the melon-heavy class -- a different game, not a rounding difference.
The 9-game strawberry-heavy class matches exactly.

He wins 47 of these 51 games.

### The d3 rule does separate his games -- 51/51

Opponent MELON tiles at dawn of d3 (turn 72), read off his own replays:

```
  MELON/STRAW  games  opp melon d3 min   max  >= 9  YARN by d6
        20/34     41                 4     8      0       15/41
        12/42      9                 9    13      9        1/9
        20/33      1                 5     5      0        1/1
```

The two classes do not overlap and do not touch: melon-heavy tops out at 8, strawberry-heavy starts
at 9.
The threshold of 9 separates all 51 games.
**This is the hypothesis, not the result.** The result is further down.

### Representative tapes

Chosen as the game whose per-day action hashes agree with its class's modal day script on the most
days, ties broken on the episode name.
Deliberately **not** the richest game in the class: selecting the representative on money would put
the branch's luckiest board into the arm and then credit the branch with the board.

| decision point | branch | episode | why | his result in that game |
|---|---|---|---|---|
| dp1 | A, melon-heavy (MELON 20 / STRAW 34, 41 games) | `91919278` | agrees with the class's modal day script on 20/30 days | seat 1, $79,486 vs $80,026 |
| dp1 | B, straw-heavy (MELON 12 / STRAW 42, 9 games) | `91891131` | agrees with the class's modal day script on 21/30 days | seat 1, $67,971 vs $1,142 |
| dp2 | A, three-quadrant | `92498144` (`data/seed_scripts/kawashigi/`) | given in the brief | - |
| dp2 | B, four-quadrant | `91907974` | given in the brief | seat 0, $88,763 vs $49,859 |

Caveat on `91891131`: his opponent in that game collapsed to $1,142, so his own bank there says
little. It is used only as a source of *actions*, never of a result.

### The four-quadrant herd is COW 6 / SHEEP 10, not COW 6 / SHEEP 8

Read from the final observation of `91907974`:

    herd  COW 6, SHEEP 10          tiles owned  100
    crops WHEAT 142, MELON 20, STRAWBERRY 34, CARROT 7
    YARN_STORE unlocked by d6: True

The sheep count in the brief is wrong by two.
Note also that `91907974` is itself a **melon-heavy** game (MELON 20 / STRAW 34), so dp2's branch B
is not a strawberry-heavy tape.

### Splice validity

A selector splices two tapes at a turn. That is only exact where the two tapes agree before it.

```
  dp1  72/72 turns identical before the switch, no difference anywhere in d0-d2
  dp2  170/216 turns identical before the switch, first difference at turn 96 (d4)
```

dp1's splice is **exact**: the two branches are byte-identical for the whole opening, so the
selector arm is one season with a fork in it.

dp2's is not. The two tapes already differ on d4, so `dp2/selector` is a hybrid of two seasons and
carries an extra handicap that neither constant has. That matters for reading its number: it is a
lower bound.

## Result

Opponent `data/sweep/frozen_1186_opponent.py`, `weedSpawnChance 0.005`, 96 seeds x 2 seats.

```
arm                   games     WIN   draw   loss  mean $ (diag)  mean margin  B fired
--------------------------------------------------------------------------------------
dp1/always-melon        192   62.5%   0.0%  37.5%         89,381         +990
dp1/always-straw        192   60.4%   0.0%  39.6%         90,871       +1,067
dp1/selector            192   60.4%   0.0%  39.6%         90,871       +1,067     100%
dp2/always-3q           192   52.6%   0.0%  47.4%         86,455       -1,420
dp2/always-4q           192   19.3%   0.0%  80.7%         80,196      -13,701
dp2/selector            192   62.0%   0.0%  38.0%         86,896         +234      16%

noise floor 2*sqrt(0.25/n) at n=192 is 7.2%. Anything smaller than that is a NULL.
```

```
point  better constant       its WIN  selector WIN    delta  paired W-L   sign p  does the selector beat it?
------------------------------------------------------------------------------------------------------------
dp1    dp1/always-melon        62.5%         60.4%    -2.1%       31-35    1.000  NO -- and UNTESTED (see below)
dp2    dp2/always-3q           52.6%         62.0%    +9.4%        19-1    0.000  YES
```

The paired columns compare the selector with the better constant on the same (seed, seat).
They are secondary to the noise floor and are reported because the two arms share every board and
are byte-identical wherever the rule did not fire, which makes an unpaired floor over all 192 games
the wrong yardstick for them. A sign test on a handful of discordant pairs is not proof either.

## Verdict, decision point 1 -- melon vs strawberry at d3: NO, and the test did not run

`-2.1%`, inside the 7.2% floor. But the number is not the point.

**The rule fired on 100% of the 192 games.**
`frozen_1186_opponent.py` plays カワシギ's own schedule, which buys MELON 12 on d0, so it holds
**12 melon tiles at dawn of d3 on every seed** -- measured directly, seeds 1, 2, 3 all read 12.
The threshold is 9.
So `dp1/selector` is byte-identical to `dp1/always-straw` by construction, and its row reproduces
that arm to the dollar ($90,871 on both, 60.4% on both, 0 discordant pairs against it).

**This is a fact about the opponent, not evidence about the rule.**
A delta of 0.0 against a constant that the selector *is* reads exactly like a measured null, and
must not be recorded as one.

The mandated opponent is effectively a mirror of the player whose rule is being tested, and a mirror
cannot exercise a rule that keys on the opponent's crop mix.
For reference, the two branch tapes are also indistinguishable from each other here: melon-heavy
62.5% vs strawberry-heavy 60.4%, a 2.1% gap inside the same 7.2% floor.

To actually test dp1, a **built bundle** opponent holding fewer than 9 melon tiles at d3 is needed.
None exists in `data/sweep/`. The `cand_*.py` files there look like candidates but are not usable:
they `import kagg.search.schedule_agent` live and set module-level dials, which would overwrite the
arm under test in the same process, and their entry point takes `(obs, config)` and raises
`KeyError: 'step'` when called with a turn index. One would have to be built with
`scripts/build_planner_submission.py` and a melon-reducing dial.

## Verdict, decision point 2 -- four quadrants at d6: YES

`+9.4%` over the better constant, above the 7.2% floor, paired 19-1 (sign test p < 0.001).

The split by whether the rule fired is what makes it readable:

```
subset          games         always-3q       always-4q        selector
fired              30        3/30 = 10%     23/30 = 77%     21/30 = 70%
did not fire      162      98/162 = 60%     14/162 = 9%    98/162 = 60%
```

This is a clean interaction, not a main effect.

- The four-quadrant tape is a **disaster** as a constant: 19.3% over the season, 9% on the boards
  where YARN_STORE has not unlocked by d6.
- On the 30 boards where YARN_STORE *has* unlocked by d6, it inverts completely: 77% against the
  three-quadrant tape's 10%.
- `YARN_STORE in town.unlocked_shops` at the last turn of d6 identifies exactly those boards, and
  the selector converts a 10% subset into a 70% one.
- On the 162 boards where it does not fire, the selector is identical to `always-3q` by
  construction, which is why the whole-set delta (+9.4%) is much smaller than the subset delta
  (+60 points) -- the whole-set number is diluted by the 84% of games the rule never touches.

Two things bound this result:

1. The selector reaches 70% on the fired subset where `always-4q` reaches 77%. The 7-point gap is
   the splice: the selector plays the three-quadrant opening (d0-d8) and then the four-quadrant
   tape, and those two tapes already differ at d4. A tape solved as one season would presumably do
   better. **70% is a lower bound.**
2. The rule fired on 30/192 = 15.6% of our seeds, consistent with the project's existing "15 of 100
   seeds" note. In his own 51 games it fired on 17/51 = 33%. Those are different populations (our
   seeds 1-96 versus his ladder boards) and I have not checked why they differ. On the ladder the
   payoff scales with whichever rate is real.

## What this does and does not license

- dp2 is a **real, measured, positive selector**, and it is the first thing in this line of work
  that beats its own better constant rather than merely separating his games.
- dp1 is **open**. The separation is perfect and the mechanism is plausible (melon is the one crop
  no shop buys, so its price is set entirely by what the two farms dump into the town book), but no
  measurement has been taken. Do not carry the separation table forward as support for it.
- Nothing here says our live planner should adopt either branch. Every arm was a tape.
