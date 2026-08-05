"""End of each day: plants, animals, pens, money and shed inventory must equal the tape's.

Alex's test, and it is the right one. Everything else this project measures is a proxy -- op counts,
turn budgets, tape-cell fidelity, final bank. The tape records what the farm actually WAS at the end
of every day, and if our farm is the same farm on day N then it is the same farm, full stop.

Final money is deliberately NOT the criterion. It is downstream of thirty days of compounding, so a
run can bank more while being less like the tape, and a fix that makes day 1 exact can look like a
regression at day 29 because something on day 14 is still wrong. Judge the state, day by day, and the
bank follows.

Both sides are played in the real environment against the SAME opponent -- the other seat's own
recorded tape -- with the episode's own configuration, and with the weed spawner switched off so the
comparison is not decided by an RNG stream this project deliberately does not reproduce. Any WEED
tile that appears is then our own crop dying of thirst, which is information rather than noise.
"""

import collections
import json
import pathlib
import sys

import pytest

sys.path.insert(0, "scripts")

REPLAY = pathlib.Path("data/seed_scripts/new_leader/90016067.json")
SCHEDULE = pathlib.Path("data/seed_scripts/new_leader/schedule.json")
TEAM = "somewhere after"
TD = 24

pytestmark = pytest.mark.slow          # plays two whole seasons in the real environment


def _state(step):
    obs = (step[0] or {}).get("observation") or {}
    farms = obs.get("farms") or []
    priv = obs.get("private") or {}
    if not farms:
        return None
    farm = farms[0]
    kinds = collections.Counter()
    animals = 0
    for row in farm.get("tiles") or []:
        for cell in row:
            if isinstance(cell, dict):
                kinds[cell.get("kind", "?")] += 1
                if "animal" in cell:
                    animals += 1
            elif isinstance(cell, str):
                kinds[cell] += 1
    return dict(money=float(farm.get("money", 0)),
                plants=kinds["PLANT"],
                pens=kinds["PASTURE"] + kinds["COOP"],
                weeds=kinds["WEED"],
                animals=animals,
                shed=sum((priv.get("shed") or {}).values()))


@pytest.fixture(scope="module")
def seasons():
    if not REPLAY.exists() or not SCHEDULE.exists():
        pytest.skip("replay or schedule missing; run scripts/extract_tape.py first")
    from kaggle_environments import make

    import build_script_submission as B
    from kagg.search import dayplan

    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    other = 1 - seat
    cfg = {k: v for k, v in (d.get("configuration") or {}).items()
           if k not in ("actTimeout", "runTimeout")}
    cfg["weedSpawnChance"] = 0.0

    def recorded(s):
        # From steps[1:] -- steps[0].action is the reset placeholder and is never applied.
        out = []
        for st in d["steps"][1:]:
            act = (st[s] or {}).get("action") or {}
            out.append({"farmer": act.get("farmer") or ["PASS"],
                        "hands": list(act.get("hands") or []),
                        "market": list(act.get("market") or [])})
        return out

    def replayer(tp):
        def agent(obs, config=None):
            t = int(obs.get("step", 0) or 0)
            if t >= len(tp):
                return {"farmer": ["PASS"], "hands": [], "market": []}
            r = tp[t]
            farms = obs.get("farms") or []
            me = int(obs.get("player", 0) or 0)
            n = len(farms[me].get("hands", []) or []) if me < len(farms) else 0
            return {"farmer": r["farmer"], "hands": r["hands"][:n], "market": r["market"]}
        return agent

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, _report = dayplan.emit(sched)
    plan = B.build_plan(script.arrays())

    def emitted(obs, config=None):
        t = int(obs.get("step", 0) or 0)
        if t >= len(plan):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        f, h, m = plan[t]
        farms = obs.get("farms") or []
        me = int(obs.get("player", 0) or 0)
        n = len(farms[me].get("hands", []) or []) if me < len(farms) else 0
        return {"farmer": f, "hands": h[:n], "market": m}

    opponent = replayer(recorded(other))
    out = {}
    for label, agent in (("A", replayer(recorded(seat))), ("B", emitted)):
        env = make("kaggriculture", configuration=cfg, debug=False)
        res = env.run([agent, opponent])
        out[label] = {day: _state(res[min(day * TD, len(res) - 1)]) for day in range(30)}
    return out


@pytest.fixture(scope="module")
def orders():
    """`day -> Counter(order kind)` in units, for the tape and for what we emit."""
    import numpy as np

    from kagg.search import dayplan
    from kagg.search import routines as R

    d = json.loads(REPLAY.read_text())
    seat = d["info"]["TeamNames"].index(TEAM)
    a = collections.defaultdict(collections.Counter)
    for t, st in enumerate(d["steps"][1:]):
        act = (st[seat] or {}).get("action") or {}
        for o in (act.get("market") or []):
            if o:
                a[t // TD][o[0]] += int(o[2]) if len(o) > 2 else 1

    sched = {int(k): v for k, v in json.loads(SCHEDULE.read_text()).items()}
    script, _r = dayplan.emit(sched)
    arr = script.arrays()
    b = collections.defaultdict(collections.Counter)
    for t in range(arr["sell"].shape[0]):
        day = t // TD
        b[day]["SELL"] += int(arr["sell"][t].sum())
        b[day]["BUY_PRODUCT"] += int(arr["buy_product"][t].sum())
        b[day]["BUY_SEED"] += int(arr["buy_seed"][t].sum())
        b[day]["BUY_ANIMAL"] += int(arr["buy_animal"][t].sum())
        b[day]["HIRE"] += int(arr["hire"][t])
        b[day]["BUY_LAND"] += int(arr["buy_land"][t])
    return a, b


def _diff(seasons, field, upto):
    rows = []
    for day in range(1, upto + 1):
        a, b = seasons["A"].get(day), seasons["B"].get(day)
        if not a or not b:
            continue
        if a[field] != b[field]:
            rows.append(f"day {day}: {field} {b[field]} against the tape's {a[field]}")
    return rows


def test_the_pens_match_every_day(seasons):
    """Fixed by not building on locked shed tiles -- three of the four are in locked quadrants."""
    assert not _diff(seasons, "pens", 29), "\n  " + "\n  ".join(_diff(seasons, "pens", 29))


def test_the_animals_match_every_day(seasons):
    assert not _diff(seasons, "animals", 29), "\n  " + "\n  ".join(_diff(seasons, "animals", 29))


def test_the_planted_tiles_match_through_the_first_week(seasons):
    """Day 1 was 12 against the tape's 17 -- five PLANT ops emitted onto tiles a hand could not
    reach, because unit 3 spawns in SE and cannot move until two parcels are bought."""
    rows = _diff(seasons, "plants", 7)
    assert not rows, "\n  " + "\n  ".join(rows)


def test_no_tile_of_ours_dies_of_thirst(seasons):
    """The weed spawner is off, so every WEED here is one of our own crops that missed two
    waterings (`kaggriculture.py:752-753`) -- and a WEED makes PLANT a no-op, so the ground is
    dead for the season too."""
    ours = [f"day {d}: {seasons['B'][d]['weeds']} weeds" for d in range(1, 30)
            if seasons["B"].get(d) and seasons["B"][d]["weeds"]]
    assert not ours, "crops dying of thirst with the spawner disabled:\n  " + "\n  ".join(ours[:10])


def test_the_shed_matches_through_the_first_week(seasons):
    rows = _diff(seasons, "shed", 7)
    assert not rows, "\n  " + "\n  ".join(rows)


def test_what_we_buy_and_sell_matches_day_by_day(seasons, orders):
    """Alex's addition, and it belongs here rather than in the op census.

    `scripts/tape_match.py` already shows every market TOTAL is exact -- SELL 4427, BUY_PRODUCT 967,
    HIRE 306, BUY_SEED 131, BUY_ANIMAL 14, BUY_LAND 2. That is not the same as trading the same way:
    the same 967 units of wheat bought on the wrong days is a different farm, because the town's price
    walks with its inventory and a purchase made before the sale that funds it simply no-ops.
    """
    a, b = orders
    rows = []
    for day in range(0, 30):
        for kind in ("SELL", "BUY_PRODUCT", "BUY_SEED", "BUY_ANIMAL", "HIRE", "BUY_LAND"):
            av, bv = a[day][kind], b[day][kind]
            if av != bv:
                rows.append(f"day {day}: {kind} {bv} against the tape's {av}")
    assert not rows, f"{len(rows)} days differ:\n  " + "\n  ".join(rows[:15])


def test_the_money_matches_through_the_first_week(seasons):
    """Last, because it is the sum of everything above. Day 1 was $156 against the tape's $42 --
    not a surplus, $114 of investment that never happened."""
    rows = _diff(seasons, "money", 7)
    assert not rows, "\n  " + "\n  ".join(rows)
