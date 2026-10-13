"""A MATRIX-driven schedule per world, so the matrix is inside the d7 gate and not beside it.

Two things have to reproduce his day, and today only one of them is being tested:

    the schedules   one recorded season's LANDED rows per world          -- `spa_world_schedules.py`
    the matrix      amounts predicted from the SHOPS, no season attached  -- this file

Alex: "dont forget as well we have the schedules but also the matrices which pass different amounts -
they need to all be part of the matching."

The matrix (`scripts/spa_targets.py`) predicts his board quantities per (day, quantity) from which
shops are open, and `targets_to_schedule.build` differences those into rows. Here that is done with
the REAL unlock timeline of each recorded world, so the arm is the matrix answering the question his
own season answered, on the same board, comparable cell for cell against the same replay.

Days before `--start-day` come from that world's landed rows, because d0-d2 happen before the first
shop opens and there is nothing for a shop model to condition on. From `--start-day` the amounts are
the matrix's. Market rows are carried from the landed-with-fills schedule -- the matrix predicts the
BOARD, not the order book, and his offers must never come back in (`scripts/schedule_guard.py`).
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def unlock_timeline(ep, plan_rows="data/spataro_plan_rows.json"):
    """`[(day, shop)]` as that season actually opened them."""
    rows = json.loads((ROOT / plan_rows).read_text())
    for p in rows:
        if int(p["ep"]) == int(ep):
            return [(int(d), s) for d, s in sorted(p["unlocks"])]
    raise KeyError(f"episode {ep} has no unlock timeline in {plan_rows}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worlds", default="data/seed_scripts", help="where spa_<world>/ dirs live")
    ap.add_argument("--meta", default="data/seed_scripts/spataro/meta.json")
    ap.add_argument("--out-suffix", default="_mx")
    ap.add_argument("--start-day", type=int, default=3)
    ap.add_argument("--alpha", type=float, default=1.0)
    a = ap.parse_args()

    from scripts.spa_targets import load, Ridge
    from scripts.targets_to_schedule import build
    from scripts.spa_world_schedules import worlds
    from scripts.schedule_guard import check

    seasons = load()
    model = Ridge(a.alpha).fit(seasons)
    print(f"ridge fitted on {len(seasons)} seasons, start_day {a.start_day}\n")

    for key, (ep, shop, _skel) in sorted(worlds(ROOT / a.meta).items()):
        src = ROOT / a.worlds / key
        if not (src / "schedule.json").exists():
            print(f"{key:14s} SKIP -- no landed schedule at {src}")
            continue
        base = json.loads((src / "schedule.json").read_text())
        sched = build(model, unlock_timeline(ep), base, a.start_day)
        # The matrix predicts the board. Market rows stay the measured FILLS from the landed
        # schedule, so this arm differs from its neighbour in AMOUNTS only -- which is the thing
        # being tested.
        for d, r in sched.items():
            r["buys"] = dict((base.get(d) or {}).get("buys") or {})
            r["sells"] = dict((base.get(d) or {}).get("sells") or {})
        out = ROOT / a.worlds / f"{key}{a.out_suffix}"
        out.mkdir(parents=True, exist_ok=True)
        sp = out / "schedule.json"
        sp.write_text(json.dumps(sched, indent=1, sort_keys=True))
        (out / "meta.json").write_text(json.dumps(
            {"episode": ep, "team": "SpaTaro", "branch": shop, "market": "FILLS",
             "rows": f"MATRIX (ridge) from d{a.start_day}; d0-d{a.start_day - 1} from the landed rows",
             "source": "scripts/spa_matrix_worlds.py",
             "why": "puts the matrix inside the d7 gate -- same board, same replay, amounts from the "
                    "shop model instead of from the recorded season"}, indent=2))
        check(sched, sp)
        d7 = sched.get("7", {})
        print(f"{key}{a.out_suffix:4s} ep {ep}  {shop:15s} d7 plants {len(d7.get('plants') or []):>2}  "
              f"places {d7.get('places')}  pens {d7.get('pens')}")
    print("\nall written and checked")


if __name__ == "__main__":
    main()
