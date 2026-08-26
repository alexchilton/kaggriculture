"""Take the games we LOST and ask whether a carrot arm flips any of them.

Alex, 2026-08-25: *"the money is bullshit -- use the solver and let the leaderboard decide."*

The opponent pool cannot answer this. `kagg.arena.COMPETITIVE` is ten `heuristic.make_agent`
parameterisations and we beat nine of them 100%, so every arm returns the same 19/20 = 95%: we win
everything and split the mirror. Measured 2026-08-25 over eight seeds and three drain buckets, the
control returned 95% on every single one. A saturated metric cannot rank arms.

What CAN answer it is the set of real ladder games we lost. Each one is a recorded opponent on a
known seed, and the question "does this arm flip it" is exactly the Elo question -- a $1 win scores
what a $30,000 win scores (`CLAUDE.md`).

For each recorded loss, and each arm, this plays OUR agent in OUR seat, on that game's OWN seed,
against that game's recorded opponent actions, and reports:

    the margin as recorded, the margin with the arm, and whether it FLIPPED

An arm that flips nothing is dead however good its money column looks. An arm that flips a game
that was lost by $29,384 has done the only thing the ladder pays for.

The arms are the two knobs, read off the code:

    schedule_agent.CARROT_SWAP_DAYS   the window
    corner_the_book.plan(max_tiles=)  the position size

They are patched in-process here rather than built into a bundle, because this harness drives the
agent directly instead of handing a file to a subprocess pool.
"""

import argparse
import collections
import glob
import itertools
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
DIRS = ("losses", "ladder", "ladder_1943", "ladder_2026-08-16", "ladder_2026-08-16b",
        "downloads_2026-08-19", "downloads_2026-08-20", "downloads_2026-08-21",
        "field", "field_leaders", "our_games")
US = "alex chilton"


def our_losses(who=US):
    """Recorded games where `who` has a seat and LOST. Returns (ep, path, seat, seed, margin)."""
    out = []
    seen = set()
    for d in DIRS:
        for f in sorted(glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json"))):
            ep = pathlib.Path(f).stem
            if ep in seen:
                continue
            try:
                rec = json.loads(pathlib.Path(f).read_text())
            except Exception:                                                 # noqa: BLE001
                continue
            if not isinstance(rec, dict) or "steps" not in rec:
                continue
            info = rec.get("info") or {}
            names = info.get("TeamNames") or []
            if who not in names or info.get("seed") is None:
                continue
            seat = names.index(who)
            last = rec["steps"][-1]
            try:
                ours = float(last[seat]["reward"])
                theirs = float(last[1 - seat]["reward"])
            except Exception:                                                 # noqa: BLE001
                continue
            seen.add(ep)
            if ours < theirs:
                out.append((ep, f, seat, info["seed"], ours - theirs, names[1 - seat]))
    return out


def play(rec, seat, seed):
    """Our agent in our seat, that game's seed, the recorded opponent. Returns (ours, theirs)."""
    import importlib
    import breakdown as B
    import us_in_his_seat as U
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    steps = rec["steps"]
    them = 1 - seat
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, seat)

    for t in range(30 * TPD):
        o = env.state[seat].observation
        n_us = len(o["farms"][seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        a = agent(o)
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                "market": a["market"]}
        at = U._recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if seat == 0 else [yours, mine])
        if env.done:
            break
    f = env.state[seat].observation["farms"]
    return float(f[seat]["money"]), float(f[them]["money"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default=US)
    ap.add_argument("--tiles", default="0,8,16,24,32,40,56")
    ap.add_argument("--starts", default="21,23,25")
    ap.add_argument("--list-only", action="store_true")
    a = ap.parse_args()

    losses = our_losses(a.who)
    print(f"{len(losses)} recorded losses for {a.who!r}\n")
    for ep, _f, seat, seed, margin, opp in losses:
        print(f"  {ep}  seat {seat}  seed {seed}  margin ${margin:,.0f}  vs {opp}")
    if a.list_only or not losses:
        return

    import importlib
    SA = importlib.import_module("kagg.search.schedule_agent")
    CORNER = importlib.import_module("kagg.search.corner_the_book")
    live_days, live_plan = SA.CARROT_SWAP_DAYS, CORNER.plan

    tiles_arms = [int(x) for x in a.tiles.split(",") if x]
    start_arms = [int(x) for x in a.starts.split(",") if x]
    flips = collections.Counter()
    try:
        for start, tiles in itertools.product(start_arms, tiles_arms):
            if tiles == 0 and start != start_arms[0]:
                continue
            SA.CARROT_SWAP_DAYS = tuple(range(start, 28))
            CORNER.plan = ((lambda *ar, **kw: (0, "control"))
                           if tiles == 0 else
                           (lambda *ar, **kw: live_plan(*ar, **{**kw, "max_tiles": tiles})))
            print(f"\narm tiles={tiles} start=d{start}", flush=True)
            for ep, f, seat, seed, margin, opp in losses:
                rec = json.loads(pathlib.Path(f).read_text())
                try:
                    ours, theirs = play(rec, seat, seed)
                except Exception as e:                                        # noqa: BLE001
                    print(f"   {ep}: {e!r}", flush=True)
                    continue
                new = ours - theirs
                won = new > 0
                flips[(tiles, start)] += won
                print(f"   {ep}  recorded ${margin:>10,.0f}   arm ${new:>10,.0f}   "
                      f"{'FLIPPED' if won else ''}", flush=True)
    finally:
        SA.CARROT_SWAP_DAYS, CORNER.plan = live_days, live_plan

    print("\nflips per arm, of "
          f"{len(losses)} losses:")
    for (tiles, start), n in sorted(flips.items(), key=lambda kv: -kv[1]):
        print(f"   tiles {tiles:>3}  start d{start}   {n}")


if __name__ == "__main__":
    main()
