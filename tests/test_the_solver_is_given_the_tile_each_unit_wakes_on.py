"""The fixture handed to the solver carries the tile each unit WAKES on, not a prediction of it.

`solve_day.py` optimises a tour from the start tiles in `units`, so a wrong start tile misprices every
op after it and the tail of the tour does not fit. `dump_day_jobs.py` copied the `units` list straight
out of `cover.plan`, which is the DAWN PREDICTION: `_arrivals` guesses where each hire will spawn,
because `_end_of_day` discharges the whole crew (`kaggriculture.py:867`) and every hand is a fresh
`_spawn_hand` each morning.

The prediction is wrong whenever the farmer's own tour walks it off `(4,4)` before the hires settle --
hires settle in the MARKET phase, which runs AFTER the unit phase (`:922` then `:928`) -- so the ring
reads one slot emptier than predicted and every hand lands one slot early. Measured 2026-08-17, seed
11, `data/logs/start_tiles_d12_d29_2026-08-17.log`: 22 of 205 unit-days across the solved days d12-d29
are routed from a tile the unit did not wake on, and **d19 is the whole ring rotated by one, 11 of 13**.

d19 is therefore the day under test. `tests/test_a_hand_starts_the_day_on_the_tile_it_was_routed_from.py`
covers the underlying prediction defect and is XFAIL, because forcing the prediction true costs a game
turn and measured as a loss. This test is the other half: the SOLVER does not have to inherit the
prediction, because it runs offline and can be told what actually happened.
"""
import json
import pathlib
import subprocess
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
DAY, SEED, TPD = 19, 11, 24


@pytest.fixture(scope="module")
def observed():
    """`{unit_index: tile}` -- where each unit first appears on day 19, read off the live board."""
    pytest.importorskip("kaggle_environments")
    sys.path.insert(0, str(REPO / "scripts"))
    import importlib

    import breakdown as B
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    _saved_REPLAY_OPENING_DAYS = SA.REPLAY_OPENING_DAYS
    SA.REPLAY_OPENING_DAYS = ()

    replay, schedule, team = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay) or {}, seed=SEED, weedSpawnChance=0.0),
               debug=True)
    env.reset(2)
    me = SA.make_agent(thin, 0, router=True)
    them = B.tape_policy(replay, team, 1)
    first = {}
    for t in range((DAY + 1) * TPD):
        env.state[0].observation.town["unlocked_shops"] = list(shops(t))
        obs = env.state[0].observation
        farm = obs["farms"][0]
        if t // TPD == DAY:
            for u, p in enumerate([farm.get("farmer")] + list(farm.get("hands") or [])):
                if p is not None:
                    first.setdefault(u, tuple(p))
        a0 = me(obs, t)
        n0 = len(farm.get("hands") or [])
        a1 = them(env.state[1].observation, t)
        n1 = len(obs["farms"][1].get("hands") or [])
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                   "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                   "market": a1["market"]}])
        if env.state[0].status == "DONE":
            break
    try:
        yield first
    finally:
        SA.REPLAY_OPENING_DAYS = _saved_REPLAY_OPENING_DAYS



@pytest.fixture(scope="module")
def fixture_units(tmp_path_factory):
    """The `units` list `dump_day_jobs.py` writes for day 19, via the real script."""
    out = tmp_path_factory.mktemp("fx") / "day_19_probe.json"
    r = subprocess.run([sys.executable, "-u", "scripts/dump_day_jobs.py", "--day", str(DAY),
                        "--tape", "kawashigi", "--seed", str(SEED), "--weeds", "0.0",
                        "--arm", "melon", "--out", str(out)],
                       cwd=REPO, capture_output=True, text=True,
                       env={"PYTHONPATH": ".", "PATH": "/usr/bin:/bin:/usr/local/bin"})
    assert out.exists(), f"dump failed\nSTDOUT\n{r.stdout}\nSTDERR\n{r.stderr}"
    return [tuple(u) for u in json.loads(out.read_text())["units"]]


def test_the_solver_is_given_the_tile_each_unit_wakes_on(fixture_units, observed):
    """Every unit in the fixture starts where it woke. This is what the solver prices tours from."""
    wrong = [(u, fixture_units[u], observed[u]) for u in range(len(fixture_units))
             if u in observed and tuple(observed[u]) != tuple(fixture_units[u])]
    assert not wrong, "the solver is routing from tiles the units do not wake on:\n" + "\n".join(
        f"  u{u}: fixture {f}, woke on {a}" for u, f, a in wrong)


def test_day_nineteen_really_does_mispredict_so_the_test_above_is_not_vacuous(observed):
    """The ring rotates by one on d19. If this ever goes green the day under test must change."""
    ring = {(4, 4), (5, 4), (4, 5), (5, 5)}
    on_ring = [u for u, t in observed.items() if tuple(t) in ring]
    assert len(on_ring) >= 10, (
        f"only {len(on_ring)} of {len(observed)} units woke on the spawn ring; d19 was chosen "
        "because nearly every unit is a fresh hire there")
