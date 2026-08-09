"""OPEN DEFECT, diagnosed 2026-08-09, not yet fixed. See `docs/fable_the_animals_that_die_2026-08-09.md`.

`consecutive_unfed >= 2` deletes an animal outright (`reference/kaggriculture.py:792-806`) and it
is irreversible: a bank total never shows it, because a late loss barely dents the final figure
while destroying an asset that pays out every remaining day.

Measured on the shipped agent (`kagg.search.schedule_agent.make_agent`, default flags, `router=True`,
the real `data/seed_scripts/top_guys/90976060/schedule.json` fixture), mirror match (both seats
identical), full 720-turn season: **5 of 7 seeds lose at least one animal** (11, 13, 17, 23, 29;
clean on 19 and 41), 21 distinct death events (42 counting both mirrored seats), herds of 12-21.
This is systematic, not a rare one-off.

Two mechanisms, both real, roughly evenly split across the 21 events:

1. **Genuine early-game supply shortage.** `shed WHEAT at dawn` is 0 or 1 on the day(s) that seal
   the death, for established animals placed day 0-4 that die day 9-11 (seed 13's `COW (1,4)`,
   seed 17's `COW (2,4)` and `SHEEP (3,4)`, seed 23's `COW (1,3)`, seed 29's whole day-9/10/11
   cluster). This is a buy-side timing question and out of scope here (`CLAUDE.md`: do not touch
   the feed-buy line).
2. **Freshly-placed animals never revisited, wheat abundant.** `shed WHEAT at dawn` is in the
   teens; nobody stands on the animal's own tile at all on the day it dies ("no hand/farmer ever
   stood on `pos` this day" for seed 11's `SHEEP (0,4)`, seed 13's `COW (3,8)`, seed 29's
   `SHEEP (7,3)`). This is a pure routing/priority miss, not a supply problem.

`URGENT_OPS = ()` (`kagg/search/schedule_agent.py:1127`) is the code whose own docstring describes
mechanism 2 exactly -- "an animal must be fed and cared for on the day it lands... Placed at hour
18 it simply cannot be served" -- and says it was "Re-enabled 2026-08-07," but the shipped value is
the empty tuple, i.e. still disabled. **Flipping it to `("PLACE",)` was tested directly and made
ZERO measured difference** (18 deaths either way across seeds 11/13/17) even though `_router_acts`
(where it is read) is unconditionally on the `router=True` path. The mechanism the flag targets is
real; the flag as wired does not fix it. Root cause of *why* it does not fix it is still open.
"""

import sys

import pytest

sys.path.insert(0, "scripts")


@pytest.mark.slow
@pytest.mark.xfail(reason="OPEN DEFECT, diagnosed 2026-08-09, not fixed. See "
                          "docs/fable_the_animals_that_die_2026-08-09.md. Systematic on 5/7 "
                          "seeds (11,13,17,23,29), 21 distinct deaths, two mechanisms: early-game "
                          "wheat shortage and a routing/priority miss on freshly-placed animals. "
                          "URGENT_OPS=('PLACE',) was tried and measured to make zero difference.")
def test_the_shipped_agent_does_not_lose_animals_on_seeds_11_13_17():
    """Pins the defect so a future fix has something concrete to turn green.

    Not `assert not deaths` on one seed -- seed 19 and 41 are already clean by luck, and a
    single-seed pin would not distinguish "fixed" from "drew a clean seed."
    """
    import animal_death_diag as D

    total = 0
    for seed in (11, 13, 17):
        r = D.run_seed(seed)
        total += len(r["deaths"])
    assert total == 0, f"{total} animal deaths across seeds 11, 13, 17 (shipped defaults)"
