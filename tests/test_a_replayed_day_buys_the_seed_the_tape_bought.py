"""On a replayed day the seed order is the tape's, because ours costs a hand.

Measured 2026-08-24 on 92441493, seed 911634571, replaying its own melon tape. d4-d7 match his
recording on every one of 96 turns. Then:

    d8 h0   his   SELL FERT 6, HIRE x5, BUY_PRODUCT WHEAT 9, BUY_SEED WHEAT 3
            ours  SELL FERT 6, HIRE x5, BUY_PRODUCT WHEAT 9, BUY_SEED STRAWBERRY 1

    d8 h1   his bank $198   ours bank $129        both send HIRE x5
    d8 h2   his 10 hands    ours 9 hands

Hires 6-10 cost `8+13+21+34+55 = $131` on the fib ladder (`kaggriculture.py:698`). He holds $198 and
lands all five; we hold $129, two dollars short, and the tenth is refused silently. One
`BUY_SEED STRAWBERRY 1` in place of his `BUY_SEED WHEAT 3` is $69, spent one hour before a $131
hire block.

The lost hand costs a HARVEST, a COLLECT_FERTILIZER, a WATER and two PLANTs on d8, and the board
first differs at d8 in eight games for exactly this reason. We finish d8 with $572 against his $485
-- richer by the $89 hire we never paid for.

`schedule_agent.py:5458` kept the buys ours so the melon/strawberry arm could be EXPRESSED as
purchases on replayed days. That reason predates `REPLAY_OPENING_TAPE` being keyed on
`(melon_armed, q4_armed)`: the tape now IS the armed season's own recording, so its seed orders are
already that arm's seed orders. The animal re-label stays ours -- the herd split is a shop-draw
decision the tape cannot know.
"""

import collections
import glob
import json
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
WHO = "カワシギ"
TPD = 24
EP = "92441493"
DAY = 8


def _file():
    for d in ("kawashigi", "kawashigi_b3", "kawa_2026-08-24", "top_guys", "ladder"):
        hit = glob.glob(str(REPO / f"data/seed_scripts/{d}/{EP}.json"))
        if hit:
            return hit[0]
    return None


def _seed_orders():
    sys.path.insert(0, str(REPO))
    sys.path.insert(0, str(REPO / "scripts"))
    from kaggle_environments import make
    import breakdown as B
    import us_in_his_seat as U
    from kagg.search import schedule_agent as SA

    rec = json.loads(pathlib.Path(_file()).read_text())
    names = rec["info"]["TeamNames"]
    seat = names.index(WHO)
    seed = rec["info"]["seed"]
    steps = rec["steps"]
    them = 1 - seat

    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, seat)

    # **Per TURN, not per day.** The daily totals already agree -- STRAWBERRY 11 and WHEAT 3 in
    # both arms -- so a per-day comparison passes while the defect is untouched. What differs is
    # WHICH HOUR the money leaves, and the hour is what collides with the hire ladder.
    ours, his = {}, {}
    hands = None
    for t in range((DAY + 1) * TPD):
        o = env.state[seat].observation
        n_us = len(o["farms"][seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        rec_a = U._recorded(steps, t, seat)
        if t // TPD == DAY:
            for src, tally in ((mine.get("market") or [], ours),
                               (rec_a.get("market") or [], his)):
                seeds = collections.Counter()
                for od in src:
                    if od and od[0] == "BUY_SEED" and len(od) >= 3:
                        seeds[od[1]] += int(od[2])
                if seeds:
                    tally[t % TPD] = dict(seeds)
            if t % TPD == TPD - 1:
                hands = (n_us, len(steps[t][seat]["observation"]["farms"][seat]["hands"] or []))
        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])
        if env.done:
            break
    return ours, his, hands


@pytest.mark.skipif(_file() is None, reason=f"{EP} not on disk")
def test_a_replayed_day_buys_the_seed_the_tape_bought():
    """d8 is replayed, so its BUY_SEED orders must be the tape's."""
    ours, his, hands = _seed_orders()
    assert ours == his, (
        f"{EP} d{DAY} is a replayed day but our seed orders land on different hours than the "
        f"tape's.\n  his  {his}\n  ours {ours}\n  crew at dusk ours/his {hands}"
    )
