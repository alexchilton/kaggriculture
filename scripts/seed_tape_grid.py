"""Across seeds and across tapes: how many days does the replay actually hold?

Alex, 2026-08-21: *"check across the various seeds how well we match till d12 and then to d20 and
how many tapes are passing days for the different periods"*, *"there should be more than 1 tape"*,
*"at least after the q3 q4 split at d12"*.

`scripts/breakdown.py` answers this for ONE seed against ONE tape and prints a 30-column table.
That is the wrong shape for the question. This prints one LINE per `(tape, seed)`: exact days and
independent differing cells, split at d12 and at d20.

Two things about `--seed` that the single-seed grid hides, and both are why "more than 1 tape"
needs more than one `--seed`:

  **The branch latches do not read the seed.** `melon_branch` reads the OPPONENT's melon tiles and
  the opponent is `tape_policy(replay, team, 1)` -- the tape game's own seat 1, fixed by the file.
  `q4_branch` reads `YARN_STORE` unlocked by d6 and `breakdown.recorded_shops` injects the tape's
  own town draw into both columns. So on a fixed tape every seed arms the SAME key and replays the
  SAME opening. Varying the seed varies weeds and the market noise around it, nothing else.

  **Which is why the tape axis is the one that matters here.** Three registered kawashigi tapes
  bring three opponents and three shop draws between them, so they exercise different branches.

The differing-cell count is `breakdown.py --diff`'s, copied rather than imported because that
function prints as it counts: state rows, then every op except the four compass directions, and
NOT the four `=sum` rows, which are those same ops added up again.

    python -u scripts/seed_tape_grid.py --seeds 11 12 13 14 15 --days 21
"""

import argparse
import collections
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                              # noqa: E402

#: The kawashigi tapes only. `victor` is a different player on a different plan and would answer a
#: question nobody asked.
TAPES = ("kawashigi", "kawashigi_b3", "kawashigi_q4c")

COMPASS = {"NORTH", "SOUTH", "EAST", "WEST"}


def differing(ours, our_ops, his, his_ops, days):
    """`[[(field, ours - tape)]]` per day, over what `breakdown.py --diff` calls independent.

    The COUNT alone says a day is wrong; the NAMES say why, and the difference matters. `d21=2`
    onwards reads as "the tape stops working around d21" and is in fact the same pair of cells nine
    days running, which is one leak with one cause.
    """
    fields = (["money", "hands", "owned", "pen", "weed"]
              + ["crop_" + c for c in B.CROPS] + ["animals"])
    ops = [o for o in sorted(set(B.OPS) | {"OTHER"} | set(B.MARKET_FILL_OPS)) if o not in COMPASS]
    out = []
    for d in range(days):
        row = [(k.replace("crop_", ""), ours[d][k] - his[d][k])
               for k in fields if ours[d][k] != his[d][k]]
        row += [(o.lower(), our_ops[d][o] - his_ops[d][o])
                for o in ops if our_ops[d][o] != his_ops[d][o]]
        out.append(row)
    return out


def cells_per_day(ours, our_ops, his, his_ops, days):
    """`[n_differing_cells]` per day, counting exactly what `breakdown.py --diff` calls independent."""
    return [len(r) for r in differing(ours, our_ops, his, his_ops, days)]


def one(tape, seed, weeds, days, module, live_shops=False):
    replay, schedule, team = B.TAPES[tape]
    import json
    sched = {int(k): v for k, v in json.loads(pathlib.Path(schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(replay)
    # **`--live-shops` is the only setting in which `--seed` means anything.** `recorded_shops`
    # injects the tape's OWN town draw into both columns, and both latches plus the whole schedule
    # are functions of that draw -- so with it on, every seed plays the same town, arms the same
    # branch and replays the same opening. Off, the seed draws its own town and the question becomes
    # the real one: how many days does a tape recorded against one town survive against another?
    # Both columns still get the SAME draw, so the comparison stays fair.
    shops = None if live_shops else B.recorded_shops(replay)

    def opp():
        return B.tape_policy(replay, team, 1)

    his, his_ops, _, _ = B.run(lambda: B.tape_policy(replay, team, 0), opp, seed, weeds,
                               stop_day=days + 1, economy=economy, shops=shops)

    def mine():
        a = B.schedule_agent.make_agent(thin, 0, router=True)
        return lambda o, t: a(o)

    ours, our_ops, _, _ = B.run(mine, opp, seed, weeds, stop_day=days + 1, economy=economy,
                                shops=shops)
    return cells_per_day(ours, our_ops, his, his_ops, days)


def vs_all(seeds, weeds, days, live_shops, opponent="kawashigi"):
    """One run of OURS per seed, diffed against all three tape files in the same game.

    Alex, 2026-08-21: *"we need to test with the 4 tapes ... where the differences actually occur
    across seeds and why"*.

    `--tape X` cannot answer that once the shops are live, because it fixes the comparison target
    while the LATCHES are free to pick a different tape -- so a mismatch reads as "we played badly"
    when it means "we played tape B and you diffed against tape A". Diffing against all three
    instead lets the answer fall out of the data: the tape with the zero column is the one we chose,
    and the day its column stops being zero is the day the choice stopped paying.

    The opponent and the economy are held at the melon tape's for every row, so the only thing
    moving between rows is the seed's own town draw. `--live-shops` off makes every row identical,
    which is the point being demonstrated.
    """
    import json
    files = [(n,) + B.TAPES[n][::2] for n in TAPES]      # (name, replay_path, team)
    base_replay, _, base_team = B.TAPES["kawashigi"]
    _, base_schedule, _ = B.TAPES["kawashigi"]
    sched = {int(k): v for k, v in json.loads(pathlib.Path(base_schedule).read_text()).items()}
    thin = {d: {k: v for k, v in r.items() if k not in B.TAPE_ONLY} for d, r in sched.items()}
    economy = B.env_config(base_replay)

    # **The opponent is the ONLY thing `melon_branch` reads.** It counts the opponent's MELON tiles
    # at d3, so a sweep that holds the opponent fixed can never fire it however many seeds it runs
    # -- and every seed sweep before this one held it at `kawashigi`'s seat 1, which plants 5.
    # `kawashigi_b3`'s seat 1 plants 9, exactly `melon_branch.OPPONENT_MELON`, which is why that
    # game is his strawberry season. Two values of this flag are the whole melon/strawberry test.
    opp_replay, _, opp_team = B.TAPES[opponent]
    print("opponent = %s seat 1   economy held at the melon tape's   only the town draw moves\n"
          % pathlib.Path(opp_replay).name)
    for seed in seeds:
        shops = None if live_shops else B.recorded_shops(base_replay)

        def opp():
            return B.tape_policy(opp_replay, opp_team, 1)

        # **The town draw, captured off our own turns rather than probed separately.** It cannot be
        # derived from the seed alone: `_end_of_day` spends the same generator on `_spawn_weeds`
        # first, once per EMPTY TILE per player, so where the draw lands depends on how the board
        # was played -- `recorded_shops`' docstring makes the same point. A PASS-agent probe would
        # therefore report a different town from the one our agent actually faces.
        draw = {}

        def mine():
            a = B.schedule_agent.make_agent(thin, 0, router=True)

            def f(o, t):
                if t % 24 == 0:
                    draw[t // 24] = tuple((o.get("town") or {}).get("unlocked_shops") or ())
                return a(o)
            return f

        ours, our_ops, _, _ = B.run(mine, opp, seed, weeds, stop_day=days + 1, economy=economy,
                                    shops=shops)
        print("seed %d   town at d3 %s   d6 %s   d9 %s"
              % (seed, list(draw.get(3, ())), list(draw.get(6, ())), list(draw.get(9, ()))))
        print("%18s   %s" % ("", " ".join("d%-2d" % d for d in range(days))))
        best = (None, None)
        for name, path, team in files:
            his, his_ops, _, _ = B.run(lambda: B.tape_policy(path, team, 0), opp, seed, weeds,
                                       stop_day=days + 1, economy=economy, shops=shops)
            rows = differing(ours, our_ops, his, his_ops, days)
            bad = next((d for d, r in enumerate(rows) if r), None)
            print("%18s   %s   first bad %s"
                  % (name, " ".join("%3d" % len(r) for r in rows),
                     "none" if bad is None else "d%d" % bad))
            total = sum(len(r) for r in rows)
            if best[0] is None or total < best[1]:
                best = (name, total)
            if bad is not None:
                names = collections.Counter(f for r in rows for f, _ in r)
                print("%18s   %s" % ("", "  ".join("%s x%d" % (f, n)
                                                   for f, n in names.most_common(8))))
        # **The tape we CHOSE, read off the data rather than off the latch.** No instrumentation
        # needed and none possible without one: `melon_armed` and `q4_armed` live in a closure. The
        # tape we replayed is the one our ops track, so the lowest column names it.
        print("%18s   chose %s (%d cells)" % ("->", best[0], best[1]))
        print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", nargs="+", type=int, default=[11, 12, 13, 14, 15])
    ap.add_argument("--tapes", nargs="+", default=list(TAPES))
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--weeds", type=float, default=0.0)
    ap.add_argument("--module", default=B.DEFAULT_MODULE)
    #: **A harness parameter, not a shipped constant.** `REPLAY_OPENING_DAYS` ends at d23 because
    #: d24-d29 are the planner's, which is a decision about what to SHIP. Asking "how far could the
    #: tape carry us if we let it" is a different question and answering it must not leave a changed
    #: constant behind in the module -- that is exactly the stale-runnable-artifact failure.
    ap.add_argument("--replay-days", type=int, default=None, metavar="N",
                    help="override REPLAY_OPENING_DAYS to range(N) for this run only")
    ap.add_argument("--per-day", action="store_true",
                    help="print the differing-cell count for every day, not just the summary")
    ap.add_argument("--opponent", default="kawashigi", choices=sorted(B.TAPES),
                    help="whose seat 1 plays against us. kawashigi plants 5 MELON by d3 and never "
                         "arms melon_branch; kawashigi_b3 plants 9 and always does. --vs-all only.")
    ap.add_argument("--vs-all", action="store_true",
                    help="one run of ours per seed, diffed against ALL three tape files. The tape "
                         "with the zero column is the one the latches chose.")
    ap.add_argument("--live-shops", action="store_true",
                    help="let the SEED draw the town instead of injecting the tape's own draw. "
                         "The only mode in which --seed changes anything.")
    args = ap.parse_args()

    B.schedule_agent = B.load_agent_module(args.module)
    if args.replay_days is not None:
        B.schedule_agent.REPLAY_OPENING_DAYS = tuple(range(args.replay_days))
    print("module %s   weeds %.3f   days 0-%d   REPLAY_OPENING_DAYS=%s   shops=%s\n"
          % (args.module, args.weeds, args.days - 1,
             (B.schedule_agent.REPLAY_OPENING_DAYS[:1],
              B.schedule_agent.REPLAY_OPENING_DAYS[-1:]),
             "SEED DRAWS THEM" if args.live_shops else "injected from the tape"))
    if args.vs_all:
        return vs_all(args.seeds, args.weeds, args.days, args.live_shops, args.opponent)
    print("%-16s %5s | %10s %8s | %10s %8s | %s"
          % ("tape", "seed", "d0-d12", "cells", "d13-d20", "cells", "first bad day"))
    print("-" * 96)
    for tape in args.tapes:
        for seed in args.seeds:
            try:
                per = one(tape, seed, args.weeds, args.days, args.module, args.live_shops)
            except Exception as exc:                       # a missing tape file is data, not a crash
                print("%-16s %5d | %s: %s" % (tape, seed, type(exc).__name__, exc))
                continue
            early, late = per[:13], per[13:21]
            bad = next((d for d, n in enumerate(per) if n), None)
            print("%-16s %5d | %5d/13 ok %8d | %6d/%d ok %8d | %s"
                  % (tape, seed,
                     sum(1 for n in early if n == 0), sum(early),
                     sum(1 for n in late if n == 0), len(late), sum(late),
                     "none" if bad is None else "d%d" % bad))
            if args.per_day:
                print("%22s   %s" % ("", " ".join("%3d" % n for n in per)))
                print("%22s   %s" % ("", " ".join("d%-2d" % d for d in range(len(per)))))
        print()


if __name__ == "__main__":
    main()
