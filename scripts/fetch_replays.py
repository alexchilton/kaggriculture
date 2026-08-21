"""Download episode replays for imitation learning, from the daily episode datasets.

`kaggle/kaggriculture-episodes-index` lists a dataset per day. The two published so far:

    2026-07-30   864 episodes   13.6 GB   top avg score 1152
    2026-07-31   928 episodes   21.4 GB   top avg score 1427

**Those scores are the reason this is worth the bandwidth.** Our agents sit around 600, a friend's
heuristic scores 1230, and the top of 2026-07-31 averages 1427. The teachers in these files play a
game we have never played.

The whole 35 GB is not wanted and mostly not useful -- a replay of two mediocre agents teaches a
mediocre policy. Files are one JSON per episode named `<episode_id>.json`, so they can be pulled
individually and kept only when the winner banked enough to be worth imitating. Anything already in
`data/` is skipped, so this is resumable and safe to interrupt.

Run:  .venv/bin/python -u scripts/fetch_replays.py 80 2>&1 | tee data/logs/fetch.log
"""

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

OUT = Path(os.environ.get("OUT_DIR", "data"))
INDEX = "kaggle/kaggriculture-episodes-index"
# Newest first: the later day has the stronger field, so its episodes are the better teachers.
#
# **These go stale silently and that is the whole risk here.** They read 2026-07-31/07-30 until
# 2026-08-15, by which point Kaggle had published every day up to 2026-08-14 -- so a "fresh" pull
# was quietly re-reading a two-week-old field that predates the 1.32.6 town rebalance AND the
# 1.32.7 hinge change. Episodes from before 2026-08-08 describe a different economy and are not
# teachers, they are noise. `kaggle datasets list -s kaggriculture-episodes-2026-08` lists what
# actually exists; update this before every pull rather than trusting it.
#: Updated 2026-08-21. `kaggle datasets list -s kaggriculture-episodes-2026-08` shows 08-01 through
#: 08-20 published. The previous pin (08-16/15/14) was five days stale, exactly as the note above
#: predicts -- and checking it is one command, so check it before every pull.
DATASETS = ("kaggle/kaggriculture-episodes-2026-08-20",
            "kaggle/kaggriculture-episodes-2026-08-19",
            "kaggle/kaggriculture-episodes-2026-08-18")

# A replay is only worth keeping if the winner played well. `contrarian` banks ~$51k and the pair in
# 89197802 banked $106k and $113k, so this keeps the ones with something to teach and discards the
# ones that would just dilute the dataset.
MIN_WINNER_BANK = float(os.environ.get("MIN_WINNER_BANK", 60_000.0))


def existing_ids():
    ids = set()
    for p in OUT.glob("*.json"):
        stem = p.stem.replace("episode-", "").replace("-replay", "")
        if stem.isdigit():
            ids.add(stem)
    return ids


def iter_names(api, dataset, limit):
    """Walk the paginated file listing, yielding episode file names."""
    token, seen = None, 0
    while seen < limit:
        page = api.dataset_list_files(dataset, page_token=token, page_size=200)
        names = [f.name for f in page.files]
        if not names:
            return
        for n in names:
            yield n
            seen += 1
            if seen >= limit:
                return
        token = page.next_page_token
        if not token:
            return


def fetch(n_target=80):
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()

    have = existing_ids()
    print(f"{len(have)} replays already on disk; want {n_target} more", flush=True)

    kept = skipped = 0
    for dataset in DATASETS:
        if kept >= n_target:
            break
        print(f"\n{dataset}", flush=True)
        for name in iter_names(api, dataset, limit=n_target * 4):
            if kept >= n_target:
                break
            eid = Path(name).stem
            if eid in have:
                continue
            tmp = Path(tempfile.mkdtemp())
            try:
                api.dataset_download_file(dataset, name, path=str(tmp), force=True)
                got = next(iter(list(tmp.glob("*.json")) + list(tmp.glob("*.zip"))), None)
                if got is None:
                    continue
                if got.suffix == ".zip":
                    shutil.unpack_archive(str(got), str(tmp))
                    got = next(iter(tmp.glob("*.json")), None)
                    if got is None:
                        continue

                rewards = json.loads(got.read_text())["steps"][-1]
                banks = [p.get("reward") or 0.0 for p in rewards]
                if max(banks) < MIN_WINNER_BANK:
                    skipped += 1
                    print(f"  skip {eid}: winner only ${max(banks):,.0f}", flush=True)
                    continue

                shutil.move(str(got), str(OUT / f"{eid}.json"))
                have.add(eid)
                kept += 1
                print(f"  keep {eid}: ${banks[0]:,.0f} / ${banks[1]:,.0f}  ({kept}/{n_target})",
                      flush=True)
            except Exception as exc:                              # noqa: BLE001
                print(f"  {eid} failed: {type(exc).__name__}: {str(exc)[:90]}", flush=True)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
            time.sleep(0.3)

    print(f"\ndone: kept {kept}, skipped {skipped} as too weak; {len(existing_ids())} on disk")


if __name__ == "__main__":
    fetch(int(sys.argv[1]) if len(sys.argv) > 1 else 80)
