"""The hybrid Alex asked for: the planner routes the crew, the clone decides the trades.

    python -u scripts/the_planner_drives_and_the_net_supplies_the_market.py \
        --ckpt data/bc_runs/bcr_kawa-20260828-000741/latest.pkl --seeds 4

THE SPLIT, AND WHY THIS ONE
---------------------------
*"so if the quality of the results on the bc is still not so great can the planner feasibly handle
the problems? ... well and the market....but the market is linked then with the planner getting
things in on time"*

The clone's errors are not spread evenly, measured over 400 held-out カワシギ seats:

    MOVEMENT   71,516 acted turns   60.3%      wrong DIRECTION 81-86% of the time it moves at all
    WORK       54,204 acted turns   84.9%      HARVEST 48.3, FERTILIZE 27.6, DIG 6.1 -- all lose to
                                               WATER, which is 35% of work ops
    ALL ACTED 125,720               70.9%

Routing is what the planner is for and is the half the clone is worst at. The market is the half a
router has no view of. So each side supplies what it is good at, and the arms below say whether the
composition beats either alone.

WHAT EACH ARM CHANGES -- one sentence each, before the run, per CLAUDE.md
------------------------------------------------------------------------
  planner      `REPLAY_OPENING_DAYS = ()`, so the shipped agent plays its own planner and router
               on a seed it has never seen, and posts its own market orders. THE BASELINE.
               Measured 2026-08-28 over 6 fresh seeds: median $167,828, min $135,885, max $190,465.

  hybrid       identical unit ops -- same planner, same routes, same seed -- and `action["market"]`
               replaced by the clone's bundle decode. The ONLY delta is which orders go out.

  net          the clone playing everything, units included. Included because a hybrid that beats
               it is not thereby good; the number to beat is the planner. Known to bank $300 on
               seed 9000 (`data/logs/what_breaks_the_clone.log`).

For the hybrid to WIN, the clone's market head has to be better at pricing and timing than the
planner's own sell rule while looking at a board the planner produced. It has never seen that
board: it was fitted on カワシギ's, which his own routing produced. That is the risk in the arm and
it is why the diagnostic below counts trading turns as well as money.

**The epoch-6 checkpoint's market head is CONTAMINATED and its number is a lower bound.** It was
labelled through the 197-entry `bundle_vocab.json`, which cannot express 14.5% of this teacher's
traded turns -- 5,641 HIRE and 4,894 SELL orders taught as DO NOTHING
(`scripts/count_what_the_bc_vocab_could_not_say.py`). Re-run against the 256-entry
`bundle_vocab_kawa.json` checkpoint before drawing any conclusion about the ceiling.
"""
import argparse
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def idle(_obs):
    """A do-nothing opponent, so the market is uncontested and the arms differ only in themselves.

    The same opponent the planner baseline was measured against, which is the only reason the
    $167,828 median above is comparable to anything printed here.
    """
    return {"farmer": ["PASS"], "hands": [], "market": []}


def play(seed, turns, market_from=None, units_from_net=False, net=None, mode="replace"):
    """One season on `seed`. Returns `(bank, turns_the_market_was_used, turns_it_sent_orders)`.

    `market_from` is a callable `obs -> orders`, or None to keep the planner's own orders.
    """
    from kagg.il.tape_teacher import TapeTeacher
    from kaggle_environments import make

    env = make("kaggriculture", configuration={"seed": int(seed)}, debug=False)
    env.reset(2)
    me = TapeTeacher(0)
    asked = traded = 0
    for t in range(turns):
        if env.done:
            break
        obs = env.state[0].observation
        n_units = 1 + len(obs["farms"][0].get("hands") or [])
        if units_from_net:
            mine = net(obs)
        else:
            mine = me.sendable(me.act(obs), n_units)
            if market_from is not None:
                orders = market_from(obs)
                asked += 1
                traded += 1 if orders else 0
                if mode == "add":
                    # **ADD, do not replace.** Replacing deletes the planner's own HIRE, BUY_LAND,
                    # BUY_SEED, feed buys and SELLs -- and it has ALREADY booked them in its ledgers
                    # (`schedule_agent.py:5115, :5434`), so its world-model is falsified too.
                    # Measured 2026-08-28: replacing the market with an unconditional sell-everything
                    # rule banks exactly $3,000 on every seed, the untouched starting bank -- no seed
                    # bought, nothing planted, nothing harvested. That is the harness, not the net.
                    own = list(mine.get("market") or [])
                    mine["market"] = (own + [o for o in orders if o not in own])[:10]
                else:
                    mine["market"] = orders
        env.step([mine, idle(env.state[1].observation)])
    return float(env.state[0].observation["farms"][0]["money"]), asked, traded


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default="data/bc_runs/bcr_kawa-20260828-000741/latest.pkl")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--turns", type=int, default=719)
    ap.add_argument("--base-seed", type=int, default=9000)
    ap.add_argument("--market-mode", choices=("replace", "add"), default="replace",
                    help="add: keep the planner's own orders and append the net's")
    ap.add_argument("--skip-net-only", action="store_true",
                    help="drop the third arm; it is the slowest and its answer is already known")
    args = ap.parse_args()

    from kagg.agents import neural
    from kagg.search import schedule_agent as SA

    # **The replay is switched off in memory, for this process only.** `REPLAY_OPENING_DAYS` ships
    # as `tuple(range(30))` -- the agent sends カワシギ's RECORDED ops keyed on turn index and never
    # on the seed, so on a fresh board it is a fixed tape played into the wrong game. Leaving it on
    # would measure the tape, not the planner, and the planner is the thing being composed with.
    SA.REPLAY_OPENING_DAYS = ()

    net = neural.make_agent(args.ckpt)
    seeds = [args.base_seed + 137 * i for i in range(args.seeds)]

    print(f"ckpt   {args.ckpt}")
    print(f"{args.seeds} fresh seeds, {args.turns} turns, idle opponent, planner replay OFF\n")
    print(f"  {'seed':>10}{'planner':>13}{'hybrid':>13}{'delta':>12}{'net traded':>13}")

    rows = []
    for s in seeds:
        base, _a, _tr = play(s, args.turns)
        hyb, asked, traded = play(s, args.turns,
                                  market_from=lambda o: net(o)["market"], mode=args.market_mode)
        rows.append((s, base, hyb))
        print(f"  {s:>10}{base:>13,.0f}{hyb:>13,.0f}{hyb - base:>+12,.0f}"
              f"{traded:>8,}/{asked:,}", flush=True)

    b = [r[1] for r in rows]
    h = [r[2] for r in rows]
    print(f"\n  {'median':>10}{statistics.median(b):>13,.0f}{statistics.median(h):>13,.0f}"
          f"{statistics.median(h) - statistics.median(b):>+12,.0f}")
    print(f"  {'min':>10}{min(b):>13,.0f}{min(h):>13,.0f}")
    print(f"  {'max':>10}{max(b):>13,.0f}{max(h):>13,.0f}")
    print(f"  hybrid wins on {sum(1 for x, y in zip(b, h) if y > x)} of {len(rows)} seeds")

    if not args.skip_net_only:
        print("\n  net playing EVERYTHING (units and market), same seeds:")
        for s in seeds:
            n, _a, _t = play(s, args.turns, units_from_net=True, net=net)
            print(f"  {s:>10}{n:>13,.0f}", flush=True)

    print("\nREAD IT LIKE THIS")
    print("  hybrid > planner   the clone's market head is worth having and the split is the "
          "prototype to build on.")
    print("  hybrid ~ planner   the market is not where the clone's value is; test the other "
          "split -- planner routes, net picks crops.")
    print("  hybrid < planner   the clone trades against a board it was not fitted on. Re-run on "
          "the corrected-vocabulary checkpoint before concluding anything.")


main()
