"""Acceptance: does reading the book's depth win games our agent was losing?

Alex, 2026-08-24: *"i want you to prove the mechanism and then to improve our agent by using the
mechanism for ourselves -- that is the acceptance."*

Two arms, same games, same seeds, same replayed prefix:

    control    `_carrot_pays` restored to the shipped two constants
               (CARROT_DRAIN_MIN = 5, CARROT_OPP_MAX = 7)
    treatment  `_carrot_pays` reading the town's inventory deficit (`corner_the_book.plan`)

Both tapes are replayed verbatim to the handover, so the board, the bank and -- the point -- the
town's BOOK are the real ones. Prices here are endogenous: the same seed that paid $270 for milk in
a recording paid $1 in a rematch from turn 0, so re-simulating the season would measure a different
market and answer a different question.

**Handover at d21, not d28.** The carrot window is d25-d27 and the crop needs two days to ripen, so
a d28 handover cannot express the decision at all. d21 is the first day the real opponent in
98495047 began converting.

## The metric is FLIPPED GAMES

Not mean money. The ladder is Elo: a $1 win scores exactly what a $30,000 win scores. An arm that
adds $10k to games we already lose by $29k has done nothing. So the columns that decide this are
`control_win` and `treat_win`, and the number that matters is how many losses became wins with no
win becoming a loss.

    python -u scripts/does_the_book_reading_win_games.py --handover 21
"""

import argparse
import collections
import importlib
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
US = "alex chilton"
GAMES = ("98495047", "98460892", "98494953", "98499540", "98501831", "98428765")


def _find(ep):
    """First hit that is actually a full replay (`info` + `steps`), not a derived summary.

    `data/seed_scripts/field_leaders/*.json` (and similar dirs) hold a lightweight per-game
    summary -- keys `team, episode, seat_in_recording, their_money, our_money, actions` -- for the
    same episode id as the real download elsewhere in the tree. `rglob` order is filesystem order,
    not "real replay first", so picking `hits[0]` blind can hand back the summary file and crash on
    `rec["info"]`. Found 2026-08-24 scanning drain 7-8 games: `field_leaders/91108446.json` sorted
    before `top_guys/91108446.json`.
    """
    hits = list((REPO / "data/seed_scripts").rglob(f"{ep}.json"))
    for h in hits:
        try:
            rec = json.loads(h.read_text())
        except Exception:                                                   # noqa: BLE001
            continue
        if isinstance(rec, dict) and "info" in rec and "steps" in rec:
            return h
    return None


def _recorded(steps, t, seat):
    if t + 1 < len(steps):
        a = steps[t + 1][seat].get("action")
        if isinstance(a, dict):
            return a
    return {"farmer": ["PASS"], "hands": [], "market": []}


def _old_gate(obs, me=0):
    """The shipped rule, restored verbatim for the control arm."""
    SA = importlib.import_module("kagg.search.schedule_agent")
    if SA._carrot_town_drain(obs) < SA.CARROT_DRAIN_MIN:
        return False
    farms = obs.get("farms") or []
    seat = int(obs.get("player", me) or 0)
    if len(farms) < 2:
        return True
    theirs = sum(1 for row in ((farms[1 - seat] or {}).get("tiles") or []) for t in row
                 if isinstance(t, dict) and t.get("crop") == "CARROT")
    return theirs <= SA.CARROT_OPP_MAX


def play(path, our_seat, seed, handover, use_old_gate):
    """Replay both tapes to `handover`, then our agent plays out. Returns a row.

    `handover=None` never calls our agent at all: both tapes run to the bell. That arm is the zero
    the money columns are read against, because taking the wheel at the handover is itself worth
    -$6,817 to -$20,878 before any arm acts.
    """
    from kaggle_environments import make

    import breakdown as B
    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    live = SA._carrot_pays
    if use_old_gate:
        SA._carrot_pays = _old_gate
    try:
        rec = json.loads(pathlib.Path(path).read_text())
        cfg = dict(rec.get("configuration") or {})
        cfg.pop("seed", None)
        steps = rec["steps"]
        them = 1 - our_seat

        env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
        env.reset(2)
        agent = None if handover is None else SA.make_agent(sched, our_seat)
        cut = 30 * TPD if handover is None else handover * TPD
        carrot_at_close = 0

        for t in range(30 * TPD):
            o_us = env.state[our_seat].observation
            n_us = len(o_us["farms"][our_seat].get("hands") or [])
            n_them = len(o_us["farms"][them].get("hands") or [])
            if t == 29 * TPD:
                # Fable's intermediate assertion. The corner is a POSITION, and whether it was
                # built is visible here, one day before money can confound it. On 98495047 the
                # opponent who beat us by $29,384 opened d29 holding ~76 units.
                p = env.state[our_seat].observation["private"]
                c = collections.Counter(p.get("shed") or {})
                for i in (p.get("inventories") or []):
                    c.update(i)
                carrot_at_close = int(c.get("CARROT", 0))
            if t >= cut:
                a = agent(o_us)
                mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                        "market": a["market"]}
            else:
                a = _recorded(steps, t, our_seat)
                mine = {"farmer": a.get("farmer") or ["PASS"],
                        "hands": list(a.get("hands") or [])[:n_us],
                        "market": a.get("market") or []}
            at = _recorded(steps, t, them)
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n_them],
                     "market": at.get("market") or []}
            env.step([mine, yours] if our_seat == 0 else [yours, mine])
            if env.done:
                break

        obs = env.state[0].observation
        farms = obs["farms"]
        px = (obs.get("market") or {}).get("prices") or {}
        inv = (obs.get("market") or {}).get("inventory") or {}
        priv = env.state[our_seat].observation["private"]
        held = collections.Counter(priv.get("shed") or {})
        for i in (priv.get("inventories") or []):
            held.update(i)
        carrot_tiles = sum(
            1 for row in farms[our_seat]["tiles"] for t2 in row
            if isinstance(t2, dict) and t2.get("crop") == "CARROT")
        return {"ours": farms[our_seat]["money"], "theirs": farms[them]["money"],
                "carrot_price": float(px.get("CARROT", 0) or 0),
                "deficit": 10_000 - int(inv.get("CARROT", 10_000)),
                "our_carrot_tiles": carrot_tiles,
                "carrot_at_close": carrot_at_close}
    finally:
        SA._carrot_pays = live


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handover", type=int, default=21)
    ap.add_argument("--games", default=",".join(GAMES))
    ap.add_argument("--out", default="data/logs/book_reading_acceptance.csv")
    a = ap.parse_args()

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["episode", "seed", "recorded_margin", "tape_margin", "control_margin", "treat_margin",
            "handover_bias", "control_win", "treat_win", "flip", "treat_carrot_tiles",
            "treat_carrot_at_close", "control_carrot_at_close", "treat_carrot_price",
            "treat_deficit"]
    fh = out.open("w")
    fh.write(",".join(cols) + "\n")
    fh.flush()

    print(f"handover d{a.handover}; both tapes replayed to there so the BOOK is real")
    print("metric is FLIPPED GAMES -- Elo pays the same for $1 and $30,000")
    print("`tape` replays BOTH tapes to the bell and never calls our agent. `bias` is")
    print("control - tape: what taking the wheel at the handover costs before any arm acts.")
    print("`d29 c` is carrot held at d29 dawn -- the POSITION, before money can confound it.\n",
          flush=True)
    print(f"{'episode':>10} {'recorded':>10} {'tape':>10} {'control':>10} {'treat':>10} "
          f"{'bias':>10} {'flip':>5} {'tiles':>6} {'d29 c/t':>9} {'price':>6} {'deficit':>8}",
          flush=True)

    t0 = time.time()
    flips = unflips = 0
    for ep in a.games.split(","):
        path = _find(ep)
        if path is None:
            print(f"{ep:>10}  not downloaded", flush=True)
            continue
        rec = json.loads(path.read_text())
        names = rec["info"]["TeamNames"]
        if US not in names:
            continue
        seat = names.index(US)
        seed = rec["info"]["seed"]
        rw = rec.get("rewards") or [0, 0]
        try:
            z = play(path, seat, seed, None, use_old_gate=True)
            c = play(path, seat, seed, a.handover, use_old_gate=True)
            t = play(path, seat, seed, a.handover, use_old_gate=False)
        except Exception as e:                                               # noqa: BLE001
            print(f"{ep:>10}  {e!r}", flush=True)
            continue
        zm = z["ours"] - z["theirs"]
        cm = c["ours"] - c["theirs"]
        tm = t["ours"] - t["theirs"]
        cw, tw = int(cm > 0), int(tm > 0)
        flip = tw - cw
        flips += flip == 1
        unflips += flip == -1
        print(f"{ep:>10} {rw[seat] - rw[1 - seat]:>+10,.0f} {zm:>+10,.0f} {cm:>+10,.0f} "
              f"{tm:>+10,.0f} {cm - zm:>+10,.0f} "
              f"{['', 'WIN', ''][flip + 1] if flip else '':>5} "
              f"{t['our_carrot_tiles']:>6} "
              f"{str(c['carrot_at_close']) + '/' + str(t['carrot_at_close']):>9} "
              f"{t['carrot_price']:>6.0f} {t['deficit']:>8}",
              flush=True)
        fh.write(",".join(str(x) for x in [ep, seed, round(rw[seat] - rw[1 - seat]), round(zm),
                                           round(cm), round(tm), round(cm - zm), cw, tw, flip,
                                           t["our_carrot_tiles"], t["carrot_at_close"],
                                           c["carrot_at_close"], round(t["carrot_price"]),
                                           t["deficit"]]) + "\n")
        fh.flush()
    fh.close()
    print(f"\nlosses flipped to wins: {flips}    wins lost: {unflips}    ({time.time() - t0:.0f}s)")
    print(f"rows -> {out}")


if __name__ == "__main__":
    main()
