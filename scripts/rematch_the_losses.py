"""Replay our own ladder games: OUR LIVE AGENT in our seat, THEIR RECORDED ACTIONS in theirs.

**The controlled experiment this project has been missing.** `how_much_does_the_draw_move_us.py`
measured the shop draw at $72,008 of spread over 12 seeds -- 80% of the mean season -- which makes
any arm under ~$5,000 unmeasurable on the seed counts used here. A rematch removes that entirely:
the game's own `info.seed` fixes the draw (`reference/kaggriculture.py:869`,
`rng = random.Random((seed * 1_000_003) ^ day)`), so two runs of this differ by our agent and
nothing else. The three analysed losses were $645, $3,919 and $962 -- invisible on random seeds,
directly readable here.

**And the opponent is faithful, not approximated.** The field submits fixed 720-turn scripts; on
2026-08-16 a downloaded game showed Thomas Tschinkel reproducing Kawashigi's opening 24/24 for eight
straight days. Replaying a scripted opponent's recorded actions IS that opponent.

One thing it is NOT: a ladder win rate. It is a rematch of games we already played, most of them
selected because we lost. Read the DELTA against the same corpus, never the level.

Their recorded bank will not match the recording either, and that is expected rather than a bug --
we sell into the same book, so a different agent of ours makes them a different amount of money.
`docs/matching_the_tape` has the long version.

    python -u scripts/rematch_the_losses.py --dir data/seed_scripts/ladder_2026-08-16b --limit 12
    python -u scripts/rematch_the_losses.py --only 93239838,93242536
"""
import argparse
import glob
import importlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
US = "alex chilton"


def games(folder, only=None, losses_only=True):
    """`[(episode, path, our_seat, seed, our_recorded, their_recorded)]`, closest losses first."""
    out = []
    for p in sorted(glob.glob(str(REPO / folder / "*.json"))):
        try:
            raw = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        if not isinstance(raw, dict) or len(raw.get("steps") or []) < 700:
            continue
        info = raw.get("info") or {}
        names = info.get("TeamNames") or []
        if US not in names:
            continue
        seat = names.index(US)
        rw = raw.get("rewards") or []
        if len(rw) < 2 or rw[0] is None or rw[1] is None:
            continue
        ours, theirs = rw[seat], rw[1 - seat]
        ep = str(info.get("EpisodeId") or pathlib.Path(p).stem)
        if only and ep not in only:
            continue
        if losses_only and not only and ours >= theirs:
            continue
        out.append((ep, p, seat, info.get("seed"), ours, theirs))
    # **Deduplicate on EPISODE, not on filename.** The same game is downloaded twice under names
    # like `93525585.json` and `93525585-0.json`, and counting it twice silently reweights the
    # corpus. Four of 97 games were duplicated, which was enough to turn a 6/11 into a 7/12 and
    # make a regression read as a tie.
    seen, uniq = set(), []
    for row in out:
        if row[0] in seen:
            continue
        seen.add(row[0])
        uniq.append(row)
    uniq.sort(key=lambda r: (r[5] - r[4]))           # narrowest margin first
    return uniq


def rematch(path, our_seat, seed, days=30):
    """Play the game again with our live agent. Returns `(ours, theirs)` final banks."""
    from kaggle_environments import make

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    rec = json.loads(pathlib.Path(path).read_text())
    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    steps = rec["steps"]
    them = 1 - our_seat

    def their_action(t):
        """Their recorded action for turn `t`, or a no-op past the end of the recording."""
        if t + 1 < len(steps):
            a = steps[t + 1][them].get("action")
            if isinstance(a, dict):
                return a
        return {"farmer": ["PASS"], "hands": [], "market": []}

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=True)
    env.reset(2)
    agent = SA.make_agent(sched, our_seat)
    for t in range(days * TPD):
        o_us = env.state[our_seat].observation
        a_us = agent(o_us)
        a_them = their_action(t)
        n_us = len(o_us["farms"][our_seat].get("hands") or [])
        n_them = len(o_us["farms"][them].get("hands") or [])
        mine = {"farmer": a_us["farmer"], "hands": list(a_us["hands"] or [])[:n_us],
                "market": a_us["market"]}
        yours = {"farmer": a_them.get("farmer") or ["PASS"],
                 "hands": list(a_them.get("hands") or [])[:n_them],
                 "market": a_them.get("market") or []}
        env.step([mine, yours] if our_seat == 0 else [yours, mine])
        if env.done:
            break
    farms = env.state[0].observation["farms"]
    return farms[our_seat]["money"], farms[them]["money"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="data/seed_scripts/ladder_2026-08-16b")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--only", default=None, help="comma-separated episode ids")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--all", action="store_true", help="include games we won")
    a = ap.parse_args()

    only = {x.strip() for x in a.only.split(",")} if a.only else None
    rows = games(a.dir, only, losses_only=not a.all)[:a.limit]
    print(f"{len(rows)} games from {a.dir}\n")
    print(f"{'episode':>10} {'seat':>4} {'recorded ours':>14} {'recorded theirs':>16} "
          f"{'margin':>10} | {'rematch ours':>13} {'rematch theirs':>15} {'result':>7} {'swing':>10}")
    flipped = won = 0
    swings = []
    for ep, path, seat, seed, ours, theirs in rows:
        got, got_them = rematch(path, seat, seed, a.days)
        res = "WIN" if got > got_them else "loss"
        won += got > got_them
        flipped += (got > got_them) and (ours < theirs)
        swings.append(got - ours)
        print(f"{ep:>10} {seat:>4} {ours:>14,.0f} {theirs:>16,.0f} {theirs - ours:>10,.0f} | "
              f"{got:>13,.0f} {got_them:>15,.0f} {res:>7} {got - ours:>+10,.0f}", flush=True)
    if swings:
        print(f"\n  rematch wins {won}/{len(rows)}   games flipped from a recorded LOSS: {flipped}")
        print(f"  mean swing in our bank vs the recording: ${sum(swings) / len(swings):+,.0f}")


if __name__ == "__main__":
    main()
