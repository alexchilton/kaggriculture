"""How many of kawa's trades did the BC learn as "do nothing"?

    python -u scripts/count_what_the_bc_vocab_could_not_say.py --games 40

`kagg/il/bc.py:235` labels with `replays.encode_action(action, J.MAX_UNITS)` -- **no vocab
argument** -- against a function whose docstring says "Pass it." It therefore falls back to
`MB.load_vocab()`, the 197-entry `data/il/bundle_vocab.json` built from LEADERBOARD games rather
than from this teacher.

`Vocabulary.index` returns 0 for an unknown basket and 0 means "place no orders". So every kawa
trade outside that vocabulary was taught to the student as DO NOTHING -- and bundle agreement scores
it as a hit, because the student then obediently emits nothing too. Measured on the four tape
teachers in 2026-08-22 that was 179 of 1451 traded turns, 12.3%, containing 512 HIRE and 444 SELL
orders, the entire opening among them
(`docs/the_vocabulary_labels_the_opening_as_nothing_2026-08-22.md`).

`encode_action` returns `w_bundle_miss` so a caller can count exactly this. `build_rows` drops it --
the cached npz has `w_qty_sell`, `w_qty_buy_product`, `w_qty_buy_seed` and no `w_bundle_miss` -- so
for `data/bc_rows_kawa.npz` the number was never taken.

This takes it. No environment stepping: the recorded action stream is enough to say which baskets
the vocabulary can express, which is the whole question.
"""
import argparse
import collections
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="カワシギ")
    ap.add_argument("--games", type=int, default=40)
    ap.add_argument("--vocabs", nargs="*", default=["data/il/bundle_vocab.json",
                                                    "data/il/bundle_vocab_planner.json",
                                                    "data/il/bundle_vocab_teacher_pre_topup.json"])
    args = ap.parse_args()

    from kagg.il import bc, market_bundles as MB

    vocabs = {}
    for p in args.vocabs:
        path = REPO / p
        if not path.exists():
            continue
        bundles = json.loads(path.read_text())
        vocabs[p] = (MB.Vocabulary.from_bundles(
            [tuple(tuple(x) for x in b) for b in bundles], max_size=None), len(bundles))

    refs = bc.rank_seats(bc.find_replays("data"), team=args.team)[: args.games]
    print(f"{len(refs)} {args.team} seats, banks ${refs[-1].bank:,.0f}-${refs[0].bank:,.0f}\n")

    traded = 0
    miss = {k: 0 for k in vocabs}
    miss_orders = {k: collections.Counter() for k in vocabs}
    for r in refs:
        doc = json.loads(pathlib.Path(r.path).read_text())
        for step in doc["steps"][1:]:
            orders = ((step[r.seat] or {}).get("action") or {}).get("market") or []
            orders = [o for o in orders if o]
            if not orders:
                continue
            traded += 1
            shape = MB.bundle_of(orders)
            for k, (v, _n) in vocabs.items():
                if int(v.index(shape)) == 0:
                    miss[k] += 1
                    for o in orders:
                        miss_orders[k][o[0]] += 1

    print(f"{'vocabulary':<46}{'size':>6}{'traded turns':>14}{'MISSED':>9}{'rate':>8}")
    for k, (_v, n) in vocabs.items():
        print(f"  {k:<44}{n:>6}{traded:>14,}{miss[k]:>9,}{miss[k] / max(1, traded):>8.1%}")

    for k in vocabs:
        if not miss[k]:
            continue
        top = ", ".join(f"{op} {c:,}" for op, c in miss_orders[k].most_common(6))
        print(f"\n  {k}\n    orders taught as DO NOTHING: {top}")

    print("\nWHAT THIS MEANS")
    worst = "data/il/bundle_vocab.json"
    if worst in miss and traded:
        rate = miss[worst] / traded
        print(f"  data/bc_rows_kawa.npz was labelled with {worst}.")
        print(f"  {rate:.1%} of kawa's traded turns are unlearnable in it, and bundle agreement")
        print("  scores every one of them as a HIT. The market head of that checkpoint cannot be")
        print("  trusted, and a hybrid built on it would be built on the wrong number.")


main()
