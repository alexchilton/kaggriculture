"""(0,0) is harvested on d4 and left EMPTY overnight, because d5 plants strawberry on it.

`REPLANT_A_CLEARED_TILE` gives every one-shot harvest the PLANT its cleared tile can take, in the
same stop. That is right nearly everywhere and wrong on exactly one square of the opening: the
leader harvests his (0,0) wheat during d4 and leaves the ground bare, so his d5 h14 hand can sow
strawberry there. We harvest at d4 h11 and re-sow wheat at h12, and the strawberry is then refused
the next day -- `PLANT` onto an occupied tile does nothing.

Measured 2026-08-17 on the melon tape's OWN seed 1240813987, our agent in his seat, replay d5-d11 on:

    d4 h10  WATER          d4 h11  HARVEST -> empty      d4 h12  PLANT WHEAT   <- the defect
    d5 h14  PLANT STRAWBERRY -> refused, our d4 wheat is standing

It is the last surviving member of the family `OPENING_GEOMETRY` fixed: three tiles carrying the
wrong crop into d5, of which two were the wrong SPECIES at sowing and this one is the right species
sown a day too late. With it, every replayed PLANT in d5-d11 lands.

Seed matters here and did not used to: these tapes' own seeds are 1240813987 and 70683142, not 11,
and on seed 11 the trigger and the town are both somebody else's.
"""
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
TAPE = REPO / "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"


@pytest.fixture(scope="module")
def dawn_of_day_five():
    """Our own (0,0) at dawn on d5, playing his seat on his seed against his opponent."""
    pytest.importorskip("kaggle_environments")
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    import breakdown as B
    from kaggle_environments import make

    from kagg.search import schedule_agent as SA
    B.schedule_agent = SA
    # **The window the agent SHIPS with, not the one this test was written against.** It pinned
    # `(5..11)` and therefore played d4 with our own planner, which is the configuration
    # `FALLOW_UNTIL` existed for. d4 is taped now, so the tape's own d4 actions are sent and the
    # re-sow this file is about cannot happen -- which is why `FALLOW_UNTIL` was deleted on
    # 2026-08-18. Pinning a superseded window here would have kept the test green against an agent
    # nobody ships.
    SA.REPLAY_OPENING_DAYS = (4, 5, 6, 7, 8, 9, 10, 11)

    d = json.loads(TAPE.read_text())
    names = d["info"]["TeamNames"]
    s = names.index(TEAM)
    o = 1 - s
    plan = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in plan.items()}
    opp = [((f[o] or {}).get("action") or {}) for f in d["steps"][1:]]
    cfg = dict(d.get("configuration") or {})
    cfg.pop("steps", None)
    cfg["seed"] = d["info"]["seed"]

    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    agent = SA.make_agent(thin, s, router=True)
    seen = {}
    for t in range(6 * 24):
        ob = env.state[s].observation
        if int(ob.get("day", 0) or 0) == 5 and int(ob.get("hour", 0) or 0) == 0:
            tiles = ((ob.get("farms") or [{}])[s] or {}).get("tiles") or []
            c = tiles[0][0] if tiles and tiles[0] else None
            seen["cell"] = c if isinstance(c, dict) else {}
            break
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        m = agent(ob)
        st = opp[t] if t < len(opp) else {}
        a = [None, None]
        a[s] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[s]], "market": m["market"]}
        a[o] = {"farmer": st.get("farmer") or ["PASS"],
                "hands": list(st.get("hands") or [])[:n[o]], "market": st.get("market") or []}
        env.step(a)
    return seen["cell"]


def test_the_tile_the_strawberry_needs_is_left_fallow(dawn_of_day_five):
    """No crop on (0,0) at dawn d5, so d5's strawberry has somewhere to go."""
    assert not dawn_of_day_five.get("crop"), (
        f"(0,0) carries {dawn_of_day_five.get('crop')} planted on day "
        f"{dawn_of_day_five.get('planted_day')} at dawn d5; the tape sows STRAWBERRY here at d5 h14 "
        "and PLANT onto an occupied tile is refused")


def test_his_own_board_has_it_empty_there(dawn_of_day_five):
    """The target, straight off his replay. If this fails the premise is wrong, not the agent."""
    d = json.loads(TAPE.read_text())
    s = d["info"]["TeamNames"].index(TEAM)
    obs = (d["steps"][5 * 24][s] or {}).get("observation") or {}
    tiles = ((obs.get("farms") or [{}])[s] or {}).get("tiles") or []
    c = tiles[0][0] if tiles and tiles[0] else None
    c = c if isinstance(c, dict) else {}
    assert not c.get("crop"), f"his own (0,0) is not empty at dawn d5, it holds {c.get('crop')}"
