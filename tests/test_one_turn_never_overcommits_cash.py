"""A turn must not promise the same dollar twice.

`executor.decide` sizes each kind of purchase against the bank, but not against each other::

    budget = np.maximum(view.money - plan.seed_reserve, 0.0)               # :499   seed
    cash   = np.maximum(view.money - wheat_order * WHEAT_PRICE_CAP, 0.0)   # :570   animals

The animal budget deducts the wheat order. It does not deduct the seed order, and the seed budget
deducts neither. So seed, feed and livestock are each sized as though they had the whole bank.

Measured 2026-08-04 on day 0 of a real season with the leaders' allocation
(`data/logs/executor_cash_ledger.log`, `data/logs/executor_vs_tape_by_day.log`)::

    stake                          $3,000
    seed      20 premium seeds     $1,800     <- 60% of the bank, priced first
    wheat     feed                 $  956
    animal    1 cow                $  400
                                   -------
    committed                      $3,156     against $3,000 available

The reference settles the order list in slot order, so seeds fill and the animal purchase is what
gets refused. The season then runs $0 from day 5 to day 12, plants fall 20 -> 4 for want of seed
money, land slips from the tape's day 7 to day 13, and it ends on $0 against $147,178. The tape, on
the same board against the same opponent, finishes day 0 with four animals standing and $42 in hand.

**This is a bug the file has already fixed once, in a narrower place.** `executor.py:568` records it
for the species loop: "computing `afford` from `view.money` each time let all three species
independently believe they could afford the whole stake." The same reasoning was applied to
wheat-versus-animals and never extended to seed.

**The invariant is deliberately priority-free.** Whether seed should outrank livestock on day 0 is a
plan question -- `seed_reserve` is the gene for it, and the tape's answer is animals first. This
asserts only that the total is affordable, so a fix cannot be credited for picking a priority, and
picking a priority cannot be credited for fixing the double-commit.
"""

import numpy as np
import pytest

from kagg.search import executor as X
from kagg.search import library, rollout
from kagg.search import plan as P
from kagg.sim.farm import LAND_PRICES
from kagg.sim.game import Actions, Game

SEED = 0
WEED_CHANCE = 0.005
DAYS = 12


def _committed(decision, view, b):
    """Cash this turn's orders ask for, priced the way the reference will charge them.

    HIRE is excluded: `HIRE_COST` is Fibonacci in `hires_today` and a `Decision` does not carry that
    counter, so including it would need reconstruction that has already gone wrong once
    (`data/logs/executor_cash_ledger.log`, the exploding `hire-` column). Excluding it makes this
    test *weaker*, never wrong -- a failure here is a real overcommit with hiring still unpriced.
    """
    prices = view.prices[b].astype(float)
    seed = float((decision.buy_seed[b] * np.asarray(X.SEED_COST)).sum())
    wheat = float(decision.buy_product[b] @ prices)
    animals = float((decision.buy_animal[b] * X.ANIMAL_COST).sum())
    parcel = int(view.n_land[b])
    land = float(np.asarray(LAND_PRICES)[parcel]) if bool(decision.buy_land[b]) else 0.0
    return seed + wheat + animals + land


def _worst_overcommit():
    """Play a season and return the turn with the largest (committed - available) gap."""
    rng = np.random.default_rng(SEED)
    schedule = rollout.sample_unlock_schedule(rng)
    opponents = library.opposition()
    batch = opponents.shape[0]
    mine = P.decode(np.repeat(P.leaders_genome()[None, :], batch, axis=0))
    theirs = P.decode(opponents)

    game = Game(batch, weed_chance=WEED_CHANCE, rng=np.random.default_rng(SEED),
                unlock_schedule=schedule)
    worst = dict(gap=-np.inf)
    committed_any = 0.0

    for step in range(DAYS * 24):
        day, hour = step // 24, step % 24
        actions = Actions(batch)
        for player in (0, 1):
            view = rollout.build_view(game, player, day, hour)
            decision = X.decide(view, (mine, theirs)[player])
            if player == 0:
                for b in range(batch):
                    want = _committed(decision, view, b)
                    committed_any += want
                    gap = want - float(view.money[b])
                    if gap > worst["gap"]:
                        worst = dict(gap=gap, day=day, hour=hour, game=b,
                                     want=want, have=float(view.money[b]),
                                     seed=float((decision.buy_seed[b]
                                                 * np.asarray(X.SEED_COST)).sum()),
                                     wheat=float(decision.buy_product[b]
                                                 @ view.prices[b].astype(float)),
                                     animals=float((decision.buy_animal[b]
                                                    * X.ANIMAL_COST).sum()))
            rollout._write(actions, player, decision)
        if game.step(actions):
            break
    worst["total_committed"] = committed_any
    return worst


def test_a_turn_never_commits_more_cash_than_the_farm_holds():
    """**The claim.** Seed, feed and livestock must be sized against one shared ledger."""
    worst = _worst_overcommit()
    assert worst["gap"] <= 0.0, (
        f"day {worst['day']} hour {worst['hour']} (game {worst['game']}): committed "
        f"${worst['want']:,.0f} against ${worst['have']:,.0f} in the bank -- over by "
        f"${worst['gap']:,.0f}.\n"
        f"  seed ${worst['seed']:,.0f}  feed ${worst['wheat']:,.0f}  "
        f"animals ${worst['animals']:,.0f}\n"
        f"The reference settles in slot order, so the last orders in the list are silently refused.")


def test_the_season_actually_tries_to_buy_things():
    """Anti-vacuity: a farm that orders nothing satisfies the invariant and proves nothing."""
    worst = _worst_overcommit()
    assert worst["total_committed"] > 1_000.0, (
        f"only ${worst['total_committed']:,.0f} committed across {DAYS} days -- the invariant held "
        f"because nothing was bought, not because the ledger is shared")
