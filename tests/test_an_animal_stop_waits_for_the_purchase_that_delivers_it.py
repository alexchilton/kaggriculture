"""A draw for an animal the row buys TODAY is deferred until the purchase lands, not binned.

The last hole in day 8. The plan is right and the route is right -- `cover` hands u9 the job

    (5,3)  ['PLACE', 'FEED', 'CARE']   needs={'SHEEP': 1, 'WHEAT': 1}

and materialises it behind `Shed(5,4)[SHEEPx1+WHEATx1]`. `PLAN_TODAYS_PURCHASES` credits the shed
with the animal at dawn, so the plan is built against a shed that HAS the sheep. It does not have it
yet: the unit phase runs before `_process_market` (`kaggriculture.py:922` then `:928`), the row buys
`SHEEP 1` at h05, and the shed reads

    h00-h05  SHEEP 0        h06 onward  SHEEP 1

The hand reaches the shed inside that window, `take = min(want, shed)` is 0, and because the two
rescues in that branch are both `hour == 0` only, the want is deleted outright. No unit ever emits
`PICKUP SHEEP`, so the PLACE never fires, the pen at (5,3) stays empty, and the feed and care that
travel with it are lost too -- `place 0/3`, `animals 9/10`, `feed 9/10`, `care 9/10`.

The tape does the same purchase and simply does not arrive early:

    h05  BUY_ANIMAL SHEEP 1     h06  u3 PICKUP/SHEEP     h09  u3 PLACE/SHEEP

An animal is the one draw where deferring is unambiguously safe, which is why this is narrower than
the all-day carry-forward that lost d3 and d7. Wheat is contested -- a short shed at h13 means
another hand drew it first, and waiting steals the ration from a pen that already has it. A bought
animal is contested by nobody: at h05 there is no sheep in the world, one beast is bought for one
named pen, and lifting it from the shed takes nothing from anyone.

It goes to the BACK of the tour rather than being held under foot, for the same reason
`HOLD_A_PLANT_STOP_UNTIL_ITS_SEED_ARRIVES` does: the hand has other work, and the two arms that made
a hand stand and wait past hour 0 both lost the d6 land parcel.

See `THE_ANIMAL_WAITS_FOR_THE_PURCHASE_THAT_DELIVERS_IT`.
"""
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

DAY, SEED, TPD = 8, 11, 24


def _run():
    from kaggle_environments import make

    import breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent_1455mh")
    replay, schedule, team = B.TAPES["kawashigi"]
    raw = json.loads(pathlib.Path(schedule).read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}
    shops = B.recorded_shops(replay)

    env = make("kaggriculture",
               configuration=dict(B.env_config(replay), seed=SEED, weedSpawnChance=0.0), debug=True)
    env.reset(2)
    agent = SA.make_agent(thin, 0, router=True)
    opp = B.tape_policy(replay, team, 1)

    acts, animals = [], 0
    for t in range(TPD * (DAY + 1)):
        o0, o1 = env.state[0].observation, env.state[1].observation
        o0.town["unlocked_shops"] = list(shops(t))
        a0, a1 = agent(o0), opp(o1, t)
        n0 = len(o0["farms"][0].get("hands") or [])
        n1 = len(o0["farms"][1].get("hands") or [])
        if t // TPD == DAY:
            for h in [a0["farmer"]] + list(a0["hands"])[:n0]:
                if h and h[0] in ("PICKUP", "PLACE") and "SHEEP" in [str(x) for x in h]:
                    acts.append((t % TPD, h[0]))
            if t % TPD == TPD - 1:
                animals = sum(1 for row in o0["farms"][0]["tiles"]
                              for c in row if isinstance(c, dict) and c.get("animal"))
        env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0], "market": a0["market"]},
                  {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1], "market": a1["market"]}])
    return acts, animals


def test_the_sheep_is_drawn_and_placed():
    """The row buys it at h05; the pen it was bought for must have it by dusk."""
    acts, animals = _run()
    kinds = {k for _h, k in acts}
    assert "PICKUP" in kinds, (
        f"no unit ever drew the SHEEP the row bought at h05 -- the draw was binned as a shortfall\n"
        f"  SHEEP actions on d{DAY}: {acts}")
    assert "PLACE" in kinds, (
        f"the SHEEP was drawn but never placed\n  SHEEP actions on d{DAY}: {acts}")
    assert animals == 10, (
        f"d{DAY} ends holding {animals} animals, not 10 -- the bought sheep is still in the shed\n"
        f"  SHEEP actions: {acts}")


def test_the_draw_does_not_beat_the_purchase():
    """It settles at the END of h05, so h06 is the earliest hour it can be lifted."""
    acts, _animals = _run()
    picks = [h for h, k in acts if k == "PICKUP"]
    assert picks and min(picks) >= 6, (
        f"drew the SHEEP at h{min(picks) if picks else '--'}, before the purchase settles at h05\n"
        f"  SHEEP actions on d{DAY}: {acts}")
