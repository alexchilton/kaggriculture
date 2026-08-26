"""Seed bought and never sown is unconditional loss, and we end the season holding piles of it.

Measured on ladder game 99370605 (lost by $329), reading `private["seeds"]` at the final step:

    us       CARROT  8   WHEAT 12      $280
    Khalid   CARROT  1   WHEAT  8      $100

and on 99361310 (lost by $12,165):

    us       CARROT 10   MELON 1   WHEAT 19    $470
    them     WHEAT   1                          $10

The per-day trace of 99370605 shows two distinct causes, and only the second is a code defect:

    d6    BUY_SEED CARROT 8      -- and CARROT sits at exactly 8 every dawn from d7 to d29
    d27   dawn WHEAT 11, BUY_SEED WHEAT 12, 11 PLANTs  -- the store is never drawn down

The wheat one is `schedule_agent.py:5244`:

    short = max(short, _row_q - max(0, _bought))

The line above it already nets held stock (`short = qty - seeds[crop]`). This floor then replaces
that with the tape row's PURCHASE total, so the row is re-bought daily however full the store is.
The floor is deliberate -- `:5231` records that netting against carry cancelled d7's strawberry row
and cost `plant 9/11` and `water 38/41` on d11 -- so the fix has to cap it, not delete it.

This test pins the OUTCOME, not the mechanism, so it stays honest if the fix moves elsewhere: a
finished season must not be holding more seed than a single day could plant.

Run it alone. Never the whole suite -- `CLAUDE.md` and the `matching-the-tape` skill both forbid it.

    python -u -m pytest tests/test_the_season_does_not_end_holding_seed_it_never_sowed.py -q
"""

import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
TPD = 24
TAPE_ONLY = ("plant_tiles", "build_tiles", "land_turns", "orders")

#: The most a day has ever planted of one crop in these games is 27 (d11 of 99370605, all crops
#: together). A store above this cannot be explained as "tomorrow's plantings, bought early".
MAX_DEFENSIBLE_CARRY = 6


def _play(seed=700, opponent="contrarian"):
    from kaggle_environments import make

    from kagg.arena.pool import OPPONENTS, _build
    import kagg.search.schedule_agent as SA

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in TAPE_ONLY}
             for k, r in raw.items()}

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = SA.make_agent(sched, 0, router=True)
    them = _build(OPPONENTS[opponent], None)
    for _ in range(30 * TPD):
        o0 = env.state[0].observation
        a0 = me(o0, env.configuration)
        n0 = len(o0["farms"][0].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"] or [])[:n0],
                   "market": a0["market"]},
                  them(env.state[1].observation, env.configuration)])
        if env.done:
            break
    priv = env.state[0].observation.get("private") or {}
    return {k: int(v) for k, v in (priv.get("seeds") or {}).items() if int(v or 0) > 0}


@pytest.mark.parametrize("seed", [700, 701])
def test_the_bell_does_not_find_us_holding_a_pile_of_unsown_seed(seed):
    held = _play(seed)
    worst = max(held.values()) if held else 0
    assert worst <= MAX_DEFENSIBLE_CARRY, (
        f"seed {seed}: holding {held} at the bell. Anything above {MAX_DEFENSIBLE_CARRY} of one "
        f"crop was bought and never sown -- see `schedule_agent.py:5244`."
    )
