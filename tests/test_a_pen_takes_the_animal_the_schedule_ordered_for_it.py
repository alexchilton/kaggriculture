"""The `places` row is an ORDER, and the executor re-decides it by global rank.

`schedule.json` d0 says:

    places = ['SHEEP', 'COW', 'SHEEP', 'COW']

The leader places exactly that -- SHEEP (4,3) h04, COW (4,4) h04, SHEEP (3,3) h05, COW (3,4) h12.
We place SHEEP (2,4) h07, SHEEP (3,4) h12, COW (4,4) h17, COW (4,3) h20: **SHEEP, SHEEP, COW, COW**.

The cause is `_place_order()`, a global species ranking that never reads the row:

    sorted(R.ANIMAL_NAMES, key=lambda a: ANIMALS[a]["first_yield_day"] - ANIMALS[a]["max_held"])
    -> ['GOOSE', 'SHEEP', 'COW']            SHEEP key 0, COW key 2

`_live_ops` uses it for any bare pen, so a hand carrying both a sheep and a cow places the sheep
every time, and the row's alternation is lost. `router.build_nodes` already does this correctly --
it reads `pen_for` off the row and calls it "a preference, never a lock" -- so the PLANNER reserves
the pen and the EXECUTOR ignores the reservation.

**Why it costs money rather than being cosmetic.** Same six animals, same counts, different tiles:

    ours   SHEEP (2,4)  SHEEP (3,4)  COW (4,4)  COW (4,3)  COW (3,3)  COW (4,2)
    tape   SHEEP (4,3)  SHEEP (3,3)  COW (4,4)  COW (3,4)  COW (2,4)  COW (4,2)

Produce is harvested into the HAND's inventory, not the shed. At d6 h4 his u4 carries
`{'WOOL': 6}` and ours carries `{}`, because his HARVEST landed on a sheep pen and ours on a cow
pen. His `SELL WOOL 6` fills for +$234 and ours no-ops; from that turn the two games diverge --
his BUY_LAND settles, ours is refused, and the day ends $4 against $1,251.

A herd census hides all of it: both boards read `{'COW': 4, 'SHEEP': 2}` at d6 dawn.
"""
import importlib
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
REPLAY = "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"


def placements(days=1, seed=11, weeds=0.0):
    """`[(day, hour, animal, tile)]` in the order seat 0 actually places them."""
    from kaggle_environments import make

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 99

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / REPLAY)
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, 0)
    opp = B.tape_policy(replay, TEAM, 1)
    out, seen = [], set()
    for t in range(days * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        env.step([agent(o0), opp(o1, t)])
        d, h = divmod(t, TPD)
        for y, row in enumerate(env.state[0].observation["farms"][0]["tiles"]):
            for x, c in enumerate(row):
                if isinstance(c, dict) and c.get("animal") and (x, y) not in seen:
                    seen.add((x, y))
                    out.append((d, h, c["animal"], (x, y)))
    return out


def test_the_premise_the_row_alternates():
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    assert raw["0"]["places"] == ["SHEEP", "COW", "SHEEP", "COW"]


def test_the_premise_the_optimiser_puts_sheep_first():
    """So a hand holding both always picks SHEEP, whatever the row says."""
    from kagg.search.schedule_agent import _place_order
    order = _place_order()
    assert order.index("SHEEP") < order.index("COW")


#: The leader's opening pen map, read off the replays and **identical on both his seasons** --
#: melon `92498144` and strawberry `92466371` place the same species on the same six tiles at the
#: same hours. It is a fixed opening, not a reaction to the board.
#:
#: The species sequence is exactly the schedule's own `places` rows in order -- d0
#: `['SHEEP','COW','SHEEP','COW']`, d3 `['COW']`, d5 `['COW']` -- so nothing here invents an
#: allocation. What it pins is the GROUND, which `_refresh_pins` currently chooses by depot
#: distance and gets wrong: we take `(2,4)` on d0 where he takes `(3,3)`, and the row then lands on
#: different tiles.
#:
#: `schedule.json`'s own `build_tiles` disagrees with both replays -- it says `(4,3) COW` and
#: `(4,2) SHEEP` where the games show `(4,3) SHEEP` and `(4,2) COW` -- so it is not usable as the
#: source. These come from the recorded boards.
PEN_MAP = {(4, 3): "SHEEP", (4, 4): "COW", (3, 3): "SHEEP", (3, 4): "COW",
           (2, 4): "COW", (4, 2): "COW"}


def test_the_pens_hold_the_species_the_leader_put_them_on():
    """The tile -> species map through d5, which is what the season actually reads.

    Op counts cannot see this. A HARVEST on a sheep and a HARVEST on a cow are both `HARVEST 1`,
    so the grid reads `HARVEST 5/5` while one hand carries wool and the other milk. Measured by
    replaying his d8 onto our board: `u2 HARVEST @ (3,4)` finds `SHEEP` where his finds `COW`,
    both `PLACE MILK 6` move zero units, and the `SELL MILK 12` in the same basket -- the one
    funding his eleventh hire and ten strawberry seeds -- no-ops on an empty shed.
    """
    got = {t: a for _d, _h, a, t in placements(days=6)}
    assert got == PEN_MAP, (
        f"pens hold {dict(sorted(got.items()))}\n"
        f"leader holds {dict(sorted(PEN_MAP.items()))}")


def yields_at_dawn(day=6, seed=11, weeds=0.0):
    """`{tile: (animal, yield_units)}` on seat 0's board at the dawn of `day`."""
    import importlib as _il

    from kaggle_environments import make

    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = _il.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 99
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / REPLAY)
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    agent, opp = SA.make_agent(sched, 0), B.tape_policy(replay, TEAM, 1)
    for t in range(day * TPD):
        o0, o1 = env.state[0].observation, env.state[1].observation
        env.step([agent(o0), opp(o1, t)])
    return {(x, y): (c["animal"], c["yield_units"])
            for y, row in enumerate(env.state[0].observation["farms"][0]["tiles"])
            for x, c in enumerate(row) if isinstance(c, dict) and c.get("animal")}


def test_the_day_zero_sheep_reach_their_first_shearing_full():
    """A SHEEP placed on d0 must bank five fed-and-cared nights before it first produces.

    `_daily_refresh_animals` (`reference/kaggriculture.py:823`) pays
    `yield_units = min(max_held, 1 + pending_care_bonus)` on the first production night, and
    `pending_care_bonus` gains +1 only on a night the animal was BOTH fed and cared (`:831`).
    A SHEEP has `first_yield_day 6` and `max_held 6`, so its first shearing is the d5 -> d6
    rollover and it needs 5 of those 6 nights to come out full.

    We bank 4 and shear 5; the tape banks 5 and shears 6. The gap is d0: `will_be_fed` gives an
    arriving pen a feed only while `ARRIVAL_FEED_REMAINING > 0`, the row allows two, and our route
    reaches the two COWs first -- so the cows eat the whole allowance. Their bonus is wasted. A COW
    first produces at the d7 -> d8 rollover, so it has 8 nights to bank the same 5 and caps either
    way; measured at d6 dawn our cows carry `bonus 6` against the tape's 5.

    Two units of wool at d6, which is `SELL 15/17` and the money that settles his d6 BUY_LAND.
    """
    got = yields_at_dawn(6)
    sheep = {t: y for t, (a, y) in got.items() if a == "SHEEP"}
    assert sorted(sheep.values()) == [6, 6], (
        f"sheep shear {sheep}, want 6 each. Board at d6 dawn: {dict(sorted(got.items()))}")


def wool_fills(day=6, seed=11, weeds=0.0):
    """`[(hour, [unit prices])]` for every WOOL sale seat 0 makes on `day`."""
    import collections as _c
    import importlib as _il

    from kaggle_environments import make

    import breakdown as B
    from kagg.analysis.fills import record_fills
    from kagg.search import melon_branch as _MB
    SA = _il.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0                       # the strawberry season
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    replay = str(REPO / "data/seed_scripts/kawashigi/92466371.json")
    shops = B.recorded_shops(replay)
    env = make("kaggriculture", configuration=dict(B.env_config(replay), seed=seed,
                                                   weedSpawnChance=weeds), debug=True)
    env.reset(2)
    agent, opp = SA.make_agent(sched, 0), B.tape_policy(replay, TEAM, 1)
    with record_fills(env) as f:
        for t in range((day + 1) * TPD):
            o0, o1 = env.state[0].observation, env.state[1].observation
            env.state[0].observation.town["unlocked_shops"] = list(shops(t))
            a0, a1 = agent(o0), opp(o1, t)
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o1["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
    lots = _c.defaultdict(list)
    for d, h, op, item, price in f.at_turn(0):
        if d == day and op == "SELL" and item == "WOOL":
            lots[h].append(price)
    return sorted(lots.items())


@pytest.mark.xfail(reason="OPEN: the hour a loaded pen is REACHED is not set by crew.OP_ORDER. "
                          "Reordering the ops within a tile moved nothing -- first sale stays h11. "
                          "The lever is which RUN a unit walks first, in crew.cover's packing.",
                   strict=False)
def test_the_day_six_wool_reaches_the_market_on_the_top_rung():
    """First seller takes the top of the price ladder, and d6 is a wool day.

    Both sides shear the same 12 units and sell them in two lots of six, and all four lots fill.
    Measured, seed 11, strawberry arm, `weeds 0.0`:

        tape   HARVEST h02, h04   SELL h04 [218,217,215,214,212,209]   SELL h07 [199..194]   2,464
        ours   HARVEST h09, h18   SELL h11 [199,198,197,196,195,194]   SELL h21 [193..185]   2,315

    Our first lot is byte-identical to his SECOND -- the same rung -- because the book has already
    been walked down by the time we arrive. Spending is level across the day, $1,645 to $1,651, so
    the whole $143 gap in d6's bank is this, and it is what leaves d7 unable to fund its seed.

    HARVEST does not wait on upkeep: `reference/kaggriculture.py:446` tests `yield_units > 0` and
    nothing else, and `yield_units` is written only by `_daily_refresh_animals:827` at the night
    rollover. The wool is standing on both sheep when the day opens.
    """
    lots = wool_fills(6)
    assert lots, "no wool sold on d6 at all"
    first_hour = lots[0][0]
    total = sum(sum(ps) for _h, ps in lots)
    assert first_hour <= 7 and total >= 2400, (
        f"first wool sale at h{first_hour} for {round(total)} over lots "
        f"{[(h, [round(p) for p in ps]) for h, ps in lots]}; the tape opens at h4 and banks 2,464.")
