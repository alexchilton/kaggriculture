"""Boil a day of ladder episodes down to one compact row per seat, in parallel.

A day's dataset is ~686 replays and 20 GB of JSON. Everything worth knowing about a seat is a few
hundred bytes, so this extracts once and writes JSONL that the actual analysis can read in a second.

What each row carries, and why:

- **Everything ending `_offered`** -- `sell_offered`, `buy_offered`, `seed_offered`,
  `animals_offered`, `plant_ops` -- is what the seat ASKED FOR, summed over turns. An agent that
  re-posts a standing quota until it fills contributes the same intention up to 24 times a day, and
  ours does exactly that. These fields used to be called `sell`, `buy`, `seed`, `animals` and
  `plants`, with the warning in this docstring and nowhere else; the name is what travels into a
  table, so the name now says what the number is. `plant_ops` is in the list because a PLANT is
  dropped wholesale when the atomic rule bites, so even a unit op is a request.

- **`plants_real`, `seed_fills`, `sold`, `bought`, `hires`, `land`, `herd`** -- what actually
  happened, from `kagg/analysis/replay_fills.py`. Plants are tile transitions, seed purchases come
  off the closed `private["seeds"]` ledger, hires off `hires_today` and parcels off
  `unlocked_quadrants`; all four are exact. `sold` and `bought` reconcile the shed against the
  market inventory and are LOWER BOUNDS, with `shared_sold` holding volume both sides traded on the
  same turn. See that module for what each bound is made of.

- **`orders` / `order_turns`** -- the re-posting tell, kept as corroboration. An agent whose
  `orders` far exceeds `order_turns` is holding a standing quota open. Ours re-posts on all 24 turns
  of a day; Victor does not.

- **`sell_turns` / `buy_turns`** -- the turn index of every market order, so cadence and TIMING can
  be read off without re-parsing 26 MB.

- **`shops`** -- read from the final observation, so it is the full season's draw.

- **`act_sig`** -- a hash of the whole 720-turn action sequence for this seat. Two games by the same
  player with the same signature are the same script. This is how open-loop is detected without
  holding two full replays in memory at once.

- **`day_sig`** -- per-day hashes, so a pair of games can be compared for the day they diverge.

    python -u scripts/episode_index.py --src <dir> --out data/episodes_2026-08-10.jsonl --workers 10
"""

import argparse
import collections
import hashlib
import json
import logging
import multiprocessing
import pathlib
import sys

sys.path.insert(0, ".")

from kagg.analysis.replay_fills import (animals_alive, hires, land, real_plants,
                                        seed_fills, trade_fills)
from kagg.logs import get_logger

TPD = 24

#: **Named at import, handled in `main()` only.** This module is re-imported inside every
#: multiprocessing worker, and attaching a `FileHandler` there gives N processes an open handle on
#: one file and prints "logging to ..." N times. `get_logger` returns `logging.getLogger(name)`, so
#: this is the same object the parent later attaches handlers to -- a worker just gets a quiet one.
log = logging.getLogger(__name__)


def one(path):
    """One replay -> a row per seat. Returns [] on anything malformed rather than raising."""
    try:
        d = json.loads(pathlib.Path(path).read_text())
    except Exception:                                                       # noqa: BLE001
        return []
    names = (d.get("info") or {}).get("TeamNames") or []
    rewards = d.get("rewards") or []
    steps = d.get("steps") or []
    if len(names) != 2 or len(rewards) != 2 or not steps:
        return []
    cfg = d.get("configuration") or {}
    last = (steps[-1][0] or {}).get("observation") or {}
    shops = sorted(collections.Counter((last.get("town") or {})
                                       .get("unlocked_shops") or []).items())
    # One reconciliation for the whole file rather than one per seat: it walks every step once.
    fills = trade_fills(d)
    out = []
    for seat in (0, 1):
        plant_ops, seed, buy, sell, animals = (collections.Counter() for _ in range(5))
        sell_turns, buy_turns, animal_turns, plant_turns = [], [], [], []
        orders = 0
        order_turns = set()
        per_day = collections.defaultdict(list)
        for t, st in enumerate(steps):
            a = st[seat].get("action") if seat < len(st) else None
            if not a:
                continue
            per_day[t // TPD].append(json.dumps(a, sort_keys=True))
            for u in [a.get("farmer")] + list(a.get("hands") or []):
                if u and u[0] == "PLANT" and len(u) > 1:
                    plant_ops[u[1]] += 1
                    plant_turns.append(t)
            for o in (a.get("market") or []):
                if not o:
                    continue
                orders += 1
                order_turns.add(t)
                n = int(o[2]) if len(o) > 2 and str(o[2]).lstrip("-").isdigit() else 1
                if o[0] == "SELL":
                    sell[o[1]] += n
                    sell_turns.append((t, o[1], n))
                elif o[0] == "BUY_PRODUCT":
                    buy[o[1]] += n
                    buy_turns.append((t, o[1], n))
                elif o[0] == "BUY_SEED":
                    seed[o[1]] += n
                elif o[0] == "BUY_ANIMAL":
                    animals[o[1]] += n
                    animal_turns.append((t, o[1], n))
        allacts = [x for day in sorted(per_day) for x in per_day[day]]
        out.append(dict(
            episode=pathlib.Path(path).stem, seat=seat, name=names[seat],
            reward=float(rewards[seat] or 0), shops=shops,
            weeds=float(cfg.get("weedSpawnChance", 0) or 0),
            interval=cfg.get("townCenterSellInterval"),
            plant_ops=dict(plant_ops), seed_offered=dict(seed),
            animals_offered=dict(animals), buy_offered=dict(buy), sell_offered=dict(sell),
            plants_real=dict(real_plants(d, seat)), seed_fills=dict(seed_fills(d, seat)),
            sold=dict(fills.sold[seat]), bought=dict(fills.bought[seat]),
            shared_sold=dict(fills.shared_sold), shared_bought=dict(fills.shared_bought),
            unresolved_sold=dict(fills.unresolved_sold),
            unresolved_bought=dict(fills.unresolved_bought),
            floored=sorted(fills.floored),
            hires=hires(d, seat), land=land(d, seat), herd=dict(animals_alive(d, seat)),
            shed_readable=round(fills.coverage(seat), 3),
            orders=orders, order_turns=len(order_turns),
            sell_turns=sell_turns, buy_turns=buy_turns, animal_turns=animal_turns,
            first_plant=min(plant_turns) if plant_turns else None,
            act_sig=hashlib.md5("|".join(allacts).encode()).hexdigest()[:16],
            day_sig=[hashlib.md5("|".join(per_day[dd]).encode()).hexdigest()[:8]
                     for dd in sorted(per_day)],
        ))
    return out


def main():
    get_logger(__name__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    files = sorted(pathlib.Path(args.src).rglob("*.json"))
    if args.limit:
        files = files[:args.limit]
    log.info("%d replays -> %s on %d workers", len(files), args.out, args.workers)
    n = 0
    with open(args.out, "w") as fh, multiprocessing.Pool(args.workers) as pool:
        for i, rows in enumerate(pool.imap_unordered(one, map(str, files), chunksize=2)):
            for r in rows:
                fh.write(json.dumps(r) + "\n")
                n += 1
            if (i + 1) % 50 == 0:
                log.info("%d/%d replays, %d seats", i + 1, len(files), n)
    log.info("done: %d seat rows from %d replays", n, len(files))


if __name__ == "__main__":
    main()
