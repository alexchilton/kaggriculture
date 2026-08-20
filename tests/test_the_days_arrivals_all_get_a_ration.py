"""A day that places five animals must reserve five rations, not three.

**The theory, stated before the fix.** On tetsuya's d0 the row is
`places ['SHEEP','SHEEP','SHEEP','COW','COW']` with `feeds 5`, and he feeds all five. We feed ONE.
Measured against his own recorded ops on his board and seed (`data/logs/vs_tets_d0d10_2026-08-20.log`):

    day   FEED ours/his     CARE ours/his
      0        1/5              1/5
      4        5/8              5/8
      5        7/8              7/8
      7        8/9              8/9
      1,2,6    exact            exact

The shortfall lands only on days animals ARRIVE, and d1/d2/d6 -- where nothing is placed -- are
exact. So this is about arrivals, not about the standing herd.

**Two candidate causes were measured and are NOT it**, recorded here so they are not re-derived:

  - `will_be_fed`'s skip-the-young rule. It is unreachable: an unconditional `return True` sits in
    front of it. It already feeds every standing pen.
  - the market slot gate. Opening the tenth slot left d0 `feed 1/5` byte-for-byte and made idle
    worse, PASS 911 -> 959. Reverted.

**What is left, and what this file asserts.** The dawn ration is sized off `arriving`, which filters
the row's placements through `ARRIVAL_FEED_EARLIEST_YIELD` -- only the earliest-yielding species
still owed is admitted. On a row of three SHEEP (`first_yield_day` 6) and two COWs (8), the sheep
set the earliest at 6, so both cows fail `8 <= 6` and the day reserves three rations for five
animals.

That filter exists for a real reason -- a scarce ration should reach the animal that produces
soonest first, which was worth a unit of wool a day on the kawashigi tape. It is a PRIORITY rule
being used as an EXCLUSION rule: when the budget covers every arrival, nobody should be excluded.
"""
import pytest

from kagg.search import router as RT


ROW = ["SHEEP", "SHEEP", "SHEEP", "COW", "COW"]


def _cell(animal, day=0):
    """A pen holding `animal`, placed today."""
    return {"animal": animal, "consecutive_unfed": 0, "placed_day": day, "fed_today": False}


@pytest.fixture(autouse=True)
def _restore():
    """These are module globals the agent sets once per turn; put them back."""
    before = (RT.ARRIVAL_FEED_REMAINING, RT.ARRIVAL_FEED_EARLIEST_YIELD, RT.ARRIVAL_FEED_OWED)
    RT.ARRIVAL_FEED_OWED = 0          # "unknown"; the scarcity cases below rely on this default
    yield
    (RT.ARRIVAL_FEED_REMAINING, RT.ARRIVAL_FEED_EARLIEST_YIELD,
     RT.ARRIVAL_FEED_OWED) = before


def _earliest(row):
    """`ARRIVAL_FEED_EARLIEST_YIELD` as the agent computes it: the soonest first yield still owed."""
    return min(RT.ANIMALS[a]["first_yield_day"] for a in row)


def test_the_soonest_producer_is_served_first_when_the_ration_is_short():
    """**The rule this file must not break.** With one ration and a mixed row, the sheep gets it.

    A SHEEP reaches its first production night at d5->d6 with only six nights to bank the five
    bonuses it can use; a COW reaches its at d7->d8 with eight nights for the same five, so it caps
    regardless. Giving the single ration to the cow is the waste this filter was written to stop.
    """
    RT.ARRIVAL_FEED_REMAINING = 1
    RT.ARRIVAL_FEED_EARLIEST_YIELD = _earliest(ROW)
    assert RT.will_be_fed(_cell("SHEEP"), 0), "the soonest producer must take a scarce ration"
    assert not RT.will_be_fed(_cell("COW"), 0), (
        "a COW must not take the last ration ahead of a SHEEP that produces two days sooner")


def test_every_arrival_is_fed_when_the_row_pays_for_every_arrival():
    """**The defect.** Five placements, five feeds in the row, and the cows are still refused.

    `ARRIVAL_FEED_EARLIEST_YIELD` is a PRIORITY: serve the soonest producer first. It is being used
    as an EXCLUSION: never serve anything else. Those are the same rule only while the ration is
    scarce. Here the budget covers the whole row, so no cow is taking anything from any sheep --
    and refusing it costs the animal-day and the care chain that hangs off it, since CARE is only
    offered on a pen that is already fed.

    RED as written on 2026-08-20.
    """
    RT.ARRIVAL_FEED_REMAINING = len(ROW)
    RT.ARRIVAL_FEED_EARLIEST_YIELD = _earliest(ROW)
    # Five arrivals still want a ration -- the state the agent publishes on d0 at dawn.
    RT.ARRIVAL_FEED_OWED = len(ROW)
    served = [a for a in ROW if RT.will_be_fed(_cell(a), 0)]
    assert len(served) == len(ROW), (
        "the row places %d and pays for %d feeds, but only %s are offered a ration -- the "
        "priority filter is excluding %s"
        % (len(ROW), len(ROW), served, sorted(set(ROW) - set(served))))


def test_a_cow_only_row_is_not_starved_by_its_own_species():
    """The degenerate case the filter must already handle: if only cows arrive, cows are earliest.

    Guards against a fix that hard-codes SHEEP rather than reading the row.
    """
    RT.ARRIVAL_FEED_REMAINING = 2
    RT.ARRIVAL_FEED_EARLIEST_YIELD = _earliest(["COW", "COW"])
    assert RT.will_be_fed(_cell("COW"), 0), "a cow-only row must feed its cows"


def test_a_goose_outranks_both_when_it_arrives_with_them():
    """A GOOSE is `first_yield_day` 4 and `interval` 1 -- it produces EVERY day from d4.

    Feed and care are worth one unit per production day, so a goose is worth three times a sheep and
    twice a cow per day fed. Whatever replaces the exclusion must keep serving it first.
    """
    row = ["GOOSE", "SHEEP", "COW"]
    RT.ARRIVAL_FEED_REMAINING = 1
    RT.ARRIVAL_FEED_EARLIEST_YIELD = _earliest(row)
    assert RT.will_be_fed(_cell("GOOSE"), 0), "the goose produces daily from d4 and must be first"
    assert not RT.will_be_fed(_cell("SHEEP"), 0)
