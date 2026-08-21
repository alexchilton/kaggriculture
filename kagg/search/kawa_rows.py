"""Kawashigi's season as a schedule: library rows at the ends, the planner's own count in the middle.

The shipped agent plays ONE recorded season's target rows for all 30 days (`kagg/plan.py`). This
builds a schedule from the whole 213-season library instead, and hands the middle back to the
planner.

    d0-d13     the MODAL library row for that day, under the executor's own label
    d14-d27    the modal row with its planting replaced by "wheat, as much as you can reach"
    d28-d29    the MODAL library row
    all days   the species in `animals_bought` is re-labelled at PLAY time by
               `schedule_agent._herd_split`, from the live shop draw. Nothing here decides it.

## Why the middle is not a row

Measured 2026-08-21, 2,982 day-rows over 213 seasons
(`docs/the_middle_is_not_board_capacity_2026-08-21.md`): his mid-season wheat count is **not** board
capacity. He ends 85.7% of d14-d27 days with empty, unlocked, affordable ground -- a mean of 6.18
tiles at the day's own minimum -- and no board-side quantity predicts the count above r=0.6:

    corr(wheat, free tiles at dawn)     0.274
    corr(wheat, free tiles at any hour) 0.507
    corr(wheat, tiles freed today)      0.598
    within-season SD 3.57 vs between-season SD 0.71   -- not a per-season constant either

What binds is his TURN budget: 1.8% idle, 43.4% of days with no idle turn at all, 53.6% of the
budget spent walking and 31.9% of the work on WATER. That is a property of his ROUTING, not of the
board, so it cannot be read off a dawn observation and it cannot be copied as a number. **Our
router has its own budget, so it must set its own count.**

Which is why `MID_SEASON` rows ask for a whole board of wheat. Under `router=True`,
`schedule_agent._router_acts` sites one PLANT pin per entry in `row["plants"]`, on ground the board
says is empty at dawn, and `want_seed` is then the remaining pins. So a row longer than the board
can never bind: the empty-tile count and the tour bind first, which is exactly the intent. A row of
the length he actually planted would be copying a number the measurement says is his routing's, not
his plan's.

`seeds` is dropped on those days for the same reason. `schedule_agent.py:5200` treats a row's seed
order as a FLOOR under the emission, so any figure here can only buy seed the pins do not justify.
With no row order the buy follows the pins exactly.

## Why the crop is still pinned

The crop half of the finding held: `planted == wheat` exactly on d14-d20 and d27 across all 213
seasons, with 1-2 CARROT on d21-d26 and nothing else. No melon, no tomato, no strawberry anywhere in
his middle. The carrot trigger is unknown and is NOT reproduced here.
"""

import collections
import hashlib
import json
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent.parent

#: 6,840 day-rows over 213 distinct game-seats, written by `scripts/extract_target_rows.py`.
#: `data/` is gitignored, exactly as `kagg/plan.py`'s `SHIPPED_PLAN` is.
LIBRARY = REPO / "data/target_rows_kawa_norm.json"

#: `boardSize` 10, so a farm can never hold more than this many tiles. A `plants` row at least this
#: long cannot be the binding constraint on the day's planting, whatever the board looks like --
#: which is the point. It is a board fact, not a tuned figure: any value at or above it behaves
#: identically.
BOARD_TILES = 100

#: **The first day the planner is allowed to choose the planting.** Everything before it is strict
#: row matching, and the wheat fill must not reach it -- not as a fallback, not as a top-up, not to
#: use spare turns.
#:
#: Alex, 2026-08-21: "the greedy wheat planting should only be in the days 13 plus or whenever it is
#: seen... till d12 it should just be tape matching".
#:
#: The day itself is ambiguous and was measured rather than chosen. His pure-wheat run starts at
#: **d14** -- d13 is still mixed STRAWBERRY+WHEAT and carries 58 distinct rows under the executor
#: label -- so d13 can be argued into either phase. `scripts/where_does_the_middle_start.py` runs
#: both and the result is in `docs/`. Change this number only against a fresh run of that script.
MID_SEASON_FROM = 14

#: The season's last day, and the two closing days that come back from the library. `LAST_DAY` in
#: `schedule_agent` is 29.
CLOSE_DAYS = (28, 29)
SEASON_DAYS = 30


def mid_season(mid_from=None):
    """The days the planner plants, given a boundary. Never includes the two closing days."""
    start = MID_SEASON_FROM if mid_from is None else int(mid_from)
    return tuple(d for d in range(start, SEASON_DAYS) if d not in CLOSE_DAYS)


def library_days(mid_from=None):
    """The days played strictly from the library."""
    mid = set(mid_season(mid_from))
    return tuple(d for d in range(SEASON_DAYS) if d not in mid)

#: The ten keys `schedule_agent` reads off a row. `grep -o 'row.get("[a-z_]*"'` on that file.
#: It never reads `builds`, `feeds`, `cares`, `harvests`, `fertilises` or `clears` -- the router
#: re-derives all six from the live board -- so hashing them would split one plan into several rows
#: for a difference that cannot reach the game.
READS = ("seeds", "hands", "buys", "sells", "land", "plants", "shed_dusk",
         "places", "hires", "animals_bought")

#: **From this day on, `sells` and `buys` are EXECUTION, not intent, so the CHOICE of row is made
#: blind to them.** The row still carries its own orders and the executor still plays them; only the
#: label stops splitting on them.
#:
#: Alex, 2026-08-21, recorded at the foot of `scripts/executor_label.py`: "the sell is only
#: problematic in the first d0-d12 to manage to get the land and items - after that we found sell at
#: h16 is better - so you can discount that and buying cadence is pretty irrelevant also after the
#: land buy".
#:
#: Measured here on the same 228 rows per day. Modal share of the day, under three labels:
#:
#:      day    all ten keys    minus sells    minus sells and buys
#:      d22            1%             1%                      2%
#:      d27            1%             1%                      1%
#:      d28            1%            13%                     27%
#:      d29            1%            98%                     98%
#:
#: d29 is the whole case in one row: 224 of 228 seasons play the SAME closing day, and hashing the
#: sell quota reported 212 distinct plans for it. The doc this work implements records the same
#: thing from the other side -- d29 has 211 distinct `sells` dicts while every other field on that
#: day holds one value across all 228.
#:
#: It does NOT rescue the middle. d22-d27 stay at 1-2% under every label, which is what the
#: capacity measurement predicts: those days differ in a wheat COUNT that the middle no longer
#: copies anyway.
SELLS_ARE_EXECUTION_FROM_DAY = 13

#: COW and SHEEP both build a PASTURE and which one pays is decided by the shop draw, so
#: `schedule_agent._herd_split` substitutes the species at play time. Hashing it here would split
#: one plan into several for a difference the executor is going to overwrite anyway.
#:
#: Mirrors `scripts/extract_target_rows.normalise_herd`. Duplicated deliberately: that file lives in
#: `scripts/`, and a module the submission bundles must not import from there.
ANIMAL_TOKEN = "ANIMAL"
ANIMAL_NAMES = frozenset(("GOOSE", "COW", "SHEEP"))


def only_animals_get_placed(row):
    """A copy of `row` whose `places` names animals and nothing else.

    **`PLACE` is two different ops and the extractor recorded them as one.** The reference's PLACE
    branch puts an animal on a matching empty structure, and otherwise falls back to dropping the
    named item into the shed. Kawashigi uses the second form constantly, and
    `scripts/extract_target_rows.py` appends `u[1]` verbatim, so the library's `places` lists are
    mostly PRODUCTS:

        STRAWBERRY 2794   WOOL 2218   COW 1936   MELON 1653   SHEEP 1496
        FERTILIZER 1204   MILK 1039

    `schedule_agent._outstanding_places` reads every entry as `R.ANIMALS[a]["first_yield_day"]`, so
    one product in that list kills the day on its first turn -- `KeyError: 'FERTILIZER'` at
    `schedule_agent.py:3862`, which is how this was found. It is not a cosmetic filter.

    A shed drop is work the router re-derives from the live board at each stop. It was never part of
    the plan, and leaving it in also split the label on drop cadence, which is execution.
    """
    out = dict(row)
    out["places"] = [p for p in (row.get("places") or []) if p in ANIMAL_NAMES]
    return out


def normalise_herd(row):
    """A copy of `row` with the species blanked, keeping the COUNTS, which do matter."""
    out = only_animals_get_placed(row)
    out["places"] = sorted(ANIMAL_TOKEN for _ in out["places"])
    bought = row.get("animals_bought") or {}
    out["animals_bought"] = ({ANIMAL_TOKEN: sum(int(v or 0) for v in bought.values())}
                             if bought else {})
    return out


def label(row, day=0):
    """A row's identity, as coarsely as the executor can actually act on it.

    `day` matters only through `SELLS_ARE_EXECUTION_FROM_DAY`; see its docstring for the numbers.
    """
    r = normalise_herd(row)
    keys = set(READS)
    if int(day) >= SELLS_ARE_EXECUTION_FROM_DAY:
        keys -= {"sells", "buys"}
    r = {k: v for k, v in r.items() if k in keys}
    return hashlib.md5(json.dumps(r, sort_keys=True).encode()).hexdigest()[:10]


def modal_row(rows, day=0):
    """The row of the largest label class, and its share of `rows`.

    Modal by LABEL, not by row: two seasons differing only in a field the executor never reads are
    the same plan, and counting them apart can hand the mode to a minority row.

    Ties break on the label that sorts first, so the choice is deterministic across runs -- a schedule
    that changes between two runs of the same command is not measurable, and `Counter.most_common`
    breaks ties on insertion order, which is not a property of the data.
    """
    groups = collections.defaultdict(list)
    for r in rows:
        groups[label(r, day)].append(r)
    best = max(sorted(groups), key=lambda k: len(groups[k]))
    return groups[best][0], len(groups[best]) / len(rows)


def wheat_fill(row):
    """`row` with its planting replaced by a whole board of wheat and its seed order dropped.

    Everything else is left alone. The crew, the market cadence and the herd are not the planting
    decision and the executor has no other source for them.
    """
    out = dict(row)
    out["plants"] = ["WHEAT"] * BOARD_TILES
    out["seeds"] = {}
    return out


def build(path=None, mid_from=None):
    """`{day: row}` for all 30 days, ready for `schedule_agent.make_agent`.

    `mid_from` exists so the boundary can be measured both ways from one command
    (`scripts/where_does_the_middle_start.py`). It is a parameter, not a switch: exactly one value
    ships, and it is `MID_SEASON_FROM`.
    """
    rows = json.loads(pathlib.Path(path or LIBRARY).read_text())
    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[int(r["day"])].append(r["target"])

    mid = set(mid_season(mid_from))
    out = {}
    for day in sorted(by_day):
        row, _share = modal_row(by_day[day], day)
        row = only_animals_get_placed(row)
        out[day] = wheat_fill(row) if day in mid else row
    return out


def coverage(path=None):
    """`{day: (label, share, n)}` -- how much of the library each chosen row speaks for.

    A selector is only worth building where this is low, and the instruction is to measure the
    constant before building one.
    """
    rows = json.loads(pathlib.Path(path or LIBRARY).read_text())
    by_day = collections.defaultdict(list)
    for r in rows:
        by_day[int(r["day"])].append(r["target"])
    out = {}
    for day in sorted(by_day):
        row, share = modal_row(by_day[day], day)
        out[day] = (label(row, day), share, len(by_day[day]))
    return out
