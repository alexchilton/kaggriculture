"""The dumbest possible market: sell whatever is in the shed. Does it beat the planner's own?

    python -u scripts/what_if_we_just_sell_everything_that_hits_the_shed.py --seeds 3

ALEX'S TEST
-----------
*"the selling in its worst or easiest form is simply sell anything hitting the shed - try that to
test"*

This is the floor for the market half. If a rule with no state, no prices and no timing gets close
to the planner, then market timing is worth little and the cloned head is chasing a small prize. If
it is far worse, the planner's sell logic is carrying real value and any replacement has to earn it.

THREE ARMS, and the difference between the last two is the whole point:

  planner            untouched. The baseline everything is measured against.
  naive, ADDED       the planner's own orders are KEPT and the naive sells replace only its SELL
                     lines. Hires, land, seed and feed purchases still go out, so the planner's
                     economy and its internal ledgers stay intact.
  naive, REPLACED    `mine["market"] = naive`, which is what the hybrid harness does. Kept as a
                     control because it should be catastrophic for a reason that has nothing to do
                     with selling: it deletes HIRE, BUY_LAND, BUY_SEED and the feed buys, and the
                     planner has *already booked* those orders in its ledgers
                     (`schedule_agent.py:5115, :5434`). If this arm collapses and the added arm does
                     not, the earlier $20 hybrid table was measuring the harness, not the net.

THE FEED RESERVE
----------------
Animals eat WHEAT. The planner holds back `feed_days(day) * hungry` (`schedule_agent.py:1855`) for
exactly that, and a rule that sells the shed bare starves the herd two days later -- Alex's own
point about trades the ops cannot back up. So the naive rule is run at two reserves: 0, which is the
literal "sell anything hitting the shed", and a held-back wheat float.
"""
import argparse
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

MAX_ORDERS = 10          # the environment accepts ten a turn and silently drops the rest


def idle(_obs):
    return {"farmer": ["PASS"], "hands": [], "market": []}


def feed_reserve(obs, seat, day):
    """The planner's OWN reserve: `feed_days(day) * hungry` (`schedule_agent.py:1855`).

    `keep_wheat = 20` was a number I invented. This is the rule the planner protects its own sell
    row with, so the naive arm and the planner cannot disagree about how much wheat is not for sale.
    `hungry` counts animals not yet fed today, exactly as the planner counts them.
    """
    from kagg.search.schedule_agent import feed_days

    farm = ((obs.get("farms") or [])[seat]) or {}
    hungry = sum(1 for r in (farm.get("tiles") or []) for c in r
                 if isinstance(c, dict) and "animal" in c and not c.get("fed_today"))
    return feed_days(day) * hungry


def naive_sells(obs, seat, keep_wheat):
    """`SELL` every unit in the shed, less a wheat float. No prices, no timing, no state."""
    shed = dict((obs.get("private") or {}).get("shed") or {})
    out = []
    for item, n in sorted(shed.items()):
        n = int(n or 0)
        if item == "WHEAT":
            n = max(0, n - keep_wheat)
        if n > 0:
            out.append(["SELL", item, n])
    return out


def play(seat_cfg, turns, mode, keep_wheat, sell_hour=None, dump_from=None):
    from kaggle_environments import make

    from kagg.il.tape_teacher import TapeTeacher

    env = make("kaggriculture", configuration=seat_cfg, debug=False)
    env.reset(2)
    me = TapeTeacher(0)
    sold_turns = 0
    for t in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        n_units = 1 + len(obs["farms"][0].get("hands") or [])
        mine = me.sendable(me.act(obs), n_units)

        if mode != "planner":
            # `sell_hour` posts once a day instead of every turn. A sell is a standing offer that
            # fills a unit at a time and is re-posted free, so "every turn" and "once at hour H" are
            # different rates, not the same order placed differently -- and posting late leaves
            # fewer turns before the bell for it to clear.
            day = t // 24
            # **The terminal dump.** Past the last yield an animal cannot pay for its feed and a
            # crop cannot ripen, so the reserve is dead capital and the shed is worth only what it
            # sells for. From `dump_from` the reserve goes to zero and the rule sells every turn
            # rather than once a day -- fills are one unit per turn, so the last days need the rate.
            # **ONE delta.** The first version of this released the reserve AND switched to selling
            # every turn from `dump_from`, so its small loss could not be attributed -- and selling
            # every turn is separately worth -$71k, which would swamp anything the release bought.
            # The cadence is now untouched: `dump_from` releases the reserve and nothing else.
            dumping = dump_from is not None and day >= dump_from
            keep = (0 if dumping
                    else feed_reserve(obs, 0, day) if keep_wheat == "feed_rule" else keep_wheat)
            quiet = (sell_hour is not None and t % 24 != sell_hour)
            naive = [] if quiet else naive_sells(obs, 0, keep)
            if mode == "added":
                # Keep everything the planner asked for EXCEPT its own SELLs, then add ours.
                others = [o for o in (mine.get("market") or []) if not (o and o[0] == "SELL")]
                mine["market"] = (naive + others)[:MAX_ORDERS]
            else:                                   # "replaced" -- what the hybrid harness does
                mine["market"] = naive[:MAX_ORDERS]
            sold_turns += 1 if naive else 0

        env.step([mine, idle(env.state[1].observation)])
    return float(env.state[0].observation["farms"][0]["money"]), sold_turns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--base-seed", type=int, default=9000)
    ap.add_argument("--turns", type=int, default=719)
    ap.add_argument("--dump-from", type=int, default=28,
                    help="from this day: reserve 0 and sell every turn, not once a day")
    ap.add_argument("--sell-hour", type=int, default=16,
                    help="post the sell once a day at this hour instead of every turn")
    ap.add_argument("--keep-wheat", type=int, default=20,
                    help="wheat held back for feed in the reserved arm")
    args = ap.parse_args()

    from kagg.search import schedule_agent as SA

    # The planner arm, not the tape: `REPLAY_OPENING_DAYS` ships as every day, which would replay
    # カワシギ's recorded ops onto a fresh seed regardless of the board.
    SA.REPLAY_OPENING_DAYS = ()

    seeds = [args.base_seed + 137 * i for i in range(args.seeds)]
    k = args.keep_wheat
    h = args.sell_hour
    d = args.dump_from
    arms = [("planner", "planner", 0, None, None),
            (f"h{h}, keep {k}", "added", k, h, None),
            (f"h{h}, keep {k}, dump d{d}", "added", k, h, d),
            (f"h{h}, keep {k}, dump d26", "added", k, h, 26)]

    print(f"{args.seeds} seeds, {args.turns} turns, idle opponent, planner replay OFF")
    print(f"selling is unconditional: every unit in the shed, every turn\n")
    head = f"  {'seed':>8}" + "".join(f"{name:>26}" for name, _m, _k, _h, _d in arms)
    print(head)

    banks = {name: [] for name, _m, _k, _h, _d in arms}
    for s in seeds:
        row = f"  {s:>8}"
        for name, mode, keep, hour, dump in arms:
            bank, _n = play({"seed": int(s)}, args.turns, mode, keep, hour, dump)
            banks[name].append(bank)
            row += f"{bank:>26,.0f}"
        print(row, flush=True)

    print(f"\n  {'median':>8}" + "".join(
        f"{statistics.median(banks[name]):>26,.0f}" for name, _m, _k, _h, _d in arms))

    base = statistics.median(banks["planner"])
    print("\nREAD IT LIKE THIS")
    print(f"  planner median is {base:,.0f}")
    print("  an ADDED arm near or above it   naive selling is enough; market timing is a small")
    print("                                  prize and the cloned head is chasing very little.")
    print("  an ADDED arm far below it       the planner's sell logic carries real value.")
    print("  REPLACED far below ADDED        the hybrid harness, not the market, was the problem.")


main()
