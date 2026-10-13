"""One REAL season per demand cluster, not a generated one.

Measured 2026-09-11, 96 games each against shop0909: routing to the five MODEL-GENERATED cluster
schedules (`scripts/targets_to_schedule.py`) scored a mean bank of $67,739 against $79,679 for the
single real season -- **minus $11,940 for adding the routing**.

The likely reason, and it is structural rather than a tuning miss: a generated row is a per-day
MEDIAN, so the rows need not be consistent with each other. A plant count that its own `seeds` row
cannot supply, a herd that outpaces the money the same rows raise, a sell that assumes stock a
different day's median produced. A recorded season's landed rows are consistent by construction --
they happened, on one board, in one order, with one bank paying for all of it.

So the cluster carries a real season: the best-banking one that opens on that cluster's shops AND
plays the cluster's own dominant d3-d5 placement sequence, so it is typical of the cluster as well
as good. Rows are the LANDED ones (`scripts/spataro_landed_schedule.py`) -- what his board did, not
what he ordered, since he over-requests BUY_LAND in 162 of 179 seasons.

The matrix is not discarded by this. It is what says the clusters are real and what the amounts in
each should be; this file just stops it writing the rows.
"""
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.spa_targets import CLUSTERS, SHOP_CLUSTER

SEASON = 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--landed", default="data/spataro_landed_rows.json")
    ap.add_argument("--flows", default="data/spataro_plan_rows.json")
    ap.add_argument("--out-dir", default="data/seed_scripts/spa_real")
    args = ap.parse_args()

    L = json.loads((ROOT / args.landed).read_text())
    unlocks = {p["ep"]: p["unlocks"] for p in json.loads((ROOT / args.flows).read_text())}

    def skel(s, a, b):
        out = []
        for d in range(a, b):
            out += s["rows"][str(d)]["places"]
        return tuple(out)

    by_cluster = defaultdict(list)
    for s in L:
        first = next((sh for d, sh in sorted(unlocks.get(s["ep"]) or []) if d <= 3), None)
        c = SHOP_CLUSTER.get(first)
        if c:
            by_cluster[c].append(s)

    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {}
    print(f"{'cluster':12} {'n':>4} {'dominant':>9} {'on it':>6} {'episode':>11} {'bank':>10}")
    for cluster in CLUSTERS:
        seasons = by_cluster.get(cluster) or []
        if not seasons:
            raise SystemExit(f"no seasons for cluster {cluster!r}")
        dom = Counter(skel(s, 3, 6) for s in seasons).most_common(1)[0][0]
        pool = sorted((s for s in seasons if skel(s, 3, 6) == dom), key=lambda s: -s["bank"])
        pick = pool[0] if pool else sorted(seasons, key=lambda s: -s["bank"])[0]
        rows = {str(d): {k: v for k, v in pick["rows"][str(d)].items() if k != "escapes"}
                for d in range(SEASON)}
        (out_dir / f"{cluster}.json").write_text(json.dumps(rows, indent=1))
        herd = Counter()
        crops = Counter()
        land = 0
        for d in range(SEASON):
            herd.update(rows[str(d)]["animals_bought"])
            crops.update(rows[str(d)]["plants"])
            land += rows[str(d)]["land"]
        meta[cluster] = {"episode": pick["ep"], "bank": pick["bank"], "seed": pick["seed"],
                         "n_in_cluster": len(seasons), "n_on_dominant": len(pool),
                         "dominant_d3_d5": "".join(x[0] for x in dom),
                         "herd": dict(herd), "land": land, "plants": dict(crops)}
        print(f"{cluster:12} {len(seasons):>4} {''.join(x[0] for x in dom) or '-':>9} "
              f"{len(pool):>6} {pick['ep']:>11} {pick['bank']:>10,.0f}   "
              f"herd {dict(herd)} land {land}")
    (out_dir / "meta.json").write_text(json.dumps(
        {"source": "scripts/cluster_real_schedules.py", "submission": 56114097,
         "rows": "LANDED", "clusters": meta}, indent=2))
    print(f"\nwrote {out_dir}/*.json")


if __name__ == "__main__":
    main()
