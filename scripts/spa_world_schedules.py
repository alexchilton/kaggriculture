"""One schedule per world, each from its OWN season, end to end, with the over-asks already gone.

The d7 gate is "the planner reproduces his d7 on every world". Testing that needs one arm per world,
and an arm is a PAIR: the replay that puts the board down through d6, and the rows the planner takes
over with. Those two must be the same season -- `scripts/schedule_guard.same_season` enforces it --
because rows from another season describe ground that is not there, and a PLANT or BUILD onto an
occupied tile is a silent no-op (`reference/kaggriculture.py:499`).

Everything the extraction used to get wrong is fixed at the source here, so there is no second step
to forget:

    seeds   the crop tally of `plants`, not his BUY_SEED orders -- he asks 1.41x the strawberry and
            1.62x the melon he plants, and the difference is the day's animal
    buys    what the engine SETTLED, via `kagg/analysis/fills.py` -- he offers WHEAT 48 at d7 on a
            world that fills 11
    sells   the same
    market  stamped "FILLS" in `meta.json`, which `schedule_guard` requires

Run this, then `scripts/d7_all_worlds.py`.
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

#: The eight first-shop branches and the season chosen for each, from
#: `data/seed_scripts/spataro/meta.json` -- the best bank inside the branch's own dominant d3-d5
#: placement skeleton, so a branch is represented by a season that plays it typically AND plays it
#: well. Read from that file rather than copied, so one rebuild moves both.
def worlds(meta_path):
    meta = json.loads(pathlib.Path(meta_path).read_text())
    out = {}
    for shop, d in meta["branches"].items():
        key = ("spa_" + shop.lower()
               .replace("_shop", "").replace("_store", "").replace("_spot", "")
               .replace("farmers_market", "fmarket").replace("ice_cream", "icecream"))
        out[key] = (int(d["episode"]), shop, d.get("dominant_d3_d5", ""))
    return out



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--landed", default="data/spataro_landed_rows.json")
    ap.add_argument("--meta", default="data/seed_scripts/spataro/meta.json")
    ap.add_argument("--team", default="SpaTaro")
    ap.add_argument("--replay-dir", default="data/replays_spa_sub")
    ap.add_argument("--out", default="data/seed_scripts")
    a = ap.parse_args()

    from scripts.tape_fills import animal_offers, tape_fills
    from scripts.schedule_guard import check, same_season

    L = {int(x["ep"]): x for x in json.loads((ROOT / a.landed).read_text())}
    for key, (ep, shop, skel) in sorted(worlds(ROOT / a.meta).items()):
        g = L.get(ep)
        if g is None:
            print(f"{key:14s} SKIP -- episode {ep} not in {a.landed}")
            continue
        replay = ROOT / a.replay_dir / f"{ep}.json"
        if not replay.exists():
            print(f"{key:14s} SKIP -- no replay at {replay}")
            continue
        f = tape_fills(str(replay), a.team)
        herd = animal_offers(str(replay), a.team)
        rows = {}
        for d, r in g["rows"].items():
            r = dict(r)
            r["buys"] = dict(f[int(d)].get("BUY_PRODUCT", {}))
            r["sells"] = dict(f[int(d)].get("SELL", {}))
            r["animals_bought"] = dict(herd.get(str(d)) or {})
            rows[d] = r
        out = ROOT / a.out / key
        out.mkdir(parents=True, exist_ok=True)
        sp = out / "schedule.json"
        sp.write_text(json.dumps(rows, indent=1, sort_keys=True))
        (out / "meta.json").write_text(json.dumps(
            {"episode": ep, "bank": g["bank"], "team": a.team, "branch": shop,
             "skeleton_d3_d5": skel, "market": "FILLS",
             "rows": "LANDED (scripts/spataro_landed_schedule.py); seeds are PLANTS",
             "market_from": {"replay": str(replay.relative_to(ROOT)),
                             "how": "kagg/analysis/fills.py wraps _commit_unit"},
             "source": "scripts/spa_world_schedules.py"}, indent=2))
        check(rows, sp)
        same_season(str(sp), str(replay))
        d7 = rows.get("7", {})
        # Bank is deliberately NOT printed. The gate is the BOARD -- same animals, same plants, same
        # pens, same feed and care -- and a money column next to it invites reading a season as good
        # when its board does not match. Alex: "forget the fucking bank".
        print(f"{key:14s} ep {ep}  {shop:15s} d7 plants {len(d7.get('plants') or []):>2}  "
              f"places {d7.get('places')}  builds {d7.get('builds')}  buys {d7.get('buys')}")
    print("\nall written and checked")


if __name__ == "__main__":
    main()
