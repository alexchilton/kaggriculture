"""Two sheep and two cows in the schedule become GEESE, in place, early.

`SHOP_ADAPT_HERD` already re-decides the cow/sheep split from the shop draw, and it works -- across
eleven downloaded ladder games it ran SHEEP 8 on a board draining 716 wool and SHEEP 4 on the boards
draining none.
But it never gets to decide the ones that matter, for two reasons that compound:

1. It starts at `SHOP_ADAPT_FROM_DAY = 6`.
2. `split` is anchored on `state["bought"]`, which never decreases -- deliberately, so the total
   cannot overshoot the schedule's count.

The reference schedule buys `SHEEP 4` on **day 0**, when `town["unlocked_shops"]` is still empty
(`kaggriculture.py:176`; the first unlock is day 3, one every three days to a maximum of eight).
So four of the five sheep are a blind bet placed before any evidence exists, and by day 6
`bought["SHEEP"]` is already 4, which is why `HERD_FLOOR_SHEEP = 1` can never bind and why the
ladder games read `SHEEP 4` on all six boards where wool was drained ZERO.

WOOL is carried by `YARN_STORE` alone -- one shop of eight -- the least-supported product in the
game bar MELON, which no shop carries at all:

    WHEAT 5/8   STRAWBERRY 4/8   MILK 3/8   EGG 2/8   TOMATO 2/8   CARROT 2/8   WOOL 1/8   MELON 0/8

Measured over one season by `tests/test_production.py:probe_animal`, per animal:

    GOOSE   $300  ->  26 units of EGG    (2 shops of 8, drained in 10 of our 11 games)
    COW     $400  ->  11 units of MILK   (3 shops of 8, drained in 11 of 11)
    SHEEP   $500  ->   8 units of WOOL   (1 shop of 8,  drained in  4 of 11)

A goose is the cheapest animal, out-produces a sheep 3.25x, has twice the chance of a buyer
existing, and yields from day 4 against a sheep's day 6. Under ignorance -- which day 0 is, exactly
-- it dominates a sheep on every axis at once, so no board reading is needed to prefer it.

**The swap is in place: the per-day animal COUNT never changes.** The pen build schedule is paced to
that count, and `BUILD_COOP`/`BUILD_PASTURE` are the same operation on an empty tile (one turn, no
money, `kaggriculture.py:480,486`), so the geometry is untouched and only the op name differs.
Geese come from the EARLIEST cow rows because a goose yields from day 4 at `interval 1`, so each
day of delay costs it a unit outright.
"""
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from kagg.search import schedule_agent_1455mh as SA

RAW = {int(k): v for k, v in
       json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text()).items()}
ANIMALS = ("GOOSE", "COW", "SHEEP")


def _counts(sched):
    """`day -> Counter(species)` for the days that buy anything."""
    return {d: collections.Counter({a: int(q) for a, q in
                                    (sched[d].get("animals_bought") or {}).items()})
            for d in sorted(sched)}


def _season(sched):
    total = collections.Counter()
    for c in _counts(sched).values():
        total.update(c)
    return total


def test_the_premise_the_schedule_commits_to_wool_before_a_single_shop_is_known():
    """Guards the fixture. If the reference schedule stops buying sheep on d0, this file is stale."""
    assert _counts(RAW)[0]["SHEEP"] >= 2, (
        f"the reference schedule no longer buys sheep on day 0 ({dict(_counts(RAW)[0])}); the "
        f"defect this file was written for is gone and the file must be re-derived.")
    assert SA.SHOP_ADAPT_FROM_DAY > 0, (
        "the herd adapter now runs from day 0, so nothing is bought blind and this file is stale.")


def test_geese_come_out_of_the_dominated_animal_first():
    """SHEEP leads the cycle because it is the animal a goose beats on every axis at once."""
    before, after = _season(RAW), _season(SA.swap_in_geese(RAW, 1))
    assert after["GOOSE"] == 1 and after["SHEEP"] == before["SHEEP"] - 1, (
        f"one goose gave {dict(after)} from {dict(before)}; the first goose should cost a SHEEP, "
        f"which is $500 for 8 units of a product with a buyer in 4 of our 11 games.")
    assert after["COW"] == before["COW"], f"the first goose took a COW: {dict(after)}"


def test_the_goose_count_is_capped_by_the_zero_walk_cells_we_actually_own():
    """Asking for more geese than there are ranch cells must not buy one onto ordinary ground.

    Only `(4,4)` is owned at the start; `(5,4)` needs the $1,000 NE parcel, `(4,5)` $3,000 and
    `(5,5)` $7,000. A GOOSE is `interval 1` -- it produces, and therefore wants servicing, every
    night -- so an off-cell goose pays a walk nightly. Measured with four taken from the earliest
    rows: `feed 4/12` by d8, two birds escaped, weeds 2 -> 8, d16 money halved.
    """
    counts = {n: _season(SA.swap_in_geese(RAW, n))["GOOSE"] for n in (3, 4, 5, 8)}
    assert counts[4] == counts[3], (
        f"asking for 4 geese bought {counts[4]} where 3 bought {counts[3]}. The fourth has no "
        f"zero-walk cell -- that is $7,000 of land -- so it must not be bought at all.")
    assert counts[8] == counts[3], f"the cap does not hold at 8: {counts}"
    assert counts[3] <= len(SA.HERD_GEESE_EARLIEST), f"more geese than cells: {counts}"


def test_the_per_day_animal_count_is_untouched():
    """The pen build schedule is paced to this. Change it and animals strand or pens sit empty."""
    before, after = _counts(RAW), _counts(SA.swap_in_geese(RAW))
    for day in sorted(before):
        assert sum(after[day].values()) == sum(before[day].values()), (
            f"day {day}: {dict(before[day])} became {dict(after[day])}, changing that day's animal "
            f"count from {sum(before[day].values())} to {sum(after[day].values())}.")


def test_no_goose_is_bought_before_its_zero_walk_cell_exists():
    """The geometry constraint, stated as a schedule constraint.

    Earlier is better for a goose in isolation -- it yields from day 4 at `interval 1`, so a day of
    delay costs a unit outright. But a goose without a ranch cell is serviced by a walk every night,
    and the cells arrive on the land schedule, not on demand. This pins the second consideration
    beating the first, which is the whole content of the change.
    """
    bought = _counts(SA.swap_in_geese(RAW, len(SA.HERD_GEESE_EARLIEST)))
    days = sorted(d for d, c in bought.items() if c["GOOSE"] for _ in range(c["GOOSE"]))
    assert days, "no geese were bought at all; the swap is disabled and this file measures nothing."
    for k, day in enumerate(days):
        assert day >= SA.HERD_GEESE_EARLIEST[k], (
            f"goose {k} is bought on day {day}, before its cell exists on day "
            f"{SA.HERD_GEESE_EARLIEST[k]} -- so it is placed on ordinary ground and walked to every "
            f"night. Geese bought on days {days} against cells {list(SA.HERD_GEESE_EARLIEST)}.")
    assert days[0] == 0, (
        f"the first goose is bought on day {days[0]}, but `(4,4)` is owned from day 0 and the bird "
        f"yields from day 4 -- every day of delay past its cell is a unit lost.")


def test_the_purchase_row_and_the_pen_row_agree_at_every_count():
    """`places` is a SECOND statement of the species and the pen planner reads THAT one.

    `schedule_agent._pens` builds `wanted` from `sched[d]["places"]` and pins `("BUILD", a, ...)`
    from it, so a swap that moves `animals_bought` alone buys a goose and builds it a PASTURE.
    `PLACE` is a silent no-op on the wrong structure -- nothing raises, the bird sits in the shed all
    season, and the pen tile is wasted too. Measured the first time this was got wrong: five pastures
    and zero coops on day 0, `place 2/5`, `feed 2/5` for a week, season idle 595 -> 1067.
    """
    for n in (0, 1, 2, 3, 4, 5, 6):
        sched = SA.swap_in_geese(RAW, n)
        bought = collections.Counter()
        placed = collections.Counter()
        for d in sched:
            bought.update({a: int(q) for a, q in (sched[d].get("animals_bought") or {}).items()})
            placed.update(sched[d].get("places") or [])
        assert bought == placed, (
            f"HERD_GEESE={n}: the schedule buys {dict(bought)} but plans pens for {dict(placed)}. "
            f"Every animal in the mismatch is bought and stranded, or has a pen built for nothing.")


def test_the_reference_schedule_is_not_mutated():
    """It is Victor's recording. The swap must return a new plan, never edit the tape in place."""
    before = _season(RAW)
    SA.swap_in_geese(RAW)
    assert _season(RAW) == before, (
        f"`swap_in_geese` mutated the schedule it was handed: {dict(_season(RAW))} != "
        f"{dict(before)}. Every later reader of that dict now sees the swap too.")
