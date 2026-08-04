"""Can we replicate the winner -- actions, money, squares -- day by day?

Alex's standard, and the only one that answers the question: not "how close is the total", but for each
day, do we emit their actions, hold their money, and own their squares. A day that diverges is the day
the answer is no, and everything after it is downstream of that day.

Two panels, because they answer different questions and conflating them is how "0/720 turns match" got
reported as an impossibility:

**ACTIONS -- teacher-forced.** Our `decide` is fed the replay's own observation each turn, so nothing
compounds: turn 137 is judged against the exact board the winner faced on turn 137. This isolates
"can the plan produce their action", with no drift. Money is *theirs* by construction here, so it is
not compared in this panel.

Market orders are compared as a merged multiset per `(op, item)`, which is what the simulator itself
does: `tests/test_split_sell_orders.py` measures that any partition of a quantity banks identically
($0 delta uncontested, +/-$2 zero-sum contested), because `_refresh_prices` is a pure function of
inventory and the per-unit quote recomputes off live inventory. Comparing raw order lists instead
scores `SELL WHEAT 1/3/1` against `SELL WHEAT 5` as four disagreements when the answer is none.

**MONEY AND SQUARES -- free-running.** The plan plays its own season from the $3,000 stake. This is
the panel that can go wrong cumulatively, and it is the one that says whether the encoded plan *is*
the winner rather than merely agreeing with it turn by turn.

    PYTHONPATH=. python3 -u scripts/replicate_by_day.py 2>&1 | tee data/logs/replicate_by_day.log
"""

import argparse
import collections
import json

import numpy as np

from kagg.search import agent as A
from kagg.search import executor as X
from kagg.search import library, plan as P, replay_plan as RP, rollout
from kagg.sim.game import Actions, Game
from kagg.sim.tiles import COOP, PASTURE

TURNS_PER_DAY = 24


def _market(orders):
    """{(op, item): total_qty}, merging repeats -- see the module docstring."""
    out = collections.Counter()
    for o in orders or []:
        if not isinstance(o, list) or not o:
            continue
        if o[0] in ("HIRE", "BUY_LAND"):
            out[(o[0], None)] += 1
        elif len(o) >= 3:
            try:
                n = int(o[2])
            except (TypeError, ValueError):
                continue
            if n > 0:
                out[(o[0], o[1])] += n
    return out


def _units(action):
    return collections.Counter(
        tuple(u) for u in [action.get("farmer")] + list(action.get("hands") or []) if u)


def actions_by_day(episode, seat, plan):
    """Teacher-forced: per day, how many turns agree on market orders and on unit ops."""
    steps = json.loads(open(episode).read())["steps"]
    rows = collections.defaultdict(lambda: dict(turns=0, market=0, units=0, both=0,
                                                qty_off=0, op_off=0))
    for t, step in enumerate(steps):
        cell = step[seat]
        obs, theirs = cell.get("observation"), cell.get("action")
        if not isinstance(theirs, dict) or not obs or "farms" not in obs:
            continue
        obs = dict(obs)
        obs.setdefault("player", seat)
        view = A.observation_view(obs)
        ours = A.to_action(obs, X.decide(view, plan), int(view.n_units[0]))

        tm, om = _market(theirs.get("market")), _market(ours["market"])
        tu, ou = _units(theirs), _units(ours)
        r = rows[t // TURNS_PER_DAY]
        r["turns"] += 1
        r["market"] += int(tm == om)
        r["units"] += int(tu == ou)
        r["both"] += int(tm == om and tu == ou)
        r["qty_off"] += sum(abs(om[k] - tm[k]) for k in set(om) | set(tm))
        r["op_off"] += sum(abs(ou[k] - tu[k]) for k in set(ou) | set(tu))
    return rows


def free_run(plan, days, seed=0):
    """Play the encoded plan from the stake, recording money and squares at each day's noon.

    Noon, not hour 23: the dawn reset fires inside the hour-23 step, dismissing every hand, so a row
    sampled after it reports a crew of 1 every day regardless of hiring.
    """
    opp = P.decode(library.opposition()).take([0])
    schedule = rollout.sample_unlock_schedule(np.random.default_rng(seed))
    game = Game(1, rng=np.random.default_rng(seed), unlock_schedule=schedule)
    actions = Actions(1)
    rows = {}
    for step in range(days * TURNS_PER_DAY):
        day, hour = divmod(step, TURNS_PER_DAY)
        for player, pl in ((0, plan), (1, opp)):
            view = rollout.build_view(game, player, day, hour)
            rollout._write(actions, player, X.decide(view, pl))
        if game.step(actions):
            break
        if hour == 12:
            tiles, farm = game.tiles[0], game.farms[0]
            rows[day] = dict(
                money=float(farm.money[0]),
                crew=int(farm.n_units[0]),
                pens=int(((tiles.kind[0] == PASTURE) | (tiles.kind[0] == COOP)).sum()),
                crops=int((tiles.crop[0] >= 0).sum()),
                animals=int((tiles.animal[0] >= 0).sum()),
            )
    return rows


def their_money_by_day(episode, seat):
    steps = json.loads(open(episode).read())["steps"]
    out = {}
    for t, step in enumerate(steps):
        obs = step[seat].get("observation") or step[0].get("observation")
        farms = (obs or {}).get("farms")
        if farms and seat < len(farms):
            out[t // TURNS_PER_DAY] = float(farms[seat]["money"])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", default="data/episodes/89873723.json")
    ap.add_argument("--seat", type=int, default=0)
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()

    layout = RP.layout_from_replay(a.episode, seat=a.seat)
    plan = P.decode(RP.genome_from_layout(layout)[None])
    acts = actions_by_day(a.episode, a.seat, plan)
    mine = free_run(plan, a.days)
    theirs = their_money_by_day(a.episode, a.seat)
    their_pens = layout.n_pasture + layout.n_coop
    their_crops = len(layout.crops)

    print(f"{a.episode} seat {a.seat}: ${layout.money:,.0f}   "
          f"squares: {their_pens} pens, {their_crops} crops\n")
    print(f"{'':>3} | {'ACTIONS (teacher-forced)':^34} | {'MONEY (free-run)':^26} | "
          f"{'SQUARES (free-run)':^20}")
    print(f"{'day':>3} | {'both':>6} {'mkt':>6} {'unit':>6} {'qty off':>7} {'op off':>6} | "
          f"{'ours':>11} {'theirs':>11} | {'pens':>5} {'crops':>6} {'herd':>5}")
    print("=" * 108)
    first_bad = None
    for d in range(a.days):
        r = acts.get(d)
        m = mine.get(d)
        if r is None and m is None:
            continue
        n = (r or {}).get("turns", 0) or 1
        both = (r or {}).get("both", 0)
        if first_bad is None and both < n:
            first_bad = d
        print(f"{d:>3} | {both:>3}/{n:<2} {(r or {}).get('market', 0):>3}/{n:<2} "
              f"{(r or {}).get('units', 0):>3}/{n:<2} {(r or {}).get('qty_off', 0):>7} "
              f"{(r or {}).get('op_off', 0):>6} | "
              f"{(m or {}).get('money', float('nan')):>11,.0f} "
              f"{theirs.get(d, float('nan')):>11,.0f} | "
              f"{(m or {}).get('pens', 0):>5} {(m or {}).get('crops', 0):>6} "
              f"{(m or {}).get('animals', 0):>5}")
    print("=" * 108)

    total = sum(r["turns"] for r in acts.values())
    exact = sum(r["both"] for r in acts.values())
    print(f"turn-exact actions : {exact}/{total} ({exact / max(total, 1):.1%})")
    print(f"first day not turn-exact : {first_bad}")
    last = max(mine) if mine else None
    if last is not None:
        print(f"free-run day {last}: ours ${mine[last]['money']:,.0f} vs theirs "
              f"${theirs.get(last, 0):,.0f}   "
              f"pens {mine[last]['pens']}/{their_pens}  crops {mine[last]['crops']}/{their_crops}")


if __name__ == "__main__":
    raise SystemExit(main())
