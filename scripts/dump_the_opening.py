"""One pass over every kawashigi replay. Everything per day, ours and his, to one CSV.

Alex, 2026-08-24: *"why do you need to rerun all the time -- why not do it once right and store that
shit."* Fair. This exists so no later question needs another 35-game simulation.

Our agent plays HIS seat, on the game's OWN seed, against that game's recorded opponent. His column
is the same board driven by his recorded actions instead. Per game per day, both arms:

    bank            at h0 and at h23
    shed            FERTILIZER, WHEAT, MILK, WOOL, MELON, STRAWBERRY
    crew            hands owned at h12 -- NOT h0: `kaggriculture.py:880` clears `hands` at dawn and
                    respawns them during the day, so an h0 reading is always 0
    animals         count, and per tile `placed_day`, `yield_units`, `pending_care_bonus`
    tiles           crop counts on the board at h0
    ops             FEED, CARE, WATER, PLANT, HARVEST, DIG, COLLECT_FERTILIZER, PICKUP, PLACE
    orders          every market order, summed over the day, by type and product
    diff_turns      how many of the day's 24 turns our submitted action differs from his

Read it with pandas, or with csv.DictReader. Columns are `<arm>_<field>`; `arm` is `ours` or `his`.

    python -u scripts/dump_the_opening.py --upto 12
"""

import argparse
import collections
import csv
import glob
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
DIRS = ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c", "kawa_2026-08-24",
        "leaders_2026-08-24", "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
SHED = ("FERTILIZER", "WHEAT", "MILK", "WOOL", "MELON", "STRAWBERRY", "CARROT")
OPS = ("FEED", "CARE", "WATER", "PLANT", "HARVEST", "DIG", "COLLECT_FERTILIZER",
       "PICKUP", "PLACE", "BUILD_PASTURE", "BUILD_COOP", "PASS")


def _norm(a):
    return (tuple(a.get("farmer") or ["PASS"]),
            tuple(tuple(x) for x in (a.get("hands") or [])),
            tuple(sorted(tuple(x) for x in (a.get("market") or []))))


def _board(farm):
    crops, animals, weeds = collections.Counter(), {}, 0
    for y, row in enumerate(farm.get("tiles") or []):
        for x, t in enumerate(row):
            if not isinstance(t, dict):
                continue
            if t.get("crop"):
                crops[t["crop"]] += 1
            elif t.get("animal"):
                animals[(x, y)] = (t["animal"], t.get("placed_day"), t.get("yield_units", 0),
                                   t.get("pending_care_bonus", 0), t.get("consecutive_unfed", 0))
            elif t.get("kind") == "WEED":
                weeds += 1
    return crops, animals, weeds


def run(rec, seat, seed, upto):
    """Both arms, in lockstep, each in its own env. Returns `{(arm, day): row}`."""
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

    envs, out = {}, {}
    for arm in ("ours", "his"):
        e = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
        e.reset(2)
        envs[arm] = e
    agent = SA.make_agent(sched, seat)

    diff = collections.Counter()
    for t in range((upto + 1) * TPD):
        d, h = divmod(t, TPD)
        acts = {}
        for arm, e in envs.items():
            o = e.state[seat].observation
            farm = o["farms"][seat]
            priv = o.get("private") or {}
            n_us = len(farm.get("hands") or [])
            if arm == "ours":
                a = agent(o)
                act = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                       "market": a["market"]}
            else:
                a = U._recorded(steps, t, seat)
                act = {"farmer": a.get("farmer") or ["PASS"],
                       "hands": list(a.get("hands") or [])[:n_us],
                       "market": a.get("market") or []}
            acts[arm] = act

            key = (arm, d)
            r = out.setdefault(key, dict(arm=arm, day=d, ops=collections.Counter(),
                                         orders=collections.Counter(), crew=0))
            if h == 0:
                shed = collections.Counter(priv.get("shed") or {})
                crops, animals, weeds = _board(farm)
                r["bank_dawn"] = farm["money"]
                r["weeds"] = weeds
                r["n_animals"] = len(animals)
                r["animals"] = json.dumps({f"{x},{y}": v for (x, y), v in sorted(animals.items())})
                for k in SHED:
                    r[f"shed_{k}"] = shed[k]
                for k in ("WHEAT", "MELON", "STRAWBERRY", "CARROT"):
                    r[f"tiles_{k}"] = crops[k]
            if h == 12:
                r["crew"] = n_us
            if h == TPD - 1:
                r["bank_dusk"] = farm["money"]
            for op in [act["farmer"]] + list(act["hands"]):
                if op and op[0] in OPS:
                    r["ops"][op[0]] += 1
            for o_ in (act["market"] or []):
                if not o_:
                    continue
                # `HIRE` and `BUY_LAND` are single-element orders -- indexing `o_[1]` on those
                # raises, which is what emptied this CSV on the first run.
                key = o_[0] if len(o_) < 2 else f"{o_[0]} {o_[1]}"
                r["orders"][key] += int(o_[2]) if len(o_) >= 3 else 1

        if _norm(acts["ours"]) != _norm(acts["his"]):
            diff[d] += 1

        for arm, e in envs.items():
            o = e.state[seat].observation
            n_them = len(o["farms"][them].get("hands") or [])
            at = U._recorded(steps, t, them)
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n_them],
                     "market": at.get("market") or []}
            e.step([acts[arm], yours] if seat == 0 else [yours, acts[arm]])
        if any(e.done for e in envs.values()):
            break

    for (arm, d), r in out.items():
        r["diff_turns"] = diff.get(d, 0)
        r["ops"] = json.dumps(dict(r["ops"]))
        r["orders"] = json.dumps(dict(r["orders"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who", default="カワシギ")
    ap.add_argument("--upto", type=int, default=12)
    ap.add_argument("--out", default="data/logs/the_opening.csv")
    a = ap.parse_args()

    files = {}
    for d in DIRS:
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)

    out = REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    # **Header and flush per game, not at the end.** A sweep that writes only on completion loses
    # everything to a SIGKILL -- `feedback_write_results_incrementally`.
    fh = out.open("w", newline="")
    w = None
    t0 = time.time()
    n = 0
    for ep, f in sorted(files.items()):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                     # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if a.who not in names:
            continue
        seed = (rec.get("info") or {}).get("seed")
        if seed is None:
            continue
        seat = names.index(a.who)
        try:
            rows = run(rec, seat, seed, a.upto)
        except Exception as e:                                                # noqa: BLE001
            print(f"{ep:>10}  {e!r}", flush=True)
            continue
        for (arm, d), r in sorted(rows.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            r = dict(episode=ep, seed=seed, seat=seat, opponent=names[1 - seat], **r)
            if w is None:
                w = csv.DictWriter(fh, fieldnames=list(r))
                w.writeheader()
            w.writerow(r)
        fh.flush()
        n += 1
        print(f"{ep:>10}  done  ({n} games, {time.time() - t0:.0f}s)", flush=True)
    fh.close()
    print(f"\n{n} games -> {a.out}  ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
