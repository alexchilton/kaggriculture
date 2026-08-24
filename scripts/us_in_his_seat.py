"""Play OUR agent in カワシギ's seat, in every game of his we hold, on that game's own seed.

Alex, 2026-08-24: *"play every kawa game against our agent on the correct seed or town -- find those
where the output differs most. I think most games are fine but my suspicion is there are some large
divergences."*

Two arms per game, same seed, same seat, same recorded opponent:

    tape   カワシギ's own actions, verbatim, against the opponent's actions, verbatim
    us     our agent in his seat, from turn 0, against the same opponent tape

`tape` is also the VALIDITY CHECK, and it has to be, because half these games predate the
2026-08-15 balance change (`kaggle-environments` 1.32.6 -> 1.32.7 put CARROT, TOMATO and EGG on the
`hinge` curve). Replayed under the current env those games cannot reproduce their own recorded
result: the economy is different. So any game where `tape` does not reproduce `rewards` is reporting
on a game that no longer exists, and its `us` number means nothing. Those are printed and excluded
rather than silently averaged in.

`split` is the first day the two arms' banks differ by more than `--split-at` dollars. It is where
to look, not a verdict: a bank gap opens the turn a purchase succeeds in one arm and fails in the
other, and everything after inherits it.
"""

import argparse
import collections
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
HIM = "カワシギ"


def _recorded(steps, t, seat):
    if t + 1 < len(steps):
        a = steps[t + 1][seat].get("action")
        if isinstance(a, dict):
            return a
    return {"farmer": ["PASS"], "hands": [], "market": []}


def play(rec, his_seat, seed, use_agent):
    """Returns (ours, theirs, per-day bank). `use_agent=False` replays his tape verbatim."""
    from kaggle_environments import make
    import importlib
    import breakdown as B

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    steps = rec["steps"]
    them = 1 - his_seat

    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
    env.reset(2)
    agent = SA.make_agent(sched, his_seat) if use_agent else None

    banks = {}
    for t in range(30 * TPD):
        o = env.state[his_seat].observation
        if t % TPD == 0:
            banks[t // TPD] = o["farms"][his_seat]["money"]
        n_us = len(o["farms"][his_seat].get("hands") or [])
        n_them = len(o["farms"][them].get("hands") or [])
        if use_agent:
            a = agent(o)
            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
        else:
            a = _recorded(steps, t, his_seat)
            mine = {"farmer": a.get("farmer") or ["PASS"],
                    "hands": list(a.get("hands") or [])[:n_us],
                    "market": a.get("market") or []}
        at = _recorded(steps, t, them)
        yours = {"farmer": at.get("farmer") or ["PASS"],
                 "hands": list(at.get("hands") or [])[:n_them],
                 "market": at.get("market") or []}
        env.step([mine, yours] if his_seat == 0 else [yours, mine])
        if env.done:
            break
    farms = env.state[0].observation["farms"]
    return farms[his_seat]["money"], farms[them]["money"], banks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default=HIM)
    ap.add_argument("--split-at", type=float, default=2000.0)
    ap.add_argument("--fidelity", type=float, default=1.0,
                    help="dollars of slack allowed before a game is called stale")
    ap.add_argument("--out", default="data/logs/us_in_his_seat.csv")
    a = ap.parse_args()

    import glob
    files = set()
    for d in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
              "leaders_2026-08-24", "losses", "top_guys", "top2", "field_leaders",
              "new_leader", "ladder", "our_games"):
        files |= set(glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")))
    files |= set(glob.glob("/Users/alexchilton/Downloads/*.json"))

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("episode,seed,seat,opponent,recorded_him,recorded_opp,tape_him,tape_opp,"
             "us_him,us_opp,tape_margin,us_margin,divergence,split_day,stale\n")
    fh.flush()

    print(f"{a.who}: our agent in his seat, every game on its own seed.")
    print("`tape` must reproduce `recorded` or the game predates the 2026-08-15 hinge change "
          "and is excluded.\n", flush=True)
    print(f"{'episode':>10} {'seed':>11} {'rec':>9} {'tape':>9} {'us':>9} "
          f"{'diverge':>9} {'split':>6}  opponent", flush=True)

    rows = []
    t0 = time.time()
    for f in sorted(files):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                    # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seat = names.index(a.who)
        seed = (rec.get("info") or {}).get("seed")
        if seed is None:
            continue
        ep = pathlib.Path(f).stem
        rw = rec.get("rewards") or [0, 0]
        rec_margin = rw[seat] - rw[1 - seat]
        try:
            th, to, tb = play(rec, seat, seed, use_agent=False)
            uh, uo, ub = play(rec, seat, seed, use_agent=True)
        except Exception as e:                                               # noqa: BLE001
            print(f"{ep:>10}  {e!r}", flush=True)
            continue

        stale = abs((th - to) - rec_margin) > a.fidelity
        split = ""
        for d in sorted(tb):
            if d in ub and abs(ub[d] - tb[d]) > a.split_at:
                split = f"d{d}"
                break
        tm, um = th - to, uh - uo
        rows.append((um - tm, ep, tm, um, stale, names[1 - seat], split))
        print(f"{ep:>10} {seed:>11} {rec_margin:>+9,.0f} {tm:>+9,.0f} {um:>+9,.0f} "
              f"{um - tm:>+9,.0f} {split:>6}  {names[1 - seat][:22]}"
              f"{'   STALE' if stale else ''}", flush=True)
        fh.write(",".join(str(x) for x in [
            ep, seed, seat, names[1 - seat], round(rw[seat]), round(rw[1 - seat]),
            round(th), round(to), round(uh), round(uo), round(tm), round(um),
            round(um - tm), split, int(stale)]) + "\n")
        fh.flush()
    fh.close()

    live = [r for r in rows if not r[4]]
    dead = [r for r in rows if r[4]]
    print(f"\n{len(rows)} games: {len(live)} reproduce their recording, {len(dead)} STALE "
          f"(pre-hinge economy) and excluded below.")
    if live:
        print("\nRANKED BY DIVERGENCE -- our agent minus his tape, same seed, same seat, "
              "same opponent\n")
        print(f"{'diverge':>9} {'episode':>10} {'tape':>9} {'us':>9} {'split':>6}  opponent")
        for d, ep, tm, um, _s, opp, split in sorted(live):
            print(f"{d:>+9,.0f} {ep:>10} {tm:>+9,.0f} {um:>+9,.0f} {split:>6}  {opp[:22]}")
        wins_t = sum(1 for r in live if r[2] > 0)
        wins_u = sum(1 for r in live if r[3] > 0)
        print(f"\nhis tape wins {wins_t}/{len(live)}   our agent wins {wins_u}/{len(live)}")
        print(f"mean divergence {sum(r[0] for r in live) / len(live):>+,.0f}   "
              f"median {sorted(r[0] for r in live)[len(live) // 2]:>+,.0f}")
    print(f"\n({time.time() - t0:.0f}s)  rows -> {out}")


if __name__ == "__main__":
    main()
