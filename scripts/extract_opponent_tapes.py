"""Strip each pool opponent's recording down to the 720 actions the sweep actually reads.

A downloaded game is about 30 MB, almost all of it observations: every tile of both boards at every
one of 720 turns. `breakdown.tape_policy` reads exactly one thing out of it --
`steps[t][seat].action` -- and the twelve-opponent pool needs 1.13 GB of files on the box to
deliver about 8 MB of actions.

So this writes the thin form, one file per opponent:

    {"name": ..., "seat": ..., "source": ..., "economy": {...},
     "actions": [{"farmer": [...], "hands": [[...]], "market": [[...]]}, ...]}

`economy` carries `townCenterSellInterval` from the recording, because a tape replayed on a
different economy is fiction (`breakdown.env_config`) -- and once the 30 MB source is gone, that is
the only place left to read it from.

    python -u scripts/extract_opponent_tapes.py
    python -u scripts/extract_opponent_tapes.py --out data/opponent_tapes
"""

import argparse
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import breakdown as B                                                        # noqa: E402

POOL_FILE = REPO / "data/opponent_pool.json"


def thin(replay, seat):
    """`(actions, economy)` for one seat -- `steps[1:]`, since `steps[0]` is the reset state."""
    d = json.loads(pathlib.Path(replay).read_text())
    acts = []
    for frame in d["steps"][1:]:
        a = (frame[seat] or {}).get("action") or {} if len(frame) > seat else {}
        acts.append({"farmer": a.get("farmer") or ["PASS"],
                     "hands": list(a.get("hands") or []),
                     "market": list(a.get("market") or [])})
    cfg = d.get("configuration") or {}
    economy = {k: cfg[k] for k in B.ECONOMY_KEYS if cfg.get(k) is not None}
    return acts, economy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/opponent_tapes")
    ap.add_argument("--pool", default=str(POOL_FILE))
    args = ap.parse_args()

    out = REPO / args.out
    out.mkdir(parents=True, exist_ok=True)
    rows = json.loads(pathlib.Path(args.pool).read_text())
    total_src = total_dst = 0
    for r in rows:
        src = REPO / r["replay"]
        if not src.exists():
            print("  SKIP %-28s no file: %s" % (r["name"][:28], r["replay"]))
            continue
        acts, economy = thin(src, int(r["seat"]))
        # The filename must survive a shell and a Windows filesystem, so it is the game id and the
        # name lives inside the file. `カワシギ` as a filename is a transfer waiting to fail.
        dst = out / ("%s_seat%d.json" % (pathlib.Path(r["replay"]).stem, int(r["seat"])))
        payload = {"name": r["name"], "seat": int(r["seat"]), "source": r["replay"],
                   "melon_at_d3": r.get("melon_at_d3"), "economy": economy, "actions": acts}
        dst.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
        total_src += src.stat().st_size
        total_dst += dst.stat().st_size
        print("  %-28s %7.1f MB -> %6.2f MB   %s"
              % (r["name"][:28], src.stat().st_size / 1e6, dst.stat().st_size / 1e6, dst.name))
    print("\n%.1f MB -> %.1f MB  (%.0fx smaller)"
          % (total_src / 1e6, total_dst / 1e6, total_src / max(1, total_dst)))


if __name__ == "__main__":
    main()
