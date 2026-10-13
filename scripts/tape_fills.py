"""What his tape ACTUALLY traded, per day and per product, measured by the engine.

The market rows in `spataro_landed_rows.json` are what he OFFERED. The engine drops what the bank
cannot cover, silently, and he plays on -- so the offer is a ceiling he does not reach and copying it
makes our planner spend money he never spent. Measured on the d7 handover, seed 666671489, with
`buys {WHEAT: 24}` in the row:

    fill.buy_product   ours 23   his 6          cash.product   ours $745   his $192
    shed_wheat         ours 19   his 2          fill.hire      ours  5     his   7
    water              ours 14   his 26         buy_animal     ours  0     his   1

$553 of wheat we did not need bought two hires fewer and twelve waterings fewer, and left nothing
for the $400 COW.

`kagg/analysis/fills.py` wraps `_commit_unit`, the one function that moves shed and money together,
so this is per-unit ground truth rather than a proxy -- read that module's docstring for the three
proxies this project has already got wrong. Seat 0 only; his opponent is not our business.

Writes `buys` and `sells` back into a schedule, replacing the offered numbers with the filled ones.
`seeds` is NOT touched here: it comes from `plants` in `spataro_landed_schedule.py`, which is the
ground the crop stands on and needs no engine run.
"""
import argparse, collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import scripts.breakdown as B


def tape_fills(replay_path, team, seed=11):
    from kaggle_environments import make
    from kagg.analysis.fills import record_fills

    economy = B.env_config(replay_path)
    shops = B.recorded_shops(replay_path)
    cfg = dict(economy, seed=seed, weedSpawnChance=0.0)
    env = make("kaggriculture", configuration=cfg, debug=True)
    env.reset(2)
    p0 = B.tape_policy(replay_path, team, 0)
    p1 = B.tape_policy(replay_path, team, 1)
    with record_fills(env) as fills:
        for t in range(719):
            o0, o1 = env.state[0].observation, env.state[1].observation
            o0.town["unlocked_shops"] = list(shops(t))
            env.step([p0(o0, t), p1(o1, t)])
    if fills.unattributed:
        raise RuntimeError(f"{fills.unattributed} fills unattributed -- the seat map is broken")
    out = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for e in fills.events:
        if e["seat"] != 0:
            continue
        out[int(e["day"])][e["op"]][e["item"]] += 1
    return out



def animal_offers(replay_path, team):
    """His BUY_ANIMAL ORDERS, per day -- the offer, not the fill.

    Every other market row is a fill, deliberately: he offers WHEAT 48 at d7 on a world that fills
    11, and obeying the offer spends the day's animal. The herd is the one place the OFFER is the
    right input, and it is measured, not argued. On all nine worlds at d7 he offers two head ONCE,
    at hour 0, and never again that day. One fills on eight of them and none on FARMERS_MARKET,
    because the sells settling in the same turn do not cover the second.

    `_do_buy_*` re-checks the bank per unit (`reference/kaggriculture.py:666-673`), so the second
    head costs nothing when it is refused and lands whenever the turn's sales run ahead of his.
    Recording the fill throws that redundancy away: every row asked for one head, and FARMERS_MARKET
    -- where both were refused -- asked for no animal at all.
    """
    rep = json.loads(pathlib.Path(replay_path).read_text())
    seat = rep["info"]["TeamNames"].index(team)
    out = {}
    for i, step in enumerate(rep["steps"]):
        if i == 0:
            continue
        for o in (((step[seat] or {}).get("action") or {}).get("market") or []):
            if o and o[0] == "BUY_ANIMAL":
                out.setdefault(str((i - 1) // 24), collections.Counter())[o[1]] += (
                    int(o[2]) if len(o) > 2 else 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", default="data/replays_spa_sub/107068412.json")
    ap.add_argument("--team", default="SpaTaro")
    ap.add_argument("--schedule", default="data/seed_scripts/spataro/schedule.json")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--write", action="store_true", help="write buys/sells back into the schedule")
    a = ap.parse_args()

    f = tape_fills(a.replay, a.team, a.seed)
    sched = json.loads(pathlib.Path(a.schedule).read_text())
    print(f"{'day':>4} {'buys OFFERED':>22} {'buys FILLED':>22}   {'sells OFFERED':>26} {'sells FILLED':>26}")
    for d in sorted(sched, key=int):
        r = sched[d]
        fb = dict(f[int(d)].get("BUY_PRODUCT", {}))
        fs = dict(f[int(d)].get("SELL", {}))
        print(f"{d:>4} {str(r.get('buys')):>22} {str(fb):>22}   {str(r.get('sells')):>26} {str(fs):>26}")
        if a.write:
            r["buys"], r["sells"] = fb, fs
    if a.write:
        sp = pathlib.Path(a.schedule)
        sp.write_text(json.dumps(sched, indent=1, sort_keys=True))
        # **Stamp it.** `scripts/schedule_guard.py` refuses a schedule without this, so a stale or
        # hand-made file cannot quietly reintroduce his offers. Written here and nowhere else.
        mp = sp.parent / "meta.json"
        meta = json.loads(mp.read_text()) if mp.exists() else {}
        meta["market"] = "FILLS"
        meta["market_from"] = {"replay": a.replay, "team": a.team, "seed": a.seed,
                               "how": "kagg/analysis/fills.py wraps _commit_unit -- per-unit truth"}
        mp.write_text(json.dumps(meta, indent=2))
        print(f"\nwrote {a.schedule} and stamped {mp}")


if __name__ == "__main__":
    main()
