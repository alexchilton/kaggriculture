"""Every market order at the turn the tape placed it, not just on the day it placed it.

The schedule used to aggregate the book to a day total, and the emitter re-invented the lots: six equal
buys on turns 2, 5, 8... and six equal sells on 0, 3, 6... That loses the only thing the market cares
about.

`market_price` quotes a BUY_PRODUCT at **post-buy inventory** (`kaggriculture.py:575`, "so a buy/sell
round-trip against an unchanged market nets zero"), so a SELL and a BUY of the same product **in the
same turn** cost about nothing. The tape does this constantly -- day 0 hour 5 is `BUY WHEAT 1 +
SELL WHEAT 1 -> +$0`, hour 14 is `BUY 3 + SELL 1 -> +$0` -- moving wheat from the town into the shed for
free, all season, to feed a herd of 14.

Measured on identical daily totals (`scripts/diff_realised_sales.py`):

    day 2  tape   BUY WHEAT in lots of 4, 9, 2, 1, 1, 1, interleaved with its sells   net  +$76
    day 2  ours   BUY WHEAT in six equal lots of 3, sells on the turns between        net   -$89

That $165 on day 2 is the origin of the whole cash divergence: day 3 opens $45 against $217 and never
recovers, and a short bank is what silently kills `BUY_ANIMAL` -- which is why 11 pens stand with 5
animals in them and the herd never reaches 14.

It is the same defect as the lost parcel, one layer out. `BUY_LAND` was emitted on the right day at the
wrong hour and vanished; so is everything else. The hour was in the tape the whole time and the
extractor was throwing it away.

**HIRE is deliberately excluded.** Its cost is the Fibonacci partial sum over the day, independent of
which turn each order sits in, so nothing is lost by keeping our own two-per-turn cadence -- and that
cadence is load-bearing: `_spawn_hand` picks by occupancy at settle time, so three orders in one turn
put a hand on the trapped `(5,5)` corner and dead reckoning stops working.
"""


import pytest

#: **Disabled 2026-08-07: this whole file asserts against the OLD LEADER's tape (`new_leader`).**
#:
#: Kept, not deleted, because it is the record of a specific and expensive mistake. The agent is now
#: matched against Seb's tape (`top_guys/90494364`), and the two tapes play differently -- the case
#: that forced this was watering. `router.py` had been made to water every tile every day on the
#: strength of a table showing "the tape" watering ~1.06 per live tile daily, 18 times on day 1
#: against our 1. That table was measured here, on the old leader, and then applied to Seb:
#:
#:     oldleader  d0 16/17  d1 17/18  d2 18/19  d3 18/19   waters daily
#:     seb        d0 17/17  d1 17/0   d2 17/17  d3 17/14   waters alternate days
#:
#: Seb takes zero weeds through day 7 on the alternate-day cadence, and the every-day rule was
#: costing 17 work turns and ~31 walk turns on day 1 alone for nothing.
#:
#: So these assertions are not wrong about the old leader; they are answers to a question we stopped
#: asking. Left red, they read as regressions and pull work towards the wrong target. Re-enable only
#: by first deciding which tape the number is supposed to describe.
_OLD_LEADER_SKIP = pytest.mark.skip(
    reason="asserts against the OLD LEADER's tape; the agent now targets Seb's -- see banner")

pytestmark = _OLD_LEADER_SKIP
import collections
import json
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, "scripts")

from kagg.search import routines as R

SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TPD = R.TURNS_PER_DAY


@pytest.fixture(scope="module")
def emitted():
    if not SCHEDULE.exists():
        pytest.skip(f"{SCHEDULE} missing; run scripts/extract_leader_schedule.py")
    from kagg.search import dayplan

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    if not any(r.get("orders") for r in sched.values()):
        pytest.skip("schedule carries no per-turn book; re-run scripts/extract_leader_schedule.py")
    script, report = dayplan.emit(sched)
    return sched, script


def _ours(script):
    """`(turn, op, item) -> qty` for every market order our tape places, HIRE excluded."""
    got = collections.Counter()
    for arr, op, names in ((script.sell, "SELL", R.PRODUCTS),
                           (script.buy_seed, "BUY_SEED", R.CROPS),
                           (script.buy_product, "BUY_PRODUCT", R.PRODUCTS),
                           (script.buy_animal, "BUY_ANIMAL", R.ANIMAL_NAMES)):
        a = np.asarray(arr)
        for t in range(a.shape[0]):
            for i in range(a.shape[1]):
                if a[t, i]:
                    got[(t, op, names[i])] += int(a[t, i])
    land = np.asarray(script.buy_land)
    for t in range(land.shape[0]):
        if land[t]:
            got[(t, "BUY_LAND", None)] += int(land[t])
    return got


def _tapes(sched):
    want = collections.Counter()
    for day, row in sched.items():
        for hour, op, item, qty in (row.get("orders") or []):
            if op == "HIRE":
                continue
            want[(day * TPD + int(hour), op, item)] += int(qty)
    return want


def test_the_market_book_is_the_tapes_turn_by_turn(emitted):
    """Order for order, at the turn. The day total matching is what we already had, and it was not enough."""
    sched, script = emitted
    want, got = _tapes(sched), _ours(script)
    wrong = []
    for key in sorted(set(want) | set(got), key=lambda k: (k[0], str(k[1]), str(k[2]))):
        if want[key] != got[key]:
            t, op, item = key
            wrong.append(f"turn {t} (day {t // TPD} h{t % TPD}) {op} {item}: "
                         f"ours {got[key]} against the tape's {want[key]}")
    assert not wrong, (f"{len(wrong)} market cells differ:\n  " + "\n  ".join(wrong[:20]))


def test_a_same_turn_round_trip_is_preserved(emitted):
    """The specific structure that makes it free: a SELL and a BUY of one product in the same turn.

    Counted rather than asserted in the abstract -- if the emitter spreads the book back out these go to
    zero, and the $165 a day comes back.
    """
    sched, script = emitted
    sell, buy = np.asarray(script.sell), np.asarray(script.buy_product)
    pairs = sum(1 for t in range(min(len(sell), len(buy)))
                for i in range(sell.shape[1])
                if sell[t, i] and buy[t, i])
    tape_pairs = 0
    for day, row in sched.items():
        by_turn = collections.defaultdict(lambda: [set(), set()])
        for hour, op, item, qty in (row.get("orders") or []):
            if op == "SELL":
                by_turn[hour][0].add(item)
            elif op == "BUY_PRODUCT":
                by_turn[hour][1].add(item)
        tape_pairs += sum(len(s & b) for s, b in by_turn.values())
    assert pairs >= tape_pairs, (
        f"{pairs} same-turn sell/buy round trips against the tape's {tape_pairs}; "
        "each one lost pays the spread instead of netting zero")
