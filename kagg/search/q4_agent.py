"""FIRST DRAFT of a four-quadrant variant of the shipped agent. Exploratory, not a ship candidate.

The shipped agent (`kagg/search/schedule_agent.py`) plays a THREE-quadrant board: NW from the
start, NE bought at d6 and SW at d11, and that is the whole board for the rest of the season.
Three top players -- Kawashigi, Emon xu, Yura -- run the same opening and then, in a minority of
their games, take the SE parcel at d12 and run a sheep-heavy herd on it.

This module is that branch, and nothing else. Days 0 through 11 are the shipped agent, action for
action; `tests/test_the_fourth_quadrant_branch_leaves_the_opening_alone.py` plays both agents
against one environment and compares every action to prove it.

## How it is built, and why it is not a copy

`schedule_agent` reads its schedule live: the land block walks `sched[d]["land"]` every turn to
find the next parcel due, `want_total` re-accumulates `animals_bought` every turn, and
`_refresh_pins` re-reads `builds` and `places` every turn. Nothing is latched at construction. So
the whole q4 branch is expressible as an edit to ONE ROW of the schedule -- day 12 -- and needs no
change to the agent at all.

`schedule_agent.make_agent` shallow-copies the outer schedule dict (`{int(k): v for k, v in
schedule.items()}`) and SHARES every row object with its caller. That is what makes the edit
reachable mid-game: we hold the day-12 row, the inner agent holds the same object, and mutating it
at d6 is seen by the agent at d12. The module says so itself, in the comment above
`_melon_to_strawberry`, which replaces a row with a copy for exactly this reason.

## Why the d12 row can be armed at d6 without touching the opening

Adding a `land` day is not obviously inert before that day. `_pens_due_before_more_land(sched, day)`
scans days AFTER today for the next parcel and counts the pens due before it, so a new land day at
d12 changes what d11 believes about its own pens: with no land after d11 it counts every remaining
build, and with a parcel at d12 it counts only the builds in between.

The two halves of the arming cancel there. Arming adds `builds: 4` at d12, which would make d11's
count 4 instead of 0; it also adds `land: 1` at d12, which cuts the scan short before those builds
and returns it to 0. Neither edit is safe alone. This is reasoning about someone else's function,
so it is not trusted -- the action-for-action test is what actually holds the property.

## What is deliberately NOT modelled

The field relocates ~8 wheat plantings onto the new quadrant rather than adding crew
(`docs/fable_fourth_quadrant_reopened_2026-08-15.md`: all three 100-tile seats run 277 season
hires, exactly what the 75-tile seats run). This draft does not relocate anything. The extra ground
is offered to the router and the router does what it does with it. That is a known gap and the
first thing to try if the parcel measures flat.

## Process globals

`_routes_go_live_from` mutates `cover.PRECOMPUTED_ROUTES`, which is module state shared by every
agent in the process. The solved routes were solved for a three-quadrant board and are wrong once
SE unlocks, so this is required, not optional -- but it means **one agent per process**, which is
what `scripts/q4_probe.py` enforces anyway for an unrelated and equally hard-won reason.
"""
import collections
import copy
import sys

import reference.kaggriculture as KG

from kagg.search import cover as COVER
from kagg.search import schedule_agent as SA

#: The shop that carries WOOL. Pinned against `reference.kaggriculture.SHOPS` by
#: `test_the_trigger_names_a_shop_the_environment_can_draw`, because a predicate keyed on a
#: misspelled shop never fires and reads exactly like a measured null.
YARN_STORE = "YARN_STORE"

#: The day the trigger is read and latched. Shops unlock every `townShopUnlockInterval` = 3 days
#: (`reference/kaggriculture.py:867,886`), and the draw for day N lands at the END of day N-1, so
#: d6 hour 0 has seen exactly two draws: d3 and d6. "A yarn store by d3-d6" is therefore
#: "YARN_STORE among the first two entries of `unlocked_shops`", and asking on d6 asks it exactly.
Q4_DECISION_DAY = 6

#: How many draws are on the board at `Q4_DECISION_DAY`. Not a tuning knob -- it is
#: `Q4_DECISION_DAY // townShopUnlockInterval`.
Q4_DRAWS_BY_DECISION_DAY = 2

#: The day the parcel is ordered. The schedule's `land` row is a FLOOR, so the agent buys on the
#: first turn of d12 it can pay for; the tapes emit at d12h1.
Q4_BUY_DAY = 12

#: `_do_buy_land` takes `LAND_ORDER[len(unlocked) - 1]` (`reference/kaggriculture.py:712-725`), so
#: owning NW + NE + SW makes the third parcel SE deterministically. Recorded here to be asserted,
#: not to be chosen.
Q4_QUADRANT = "SE"

#: The herd the four-quadrant games run. COW 6 comes from the shipped
#: `WOOL_SHOP_COW_CAP` -- an early yarn store holds cows at six in 24 of 24 recorded games -- and
#: the extra four animals all go to sheep.
#:
#: **This number is contested inside the repo and the conflict is left visible on purpose.**
#: `docs/fable_fourth_quadrant_reopened_2026-08-15.md` measures the 2026-08-14 field and finds
#: "every 100-tile seat carries 18 animals against the 75-tile seats' 14 (the +4 are SHEEP, in SE,
#: from d12)". `schedule_agent.WOOL_SHOP_SETS_THE_HERD` measures 74 Kawashigi seats and finds his
#: four-quadrant herds run 13-16, never 18. Both can be true -- they are different players -- but
#: 18 is the FIELD's number, not the leader's, and if this draft measures flat that is one of the
#: two places to look.
Q4_COW = 6
Q4_SHEEP = 12

#: Animals added to the schedule's own row. The shipped schedule asks for COW 10 / SHEEP 4 = 14;
#: on an early-yarn board `_herd_split` already turns that into COW 6 / SHEEP 8. Four more animals
#: takes the total to 18 and the split spends all four on sheep, giving COW 6 / SHEEP 12.
Q4_EXTRA_SHEEP = (Q4_COW + Q4_SHEEP) - 14

#: The first day whose route is re-solved live. `cover._apply_precomputed` keys a stop on
#: `(tile, ops)` against routes solved for a 75-tile board; on 100 tiles those routes describe a
#: board the game never reaches. Live routing costs real money on its own -- measured at -$11,431
#: on seed 3 in `scripts/swap_one_crop.py` -- which is why `scripts/q4_probe.py` runs the shipped
#: agent WITH live routes as a separate arm. Without that arm the parcel is confounded with the
#: routing handicap and the comparison says nothing.
Q4_LIVE_ROUTES_FROM = 12


def the_town_promised_wool_early(obs, draws=Q4_DRAWS_BY_DECISION_DAY):
    """True when a YARN_STORE is among the shop draws that have landed by `Q4_DECISION_DAY`.

    Read straight off a live observation. The shop list is `observation["town"]["unlocked_shops"]`
    -- NOT `observation["shops"]`, which does not exist -- and it is `shared: True`, so this is a
    fact the environment hands us rather than an inference.

    Sliced rather than taken whole, for the same reason `schedule_agent.WOOL_SHOP_DRAW_LIMIT`
    exists: `unlocked_shops` is in unlock order and a draw lands every third day, so slicing the
    list is slicing by day. A yarn store that arrives at d9 or later is a different board -- the
    leader holds cows at 10 on all 16 of those recorded seats -- and this predicate must not claim
    it. Calling this on a day later than `Q4_DECISION_DAY` still answers the d6 question, which is
    what makes the latch below idempotent.
    """
    shops = list(((obs.get("town") or {}).get("unlocked_shops")) or [])
    return YARN_STORE in shops[:draws]


def _own_the_schedule(schedule):
    """A deep copy of `schedule`, keyed by int, that this module may mutate freely.

    Deep, not shallow. `schedule_agent.make_agent` shares its rows with its caller, so two agents
    built from one loaded dict would otherwise infect each other -- and the probe builds a shipped
    agent and a q4 agent from the same file.
    """
    return {int(k): copy.deepcopy(v) for k, v in schedule.items()}


def _arm_the_fourth_quadrant(sched):
    """Write the d12 package into the schedule: the parcel, the pens, and the sheep.

    All four edits land on one row, and they are not independent -- see the module docstring on
    `_pens_due_before_more_land`. Arming is idempotent.
    """
    row = sched.setdefault(Q4_BUY_DAY, {})
    if int(row.get("land", 0) or 0) >= 1:
        return row
    row["land"] = int(row.get("land", 0) or 0) + 1
    bought = dict(row.get("animals_bought") or {})
    bought["SHEEP"] = int(bought.get("SHEEP", 0) or 0) + Q4_EXTRA_SHEEP
    row["animals_bought"] = bought
    row["builds"] = int(row.get("builds", 0) or 0) + Q4_EXTRA_SHEEP
    row["places"] = list(row.get("places") or []) + ["SHEEP"] * Q4_EXTRA_SHEEP
    return row


def _routes_go_live_from(day):
    """Drop every solved route from `day` onward, so those days are planned live.

    The idiom is `scripts/swap_one_crop.py`'s, unchanged: set `UNSOLVE_DAYS` for anything that
    rebuilds the table, and filter the already-built dict because `PRECOMPUTED_ROUTES` is
    constructed once at import and `_apply_precomputed` reads it per call.
    """
    unsolved = tuple(range(day, SA.LAST_DAY + 1))
    COVER.UNSOLVE_DAYS = unsolved
    COVER.PRECOMPUTED_ROUTES = {d: v for d, v in COVER.PRECOMPUTED_ROUTES.items()
                                if d not in unsolved}
    return unsolved


def _herd_on_the_board(farm):
    out = collections.Counter()
    for row in farm.get("tiles") or []:
        for cell in row:
            if isinstance(cell, dict) and cell.get("animal"):
                out[cell["animal"]] += 1
    return out


def make_agent(schedule, me=0, router=True, log=sys.stderr):
    """`agent(obs, config) -> action`, identical to the shipped agent until d12.

    The returned callable carries `.q4_report`, a dict the probe reads after the game:

        armed        whether the trigger fired at d6
        shops_at_d6  the draws the decision was made on
        bought_day   the day SE actually unlocked, or None
        quadrants    quadrants owned at the last turn seen
        herd         animals standing on the board at the last turn seen
        refusals     every purchase the branch asked for and did not get

    `quadrants`, `herd`, `bought_day` and `refusals` describe the board at `me`, so they are only
    meaningful when THIS agent is the one driving that seat. A test that plays the shipped agent
    and merely asks the q4 agent what it would do gets the shipped agent's board back.

    **Refusals are reported, not swallowed.** `_do_buy_land` returns silently when the bank is
    short (`reference/kaggriculture.py:717-718`) and so does `_do_hire` (`:704-705`), so a
    four-quadrant run that quietly stayed on three quadrants would otherwise be measured and
    written up as "the parcel does not pay". Every refusal is printed to `log` once, on the turn it
    becomes certain, and recorded here.
    """
    if SA.HERD_GEESE:
        raise RuntimeError(
            "schedule_agent.HERD_GEESE is on; the q4 branch rewrites the same rows swap_in_geese "
            "does and the two have not been reconciled")

    sched = _own_the_schedule(schedule)
    inner = SA.make_agent(sched, me=me, router=router)
    report = dict(armed=False, shops_at_d6=None, bought_day=None, quadrants=1,
                  herd={}, refusals=[], live_routes_from=None)

    seen = set()

    def _refuse(tag, msg):
        """Report once per CONDITION, not once per message.

        Keyed on `tag` because every message carries the live bank, so keying on the text prints
        the same refusal on every turn for the rest of the season -- 12 lines per game in the first
        version, which is how a report becomes noise and then gets ignored.
        """
        if tag in seen:
            return
        seen.add(tag)
        report["refusals"].append(msg)
        if log is not None:
            print(f"Q4 REFUSED: {msg}", file=log, flush=True)

    def agent(obs, config=None):
        day = int(obs.get("day", 0) or 0)
        farms = obs.get("farms") or []
        farm = farms[me] if len(farms) > me else {}

        # --- the decision, once, at d6 -----------------------------------------------------
        if report["shops_at_d6"] is None and day >= Q4_DECISION_DAY:
            report["shops_at_d6"] = list(
                ((obs.get("town") or {}).get("unlocked_shops")) or [])[:Q4_DRAWS_BY_DECISION_DAY]
            if the_town_promised_wool_early(obs):
                report["armed"] = True
                _arm_the_fourth_quadrant(sched)
                report["live_routes_from"] = Q4_LIVE_ROUTES_FROM
                _routes_go_live_from(Q4_LIVE_ROUTES_FROM)

        # --- what actually happened --------------------------------------------------------
        quads = list(farm.get("unlocked_quadrants") or ["NW"])
        report["quadrants"] = len(quads)
        if report["bought_day"] is None and Q4_QUADRANT in quads:
            report["bought_day"] = day
        herd = _herd_on_the_board(farm)
        report["herd"] = dict(herd)

        if report["armed"]:
            # The parcel is due on d12 and the bank is checked every turn of it, so by dawn on d13
            # a missing SE is a refusal and not a delay.
            if day > Q4_BUY_DAY and Q4_QUADRANT not in quads:
                _refuse("parcel",
                        f"SE parcel (${KG.LAND_PRICES[2]:,}) not bought -- d{day} still on "
                        f"{quads}, bank ${float(farm.get('money', 0) or 0):,.0f}")
            # A sheep placed on d12 first shears on d18; anything not standing by d20 was never
            # bought or never got a pen, and either way it is not going to pay.
            if day >= 20 and herd["SHEEP"] < Q4_SHEEP:
                _refuse("herd",
                        f"herd short at d{day}: COW {herd['COW']} / SHEEP {herd['SHEEP']} "
                        f"against target COW {Q4_COW} / SHEEP {Q4_SHEEP}, "
                        f"bank ${float(farm.get('money', 0) or 0):,.0f}")

        return inner(obs, config)

    agent.q4_report = report
    return agent
