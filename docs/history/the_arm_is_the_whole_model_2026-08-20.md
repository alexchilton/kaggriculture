# The arm is the whole model

Measured 2026-08-20. Full 30-day seasons, held-out games, real environment.
Scripts: `scripts/clone_play.py`, `scripts/cache_turns.py`, `scripts/compare_players.py`.

## The structure

    trunk        d0-d6 (tetsuya)         identical in all 88 games, replays EXACT
    arm          crop + animal mix       a handful per player
    within arm   op sequence + jitter    the perturbation space

A "clone" is a lookup table keyed on `(day, hour, unit slot)` -- **no board state at all** -- built
from the games in one arm. It is not a network. It has no parameters. It plays a full legal
720-turn game.

## The board must NOT be in the key

Keying a unit on `(day, hour, x, y, tile-under)` fails completely, and not for want of data:

    board-keyed, held out          work ops off by 402 (79.3%)   FEED 0/85, CARE 0/85
    board-keyed, table = that game work ops off by 388 (76.5%)   FEED 0/85, CARE 1/85

It cannot reproduce a game whose table was built from that game alone. Position is an OUTPUT of the
sequence: one wrong move puts a unit on a square the teacher never occupied at that hour, every
later key misses, it falls back to the modal action -- PASS or a move -- and it never stands on a
pen again. Hence zero feeds all season.

**This is why 86.2% per-decision accuracy meant nothing.** That figure was measured on the
TEACHER'S states. On its own trajectory the same table scores 79.3% error. Per-decision accuracy on
expert states does not predict closed-loop play, and this project should not accept one as evidence
for the other again.

## The arm is worth more than the data

    tetsuya (88 games)                  kawashigi (140 games)
      no arm            25.6%             no arm            21.3%
      dominant arm      16.3%             arm @ 0.05        16.0%
      oracle arm (7)     3.7%             arm @ 0.03        13.0%
                                          oracle arm (7)     6.5%

Both players reach their best with **exactly 7 games in the arm**. That is probably the real
granularity of a tape: about seven games of genuinely identical play. Both are still improving at
the tightest threshold and both run out of games there.

The modal tape averages across arms that plant DIFFERENT crops, so at a slot where one arm plants
strawberry and another plants wheat the mode is "plant nothing". That is the whole of
`PLANT 66/212`; the animal cadence, identical across arms, transferred untouched.

    tetsuya, oracle arm, full season:
      PLANT 191/212   WATER 885/854   HARVEST 411/443
      FEED 353/353    CARE 352/353    COLLECT_FERTILIZER 363/353

## kawashigi was never harder -- we could not afford a tight enough arm

At 45 games his best was 16.9%. At 140 games it is 6.5%, from a 7-game arm at threshold 0.02. The
threshold sweep was monotonic at both sample sizes, so the limit was cluster purity, not the player.

**The 45 games were an artifact of `MIN_WINNER_BANK = 60_000`.** Removing the filter and pulling
2026-08-14..16 took him from 45 to 140. tetsuya appears in ZERO games before 08-19 -- he is a recent
arrival.

Three earlier readings that all said "kawa is harder" were reading this same data shortage:
board-keyed 72.0% against tetsuya's 86.2%, 34 clusters from 34 games, and 16.9% against 3.7%.

## The arm cannot be chosen at dawn

Purity of the arm given what is observable at each day, over 88 tetsuya games and 17 arms:

    day    shops predict arm    planted-so-far predicts arm
    d0           35%                      35%
    d3           41%                      35%
    d6           66%                      40%
    d9           77%                      61%
    d12          85%                      84%
    d14          85%                      92%

35% at d0 is the base rate of the dominant arm -- no signal. The shop draw only becomes useful at
d6 (66%) and good at d12 (85%).

**This is survivable because of the trunk.** d0-d6 is identical across every arm, so no choice is
needed until d7 -- exactly when the shop signal arrives. And the choice need not be irreversible:
open on the dominant arm and switch as the draw disambiguates.

Expected cost of a 66% pick at d7 is roughly `0.66 * 3.7% + 0.34 * 16.3%` = about **8%**, half the
error of always playing the dominant line.

## What this is, and what it is not

It is a classifier plus a replay table -- a glorified if/else, and that is an accurate description.
It plans nothing. It also beats the planner on d0-d10 (6.9% against ~9%) and is exact through d7
including the walking route, which the planner has never been on any day.

**It does not react.** It replays the same turns whoever it faces. That works only because the
seats interact solely through the shared market book, and it is the ceiling of the approach: it
caps at roughly the teacher's own strength. The teacher banks $94,906 mean and sits second on the
ladder, so the cap is a medal, not a win.

**As an RL teacher it is strong for initialisation and weak for DAgger.** It is queryable at any
state -- `(day, hour, unit)` always exists -- which is what our planner could not offer. But its
answer is "what he did at this hour", not "what is best here", so it cannot correct a student's
mistake. Good prior, poor corrector.

## Order of work

1. **Arm classifier.** 16.3% -> 3.7% is the measured headroom and the only step that makes this
   shippable. Everything else is confounded until it is done.
2. **Perturbation in `jax_sim`**, which scores an edit exactly. This is where a GPU earns its keep
   and where beating the teacher actually happens.
3. **RL from the tape as prior**, KL-anchored to it, terminal reward, gated on win rate against the
   frozen pool.

Doing 2 before 1 means hill-climbing a 16%-wrong copy and confounding every result with its
defects -- the same trap that made the care-bid change measure as a null this morning.
