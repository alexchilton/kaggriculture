"""A minimal plant-wait-harvest MDP, in numpy, for settling credit-window questions on a laptop.

**Why this exists.** Every claim about why the real run is stuck -- the credit window is too short,
the reward is flat over the occupied range, money shaping would fix it, a reverse curriculum would
fix it -- costs GPU-days to test on the real game and gets one noisy answer. This is the same
*structure* at 1/100th the size: it runs thousands of episodes per second on a CPU, so a 2x2 of
interventions is a few seconds rather than a week.

**What is preserved, and what is thrown away.** Preserved: money starts at a stake, spending precedes
earning, the payoff arrives `RIPEN` turns after the action that causes it, the reward is terminal and
binary, and the bar is what doing nothing achieves. Thrown away: the board, units, walking, the
market, the opponent's play, and every other op. If a fix does not work here it will not work there;
if it does work here that is necessary and not sufficient.

**The ratio is the point.** The real game has `RIPEN`-to-credit-window of roughly 240:20, so this
uses 12:1. Matching that ratio matters far more than matching any absolute number, because it is what
decides whether the cost of planting and the benefit of harvesting land in the same window.

Nothing here imports JAX and nothing here touches the trainer.
"""

import numpy as np

# Chosen so that exactly one plant-harvest cycle beats the bar and doing nothing does not:
# 3000 - 100 + 500 = 3400 > 3000. Anything less than a full cycle loses.
START_MONEY = 3000
BAR = 3000              # what an idle opponent banks -- the real `idle` seat, scaled
SEED_COST = 100
HARVEST_GAIN = 500
RIPEN = 12              # turns from planting to harvestable
EPISODE = 60            # ~5 possible cycles, as a 30-day season allows several crops

NOOP, PLANT, HARVEST = 0, 1, 2
N_ACTIONS = 3

NO_CROP = -1            # `ripe_in` when nothing is planted


class ToyFarm:
    """One episode of plant -> wait -> harvest, with a terminal win/loss against a fixed bar.

    State is `(t, money, ripe_in)` and is fully Markov: `ripe_in` counts turns until the crop can be
    harvested, `0` meaning ready now and `NO_CROP` meaning the ground is empty.
    """

    def __init__(self, start_t=0, start_money=START_MONEY, start_ripe=NO_CROP):
        """`start_t` and `start_ripe` are the reverse-curriculum knobs.

        Beginning at `start_t = 48` with `start_ripe = 0` is P2b in miniature: the spend has already
        happened, the payoff is one action away, and the terminal is close enough to reach.
        """
        self.start = (int(start_t), int(start_money), int(start_ripe))
        self.reset()

    def reset(self):
        self.t, self.money, self.ripe_in = self.start
        return self.state

    @property
    def state(self):
        return (self.t, self.money, self.ripe_in)

    def legal(self):
        """`[N_ACTIONS]` bool. NOOP is always legal, matching `jax_masks.py`'s rule for the real game."""
        ok = np.zeros(N_ACTIONS, bool)
        ok[NOOP] = True
        ok[PLANT] = (self.ripe_in == NO_CROP) and (self.money >= SEED_COST)
        ok[HARVEST] = self.ripe_in == 0
        return ok

    def step(self, action):
        """Returns `(state, reward, done)`. Reward is **terminal only** -- 0 on every other turn.

        An illegal action is a no-op rather than an error, mirroring the real simulator, which
        ignores an action a unit cannot perform rather than rejecting the turn.
        """
        if action == PLANT and self.legal()[PLANT]:
            self.money -= SEED_COST
            self.ripe_in = RIPEN
        elif action == HARVEST and self.legal()[HARVEST]:
            self.money += HARVEST_GAIN
            self.ripe_in = NO_CROP
        elif self.ripe_in > 0:
            # Only an otherwise-idle turn advances the crop. The `elif` is load-bearing: a second
            # decrement after a successful PLANT made crops ripen in `RIPEN - 1` turns, which
            # `test_a_crop_cannot_be_harvested_before_it_ripens` did *not* catch -- it asserted the
            # crop was unready before each of `RIPEN - 1` waits, which stays true when it ripens a
            # turn early. `test_playing_the_optimal_policy_by_hand_reaches_the_optimal_return` caught
            # it, because an off-by-one in the cycle length changes how many cycles fit in a season.
            self.ripe_in -= 1

        self.t += 1
        done = self.t >= EPISODE
        # `>` strict, and a tie pays 0 -- the real game pays 0.5 for a tie, but a fixed-bar opponent
        # makes an exact tie a measure-zero event and the binary form keeps the toy readable.
        reward = float(self.money > BAR) if done else 0.0
        return self.state, reward, done


def optimal_return():
    """The best achievable final bank, for calibrating whether a learner got there.

    A cycle is one PLANT, `RIPEN` waits, one HARVEST -- `RIPEN + 2` turns for a net `+400`.
    """
    per_cycle = RIPEN + 2
    cycles = EPISODE // per_cycle
    return START_MONEY + cycles * (HARVEST_GAIN - SEED_COST)


def credit_gap():
    """Turns between paying for a crop and being paid for it. The quantity this toy is about."""
    return RIPEN + 1
