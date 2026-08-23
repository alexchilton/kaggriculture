"""Encode recorded opponent seats into a head-label array the JAX trainer can index by turn.

The RL trainer only knows the built-in heuristic roles, and those cap out around $15k. The tapes in
`data/opponent_tapes/` are real recorded players. This turns them into

    {head: int array [n_tapes, EPISODE_TURNS, ...]}

so a rollout can seat tape `i` at seat 1 and read its action for turn `t` with a gather -- no
Python in the jitted loop.

    python -u scripts/build_opponent_tape_actions.py --out data/il/opponent_tape_actions.npz
"""
import argparse
import json
import pathlib
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from kagg.il import market_bundles as MB, replays as RP        # noqa: E402

EPISODE_TURNS = 719


def seat_of(path):
    """`93801334_seat0.json` -> 0. The filename carries which seat was recorded."""
    stem = path.stem
    if "_seat" in stem:
        return int(stem.rsplit("_seat", 1)[1])
    return 0


def encode_tape(path, vocab):
    """One recorded seat -> {head: array}, padded/truncated to EPISODE_TURNS.

    These files are already-extracted action streams, not raw replays: `{name, seat, source,
    melon_at_d3, economy, actions}` with `actions` the per-turn list for that seat.
    """
    d = json.loads(path.read_text())
    actions = d.get("actions")
    if not actions:
        return None
    per_turn = []
    for action in actions[:EPISODE_TURNS]:
        action = action or {}
        n_units = 1 + len(action.get("hands") or [])
        per_turn.append(RP.encode_action(action, n_units, vocab=vocab))
    if not per_turn:
        return None
    # **Take every head, including the 0-d ones.** `encode_action` returns `bundle` as a numpy
    # `int32` scalar, which is not an `ndarray`, so an `isinstance(v, np.ndarray)` filter dropped it
    # in silence. The bundle names WHICH products carry an order; the per-product quantities beside
    # it are inert without it. A tape opponent built from a bundle-less file farms all season and
    # never trades a unit -- and reads as a working opponent while doing it.
    heads = list(per_turn[0])
    out = {}
    for h in heads:
        stacked = np.stack([np.asarray(p[h]) for p in per_turn])
        if len(stacked) < EPISODE_TURNS:                       # pad with the last turn
            pad = np.repeat(stacked[-1:], EPISODE_TURNS - len(stacked), axis=0)
            stacked = np.concatenate([stacked, pad])
        out[h] = stacked
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tapes", default=str(REPO / "data/opponent_tapes"))
    ap.add_argument("--vocab", default=str(REPO / "data/il/bundle_vocab_teacher.json"))
    ap.add_argument("--out", default=str(REPO / "data/il/opponent_tape_actions.npz"))
    args = ap.parse_args()

    vocab = MB.load_vocab(args.vocab)
    paths = sorted(pathlib.Path(args.tapes).glob("*.json"))
    print("tapes found: %d" % len(paths), flush=True)

    encoded, names = [], []
    for p in paths:
        try:
            e = encode_tape(p, vocab)
        except Exception as exc:                               # a malformed tape must not kill the set
            print("  SKIP %-28s %s" % (p.name, exc))
            continue
        if e is None:
            print("  SKIP %-28s no actions" % p.name)
            continue
        encoded.append(e)
        names.append(p.stem)
        print("  ok   %-28s heads %s" % (p.name, sorted(e)))

    if not encoded:
        raise SystemExit("no tapes encoded")

    heads = sorted(encoded[0])
    bundle = {h: np.stack([e[h] for e in encoded]) for h in heads}
    np.savez_compressed(args.out, names=np.array(names), **bundle)
    print()
    print("wrote %s" % args.out)
    for h in heads:
        print("  %-14s %s" % (h, bundle[h].shape))


if __name__ == "__main__":
    main()
