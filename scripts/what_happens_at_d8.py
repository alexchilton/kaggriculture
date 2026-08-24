"""d3 is a one-hour timing shift. So why does the BOARD differ at d8?

Alex, 2026-08-24: *"what is the difference at d8 if the d3 is only timing."*

d4-d11 is a verbatim REPLAY of his tape (`schedule_agent.REPLAY_OPENING_DAYS`). If the replay is
working, our submitted action on every turn of d4-d8 is byte-identical to his recorded one, and any
board difference at d8 must have been SEEDED at d3 and carried forward -- an inherited state gap,
not a new decision.

If instead our action differs from his somewhere inside d4-d8, the replay itself is not replaying,
and d3 is a red herring.

Those two are distinguishable in one pass, so this does both at once:

    per day   how many of the 24 turns our submitted action differs from his recording
    at d8     the exact cells that differ, ours vs his, with what each holds

Both arms are his seat, on the game's own seed, against the same recorded opponent tape.
"""

import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24


def _norm(a):
    if not isinstance(a, dict):
        return (("PASS",), (), ())
    return (tuple(a.get("farmer") or ["PASS"]),
            tuple(tuple(x) for x in (a.get("hands") or [])),
            tuple(tuple(x) for x in (a.get("market") or [])))


def _cells(farm):
    out = {}
    for r, row in enumerate(farm.get("tiles") or []):
        for c, t in enumerate(row):
            if not isinstance(t, dict):
                continue
            sig = (t.get("kind"), t.get("crop"), t.get("animal"))
            if any(sig):
                out[(r, c)] = sig
    return out


def run(rec, his_seat, seed, upto):
    """Plays BOTH arms in lockstep, each in its own env, so the boards are comparable."""
    from kaggle_environments import make
    import importlib
    import breakdown as B
    import us_in_his_seat as U

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    cfg = dict(rec.get("configuration") or {})
    cfg.pop("seed", None)
    steps = rec["steps"]
    them = 1 - his_seat

    envs, boards = {}, {}
    for arm in ("tape", "ours"):
        e = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
        e.reset(2)
        envs[arm] = e
        boards[arm] = {}
    agent = SA.make_agent(sched, his_seat)

    per_day = {}
    detail = []
    crew = {}
    for t in range((upto + 1) * TPD):
        d, h = divmod(t, TPD)
        acts = {}
        for arm, e in envs.items():
            o = e.state[his_seat].observation
            if h == 0:
                boards[arm][d] = _cells(o["farms"][his_seat])
                crew.setdefault(d, {})[arm] = (
                    len(o["farms"][his_seat].get("hands") or []),
                    o["farms"][his_seat]["money"])
            n_us = len(o["farms"][his_seat].get("hands") or [])
            if arm == "ours":
                a = agent(o)
                acts[arm] = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                             "market": a["market"]}
            else:
                a = U._recorded(steps, t, his_seat)
                acts[arm] = {"farmer": a.get("farmer") or ["PASS"],
                             "hands": list(a.get("hands") or [])[:n_us],
                             "market": a.get("market") or []}

        if _norm(acts["ours"]) != _norm(acts["tape"]):
            per_day[d] = per_day.get(d, 0) + 1
            if 4 <= d <= upto and len(detail) < 12:
                detail.append((t, acts["tape"], acts["ours"]))

        for arm, e in envs.items():
            o = e.state[his_seat].observation
            n_them = len(o["farms"][them].get("hands") or [])
            at = U._recorded(steps, t, them)
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n_them],
                     "market": at.get("market") or []}
            mine = acts[arm]
            e.step([mine, yours] if his_seat == 0 else [yours, mine])
        if any(e.done for e in envs.values()):
            break
    return per_day, boards, detail, crew


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", default="97210773")
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--upto", type=int, default=8)
    a = ap.parse_args()

    import glob
    files = {}
    for dd in ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c",
               "leaders_2026-08-24", "kawa_2026-08-24", "losses", "top_guys", "top2",
               "new_leader", "ladder", "our_games"):
        for f in glob.glob(str(REPO / f"data/seed_scripts/{dd}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)
    for f in glob.glob("/Users/alexchilton/Downloads/*.json"):
        files.setdefault(pathlib.Path(f).stem, f)

    for ep in a.games.split(","):
        f = files.get(ep)
        if f is None:
            print(f"{ep}: not found", flush=True)
            continue
        rec = json.loads(pathlib.Path(f).read_text())
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            print(f"{ep}: {a.who} not in {names}", flush=True)
            continue
        seat = names.index(a.who)
        seed = (rec.get("info") or {}).get("seed")
        print(f"\n########## {ep}  seed {seed}  vs {names[1 - seat]}", flush=True)

        per_day, boards, detail, crew = run(rec, seat, seed, a.upto)

        print("\n  turns where OUR action differs from HIS recording,"
              "  and the crew and bank each arm holds at h0:")
        print(f"    {'':13}  {'diff':>4}      {'his crew':>8} {'our crew':>8}"
              f"   {'his bank':>9} {'our bank':>9}")
        for d in range(a.upto + 1):
            zone = "opening" if d <= 3 else "REPLAY"
            ct, cu = crew.get(d, {}).get("tape", (0, 0)), crew.get(d, {}).get("ours", (0, 0))
            print(f"    d{d:<2} {zone:>8}   {per_day.get(d, 0):>2}/24      "
                  f"{ct[0]:>8} {cu[0]:>8}   {ct[1]:>9,.0f} {cu[1]:>9,.0f}")

        print("\n  board cells that differ, at the START of each day:")
        for d in range(a.upto + 1):
            tb, ub = boards["tape"].get(d, {}), boards["ours"].get(d, {})
            keys = sorted(set(tb) | set(ub))
            bad = [k for k in keys if tb.get(k) != ub.get(k)]
            print(f"    d{d:<2}  {len(keys) - len(bad):>3} same  {len(bad):>3} diff")
            if bad and d == a.upto:
                for k in bad:
                    print(f"          {k}   his {tb.get(k)}   ours {ub.get(k)}")

        if detail:
            print("\n  differing turns INSIDE the replay window (d4+):")
            for t, his, ours in detail:
                d, h = divmod(t, TPD)
                print(f"    turn {t} = d{d} h{h}")
                print(f"      his   {his['farmer']}  hands {his['hands']}  mkt {his['market']}")
                print(f"      ours  {ours['farmer']}  hands {ours['hands']}  mkt {ours['market']}")
        else:
            print("\n  NO differing action inside the replay window -- the replay is exact,")
            print("  and any board gap at d8 was seeded at d3 and carried.")


if __name__ == "__main__":
    main()
