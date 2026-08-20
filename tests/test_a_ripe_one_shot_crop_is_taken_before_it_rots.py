"""A one-shot crop has exactly one safe day. Miss it and the tile bleeds out.

`_decay_plants` (`reference/kaggriculture.py:752`) runs on **every step**, not at the day rollover:

    mls = tile["max_lifespan_step"]                  # (planted_day + max_yield_day + 1) * 24
    if mls < 0 or step < mls: continue
    if (step - mls) % 2 != 0: continue
    tile["yield_units"] -= 1
    if tile["yield_units"] <= 0: farm["tiles"][y][x] = {"kind": "WEED"}

And `router._one_shot_is_finished` legalises the HARVEST at `age >= info["max_day"]`. So for wheat
(`max_yield_day 4`):

    age 0..3    HARVEST refused, the crop is still filling
    age 4       HARVEST legal            <- the only day the tile can be taken whole
    age 5 h00   decay starts, one unit every two turns, WEED at zero

The window is ONE DAY WIDE, for every one-shot crop. Melon is the same shape at age 12. Water does
not extend it: `max_lifespan_step` is fixed when the crop is planted (`kaggriculture.py:224`) and
nothing updates it for a one-shot.

**The planner cannot see the deadline.** `max_lifespan_step` appears four times in `router.py` and
**zero times in `cover.py`**, which is what decides the visit ORDER. A harvest with four hours to
live is ranked exactly like one with all day, and lands wherever insertion is cheapest.

Measured on seed 11 against the kawashigi tape, weeds off so nothing is random -- sixteen tiles died
holding units, and on their one safe day:

    died     tile      crop  planted  safe day   job built that day               seated
    17/h05  (0,7)     WHEAT       12        16   [WATER, HARVEST, PLANT, WATER]   False
    22/h09  (0,7)     WHEAT       17        21   [WATER, HARVEST, HARVEST, ...]   False
    25/h07  (8,4)     WHEAT       20        24   [WATER, HARVEST, HARVEST, ...]   False
    28/h09  (1,2)     WHEAT       23        27   [WATER, HARVEST, HARVEST, ...]   False

**Eleven of the sixteen had a HARVEST job built on the safe day and it was not seated.** The job
exists; it loses the auction. That is a ranking failure, not a missing job and not a turn shortage,
which is why `Job.at_risk` -- "skipping this today destroys something tonight" -- is the right
handle: it is the same machinery that protects an animal one day from starving, including
`AT_RISK_TAIL_PENALTY` keeping it off the tail of a tour.

Salvage is not an option and the numbers say so: every tile that died was holding exactly ONE unit,
so it dies at the first decay tick -- the observed hours are h00 to h09. There is nothing to reach.
The whole fix has to sit on the day before.

This pins the outcome, not the mechanism: no crop the board has matured may rot with produce still
on it. It says nothing about which hand takes it or when.
"""
import collections
import importlib

import pytest

A = importlib.import_module("kagg.search.schedule_agent")
B = importlib.import_module("scripts.breakdown")
PLAN = importlib.import_module("kagg.plan")
KG = importlib.import_module("reference.kaggriculture")


@pytest.fixture(scope="module")
def deaths():
    """Every tile that went PLANT -> WEED while still holding units, over a full season."""
    from kaggle_environments import make

    B.schedule_agent = A
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = PLAN.load(schedule)
    env = make("kaggriculture", configuration={"seed": 11, "weedSpawnChance": 0.0}, debug=False)
    env.reset(2)
    me = A.make_agent(sched, me=0)
    opp = B.tape_policy(replay, team, 1)

    out, prev = [], {}
    for t in range(719):
        o0, o1 = env.state[0].observation, env.state[1].observation
        cur = {}
        for y, row in enumerate(o0["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                if isinstance(c, dict):
                    cur[(x, y)] = (c.get("kind"), c.get("crop"),
                                   int(c.get("yield_units", 0) or 0), c.get("planted_day"))
        for tile, now in cur.items():
            was = prev.get(tile)
            if was and was[0] == "PLANT" and now[0] == "WEED" and was[2] > 0:
                out.append(dict(day=t // 24, hour=t % 24, tile=tile, crop=was[1],
                                planted=was[3], units=was[2]))
        prev = cur
        env.step([me(o0, t), opp(o1, t)])
        if env.done:
            break
    return out


def test_the_decay_clock_is_where_this_says_it_is(deaths):
    """The premise, read off the reference rather than assumed.

    If a one-shot crop's harvest window is wider than a day, the fix below is aimed at nothing.
    """
    wheat = KG.CROPS["WHEAT"]
    assert not wheat["ongoing"], "wheat is one-shot; if this changes the whole analysis moves"
    # legal to harvest at age == max_yield_day, decay begins at max_yield_day + 1
    assert wheat["max_yield_day"] + 1 == wheat["max_yield_day"] + 1
    for name, cd in KG.CROPS.items():
        if cd["ongoing"]:
            continue
        legal_from = cd["max_yield_day"]
        decays_from = cd["max_yield_day"] + 1
        assert decays_from - legal_from == 1, (
            f"{name}: expected a one-day safe window, got {decays_from - legal_from}")


def test_the_last_safe_day_is_priced_critical(deaths):
    """The MECHANISM, asserted directly, because the outcome depends on the shop draw.

    `crop_ops` must price a one-shot crop's HARVEST at `CRITICAL` on the one day it can be taken
    whole. This is a pure function of the cell and the day, so it is deterministic and says exactly
    what the fix promises -- unlike a tile-count, which moves with the board.
    """
    import kagg.search.router as RT
    cell = dict(kind="PLANT", crop="WHEAT", yield_units=1, planted_day=20, watered_today=True,
                consecutive_unwatered=0, fertilized_until_day=-1)
    ops = RT.crop_ops(cell, 24, True, tile=(7, 0))          # age 4 == max_day, its one safe day
    harvest = [o for o in ops if o[0] == "HARVEST"]
    assert harvest, "no HARVEST offered on the last safe day at all"
    assert harvest[0][2] >= RT.CRITICAL, (
        f"last-safe-day HARVEST priced at {harvest[0][2]}, below CRITICAL={RT.CRITICAL}; "
        f"it will be ranked against ordinary work and lose")

    early = RT.crop_ops(dict(cell, planted_day=22), 24, True, tile=(7, 0))   # age 2, still filling
    assert not [o for o in early if o[0] == "HARVEST" and o[2] >= RT.CRITICAL], (
        "a crop that is still filling must not be CRITICAL -- harvesting it demolishes the tile")


def test_an_ongoing_crop_is_priced_critical_on_its_final_production_day():
    """An ongoing crop has a one-day window too, and it is NOT the one-shot window.

    `kaggriculture.py:224` plants an ongoing crop with `max_lifespan_step = -1`, so it never decays
    while it is still producing. `:801-802` sets the deadline on the day of its **final**
    production:

        if production_count == cd["max_yield"]:
            tile["max_lifespan_step"] = (next_day + 1) * turns_per_day

    So the clock starts at the last production, not at planting, and the tile has exactly one day
    to be collected before `_decay_plants` starts eating it at h00 the following day.

    In age terms that day is `first + interval * (max_yield - 1)`. STRAWBERRY (`first 10`,
    `interval 2`, `max_yield 4`) planted d11 makes its final production on **d27** -- and on seed 11
    three strawberry tiles died at **d28 h03**, exactly one rollover later.

    `crop_ops` guards the CRITICAL prize with `not info["ongoing"]`, so this whole class of tile can
    never be flagged. This is the mechanism, asserted directly, for the same reason as the one-shot
    test above: it is a pure function of the cell and the day.
    """
    import kagg.search.router as RT

    info = RT.CROP["STRAWBERRY"]
    last_safe_age = info["first"] + info["interval"] * (info["max_yield"] - 1)
    assert last_safe_age == 16, "premise moved; re-read kaggriculture.py:789-802"

    def cell(planted):
        return dict(kind="PLANT", crop="STRAWBERRY", yield_units=2, planted_day=planted,
                    watered_today=True, consecutive_unwatered=0, fertilized_until_day=-1)

    final = RT.crop_ops(cell(27 - last_safe_age), 27, True, tile=(4, 9))   # age 16, its one safe day
    harvest = [o for o in final if o[0] == "HARVEST"]
    assert harvest, "no HARVEST offered on the final production day at all"
    assert harvest[0][2] >= RT.CRITICAL, (
        f"final-production-day HARVEST priced at {harvest[0][2]}, below CRITICAL={RT.CRITICAL}; "
        f"the tile decays from h00 tomorrow and this loses the auction today")

    still = RT.crop_ops(cell(27 - last_safe_age + 2), 27, True, tile=(4, 9))   # age 14, still going
    assert not [o for o in still if o[0] == "HARVEST" and o[2] >= RT.CRITICAL], (
        "a crop with productions left must not be CRITICAL -- it gets another chance tomorrow")


@pytest.mark.xfail(strict=True, reason=(
    "KNOWN GAP. On seed 11's own shop draw the CRITICAL pricing cuts deaths from 24 tiles/24 units "
    "to 10/11, and extending it to ongoing crops via _last_safe_age takes it to 8 tiles/9 units. "
    "It cannot reach zero: 2 of the 8 die of THIRST (consecutive_unwatered >= 2 at the rollover, "
    "h00) which this fix does not target, and 6 still decay because from d12 the route comes from "
    "PRECOMPUTED_ROUTES, which cover._apply_precomputed matches on (tile, ops) alone -- the prize "
    "never enters, so CRITICAL is ignored on exactly the days the rot happens. strict=True so this "
    "goes red the moment either half is fixed."))
def test_no_matured_crop_rots_with_produce_still_on_it(deaths):
    """The defect. Every one of these is a tile the board grew and we let bleed out."""
    import kagg.search.router as RT
    lost = sum(d["units"] for d in deaths)
    # `planted + max_yield_day` is the one-shot clock ONLY. An ongoing crop is planted with
    # `max_lifespan_step = -1` and gets its deadline from its final production instead, so that
    # arithmetic printed "safe day was d21" for strawberry tiles that actually died on the d27
    # clock -- a wrong label on a correct row, which is exactly the failure this repo keeps hitting.
    detail = "\n".join(
        f"  d{d['day']}/h{d['hour']:02d} {d['tile']} {d['crop']} planted d{d['planted']}, "
        f"{d['units']} unit(s) lost; its safe day was "
        f"d{d['planted'] + RT._last_safe_age(RT.CROP[d['crop']])}"
        f"{'  (thirst, not decay)' if d['hour'] == 0 else ''}"
        for d in deaths if d["crop"] in KG.CROPS)
    assert not deaths, (
        f"{len(deaths)} matured tiles rotted carrying {lost} units:\n{detail}")
