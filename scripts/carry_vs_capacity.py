"""Does his DELIVERY priority follow the world's book, or is it the same every game?

Capacity varies enormously by town -- WOOL 30 in one of the nine gate worlds and 894 in another,
CARROT 18x, TOMATO 11x -- while MELON is 30 everywhere and FERTILIZER 0 everywhere. So if delivery
is value-driven, the carry% of a crop should FALL where that crop's book is deep (worth getting to
market) and RISE where the town cannot absorb it. If it is tape-driven, carry% is the same whatever
the shops.

carry% = turn-weighted units sitting in unit inventories / (inventories + shed). High means the
goods ride around unsellable.

    python -u scripts/carry_vs_capacity.py Majkel1337 mtmr_s1
"""
import collections, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import kaggle_environments.envs.kaggriculture.kaggriculture as K

DIRS = ["data/replays_2026-09-07", "data/replays_2026-09-08", "data/replays_2026-09-09",
        "data/replays_2026-09-11", "data/replays_hayashi", "data/replays_spa_sub"]
PR = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]


def episodes_with(team):
    seen, out = set(), []
    for d in DIRS:
        for p in sorted((ROOT / d / "summaries").glob("*.summary.json")):
            r = json.loads(p.read_text())
            if r["episode"] in seen:
                continue
            seen.add(r["episode"])
            if team in r["teams"] and (ROOT / d / f"{r['episode']}.json").exists():
                out.append((ROOT / d / f"{r['episode']}.json", r["teams"].index(team)))
    return out


def main():
    for team in sys.argv[1:] or ["Majkel1337"]:
        eps = episodes_with(team)
        print(f"\n=== {team}: {len(eps)} episodes ===")
        print(f"{'episode':>10} {'crop':11}{'capacity':>9}{'carry%':>8}{'shed':>9}")
        pairs = collections.defaultdict(list)
        for path, seat in eps:
            rep = json.loads(path.read_text())
            cap = collections.Counter()
            carry, shed = collections.Counter(), collections.Counter()
            for t, step in enumerate(rep["steps"]):
                shops = (((step[0] or {}).get("observation") or {}).get("town") or {}).get(
                    "unlocked_shops") or []
                if t % 4 == 0:
                    for n in shops:
                        pr = K.SHOPS.get(n) or []
                        m = 2 if len(pr) == 1 else 1
                        for it in pr:
                            cap[it] += m
                if t % 24 == 0:
                    for it in K.TOWN_CENTER_PRODUCTS:
                        cap[it] += 1
                priv = (((step[seat] if seat < len(step) else None) or {})
                        .get("observation") or {}).get("private") or {}
                for iv in priv.get("inventories") or []:
                    for k, v in (iv or {}).items():
                        carry[k] += int(v or 0)
                for k, v in (priv.get("shed") or {}).items():
                    shed[k] += int(v or 0)
            for p in PR:
                tot = carry[p] + shed[p]
                if tot < 200:
                    continue
                pct = 100 * carry[p] / tot
                pairs[p].append((cap[p], pct))
                print(f"{path.stem:>10} {p:11}{cap[p]:>9,}{pct:>8.0f}{shed[p]:>9,}")
        print(f"\n{'crop':12}{'capacity range':>18}{'carry% range':>16}   reads the world?")
        for p in PR:
            v = pairs.get(p) or []
            if len(v) < 2:
                continue
            caps = [c for c, _ in v]
            pcts = [x for _c, x in v]
            spread = max(caps) / max(1, min(caps))
            verdict = ("capacity flat -- cannot tell" if spread < 1.5
                       else "YES, falls as book deepens"
                       if (max(pcts) - min(pcts)) > 15 and
                          (caps[pcts.index(max(pcts))] < caps[pcts.index(min(pcts))])
                       else "no -- same whatever the shops")
            print(f"{p:12}{f'{min(caps):,}-{max(caps):,}':>18}"
                  f"{f'{min(pcts):.0f}-{max(pcts):.0f}%':>16}   {verdict}")


if __name__ == "__main__":
    main()
