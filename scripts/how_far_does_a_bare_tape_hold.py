"""Replay a clone tape VERBATIM on other shop draws. Where does it stop working?

Alex, 2026-08-26: *"i just wanna know how well it works with the 3 bare tapes and if the solver or
planner are necessary and where - test it across different shops and see how close they stay to the
other tapes of that guy playing those shop systems"*.

No planner, no solver, no schedule. Just the recorded 720 turns fired at a fresh environment on a
DIFFERENT shop draw, which is the honest test of an open-loop script: the start state is fixed
(same board, $3000, NW only), so the only things that move under it are the opponent, the shop
unlocks and the weed rolls.

Two questions, and they need different columns:

    does it BANK        final money against the tape's own recorded final money. A tape that banks
                        its recorded total on a foreign draw needs no engine at all.
    where does it BREAK the first day our replayed board stops matching the recorded board -- money,
                        owned tiles, or standing crop. **That day is where a planner becomes
                        necessary, and not before.** Before it, an engine can only do what the tape
                        already does.

An op that cannot execute is silently dropped by the environment -- a PLANT onto a weed-spawned
tile, a BUY refused on a thin bank -- so divergence is measured on the BOARD, not on the action
stream, which would read identical by construction.

Shop draws come from other recorded games, injected the way `breakdown.run` does it, so each trial
is a real draw the ladder produced rather than a synthetic one.
"""

import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
#: name -> (replay, team, own seed). The three branch tapes plus the d27-coherent one.
TAPES = {
    "clone_open": ("data/seed_scripts/clone_open/98907591.json", "UjjwalPardeshi", 123641874),
    "clone_late": ("data/seed_scripts/clone_late/98898511.json", "G!vIOne", 1598723111),
    "clone_yarn3": ("data/seed_scripts/clone_yarn3/98889302.json", "WeAreFarmers", 1290360884),
    "clone_yarn6": ("data/seed_scripts/clone_yarn6/98857364.json", "Bharath Varma", 205177061),
}


def board(obs, seat):
    """`{money, tiles, crop, animals}` for one seat.

    **`tiles` is OWNED LAND, counted as 100 minus the LOCKED squares.** The first cut used
    `c.get("owned", True)` over dict cells, and there is no `owned` key -- a locked square is the
    literal string `"LOCKED"` and an empty one is `None`, so only PLANT and PASTURE cells are dicts
    at all. That counted "squares with something on them", which climbs every time anything is
    planted: 16, 20, 23 over d0-d2 of one recording. It read as the tape diverging on d1 when
    nothing had diverged.
    """
    farms = (obs or {}).get("farms") or []
    if seat >= len(farms):
        return None
    f = farms[seat]
    locked = crop = animals = 0
    for row in (f.get("tiles") or []):
        for c in row:
            if c == "LOCKED":
                locked += 1
                continue
            if not isinstance(c, dict):
                continue
            if c.get("crop"):
                crop += int(c.get("yield_units", 0) or 0)
            if c.get("animal"):
                animals += 1
    return dict(money=float(f.get("money", 0)), tiles=100 - locked, crop=crop, animals=animals)


def recorded(replay, seat):
    """`{day: board}` at the last turn of each day, from the recording itself."""
    out = {}
    for t, step in enumerate(replay.get("steps") or []):
        if t % TPD != TPD - 1:
            continue
        b = board((step[0] or {}).get("observation") or {}, seat)
        if b:
            out[t // TPD] = b
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", default="clone_open,clone_late,clone_yarn3,clone_yarn6")
    ap.add_argument("--draws", type=int, default=4,
                    help="how many OTHER tapes' shop draws to borrow")
    args = ap.parse_args()

    from kaggle_environments import make
    import scripts.breakdown as B

    names = [n for n in args.tapes.split(",") if n in TAPES]
    print(f"{len(names)} tapes x (own draw + {args.draws} borrowed draws)\n")

    for name in names:
        path, team, own = TAPES[name]
        full = str(REPO / path)
        rep = json.loads(pathlib.Path(full).read_text())
        seat = rep["info"]["TeamNames"].index(team)
        rec = recorded(rep, seat)
        rec_final = rec[max(rec)]["money"] if rec else 0.0
        print(f"=== {name}   recorded final ${rec_final:,.0f}")
        print(f"   {'draw from':<14}{'seed':>12}{'final $':>11}{'vs rec':>9}"
              f"{'money@d':>9}{'tiles@d':>9}{'crop@d':>8}")

        draws = [(name, own)] + [(o, TAPES[o][2]) for o in names if o != name][:args.draws]
        for draw_name, seed in draws:
            dpath = str(REPO / TAPES[draw_name][0])
            economy = B.env_config(dpath)
            shops = B.recorded_shops(dpath)
            env = make("kaggriculture", configuration=dict(economy, seed=seed), debug=False)
            env.reset(2)
            # Our seat replays the tape; the other seat replays the SAME tape, so the market is
            # contested the way a real ladder game is and neither side is a pushover.
            mine = B.tape_policy(full, team, 0)
            opp = B.tape_policy(full, team, 1)
            first = {"money": None, "tiles": None, "crop": None}
            for t in range(719):
                env.state[0].observation.town["unlocked_shops"] = list(shops(t))
                env.step([mine(env.state[0].observation, t), opp(env.state[1].observation, t)])
                if t % TPD == TPD - 1:
                    day = t // TPD
                    now = board(env.state[0].observation, 0)
                    ref = rec.get(day)
                    if now and ref:
                        for k, tol in (("money", 0.05), ("tiles", 0.0), ("crop", 0.10)):
                            if first[k] is not None:
                                continue
                            a, b = now[k], ref[k]
                            off = abs(a - b) > max(1.0, tol * max(1.0, abs(b)))
                            if off:
                                first[k] = day
            fin = board(env.state[0].observation, 0)
            f = fin["money"] if fin else 0.0
            print(f"   {draw_name:<14}{seed:>12}{f:>11,.0f}"
                  f"{100*f/max(1.0, rec_final):>8.0f}%"
                  f"{('d'+str(first['money'])) if first['money'] is not None else 'never':>9}"
                  f"{('d'+str(first['tiles'])) if first['tiles'] is not None else 'never':>9}"
                  f"{('d'+str(first['crop'])) if first['crop'] is not None else 'never':>8}")
        print()


if __name__ == "__main__":
    main()
