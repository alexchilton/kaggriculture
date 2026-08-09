"""The hundred shed slots are one budget, and allocating them is a SORT, not a knapsack.

Task #46 asked for "shed slots as an explicit value-per-slot knapsack -- nine products and 100
slots is a small exact knapsack". This module is the measurement that answers it, and the answer is
that the knapsack has no combinatorial content:

**every unit of every product occupies exactly one slot** (`_drop_inventories_to_shed` counts
`sum(shed.values())` against `capacity`, `reference/kaggriculture.py:830-849`; there is no per-item
size). A 0/1 knapsack in which every item has weight 1 is solved exactly by taking items in
descending value -- there is nothing for a DP to search. `release_order` already sorts ascending by
`BASE_PRICE` over the products the shed holds, so the shipped rule IS the optimum, and replacing it
with a solver could only cost runtime.

`test_the_greedy_release_is_the_exact_optimum` brute-forces the optimum over random sheds and
confirms it. It exists so that a future session reading task #46 does not build the solver: the
reason not to is measured here, not asserted.

What was genuinely missing was not the ALGORITHM but a PARTICIPANT. Three rules spent those hundred
slots without seeing each other -- the feed reserve, the sell rule (`allow`/`rate`) and the
router's collection -- and the feed reserve was the one that never read the shed at all. That is
what `feed_hold()` fixes, and `test_the_feed_hold_never_asks_for_slots_the_night_cannot_spare`
below pins its contract.
"""

import itertools
import random

import pytest

import sys

sys.path.insert(0, ".")

from kagg.search import schedule_agent as SA


def _greedy_release(shed, room_needed):
    """What the shipped rule actually releases, in units, per product."""
    out, left = {}, room_needed
    for p in SA.release_order(shed):
        if left <= 0:
            break
        take = min(int(shed.get(p, 0)), left)
        if take:
            out[p] = take
        left -= take
    return out


def _value(sel):
    return sum(SA.RT.BASE_PRICE.get(p, 0) * n for p, n in sel.items())


def _exact_min_value_release(shed, room_needed):
    """Brute force: the cheapest set of `room_needed` units that can be freed from this shed."""
    prods = [p for p in SA.SELLABLE if int(shed.get(p, 0)) > 0]
    best = None
    for counts in itertools.product(*[range(int(shed[p]) + 1) for p in prods]):
        if sum(counts) < room_needed:
            continue
        sel = {p: n for p, n in zip(prods, counts) if n}
        v = _value(sel)
        if best is None or v < best:
            best = v
    return best


@pytest.mark.parametrize("trial", range(60))
def test_the_greedy_release_is_the_exact_optimum(trial):
    """A unit-size knapsack is a sort. Nothing a solver could find is cheaper than `release_order`."""
    rng = random.Random(9000 + trial)
    shed = {p: rng.randint(0, 6) for p in SA.SELLABLE if rng.random() < 0.8}
    shed = {p: n for p, n in shed.items() if n}
    total = sum(shed.values())
    if total == 0:
        pytest.skip("empty shed frees nothing")
    room_needed = rng.randint(1, total)

    greedy = _greedy_release(shed, room_needed)
    assert sum(greedy.values()) == room_needed, (
        f"the greedy freed {sum(greedy.values())} of the {room_needed} slots asked for, from a shed "
        f"holding {total}: {shed}")
    exact = _exact_min_value_release(shed, room_needed)
    assert _value(greedy) == exact, (
        f"an exact search released ${exact} of stock where `release_order` released "
        f"${_value(greedy)} -- shed {shed}, room_needed {room_needed}, greedy {greedy}. If this "
        "ever fires, the unit-size assumption behind task #46's 'it is only a sort' finding has "
        "been broken by a rule change, and the knapsack is worth building after all.")


def test_the_feed_hold_never_asks_for_slots_the_night_cannot_spare():
    """The reserve is a participant in the hundred-slot budget, not a rule that ignores it."""
    day, alive = 20, 19
    want = SA.feed_days(day) * alive
    assert want == SA.FEED_DAYS_LATE * alive, "the first term is still the constant it replaces"

    # An empty shed and empty hands: nothing is competing, so the hold is the full buffer.
    assert SA.feed_hold(day, alive, {}, [{}]) == want

    # A shed already carrying 70 units of OTHER product, plus 20 units coming home in hands, leaves
    # ten slots. Asking for 76 of them is what destroys the harvest at the rollover.
    hold = SA.feed_hold(day, alive, {"MILK": 70, "WHEAT": 40}, [{"STRAWBERRY": 20}])
    assert hold == SA.FEED_DAYS_FLOOR * alive, (
        f"hold {hold}: with 90 slots already spoken for, the herd's floor of "
        f"{SA.FEED_DAYS_FLOOR * alive} is all that may be held")

    # The floor is a floor. Even when the night has no room at all, one meal a head stands: an
    # escape is irreversible and a binned melon is not.
    assert SA.feed_hold(day, alive, {"MILK": 100}, [{"STRAWBERRY": 40}]) == SA.FEED_DAYS_FLOOR * alive

    # Wheat already in a hand is not "other" -- it is the reserve arriving, and counting it against
    # itself would shrink the hold every time a hand picked feed up.
    assert (SA.feed_hold(day, alive, {"MILK": 50}, [{"WHEAT": 30}])
            == SA.feed_hold(day, alive, {"MILK": 50}, [{}]))
