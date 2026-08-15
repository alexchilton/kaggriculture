"""A weed is only worth clearing if something is going into that square. Per day, per value.

**The mechanism.** `router.build_nodes` offers a DIG on every WEED tile in an unlocked quadrant,
priced at half the best plant prize for the day. Nothing in that branch asks whether we will ever
sow the square. `DIG_ONLY_IF_REPLANTING` looks like the guard and is not: it lives in
`_pointless_tiles` and gates on `plants_left`, one flag for the WHOLE SEASON, which reads True while
21 squares are pinned for pasture and the rest are outside any plan.

A weed blocks only the tile it sits on. So a DIG on ground the plan never sows buys nothing at all,
and it is not free -- it is a turn, plus the walk to reach it.

Measured on 91422988 (`townCenterSellInterval = 24`, the economy we actually play) before the gate:

    dig      d7 1/0   d12 3/0   d13 3/0   d14 5/0        the tape digs NOTHING all season
    work     953/1299 over d0-d16
    idle    1888/807

and after:

    dig      none, any day
    work    1183/1299          +230 turns, all of it d11-d16
    idle    1647/807

d0-d5 is byte-identical either way, which is why this is stated as a rule about WHICH square rather
than as a season total: the total is the consequence, the rule is the claim.

Two tests, because they fail for different reasons and a single one would hide that:

- `test_no_dig_is_offered_on_ground_the_plan_will_not_sow` is the mechanism, checked against the
  planner's own pin set. It goes red the moment the `plantable` argument is dropped.
- `test_we_do_not_dig_more_than_the_tape_on_any_day` is the per-day value, which is what Alex asked
  for and what actually caught this: a season total of "a few digs" is invisible, `d14 5/0` is not.
"""
import collections
import importlib
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
REPLAY = REPO / "data/seed_scripts/top_guys/91422988.json"
SCHEDULE = REPO / "data/seed_scripts/top_guys/91422988/schedule.json"
TEAM = "Seb (allegedly)"
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")
SEED = 11
DAYS = 17
MODULE = "kagg.search.schedule_agent"


def _thin():
    raw = json.loads(SCHEDULE.read_text())
    return {int(k): {k2: v2 for k2, v2 in r.items() if k2 not in TAPE_ONLY}
            for k, r in raw.items()}


def _opponent():
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    return [{"farmer": (s.get("action") or {}).get("farmer", ["PASS"]) or ["PASS"],
             "hands": list((s.get("action") or {}).get("hands") or []),
             "market": list((s.get("action") or {}).get("market") or [])}
            for s in (step[1 - seat] or {} for step in d["steps"][1:])], seat


def _tape_digs_per_day():
    """His own DIG count per day, straight off the replay actions."""
    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    per = collections.Counter()
    for t, step in enumerate(d["steps"][1:]):
        act = (step[seat] or {}).get("action") or {}
        for a in [act.get("farmer") or ["PASS"], *(act.get("hands") or [])]:
            if a and a[0] == "DIG":
                per[t // 24] += 1
    return per


@pytest.fixture(scope="module")
def our_digs():
    """Our DIG count per day, and the tiles they landed on."""
    from kaggle_environments import make

    SA = importlib.import_module(MODULE)
    opp_acts, _seat = _opponent()

    env = make("kaggriculture", configuration={"seed": SEED, "weedSpawnChance": 0.0}, debug=True)
    env.reset(2)
    agent = SA.make_agent(_thin(), 0, router=True)

    per = collections.Counter()
    where = []
    for t in range(24 * DAYS):
        o0 = env.state[0].observation
        a0, a1 = agent(o0), opp_acts[t]
        farm = o0["farms"][0]
        pos = [tuple(farm["farmer"])] + [tuple(h) for h in (farm.get("hands") or [])]
        for u, ac in enumerate([a0["farmer"], *a0["hands"]]):
            if ac and ac[0] == "DIG":
                per[t // 24] += 1
                where.append((t // 24, t % 24, u, pos[u] if u < len(pos) else None))
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return per, where


def test_no_dig_is_offered_on_ground_the_plan_will_not_sow():
    """The mechanism, at the node level: `build_nodes` must not offer a DIG off the pin set.

    Driven directly rather than through a season, so a failure names the rule and not a total.
    Red with `plantable` removed from the call, which is the whole content of the fix.
    """
    RT = importlib.import_module("kagg.search.router")
    R = importlib.import_module("kagg.search.routines")

    weed = {"kind": "WEED"}
    tiles = [[dict(weed) for _ in range(10)] for _ in range(10)]
    # `unlocked` holds quadrant NAMES ("NW"), not indices. Passing `set(range(4))` matches nothing,
    # every tile is skipped, and the test reads as "the gate disabled digging" when it did no such
    # thing -- which is exactly the wrong conclusion this fixture drew the first time.
    unlocked = {R.quadrant_of(1, 1)}
    sown = {(1, 1), (2, 2)}

    offered = RT.build_nodes(tiles, 3, {}, {}, unlocked, {}, 0, plantable=sown)
    dug = {n.tile for n in offered if any(o == "DIG" for o, _i in n.ops)}

    # The control: without the gate this same board offers a DIG on every weed in the quadrant.
    ungated = RT.build_nodes(tiles, 3, {}, {}, unlocked, {}, 0)
    wide = {n.tile for n in ungated if any(o == "DIG" for o, _i in n.ops)}
    assert len(wide) > len(sown), (
        "the ungated call did not offer more digs than the gated one, so this board cannot "
        "distinguish the rule from its absence and the test proves nothing."
    )

    assert dug <= sown, (
        f"a DIG was offered on ground the plan will never sow: {sorted(dug - sown)[:10]}\n"
        "  A weed blocks only its own tile. Clearing one nothing is going into is a turn spent "
        "tidying, plus the walk to reach it."
    )
    assert dug, (
        "no DIG was offered at all, on a board that is entirely weeds with two squares pinned to "
        "be sown -- the gate has gone from narrowing the rule to disabling it."
    )


@pytest.mark.parametrize("day", range(DAYS))
def test_we_do_not_dig_more_than_the_tape_on_any_day(day, our_digs):
    """Per day, per value. He digs nothing all season; neither should we."""
    per, where = our_digs
    his = _tape_digs_per_day().get(day, 0)
    ours = per.get(day, 0)
    detail = "\n".join(f"      d{d} h{h} u{u} @ {t}" for d, h, u, t in where if d == day)
    assert ours <= his, (
        f"d{day}: we dug {ours} times, the tape dug {his}\n{detail}\n"
        "  Before the per-tile gate this was d7 1/0, d12 3/0, d13 3/0, d14 5/0, and removing "
        "those digs returned +230 work turns over d0-d16."
    )
