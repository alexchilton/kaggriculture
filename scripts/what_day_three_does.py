"""Day 3's whole ledger, ours against his, in one pass over every kawashigi game.

Alex, 2026-08-24: *"does that mean we are then buying differing animals in d3, sheep or cow? And
that is 100 difference?"*

Two decisions land on d3 and only one of them is a latch:

    melon_branch.DECIDE_BY_DAY = 3     one-shot: picks which tape d4-d11 replays
    SHOP_ADAPT_FROM_DAY        = 3     re-decided every turn from here to the end of the season

The second re-labels COW as SHEEP or back, and `schedule_agent.py:5535` records the consequence --
"the bill, $400 against $500, so a swap can be refused on a thin bank". The d7 hire fails on a gap
of about $119, so a single swap is enough to explain it.

d3 is the one day inside d0-d11 that we still play ourselves: `REPLAY_OPENING_DAYS` covers d0-d2 and
d4-d11. At d3 h0 our bank and shed match his exactly in all 35 games, so everything below is a
difference d3 itself creates.

Writes one row per game to CSV -- animals bought, seeds bought, products bought and sold, hires,
and the bank and shed at both ends of the day -- so later questions read the file instead of
re-simulating.
"""

import collections
import csv
import glob
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

TPD = 24
DIRS = ("kawashigi", "kawashigi_b3", "kawashigi_q4", "kawashigi_q4c", "kawa_2026-08-24",
        "leaders_2026-08-24", "losses", "top_guys", "top2", "ladder", "our_games", "new_leader")
OUT = "data/logs/what_day_three_does.csv"


def _orders(a):
    return [list(o) for o in (a.get("market") or []) if o]


def _tally(orders):
    t = collections.Counter()
    for o in orders:
        if o[0] == "HIRE":
            t["HIRE"] += 1
        elif len(o) >= 3:
            t[f"{o[0]} {o[1]}"] += int(o[2])
    return t


def main():
    import importlib
    import breakdown as B
    import us_in_his_seat as U
    from kaggle_environments import make

    SA = importlib.import_module("kagg.search.schedule_agent")
    B.schedule_agent = SA
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY}
             for k, r in raw.items()}

    files = {}
    for d in DIRS:
        for f in glob.glob(str(REPO / f"data/seed_scripts/{d}/*.json")):
            files.setdefault(pathlib.Path(f).stem, f)

    rows = []
    print(f"{'episode':>10}  {'animals d3 his':>22}  {'animals d3 ours':>22}   "
          f"{'d3 dawn':>9}  {'d4 dawn his/ours':>18}  swap")
    for ep, f in sorted(files.items()):
        try:
            rec = json.loads(pathlib.Path(f).read_text())
        except Exception:                                                     # noqa: BLE001
            continue
        if not isinstance(rec, dict) or "steps" not in rec:
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        if "カワシギ" not in names:
            continue
        seat = names.index("カワシギ")
        seed = (rec.get("info") or {}).get("seed")
        if seed is None:
            continue
        steps = rec["steps"]
        them = 1 - seat
        cfg = dict(rec.get("configuration") or {})
        cfg.pop("seed", None)
        env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=False)
        env.reset(2)
        agent = SA.make_agent(sched, seat)

        ours_t, his_t = collections.Counter(), collections.Counter()
        dawn3 = dawn4 = None
        for t in range(4 * TPD + 1):
            o = env.state[seat].observation
            farm = o["farms"][seat]
            shed = collections.Counter((o.get("private") or {}).get("shed") or {})
            if t == 3 * TPD:
                h = steps[t][seat]["observation"]
                hs = collections.Counter((h.get("private") or {}).get("shed") or {})
                dawn3 = (h["farms"][seat]["money"], hs["FERTILIZER"],
                         farm["money"], shed["FERTILIZER"])
            if t == 4 * TPD:
                h = steps[t][seat]["observation"]
                hs = collections.Counter((h.get("private") or {}).get("shed") or {})
                dawn4 = (h["farms"][seat]["money"], hs["FERTILIZER"],
                         farm["money"], shed["FERTILIZER"])
                break
            n_us = len(farm.get("hands") or [])
            n_them = len(o["farms"][them].get("hands") or [])
            a = agent(o)
            mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us],
                    "market": a["market"]}
            if t // TPD == 3:
                ours_t += _tally(_orders(mine))
                his_t += _tally(_orders(U._recorded(steps, t, seat)))
            at = U._recorded(steps, t, them)
            yours = {"farmer": at.get("farmer") or ["PASS"],
                     "hands": list(at.get("hands") or [])[:n_them],
                     "market": at.get("market") or []}
            env.step([mine, yours] if seat == 0 else [yours, mine])
            if env.done:
                break

        def animals(t):
            return {k.split()[1]: v for k, v in t.items() if k.startswith("BUY_ANIMAL")}

        ha, oa = animals(his_t), animals(ours_t)
        swap = "SWAP" if ha != oa else ""
        rows.append(dict(episode=ep, seed=seed,
                         his_animals=json.dumps(ha), our_animals=json.dumps(oa),
                         his_hires=his_t["HIRE"], our_hires=ours_t["HIRE"],
                         d3_bank_his=dawn3[0], d3_fert_his=dawn3[1],
                         d3_bank_ours=dawn3[2], d3_fert_ours=dawn3[3],
                         d4_bank_his=dawn4[0], d4_fert_his=dawn4[1],
                         d4_bank_ours=dawn4[2], d4_fert_ours=dawn4[3],
                         his_all=json.dumps(dict(his_t)), our_all=json.dumps(dict(ours_t))))
        print(f"{ep:>10}  {str(ha):>22}  {str(oa):>22}   "
              f"${dawn3[0]:>8,.0f}  ${dawn4[0]:>7,.0f}/${dawn4[2]:<7,.0f}  {swap}", flush=True)

    out = REPO / OUT
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    n = sum(1 for r in rows if r["his_animals"] != r["our_animals"])
    print(f"\n{len(rows)} games. d3 animal purchase differs in {n}.")
    print(f"hires on d3 differ in {sum(1 for r in rows if r['his_hires'] != r['our_hires'])}.")
    print(f"rows -> {OUT}")


if __name__ == "__main__":
    main()
