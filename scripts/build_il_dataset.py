"""Turn the downloaded replays into a supervised dataset for behaviour cloning.

Features come from `adapter.state_from_obs` followed by the *same* `jax_obs.encode` the policy
trains on, so the network sees in training exactly the tensors it will see in play. Building a
second encoder that goes straight from dicts to features would create two things that must agree
forever, and this project has already been bitten twice by exactly that.

Only the winning seat is kept. A replay contains one agent worth imitating and one worth beating,
and they are equally represented in the file.

Stored as float16 shards: 112k turns of `[100, 25] + [24, 16] + [57]` is 1.3 GB in float32 and
660 MB in half, and the observation is counts and small integers that half represents exactly.

Run:  .venv/bin/python -u scripts/build_il_dataset.py 2>&1 | tee data/logs/il_dataset.log
"""

import sys
import time
from pathlib import Path

import numpy as np

from kagg.il import replays
from kagg.rl import adapter, jax_obs

OUT = Path("data/il")
SHARD = 20_000


def build(pattern="*.json", shard_size=SHARD, min_bank=60_000.0):
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in Path("data").glob(pattern) if p.stem.replace(
        "episode-", "").replace("-replay", "").isdigit())
    print(f"{len(files)} replays", flush=True)

    tiles_b, units_b, glob_b, labels_b = [], [], [], {}
    n_kept = n_files = shard = 0
    started = time.time()

    def flush():
        nonlocal tiles_b, units_b, glob_b, labels_b, shard
        if not tiles_b:
            return
        path = OUT / f"shard_{shard:03d}.npz"
        np.savez_compressed(
            path,
            tiles=np.asarray(tiles_b, dtype=np.float16),
            units=np.asarray(units_b, dtype=np.float16),
            glob=np.asarray(glob_b, dtype=np.float16),
            **{f"y_{k}": np.asarray(v, dtype=np.int16) for k, v in labels_b.items()},
        )
        print(f"  wrote {path.name}: {len(tiles_b)} rows", flush=True)
        tiles_b, units_b, glob_b, labels_b = [], [], [], {}
        shard += 1

    for path in files:
        try:
            summary = replays.replay_summary(path)
        except Exception as exc:                                    # noqa: BLE001
            print(f"  {path.name}: unreadable ({type(exc).__name__})", flush=True)
            continue
        if max(summary["rewards"]) < min_bank:
            continue
        n_files += 1

        for obs, priv, action, seat in replays.iter_turns(path):
            try:
                state = adapter.state_from_obs(obs, priv)
                t, u, g = jax_obs.encode(state)
            except Exception:                                       # noqa: BLE001
                continue
            # `encode` returns [1, 2, ...]; keep the winner's seat only.
            tiles_b.append(np.asarray(t[0, seat]))
            units_b.append(np.asarray(u[0, seat]))
            glob_b.append(np.asarray(g[0, seat]))
            for k, v in replays.encode_action(action, n_units=len(obs["farms"][seat]
                                                                 .get("hands", [])) + 1).items():
                labels_b.setdefault(k, []).append(v)
            n_kept += 1
            if len(tiles_b) >= shard_size:
                flush()

        rate = n_kept / max(1e-9, time.time() - started)
        print(f"  {path.name}: {n_kept:,} rows total ({rate:.0f}/s, {n_files} files)", flush=True)

    flush()
    print(f"\n{n_kept:,} rows from {n_files} replays in {shard} shards, "
          f"{time.time() - started:.0f}s", flush=True)


if __name__ == "__main__":
    build(shard_size=int(sys.argv[1]) if len(sys.argv) > 1 else SHARD)
