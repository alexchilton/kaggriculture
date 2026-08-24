"""Scan EVERY replay under data/seed_scripts for CARROT drain, any seat.

GAP 1 (docs/carrot_drain_gaps_2026-08-24.md, task from the orchestrating agent): the curated
subset used by does_anyone_read_the_carrot_drain.py never showed drain 7-10. This scans the WHOLE
corpus, both seats, and also records whether "alex chilton" is present and whether we won
(top-level `rewards`, higher = win), so gap 2 (won games) can be pulled from the same pass.

Drain formula matches does_anyone_read_the_carrot_drain.py: a shop selling ONLY carrot drains 2
per tick, any other carrot-carrying shop drains 1. Computed at the last available step (day 29 if
the episode ran that long, else the final step), same as the reference script.

Writes one row per (file, seat) to a CSV, flushed per file, so a kill loses at most one file.
"""
import glob
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "reference"))

TPD = 24
US = "alex chilton"


def shops():
    import kaggriculture as KG
    return KG.SHOPS


def carrot_drain(obs, shop_table):
    d = 0
    for name in ((obs.get("town") or {}).get("unlocked_shops") or []):
        ps = shop_table.get(name) or []
        if "CARROT" in ps:
            d += 2 if len(ps) == 1 else 1
    return d


def main():
    out = REPO / "data/logs/full_corpus_drain_scan.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fh = out.open("w")
    fh.write("file,episode,seed,seat,team,drain,is_us,us_reward,them_reward,us_won\n")
    fh.flush()

    shop_table = shops()
    files = sorted(set(glob.glob(str(REPO / "data/seed_scripts/**/*.json"), recursive=True)))
    print(f"{len(files)} files to scan", flush=True)

    t0 = time.time()
    n_ok = n_bad = 0
    drain_counter = {}
    for i, f in enumerate(files):
        p = pathlib.Path(f)
        try:
            rec = json.loads(p.read_text())
        except Exception as e:                                              # noqa: BLE001
            n_bad += 1
            fh.write(f"{p.name},PARSE_ERROR,,,,,,,,\n")
            fh.flush()
            continue
        if not isinstance(rec, dict) or "steps" not in rec or "info" not in rec:
            n_bad += 1
            continue
        names = (rec.get("info") or {}).get("TeamNames") or []
        seed = (rec.get("info") or {}).get("seed")
        episode = (rec.get("info") or {}).get("EpisodeId") or p.stem
        steps = rec["steps"]
        rewards = rec.get("rewards") or [None] * len(names)
        t = min(29 * TPD, len(steps) - 1)
        for seat, who in enumerate(names):
            try:
                obs = steps[t][seat]["observation"]
            except Exception:                                               # noqa: BLE001
                continue
            dr = carrot_drain(obs, shop_table)
            drain_counter[dr] = drain_counter.get(dr, 0) + 1
            is_us = who == US
            us_r = rewards[seat] if seat < len(rewards) else None
            them_r = rewards[1 - seat] if (1 - seat) < len(rewards) else None
            won = ""
            if is_us and us_r is not None and them_r is not None:
                won = int(us_r > them_r)
            fh.write(f"{p.name},{episode},{seed},{seat},{who},{dr},{int(is_us)},"
                     f"{us_r},{them_r},{won}\n")
            if dr >= 7:
                fh.flush()
                print(f"  DRAIN {dr}: {p.name}  seat {seat} ({who})  seed {seed}", flush=True)
        n_ok += 1
        if (i + 1) % 100 == 0:
            fh.flush()
            print(f"  ...{i + 1}/{len(files)}  ({time.time() - t0:.0f}s)", flush=True)
    fh.close()
    print(f"\ndone: {n_ok} parsed, {n_bad} skipped/bad, {time.time() - t0:.0f}s", flush=True)
    print("drain histogram (per seat-row):", flush=True)
    for d in sorted(drain_counter):
        print(f"  drain {d:>2}: {drain_counter[d]}", flush=True)
    print(f"rows -> {out}", flush=True)


if __name__ == "__main__":
    main()
