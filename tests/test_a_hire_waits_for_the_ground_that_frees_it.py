"""On a day that buys a parcel, no hand is spawned onto a square that parcel is about to open.

`_spawn_hand` takes the least-occupied shed-access tile, so with four hires at dawn the ring
`(4,4) (5,4) (4,5) (5,5)` fills completely. While the farm owns NW alone, `(5,5)` is the only one of
the four with no unlocked orthogonal neighbour -- `(4,5)` is SW and `(5,4)` is NE, both locked -- so
the hand that lands there cannot move all day.

That is not automatically a defect. On d0 the tape strands a hand on `(5,5)` too, and d0 matches op
for op: a walled hand still spawns ON a shed-access tile, and PICKUP and DROP test shed-adjacency
only, so it loads and unloads all day. `HIRE_FIRST`'s own comment says exactly this, and refusing
the hire outright was measured at -17 hand-turns a day.

d6 is the case the comment does not cover: the square is walled **at dawn and not for the rest of
the day**. The schedule buys a parcel, that parcel is NE, and NE is `(5,5)`'s way out. Victor plays
it explicitly -- his d6 orders are `HIRE` at h0, h0, h0 and then `HIRE` at **h17**, one hour after
his `BUY_LAND` at h16. Three hands at dawn, the fourth once the ground exists.

We send the whole `hands` row at hour 0 (`HIRE_PINNED_DAYS` covers all thirty days), so the fourth
hand lands on `(5,5)` and PASSes twenty-four times. Its dawn route is four WATERs and the day's only
PLANT:

    u3: (3,2)[WATER] -> (0,2)[WATER] -> (0,3)[WATER] -> (2,3)[WATER] -> (5,3)[PLANT]

None of it runs. `water 7/12`, `plant 0/1`, and two melon tiles weed out for want of a drink, since
two consecutive unwatered days turn an ongoing crop into a WEED (`kaggriculture.py:771`).

The assertion is scoped to days the quadrant set actually GREW, which is what keeps d0 -- where the
stranding is real, permanent, and correct -- out of it.
"""
import collections
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))

SEED = 11
DAYS = 12
TPD = 24


@pytest.fixture(scope="module")
def played():
    """`{day: ({unit: [op, ...]}, quadrants_gained)}` for our seat over d0-d11."""
    import breakdown as B
    from kaggle_environments import make
    import kagg.search.schedule_agent as sa

    replay, schedule, team = B.TAPES["victor"]
    sched = {int(k): v for k, v in json.loads((REPO / schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}

    cfg = dict(B.env_config(REPO / replay), seed=SEED, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    agent = sa.make_agent(thin, 0, router=True)
    tape = B.tape_policy(REPO / replay, team, 1)

    acts = collections.defaultdict(lambda: collections.defaultdict(list))
    at_dawn, at_dusk = {}, {}
    for t in range(TPD * DAYS):
        day = t // TPD
        o0, o1 = env.state[0].observation, env.state[1].observation
        farm = o0["farms"][0]
        quads = set(farm.get("unlocked_quadrants") or ["NW"])
        if t % TPD == 0:
            at_dawn[day] = set(quads)
        at_dusk[day] = set(quads)
        a0, a1 = agent(o0), tape(o1, t)
        n0 = len(farm.get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        for u, a in enumerate([a0["farmer"]] + list(a0["hands"] or [])[:n0]):
            acts[day][u].append(a[0] if a else "-")
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return {d: (dict(acts[d]), at_dusk[d] - at_dawn[d]) for d in at_dawn}


def test_the_premise_a_parcel_arrives_mid_day_in_range(played):
    """Guard. Without a land day in range the assertion below is vacuous."""
    days = [d for d, (_a, gained) in played.items() if gained]
    assert days, f"no quadrant was bought in d0-d{DAYS - 1}; nothing to assert"


@pytest.mark.parametrize("day", range(DAYS))
def test_no_hand_is_stranded_on_a_day_that_buys_its_way_out(played, day):
    """A hand walled in at dawn is fine only if it stays walled. Today's parcel is its way out."""
    acts, gained = played[day]
    if not gained:
        pytest.skip(f"d{day} bought no land; a stranded hand there is permanent, not premature")
    idle = [u for u, ops in sorted(acts.items()) if ops and set(ops) <= {"PASS", "-"}]
    assert not idle, (
        f"d{day} bought {sorted(gained)} and units {idle} spent all {TPD} turns passing. "
        "A hand spawned on (5,5) while NW is the only quadrant cannot move until the parcel "
        "unlocks NE -- the tape hires that hand AFTER its BUY_LAND, we hire it at dawn.")
