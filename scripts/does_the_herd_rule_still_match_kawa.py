"""Predict カワシギ's cow/sheep split from his town's shops, and score each rule against it.

Alex, 2026-08-25: *"if the algo doesnt match kawa then it was wrong in the first place."*

`WOOL_SHOP_SETS_THE_HERD` was fitted to his recorded seats, so any replacement has to clear the same
bar before it can ship. This scores three rules on his archived games:

    ship          the shipped presence test -- YARN_STORE in the first three draws caps cows at
                  `WOOL_SHOP_COW_CAP`, otherwise `WOOL_SHOP_NO_YARN_COW`.
    greedy        `WOOL_SHOP_SETS_THE_HERD = False`, so `_herd_split` falls through to the
                  drain-aware block at `schedule_agent.py:3021` that already exists.
    proportional  sheep:cow straight off the wool:milk drain ratio.

Each rule is driven the way the agent drives it: once per day, fed the shops unlocked ON that day
and the split it has committed to so far, so an early decision constrains a later one exactly as
`bought` does in the live agent. His FINAL head count is used as `want_total`, because every rule
here keeps the schedule's count and only moves the species mix.

A rule is scored on the final COW count. `exact` is COW predicted == COW observed.

    python -u scripts/does_the_herd_rule_still_match_kawa.py --limit 80
"""

import argparse
import collections
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

TPD = 24
KAWA = "カワシギ"
DIRS = ("downloads_2026-08-14to16", "downloads_2026-08-13", "downloads_2026-08-19",
        "downloads_2026-08-20", "downloads_2026-08-21")


def drain_per_tick(shops, product):
    import kaggle_environments.envs.kaggriculture.kaggriculture as KG

    return sum(2 if len(KG.SHOPS.get(s, ())) == 1 else 1
               for s in shops if product in KG.SHOPS.get(s, ()))


def _predict(mod, shops_by_day, total, rule):
    """Walk the season a day at a time, carrying the committed split forward as `bought`."""
    bought = {"COW": 0, "SHEEP": 0}
    for day in range(30):
        seen = shops_by_day[day]
        # `_herd_split` reads only the SUM of this dict, so the way it is halved does not matter.
        want = {"COW": total // 2, "SHEEP": total - total // 2}
        if rule == "proportional":
            wool, milk = drain_per_tick(seen, "WOOL"), drain_per_tick(seen, "MILK")
            split = dict(bought)
            split["COW"] = max(split["COW"], min(mod.HERD_FLOOR_COW, total))
            split["SHEEP"] = max(split["SHEEP"], min(mod.HERD_FLOOR_SHEEP,
                                                    total - split["COW"]))
            if wool + milk > 0:
                sheep_t = int(round(total * wool / float(wool + milk)))
                cow_t = total - sheep_t
                split["COW"] = max(split["COW"], min(cow_t, total))
                split["SHEEP"] = max(split["SHEEP"], min(sheep_t, total - split["COW"]))
        else:
            split = mod._herd_split(want, bought, day, 0, seen)
        bought = {a: max(bought[a], split.get(a, 0)) for a in ("COW", "SHEEP")}
        if bought["COW"] + bought["SHEEP"] >= total:
            break
    return bought


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=80)
    a = ap.parse_args()

    from kagg.analysis import replay_fills as RF
    import kagg.search.schedule_agent as SA

    paths = []
    for d in DIRS:
        paths += sorted(glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")))

    rows = []
    for p in paths:
        if len(rows) >= a.limit:
            break
        try:
            rec = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if KAWA not in names:
            continue
        seat = names.index(KAWA)
        herd = RF.animals_alive(rec, seat)
        cow, sheep = int(herd.get("COW", 0)), int(herd.get("SHEEP", 0))
        total = cow + sheep
        if total <= 0:
            continue
        steps = rec["steps"]
        shops_by_day = []
        for day in range(30):
            t = min(day * TPD, len(steps) - 1)
            o = (steps[t][0] or {}).get("observation") or {}
            shops_by_day.append(list((o.get("town") or {}).get("unlocked_shops") or []))
        final = shops_by_day[-1]
        rows.append({
            "game": pathlib.Path(p).stem, "cow": cow, "sheep": sheep, "total": total,
            "wool": drain_per_tick(final, "WOOL"), "milk": drain_per_tick(final, "MILK"),
            "early": "YARN_STORE" in final[:SA.WOOL_SHOP_DRAW_LIMIT],
            "shops_by_day": shops_by_day,
        })
        print(f"  {len(rows):>3}  {rows[-1]['game']:<12} COW {cow:>3} SHEEP {sheep:>3}"
              f"   wool {rows[-1]['wool']} milk {rows[-1]['milk']}"
              f"   early_yarn {rows[-1]['early']}", flush=True)

    if not rows:
        print("No カワシギ games found. Nothing measured -- do not draw a conclusion from this.")
        return

    print(f"\n{len(rows)} カワシギ seats\n")
    print(f"{'rule':<14}{'exact COW':>11}{'within 1':>10}{'mean |err|':>12}")
    preds = {}
    for rule in ("ship", "greedy", "proportional"):
        mod = SA
        if rule == "greedy":
            # A private copy so the shipped module keeps its constant.
            import importlib.util
            import kagg.search  # noqa: F401
            spec = importlib.util.spec_from_file_location(
                "kagg.search._kawa_arm", REPO / "kagg/search/schedule_agent.py")
            mod = importlib.util.module_from_spec(spec)
            sys.modules["kagg.search._kawa_arm"] = mod
            spec.loader.exec_module(mod)
            mod.WOOL_SHOP_SETS_THE_HERD = False
        errs, exact, near = [], 0, 0
        got = []
        for r in rows:
            pred = _predict(mod, r["shops_by_day"], r["total"], rule)
            e = abs(pred["COW"] - r["cow"])
            errs.append(e)
            exact += e == 0
            near += e <= 1
            got.append(pred["COW"])
        preds[rule] = got
        n = len(rows)
        print(f"{rule:<14}{exact / n * 100:>10.0f}%{near / n * 100:>9.0f}%"
              f"{sum(errs) / n:>12.2f}")

    print(f"\nper-seat COW: observed vs each rule\n")
    print(f"{'game':<12}{'wool':>5}{'milk':>5}{'obs':>5}{'ship':>6}{'greedy':>8}{'prop':>6}")
    for i, r in enumerate(rows):
        print(f"{r['game']:<12}{r['wool']:>5}{r['milk']:>5}{r['cow']:>5}"
              f"{preds['ship'][i]:>6}{preds['greedy'][i]:>8}{preds['proportional'][i]:>6}")

    by = collections.Counter((r["wool"], r["milk"]) for r in rows)
    print(f"\nhis towns by (wool drain, milk drain): {dict(by)}")


if __name__ == "__main__":
    main()
