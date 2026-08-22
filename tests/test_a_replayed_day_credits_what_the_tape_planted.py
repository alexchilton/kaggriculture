"""A replayed day credits `state["planted"]` with what the TAPE planted, not what we would have.

`_refresh_pins` accumulates `want` over every row up to today and seats pins for
`want - state["planted"] - live`. `state["planted"]` only increments where OUR planner emits a PLANT
(`schedule_agent:2374`), and on a replayed turn our planner's answer is thrown away while the tape's
is sent. So every crop the tape puts in the ground is invisible to the counter, and the planner
arrives at the handover believing it owes the entire opening again.

Measured 2026-08-18, strawberry arm, its own seed 70683142, replay d4-d11:

    rows d0-d11 ask cumulatively      WHEAT 27, MELON 12, STRAWBERRY 37
    actually standing on the board    STRAWBERRY 37, WHEAT 17
    state["planted"] believed         WHEAT  9, MELON 12, STRAWBERRY  0
    so the backlog it chases          STRAWBERRY 37, WHEAT 18

Nothing is missing from the field -- the rows were met in full by the tape. The debt exists only in
the counter. d12's row asks for 5 plants and we emitted 10, filling every empty square with
strawberry we were already standing on, and `router.PLANT_THEN_WATER` chained a WATER onto each.

Same defect and same fix as `state["bought"]`, which is already corrected in `replayed` for exactly
this reason: the discarded planner's increments are rolled back and the tape's real actions credited.
This is the crop half, which was left undone.
"""
import collections
import json
import pathlib

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
TAPE = REPO / "data/seed_scripts/kawashigi/92466371.json"
TEAM = "カワシギ"
SEED = 70683142


def _find_state(agent):
    """The `state` dict out of `make_agent`'s closure, at whatever depth it sits."""
    seen = []

    def walk(fn, depth=0):
        if depth > 3 or not getattr(fn, "__closure__", None):
            return
        for cell in fn.__closure__:
            try:
                v = cell.cell_contents
            except ValueError:
                continue
            if isinstance(v, dict) and "planted" in v and "bought" in v:
                seen.append(v)
            elif callable(v):
                walk(v, depth + 1)
    walk(agent)
    return seen[0] if seen else None


@pytest.fixture(scope="module")
def at_dawn_of_twelve():
    """`(state, board counts, d12 PLANT count)` for the strawberry arm on its own seed."""
    pytest.importorskip("kaggle_environments")
    import sys
    sys.path.insert(0, str(REPO / "scripts"))
    import breakdown as B
    from kaggle_environments import make

    from kagg.search import melon_branch as MB
    from kagg.search import schedule_agent as SA
    B.schedule_agent = SA
    _saved_REPLAY_OPENING_DAYS = SA.REPLAY_OPENING_DAYS
    _saved_OPPONENT_MELON = MB.OPPONENT_MELON
    SA.REPLAY_OPENING_DAYS = (4, 5, 6, 7, 8, 9, 10, 11)
    MB.OPPONENT_MELON = 0                       # force the strawberry season, as resolve_days does

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
    cfg["seed"] = SEED

    env = make("kaggriculture", configuration=cfg, debug=False)
    env.reset(2)
    agent = SA.make_agent(thin, s, router=True)
    state = _find_state(agent)
    snapshot, plants, board = None, 0, collections.Counter()
    for t in range(13 * 24):
        ob = env.state[s].observation
        day = int(ob.get("day", 0) or 0)
        if day == 12 and int(ob.get("hour", 0) or 0) == 0 and snapshot is None:
            snapshot = collections.Counter(state["planted"])
            # **The board is read HERE, at the same instant as the counter.** It used to be read
            # after the loop broke at d13, so the comparison was a d12-dawn counter against a d13
            # board and the gap was d12's own five plantings. That is the `farm:0.445` failure in
            # CLAUDE.md -- both numbers right, taken over different units -- and it read as a
            # 2-crop crediting bug that does not exist. Corrected 2026-08-22.
            board = collections.Counter()
            for _row in (((ob.get("farms") or [{}])[s] or {}).get("tiles") or []):
                for _c in _row:
                    if isinstance(_c, dict) and _c.get("crop"):
                        board[_c["crop"]] += 1
        n = [len((env.state[0].observation["farms"][i] or {}).get("hands") or []) for i in (0, 1)]
        m = agent(ob)
        if day == 12:
            plants += sum(1 for u in [m["farmer"]] + list(m["hands"])[:n[s]]
                          if u and u[0] == "PLANT")
        if day == 13:
            break
        st = opp[t] if t < len(opp) else {}
        a = [None, None]
        a[s] = {"farmer": m["farmer"], "hands": list(m["hands"])[:n[s]], "market": m["market"]}
        a[o] = {"farmer": st.get("farmer") or ["PASS"],
                "hands": list(st.get("hands") or [])[:n[o]], "market": st.get("market") or []}
        env.step(a)
    try:
        yield snapshot, board, plants
    finally:
        SA.REPLAY_OPENING_DAYS = _saved_REPLAY_OPENING_DAYS
        MB.OPPONENT_MELON = _saved_OPPONENT_MELON



def test_the_counter_knows_the_tape_planted_the_strawberry(at_dawn_of_twelve):
    """Whatever is standing at d12 dawn, the counter must know about it. It used to read 0.

    **Asserted against the board taken at the SAME instant, from 2026-08-22.** The literal `37` was
    a d13 board number checked against a d12-dawn counter, so it failed at 35 and read as a
    two-crop crediting bug. The two missing plants were d12's own row, which
    `test_the_handover_day_plants_its_row_and_not_the_whole_opening` measures separately and which
    passes at 5. Comparing the counter to the board it is a counter OF removes the gap entirely and
    is a stronger assertion than a hard-coded number, which cannot tell a real regression from a
    changed tape.

    **The margin is ZERO, measured.** Tightened to `==` as a probe on 2026-08-22 and it passed:
    counter and board are exactly equal at d12 dawn. So `>=` is not slack hiding a defect -- one
    crop of under-crediting fails it. `>=` is kept rather than `==` because over-crediting is
    legitimate later in a season: a harvested tile clears from the board while the counter, which
    counts plantings rather than standing crops, correctly does not go down.
    """
    planted, board, _plants = at_dawn_of_twelve
    assert board["STRAWBERRY"] > 0, "no strawberry on the board at d12; the fixture is not replaying"
    assert planted["STRAWBERRY"] >= board["STRAWBERRY"], (
        f"state['planted'] says STRAWBERRY {planted['STRAWBERRY']} while {board['STRAWBERRY']} are "
        f"standing at d12 dawn; `_refresh_pins` seats pins for `want - planted - live`, so the "
        f"planner will chase the difference and plant them again")


def test_the_handover_day_plants_its_row_and_not_the_whole_opening(at_dawn_of_twelve):
    """d12's row asks for 5. It emitted 10 before the fix."""
    _planted, _board, plants = at_dawn_of_twelve
    # 10 before the counter fix, 7 after, 5 once the surplus PINS were dropped as well. The residual
    # two were never the backlog -- the counter read exactly what the rows asked -- they were pins
    # seated during the replay that the tape had satisfied on other squares and nothing released.
    # See `tests/test_a_pin_is_dropped_when_the_row_no_longer_wants_it.py`.
    assert plants == 5, (
        f"d12 emitted {plants} PLANTs against a row of 5; 10 before the counter fix, 7 before the "
        "surplus pins were dropped")
