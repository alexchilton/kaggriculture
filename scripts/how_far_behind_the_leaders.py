"""A regression bench against top-finisher tapes, reporting DELTA rather than win rate.

**Why delta and not wins.** The 97-game rematch resolves to +/-3 games, which is noise for anything
worth ~$2,000 -- three arms measured on 2026-08-16 all landed inside that band and were reverted on
a signal that could not distinguish them. These 14 games are against the strongest recorded
opponents (`somewhere after` at 160k, Victor @ Tufa Labs, THUNDER THUNDER, Ueddy), and the mean
bank delta over them is continuous, so a change that moves us $2,000 closer shows up as $2,000.

Our agent takes the loser's seat; the WINNER's recorded actions play theirs, on the game's own seed.
Read the DELTA against a previous run of this same bench, never the level.

    python -u scripts/how_far_behind_the_leaders.py
    ARM=penspots python -u scripts/how_far_behind_the_leaders.py
"""
import collections, glob, importlib, json, os, pathlib, statistics, sys
REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
import breakdown as B
from kaggle_environments import make
SA = importlib.import_module("kagg.search.schedule_agent"); B.schedule_agent = SA
TPD = 24
DIRS = (os.environ.get("DIRS") or "new_leader,top2").split(",")

#: Arms are attribute overrides only -- anything needing a code edit is not expressible here and
#: should be a local uncommitted change instead.
ARMS = {
    "base": {},
    "penspots": {"PEN_SPOTS": ((4, 4), (4, 3), (3, 3), (3, 4), (2, 4), (4, 2),
                               (5, 4), (5, 3), (6, 4), (6, 3))},
    "cowcap4": {"WOOL_SHOP_COW_CAP": 4},
    "cowcap8": {"WOOL_SHOP_COW_CAP": 8},
    "sell12": {"LATE_SELL_FROM_HOUR": 12},
    "sell20": {"LATE_SELL_FROM_HOUR": 20},
}
arm = os.environ.get("ARM", "base")
for k, v in ARMS[arm].items():
    setattr(SA, k, v)

raw_s = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY} for k, r in raw_s.items()}

games = []
for d in DIRS:
    for p in sorted(glob.glob(str(REPO / "data/seed_scripts" / d / "*.json"))):
        try:
            rec = json.loads(pathlib.Path(p).read_text())
        except Exception:
            continue
        if not isinstance(rec, dict) or len(rec.get("steps") or []) < 700:
            continue
        info = rec.get("info") or {}
        names = info.get("TeamNames") or []
        rw = rec.get("rewards") or []
        if len(names) < 2 or len(rw) < 2 or rw[0] is None or rw[1] is None:
            continue
        win = 0 if rw[0] >= rw[1] else 1
        games.append((str(info.get("EpisodeId") or pathlib.Path(p).stem), p,
                      info.get("seed"), names[win], rw[win], win))

print(f"ARM={arm}   {ARMS[arm] if ARMS[arm] else '(shipped)'}")
print(f"{len(games)} leader games from {','.join(DIRS)}\n")
print(f"{'episode':>10} {'opponent':>22} {'ours':>10} {'theirs':>10} {'delta':>10}")
deltas, per = [], collections.defaultdict(list)
for ep, p, seed, wname, wscore, wseat in games:
    rec = json.loads(pathlib.Path(p).read_text())
    cfg = dict(rec.get("configuration") or {}); cfg.pop("seed", None)
    steps = rec["steps"]; our = 1 - wseat
    env = make("kaggriculture", configuration=dict(cfg, seed=seed), debug=True)
    env.reset(2); agent = SA.make_agent(sched, our)
    for t in range(30 * TPD):
        o = env.state[our].observation
        a = agent(o)
        th = steps[t + 1][wseat].get("action") if t + 1 < len(steps) else None
        if not isinstance(th, dict):
            th = {"farmer": ["PASS"], "hands": [], "market": []}
        n_us = len(o["farms"][our].get("hands") or [])
        n_th = len(o["farms"][wseat].get("hands") or [])
        mine = {"farmer": a["farmer"], "hands": list(a["hands"] or [])[:n_us], "market": a["market"]}
        yours = {"farmer": th.get("farmer") or ["PASS"],
                 "hands": list(th.get("hands") or [])[:n_th], "market": th.get("market") or []}
        env.step([mine, yours] if our == 0 else [yours, mine])
        if env.done:
            break
    f = env.state[0].observation["farms"]
    us, them = f[our]["money"], f[wseat]["money"]
    deltas.append(us - them); per[wname].append(us - them)
    print(f"{ep:>10} {wname:>22} {us:>10,.0f} {them:>10,.0f} {us - them:>+10,.0f}", flush=True)
print(f"\n  wins {sum(1 for d in deltas if d > 0)}/{len(deltas)}")
print(f"  MEAN DELTA   {statistics.mean(deltas):>+10,.0f}      <- the bench number")
print(f"  median       {statistics.median(deltas):>+10,.0f}")
print(f"  worst        {min(deltas):>+10,.0f}")
for who, ds in sorted(per.items(), key=lambda kv: statistics.mean(kv[1])):
    print(f"    {who:>22} n={len(ds)}  mean {statistics.mean(ds):>+9,.0f}")
