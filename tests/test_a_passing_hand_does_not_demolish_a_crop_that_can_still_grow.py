"""`HARVEST_WHAT_YOU_STAND_ON` lets a hand crossing a tile harvest a crop that still owes a water.

The underfoot rule is deliberately harvest-only::

    # HARVEST only, never WATER: a harvest is a turn for a whole yield and it clears the
    # tile for a replant, whereas watering a tile someone else is routed to merely moves
    # the turn around.

That reasoning holds every day but one. On a one-shot crop's `max_day` the water is not a turn moved
around -- it is a unit of yield, because `crop_ops` offers WATER while
`in_window = (max_day + 1) // 2 <= age <= max_day` is still true at the top of the range. So a hand
that merely walks over the tile demolishes a crop with a unit still coming, and the routed hand that
was going to water it then arrives at bare ground.

Measured on the kawashigi board, seed 11, day 4 -- wheat's `max_day`, sown d0, every one of the
seven tiles standing at `yield_units = 3` at dawn:

      h06 (3,2)  3 -> 0    demolished underfoot; `_live_ops` is never consulted at (3,2) until h11,
                           by which point it is bare ground carrying a PLANT pin, and the routed
                           WATER lands at h12 on the replant (planted_day 4, yield 1)
      h14 (1,4)  3 -> 0    same
      h07 (4,1)  4 -> 0    routed: WATER h05, HARVEST h06
      h09 (2,2)  4 -> 0    routed: WATER h07, HARVEST h08
      h17 (0,4)  4 -> 0    routed: WATER h15, HARVEST h16
      h18 (1,3)  4 -> 0    routed: WATER h16, HARVEST h17
      h21 (2,3)  4 -> 0    routed: WATER h19, HARVEST h20

Five routed tiles bank 4; the two taken underfoot bank 3. 26 against the tape's 28, whose earliest
harvest of the day is h08 -- after its watering round -- and whose seven tiles all come in full.

The two units do not come back. The wheat ledger holds the gap at exactly 2 through d5 and d6, and
we open d7 holding 0 against his 1, which is a hand reaching the pen on (4,2) at h14 with
`inv_WHEAT = 0` and day 7 reading `feed 8/9`.

**Withholding the HARVEST is not the fix and must not be retried** -- see
`docs/the_last_growing_days_water_2026-08-14.md`. Gating `_one_shot_is_finished` on `watered_today`
banks the 28 and costs $19,595, because a deferred harvest is a tile that never clears, never
replants, and starves the herd: d8 animals 9 -> 0. The harvest must still be offered the moment it
is legal. What has to stop is a PASSER-BY taking it off a crop that is still growing, which leaves
the tile to the routed hand that already emits WATER then HARVEST back to back.
"""
import importlib
import json
import pathlib

import pytest

SEED = 11
DAY = 4


def _wheat(farm):
    return {(x, y): (c.get("yield_units") or 0)
            for y, row in enumerate(farm["tiles"])
            for x, c in enumerate(row)
            if isinstance(c, dict) and c.get("kind") == "PLANT" and c.get("crop") == "WHEAT"}


@pytest.fixture(scope="module")
def harvest():
    """Wheat units taken off our tiles on day 4, and the board at that day's dawn."""
    import scripts.breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay, schedule, team = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    ours = SA.make_agent(thin, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    prev, taken, dawn = None, [], {}
    for t in range((DAY + 1) * 24):
        o0, o1 = env.state[0].observation, env.state[1].observation
        o0.town["unlocked_shops"] = list(shops(t))
        cur = _wheat(o0["farms"][0])
        if t == DAY * 24:
            dawn = dict(cur)
        if prev is not None and t // 24 == DAY:
            for k, v in prev.items():
                gone = max(0, v - cur.get(k, 0))
                if gone:
                    taken.append((t % 24, k, gone))
        prev = cur
        a0, a1 = ours(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return taken, dawn


def test_the_premise_day_four_is_wheats_last_growing_day(harvest):
    """Guard. A day earlier the harvest is not legal; a day later the water buys nothing."""
    from kagg.search import routines as R
    _taken, dawn = harvest
    assert dawn, f"no wheat standing at d{DAY} dawn"
    assert DAY == R.CROP_TABLE["WHEAT"]["max_day"], (
        f"d{DAY} is not wheat's max_day ({R.CROP_TABLE['WHEAT']['max_day']}) for a d0 sowing, so a "
        "water here is not worth a unit and this test measures nothing")


def test_the_premise_every_tile_can_still_take_one_more_unit(harvest):
    """Guard. A tile at `max_yield` is finished and harvesting it underfoot loses nothing."""
    from kagg.search import routines as R
    _taken, dawn = harvest
    cap = R.CROP_TABLE["WHEAT"]["max_yield"]
    full = {t: v for t, v in dawn.items() if v >= cap}
    assert not full, (
        f"tiles {full} are already at max_yield {cap} at dawn -- nothing to lose, nothing to measure")


def test_every_tile_banks_the_water_it_was_still_owed(harvest):
    taken, dawn = harvest
    short = [(h, t, got, dawn.get(t, 0)) for h, t, got in taken if got < dawn.get(t, 0) + 1]
    total = sum(got for _h, _t, got in taken)
    assert not short, (
        f"d{DAY} took {total} wheat units off {len(taken)} tiles; {len(short)} banked no more than "
        f"they held at dawn: {short} (hour, tile, banked, dawn). d{DAY} is wheat's max_day, so every "
        "tile is owed one more unit from one more water. `HARVEST_WHAT_YOU_STAND_ON` lets a hand "
        "merely crossing the tile take the harvest -- and it explicitly refuses to water -- so a "
        "crop that was still growing is demolished by a passer-by while the routed hand that would "
        "have watered it arrives at bare ground. The tape's earliest harvest that day is h08, after "
        "its watering round, and all seven of its tiles come in full.")
