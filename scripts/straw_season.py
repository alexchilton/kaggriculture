"""Straw-branch season totals: weeds, strawberry tiles, money. For judging d12+ changes.

The d0-d8 grid cannot see a fix that only touches the solved days, and the strawberry deaths this
project cares about start at d12-d14. This runs the branch armed, whole season, several seeds.
"""
import argparse, collections, importlib, json, pathlib, sys
REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(REPO / "scripts"))
B3 = "data/seed_scripts/kawashigi/92466371.json"
A3 = "data/seed_scripts/kawashigi/92498144.json"
TEAM = "カワシギ"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("straw", "melon"), default="straw")
    ap.add_argument("--seeds", default="3,7,11,23")
    ap.add_argument("--weeds", type=float, default=0.005)
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()
    import breakdown as B
    from kagg.search import melon_branch as _MB
    SA = importlib.import_module("kagg.search.schedule_agent"); B.schedule_agent = SA
    _MB.OPPONENT_MELON = 0 if a.arm == "straw" else 99
    raw = json.loads((REPO / "data/seed_scripts/kawashigi/schedule.json").read_text())
    sched = {int(k): {kk: vv for kk, vv in r.items() if kk not in B.TAPE_ONLY} for k, r in raw.items()}
    replay = str(REPO / (B3 if a.arm == "straw" else A3))
    economy, shops = B.env_config(replay), B.recorded_shops(replay)
    print(f"arm {a.arm!r}, weeds {a.weeds}, {a.days} days\n")
    print(f"{'seed':>5}{'money':>12}{'weeds d29':>11}{'straw d29':>11}{'melon d29':>11}{'WATER':>8}")
    tot = collections.Counter()
    for s in [int(x) for x in a.seeds.split(",")]:
        opp = lambda: B.tape_policy(replay, TEAM, 1)
        def ours():
            ag = SA.make_agent(sched, 0)
            return lambda o, t: ag(o)
        d, ops, _c, _dd = B.run(ours, opp, s, a.weeds, stop_day=a.days,
                                economy=economy, shops=shops)
        last = a.days - 1
        w = sum(ops[x]["WATER"] for x in range(a.days))
        print(f"{s:>5}{round(d[last].get('money',0)):>12,}{d[last].get('weed',0):>11}"
              f"{d[last].get('crop_STRAWBERRY',0):>11}{d[last].get('crop_MELON',0):>11}{w:>8}")
        tot["money"] += d[last].get("money", 0); tot["weed"] += d[last].get("weed", 0)
        tot["straw"] += d[last].get("crop_STRAWBERRY", 0); tot["water"] += w
    n = len(a.seeds.split(","))
    print(f"\n  mean money {tot['money']/n:,.0f}   total weeds {tot['weed']}   "
          f"total straw {tot['straw']}   total water {tot['water']}")

if __name__ == "__main__":
    main()
