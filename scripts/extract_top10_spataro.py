"""Pull SpaTaro's seasons out of the top-10 replay archive, streaming.

`ashok205/kaggriculture-top10-replay-archive` holds every top-10 episode per day as one
parquet row per episode: `episode_id` plus the whole 33 MB replay as a string. 500 rows a
shard, so the file must be walked row group by row group -- reading one shard whole is
~16 GB.

Only 2026-09-09 by default. He last submitted 2026-09-09 05:04, so 09-07 and 09-08
episodes are a DIFFERENT agent, and our existing 62-season set mixes them.

Writes one compact record per season: unlock history, bank, and the 719 actions.
"""
import argparse, json
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
TEAM = "SpaTaro"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dates", nargs="+", default=["2026-09-09"])
    ap.add_argument("--out", default="data/spataro_seasons.json")
    args = ap.parse_args()

    out, seen = [], set()
    for date in args.dates:
        path = ROOT / "data" / "top10" / f"replays_{date}.parquet"
        if not path.exists():
            print(f"missing {path}", flush=True)
            continue
        f = pq.ParquetFile(path)
        print(f"{path.name}: {f.metadata.num_rows} rows, "
              f"{f.metadata.num_row_groups} row groups", flush=True)
        for g in range(f.metadata.num_row_groups):
            tbl = f.read_row_group(g)
            for row in tbl.to_pylist():
                ep = row["episode_id"]
                if ep in seen:
                    continue
                r = json.loads(row["replay_json"])
                names = r.get("info", {}).get("TeamNames") or []
                if TEAM not in names:
                    continue
                seen.add(ep)
                seat = names.index(TEAM)
                steps = r["steps"]
                shops, unlocks = [], []
                for i, s in enumerate(steps):
                    for x in ((s[seat]["observation"].get("town") or {}).get("unlocked_shops") or []):
                        if x not in shops:
                            shops.append(x)
                            unlocks.append([i // 24, x])
                out.append({"ep": ep, "date": date, "seat": seat,
                            "opponent": names[1 - seat],
                            "bank": r["rewards"][seat],
                            "seed": r["info"].get("seed"),
                            "unlocks": unlocks,
                            "stream": [s[seat].get("action") for s in steps[1:]]})
                if len(out) % 20 == 0:
                    print(f"  {len(out)} seasons", flush=True)
            del tbl
    p = ROOT / args.out
    p.write_text(json.dumps(out, separators=(",", ":")))
    print(f"\n{len(out)} {TEAM} seasons -> {p}  ({p.stat().st_size/1e6:.0f} MB)")
    if out:
        banks = sorted(x["bank"] for x in out)
        print(f"bank: min {banks[0]:,.0f} p50 {banks[len(banks)//2]:,.0f} max {banks[-1]:,.0f}")


if __name__ == "__main__":
    main()
