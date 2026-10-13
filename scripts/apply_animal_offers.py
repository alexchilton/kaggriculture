"""Set `animals_bought` from his BUY_ANIMAL ORDERS on the schedules already on disk.

`scripts/spa_world_schedules.py` and `scripts/spataro_branch_schedules.py` now take this field from
`tape_fills.animal_offers`, so a full rebuild gets it. This applies the SAME field to the current
files without a rebuild, because rebuilding also pulls unrelated upstream changes into the rows
(`waters`, `harvests` appeared in `branches.json`) and a measurement of the animal rule must not
carry those.

    python -u scripts/apply_animal_offers.py            # report only
    python -u scripts/apply_animal_offers.py --write
"""
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.tape_fills import animal_offers
import scripts.breakdown as B


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    for tape in sorted(k for k in B.TAPES if k.startswith("spa")):
        replay, sched_path, team = B.TAPES[tape]
        offers = animal_offers(str(ROOT / replay), team)
        p = ROOT / sched_path
        sched = json.loads(p.read_text())
        changed = []
        for d, row in sched.items():
            want = dict(offers.get(str(d)) or {})
            if dict(row.get("animals_bought") or {}) != want:
                changed.append(f"d{d} {dict(row.get('animals_bought') or {})}->{want}")
                row["animals_bought"] = want
        if a.write and changed:
            p.write_text(json.dumps(sched, indent=1, sort_keys=True))
        print(f"{tape:14s} {len(changed):>2} days  {' '.join(changed[:6])}")

    # The eight branch rows the router falls back to, from the same season each branch names.
    meta = json.loads((ROOT / "data/seed_scripts/spataro/meta.json").read_text())
    bp = ROOT / "data/seed_scripts/spataro/branches.json"
    branches = json.loads(bp.read_text())
    n = 0
    for shop, rows in branches.items():
        ep = meta["branches"][shop]["episode"]
        rp = next((ROOT / d / f"{ep}.json" for d in ("data/replays_spa_sub", "data/replays")
                   if (ROOT / d / f"{ep}.json").exists()), None)
        if rp is None:
            print(f"  branch {shop}: no replay for ep {ep} -- left alone")
            continue
        offers = animal_offers(str(rp), "SpaTaro")
        for d, row in rows.items():
            want = dict(offers.get(str(d)) or {})
            if dict(row.get("animals_bought") or {}) != want:
                row["animals_bought"] = want
                n += 1
    if a.write:
        bp.write_text(json.dumps(branches, indent=1))
    print(f"branches.json: {n} rows")


if __name__ == "__main__":
    main()
