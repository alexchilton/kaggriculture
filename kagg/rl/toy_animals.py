"""A toy with two economies: an easy crop chain and a hard animal chain that pays better.

**What this is for.** The real policy learned melons and never touched livestock, across at least
three separate attempts (`docs/HANDOFF.md:964`, `:1363`, `:1421`, and the current run). The animal
economy is what actually wins -- `CLAUDE.md` measures FEED at +0.452 and CARE at +0.441 over 312 real
seats, and the top two agents drew ~83% of revenue from milk and wool. So the question worth settling
on a laptop is not "can RL learn a delayed payoff" -- `kagg/rl/toy.py` already showed it can -- but
**"can RL learn a chain whose every link must land and whose failure is a total loss, when an easier
chain is available?"**

**The structure being reproduced**, from the real game:

- An animal costs $300-$500 and **escapes after two unfed nights** (`jax_sim.py:1157`, matching the
  reference at `:786`), while its first yield is on day 4-8. So it must be fed *before* it can ever
  pay, and a single missed feed destroys the whole investment.
- FEED requires the unit to be **carrying wheat**, which means a separate trip
  (`jax_masks.py:96`). `commit.py:82-88` measured 629 FEED ops of which only 22.9% were carrying
  wheat.
- Meanwhile PLANT -> wait -> HARVEST is two actions on a tile the unit already stands on.

So the animal path is a repeating conjunction with a cliff, and the crop path is not. This module
keeps exactly that and nothing else.

**The two interventions it can test**, both switchable:

- `tend` -- one action that does the wheat trip *and* the feed, i.e. the `COMMIT_TEND` proposal.
  `commit.py:90-94` deliberately refused to chain two commitments because "ordering is where a
  mechanism starts becoming a plan"; the counter-evidence is that both single commitments are live
  in the current run and FEED is still ~0.00%.
- `start_animal` -- begin with an animal already owned and fed, so feeding can be discovered without
  first paying for the privilege.

Numbers are chosen so the animal economy is **strictly better than crops if executed**, which is what
makes a failure to learn it a real failure rather than a correct preference.
"""

import numpy as np

START_MONEY = 3000
BAR = 3000

# --- the easy chain: plant, wait, harvest -------------------------------------------------------
SEED_COST = 100
HARVEST_GAIN = 500
RIPEN = 12

# --- the hard chain: buy, feed repeatedly, collect ------------------------------------------------
ANIMAL_COST = 300
WHEAT_COST = 20          # one feed's worth, bought on the shed trip
ANIMAL_FIRST_YIELD = 4   # turns after purchase before the first collectable product
ANIMAL_INTERVAL = 2      # turns between products thereafter
ANIMAL_GAIN = 140        # per collection
UNFED_ESCAPE = 2         # matches the real rule exactly

EPISODE = 60

(NOOP, PLANT, HARVEST, BUY_ANIMAL, GET_WHEAT, FEED, COLLECT, TEND) = range(8)
N_ACTIONS = 8

NO_CROP = -1


class ToyFarmAnimals:
    """One season with both economies available.

    State is `(t, money, ripe_in, has_animal, unfed, yield_in, carrying)` and is fully Markov.
    """

    def __init__(self, start_t=0, start_money=START_MONEY, start_animal=False, tend=False):
        self.tend_enabled = bool(tend)
        self.start = (int(start_t), int(start_money), bool(start_animal))
        self.reset()

    def reset(self):
        self.t, self.money, has = self.start
        self.ripe_in = NO_CROP
        self.has_animal = has
        self.unfed = 0
        self.yield_in = ANIMAL_FIRST_YIELD if has else -1
        self.carrying = False
        return self.state

    @property
    def state(self):
        return (self.t, self.money, self.ripe_in,
                int(self.has_animal), self.unfed, self.yield_in, int(self.carrying))

    def legal(self):
        ok = np.zeros(N_ACTIONS, bool)
        ok[NOOP] = True
        ok[PLANT] = (self.ripe_in == NO_CROP) and (self.money >= SEED_COST)
        ok[HARVEST] = self.ripe_in == 0
        ok[BUY_ANIMAL] = (not self.has_animal) and (self.money >= ANIMAL_COST)
        ok[GET_WHEAT] = (not self.carrying) and (self.money >= WHEAT_COST)
        # The real conjunction: an animal, and wheat in hand. `jax_masks.py:96`.
        ok[FEED] = self.has_animal and self.carrying
        ok[COLLECT] = self.has_animal and (self.yield_in == 0)
        # The proposed commitment: the shed trip and the feed as one decision.
        ok[TEND] = self.tend_enabled and self.has_animal and (self.money >= WHEAT_COST)
        return ok

    def step(self, action):
        legal = self.legal()
        fed_now = False

        if action == PLANT and legal[PLANT]:
            self.money -= SEED_COST
            self.ripe_in = RIPEN
        elif action == HARVEST and legal[HARVEST]:
            self.money += HARVEST_GAIN
            self.ripe_in = NO_CROP
        elif action == BUY_ANIMAL and legal[BUY_ANIMAL]:
            self.money -= ANIMAL_COST
            self.has_animal = True
            self.unfed = 0
            self.yield_in = ANIMAL_FIRST_YIELD
            fed_now = True                      # arrives fed, as a bought animal does
        elif action == GET_WHEAT and legal[GET_WHEAT]:
            self.money -= WHEAT_COST
            self.carrying = True
        elif action == FEED and legal[FEED]:
            self.carrying = False
            fed_now = True
        elif action == COLLECT and legal[COLLECT]:
            self.money += ANIMAL_GAIN
            self.yield_in = ANIMAL_INTERVAL
        elif action == TEND and legal[TEND]:
            # One decision, the whole conjunction the rules impose: buy the wheat and feed with it.
            self.money -= WHEAT_COST
            fed_now = True
        elif self.ripe_in > 0:
            self.ripe_in -= 1

        # A crop advances only on a turn spent on nothing else -- same rule as `kagg/rl/toy.py`.
        if action != NOOP and self.ripe_in > 0 and action not in (PLANT,):
            pass

        # --- the animal's day, in the reference's order -----------------------------------------
        if self.has_animal:
            self.unfed = 0 if fed_now else self.unfed + 1
            if self.unfed >= UNFED_ESCAPE:
                # Escapes, taking the whole purchase price with it. No refund, no partial credit.
                self.has_animal = False
                self.unfed = 0
                self.yield_in = -1
            elif self.yield_in > 0:
                self.yield_in -= 1

        self.t += 1
        done = self.t >= EPISODE
        reward = float(self.money > BAR) if done else 0.0
        return self.state, reward, done


def crop_only_return():
    """Best bank using crops alone -- the fallback the policy already reaches for."""
    per_cycle = RIPEN + 2
    return START_MONEY + (EPISODE // per_cycle) * (HARVEST_GAIN - SEED_COST)


def animal_upside():
    """Roughly what one well-run animal adds, so the toy can assert crops are NOT optimal.

    Bought at turn 0, fed every other turn, collecting from `ANIMAL_FIRST_YIELD` onward.
    """
    collections = max(0, (EPISODE - ANIMAL_FIRST_YIELD) // ANIMAL_INTERVAL)
    feeds = EPISODE // UNFED_ESCAPE
    return collections * ANIMAL_GAIN - feeds * WHEAT_COST - ANIMAL_COST