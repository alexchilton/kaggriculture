"""The `seeds` row is a PURCHASE total, so it nets against seed bought today -- never against sowing.

`SEED_ROW_IS_A_FLOOR` floors the day's seed offer at the row, and nets the floor down as the ground
is sown:

    done = state["planted"][c] - state["planted_dawn"][c]
    emit_seed[c] = max(int(emit_seed.get(c, 0)), max(0, int(q) - done))

That assumes every planting spends a seed bought today. It does not. Seed lives in
`private["seeds"]` and carries between days at no capacity cost -- the comment three lines above
this one says exactly that about Victor's d6, which buys four and plants one.

d7 is where it bites. The row is `seeds {WHEAT 3, STRAWBERRY 9}` = 12 against **14** plants, and
the dawn store already holds `{WHEAT 1, STRAWBERRY 2}`. Two of those fourteen plantings are paid
for by the carry, so netting the row against plantings drops the strawberry floor from 9 to 8 as
soon as the day is two plants in. We buy 11, he buys 12:

    d7 dawn   ours {WHEAT 1, STRAWBERRY 2}   tape {WHEAT 1, STRAWBERRY 2}
    d7 dusk   ours {}                        tape {STRAWBERRY 1}

`plant 14/14` and `strawb 18/18` both match, which is why this read as benign. It is not. That one
seed then sits untouched:

    d8 dusk   ours {}  tape {STRAWBERRY 1}
    d9 dusk   ours {}  tape {STRAWBERRY 1}
    d10 dusk  ours {WHEAT 1, STRAWBERRY 5, MELON 2}  tape {WHEAT 1, STRAWBERRY 6, MELON 2}

and on d11 it is a planting: `buy_seed 3/4`, `plant 9/11`, and `water 38/41` because each of those
two plants owes a water. The d11 board is otherwise identical to his -- 56 planted tiles, the same
18 on the brink, the same 7 empty squares, the same bank.

The right quantity to net against is seed BOUGHT today, which is exact and needs no new tally:

    bought_today = seeds_now + planted_today - seeds_at_dawn
"""
import collections
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
#: The day the row is smaller than the plantings it funds, because two are paid for by the carry.
FOCUS_DAY = 7


def _store_at_dusk(day):
    """Seed still in `private['seeds']` on the last turn of `day`, ours and the tape's."""
    from kaggle_environments import make

    import breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent")
    replay, schedule, team = B.TAPES["victor"]
    raw = json.loads(pathlib.Path(schedule).read_text())
    thin = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
            for k, r in raw.items()}
    economy = B.env_config(replay)

    def play(make_me):
        env = make("kaggriculture", configuration=dict(economy, seed=11, weedSpawnChance=0.0),
                   debug=True)
        env.reset(2)
        me, opp = make_me(), B.tape_policy(replay, team, 1)
        out = {}
        for t in range(TPD * (day + 1)):
            o0, o1 = env.state[0].observation, env.state[1].observation
            a0, a1 = me(o0, t), opp(o1, t)
            if t == TPD * day + TPD - 1:
                out = {k: int(v) for k, v in (o0["private"].get("seeds") or {}).items() if int(v)}
            n0 = len(o0["farms"][0].get("hands") or [])
            n1 = len(o0["farms"][1].get("hands") or [])
            env.step([{"farmer": a0["farmer"], "hands": list(a0["hands"])[:n0],
                       "market": a0["market"]},
                      {"farmer": a1["farmer"], "hands": list(a1["hands"])[:n1],
                       "market": a1["market"]}])
        return out

    mine = play(lambda: (lambda a: (lambda o, t: a(o)))(SA.make_agent(thin, 0, router=True)))
    his = play(lambda: B.tape_policy(replay, team, 0))
    return mine, his


def test_the_premise_the_row_is_smaller_than_the_plantings_it_funds():
    """If d7's row ever covers its own plantings this test is measuring nothing. Fail loudly."""
    sched = json.loads((REPO / "data/seed_scripts/victor/schedule.json").read_text())
    row = sched[str(FOCUS_DAY)]
    bought = sum(int(q) for q in (row.get("seeds") or {}).values())
    sown = len(row.get("plants") or [])
    assert bought < sown, (
        f"d{FOCUS_DAY} buys {bought} seed and plants {sown}; the carry this test is about is gone "
        f"and its premise is stale.")


def test_the_carry_survives_the_day_that_spends_around_it():
    mine, his = _store_at_dusk(FOCUS_DAY)
    assert mine == his, (
        f"d{FOCUS_DAY} ends holding {mine or '{}'} against the tape's {his}. The seed row is a "
        f"PURCHASE total and `SEED_ROW_IS_A_FLOOR` nets it against plantings, so the two plantings "
        f"funded by the seed carried in from d6 also cancel two units off the day's buy. The seed "
        f"is not spent by d10 and costs a planting on d11.")
