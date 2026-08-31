"""Which of the teacher's own actions can the representation not express? Per tape.

    python -u scripts/audit_what_the_teacher_cannot_be_taught.py

Alex, 2026-08-27: *"those 2 separate arms must have a bug if not the 72 on 64 max then something
else similar, if it works on 2 arms already"*.

The reasoning is the repo's own: two tapes replay at 98-99% and two collapse, on an IDENTICAL start
board. That is not what a capacity limit looks like. It is what an unlearnable LABEL looks like --
and this project has now been bitten by that three times:

  * a 197-entry bundle vocabulary silently marked 12.3% of a teacher's trades EMPTY, and the student
    learned to do nothing (`project_kaggriculture_vocab_blanked_the_opening`);
  * 7 of 104 DIG labels target an already-empty tile, are masked, and cap DIG at 0.933 forever
    (`docs/the_clone_only_misses_the_unlearnable_digs_2026-08-23.md`);
  * `MAX_QTY = 64` cannot name the day-29 `SELL WHEAT 72` that all four tapes make.

So: encode every teacher action and decode it back BEFORE reasoning about the net. Anything that does
not survive the round trip is a label no amount of training can reach, and it is reported per tape so
it can be lined up against which tapes actually fail.

Reports, per tape:
    turns          turns with any market order
    not in vocab   the bundle is absent from the checkpoint's vocabulary -> decodes as something else
    qty capped     an order above MAX_QTY - 1 -> silently truncated
    lost orders    orders present in the teacher's action and missing after the round trip
    added orders   orders the round trip invents
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))


def _orders(action):
    c = collections.Counter()
    for o in (action or {}).get("market") or []:
        if o:
            c[tuple(str(z) for z in o)] += 1
    return c


def _seated(labels):
    """`encode_action` gives per-unit arrays; `decode_action` indexes a leading SEAT axis first
    (`kagg/agents/neural.py:94`). Duplicate every entry onto two seats so seat 0 reads back what was
    encoded."""
    import numpy as np
    out = {}
    for k, v in labels.items():
        a = np.asarray(v)
        out[k] = np.stack([a, a]) if a.ndim else np.asarray([a, a])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="data/dagger_tape/season_fast-20260822-235031")
    ap.add_argument("--ckpt", default="pinned_round27.pkl")
    ap.add_argument("--show", type=int, default=8)
    args = ap.parse_args()

    import pickle

    import dagger_tape as DT
    from kagg.agents import neural as NEURAL
    from kagg.il import market_bundles as MB
    from kagg.il import replays as RP
    from kagg.rl import jax_policy as P

    with (pathlib.Path(args.run) / args.ckpt).open("rb") as fh:
        ckpt = pickle.load(fh)
    want = ckpt.get("vocab_size")
    vocab_path = None
    for c in ((ckpt.get("args") or {}).get("vocab"),
              str(REPO / "data/il/bundle_vocab_teacher_pre_topup.json"),
              str(REPO / "data/il/bundle_vocab_teacher.json"),
              str(REPO / "data/il/bundle_vocab.json")):
        if c and pathlib.Path(c).exists() and len(json.loads(pathlib.Path(c).read_text())) == want:
            vocab_path = c
            break
    if vocab_path is None:
        raise SystemExit(f"no vocabulary on disk holds {want} bundles")
    bundles = json.loads(pathlib.Path(vocab_path).read_text())
    vocab = MB.Vocabulary.from_bundles([tuple(tuple(p) for p in b) for b in bundles],
                                       max_size=P.N_BUNDLES)
    print(f"{args.ckpt} round {ckpt.get('round')}   vocab {pathlib.Path(vocab_path).name} "
          f"({want} bundles)   MAX_QTY {P.MAX_QTY}")

    print(f"\n{'tape':<16}{'turns':>7}{'no vocab':>10}{'qty capped':>12}"
          f"{'lost':>7}{'added':>7}")
    detail = []
    for spec in DT.tape_games():
        doc = json.loads((REPO / spec["tape_path"]).read_text())
        seat = spec["seat"]
        turns = miss = capped = lost = added = 0
        examples = []
        for t, step in enumerate(doc["steps"][1:]):
            act = ((step[seat] or {}).get("action") or {})
            want_orders = _orders(act)
            if not want_orders:
                continue
            turns += 1
            n_units = 1 + len(act.get("hands") or [])

            for o in act.get("market") or []:
                if o and len(o) > 2 and int(o[2]) > P.MAX_QTY - 1:
                    capped += 1

            labels = RP.encode_action(act, n_units, vocab=vocab)
            bidx = int(labels["bundle"])
            if bidx == 0 and want_orders:
                miss += 1
                if len(examples) < args.show:
                    examples.append(f"    turn {t + 1:>3} day {(t + 1) // 24:>2}  "
                                    f"NOT IN VOCAB  {sorted(want_orders.elements())}")

            # `encode_action` returns per-unit arrays; `decode_action` indexes a leading SEAT axis
            # first (`neural.py:94`). Duplicate onto two seats and read seat 0.
            got = _orders(NEURAL.decode_action(_seated(labels), n_units, vocab, seat=0))
            for k, n in want_orders.items():
                if got.get(k, 0) < n:
                    lost += n - got.get(k, 0)
            for k, n in got.items():
                if want_orders.get(k, 0) < n:
                    added += n - want_orders.get(k, 0)

        print(f"{spec['name'][:15]:<16}{turns:>7}{miss:>10}{capped:>12}{lost:>7}{added:>7}")
        detail.append((spec["name"], examples))

    for name, ex in detail:
        if ex:
            print(f"\n{name}:")
            for e in ex:
                print(e)


main()
