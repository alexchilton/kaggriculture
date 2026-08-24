"""A tape hand that PLANTs onto a WEED plants nothing, and the ground stays dead.

`kaggriculture.py:417-421` -- `PLANT` returns silently when the tile is not `None`, and a WEED is a
dict, so the seed is not even spent. `DIG` (`:484`) clears it. So a tape written on a board with no
weed on that tile, replayed on a board that has one, loses the tile for the rest of the season.

Measured 2026-08-24 on the two kawashigi games whose board first differs at d6:

    97397843  d5 h11  his hand DIG                ours hand PLANT STRAWBERRY
              d5 h12  his hand PLANT STRAWBERRY   ours hand WATER
              d6      tile (3,1)  his STRAWBERRY  ours WEED

    92452538  d5 h14  his hand DIG                ours hand PLANT STRAWBERRY
              d6      tile (4,1)  his STRAWBERRY  ours WEED

`weedSpawnChance` is 0.005 on the ladder, so which tiles carry a weed is a per-game draw the canned
tape cannot know. The replay must read the live board, exactly as it already does for the shed when
it rewrites a `PICKUP`/`PLACE` whose species was re-labelled (`schedule_agent.py:5530-5550`).
"""

import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
GAME = REPO / "data/seed_scripts/kawa_2026-08-24/97397843.json"
WHO = "カワシギ"
TPD = 24

#: d5 h11 -- the turn his recording DIGs and our replay plants into the weed.
TURN = 5 * TPD + 11


def _agent_actions_up_to(turn):
    """Drives our agent in his seat, on the game's own seed, against his recorded opponent.

    Returns the action our agent submits on `turn`, and the board it is looking at.
    """
    import sys
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(REPO / "scripts"))
    from kaggle_environments import make
    import breakdown as B
    import us_in_his_seat as U
    from kagg.search import schedule_agent as SA

    B.schedule_agent = SA
    rec = json.loads(GAME.read_text())
    names = (rec.get("info") or {}).get("TeamNames") or []
    seat = names.index(WHO)
    seed = (rec.get("info") or {}).get("seed")
    steps = rec["steps"]
    them = 1 - seat

    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, seat)

    for t in range(turn + 1):
        o = env.state[seat].observation
        farm = o["farms"][seat]
        n_us = len(farm.get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        if t == turn:
            return mine, farm
        at = U._recorded(steps, t, them)
        n_them = len(o["farms"][them].get("hands") or [])
        env.step([mine, {"farmer": at.get("farmer") or ["PASS"],
                         "hands": list(at.get("hands") or [])[:n_them],
                         "market": at.get("market") or []}]
                 if seat == 0 else
                 [{"farmer": at.get("farmer") or ["PASS"],
                   "hands": list(at.get("hands") or [])[:n_them],
                   "market": at.get("market") or []}, mine])
    raise AssertionError("never reached the turn")


@pytest.mark.skipif(not GAME.exists(), reason="replay not on disk")
def test_a_replayed_hand_digs_the_weed_it_is_standing_on():
    """No unit may be sent to PLANT on a tile the live board says is a WEED."""
    mine, farm = _agent_actions_up_to(TURN)

    tiles = farm["tiles"]
    positions = [tuple(farm["farmer"])] + [tuple(p) for p in (farm.get("hands") or [])]
    acts = [mine["farmer"]] + list(mine["hands"])

    planting_onto_occupied = []
    for i, act in enumerate(acts):
        if not act or act[0] != "PLANT":
            continue
        y, x = positions[i]
        tile = tiles[y][x]
        if tile is not None:
            kind = tile.get("kind") if isinstance(tile, dict) else tile
            planting_onto_occupied.append((i, (y, x), list(act), kind))

    assert not planting_onto_occupied, (
        "a hand is planting onto an occupied tile, which the reference makes a silent no-op "
        f"(kaggriculture.py:420): {planting_onto_occupied}"
    )
